"""
PR-B0.1 Gatekeeper CI.

Runs all automated checks and produces a run ID.
This is the CI-equivalent that fills the empty Gatekeeper line in GATE_REPORT.md.

Usage: python -m prb0 ci
"""
import os
import sys
import json
import hashlib
import datetime


def run_ci():
    """
    Gatekeeper CI sequence:
    1. verify-grid (exact)
    2. verify-injective (exact)
    3. Version guard: tau.json and admissible_region.json must be PR-B0.2
    4. No class-literal leakage in detector.py
    5. Non-overlap check: no two P_B0 classes confused with each other in confusion matrix
    6. tau stability check: frozen tau is stable under +/-0.02
    """
    from .audit import verify_grid, verify_injective, verify_confusion
    from .config import P_B0

    run_id = f"CI-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"=== PR-B0.2 Gatekeeper CI ===")
    print(f"Run ID: {run_id}")
    failures = []

    # 1. verify-grid
    print("\n[1/6] verify-grid...")
    try:
        verify_grid()
    except SystemExit:
        failures.append("verify-grid FAILED")

    # 2. verify-injective
    print("\n[2/7] verify-injective...")
    try:
        verify_injective()
    except SystemExit:
        failures.append("verify-injective FAILED")

    # 2b. verify-confusion (alpha-sweep)
    print("\n[2b/7] verify-confusion (alpha-sweep)...")
    try:
        verify_confusion(alpha_sweep=True)
    except SystemExit:
        failures.append("verify-confusion FAILED (cross-class leak >= 1%)")

    # 3. Version guard
    print("\n[3/7] Version guard...")
    tau_file = os.path.abspath("verification/data/prereg-PR-B0/calibration/tau.json")
    bnd_file = os.path.abspath("verification/data/prereg-PR-B0/boundary/admissible_region.json")

    for label, path in [("tau.json", tau_file), ("admissible_region.json", bnd_file)]:
        if not os.path.exists(path):
            failures.append(f"{label} missing")
            print(f"  FAIL: {label} not found at {path}")
            continue
        with open(path, "r") as f:
            data = json.load(f)
        ver = data.get("version", "MISSING")
        if ver != "PR-B0.2":
            failures.append(f"{label} version={ver}, expected PR-B0.2")
            print(f"  FAIL: {label} version={ver}")
        else:
            print(f"  OK: {label} version={ver}")

    # 4. No class-literal leakage in detector.py
    print("\n[4/7] Class-literal leakage check...")
    det_path = os.path.abspath("verification/prereg/PR-B0/src/prb0/detector.py")
    with open(det_path, "r", encoding="utf-8") as f:
        det_src = f.read()
    forbidden = ["(2, 3)", "(2,3)", "(3, 4)", "(3,4)", "1:2:3", "target"]
    for pat in forbidden:
        # Skip comments and docstrings heuristically: only flag if in executable code
        for i, line in enumerate(det_src.splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            if pat in stripped:
                failures.append(f"detector.py line {i}: class literal '{pat}' in executable code")
                print(f"  FAIL: line {i} contains '{pat}'")
    if not any("class literal" in f for f in failures):
        print("  OK: No class-literal leakage in detector.py")

    # 5. Non-overlap check from confusion matrix
    print("\n[5/7] Non-overlap check (confusion matrix)...")
    if os.path.exists(bnd_file):
        with open(bnd_file, "r") as f:
            bnd_data = json.load(f)
        confusion = bnd_data.get("confusion_matrix_delta_0.10", {})
        p_b0_strs = [str(p) for p in P_B0]
        cross_confusion = False
        for planted_str in p_b0_strs:
            row = confusion.get(planted_str, {})
            for pred_str, cnt in row.items():
                if pred_str in p_b0_strs and pred_str != planted_str and cnt > 0:
                    total_row = sum(row.values())
                    pct = cnt / total_row * 100 if total_row > 0 else 0
                    print(f"  CROSS-CONFUSION: {planted_str} -> {pred_str}: {pct:.1f}%")
                    cross_confusion = True
        if cross_confusion:
            failures.append("Cross-class confusion detected between P_B0 members")
        else:
            print("  OK: No cross-class confusion between P_B0 members")
    else:
        failures.append("Cannot check non-overlap: admissible_region.json missing")

    # 6. Tau stability check
    print("\n[6/7] Tau stability check...")
    if os.path.exists(tau_file):
        with open(tau_file, "r") as f:
            tau_data = json.load(f)
        tau_curve = tau_data.get("tau_sweep_curve", {})
        frozen_tau = tau_data.get("tau")
        if tau_curve:
            frozen_score = tau_curve.get(str(frozen_tau), {}).get("score", 0)
            stable = True
            for d in [-0.02, -0.01, 0.01, 0.02]:
                neighbor = str(round(frozen_tau + d, 2))
                if neighbor in tau_curve:
                    n_score = tau_curve[neighbor]["score"]
                    if n_score < frozen_score * 0.9:
                        stable = False
                        print(f"  UNSTABLE: tau={neighbor} score={n_score} "
                              f"< 0.9*{frozen_score}={frozen_score*0.9:.0f}")
            if stable:
                print(f"  OK: tau={frozen_tau} is stable (+/-0.02)")
            else:
                failures.append(f"tau={frozen_tau} fails stability under +/-0.02")
        else:
            print("  SKIP: tau_sweep_curve not in tau.json (re-run calibrate)")
            failures.append("tau_sweep_curve missing from tau.json")
    else:
        failures.append("tau.json missing")

    # Verdict
    print(f"\n=== CI Verdict ===")
    if failures:
        print(f"FAILED ({len(failures)} issue(s)):")
        for f in failures:
            print(f"  - {f}")
        verdict = "FAIL"
    else:
        print("ALL CHECKS PASSED")
        verdict = "PASS"

    # Write CI result
    ci_result = {
        "run_id": run_id,
        "verdict": verdict,
        "failures": failures,
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "PR-B0.2"
    }
    ci_dir = os.path.abspath("verification/data/prereg-PR-B0/ci")
    os.makedirs(ci_dir, exist_ok=True)
    with open(os.path.join(ci_dir, "ci_result.json"), "w") as f:
        json.dump(ci_result, f, indent=2)

    print(f"\nCI result saved. Run ID: {run_id}")
    return verdict, run_id
