#!/usr/bin/env python3
"""
tools/vacuum_suppression.py  —  UIDT v3.9 Vacuum Suppression Analyser
=======================================================================
Objective
---------
Quantify the fine-tuning required to reproduce the observed vacuum energy
density ρ_vac^obs = 2.45e-47 GeV⁴ [C] via the 99-step suppression formula:

    ρ_vac^obs = ρ_vac^QFT × π⁻² × ∏_{n=1}^{99} f_n(g)

where ρ_vac^QFT ~ (Λ_Planck)^4 ~ 10^76 GeV⁴ (QFT cut-off estimate).

Parametric f_n family
---------------------
Absence of explicit f_n definitions in CANONICAL/ forces parametric treatment.
We test three families:

  Family A — Exponential:
      f_n(g) = exp(-a_n * g^b_n)
      Uniform: a_n = a0 for all n; varied g and b.

  Family B — Rational:
      f_n(g) = 1 / (1 + c_n * g^d_n)
      Uniform: c_n = c0.

  Family C — Power-law:
      f_n(g) = (1 + e_n)^{-1} * g^{-p_n}   (requires g > 0)
      Uniform: p_n = p0.

Fine-tuning metric
------------------
Δ_FT (Barbieri-Giudice) per parameter q:
    Δ_FT(q) = |∂ ln ρ_vac^obs / ∂ ln q|

For the product formula:
    ln ρ_calc = ln ρ_QFT - 2 ln π + Σ_{n=1}^{99} ln f_n(g)
    Δ_FT(g) ≈ |g * d/dg [Σ ln f_n(g)]| / |ln(ρ_obs/ρ_QFT)|

Evidence tags:
    ρ_vac^obs = 2.45e-47 GeV⁴ → [C]
    f_n parametric families    → [D] (requires definition from CLAIMS_ADDENDUM)
    Δ_FT values                → [D]

L1 limitation: 10^10 factor between ρ_calc(g~1) and ρ_obs remains open.

Usage:
    python tools/vacuum_suppression.py
"""

import sys
import json
import csv
import hashlib
from pathlib import Path
from datetime import datetime, timezone

try:
    import mpmath as mp
except ImportError:
    sys.exit("[BLOCKED] mpmath required: pip install mpmath")


def _p(dps: int = 80):
    mp.dps = dps


# ── Physical constants ────────────────────────────────────────────────────────
RHO_OBS_GEV4   = mp.mpf('2.45e-47')     # [C]
RHO_QFT_GEV4   = mp.mpf('1e76')          # QFT cut-off ~ M_Pl^4
N_STEPS        = 99
PI             = mp.pi


# ── Target suppression ───────────────────────────────────────────────────────
def target_total_log_suppression():
    """ln(ρ_obs / (ρ_QFT / π²)) — this is the total log suppression to achieve."""
    _p()
    return mp.log(RHO_OBS_GEV4) - mp.log(RHO_QFT_GEV4) + mp.log(PI**2)


def required_per_step_log(N: int = N_STEPS):
    """Average ln(f_n) needed if all steps contribute equally."""
    _p()
    total = target_total_log_suppression()
    return total / mp.mpf(N)


# ── f_n families ──────────────────────────────────────────────────────────────
def family_A_log_sum(g, a0, b=mp.mpf('2'), N: int = N_STEPS):
    """Exponential: ln f_n = -a0 * g^b  → sum = -N * a0 * g^b"""
    _p()
    return -mp.mpf(N) * a0 * g**b


def family_B_log_sum(g, c0, d=mp.mpf('2'), N: int = N_STEPS):
    """Rational: ln f_n = -ln(1 + c0 * g^d)  → sum = -N * ln(1+c0*g^d)"""
    _p()
    return -mp.mpf(N) * mp.log(mp.mpf('1') + c0 * g**d)


def family_C_log_sum(g, p0, N: int = N_STEPS):
    """Power-law: ln f_n = -p0 * ln(g) - ln(2) → sum = -N*(p0*ln g + ln 2)"""
    _p()
    return -mp.mpf(N) * (p0 * mp.log(g) + mp.log(mp.mpf('2')))


def rho_calc(log_sum_fn):
    _p()
    return mp.exp(mp.log(RHO_QFT_GEV4) - mp.mpf('2') * mp.log(PI) + log_sum_fn)


# ── Fine-tuning metric ────────────────────────────────────────────────────────
def fine_tuning_delta(g, log_sum_fn_of_g, delta_g_frac=mp.mpf('1e-4')):
    """
    Numerical Barbieri-Giudice Δ_FT(g):
        Δ_FT = |g * d ln(ρ_calc) / dg| / |ln(ρ_obs/ρ_QFT)|
    """
    _p()
    g_p = g * (mp.mpf('1') + delta_g_frac)
    g_m = g * (mp.mpf('1') - delta_g_frac)
    dg  = mp.mpf('2') * g * delta_g_frac
    d_log = (log_sum_fn_of_g(g_p) - log_sum_fn_of_g(g_m)) / dg
    numerator   = abs(g * d_log)
    denominator = abs(mp.log(RHO_OBS_GEV4 / RHO_QFT_GEV4))
    return numerator / denominator


