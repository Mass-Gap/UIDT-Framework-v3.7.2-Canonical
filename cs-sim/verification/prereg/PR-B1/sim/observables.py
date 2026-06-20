"""
Observable Extraction — Raw Spectra Only
==========================================
Extracts unclassified raw observables from the current matrix configuration.

BLINDING CONTRACT:
    This module outputs ONLY raw arrays and scalar diagnostics.
    It contains ZERO partition detection, clustering, comparison, or scoring.
    NO reference to any specific partition class or forbidden pattern.

Observables per measurement:
    1. Casimir spectrum:  sorted eigenvalues of Q = X1² + X2² + X3²
    2. X3 spectrum:       sorted eigenvalues of X3
    3. Scalars:
        - S / N²    (action density)
        - Tr(Q) / N (Casimir expectation per matrix size)
        - Myers term value (Chern-Simons contribution)

IEEE-754 float64 throughout.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

from .action import Matrices, compute_action


class Observables(NamedTuple):
    """Container for raw observables extracted from one measurement."""

    casimir_eigenvalues: np.ndarray   # shape (N,), float64, sorted ascending
    x3_eigenvalues: np.ndarray        # shape (N,), float64, sorted ascending
    action_density: float             # S / N²
    casimir_trace_per_N: float        # Tr(Q) / N
    myers_value: float                # CS contribution to the action


def extract_casimir_spectrum(X: Matrices) -> np.ndarray:
    """Compute the sorted eigenvalues of Q = X1² + X2² + X3².

    Q is Hermitian positive semi-definite, so eigenvalues are real ≥ 0.

    Parameters
    ----------
    X : Matrices
        Triple (X1, X2, X3), each N × N Hermitian complex128.

    Returns
    -------
    np.ndarray
        Sorted (ascending) real eigenvalues, shape (N,), float64.
    """
    Q = X[0] @ X[0] + X[1] @ X[1] + X[2] @ X[2]
    # Enforce exact Hermiticity for numerical stability
    Q = (Q + Q.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(Q)
    return eigenvalues  # eigvalsh returns sorted ascending


def extract_x3_spectrum(X: Matrices) -> np.ndarray:
    """Compute the sorted eigenvalues of X3.

    X3 is Hermitian, so eigenvalues are real.

    Parameters
    ----------
    X : Matrices
        Triple (X1, X2, X3), each N × N Hermitian complex128.

    Returns
    -------
    np.ndarray
        Sorted (ascending) real eigenvalues, shape (N,), float64.
    """
    X3 = X[2]
    X3_sym = (X3 + X3.conj().T) / 2.0
    eigenvalues = np.linalg.eigvalsh(X3_sym)
    return eigenvalues  # eigvalsh returns sorted ascending


def extract_observables(
    X: Matrices,
    N: int,
    alpha: float,
    mu2: float = 0.0,
    g2: float = 0.0,
) -> Observables:
    """Extract all raw observables from the current matrix configuration.

    Parameters
    ----------
    X : Matrices
        Triple (X1, X2, X3), each N × N Hermitian complex128.
    N : int
        Matrix size.
    alpha : float
        Chern-Simons coupling.
    mu2 : float
        Mass-squared deformation (M1 only; 0.0 for M0).
    g2 : float
        Double-trace coupling (M1 only; 0.0 for M0).

    Returns
    -------
    Observables
        Named tuple with all raw spectral and scalar data.
    """
    # Spectra
    casimir_eigs = extract_casimir_spectrum(X)
    x3_eigs = extract_x3_spectrum(X)

    # Action decomposition
    action_result = compute_action(X, N, alpha, mu2, g2)
    action_density = action_result.total / (N * N)

    # Casimir trace
    Q = X[0] @ X[0] + X[1] @ X[1] + X[2] @ X[2]
    casimir_trace_per_N = np.trace(Q).real / N

    return Observables(
        casimir_eigenvalues=casimir_eigs,
        x3_eigenvalues=x3_eigs,
        action_density=action_density,
        casimir_trace_per_N=casimir_trace_per_N,
        myers_value=action_result.myers,
    )
