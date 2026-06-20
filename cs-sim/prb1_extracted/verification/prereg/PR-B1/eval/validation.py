"""
AG-Eval Validation — Detector Validation Gate (Sec. 4.5)
=========================================================
Planted-ensemble test to verify detector + scorer reliability.

For every candidate class p in P and every N in N_LADDER:
  - Build planted configuration: X_a = L_a^{(p, N)} + epsilon * G_a
    where G_a are iid Gaussian random Hermitian matrices.
  - For epsilon in {0.01, 0.05, 0.1, 0.2, 0.3}:
    - Generate VALIDATION_SAMPLES_PER_LEVEL samples.
    - Run detector + scorer.
    - Compute recovery rate (fraction correctly classified).
  - Requirements:
    >= 95 % recovery for epsilon <= 0.1
    >= 80 % recovery for epsilon = 0.2
  - epsilon = 0.3 is informational only (no gate).

Gate failure at ANY (class, N, epsilon) → O5 ABORT.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from ..config import (
    CANDIDATE_SET_P,
    N_LADDER,
    VALIDATION_NOISE_LEVELS,
    VALIDATION_RECOVERY_THRESHOLD_LOW,
    VALIDATION_RECOVERY_THRESHOLD_HIGH,
    VALIDATION_SAMPLES_PER_LEVEL,
)
from ..su2 import block_diagonal_config, partition_from_ratio_class
from .detector import detect_partition_from_matrices
from .scoring import score_partition


# ── Data structures ─────────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    """Result for a single (class, N, epsilon) triplet."""
    class_label: str
    N: int
    epsilon: float
    n_samples: int
    n_correct: int
    recovery_rate: float
    threshold: Optional[float]   # None for informational epsilon = 0.3
    passed: Optional[bool]       # None for informational

    @property
    def is_gated(self) -> bool:
        """Whether this triplet is subject to a pass/fail gate."""
        return self.threshold is not None


@dataclass
class ValidationReport:
    """Aggregate validation report over all (class, N, epsilon) triplets."""
    results: list[ValidationResult] = field(default_factory=list)
    gate_passed: bool = True
    failures: list[ValidationResult] = field(default_factory=list)

    def add(self, result: ValidationResult) -> None:
        self.results.append(result)
        if result.is_gated and result.passed is False:
            self.gate_passed = False
            self.failures.append(result)


# ── Gaussian random Hermitian matrix ────────────────────────────────────────

def _random_hermitian(
    N: int,
    rng: np.random.Generator,
) -> NDArray[np.complex128]:
    """Generate a random N × N Hermitian matrix from iid Gaussian entries.

    Off-diagonal: complex Gaussian (real, imag ~ N(0, 1/sqrt(2))).
    Diagonal: real Gaussian ~ N(0, 1).
    """
    A = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))
    H = (A + A.conj().T) / 2.0
    return H


# ── Planted-ensemble generation ────────────────────────────────────────────

def _planted_sample(
    ratio_class: tuple[int, ...],
    N: int,
    epsilon: float,
    rng: np.random.Generator,
) -> tuple[NDArray[np.complex128], NDArray[np.complex128], NDArray[np.complex128]]:
    """Generate a single planted sample: X_a = L_a^{(p,N)} + epsilon * G_a."""
    partition = partition_from_ratio_class(ratio_class, N)
    X1_cl, X2_cl, X3_cl = block_diagonal_config(partition, N, alpha=1.0)

    G1 = _random_hermitian(N, rng)
    G2 = _random_hermitian(N, rng)
    G3 = _random_hermitian(N, rng)

    X1 = X1_cl + epsilon * G1
    X2 = X2_cl + epsilon * G2
    X3 = X3_cl + epsilon * G3

    return X1, X2, X3


# ── Single triplet validation ──────────────────────────────────────────────

def _get_threshold(epsilon: float) -> Optional[float]:
    """Return the recovery threshold for a given epsilon, or None."""
    if epsilon <= 0.1 + 1e-12:
        return VALIDATION_RECOVERY_THRESHOLD_LOW
    elif abs(epsilon - 0.2) < 1e-12:
        return VALIDATION_RECOVERY_THRESHOLD_HIGH
    else:
        return None  # informational only (epsilon = 0.3)


def validate_triplet(
    class_label: str,
    ratio_class: tuple[int, ...],
    N: int,
    epsilon: float,
    n_samples: int,
    base_seed: int = 42,
) -> ValidationResult:
    """Validate detector + scorer on one (class, N, epsilon) triplet.

    Parameters
    ----------
    class_label : str
        e.g. "[1:2:3]"
    ratio_class : tuple[int, ...]
        e.g. (1, 2, 3)
    N : int
        Matrix size.
    epsilon : float
        Noise level.
    n_samples : int
        Number of planted samples to test.
    base_seed : int
        Base seed; actual seed = hash(base_seed, class_label, N, epsilon).

    Returns
    -------
    ValidationResult
    """
    # Deterministic seed for reproducibility
    seed_str = f"VALIDATION|{class_label}|{N}|{epsilon}|{base_seed}"
    seed_int = int.from_bytes(
        __import__("hashlib").sha256(seed_str.encode()).digest()[:8], "big"
    )
    rng = np.random.default_rng(seed_int)

    n_correct = 0
    for _ in range(n_samples):
        X1, X2, X3 = _planted_sample(ratio_class, N, epsilon, rng)
        partition, _ = detect_partition_from_matrices(X1, X2, X3)
        assigned_class, _, _ = score_partition(partition)
        if assigned_class == class_label:
            n_correct += 1

    recovery_rate = n_correct / n_samples if n_samples > 0 else 0.0
    threshold = _get_threshold(epsilon)

    passed: Optional[bool] = None
    if threshold is not None:
        passed = recovery_rate >= threshold

    return ValidationResult(
        class_label=class_label,
        N=N,
        epsilon=epsilon,
        n_samples=n_samples,
        n_correct=n_correct,
        recovery_rate=recovery_rate,
        threshold=threshold,
        passed=passed,
    )


# ── Full validation gate ───────────────────────────────────────────────────

def run_validation_gate(
    base_seed: int = 42,
    n_samples: Optional[int] = None,
    verbose: bool = False,
) -> tuple[bool, ValidationReport]:
    """Run the full detector validation gate (Sec. 4.5).

    Iterates over every (class, N, epsilon) triplet.
    Returns (gate_passed, report).

    Gate failure at ANY triplet → gate_passed = False → O5 ABORT.
    """
    if n_samples is None:
        n_samples = VALIDATION_SAMPLES_PER_LEVEL

    report = ValidationReport()

    for class_label, ratio_class in CANDIDATE_SET_P.items():
        for N in N_LADDER:
            # Skip impossible combinations (N too small for this class)
            total_ratio = sum(ratio_class)
            if N < total_ratio:
                continue

            for epsilon in VALIDATION_NOISE_LEVELS:
                result = validate_triplet(
                    class_label=class_label,
                    ratio_class=ratio_class,
                    N=N,
                    epsilon=epsilon,
                    n_samples=n_samples,
                    base_seed=base_seed,
                )
                report.add(result)

                if verbose:
                    status = "PASS" if result.passed else (
                        "FAIL" if result.passed is False else "INFO"
                    )
                    print(
                        f"  {class_label:12s} N={N:3d} "
                        f"eps={epsilon:.2f} "
                        f"recovery={result.recovery_rate:.3f} "
                        f"[{status}]"
                    )

    return report.gate_passed, report


def main() -> None:
    """CLI entry point for the detector validation gate."""
    import sys

    print("=" * 72)
    print("PREREG-PR-B1 — Detector Validation Gate (Sec. 4.5)")
    print("=" * 72)

    passed, report = run_validation_gate(verbose=True)

    print()
    if passed:
        print("[GATE] PASSED — all recovery thresholds met.")
    else:
        print("[GATE] FAILED — O5 ABORT.")
        print(f"  {len(report.failures)} failure(s):")
        for f in report.failures:
            print(
                f"    {f.class_label} N={f.N} eps={f.epsilon:.2f}: "
                f"recovery={f.recovery_rate:.3f} < {f.threshold:.3f}"
            )

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

