"""
PREREG-PR-B1 — Frozen Protocol Configuration
=============================================
All constants in this module are FROZEN at preregistration time.
Modifying any value after the first production trajectory VOIDS the protocol (Sec. 8).

This is a stochastic simulation, NOT proof-critical arithmetic.
The canonical mp.dps = 80 rule DOES NOT APPLY. IEEE-754 float64 throughout.
Exact arithmetic (fractions.Fraction) is mandatory ONLY in scoring (Sec. 4.4).
"""

from __future__ import annotations

import hashlib
from typing import NamedTuple


# =============================================================================
# § 2.3 — Parameter Grid (frozen)
# =============================================================================

N_LADDER: tuple[int, ...] = (16, 24, 32, 48, 64)

ALPHA_TILDE_VALUES: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0)

# M1-only couplings
MU2_VALUES: tuple[float, ...] = (-1.0, 0.0, 1.0)
G2_VALUES: tuple[float, ...] = (0.0, 0.5)

SEEDS_PER_CELL: int = 8
HOT_SEEDS: int = 4   # seeds 0..3 start from Gaussian random Hermitian ("hot")
COLD_SEEDS: int = 4  # seeds 4..7 start from zero matrix ("cold")


class GridCell(NamedTuple):
    """A single point in the preregistered parameter grid."""
    model: str           # "M0" or "M1"
    N: int               # matrix size
    alpha_tilde: float   # dimensionless coupling
    mu2: float           # mass deformation (M1 only; 0.0 for M0)
    g2: float            # double-trace coupling (M1 only; 0.0 for M0)


def build_grid() -> list[GridCell]:
    """Build the full frozen parameter grid in lexicographic order.

    M0: 5 × 8 × 8 = 320 cells.
    M1: 5 × 8 × 3 × 2 × 8 = 1920 cells.
    Total per-seed cells: 2240.  Total runs: 2240 × 8 = 17920.
    """
    cells: list[GridCell] = []

    # M0 grid (mandatory)
    for N in N_LADDER:
        for alpha_tilde in ALPHA_TILDE_VALUES:
            cells.append(GridCell("M0", N, alpha_tilde, 0.0, 0.0))

    # M1 grid (contingent on budget; executed in frozen order, never selectively)
    for N in N_LADDER:
        for alpha_tilde in ALPHA_TILDE_VALUES:
            for mu2 in MU2_VALUES:
                for g2 in G2_VALUES:
                    cells.append(GridCell("M1", N, alpha_tilde, mu2, g2))

    return cells


def build_pilot_grid() -> list[GridCell]:
    """Build the pilot-phase grid: M0 only, N in {16, 24, 32}.

    Per Q1 decision: Pilot is for thermalization testing, acceptance rates,
    and memory-leak detection ONLY.  AG-Eval MUST NOT score pilot data.
    """
    pilot_N = (16, 24, 32)
    cells: list[GridCell] = []
    for N in pilot_N:
        for alpha_tilde in ALPHA_TILDE_VALUES:
            cells.append(GridCell("M0", N, alpha_tilde, 0.0, 0.0))
    return cells


# =============================================================================
# § 3.2 — Thermalization and Sampling (frozen criteria)
# =============================================================================

THERMALIZATION_WINDOW: int = 200        # trajectories per averaging window
THERMALIZATION_TOLERANCE_SE: float = 0.5  # max change in SE between windows
THERMALIZATION_MIN_TRAJECTORIES: int = 2000

PRODUCTION_TRAJECTORIES: int = 8000
MEASUREMENT_INTERVAL: int = 10          # measure every 10th trajectory
MIN_EFFECTIVE_SAMPLE_SIZE: int = 100    # ESS below this → UNDERSAMPLED flag

# HMC parameters (Sec. 3.1)
HMC_TRAJECTORY_LENGTH: float = 1.0
HMC_ACCEPTANCE_LOW: float = 0.50
HMC_ACCEPTANCE_HIGH: float = 0.85

# Initial step size for HMC (will be auto-tuned during thermalization)
HMC_INITIAL_STEP_SIZE: float = 0.005


# =============================================================================
# § 4.1–4.3 — Detector and Scoring Constants (frozen)
# =============================================================================

# KDE bandwidth: Silverman's rule-of-thumb (fixed; no per-run tuning)
# h = 0.9 * min(std, IQR/1.34) * n^(-1/5)
# Applied to sorted eigenvalues of Q = X1^2 + X2^2 + X3^2

KDE_MIN_FRACTION: float = 0.20   # local minima below 20% of global KDE max
KDE_MIN_CLUSTER_SIZE: int = 2    # discard clusters with m_j < 2 (defect modes)

SCORING_ACCEPTANCE_GATE: float = 0.08  # L2 distance threshold; else UNCLASSIFIED


