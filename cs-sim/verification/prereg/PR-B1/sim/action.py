"""
Matrix Model Action Functionals
================================
Implements the two action variants specified in the preregistration protocol:

M0 (Yang-Mills-Chern-Simons):
    S = N * Tr( -1/4 * [Xa, Xb]^2  +  2i/3 * α * ε_abc * Xa Xb Xc )

M1 (M0 + deformation):
    S = S_M0  +  N * Tr( μ²/2 * Xa Xa )  +  (g2/N) * (Tr Xa Xa)²

where the sums over a,b,c run from 1 to 3, and the Levi-Civita symbol
ε_abc selects the three cyclic permutations.

All arithmetic is IEEE-754 float64 (complex128 for Hermitian matrices).
No mpmath, no mp.dps = 80.  This is stochastic simulation code.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np

# Type alias for a matrix triple
Matrices = tuple[np.ndarray, np.ndarray, np.ndarray]


class ActionResult(NamedTuple):
    """Container for action value and diagnostic decomposition."""
    total: float        # S (real part of the full action)
    commutator_sq: float  # N * Tr(-1/4 [Xa,Xb]^2)  (YM piece)
    myers: float        # N * Tr(2i/3 α ε_abc Xa Xb Xc)  (CS piece)
    mass: float         # N * Tr(μ²/2 Xa Xa)              (M1 only)
    double_trace: float  # (g2/N) * (Tr Xa Xa)²           (M1 only)


def commutator(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Compute [A, B] = A @ B - B @ A."""
    return A @ B - B @ A


def _compute_commutator_sq_term(X: Matrices, N: int) -> tuple[float, np.ndarray]:
    """Compute -1/4 * sum_{a<b} Tr([Xa, Xb]^2) and return cached commutators.

    Returns
    -------
    (value, comm_array) where comm_array[k] stores [X_{a_k}, X_{b_k}]
    for the three pairs (0,1), (0,2), (1,2).
    """
    pairs = [(0, 1), (0, 2), (1, 2)]
    comms = []
    total = 0.0
    for a, b in pairs:
        C = commutator(X[a], X[b])
        comms.append(C)
        # Tr(C^2) — the commutator of Hermitian matrices is anti-Hermitian,
        # so C^2 is negative semi-definite Hermitian, Tr(C^2) is real ≤ 0.
        total += np.trace(C @ C).real
    # Action contribution: N * (-1/4) * sum Tr([Xa,Xb]^2)
    value = N * (-0.25) * total
    return value, comms


def _compute_myers_term(X: Matrices, N: int, alpha: float) -> float:
    """Compute the Myers (Chern-Simons) term.

    S_CS = N * Tr(2i/3 * α * ε_abc * Xa Xb Xc)

    The three cyclic permutations of ε_abc with ε_{123} = +1 give:
        Tr(X1 X2 X3) - Tr(X2 X1 X3)
        = Tr(X1 X2 X3) - Tr(X1 X3 X2)
        = Tr(X1 [X2, X3])

    So S_CS = N * (2i/3) * α * 3 * Tr(X1 [X2, X3])
            = N * 2i * α * Tr(X1 [X2, X3])

    The factor 3 comes from summing all three cyclic permutations.
    For Hermitian X_a, Tr(X1 [X2, X3]) is purely imaginary, making S_CS real.
    """
    C23 = commutator(X[1], X[2])  # [X2, X3]
    trace_val = np.trace(X[0] @ C23)
    # trace_val is purely imaginary for Hermitian matrices
    # 2i * (purely imaginary) = 2i * (i * y) = -2y, which is real
    value = N * (2.0j / 1.0) * alpha * trace_val
    return value.real


def _compute_mass_term(X: Matrices, N: int, mu2: float) -> float:
    """Compute N * Tr(μ²/2 * Xa Xa) = N * μ²/2 * sum_a Tr(Xa^2)."""
    if mu2 == 0.0:
        return 0.0
    tr_sum = sum(np.trace(X[a] @ X[a]).real for a in range(3))
    return N * (mu2 / 2.0) * tr_sum


def _compute_double_trace_term(X: Matrices, N: int, g2: float) -> float:
    """Compute (g2/N) * (sum_a Tr(Xa^2))^2."""
    if g2 == 0.0:
        return 0.0
    tr_sum = sum(np.trace(X[a] @ X[a]).real for a in range(3))
    return (g2 / N) * tr_sum ** 2


