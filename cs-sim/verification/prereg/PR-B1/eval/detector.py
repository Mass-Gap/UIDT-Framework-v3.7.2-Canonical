"""
AG-Eval Detector — KDE Partition Detector (Sec. 4.1)
=====================================================
Frozen pipeline:
  1. Compute eigenvalues of Q = X_1^2 + X_2^2 + X_3^2.
  2. Sort eigenvalues ascending.
  3. KDE with Gaussian kernel, Silverman's rule-of-thumb bandwidth (FROZEN).
  4. Cluster boundaries: local minima of KDE below 20 % of global KDE max.
  5. Discard clusters with m_j < 2 (defect modes).
  6. Output: sorted empirical partition multiset {m_j}.

KDE itself is float64 throughout (stochastic, not proof-critical).
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from numpy.typing import NDArray

from ..config import KDE_MIN_FRACTION, KDE_MIN_CLUSTER_SIZE


# ── Silverman bandwidth (frozen) ────────────────────────────────────────────

def _silverman_bandwidth(data: NDArray[np.float64]) -> float:
    """Compute Silverman's rule-of-thumb bandwidth.

    h = 0.9 * min(std, IQR / 1.34) * n^{-1/5}
    """
    n = len(data)
    if n < 2:
        return 1.0

    std = float(np.std(data, ddof=1))
    q75, q25 = float(np.percentile(data, 75)), float(np.percentile(data, 25))
    iqr = q75 - q25

    # Guard against degenerate case
    spread = min(std, iqr / 1.34) if iqr > 0.0 else std
    if spread <= 0.0:
        spread = 1.0

    return 0.9 * spread * (n ** (-0.2))


# ── Gaussian KDE evaluation ────────────────────────────────────────────────

def _kde_evaluate(
    data: NDArray[np.float64],
    grid: NDArray[np.float64],
    bandwidth: float,
) -> NDArray[np.float64]:
    """Evaluate Gaussian KDE on *grid* given *data* and fixed *bandwidth*.

    Returns the KDE density estimate at each grid point (float64).
    """
    n = len(data)
    # Vectorised: (grid[:, None] - data[None, :]) / h
    u = (grid[:, np.newaxis] - data[np.newaxis, :]) / bandwidth
    # Gaussian kernel: (1 / sqrt(2π)) * exp(-u^2 / 2)
    kernel_vals = np.exp(-0.5 * u * u) / np.sqrt(2.0 * np.pi)
    density = kernel_vals.sum(axis=1) / (n * bandwidth)
    return density


# ── Local-minima finder ─────────────────────────────────────────────────────

def _find_local_minima(
    density: NDArray[np.float64],
) -> list[int]:
    """Return indices of local minima in *density* (interior points only)."""
    minima: list[int] = []
    for i in range(1, len(density) - 1):
        if density[i] < density[i - 1] and density[i] < density[i + 1]:
            minima.append(i)
    return minima


# ── Public API ──────────────────────────────────────────────────────────────

def eigenvalues_of_Q(
    X1: NDArray[np.complex128],
    X2: NDArray[np.complex128],
    X3: NDArray[np.complex128],
) -> NDArray[np.float64]:
    """Compute sorted eigenvalues of the Casimir-like matrix Q = X1² + X2² + X3².

    Parameters
    ----------
    X1, X2, X3 : complex128 Hermitian N × N matrices.

    Returns
    -------
    1-D float64 array of N eigenvalues, sorted ascending.
    """
    Q = X1 @ X1 + X2 @ X2 + X3 @ X3
    eigs = np.linalg.eigvalsh(Q)  # real eigenvalues, ascending
    return np.sort(eigs.astype(np.float64))


def detect_partition(
    eigenvalues: NDArray[np.float64],
    kde_grid_points: int = 1024,
) -> tuple[tuple[int, ...], dict[str, object]]:
    """Run the frozen KDE partition detector on sorted eigenvalues.

    Parameters
    ----------
    eigenvalues : 1-D float64, sorted ascending.
    kde_grid_points : int
        Number of equispaced grid points for KDE evaluation.

    Returns
    -------
    partition : tuple[int, ...]
        Sorted ascending empirical partition multiset (clusters with m_j >= 2).
    diagnostics : dict
        Bandwidth, KDE grid, density, boundary indices, all cluster sizes,
        number of defect modes discarded.
    """
    n = len(eigenvalues)
    if n == 0:
        return (), {"bandwidth": 0.0, "n_defect_discarded": 0}

    # Single eigenvalue → trivial partition
    if n == 1:
        return (), {"bandwidth": 0.0, "n_defect_discarded": 1}

    # Step 1: Silverman bandwidth (frozen formula)
    bandwidth = _silverman_bandwidth(eigenvalues)

    # Step 2: evaluate KDE on equispaced grid spanning data range
    lo = float(eigenvalues[0]) - 3.0 * bandwidth
    hi = float(eigenvalues[-1]) + 3.0 * bandwidth
    grid = np.linspace(lo, hi, kde_grid_points)
    density = _kde_evaluate(eigenvalues, grid, bandwidth)

    # Step 3: find local minima below threshold
    global_max = float(density.max())
    threshold = KDE_MIN_FRACTION * global_max

    minima_indices = _find_local_minima(density)
    boundary_indices = [
        idx for idx in minima_indices if density[idx] < threshold
    ]

    # Step 4: map eigenvalues to clusters via grid boundaries
    boundary_values = [float(grid[idx]) for idx in boundary_indices]
    # Assign each eigenvalue to a cluster
    cluster_labels = np.searchsorted(boundary_values, eigenvalues, side="right")
    # cluster_labels[i] ∈ {0, 1, ..., len(boundary_values)}

    # Count cluster sizes
    n_clusters = len(boundary_values) + 1
    all_sizes: list[int] = []
    for c in range(n_clusters):
        m_j = int(np.sum(cluster_labels == c))
        all_sizes.append(m_j)

    # Step 5: discard defect modes and resolve degenerate blocks using Casimirs
    kept: list[int] = []
    n_defect = 0
    for c in range(n_clusters):
        m_j = int(np.sum(cluster_labels == c))
        if m_j == 0:
            continue
            
        cluster_eigs = eigenvalues[cluster_labels == c]
        mean_Q = float(np.mean(cluster_eigs))
        
        # Discard vacuum cluster
        if mean_Q < 0.2:
            continue
            
        # Deduce physical block size n from SU(2) Casimir Q = (n^2 - 1) / 4 -> n = sqrt(4Q + 1)
        n_block = int(np.round(np.sqrt(max(1.0, 4.0 * mean_Q + 1.0))))
        
        if n_block <= 0:
            continue
            
        # A block of size n_block provides n_block eigenvalues.
        # So m_j eigenvalues means m_j / n_block copies of this block.
        n_copies = max(1, int(np.round(m_j / float(n_block))))
        
        for _ in range(n_copies):
            if n_block >= KDE_MIN_CLUSTER_SIZE:
                kept.append(n_block)
            else:
                n_defect += 1

    partition = tuple(sorted(kept))

    diagnostics: dict[str, object] = {
        "bandwidth": bandwidth,
        "kde_grid": grid,
        "kde_density": density,
        "global_max": global_max,
        "threshold": threshold,
        "boundary_indices": boundary_indices,
        "boundary_values": boundary_values,
        "all_cluster_sizes": all_sizes,
        "n_defect_discarded": n_defect,
    }

    return partition, diagnostics


def detect_partition_from_matrices(
    X1: NDArray[np.complex128],
    X2: NDArray[np.complex128],
    X3: NDArray[np.complex128],
    kde_grid_points: int = 1024,
) -> tuple[tuple[int, ...], dict[str, object]]:
    """Convenience: eigenvalue extraction + partition detection in one call."""
    eigs = eigenvalues_of_Q(X1, X2, X3)
    return detect_partition(eigs, kde_grid_points=kde_grid_points)
