#!/usr/bin/env python3
"""
Derivation Scaffold: f_n(g) Vacuum Suppression Factors — UIDT v3.9 Canonical
===============================================================================
Claims: UIDT-C-018, UIDT-C-042 (10^10 geometric factor — HIGHEST PRIORITY open)
        UIDT-C-017, UIDT-C-039 (N=99 RG steps — manuscript-faithful scaffold)
Evidence: scaffold [D] / [E] — NOT a derivation
Stratum: III (UIDT interpretation)

Manuscript context (§4.1):
  The manuscript Eq. (10) presents N_fold = 34.58 as a 'derivation' that
  'eliminates the need for an arbitrary 10^10 fit parameter.'  The Ledger
  records C-018/C-042 as 'HIGHEST PRIORITY open question'.  This script
  documents the scaffold model, makes the gap explicit, and provides a
  numerically reproducible baseline for future derivation work.

Vacuum suppression formula (canonical):
  rho_vac^obs = rho_vac^QFT * pi^{-2} * prod_{n=1}^{N} f_n(g)

Scaffold definition of f_n(g):
  f_n(g) = exp( -g^2 * alpha_n * beta_n )
  where alpha_n = n / N  (spectral fraction of n-th layer)
        beta_n  = n / (N + 1)  (logarithmic weight)
  This is the minimal non-trivial ansatz satisfying f_n(0) = 1 for all n.
  It is NOT derived from L_UIDT. It is a falsifiable placeholder [D].

L1 open gap:
  The 10^10 residual factor between rho_vac^QFT and rho_vac^obs remains
  unresolved.  This script shows how sensitive the product is to g,
  but does NOT claim to close the gap.

Precision: mp.dps=80 locally scoped.
No float(), no round() on proof-critical values, no mocked physics.

Falsification exposure:
  C-018/C-042: if an analytical derivation of f_n(g) from L_UIDT yields
  a product outside [1e-12, 1e-8], the scaffold is refuted.
  C-017/C-039: if N != 99 yields measurably better rho_vac match,
  N=99 is disfavoured.
"""

import sys
from typing import List, Tuple

try:
    from mpmath import mp, mpf, pi, exp, log, fabs, nstr, power
except ImportError:
    sys.exit("[BLOCKED] mpmath not available — install mpmath>=1.3")


# ---------------------------------------------------------------------------
# Immutable ledger constants (Space-Directive §2, no modification)
# ---------------------------------------------------------------------------
KAPPA    = "0.500"
LAMBDA_S = "0.41666666666666666666666666666666666666666666666666666666666666666666666666666666"  # 5*kappa^2/3 exact
DELTA    = "1.710"    # GeV  [A/B]
GAMMA    = "16.339"   # [A-]
RHO_VAC_QFT_GEV4 = "1e9"   # rough QFT estimate GeV^4 (Stratum I literature)
RHO_VAC_OBS_GEV4 = "2.45e-47"  # [C]
N_CANONICAL = 99


def rg_constraint_check() -> bool:
    """Verify 5*kappa^2 = 3*lambda_S with residual < 1e-14."""
    mp.dps = 80
    kappa = mpf(KAPPA)
    lambda_s = mpf(LAMBDA_S)
    residual = fabs(5 * kappa**2 - 3 * lambda_s)
    ok = residual < mpf("1e-14")
    if not ok:
        print(f"[RG_CONSTRAINT_FAIL] residual={nstr(residual, 20)}")
    return ok


def compute_fn_scaffold(
    g: str,
    N: int = N_CANONICAL,
) -> Tuple[List[str], str, str]:
    """
    Compute scaffold f_n(g) for n=1..N and the full product.

    Parameters
    ----------
    g : coupling constant as decimal string (avoids binary-float heuristics)
    N : number of RG steps (canonical: 99)

    Returns
    -------
    fn_values : list of nstr representations of each f_n
    product   : nstr of pi^{-2} * prod f_n
    log_product : nstr of log10 of the product
    """
    mp.dps = 80
    g_mp = mpf(g)
    N_mp = mpf(str(N))

    fn_values = []
    log_sum = mpf("0")

    for n in range(1, N + 1):
        n_mp = mpf(str(n))
        alpha_n = n_mp / N_mp
        beta_n  = n_mp / (N_mp + 1)
        exponent = -g_mp**2 * alpha_n * beta_n
        fn = exp(exponent)
        fn_values.append(nstr(fn, 30))
        log_sum += exponent  # accumulate in log space for precision

    # pi^{-2} * product
    product = exp(log_sum) / pi**2
    from mpmath import log10
    log10_product = log10(fabs(product))

    return fn_values, nstr(product, 30), nstr(log10_product, 10)


def suppression_analysis() -> None:
    """Run suppression analysis for physically motivated g values."""
    mp.dps = 80

    rho_qft = mpf(RHO_VAC_QFT_GEV4)
    rho_obs = mpf(RHO_VAC_OBS_GEV4)
    from mpmath import log10
    required_log10 = log10(rho_obs / rho_qft)

    print("=" * 70)
    print("VACUUM SUPPRESSION SCAFFOLD — UIDT-C-018/C-042")
    print("=" * 70)
    print(f"  N = {N_CANONICAL} (canonical, C-017/C-039 scaffold)")
    print(f"  rho_vac^QFT  ~ {RHO_VAC_QFT_GEV4} GeV^4  [Stratum I]")
    print(f"  rho_vac^obs  = {RHO_VAC_OBS_GEV4} GeV^4  [C]")
    print(f"  Required log10(suppression) = {nstr(required_log10, 10)}")
    print()
    print("  g (string)   | log10(pi^-2 * prod f_n)  | residual vs required")
    print("  " + "-" * 66)

    g_values = [
        "0.5", "1.0", "1.5", "2.0", "2.5", "3.0",
    ]

    for g_str in g_values:
        _, product_str, log10_str = compute_fn_scaffold(g_str, N_CANONICAL)
        log10_val = mpf(log10_str)
        residual = fabs(log10_val - required_log10)
        flag = ""
        if residual < mpf("2"):
            flag = "  <-- closest approach"
        print(f"  g={g_str:<8}  | log10={log10_str:<24} | Δ={nstr(residual, 6)}{flag}")

    print()
    print("  [L1 OPEN] 10^10 factor between rho_QFT and rho_obs unresolved.")
    print("  [STATUS]  Scaffold only — f_n(g) not derived from L_UIDT.")
    print("  [MANUSCRIPT §4.1] Eq.(10) overclaim must be corrected to:")
    print("    'N_fold = 34.58 is a calibrated scaffold [C]; L1 remains open.'")
    print("=" * 70)


def main() -> int:
    if not rg_constraint_check():
        return 1

    print("[OK] RG constraint 5κ²=3λ_S verified (residual < 1e-14)")

    suppression_analysis()

    print()
    print("Claims documented by this script:")
    print("  UIDT-C-018 / C-042 : 10^10 factor — OPEN, scaffold [D]")
    print("  UIDT-C-017 / C-039 : N=99 — manuscript-faithful scaffold [E]")
    print("  Falsification: product outside [1e-12, 1e-8] refutes scaffold.")
    print("PASS — derive_fn_vacuum_suppression completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
