"""
PR-B0.1 Tau Calibration.

Sweeps tau on synthetic planted data at delta=0.10.
Uses raw multiset comparison (C2 fix) and known alpha (C1 fix).
"""
import os
import json
import numpy as np
from .config import P_B0, N_OFFSETS, ALPHAS, TRIALS_PER_CELL, get_deterministic_seed
from .planted_ensemble import generate_planted_ensemble
from .detector import projected_grid_assignment_detector


def run_calibration():
    delta = 0.10
    taus = np.arange(0.05, 0.21, 0.01)

    total_configs = len(P_B0) * len(N_OFFSETS) * len(ALPHAS)

    tau_scores = {round(float(t), 2): 0 for t in taus}
    tau_results = {round(float(t), 2): [] for t in taus}

    print(f"PR-B0.1 calibration: {len(P_B0)} classes, {len(N_OFFSETS)} N-offsets, "
          f"{len(ALPHAS)} alphas, {TRIALS_PER_CELL} trials/cell")
    print(f"Tau sweep: {[round(float(t),2) for t in taus]}")

    for pi, p in enumerate(P_B0):
        base_n = sum(p)
        print(f"  Class {pi+1}/{len(P_B0)}: {p} (base_n={base_n})")
        for offset in N_OFFSETS:
            N = base_n + offset
            for alpha in ALPHAS:
                # Pre-generate all trials for this (class, N, alpha) cell
                trials_data = []
                for t in range(TRIALS_PER_CELL):
                    seed = get_deterministic_seed(str(p), N, alpha, delta, t)
                    rng = np.random.default_rng(seed)
                    X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
                    trials_data.append((X1, X2, X3))

                # Sweep tau on pre-generated data
                for tau in taus:
                    tau_key = round(float(tau), 2)
                    correct = 0
                    for X1, X2, X3 in trials_data:
                        # C1: pass known alpha; C2: compare raw multiset
                        pred = projected_grid_assignment_detector(X1, X2, X3, tau_key, alpha)
                        if pred == p:
                            correct += 1
                    rate = correct / TRIALS_PER_CELL
                    tau_results[tau_key].append(rate)
                    if rate >= 0.95:
                        tau_scores[tau_key] += 1

    # Find best tau: maximize area of >=0.95 region, with +/-0.02 stability
    best_tau = None
    best_score = -1

    for tau in taus:
        tau_key = round(float(tau), 2)
        score = tau_scores[tau_key]
        stable = True
        for d in [-0.02, -0.01, 0.01, 0.02]:
            t_adj = round(tau_key + d, 2)
            if t_adj in tau_scores:
                if tau_scores[t_adj] < score * 0.9:
                    stable = False

        if stable and score > best_score:
            best_score = score
            best_tau = tau_key

    if best_tau is None:
        best_tau = max(tau_scores, key=tau_scores.get)
        best_score = tau_scores[best_tau]
        print("Warning: No tau met strict stability criteria. Using max score.")

    print(f"Calibration complete. Frozen tau: {best_tau:.2f} "
          f"(score {best_score}/{total_configs})")

    # Per-class breakdown at best tau
    print("\nPer-class recovery rates at frozen tau:")
    idx = 0
    for p in P_B0:
        base_n = sum(p)
        for offset in N_OFFSETS:
            N = base_n + offset
            for alpha in ALPHAS:
                rate = tau_results[best_tau][idx]
                if rate < 0.95:
                    print(f"  {p} N={N} alpha={alpha}: {rate:.3f} < 0.95 FAIL")
                idx += 1

    out_dir = os.path.abspath("verification/data/prereg-PR-B0/calibration")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "tau.json"), "w") as f:
        json.dump({
            "tau": best_tau,
            "score": best_score,
            "total": total_configs,
            "version": "PR-B0.1"
        }, f, indent=2)
