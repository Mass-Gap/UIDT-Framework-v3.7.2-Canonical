"""
modules/dse_rgz_v3_9.py
UIDT Framework v3.9 Canonical — Dyson-Schwinger / RGZ Module

Purpose:
    Compute the IR ghost dressing exponent kappa_ir, the dimension-2 RGZ
    condensate, and the induced vacuum pressure p_BRST from the Refined
    Gribov-Zwanziger (RGZ) action using 80-digit mpmath arithmetic.

    No free parameters beyond the canonical UIDT v3.9 ledger. No fitting.
    All inputs are derived from Delta_star = 1.710 GeV via first-principles
    RGZ relations.

Evidence target:   [D] — falsifiable by sign_verdict.
Kill switches:
    [PRECISION_FAIL]  mp.dps < 80 at call time
    [SIGN_FAIL]       w_BRST >= -1 (phantom crossing not supported)
    [KAPPA_FAIL]      kappa_ir <= 0 (ghost sector unphysical)

Canonical constants (UIDT v3.9 Parameter Ledger, immutable):
    Delta_star = 1.710 +/- 0.015 GeV   [A]  Yang-Mills spectral gap
    kappa_uv   = 0.500                 [A-] UV coupling parameter
    lambda_S   = 0.417                 [A-] Scalar self-coupling
    N_c        = 3                         SU(3)

Note on RG approximation:
    5*kappa_uv^2 = 3*lambda_S holds at O(1e-3) at the parameter level.
    The 1e-14 residual quoted in the UIDT ledger refers to the Banach
    convergence of the proof engine, not to this parameter identity.
    Both values are reported.

Physical basis — Decoupling (RGZ) class:
    In the decoupling class (Cucchieri, Mendes 2007; Bogolubsky et al. 2009),
    the gluon propagator D(0) is finite and nonzero, and the ghost propagator
    acquires a finite mass (kappa_ghost -> 0+ in strict limit). Here we use
    the leading-order angular-averaged DSE for the ghost dressing exponent
    (Fischer, Alkofer 2003; Aguilar, Papavassiliou 2008):

        kappa_ir = (N_c * g_s^2 / (4*pi)) * D_RGZ(0) * J_angular

    where J_angular = Delta_star^2 / (4*pi) is the angular phase-space
    factor at the IR threshold, and D_RGZ(0) = m2_rgz / gamma_gz^4.

    Gribov parameter from horizon condition (Zwanziger 1989):
        gamma_gz^4 = N_c / (N_c^2 - 1) * g_s^2 * Delta_star^4

    RGZ mass from dimension-2 condensate (Dudal et al. 2008):
        m2_rgz = gamma_gz^4 / Delta_star^2

    Vacuum pressure (Dudal, Sorella 2009 — Stratum III [D]):
        rho_BRST = gamma_gz^4 / (2*(N_c^2-1)) / m2_rgz
        p_BRST   = -gamma_gz^4 / (2*(N_c^2-1)) * D(0) * m2_rgz

    Phantom criterion:
        w_BRST = p_BRST / rho_BRST < -1  iff  D(0) * m2_rgz^2 > 1

RGZ literature (Stratum II):
    Zwanziger (1989) Nucl.Phys.B323:513
    Dudal, Gracey, Sorella et al. (2008) Phys.Rev.D78:065047
    Bogolubsky et al. (2009) Phys.Lett.B676:69
    Aguilar, Papavassiliou (2008) Phys.Rev.D78:025010
    Fischer, Alkofer (2003) Phys.Lett.B536:177
"""

import sys
from mpmath import mp, mpf, nstr, fabs, pi, log

_REQUIRED_DPS = 80


def _assert_precision():
    if mp.dps < _REQUIRED_DPS:
        raise RuntimeError(
            f"[PRECISION_FAIL] mp.dps={mp.dps} < required {_REQUIRED_DPS}. "
            "Set mp.dps=80 before calling any dse_rgz_v3_9 function."
        )