# § 4.2 — Candidate Ratio-Class Set P (frozen, public, symmetric)
# Each entry: sorted ascending normalized ratio tuple.
# All classes processed by byte-identical code paths.
CANDIDATE_SET_P: dict[str, tuple[int, ...]] = {
    "[1]":         (1,),
    "[1:1]":       (1, 1),
    "[1:2]":       (1, 2),
    "[1:1:1]":     (1, 1, 1),
    "[1:2:3]":     (1, 2, 3),
    "[1:2:4]":     (1, 2, 4),
    "[1:1:2]":     (1, 1, 2),
    "[1:3:3]":     (1, 3, 3),
    "[1:1:1:1]":   (1, 1, 1, 1),
    "[1:1:2:3]":   (1, 1, 2, 3),
    "[1:2:2:3]":   (1, 2, 2, 3),
}
# NOTE: [2:2:2] reduces to [1:1:1] per Sec. 4.2 and is listed above for traceability.


# =============================================================================
# § 4.5 — Detector Validation Gate (frozen)
# =============================================================================

VALIDATION_NOISE_LEVELS: tuple[float, ...] = (0.01, 0.05, 0.1, 0.2, 0.3)
VALIDATION_RECOVERY_THRESHOLD_LOW: float = 0.95   # for epsilon <= 0.1
VALIDATION_RECOVERY_THRESHOLD_HIGH: float = 0.80  # for epsilon = 0.2
VALIDATION_SAMPLES_PER_LEVEL: int = 200  # planted samples per (class, N, epsilon)


# =============================================================================
# § 5.2 — Blinding: Forbidden Patterns (mechanically enforced)
# =============================================================================

# These patterns are BANNED in simulation modules and eval/detector.py.
# eval/scoring.py is exempt ONLY for the public symmetric set P.
FORBIDDEN_PATTERNS: tuple[str, ...] = (
    "(1,2,3)",
    "[1,2,3]",
    "1:2:3",
    "target",
    "goal",
    "calibrate",
    "reward",
    "loss",
    "16.339",
    "49/3",
    "17/3000",
)


# =============================================================================
# § 6 — Null Controls (frozen)
# =============================================================================

# Scrambled-coupling control cells (Sec. 6, fixed now)
SCRAMBLED_CONTROL_CELLS: tuple[GridCell, GridCell] = (
    GridCell("M1", 32, 2.0, 1.0, 0.5),
    GridCell("M1", 32, 2.0, -1.0, 0.0),
)

# Multi-target false-positive: if ≥2 ratio classes with k≥3 blocks are
# each modal with frequency ≥ 0.5, scoring is non-discriminative (O4).
MULTI_TARGET_MIN_BLOCKS: int = 3
MULTI_TARGET_MIN_FREQUENCY: float = 0.5


# =============================================================================
# § 7 — O3 Signal Requirements (frozen)
# =============================================================================

O3_MIN_FREQUENCY: float = 0.5              # modal frequency threshold
O3_MIN_ADJACENT_ALPHA: int = 2             # contiguous alpha_tilde window
O3_MIN_N: int = 24                          # all N >= 24 must show signal
O3_UNCLASSIFIED_MAX_FRACTION: float = 0.5  # grid-wide UNCLASSIFIED cap for O4


# =============================================================================
# § 9.2 — Seed Policy (deterministic, non-cherry-pickable)
# =============================================================================

def compute_seed(model: str, N: int, alpha_tilde: float,
                 mu2: float, g2: float, j: int) -> int:
    """Compute the deterministic seed for a given cell and seed index.

    seed(cell, j) = int.from_bytes(
        SHA256("PREREG-PR-B1-001|{model}|{N}|{alpha_tilde}|{mu2}|{g2}|{j}").digest()[:8],
        "big"
    )
    """
    tag = f"PREREG-PR-B1-001|{model}|{N}|{alpha_tilde}|{mu2}|{g2}|{j}"
    digest = hashlib.sha256(tag.encode()).digest()[:8]
    return int.from_bytes(digest, "big")


# =============================================================================
# § 5.4 — PI Hash Commitment (Q2: strict abort without hash)
# =============================================================================

# The PI must insert the hex digest here before production.
# If this is empty, the orchestrator MUST abort with a FATAL error.
PI_COMMITMENT_HEX: str = ""
PI_COMMITMENT_UTC: str = ""


# =============================================================================
# Paths (relative to cs-sim/)
# =============================================================================

import pathlib

# Base directory: cs-sim/
_BASE = pathlib.Path(__file__).resolve().parent.parent.parent.parent
RAW_DATA_DIR = _BASE / "verification" / "data" / "prereg-PR-B1" / "raw"
OUT_DATA_DIR = _BASE / "verification" / "data" / "prereg-PR-B1" / "out"
MANIFEST_DIR = _BASE / "verification" / "data" / "prereg-PR-B1" / "manifests"
