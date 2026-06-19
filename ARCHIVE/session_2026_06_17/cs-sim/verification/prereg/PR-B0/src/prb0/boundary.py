"""
PR-B0.1 Separability Boundary Map.

Produces rho*(delta) per class on the production grid.
Uses known alpha (C1), raw multiset comparison (C2), extended 8-class set (C3).
Includes confusion matrix output.
"""
import os
import json
import numpy as np
from .config import P_B0, N_OFFSETS, ALPHAS, TRIALS_PER_CELL, DELTA_SWEEP, get_deterministic_seed
from .planted_ensemble import generate_planted_ensemble
from .detector import projected_grid_assignment_detector


def run_boundary():
    tau_file = os.path.abspath("verification/data/prereg-PR-B0/calibration/tau.json")
    if not os.path.exists(tau_file):
        print("Error: tau.json not found. Run calibrate first.")
        return

    with open(tau_file, "r") as f:
        tau_data = json.load(f)
        tau = tau_data["tau"]
        version = tau_data.get("version", "unknown")

    if version != "PR-B0.2":
        print(f"Warning: tau.json version is '{version}', expected 'PR-B0.2'. "
              "Stale calibration data may produce invalid results.")

    print(f"Loaded frozen tau = {tau} (version {version}). Computing boundary map...")

    results = {}
    # Confusion matrix: for each planted class, what does the detector output?
    # confusion[planted_str][predicted_str] = count
    confusion = {str(p): {} for p in P_B0}

    for pi, p in enumerate(P_B0):
        base_n = sum(p)
        class_results = []
        print(f"  Class {pi+1}/{len(P_B0)}: {p}")

        for delta in DELTA_SWEEP:
            for offset in N_OFFSETS:
                N = base_n + offset
                rho = base_n / N

                correct = 0
                total = TRIALS_PER_CELL * len(ALPHAS)
                for alpha in ALPHAS:
                    for t in range(TRIALS_PER_CELL):
                        seed = get_deterministic_seed(str(p), N, alpha, delta, t)
                        rng = np.random.default_rng(seed)
                        X1, X2, X3 = generate_planted_ensemble(p, N, alpha, delta, rng)
                        # C1: pass known alpha
                        pred = projected_grid_assignment_detector(X1, X2, X3, tau, alpha)
                        # C2: compare raw multiset
                        if pred == p:
                            correct += 1

                        # Track confusion (at delta=0.10 only, to keep data manageable)
                        if abs(delta - 0.10) < 1e-6:
                            pred_str = str(pred)
                            if pred_str not in confusion[str(p)]:
                                confusion[str(p)][pred_str] = 0
                            confusion[str(p)][pred_str] += 1

                rate = correct / total
                class_results.append({
                    "delta": delta,
                    "N": N,
                    "rho": round(rho, 4),
                    "rate": round(rate, 4)
                })
        results[str(p)] = class_results

    # Extract rho*(delta) per class
    rho_star = {}
    for p_str, rows in results.items():
        rho_star[p_str] = {}
        for delta in DELTA_SWEEP:
            valid_rhos = [r["rho"] for r in rows
                          if abs(r["delta"] - delta) < 1e-6 and r["rate"] >= 0.95]
            if valid_rhos:
                rho_star[p_str][str(delta)] = min(valid_rhos)
            else:
                rho_star[p_str][str(delta)] = None

    out_dir = os.path.abspath("verification/data/prereg-PR-B0/boundary")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "admissible_region.json"), "w", encoding="utf-8") as f:
        json.dump({
            "version": "PR-B0.2",
            "rho_star": rho_star,
            "confusion_matrix_delta_0.10": confusion,
            "raw": results
        }, f, indent=2)

    # Print summary
    print("\n=== PR-B0.2 Boundary Summary ===")
    for p_str, deltas in rho_star.items():
        line = f"  {p_str}: "
        for d_str, rho in deltas.items():
            if rho is not None:
                line += f"d={d_str}->rho>={rho:.4f}  "
            else:
                line += f"d={d_str}->UNSAT  "
        print(line)

    print("\n=== Confusion Matrix (delta=0.10, all N/alpha pooled) ===")
    all_labels = sorted(set(
        label for row in confusion.values() for label in row.keys()
    ))
    header = f"{'planted':>20s} | " + " | ".join(f"{l:>12s}" for l in all_labels)
    print(header)
    print("-" * len(header))
    for planted_str in [str(p) for p in P_B0]:
        row_data = confusion[planted_str]
        total_row = sum(row_data.values())
        cells = []
        for label in all_labels:
            cnt = row_data.get(label, 0)
            pct = cnt / total_row * 100 if total_row > 0 else 0
            cells.append(f"{pct:>10.1f}%")
        print(f"{planted_str:>20s} | " + " | ".join(cells))

    print("\nBoundary map and confusion matrix saved.")
