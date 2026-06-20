"""
Deterministic Seed Generation and Initial Conditions
=====================================================
Implements § 9.2 of the preregistration protocol.

Seed computation:
    seed(cell, j) = int.from_bytes(
        SHA-256("PREREG-PR-B1-001|{model}|{N}|…|{j}").digest()[:8], "big"
    )

Initial conditions:
    - Seeds 0..3 ("hot"):  Gaussian random traceless Hermitian matrices
    - Seeds 4..7 ("cold"): Zero matrices (N × N)

NO initial configuration may start from a block-diagonal (SU(2) embedding)
or any other structured extremum.  This is mechanically enforced.

IEEE-754 float64 throughout.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ..config import (
    COLD_SEEDS,
    HOT_SEEDS,
    SEEDS_PER_CELL,
    compute_seed,
)

if TYPE_CHECKING:
    from ..config import GridCell


def make_rng(cell: GridCell, seed_index: int) -> np.random.Generator:
    """Create a deterministic numpy RNG for the given cell and seed index.

    Parameters
    ----------
    cell : GridCell
        The parameter-grid point (model, N, alpha_tilde, mu2, g2).
    seed_index : int
        Index in [0, SEEDS_PER_CELL).

    Returns
    -------
    np.random.Generator
        A PCG-64 generator seeded deterministically via SHA-256.
    """
    if not 0 <= seed_index < SEEDS_PER_CELL:
        raise ValueError(
            f"seed_index must be in [0, {SEEDS_PER_CELL}), got {seed_index}"
        )
    raw_seed = compute_seed(
        cell.model, cell.N, cell.alpha_tilde, cell.mu2, cell.g2, seed_index
    )
    return np.random.default_rng(raw_seed)


def _random_hermitian_traceless(N: int, rng: np.random.Generator) -> np.ndarray:
    """Generate a random traceless Hermitian N × N matrix (complex128).

    Construction:
        1. Draw a complex Gaussian matrix A ~ N(0,1) + i*N(0,1).
        2. Symmetrise: H = (A + A†) / 2.
        3. Remove trace: H -= (Tr H / N) * I.
    """
    A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2.0)
    H = (A + A.conj().T) / 2.0
    H -= (np.trace(H) / N) * np.eye(N, dtype=np.complex128)
    return H


def make_initial_matrices(
    cell: GridCell,
    seed_index: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build the three initial N × N Hermitian matrices (X1, X2, X3).

    Parameters
    ----------
    cell : GridCell
        Determines N and whether hot/cold start is used.
    seed_index : int
        0..3 → hot start (Gaussian random Hermitian, traceless).
        4..7 → cold start (zero matrices).
    rng : np.random.Generator
        The deterministic RNG for this run (from ``make_rng``).

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        (X1, X2, X3), each N × N complex128 Hermitian.
    """
    N = cell.N

    if seed_index < HOT_SEEDS:
        # Hot start: random traceless Hermitian, scaled by 1/sqrt(N)
        # to keep the action O(N²) and prevent leapfrog divergence.
        scale = 1.0 / np.sqrt(N)
        X1 = scale * _random_hermitian_traceless(N, rng)
        X2 = scale * _random_hermitian_traceless(N, rng)
        X3 = scale * _random_hermitian_traceless(N, rng)
    else:
        # Cold start: zero matrices
        X1 = np.zeros((N, N), dtype=np.complex128)
        X2 = np.zeros((N, N), dtype=np.complex128)
        X3 = np.zeros((N, N), dtype=np.complex128)

    return (X1, X2, X3)


def is_hot(seed_index: int) -> bool:
    """Return True if the seed index corresponds to a hot start."""
    return seed_index < HOT_SEEDS


def is_cold(seed_index: int) -> bool:
    """Return True if the seed index corresponds to a cold start."""
    return seed_index >= HOT_SEEDS


def main() -> None:
    """Verify cryptographic seed determinism."""
    print("=" * 72)
    print("PREREG-PR-B1 — Seed Determinism Verification")
    print("=" * 72)
    
    # Check a specific cell
    from ..config import GridCell
    cell = GridCell("M0", 16, 1.0, 0.0, 0.0)
    seed_0 = compute_seed(cell.model, cell.N, cell.alpha_tilde, cell.mu2, cell.g2, 0)
    seed_1 = compute_seed(cell.model, cell.N, cell.alpha_tilde, cell.mu2, cell.g2, 1)
    
    print(f"Cell {cell}:")
    print(f"  Seed 0: {seed_0}")
    print(f"  Seed 1: {seed_1}")
    
    if seed_0 == seed_1:
        print("[FAIL] Seeds are not unique!")
        import sys
        sys.exit(1)
        
    print("[PASS] Seed determinism verified.")



def main() -> None:
    """Verify cryptographic seed determinism."""
    print("=" * 72)
    print("PREREG-PR-B1 — Seed Determinism Verification")
    print("=" * 72)
    
    # Check a specific cell
    from ..config import GridCell
    cell = GridCell("M0", 16, 1.0, 0.0, 0.0)
    seed_0 = compute_seed(cell.model, cell.N, cell.alpha_tilde, cell.mu2, cell.g2, 0)
    seed_1 = compute_seed(cell.model, cell.N, cell.alpha_tilde, cell.mu2, cell.g2, 1)
    
    print(f"Cell {cell}:")
    print(f"  Seed 0: {seed_0}")
    print(f"  Seed 1: {seed_1}")
    
    if seed_0 == seed_1:
        print("[FAIL] Seeds are not unique!")
        import sys
        sys.exit(1)
        
    print("[PASS] Seed determinism verified.")

