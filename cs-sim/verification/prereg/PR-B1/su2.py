"""
SU(2) Irreducible Representation Generators
=============================================
Provides the spin-j generators L_a^{(n)} for constructing block-diagonal
matrix configurations.  Used by:
  - Detector validation (planted ensembles, Sec. 4.5)
  - Cold-start initial conditions (classical extrema)

NOT used by simulation dynamics (HMC/Metropolis).
No partition information leaks into the simulation through this module.

All arithmetic is IEEE-754 float64 (stochastic simulation, not proof-critical).
"""

from __future__ import annotations

import numpy as np


def su2_generator(n: int, component: int) -> np.ndarray:
    """Return the spin-(n-1)/2 representation matrix L_a for a = component.

    Parameters
    ----------
    n : int
        Dimension of the irrep (n >= 1).  The spin is j = (n-1)/2.
    component : int
        Which generator: 0 -> L_1 (L_x), 1 -> L_2 (L_y), 2 -> L_3 (L_z).

    Returns
    -------
    np.ndarray
        Hermitian n x n matrix (complex128).
    """
    if n < 1:
        raise ValueError(f"Irrep dimension must be >= 1, got {n}")
    if n == 1:
        return np.zeros((1, 1), dtype=np.complex128)

    j = (n - 1) / 2.0
    m_vals = np.arange(j, -j - 0.5, -1.0)  # m = j, j-1, ..., -j

    if component == 2:
        # L_z = diag(j, j-1, ..., -j)
        return np.diag(m_vals).astype(np.complex128)

    # Raising/lowering matrix elements:
    # <m+1|L_+|m> = sqrt(j(j+1) - m(m+1)) = sqrt((j-m)(j+m+1))
    off_diag = np.array([
        np.sqrt(j * (j + 1) - m_vals[i] * (m_vals[i] - 1))
        for i in range(1, n)
    ])

    L_plus = np.zeros((n, n), dtype=np.complex128)
    for i in range(n - 1):
        L_plus[i, i + 1] = off_diag[i]
    L_minus = L_plus.T.conj()

    if component == 0:
        # L_x = (L_+ + L_-) / 2
        return (L_plus + L_minus) / 2.0
    elif component == 1:
        # L_y = (L_+ - L_-) / (2i)
        return (L_plus - L_minus) / (2.0j)
    else:
        raise ValueError(f"component must be 0, 1, or 2, got {component}")


def su2_generators(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return all three SU(2) generators for the n-dimensional irrep.

    Returns (L_1, L_2, L_3), each n x n Hermitian complex128.
    """
    return (su2_generator(n, 0), su2_generator(n, 1), su2_generator(n, 2))


def block_diagonal_config(
    partition: tuple[int, ...],
    N: int,
    alpha: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build block-diagonal classical extremum X_a = alpha * (L_a^{(n1)} ⊕ ... ⊕ L_a^{(nk)} ⊕ 0_z).

    Parameters
    ----------
    partition : tuple[int, ...]
        Irrep dimensions (n_1, ..., n_k).  Sum must be <= N.
    N : int
        Total matrix size.  z = N - sum(partition) zero-padding rows/cols.
    alpha : float
        Overall coupling scale.

    Returns
    -------
    tuple of three N x N Hermitian complex128 matrices (X_1, X_2, X_3).
    """
    if sum(partition) > N:
        raise ValueError(
            f"Sum of partition {partition} = {sum(partition)} exceeds N = {N}"
        )
    z = N - sum(partition)

    result = []
    for a in range(3):
        blocks = []
        for n_i in partition:
            blocks.append(alpha * su2_generator(n_i, a))
        if z > 0:
            blocks.append(np.zeros((z, z), dtype=np.complex128))

        # Build block-diagonal matrix
        from scipy.linalg import block_diag
        result.append(block_diag(*blocks))

    return (result[0], result[1], result[2])


def partition_from_ratio_class(
    ratio_class: tuple[int, ...], N: int
) -> tuple[int, ...]:
    """Map a ratio class to concrete irrep dimensions at matrix size N.

    The partition is ratio_class scaled so that sum(partition) <= N.
    The scaling factor is floor(N / sum(ratio_class)), and any remainder
    is distributed as zero-padding.

    Parameters
    ----------
    ratio_class : tuple[int, ...]
        e.g., (1, 2, 3) for the [1:2:3] class.
    N : int
        Matrix size.

    Returns
    -------
    tuple[int, ...]
        Concrete irrep dimensions.
    """
    total_ratio = sum(ratio_class)
    scale = N // total_ratio
    if scale < 1:
        raise ValueError(
            f"N={N} too small for ratio class {ratio_class} "
            f"(need at least {total_ratio})"
        )
    return tuple(r * scale for r in ratio_class)
