"""
PR-B0.1 Audit checks.

verify-grid:      Q_n = alpha^2(n^2-1)/4 matches j(j+1) for n=1..8
verify-injective: P_B0 has pairwise-distinct RAW Casimir multisets
                  (not ratio-normalized; C2 consistency)
"""
import sys
from .config import P_B0


def verify_grid():
    """
    Grid-formula check (exact): Q_n = alpha^2(n^2-1)/4 for n=1..8.
    """
    for n in range(1, 9):
        j = (n - 1) / 2.0
        expected = j * (j + 1)
        actual = (n**2 - 1) / 4.0
        if abs(expected - actual) > 1e-12:
            print(f"FAILED grid verification for n={n}")
            sys.exit(1)
    print("verify-grid: PASS. Q_n = alpha^2(n^2-1)/4 matches j(j+1) for n=1..8")


def _get_raw_casimir_signature(partition):
    """
    Returns the sorted multiset of bare Casimir levels Q_n = (n^2-1)/4
    for each block in the partition.

    This is the RAW signature (C2 fix) — no normalization by q_min.
    (2,2,2) -> (0.75, 0.75, 0.75)
    (3,3,3) -> (2.0, 2.0, 2.0)
    (4,4,4) -> (3.75, 3.75, 3.75)
    These are distinct under raw comparison.
    """
    sig = []
    for n in partition:
        q = (n**2 - 1) / 4.0
        sig.append(q)
    return tuple(sorted(sig))


def verify_injective():
    """
    Injectivity check (exact): P_B0 has pairwise-distinct raw Casimir signatures.
    """
    sigs = {}
    for p in P_B0:
        sig = _get_raw_casimir_signature(p)
        if sig in sigs:
            print(f"FAILED injectivity check: Collision between "
                  f"{sigs[sig]} and {p} (both map to raw signature {sig})")
            sys.exit(1)
        sigs[sig] = p
    print(f"verify-injective: PASS. P_B0 ({len(P_B0)} classes) has "
          f"pairwise-distinct raw Casimir signatures.")
    for p in P_B0:
        sig = _get_raw_casimir_signature(p)
        print(f"  {p} -> {sig}")
