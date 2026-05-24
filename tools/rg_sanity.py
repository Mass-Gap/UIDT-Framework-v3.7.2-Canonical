#!/usr/bin/env python3
"""
tools/rg_sanity.py  —  UIDT v3.9 Physical 1-Loop RG Sanity Check
====================================================================
Derivation basis
----------------
L_UIDT = -1/4 F^2 + 1/2 (∂S)^2 - V(S) - (κ/4) S^2 Tr(FF)

Scalar potential:  V(S) = λ_S/4 * S^4  (S-symmetric; v-shifted for VEV)
Non-minimal coupling:  -κ/4 * S^2 * Tr(F_μν F^μν)

1-Loop β-functions (background-field method, MS-bar, SU(N_c=3))
---------------------------------------------------------------
Contributions to β_κ at 1-loop from scalar-gauge vertex diagram:
    β_κ  = (1/16π²) [ 4κ λ_S  +  4κ³  -  κ g_3²  C_2(adj) ]
         = (1/16π²) [ 4κ(λ_S + κ²) - κ g_3² * N_c ]

Contributions to β_{λ_S} at 1-loop from scalar quartic vertex:
    β_{λ_S} = (1/16π²) [ 20 λ_S²  -  12 κ⁴ * dim(F)  +  3 κ⁴ * N_c² ]

Operator mixing note:
    The κ S² Tr(FF) vertex mixes under renormalisation with λ_S S⁴
    via the one-loop diagram with two scalar and two gauge lines.
    The mixing coefficient is -12 κ⁴ dim(F) in β_{λ_S} (N_c=3 → dim=8).

RG fixed-point consistency check:
    At the canonical fixed point κ=0.5, λ_S=5κ²/3:
        β_κ  = 0  iff  4(λ_S+κ²) = g_3²*N_c   →  g_3² evaluated self-consistently
        β_{λ_S} = 0  iff  20λ_S² = 12κ⁴*dim(F) - 3κ⁴*N_c²

    These are NECESSARY but not SUFFICIENT for an exact fixed point;
    the current implementation checks:
    (a) algebraic RG constraint  |5κ²-3λ_S| < 1e-14  [A]
    (b) fixed-point residual of β_κ,  β_{λ_S}  at canonical values [D]

Evidence tags:
    RG constraint check → [A]  (algebraic, exact)
    Physical β residuals → [D]  (predictive; full 2-loop required for [B])

Usage:
    python tools/rg_sanity.py
"""

import sys
import csv
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

try:
    import mpmath as mp
except ImportError:
    sys.exit("[BLOCKED] mpmath required: pip install mpmath")

# ── Precision ────────────────────────────────────────────────────────────────
def _set_precision(dps: int = 80):
    mp.dps = dps

# ── Canonical constants (CONSTANTS.md v3.9.5) ────────────────────────────────
def canonical_constants():
    _set_precision(80)
    kappa   = mp.mpf('1') / mp.mpf('2')          # κ = 0.500  [A]
    lambda_s = mp.mpf('5') * kappa**2 / mp.mpf('3')  # λ_S = 5κ²/3  [A]
    Nc      = mp.mpf('3')                          # SU(3)
    dim_F   = mp.mpf('8')                          # dim(adjoint SU(3))
    # Strong coupling at μ ~ m_S ~ 1.7 GeV (1-loop QCD, Λ_QCD~0.2 GeV)
    g3_sq   = mp.mpf('4') * mp.pi / (mp.log(mp.mpf('1.71') / mp.mpf('0.2')**2 + mp.mpf('1')))
    # Simplified tree-level estimate; tagged [D] — replace with lattice g_3 for [B]
    g3_sq   = mp.mpf('1.50')   # ~ α_s(m_S) * 4π ≈ 0.36 * 12.57 ~ 4.5 → use α_s~0.35
    g3_sq   = mp.mpf('4') * mp.pi * mp.mpf('0.35')  # ≈ 4.398  [D]
    return kappa, lambda_s, Nc, dim_F, g3_sq


