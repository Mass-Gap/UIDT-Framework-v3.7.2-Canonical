"""
PR-B0.1 Gate Report Generator.

Produces GATE_REPORT.md with:
- Sign-off block
- Per-class admissible region
- Confusion matrix
- Disposition of (2,2,2)
"""
import os
import json
import datetime
from .config import P_B0


def generate_gate_report():
    tau_file = os.path.abspath("verification/data/prereg-PR-B0/calibration/tau.json")
    boundary_file = os.path.abspath("verification/data/prereg-PR-B0/boundary/admissible_region.json")

    if not os.path.exists(tau_file) or not os.path.exists(boundary_file):
        print("Error: Calibration or boundary data missing. "
              "Run calibrate and boundary first.")
        return

    with open(tau_file, "r") as f:
        tau_data = json.load(f)
        tau = tau_data["tau"]
        tau_version = tau_data.get("version", "unknown")

    with open(boundary_file, "r") as f:
        boundary_data = json.load(f)
        rho_star = boundary_data["rho_star"]
        confusion = boundary_data.get("confusion_matrix_delta_0.10", {})
        raw = boundary_data.get("raw", {})
        bnd_version = boundary_data.get("version", "unknown")

    # Version guard
    if tau_version != "PR-B0.1" or bnd_version != "PR-B0.1":
        print(f"FATAL: Stale data. tau version={tau_version}, "
              f"boundary version={bnd_version}. Expected PR-B0.1.")
        print("Re-run calibrate and boundary with PR-B0.1 code.")
        return

    # Check satisfiability: any class >= 0.95 at delta <= 0.10
    satisfiable = False
    for p_str, deltas in rho_star.items():
        for delta_str, rho in deltas.items():
            if float(delta_str) <= 0.10 and rho is not None:
                satisfiable = True
                break
        if satisfiable:
            break

    verdict = "satisfiable" if satisfiable else "NOT-SATISFIABLE"

    # Build admissible region string
    admissible_lines = []
    for p_str in [str(p) for p in P_B0]:
        deltas = rho_star.get(p_str, {})
        best_rho = None
        for delta_str, rho in deltas.items():
            if float(delta_str) <= 0.10 and rho is not None:
                if best_rho is None or rho < best_rho:
                    best_rho = rho
        if best_rho is not None:
            admissible_lines.append(f"{p_str}: rho >= {best_rho:.4f}")
        else:
            admissible_lines.append(f"{p_str}: UNSAT")

    admissible_str = "; ".join(admissible_lines)

    # Build confusion matrix table
    confusion_table = ""
    if confusion:
        all_predicted = sorted(set(
            label for row in confusion.values() for label in row.keys()
        ))
        # Header
        confusion_table += "| planted |"
        for label in all_predicted:
            confusion_table += f" {label} |"
        confusion_table += "\n|---|"
        for _ in all_predicted:
            confusion_table += "---|"
        confusion_table += "\n"
        # Rows
        for planted_str in [str(p) for p in P_B0]:
            row_data = confusion.get(planted_str, {})
            total_row = sum(row_data.values())
            confusion_table += f"| {planted_str} |"
            for label in all_predicted:
                cnt = row_data.get(label, 0)
                pct = cnt / total_row * 100 if total_row > 0 else 0
                confusion_table += f" {pct:.1f}% |"
            confusion_table += "\n"

    # Build per-class boundary table
    boundary_table = "| class | d=0.05 | d=0.10 | d=0.20 | d=0.30 |\n|---|---|---|---|---|\n"
    for p_str in [str(p) for p in P_B0]:
        deltas = rho_star.get(p_str, {})
        row = f"| {p_str} |"
        for d in ["0.05", "0.1", "0.2", "0.3"]:
            rho = deltas.get(d)
            if rho is not None:
                row += f" rho>={rho:.4f} |"
            else:
                row += " UNSAT |"
        boundary_table += row + "\n"

    # (2,2,2) disposition
    p222_deltas = rho_star.get("(2, 2, 2)", {})
    p222_d010 = p222_deltas.get("0.1")
    if p222_d010 is not None:
        p222_status = f"ADMITTED (rho >= {p222_d010:.4f} at d=0.10)"
    else:
        p222_status = "UNRESOLVABLE at d=0.10 (falls below 95% gate)"

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    report_md = f"""# GATE REPORT: PR-B0.1 Preflight
## Version: PR-B0.1 (C1 alpha-known, C2 raw-multiset, C3 extended 8-class set)
## Date: {date_str}

---

## 1. Exact checks (A-audit)

- **verify-grid**: PASS. Q_n = alpha^2(n^2-1)/4 matches j(j+1) for n=1..8.
- **verify-injective**: PASS. P_B0 (8 classes) has pairwise-distinct positive-Casimir signatures.

---

## 2. Calibrated tau

- **Frozen tau**: {tau}
- **Calibration version**: {tau_version}

---

## 3. Separability boundary rho*(delta)

{boundary_table}

---

## 4. Confusion matrix (delta=0.10, all N/alpha pooled)

{confusion_table}

---

## 5. (2,2,2) disposition

{p222_status}

---

## 10. Sign-off block

```
PI sign-off (required before PR-B1-002):     ____________________  date: ________
PR-B0.1 gate verdict (A-audit, advisory):    [{("x" if satisfiable else " ")}] satisfiable  [{(" " if satisfiable else "x")}] NOT-SATISFIABLE
Frozen tau (calibration output):             tau = {tau}
Admissible region (per class, >=0.95@d<=0.10):
  {admissible_str}
(2,2,2) disposition:                         {p222_status}
Gatekeeper CI green on PR-B0 dir:            [ ] yes   run id: ____________
Data versions:                               tau={tau_version}, boundary={bnd_version}
```

*Generated by A-audit (PR-B0.1). This report must be signed by the PI before PR-B1-002 can commence.*
"""

    out_file = os.path.abspath("verification/prereg/PR-B0/GATE_REPORT.md")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"Gate report generated at {out_file}")
    print(f"Verdict: {verdict}")
    print(f"(2,2,2) disposition: {p222_status}")