# ── Parameter scan ────────────────────────────────────────────────────────────
def scan_families(g_values, n_param: int = 30):
    _p()
    target = target_total_log_suppression()
    rows = []

    for g in g_values:
        # --- Family A: solve for a0 that hits target ---
        # -N * a0 * g^2 = target → a0 = -target/(N*g^2)
        b_A   = mp.mpf('2')
        a0_req = -target / (mp.mpf(N_STEPS) * g**b_A)
        ls_A   = family_A_log_sum(g, a0_req, b=b_A)
        rho_A  = rho_calc(ls_A)
        ratio_A = rho_A / RHO_OBS_GEV4
        ft_A   = fine_tuning_delta(g, lambda gx: family_A_log_sum(gx, a0_req, b_A))

        # --- Family B: solve for c0 ---
        # -N * ln(1 + c0 g²) = target → 1 + c0 g² = exp(-target/N)
        c0_req = (mp.exp(-target / mp.mpf(N_STEPS)) - mp.mpf('1')) / g**2
        ls_B   = family_B_log_sum(g, c0_req)
        rho_B  = rho_calc(ls_B)
        ratio_B = rho_B / RHO_OBS_GEV4
        ft_B   = fine_tuning_delta(g, lambda gx: family_B_log_sum(gx, c0_req))

        # --- Family C: solve for p0 ---
        # -N*(p0 ln g + ln 2) = target → p0 = (-target/N - ln2)/ln g
        if abs(mp.log(g)) < mp.mpf('1e-10'):
            p0_req = mp.mpf('0')
        else:
            p0_req = (-target / mp.mpf(N_STEPS) - mp.log(mp.mpf('2'))) / mp.log(g)
        ls_C   = family_C_log_sum(g, p0_req)
        rho_C  = rho_calc(ls_C)
        ratio_C = rho_C / RHO_OBS_GEV4
        ft_C   = fine_tuning_delta(g, lambda gx: family_C_log_sum(gx, p0_req))

        rows.append({
            'g': mp.nstr(g, 6),
            # Family A
            'a0_req_A': mp.nstr(a0_req, 8),
            'rho_ratio_A': mp.nstr(ratio_A, 6),
            'delta_FT_A': mp.nstr(ft_A, 6),
            # Family B
            'c0_req_B': mp.nstr(c0_req, 8),
            'rho_ratio_B': mp.nstr(ratio_B, 6),
            'delta_FT_B': mp.nstr(ft_B, 6),
            # Family C
            'p0_req_C': mp.nstr(p0_req, 8),
            'rho_ratio_C': mp.nstr(ratio_C, 6),
            'delta_FT_C': mp.nstr(ft_C, 6),
        })
    return rows


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    _p()
    timestamp = datetime.now(timezone.utc).isoformat()

    target = target_total_log_suppression()
    per_step = required_per_step_log()

    print("=" * 70)
    print("UIDT v3.9 Vacuum Suppression Analyser")
    print(f"Run: {timestamp}")
    print(f"ρ_obs      = {mp.nstr(RHO_OBS_GEV4, 6)} GeV⁴  [C]")
    print(f"ρ_QFT      = {mp.nstr(RHO_QFT_GEV4, 4)} GeV⁴")
    print(f"Target ln(suppression) = {mp.nstr(target, 10)}")
    print(f"Required per step (N={N_STEPS}): {mp.nstr(per_step, 10)}")
    print(f"Equivalent per-step f_n ≈ exp({mp.nstr(per_step, 6)}) = {mp.nstr(mp.exp(per_step), 6)}")
    print("=" * 70)

    # g values: 0.5, 1.0, 1.5, 2.0
    g_values = [mp.mpf('0.5'), mp.mpf('1.0'), mp.mpf('1.5'), mp.mpf('2.0')]
    rows = scan_families(g_values)

    print("\nFamily results (Δ_FT = Barbieri-Giudice fine-tuning):")
    print(f"{'g':>6}  {'Δ_FT(A)':>12}  {'Δ_FT(B)':>12}  {'Δ_FT(C)':>12}")
    for r in rows:
        print(f"{r['g']:>6}  {r['delta_FT_A']:>12}  {r['delta_FT_B']:>12}  {r['delta_FT_C']:>12}")

    print("\n[TENSION ALERT] Δ_FT >> 1 indicates significant fine-tuning required.")
    print("L1 open: 10^10 unexplained factor persists — f_n definitions from")
    print("CLAIMS_ADDENDUM_C054_C056.md must be extracted to resolve this.")

    # CSV
    out_dir = Path('verification/data/visualizations')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / 'vacuum_suppression_scan.csv'
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    csv_hash = sha256_file(out_csv)

    summary = {
        'tool': 'vacuum_suppression.py',
        'version': '2.0-parametric',
        'timestamp': timestamp,
        'rho_obs_GeV4': mp.nstr(RHO_OBS_GEV4, 6),
        'rho_QFT_GeV4': mp.nstr(RHO_QFT_GEV4, 4),
        'N_steps': N_STEPS,
        'target_log_suppression': mp.nstr(target, 10),
        'per_step_log': mp.nstr(per_step, 10),
        'g_scan': [mp.nstr(g, 6) for g in g_values],
        'families_tested': ['Exponential', 'Rational', 'PowerLaw'],
        'output_csv': str(out_csv),
        'csv_sha256': csv_hash,
        'evidence_tags': {
            'rho_obs': '[C]',
            'f_n_families': '[D]',
            'delta_FT': '[D]'
        },
        'open_issues': [
            'L1: 10^10 factor unexplained',
            'L5: N=99 steps unjustified (CONSTANTS.md S1-02)',
            'f_n explicit definitions missing from CANONICAL/; extract from CLAIMS_ADDENDUM_C054_C056.md'
        ]
    }
    out_json = out_dir / 'vacuum_suppression_summary.json'
    with open(out_json, 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"\nOutput CSV : {out_csv}  SHA256: {csv_hash}")
    print(f"Summary    : {out_json}")
    print("=" * 70)
    return summary


if __name__ == '__main__':
    main()
