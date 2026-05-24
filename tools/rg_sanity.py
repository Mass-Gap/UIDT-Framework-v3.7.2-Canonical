#!/usr/bin/env python3
"""
rg_sanity.py — UIDT v3.9 1-Loop RG Stability Scanner
Scans (kappa, lambda_S) under 1-loop RG running from IR to UV.
Output: verification/data/visualizations/rg_scan.csv

WARNING: β-functions are PLACEHOLDERS until physical UIDT β-functions are derived.
Evidence: [D] — prediction, not confirmed.
Kill-switch: if physical β-functions confirm RG-CONSTRAINT_FAIL → framework falsified.
"""
from mpmath import mp, mpf, fabs, pi, exp, log
import csv
from pathlib import Path
import sys

mp.dps = 80

KAPPA0   = mpf("0.500")
LAMBDA0  = mpf("5") / mpf("3") * KAPPA0**2   # = 5/12 exactly
MU0      = mpf("1.0")      # GeV
MU_END   = mpf("1e6")      # GeV
STEPS    = 500
RG_TOL   = mpf("1e-14")


def beta_kappa(kappa: mpf, lam: mpf) -> mpf:
    """1-loop placeholder dκ/d(ln μ). Replace with physical UIDT β."""
    return mpf("2") * kappa * lam / (mpf("16") * pi**2)


def beta_lambda(lam: mpf, kappa: mpf) -> mpf:
    """1-loop placeholder dλ_S/d(ln μ). Replace with physical UIDT β."""
    return (mpf("3") * lam**2 - mpf("5") * kappa**4 / (lam + mpf("1e-100"))) / (mpf("16") * pi**2)


def run_scan(
    kappa0: mpf = KAPPA0,
    lam0:   mpf = LAMBDA0,
    mu0:    mpf = MU0,
    mu_end: mpf = MU_END,
    steps:  int = STEPS,
) -> list:
    log_step = (log(mu_end) - log(mu0)) / steps
    kappa, lam, mu = kappa0, lam0, mu0
    rows = []
    for _ in range(steps):
        dk = beta_kappa(kappa, lam) * log_step
        dl = beta_lambda(lam, kappa) * log_step
        kappa += dk
        lam   += dl
        mu    *= exp(log_step)
        deltaRG = fabs(5 * kappa**2 - 3 * lam)
        rows.append({
            "mu":       mp.nstr(mu, 8),
            "kappa":    mp.nstr(kappa, 20),
            "lambda_S": mp.nstr(lam, 20),
            "deltaRG":  mp.nstr(deltaRG, 10),
            "status":   "OK" if deltaRG < RG_TOL else "[RG_CONSTRAINT_FAIL]",
        })
    return rows


def main():
    out = Path("verification/data/visualizations/rg_scan.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = run_scan()
    fields = ["mu", "kappa", "lambda_S", "deltaRG", "status"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    fails = [r for r in rows if "FAIL" in r["status"]]
    print(f"RG scan → {out} | Steps: {STEPS} | Failures: {len(fails)}/{STEPS}")
    if fails:
        print(f"  First failure at μ={fails[0]['mu']} GeV, ΔRG={fails[0]['deltaRG']}")
        print("  INTERPRETATION: Placeholder β-functions used. Physical β required.")
        sys.exit(1)


if __name__ == "__main__":
    main()
