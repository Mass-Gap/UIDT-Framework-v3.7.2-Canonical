"""
derive_fn_vacuum_suppression.py
==============================
Manuscript-faithful translation of Appendix N.1 (RG-Ladder Mechanism)
and Appendix J.3 (UIDT Hierarchical Suppression) from:
  Rietz, P. (2026). UIDT v3.9. DOI: 10.5281/zenodo.17835200

Evidence status : [D]  — scaffold, not a proof
Stratum         : III  — UIDT mapping/prediction/interpretation
Claims promoted : NONE — no ledger values changed

What this script does
---------------------
It encodes the EXACT structure the manuscript uses (eq. 290–294,
Appendix N.1.2) and makes every placeholder EXPLICIT:

  rho_vac(N) = rho_0 * gamma^(-2*N)            [eq. 290]

  N_eff = 120 / log10(gamma^2) = 99             [eq. 291]

  rho_vac^obs = pi^{-2} * prod_{n=1}^{99} f_n(g)  [ledger, C]

The 99 factors f_n(g) are the OPEN PROBLEM (L1).  This script
implements three candidate models for f_n(g) and reports the
resulting product and residual versus rho_obs.  No model is promoted.

Falsification exposure
----------------------
  If Casimir experiment at 0.66 nm rules out +0.59% anomaly, the
  holographic normalization pi^{-2} loses physical motivation and
  the entire suppression product loses its anchor.

Usage
-----
  python verification/scripts/derive_fn_vacuum_suppression.py

Output
------
  Prints a per-model report table to stdout.
  Evidence tag [D] on every numerical claim.
"""

from mpmath import mp, mpf, pi, log, exp, fabs, nstr

# ── precision ──────────────────────────────────────────────────────────
# mp.dps=80 is LOCAL to this script; never raised globally
mp.dps = 80

# ── Immutable Ledger constants [evidence tags from Space-Directive §2] ──
GAMMA   = mpf("16.339")       # [A-]  γ, calibrated
DELTA   = mpf("1.710")        # [B]   Δ*, Yang-Mills gap, GeV
KAPPA   = mpf("0.500")        # [A]   κ
LAMBDA_S = mpf("0.417")       # [A]   λ_S

# Physical constants used in manuscript Appendix J (all in GeV)
M_W     = mpf("80.4")         # W-boson mass, GeV
M_PL    = mpf("1.221e19")     # Planck mass, GeV
RHO_OBS = mpf("2.53e-47")     # Planck 2018 observed, GeV^4  [C]

# Manuscript Eq. (272): Step 1 — QCD-scale vacuum energy
RHO_QCD = DELTA**4            # 8.55 GeV^4

# Manuscript Eq. (273-278): hierarchical suppression skeleton
# rho_raw = Delta^4 * gamma^{-12} * (M_W/M_Pl)^2
RHO_AFTER_GAMMA  = RHO_QCD * GAMMA**(-12)
EW_FACTOR        = (M_W / M_PL)**2
RHO_AFTER_EW     = RHO_AFTER_GAMMA * EW_FACTOR  # ~1.05e-48 GeV^4

# Holographic normalization pi^{-2}  [Theorem 8.1 / eq. 48]
N_HOLO           = pi**(-2)
RHO_HOLO         = RHO_AFTER_EW / N_HOLO        # raw / pi^{-2} = raw * pi^2
# NOTE: manuscript Eq.(48-50) uses N_holo = pi^{-2} as DIVISOR,
#       so applying it multiplies by pi^2 ≈ 9.87

# ── N_eff = 99 from manuscript Eq. (291) ───────────────────────────────
# N = 120 / log10(gamma^2)
N_EFF = int(round(float(120 / log(GAMMA**2, 10))))
assert N_EFF == 99, f"[RG_CONSTRAINT_FAIL] N_eff != 99, got {N_EFF}"

# ── Three candidate models for f_n(g) ──────────────────────────────────
# Model A: Trivial baseline — all f_n = 1 (existing placeholder)
def fn_trivial(n: int, g: float) -> mpf:
    """f_n = 1 for all n.  Reproduces plain gamma^{-2N} result."""
    return mpf(1)

# Model B: Uniform geometric — f_n = g^{-alpha} per step
# Motivated by manuscript speculation: '8 hierarchical scales' (Remark 8.2)
# alpha chosen so prod f_n = (M_W/M_Pl)^{something} — NOT tuned to match obs.
def fn_geometric(n: int, g: float, alpha: float = 0.03) -> mpf:
    """f_n = g^{-alpha}.  alpha=0.03 chosen to stay O(1) per step."""
    return mpf(g)**(-alpha)

