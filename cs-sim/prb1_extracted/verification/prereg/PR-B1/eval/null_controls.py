"""
AG-Eval Null Controls — Null Control Machinery (Sec. 6)
========================================================
Three null-control mechanisms:

1. **Multi-target false-positive** (Sec. 6):
   If >= 2 ratio classes with k >= 3 blocks are each modal with
   frequency >= 0.5 across the grid, scoring is declared non-discriminative → O4.

2. **Scrambled-coupling control** (Sec. 6):
   Two fixed cells (from config.SCRAMBLED_CONTROL_CELLS) with flipped
   Myers sign.  These cells serve as negative controls — if they produce
   a structured signal, the detector is suspect.

3. **Hot/cold consistency** (Sec. 6):
   Modal classes from hot and cold seed families must agree.
   Disagreement → METASTABLE flag.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..config import (
    CANDIDATE_SET_P,
    MULTI_TARGET_MIN_BLOCKS,
    MULTI_TARGET_MIN_FREQUENCY,
    HOT_SEEDS,
    COLD_SEEDS,
    SEEDS_PER_CELL,
    SCRAMBLED_CONTROL_CELLS,
    GridCell,
)
from .scoring import ClassLabel, modal_class


# ── Data structures ─────────────────────────────────────────────────────────

@dataclass
class MultiTargetResult:
    """Result of the multi-target false-positive test."""
    offending_classes: list[str]  # classes with k>=3 blocks AND modal freq>=0.5
    is_non_discriminative: bool   # True → O4

    def __str__(self) -> str:
        if self.is_non_discriminative:
            return (
                f"NON-DISCRIMINATIVE: {len(self.offending_classes)} classes "
                f"with k>=3 blocks modal at freq>=0.5: {self.offending_classes}"
            )
        return "Multi-target check PASSED"


@dataclass
class HotColdResult:
    """Result of hot/cold consistency test for a single cell."""
    cell: GridCell
    hot_modal: ClassLabel
    hot_frequency: float
    cold_modal: ClassLabel
    cold_frequency: float
    is_metastable: bool  # True if hot != cold

    def __str__(self) -> str:
        if self.is_metastable:
            return (
                f"METASTABLE: hot={self.hot_modal}({self.hot_frequency:.2f}) "
                f"vs cold={self.cold_modal}({self.cold_frequency:.2f})"
            )
        return (
            f"CONSISTENT: {self.hot_modal}({self.hot_frequency:.2f}) == "
            f"{self.cold_modal}({self.cold_frequency:.2f})"
        )


@dataclass
class ScrambledControlResult:
    """Result of the scrambled-coupling control for one cell."""
    cell: GridCell
    modal_class: ClassLabel
    modal_frequency: float
    is_structured: bool  # True if a non-[1] structured class is modal


# ── Helpers ─────────────────────────────────────────────────────────────────

def _n_blocks(class_label: str) -> int:
    """Return the number of blocks k for a given class label.

    "[1]" → 1, "[1:2]" → 2, "[1:2:3]" → 3, etc.
    """
    if class_label == "UNCLASSIFIED":
        return 0
    ratios = CANDIDATE_SET_P.get(class_label)
    if ratios is None:
        return 0
    return len(ratios)


# ── Multi-target false-positive test ────────────────────────────────────────

def check_multi_target(
    cell_modal_results: dict[GridCell, tuple[ClassLabel, float]],
) -> MultiTargetResult:
    """Check whether scoring is non-discriminative (multi-target false positive).

    Parameters
    ----------
    cell_modal_results : dict
        Maps GridCell → (modal_class, modal_frequency) for every cell in the grid.

    Returns
    -------
    MultiTargetResult
        If >= 2 classes with k >= MULTI_TARGET_MIN_BLOCKS blocks are each modal
        with frequency >= MULTI_TARGET_MIN_FREQUENCY in at least one cell,
        scoring is non-discriminative → O4.
    """
    # Count how many cells each multi-block class is modal in
    # with sufficient frequency
    class_modal_cells: dict[str, int] = {}

    for cell, (modal_cls, modal_freq) in cell_modal_results.items():
        k = _n_blocks(modal_cls)
        if k >= MULTI_TARGET_MIN_BLOCKS and modal_freq >= MULTI_TARGET_MIN_FREQUENCY:
            class_modal_cells[modal_cls] = class_modal_cells.get(modal_cls, 0) + 1

    # Offending classes: those that appear as modal (with conditions) in any cell
    offending = sorted(class_modal_cells.keys())

    return MultiTargetResult(
        offending_classes=offending,
        is_non_discriminative=len(offending) >= 2,
    )


# ── Hot/cold consistency test ───────────────────────────────────────────────

def check_hot_cold_consistency(
    cell: GridCell,
    assigned_classes: list[ClassLabel],
) -> HotColdResult:
    """Check whether hot and cold seed families agree on modal class.

    Parameters
    ----------
    cell : GridCell
    assigned_classes : list[str]
        Length = SEEDS_PER_CELL.  First HOT_SEEDS entries are hot starts,
        remaining COLD_SEEDS entries are cold starts.

    Returns
    -------
    HotColdResult
        is_metastable = True if hot and cold modal classes disagree.
    """
    assert len(assigned_classes) == SEEDS_PER_CELL, (
        f"Expected {SEEDS_PER_CELL} classes, got {len(assigned_classes)}"
    )

    hot_classes = assigned_classes[:HOT_SEEDS]
    cold_classes = assigned_classes[HOT_SEEDS:HOT_SEEDS + COLD_SEEDS]

    hot_mode, hot_freq = modal_class(hot_classes)
    cold_mode, cold_freq = modal_class(cold_classes)

    return HotColdResult(
        cell=cell,
        hot_modal=hot_mode,
        hot_frequency=hot_freq,
        cold_modal=cold_mode,
        cold_frequency=cold_freq,
        is_metastable=(hot_mode != cold_mode),
    )


# ── Scrambled-coupling control ──────────────────────────────────────────────

def check_scrambled_controls(
    scrambled_results: dict[GridCell, list[ClassLabel]],
) -> list[ScrambledControlResult]:
    """Evaluate the scrambled-coupling control cells.

    Parameters
    ----------
    scrambled_results : dict
        Maps each scrambled control cell → list of assigned classes (one per seed).

    Returns
    -------
    list[ScrambledControlResult]
        One per control cell.  If a non-[1] structured class is modal,
        is_structured = True, indicating the detector may be unreliable.
    """
    results: list[ScrambledControlResult] = []

    for cell in SCRAMBLED_CONTROL_CELLS:
        if cell not in scrambled_results:
            # Cell was not run (e.g., budget constraint) — record as missing
            results.append(ScrambledControlResult(
                cell=cell,
                modal_class="MISSING",
                modal_frequency=0.0,
                is_structured=False,
            ))
            continue

        classes = scrambled_results[cell]
        mode, freq = modal_class(classes)

        # A control cell showing a structured signal (not [1], not UNCLASSIFIED)
        # is suspicious.
        is_structured = mode not in ("[1]", "UNCLASSIFIED", "MISSING")

        results.append(ScrambledControlResult(
            cell=cell,
            modal_class=mode,
            modal_frequency=freq,
            is_structured=is_structured,
        ))

    return results