def compute_action(
    X: Matrices,
    N: int,
    alpha: float,
    mu2: float = 0.0,
    g2: float = 0.0,
) -> ActionResult:
    """Compute the full matrix model action S(X1, X2, X3).

    Parameters
    ----------
    X : tuple of three N × N Hermitian complex128 matrices
    N : int
        Matrix size.
    alpha : float
        Chern-Simons coupling (α̃ in the protocol).
    mu2 : float
        Mass-squared deformation parameter (M1 only; 0.0 for M0).
    g2 : float
        Double-trace coupling (M1 only; 0.0 for M0).

    Returns
    -------
    ActionResult
        Named tuple with .total and diagnostic components.
    """
    ym_val, _ = _compute_commutator_sq_term(X, N)
    cs_val = _compute_myers_term(X, N, alpha)
    mass_val = _compute_mass_term(X, N, mu2)
    dt_val = _compute_double_trace_term(X, N, g2)

    total = ym_val + cs_val + mass_val + dt_val
    return ActionResult(
        total=total,
        commutator_sq=ym_val,
        myers=cs_val,
        mass=mass_val,
        double_trace=dt_val,
    )


def compute_force(
    X: Matrices,
    N: int,
    alpha: float,
    mu2: float = 0.0,
    g2: float = 0.0,
) -> Matrices:
    """Compute the force F_a = -dS/dX_a for HMC (the negative gradient).

    The force is derived analytically:

    For the YM piece  S_YM = N * (-1/4) * Σ Tr([Xa,Xb]^2):
        dS_YM/dXa = N * (-1/2) * Σ_{b≠a} [Xb, [Xb, Xa]]
                   = N * (1/2) * Σ_{b≠a} [Xb, [Xa, Xb]]

    For the CS piece  S_CS = N * 2iα * Tr(X1[X2,X3]):
        dS_CS/dX1 = N * 2iα * [X2, X3]
        dS_CS/dX2 = N * 2iα * [X3, X1]
        dS_CS/dX3 = N * 2iα * [X1, X2]

    For the mass term  S_m = N * (μ²/2) * Σ Tr(Xa²):
        dS_m/dXa = N * μ² * Xa

    For the double trace  S_dt = (g2/N) * (Σ Tr(Xa²))²:
        dS_dt/dXa = (4 g2 / N) * (Σ Tr(Xb²)) * Xa

    Force: F_a = -dS/dXa
    We project onto traceless Hermitian after each computation.

    Returns
    -------
    tuple of three N × N Hermitian complex128 matrices (F1, F2, F3).
    """
    forces = []

    # Precompute the CS commutators in cyclic order:
    #   eps_{1,2,3} → [X2, X3], [X3, X1], [X1, X2]
    cs_comms = [
        commutator(X[1], X[2]),  # dS_CS/dX1  direction
        commutator(X[2], X[0]),  # dS_CS/dX2  direction
        commutator(X[0], X[1]),  # dS_CS/dX3  direction
    ]

    # For double-trace
    if g2 != 0.0:
        tr_sum = sum(np.trace(X[a] @ X[a]).real for a in range(3))
    else:
        tr_sum = 0.0

    for a in range(3):
        F_a = np.zeros((N, N), dtype=np.complex128)

        # YM contribution:  dS_YM/dXa = N * (1/2) * Σ_{b≠a} [Xb, [Xa, Xb]]
        for b in range(3):
            if b == a:
                continue
            C_ab = commutator(X[a], X[b])
            F_a += commutator(X[b], C_ab)  # [Xb, [Xa, Xb]]
        F_a *= N * 0.5

        # CS contribution: dS_CS/dXa = N * 2iα * eps-commutator
        F_a += N * (2.0j * alpha) * cs_comms[a]

        # Mass contribution: dS_m/dXa = N * μ² * Xa
        if mu2 != 0.0:
            F_a += N * mu2 * X[a]

        # Double-trace contribution: dS_dt/dXa = (4 g2 / N) * tr_sum * Xa
        if g2 != 0.0:
            F_a += (4.0 * g2 / N) * tr_sum * X[a]

        # Force = -gradient
        F_a = -F_a

        # Project back to traceless Hermitian
        F_a = (F_a + F_a.conj().T) / 2.0
        F_a -= (np.trace(F_a) / N) * np.eye(N, dtype=np.complex128)

        forces.append(F_a)

    return (forces[0], forces[1], forces[2])