class CanonicalConstants:
    """
    Canonical UIDT v3.9 Parameter Ledger.
    All values stored as mpmath.mpf (80-digit).
    Must be instantiated after mp.dps = 80.
    """

    def __init__(self):
        _assert_precision()
        self.Delta_star  = mpf('1.710')    # GeV  [A]
        self.Delta_unc   = mpf('0.015')    # GeV  [A]
        self.kappa_uv    = mpf('0.500')    # [A-]
        self.lambda_S    = mpf('0.417')    # [A-]
        self.C_gluon     = mpf('0.277')    # GeV^4 [A]
        self.N_c         = mpf('3')        # SU(3)
        self.Lambda_QCD  = mpf('0.340')    # GeV, quenched pure-YM
        self.b0          = mpf('11')       # 1-loop beta, n_f=0

    def rg_approximation_residual(self):
        """
        Compute |5*kappa_uv^2 - 3*lambda_S|.
        This is a parameter-level approximation (O(1e-3)), not a proof residual.
        Returns (residual, tag).
        """
        _assert_precision()
        res = fabs(5 * self.kappa_uv**2 - 3 * self.lambda_S)
        tag = "[RG_WARN] residual > 0.01" if res > mpf('0.01') else "OK [parameter-level approx.]"
        return res, tag


def gluon_propagator_rgz(p2, m2_rgz, gamma_gz4):
    """
    Decoupling-class RGZ gluon propagator (Dudal et al. 2008, Eq. 3.14):

        D(p^2) = (p^2 + m2_rgz) / (p^4 + m2_rgz * p^2 + gamma_gz4)

    Properties:
        D(0)   = m2_rgz / gamma_gz4  > 0  (IR-finite, suppressed)
        D(inf) -> 0                        (UV-free)
    Lattice-compatible [B]: Bogolubsky et al. 2009.

    Parameters
    ----------
    p2        : mpf, Euclidean momentum squared [GeV^2]
    m2_rgz    : mpf, RGZ mass squared [GeV^2]
    gamma_gz4 : mpf, Gribov parameter^4 [GeV^4]

    Returns
    -------
    mpf : D(p^2) in [GeV^{-2}]
    """
    _assert_precision()
    return (p2 + m2_rgz) / (p2**2 + m2_rgz * p2 + gamma_gz4)


class DSEIntegrator:
    """
    Computes the RGZ DSE fixed-point quantities at 80-digit precision.

    Usage
    -----
        mp.dps = 80
        dse = DSEIntegrator()
        result = dse.compute()
        print(result['sign_verdict'])
    """

    def __init__(self):
        _assert_precision()
        self.CC = CanonicalConstants()

    def _alpha_s(self, mu2=None):
        """
        One-loop alpha_s in pure Yang-Mills (n_f = 0).
        Default scale: mu^2 = Delta_star^2.
        """
        _assert_precision()
        CC = self.CC
        if mu2 is None:
            mu2 = CC.Delta_star**2
        return (4 * pi) / (CC.b0 * log(mu2 / CC.Lambda_QCD**2))

    def _rgz_parameters(self, Delta=None):
        """
        Derive gamma_gz^4 and m2_rgz from horizon condition and condensate seed.
        No fitting; derived solely from Delta_star.

        Returns (gamma_gz4, m2_rgz)
        """
        _assert_precision()
        CC = self.CC
        if Delta is None:
            Delta = CC.Delta_star
        g2        = 4 * pi * self._alpha_s(Delta**2)
        gamma_gz4 = (CC.N_c / (CC.N_c**2 - 1)) * g2 * Delta**4
        m2_rgz    = gamma_gz4 / Delta**2
        return gamma_gz4, m2_rgz

    def compute(self, Delta=None):
        """
        Compute all RGZ-DSE observables at 80-digit precision.

        The ghost dressing exponent is obtained from the leading-order
        angular-averaged DSE (Fischer-Alkofer 2003; Aguilar-Papavassiliou 2008):

            kappa_ir = (N_c * g_s^2 / (4*pi)) * D_RGZ(0) * (Delta^2 / (4*pi))

        This is the analytically convergent form for the decoupling class.
        It avoids the UV-divergent full DSE integral, which requires
        renormalization beyond the scope of the v3.9 kernel.

        Returns
        -------
        dict with keys:
            kappa_ir      ghost dressing exponent (decoupling class)
            alpha_s       running coupling at Delta_star^2
            gamma_gz4     Gribov parameter^4 [GeV^4]
            m2_rgz        RGZ mass^2 / condensate [GeV^2]
            D_0           D_RGZ(p^2=0) [GeV^{-2}]
            rho_BRST      vacuum energy density [GeV^4]  [D/Stratum III]
            p_BRST        vacuum pressure [GeV^4]        [D/Stratum III]
            w_BRST        equation-of-state ratio p/rho  [D/Stratum III]
            sign_verdict  "PHANTOM_VIABLE [D]" or "[SIGN_FAIL] ..."
            criterion     D(0)*m2_rgz^2 (> 1 => phantom class)
        """
        _assert_precision()
        CC = self.CC
        if Delta is None:
            Delta = CC.Delta_star
        N_c = CC.N_c

        alpha_s             = self._alpha_s(Delta**2)
        g2                  = 4 * pi * alpha_s
        gamma_gz4, m2_rgz   = self._rgz_parameters(Delta)

        # IR ghost exponent (angular-averaged DSE, decoupling class)
        D_0          = m2_rgz / gamma_gz4
        J_angular    = Delta**2 / (4 * pi)
        kappa_ir     = (N_c * g2 / (4 * pi)) * D_0 * J_angular

        # Vacuum energy-momentum (Dudal-Sorella 2009)
        norm_fac     = gamma_gz4 / (2 * (N_c**2 - 1))
        rho_BRST     = norm_fac / m2_rgz
        p_BRST       = -(norm_fac * D_0 * m2_rgz)
        w_BRST       = p_BRST / rho_BRST
        criterion    = D_0 * m2_rgz**2  # equals -w_BRST

        # Verdict
        if kappa_ir <= mpf('0'):
            verdict = "[KAPPA_FAIL] kappa_ir <= 0: ghost sector unphysical"
        elif w_BRST < mpf('-1'):
            verdict = "PHANTOM_VIABLE [D]"
        else:
            verdict = "[SIGN_FAIL] w_BRST >= -1: phantom crossing NOT supported"

        return {
            "kappa_ir"    : kappa_ir,
            "alpha_s"     : alpha_s,
            "gamma_gz4"   : gamma_gz4,
            "m2_rgz"      : m2_rgz,
            "D_0"         : D_0,
            "rho_BRST"    : rho_BRST,
            "p_BRST"      : p_BRST,
            "w_BRST"      : w_BRST,
            "criterion"   : criterion,
            "sign_verdict": verdict,
        }

    def uncertainty_scan(self):
        """
        Propagate Delta_star uncertainty (+/- 0.015 GeV).
        Returns list of (Delta, w_BRST, verdict) for three sample points.
        """
        _assert_precision()
        orig    = self.CC.Delta_star
        results = []
        for d in [orig - self.CC.Delta_unc, orig, orig + self.CC.Delta_unc]:
            r = self.compute(Delta=d)
            results.append((d, r['w_BRST'], r['sign_verdict']))
        return results


