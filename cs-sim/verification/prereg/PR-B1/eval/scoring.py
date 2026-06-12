"""
AG-Eval Scoring — Exact-Arithmetic Ratio-Class Scoring (Sec. 4.2–4.4)
======================================================================
MANDATORY: fractions.Fraction exact arithmetic for candidate vectors,
distance comparisons, and class-assignment ties.

All candidate classes in CANDIDATE_SET_P are processed by IDENTICAL code
paths (procedural symmetry, Sec. 4.2).

Pipeline per observation:
  1. Receive empirical partition multiset {m_j} from detector.
  2. Sort ascending, normalise to sum = 1 via Fraction.
  3. For EACH candidate class in P (identical code path):
     a. Normalise candidate ratios to sum = 1 via Fraction.
     b. Zero-pad both vectors to equal length.
     c. Compute L2 distance (exact Fraction arithmetic for squared terms,
        final sqrt via float for comparison).
  4. Accept closest class if distance < SCORING_ACCEPTANCE_GATE, else UNCLASSIFIED.
  5. Per-cell result: modal assigned class over production ensemble with frequency.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Optional

from ..config import CANDIDATE_SET_P, SCORING_ACCEPTANCE_GATE


# ── Type aliases ────────────────────────────────────────────────────────────

FractionVec = tuple[Fraction, ...]
ClassLabel = str  # e.g. "[1:2:3]" or "UNCLASSIFIED"


# ── Candidate vector cache (computed once, immutable) ───────────────────────

def _build_candidate_vectors() -> dict[str, FractionVec]:
    """Normalise each candidate ratio class to sum = 1 using exact Fraction.

    Sorted ascending (matching empirical partition convention).
    """
    vectors: dict[str, FractionVec] = {}
    for label, ratios in CANDIDATE_SET_P.items():
        total = Fraction(sum(ratios))
        normalised = tuple(sorted(Fraction(r) / total for r in ratios))
        vectors[label] = normalised
    return vectors


_CANDIDATE_VECTORS: dict[str, FractionVec] = _build_candidate_vectors()


# ── Core scoring functions (identical code path for every class) ────────────

def _normalise_empirical(partition: tuple[int, ...]) -> FractionVec:
    """Normalise empirical partition to sum = 1 using exact Fraction.

    Returns sorted ascending Fraction vector.
    """
    if not partition:
        return ()
    total = Fraction(sum(partition))
    if total == 0:
        return tuple(Fraction(0) for _ in partition)
    return tuple(sorted(Fraction(m) / total for m in partition))


def _zero_pad(
    vec_a: FractionVec,
    vec_b: FractionVec,
) -> tuple[FractionVec, FractionVec]:
    """Pad the shorter vector with leading zeros so both have equal length.

    Zero-padding is prepended (smallest components) to preserve ascending sort.
    """
    la, lb = len(vec_a), len(vec_b)
    if la < lb:
        vec_a = tuple([Fraction(0)] * (lb - la)) + vec_a
    elif lb < la:
        vec_b = tuple([Fraction(0)] * (la - lb)) + vec_b
    return vec_a, vec_b


def _l2_distance_squared_exact(
    vec_a: FractionVec,
    vec_b: FractionVec,
) -> Fraction:
    """Compute L2 distance squared between two Fraction vectors (exact).

    Both vectors MUST have the same length (call _zero_pad first).
    """
    assert len(vec_a) == len(vec_b), (
        f"Length mismatch: {len(vec_a)} vs {len(vec_b)}"
    )
    d2 = Fraction(0)
    for a, b in zip(vec_a, vec_b):
        diff = a - b
        d2 += diff * diff
    return d2


def _l2_distance_float(d2_exact: Fraction) -> float:
    """Convert exact squared distance to float L2 distance.

    The sqrt is the ONLY float operation in the scoring pipeline.
    """
    return math.sqrt(float(d2_exact))


# ── Single-observation scoring ──────────────────────────────────────────────

def score_partition(
    partition: tuple[int, ...],
) -> tuple[ClassLabel, float, dict[str, float]]:
    """Score a single empirical partition against ALL candidate classes.

    Parameters
    ----------
    partition : tuple[int, ...]
        Sorted ascending cluster sizes from detector (m_j >= 2 each).

    Returns
    -------
    assigned_class : str
        Best-matching class label, or "UNCLASSIFIED".
    best_distance : float
        L2 distance to the assigned class (inf if UNCLASSIFIED).
    all_distances : dict[str, float]
        L2 distance to every candidate class.

    Notes
    -----
    Tie-breaking: if two classes have EXACTLY the same squared distance
    (Fraction comparison), the one with the lexicographically smaller label
    wins.  This is deterministic and bias-free since labels are public.
    """
    if not partition:
        return "UNCLASSIFIED", float("inf"), {}

    empirical = _normalise_empirical(partition)
    gate = Fraction(SCORING_ACCEPTANCE_GATE)
    gate_sq = gate * gate  # exact threshold squared

    all_distances: dict[str, float] = {}
    best_label: Optional[str] = None
    best_d2: Optional[Fraction] = None

    # ── IDENTICAL code path for every class (procedural symmetry) ───────
    for label, candidate_vec in _CANDIDATE_VECTORS.items():
        emp_padded, cand_padded = _zero_pad(empirical, candidate_vec)
        d2 = _l2_distance_squared_exact(emp_padded, cand_padded)
        dist_float = _l2_distance_float(d2)
        all_distances[label] = dist_float

        # Exact Fraction comparison for acceptance and tie-breaking
        if d2 < gate_sq:
            if best_d2 is None or d2 < best_d2:
                best_d2 = d2
                best_label = label
            elif d2 == best_d2:
                # Exact tie → lexicographic label order (deterministic)
                assert best_label is not None
                if label < best_label:
                    best_label = label
    # ── END identical code path ─────────────────────────────────────────

    if best_label is not None:
        return best_label, all_distances[best_label], all_distances
    else:
        return "UNCLASSIFIED", float("inf"), all_distances


# ── Ensemble aggregation ───────────────────────────────────────────────────

def modal_class(
    assigned_classes: list[ClassLabel],
) -> tuple[ClassLabel, float]:
    """Compute modal (most frequent) class and its frequency over an ensemble.

    Parameters
    ----------
    assigned_classes : list[str]
        One class label per seed/run.

    Returns
    -------
    mode : str
        Most frequent class label.
    frequency : float
        Fraction of runs assigned to the mode (in [0, 1]).

    Tie-breaking: lexicographically smallest label among modes.
    """
    if not assigned_classes:
        return "UNCLASSIFIED", 0.0

    counts: dict[str, int] = {}
    for c in assigned_classes:
        counts[c] = counts.get(c, 0) + 1

    max_count = max(counts.values())
    # Among all labels with max count, choose lexicographic smallest
    mode = min(label for label, cnt in counts.items() if cnt == max_count)
    frequency = max_count / len(assigned_classes)
    return mode, frequency


def score_ensemble(
    partitions: list[tuple[int, ...]],
) -> dict[str, object]:
    """Score a full ensemble of partitions for a single cell.

    Parameters
    ----------
    partitions : list[tuple[int, ...]]
        One partition per seed/run.

    Returns
    -------
    dict with keys:
        "per_seed": list of (assigned_class, distance, all_distances) tuples
        "modal_class": str
        "modal_frequency": float
        "class_counts": dict[str, int]
    """
    per_seed: list[tuple[ClassLabel, float, dict[str, float]]] = []
    assigned: list[ClassLabel] = []

    for partition in partitions:
        cls, dist, dists = score_partition(partition)
        per_seed.append((cls, dist, dists))
        assigned.append(cls)

    mode, freq = modal_class(assigned)

    class_counts: dict[str, int] = {}
    for c in assigned:
        class_counts[c] = class_counts.get(c, 0) + 1

    return {
        "per_seed": per_seed,
        "modal_class": mode,
        "modal_frequency": freq,
        "class_counts": class_counts,
    }