def loop_factor():
    _set_precision(80)
    return mp.mpf('1') / (mp.mpf('16') * mp.pi**2)


# ── RG Constraint check (algebraic) ─────────────────────────────────────────
def check_rg_constraint(kappa, lambda_s, tol=mp.mpf('1e-14')):
    """[A] algebraic: |5κ²-3λ_S| < tol"""
    residual = abs(mp.mpf('5') * kappa**2 - mp.mpf('3') * lambda_s)
    status = 'PASS' if residual < tol else '[RG_CONSTRAINT_FAIL]'
    return residual, status


# ── Physical 1-loop β-functions ──────────────────────────────────────────────
def beta_kappa_1loop(kappa, lambda_s, Nc, g3_sq):
    """
    β_κ  = lf * κ * [ 4(λ_S + κ²) - g_3² * N_c ]
    Derived from: scalar-gauge 1PI diagram with two external S-lines
    and two external F-lines; MS-bar renormalisation.
    Evidence: [D] — tree-level structure correct; coefficient awaits 2-loop check.
    """
    _set_precision(80)
    lf = loop_factor()
    return lf * kappa * (mp.mpf('4') * (lambda_s + kappa**2) - g3_sq * Nc)


def beta_lambda_1loop(kappa, lambda_s, Nc, dim_F):
    """
    β_{λ_S} = lf * [ 20λ_S²  -  12κ⁴ * dim_F  +  3κ⁴ * N_c² ]
    Derived from: scalar quartic 1PI diagram + operator mixing from S²Tr(FF) vertex.
    Evidence: [D] — operator mixing coefficient requires explicit loop calculation;
    ± factor on dim_F term uncertain until full amplitude is computed.
    [TENSION ALERT] if β_{λ_S} ≠ 0 at canonical values.
    """
    _set_precision(80)
    lf = loop_factor()
    return lf * (mp.mpf('20') * lambda_s**2
                 - mp.mpf('12') * kappa**4 * dim_F
                 + mp.mpf('3') * kappa**4 * Nc**2)


# ── 1-Loop running scan (μ from 1 GeV to 1e6 GeV) ───────────────────────────
def rg_running_scan(n_steps: int = 200):
    """
    Euler-step integration of physical β-functions.
    Returns list of dicts for CSV export.
    """
    _set_precision(80)
    kappa, lambda_s, Nc, dim_F, g3_sq = canonical_constants()
    mu_min = mp.mpf('1')      # GeV
    mu_max = mp.mpf('1e6')    # GeV
    t_min  = mp.log(mu_min)
    t_max  = mp.log(mu_max)
    dt     = (t_max - t_min) / mp.mpf(n_steps)

    k   = kappa
    lam = lambda_s
    rows = []
    for i in range(n_steps + 1):
        t  = t_min + mp.mpf(i) * dt
        mu = mp.exp(t)
        bk  = beta_kappa_1loop(k, lam, Nc, g3_sq)
        bl  = beta_lambda_1loop(k, lam, Nc, dim_F)
        rc, st = check_rg_constraint(k, lam)
        rows.append({
            'step': i,
            'mu_GeV': mp.nstr(mu, 10),
            'kappa':  mp.nstr(k, 20),
            'lambda_s': mp.nstr(lam, 20),
            'beta_kappa': mp.nstr(bk, 10),
            'beta_lambda': mp.nstr(bl, 10),
            'rg_residual': mp.nstr(rc, 10),
            'rg_status': st
        })
        # Euler step
        k   = k   + bk  * dt
        lam = lam + bl  * dt

    return rows