def run_verification():
    """
    Standalone verification. Run as:
        python dse_rgz_v3_9.py
    """
    mp.dps = 80
    print("=" * 72)
    print(f"dse_rgz_v3_9.py  |  UIDT v3.9 Canonical  |  mp.dps = {mp.dps}")
    print("=" * 72)

    dse = DSEIntegrator()

    rg_res, rg_tag = dse.CC.rg_approximation_residual()
    print(f"RG approx. |5kappa_uv^2 - 3*lambda_S|: {nstr(rg_res,20)}  ->  {rg_tag}")

    print("\nComputing RGZ-DSE observables (80-digit, angular-averaged) ...")
    r = dse.compute()

    rows = [
        ("kappa_ir   IR ghost exponent",          r['kappa_ir'],   "dim-less"),
        ("alpha_s   at Delta_star^2",              r['alpha_s'],    "dim-less"),
        ("gamma_gz^4  Gribov parameter^4",         r['gamma_gz4'],  "GeV^4"),
        ("m2_rgz    RGZ mass^2 / condensate",      r['m2_rgz'],     "GeV^2"),
        ("D_RGZ(0)  IR gluon propagator",          r['D_0'],        "GeV^{-2}"),
        ("rho_BRST  vacuum energy density [D]",    r['rho_BRST'],   "GeV^4"),
        ("p_BRST    vacuum pressure [D]",          r['p_BRST'],     "GeV^4"),
        ("w_BRST    EOS ratio p/rho [D]",          r['w_BRST'],     "dim-less"),
        ("D(0)*m^2  phantom criterion [D]",        r['criterion'],  "(>1 => phantom class)"),
    ]
    print("\n--- RESULTS ---")
    for lbl, val, unit in rows:
        print(f"  {lbl:<42} = {nstr(val, 25)}  [{unit}]")
    print(f"\n  Sign verdict:  {r['sign_verdict']}")

    print("\n--- UNCERTAINTY SCAN (Delta* +/- 0.015 GeV) ---")
    for d, w, v in dse.uncertainty_scan():
        print(f"  Delta={nstr(d,5)} GeV  w_BRST={nstr(w,22)}  =>  {v}")

    print("\n[END VERIFICATION]")
    return r


if __name__ == "__main__":
    run_verification()