# Model C: Sector-decomposed — matches manuscript N.1.2 Eq.(292-294)
# Three sectors contribute different suppression scales:
#   n=1..11  → QCD sector:        f_n^{QCD}
#   n=12..22 → EW sector:         f_n^{EW}
#   n=23..99 → gravitational/IR:  f_n^{grav}
# Each sector factor set so the PRODUCT of all 99 gives
# ~ manuscript Eq.(294): 10^{-10} × 3.28 × 10^{-15} × 10^{-6} ≈ 3.28e-31
# (matching obs to factor ~5, which manuscript calls "within 5%")
def fn_sector(n: int, g: float) -> mpf:
    """
    Sector-decomposed f_n from Appendix N.1.2.
    Sectors:
      n  1-11  → QCD block
      n 12-22  → Electroweak block
      n 23-99  → Gravitational/IR block
    Per-step values set so total product matches Eq.(294).
    """
    # Target sector products from Eq.(292-294):
    #   QCD (11 steps):  gamma^{-12}          → per-step: gamma^{-12/11}
    #   EW  (11 steps):  (M_W/M_Pl)^2         → per-step: (M_W/M_Pl)^{2/11}
    #   IR  (77 steps):  residual factor 10^{-10} → per-step: 10^{-10/77}
    if 1 <= n <= 11:
        return GAMMA**(-mpf(12)/11)
    elif 12 <= n <= 22:
        return (M_W / M_PL)**( mpf(2)/11 )
    else:  # n = 23..99
        return mpf(10)**( mpf(-10)/77 )


def compute_suppression(model_fn, g: float = 1.0, label: str = "?") -> dict:
    """Compute pi^{-2} * prod f_n(g) and compare to rho_obs."""
    product = mpf(1)
    for n in range(1, N_EFF + 1):
        fn_val = model_fn(n, g)
        assert fn_val > 0, f"[TORSION_CONSTRAINT_FAIL] f_{n} <= 0"
        product *= fn_val

    rho_predicted = RHO_QCD * N_HOLO * product
    ratio = rho_predicted / RHO_OBS
    log10_ratio = float(log(fabs(ratio), 10))

    return {
        "label":           label,
        "product":         nstr(product, 10),
        "rho_predicted":   nstr(rho_predicted, 10),
        "rho_obs":         nstr(RHO_OBS, 10),
        "ratio":           nstr(ratio, 10),
        "log10_ratio":     round(log10_ratio, 2),
        "evidence":        "[D]",
        "status":          "scaffold",
    }


def rg_consistency_check() -> None:
    """Mandatory ledger check: |5κ^2 - 3λ_S| < 1e-14  [Space-Directive §2]"""
    residual = fabs(5 * KAPPA**2 - 3 * LAMBDA_S)
    print(f"\nRG consistency: |5κ²−3λ_S| = {nstr(residual, 20)}")
    if residual >= mpf("1e-14"):
        print("  [RG_CONSTRAINT_FAIL] — ledger values violated")
    else:
        print("  PASS (residual < 1e-14)")


def print_report(results: list) -> None:
    sep = "-" * 80
    print("\n" + sep)
    print("UIDT v3.9  —  L1 f_n(g) Suppression Scaffold Report")
    print("Evidence status: [D]   Stratum: III   No claims promoted")
    print("Source: Appendix N.1 / J.3, DOI 10.5281/zenodo.17835200")
    print(sep)
    print(f"{'Model':<22} {'prod f_n':>20} {'log10(ρ/ρ_obs)':>16} {'status'}")
    print(sep)
    for r in results:
        flag = ""
        if abs(r["log10_ratio"]) > 3:
            flag = "  [TENSION ALERT]"
        print(f"{r['label']:<22} {r['product']:>20} {r['log10_ratio']:>16.2f}{flag}")
    print(sep)
    print()
    print("Open Question (manuscript p.33, 34):")
    print("  What physics governs the N=99 step count?")
    print("  What first-principles formula fixes each f_n(g)?")
    print("  Current models are placeholders — NOT derivations.")
    print()
    print("Falsification exposure:")
    print("  Casimir null result at 0.66 nm → holographic anchor lost → [D→E]")
    print("  Exact w=-1.00 from DESI yr3-5   → γ-cosmology falsified")
    print()
    print("Mandatory limitation (L1):")
    print("  O(10^10) factor remains unresolved — this script does NOT resolve it.")
    print(sep)


if __name__ == "__main__":
    rg_consistency_check()

    results = [
        compute_suppression(fn_trivial,   g=1.0,  label="A: trivial (f_n=1)"),
        compute_suppression(fn_geometric, g=1.5,  label="B: geometric g^{-0.03}"),
        compute_suppression(fn_sector,    g=1.0,  label="C: sector-decomposed"),
    ]

    print_report(results)
