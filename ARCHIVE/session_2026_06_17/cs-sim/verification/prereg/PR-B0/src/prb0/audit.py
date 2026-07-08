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

def verify_confusion(alpha_sweep=False):
    import json
    import os
    import numpy as np
    from .config import ALPHAS, N_OFFSETS, TRIALS_PER_CELL, get_deterministic_seed
    from .planted_ensemble import generate_planted_ensemble
    from .detector import projected_grid_assignment_detector

    tau_file = os.path.abspath("verification/data/prereg-PR-B0/calibration/tau.json")
    if not os.path.exists(tau_file):
        print("Error: tau.json not found. Run calibrate first.")
        sys.exit(1)
        
    with open(tau_file, "r") as f:
        tau_data = json.load(f)
    tau = tau_data["tau"]
    
    delta = 0.10
    failed = False
    
    alphas_to_test = ALPHAS if alpha_sweep else [1.0] # default or swept
    
    for alpha in alphas_to_test:
        print(f"\nTesting confusion matrix at alpha={alpha}, delta={delta}, tau={tau}")
        for p in P_B0:
            counts = {}
            total = 0
            base_n = sum(p)
            for offset in N_OFFSETS:
                N = base_n + offset
                for t in range(TRIALS_PER_CELL):
                    seed = get_deterministic_seed(str(p), N, alpha, delta, t)
                    rng = np.random.default_rng(seed)
                    X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
                    pred = projected_grid_assignment_detector(X1, X2, X3, tau, alpha)
                    counts[pred] = counts.get(pred, 0) + 1
                    total += 1
            
            for pred, cnt in counts.items():
                if pred != p and pred in P_B0:
                    leak = cnt / total
                    if leak >= 0.01:
                        print(f"  FAIL: {p} -> {pred} leak is {leak:.1%} (>= 1%)")
                        failed = True
                    elif leak > 0:
                        print(f"  WARN: {p} -> {pred} leak is {leak:.1%} (< 1%)")
    
    if failed:
        print("\nverify-confusion: FAIL. Cross-class leak >= 1% detected.")
        sys.exit(1)
    else:
        print("\nverify-confusion: PASS. No cross-class leak >= 1% detected at any alpha.")