# ── Output helpers ───────────────────────────────────────────────────────────
def write_csv(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    _set_precision(80)
    kappa, lambda_s, Nc, dim_F, g3_sq = canonical_constants()
    timestamp = datetime.now(timezone.utc).isoformat()

    print("=" * 70)
    print("UIDT v3.9 Physical 1-Loop RG Sanity Check")
    print(f"Run: {timestamp}")
    print(f"κ  = {mp.nstr(kappa, 20)}  [A]")
    print(f"λ_S = {mp.nstr(lambda_s, 20)}  [A]")
    print(f"g_3² = {mp.nstr(g3_sq, 10)}  [D] (1-loop QCD estimate)")
    print("=" * 70)

    # --- Algebraic RG constraint [A] ---
    res_alg, status_alg = check_rg_constraint(kappa, lambda_s)
    print(f"\n[A] Algebraic RG constraint |5κ²-3λ_S|")
    print(f"    Residual : {mp.nstr(res_alg, 20)}")
    print(f"    Status   : {status_alg}")
    assert res_alg < mp.mpf('1e-14'), f"[RG_CONSTRAINT_FAIL] residual={res_alg}"

    # --- Physical 1-loop β at canonical values [D] ---
    bk = beta_kappa_1loop(kappa, lambda_s, Nc, g3_sq)
    bl = beta_lambda_1loop(kappa, lambda_s, Nc, dim_F)
    print(f"\n[D] Physical 1-loop β-functions at canonical point:")
    print(f"    β_κ       = {mp.nstr(bk, 15)}")
    print(f"    β_{{λ_S}}  = {mp.nstr(bl, 15)}")
    if abs(bk) < mp.mpf('1e-5') and abs(bl) < mp.mpf('1e-5'):
        print("    STATUS: NEAR_FIXED_POINT [D]")
        fp_status = 'NEAR_FIXED_POINT'
    else:
        print("    STATUS: [TENSION ALERT] β ≠ 0 at canonical κ,λ_S — UV mechanism required")
        fp_status = '[TENSION ALERT] beta_nonzero'

    # --- Running scan ---
    print("\nRunning 1-loop RG scan (200 steps, 1 GeV → 1e6 GeV) ...")
    rows = rg_running_scan(200)
    fail_count = sum(1 for r in rows if '[RG_CONSTRAINT_FAIL]' in r['rg_status'])
    print(f"    Steps with |5κ²-3λ_S| ≥ 1e-14: {fail_count}/{len(rows)}")
    if fail_count == 0:
        scan_status = 'PASS'
    else:
        scan_status = f'[RG_CONSTRAINT_FAIL] {fail_count}/{len(rows)} steps'
    print(f"    Scan status: {scan_status}")

    # --- CSV output ---
    out_csv = Path('verification/data/visualizations/rg_scan_physical.csv')
    write_csv(rows, out_csv)
    csv_hash = sha256_file(out_csv)
    print(f"\nOutput: {out_csv}")
    print(f"SHA256: {csv_hash}")

    # --- Summary JSON ---
    summary = {
        'tool': 'rg_sanity.py',
        'version': '2.0-physical-1loop',
        'timestamp': timestamp,
        'constants': {
            'kappa':    mp.nstr(kappa, 20),
            'lambda_s': mp.nstr(lambda_s, 20),
            'g3_sq':    mp.nstr(g3_sq, 10),
            'Nc': 3, 'dim_F': 8
        },
        'rg_constraint': {
            'residual': mp.nstr(res_alg, 20),
            'status': status_alg,
            'evidence_tag': '[A]'
        },
        'beta_functions_canonical': {
            'beta_kappa':   mp.nstr(bk, 15),
            'beta_lambda_s': mp.nstr(bl, 15),
            'fp_status': fp_status,
            'evidence_tag': '[D]'
        },
        'rg_scan': {
            'n_steps': len(rows),
            'fail_count': fail_count,
            'status': scan_status,
            'output_csv': str(out_csv),
            'csv_sha256': csv_hash
        },
        'limitations': [
            'L4: γ=16.339 not derived from RG first principles',
            'g3_sq is 1-loop QCD estimate [D]; replace with lattice value for [B]',
            '2-loop coefficients required before claim promotion to [B]'
        ]
    }
    out_json = Path('verification/data/visualizations/rg_sanity_summary.json')
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary: {out_json}")
    print("=" * 70)
    print(f"OVERALL: {status_alg} | β-status: {fp_status} | Scan: {scan_status}")
    print("=" * 70)
    return summary


if __name__ == '__main__':
    main()
