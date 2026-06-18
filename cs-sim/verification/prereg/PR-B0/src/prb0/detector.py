"""
PR-B0.1 Projected Grid-Assignment Detector.

C1 FIX: alpha is KNOWN (passed as argument), not estimated from data.
C2 FIX: Returns raw sorted block multiset, NOT gcd-reduced ratio class.
         Comparison against planted partition uses raw tuples.
"""
import numpy as np
import math
from collections import defaultdict


def projected_grid_assignment_detector(
    X1: np.ndarray, X2: np.ndarray, X3: np.ndarray,
    tau: float, alpha: float
) -> tuple:
    """
    Deterministic grid-assignment detector.

    Parameters
    ----------
    X1, X2, X3 : N x N Hermitian matrices
    tau : grid tolerance (frozen, class-symmetric scalar)
    alpha : the KNOWN coupling constant (C1 fix: no estimation)

    Returns
    -------
    tuple : raw sorted block sizes (n_1, n_2, ...), each n_i >= 2.
            Empty tuple () if unresolvable.
    """
    a2 = alpha ** 2

    def Q_bare(n):
        """Bare Casimir level for block size n: (n^2 - 1)/4."""
        return (n ** 2 - 1) / 4.0

    # 1. C <- (X_1^2 + X_2^2 + X_3^2); symmetrize; w <- eigvalsh(C) ascending.
    C = X1 @ X1 + X2 @ X2 + X3 @ X3
    C = (C + C.conj().T) / 2
    w = np.linalg.eigvalsh(C)

    # 2. PROJECTION (kill the padding band):
    #    logs <- log(clip(w, 1e-9*w_max, inf))
    #    cut  <- argmax(diff(logs))   # largest multiplicative gap
    #    Q+   <- w[cut+1:]            # retained non-kernel spectrum
    w_max = max(w[-1], 1e-15)
    logs = np.log(np.clip(w, 1e-9 * w_max, None))
    diffs = np.diff(logs)
    if len(diffs) == 0:
        return ()
    cut = int(np.argmax(diffs))
    Q_plus = w[cut + 1:]
    if len(Q_plus) == 0:
        return ()

    # 3. ASSIGN: for each q in Q+, map to nearest grid level using KNOWN alpha.
    counts = defaultdict(int)
    for q in Q_plus:
        jj = q / a2  # Q_bare = q / alpha^2
        n_float = math.sqrt(max(4 * jj + 1, 0))
        n_star = max(2, round(n_float))

        diff_val = abs(Q_bare(n_star) - jj)
        tol_val = tau * max(Q_bare(n_star), 0.75)
        if diff_val <= tol_val:
            counts[n_star] += 1

    # 4. BLOCKS: for each assigned level, number of blocks = count / n
    blocks = []
    for n_val, cnt in sorted(counts.items()):
        copies = round(cnt / n_val)
        blocks.extend([n_val] * copies)

    if not blocks:
        return ()

    # 5. OUTPUT: raw sorted multiset — NO gcd reduction (C2 fix).
    return tuple(sorted(blocks))
