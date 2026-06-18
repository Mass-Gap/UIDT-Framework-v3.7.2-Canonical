"""
AG-Eval Outcomes — Decision Rules O1–O5 (Sec. 7)
==================================================
Decision rules applied AFTER scoring and null controls:

O1: Modal [1]          → H0 confirmed, PR-B1 FAILS
O2: Modal [1:1], [1:1:1], or any equal-block class → H0 variant
O3: [1:2:3] modal >= 0.5, >= 2 adjacent alpha, all N >= 24,
    both arms (M0 + M1 if available), hot/cold consistent
                       → CANDIDATE SIGNAL [D]
O4: Multi-target or UNCLASSIFIED > 0.5 grid-wide → NON-DISCRIMINATIVE
O5: Detector gate fails → ABORT

Default                → O4 (NON-DISCRIMINATIVE)

Priority: O5 > O4 > O3 > O2 > O1.
(O5 checked first, then O4, then O3 signal criteria, then O2/O1.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..config import (
    CANDIDATE_SET_P,
    N_LADDER,
    ALPHA_TILDE_VALUES,
    O3_MIN_FREQUENCY,
    O3_MIN_ADJACENT_ALPHA,
    O3_MIN_N,
    O3_UNCLASSIFIED_MAX_FRACTION,
    GridCell,
)
from .null_controls import (
    MultiTargetResult,
    HotColdResult,
)
from .scoring import ClassLabel
from .validation import ValidationReport


# ── Outcome codes ───────────────────────────────────────────────────────────

class Outcome:
    """Symbolic outcome constants."""
    O1 = "O1"  # H0 confirmed
    O2 = "O2"  # H0 variant
    O3 = "O3"  # Candidate signal [D]
    O4 = "O4"  # Non-discriminative
    O5 = "O5"  # Abort (detector gate failure)


OUTCOME_DESCRIPTIONS: dict[str, str] = {
    Outcome.O1: "H0 CONFIRMED — PR-B1 FAILS",
    Outcome.O2: "H0 VARIANT — Equal-block partition dominant",
    Outcome.O3: "CANDIDATE SIGNAL [D] — [1:2:3] modal across required window",
    Outcome.O4: "NON-DISCRIMINATIVE — Multi-target / high UNCLASSIFIED rate",
    Outcome.O5: "ABORT — Detector validation gate failed",
}

# Equal-block classes → O2
_EQUAL_BLOCK_CLASSES: frozenset[str] = frozenset({
    "[1]", "[1:1]", "[1:1:1]", "[1:1:1:1]",
})

# O3 target class
_O3_TARGET: str = "[1:2:3]"


# ── Data structures ─────────────────────────────────────────────────────────

@dataclass
class CellResult:
    """Aggregated scoring result for a single grid cell."""
    cell: GridCell
    modal_class: ClassLabel
    modal_frequency: float
    class_counts: dict[str, int]
    flags: list[str] = field(default_factory=list)
    # Flags: "UNDERSAMPLED", "METASTABLE", "UNCLASSIFIED"
    hot_cold: Optional[HotColdResult] = None


@dataclass
class OutcomeDecision:
    """The final decision for the protocol."""
    outcome: str                 # O1..O5
    description: str
    evidence: dict[str, object] = field(default_factory=dict)
    # evidence contains the reasoning chain leading to the decision


# ── O5: Detector gate ──────────────────────────────────────────────────────

def check_o5(validation_report: ValidationReport) -> Optional[OutcomeDecision]:
    """Check O5: detector validation gate failure → ABORT."""
    if not validation_report.gate_passed:
        return OutcomeDecision(
            outcome=Outcome.O5,
            description=OUTCOME_DESCRIPTIONS[Outcome.O5],
            evidence={
                "n_failures": len(validation_report.failures),
                "failures": [
                    {
                        "class": f.class_label,
                        "N": f.N,
                        "epsilon": f.epsilon,
                        "recovery": f.recovery_rate,
                        "threshold": f.threshold,
                    }
                    for f in validation_report.failures
                ],
            },
        )
    return None


# ── O4: Non-discriminative ─────────────────────────────────────────────────

def check_o4(
    cell_results: list[CellResult],
    multi_target: MultiTargetResult,
) -> Optional[OutcomeDecision]:
    """Check O4: multi-target false positive OR high UNCLASSIFIED rate.

    O4 if:
      - multi_target.is_non_discriminative, OR
      - fraction of cells with UNCLASSIFIED modal > O3_UNCLASSIFIED_MAX_FRACTION
    """
    evidence: dict[str, object] = {}

    if multi_target.is_non_discriminative:
        evidence["multi_target"] = {
            "is_non_discriminative": True,
            "offending_classes": multi_target.offending_classes,
        }
        return OutcomeDecision(
            outcome=Outcome.O4,
            description=OUTCOME_DESCRIPTIONS[Outcome.O4],
            evidence=evidence,
        )

    # Grid-wide UNCLASSIFIED fraction
    n_total = len(cell_results)
    if n_total == 0:
        return OutcomeDecision(
            outcome=Outcome.O4,
            description=OUTCOME_DESCRIPTIONS[Outcome.O4],
            evidence={"reason": "No cell results available"},
        )

    n_unclassified = sum(
        1 for cr in cell_results if cr.modal_class == "UNCLASSIFIED"
    )
    unclassified_fraction = n_unclassified / n_total

    if unclassified_fraction > O3_UNCLASSIFIED_MAX_FRACTION:
        evidence["unclassified_fraction"] = unclassified_fraction
        evidence["n_unclassified"] = n_unclassified
        evidence["n_total"] = n_total
        return OutcomeDecision(
            outcome=Outcome.O4,
            description=OUTCOME_DESCRIPTIONS[Outcome.O4],
            evidence=evidence,
        )

    return None


# ── O3: Candidate signal ───────────────────────────────────────────────────

def _find_adjacent_alpha_runs(
    alpha_values: list[float],
) -> int:
    """Find the longest run of contiguous alpha_tilde values.

    Alpha values are considered adjacent if they are consecutive entries
    in the frozen ALPHA_TILDE_VALUES tuple.
    """
    if not alpha_values:
        return 0

    alpha_set = set(alpha_values)
    alpha_list = sorted(ALPHA_TILDE_VALUES)
    alpha_indices = {v: i for i, v in enumerate(alpha_list)}

    # Find which indices are present
    present = sorted(alpha_indices[a] for a in alpha_set if a in alpha_indices)
    if not present:
        return 0

    # Find longest consecutive run
    best = 1
    current = 1
    for i in range(1, len(present)):
        if present[i] == present[i - 1] + 1:
            current += 1
            best = max(best, current)
        else:
            current = 1

    return best


def check_o3(
    cell_results: list[CellResult],
) -> Optional[OutcomeDecision]:
    """Check O3: [1:2:3] candidate signal.

    Requirements (ALL must hold):
      1. [1:2:3] is modal with frequency >= O3_MIN_FREQUENCY
      2. In >= O3_MIN_ADJACENT_ALPHA contiguous alpha_tilde values
      3. For ALL N >= O3_MIN_N
      4. In BOTH arms (M0 and M1 if M1 data exists)
      5. Hot/cold consistent (no METASTABLE flag) in signal cells
    """
    evidence: dict[str, object] = {}

    # Separate by model
    m0_cells = [cr for cr in cell_results if cr.cell.model == "M0"]
    m1_cells = [cr for cr in cell_results if cr.cell.model == "M1"]

    arms_to_check = [("M0", m0_cells)]
    if m1_cells:
        arms_to_check.append(("M1", m1_cells))

    for arm_name, arm_cells in arms_to_check:
        # Filter to cells where [1:2:3] is modal with sufficient frequency
        signal_cells = [
            cr for cr in arm_cells
            if cr.modal_class == _O3_TARGET
            and cr.modal_frequency >= O3_MIN_FREQUENCY
        ]

        if not signal_cells:
            evidence[f"{arm_name}_signal_cells"] = 0
            return None  # O3 fails

        # Check: all N >= O3_MIN_N must show signal
        required_N = [n for n in N_LADDER if n >= O3_MIN_N]
        signal_N = set(cr.cell.N for cr in signal_cells)
        missing_N = [n for n in required_N if n not in signal_N]
        if missing_N:
            evidence[f"{arm_name}_missing_N"] = missing_N
            return None

        # Check: >= O3_MIN_ADJACENT_ALPHA contiguous alpha_tilde values
        signal_alphas = [cr.cell.alpha_tilde for cr in signal_cells]
        longest_run = _find_adjacent_alpha_runs(signal_alphas)
        if longest_run < O3_MIN_ADJACENT_ALPHA:
            evidence[f"{arm_name}_longest_alpha_run"] = longest_run
            return None

        # Check: hot/cold consistency in all signal cells
        metastable_cells = [
            cr for cr in signal_cells if "METASTABLE" in cr.flags
        ]
        if metastable_cells:
            evidence[f"{arm_name}_metastable_count"] = len(metastable_cells)
            return None

        evidence[f"{arm_name}_signal_cells"] = len(signal_cells)
        evidence[f"{arm_name}_longest_alpha_run"] = longest_run

    return OutcomeDecision(
        outcome=Outcome.O3,
        description=OUTCOME_DESCRIPTIONS[Outcome.O3],
        evidence=evidence,
    )


# ── O2/O1: H0 variants ─────────────────────────────────────────────────────

def check_o2(cell_results: list[CellResult]) -> Optional[OutcomeDecision]:
    """Check O2: equal-block classes ([1:1], [1:1:1], [1:1:1:1]) dominant.

    O2 if any equal-block class OTHER than [1] is the overall grid-wide mode.
    """
    if not cell_results:
        return None

    # Grid-wide modal class
    all_modals = [cr.modal_class for cr in cell_results]
    counts: dict[str, int] = {}
    for m in all_modals:
        counts[m] = counts.get(m, 0) + 1

    if not counts:
        return None

    grid_mode = min(
        (label for label in counts if counts[label] == max(counts.values())),
        default=None,
    )

    if grid_mode in _EQUAL_BLOCK_CLASSES and grid_mode != "[1]":
        return OutcomeDecision(
            outcome=Outcome.O2,
            description=OUTCOME_DESCRIPTIONS[Outcome.O2],
            evidence={
                "grid_mode": grid_mode,
                "cell_count": counts[grid_mode],
                "total_cells": len(cell_results),
            },
        )
    return None


def check_o1(cell_results: list[CellResult]) -> Optional[OutcomeDecision]:
    """Check O1: modal [1] → H0 confirmed, PR-B1 FAILS."""
    if not cell_results:
        return None

    all_modals = [cr.modal_class for cr in cell_results]
    counts: dict[str, int] = {}
    for m in all_modals:
        counts[m] = counts.get(m, 0) + 1

    if not counts:
        return None

    grid_mode = min(
        (label for label in counts if counts[label] == max(counts.values())),
        default=None,
    )

    if grid_mode == "[1]":
        return OutcomeDecision(
            outcome=Outcome.O1,
            description=OUTCOME_DESCRIPTIONS[Outcome.O1],
            evidence={
                "grid_mode": "[1]",
                "cell_count": counts["[1]"],
                "total_cells": len(cell_results),
            },
        )
    return None


# ── Master decision function ───────────────────────────────────────────────

def decide_outcome(
    validation_report: ValidationReport,
    cell_results: list[CellResult],
    multi_target: MultiTargetResult,
) -> OutcomeDecision:
    """Apply decision rules in priority order: O5 > O4 > O3 > O2 > O1 > default O4.

    Parameters
    ----------
    validation_report : ValidationReport
        From validation.run_validation_gate().
    cell_results : list[CellResult]
        Scored + flagged results for every grid cell.
    multi_target : MultiTargetResult
        From null_controls.check_multi_target().

    Returns
    -------
    OutcomeDecision
    """
    # Priority 1: O5 — detector gate failure
    decision = check_o5(validation_report)
    if decision is not None:
        return decision

    # Priority 2: O4 — non-discriminative
    decision = check_o4(cell_results, multi_target)
    if decision is not None:
        return decision

    # Priority 3: O3 — candidate signal
    decision = check_o3(cell_results)
    if decision is not None:
        return decision

    # Priority 4: O2 — H0 variant
    decision = check_o2(cell_results)
    if decision is not None:
        return decision

    # Priority 5: O1 — H0 confirmed
    decision = check_o1(cell_results)
    if decision is not None:
        return decision

    # Default: O4 — non-discriminative
    return OutcomeDecision(
        outcome=Outcome.O4,
        description=OUTCOME_DESCRIPTIONS[Outcome.O4],
        evidence={"reason": "No outcome rule triggered; default to O4"},
    )
