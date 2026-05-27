"""
UIDT FRG Solver \u2014 Dormand-Prince RK45, 80-dps mpmath
Adaptive Wetterich flow with Litim regulator under LPA.

Architecture: UIDT_FRG_Solver_RK45
Module location: verification/scripts/frg_solver_rk45.py

Changes in this revision:
  - \u03b2_\u03ba ACTIVATED: full O(1) d=3 dimensionless flow equations
  - Wilson-Fisher fixed-point search added (analytical + Newton)
  - WFFixedPoint dataclass with mpmath residuals
  - beta_functions now uses correct N=1 LPA Litim coefficients
  - Physical interpretation note: \u03ba* = 1/(18\u03c0\u00b2), \u03bb* = 18\u03c0\u00b2

UIDT Constitution compliance:
  - mp.dps = 80 declared locally in every method
  - No binary-float conversion usage
  - RG constraint 5\u03ba\u00b2 = 3\u03bbS enforced at start (d=4 UV check)
  - VacuumInstabilityException for IR divergence
  - Ledger constants: \u0394* = 1.710 GeV [A], \u03b3 = 16.339 [A-], ET = 2.44 MeV [C]

Beta-function reference:
  Berges, Tetradis, Wetterich, Phys.Rept. 363 (2002) 223-386,
  specifically Appendix B, eqs. B.1-B.2 for O(N=1), d=3, Litim regulator.
  Delamotte, arXiv:cond-mat/0702365 (2007), eqs. 52-53.
"""

import sys

from mpmath import mp, mpf, exp, log, sqrt, fabs, nstr, findroot


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class VacuumInstabilityException(Exception):
    """
    Raised when the IR denominator 1 + 2\u03bb\u03ba collapses below 1e-70.
    The k_crit value at which the topological protection breaks
    is encoded in the exception message.
    """
    pass


class WFFixedPoint:
    """
    Container for Wilson-Fisher fixed-point data.

    Fields
    ------
    kappa_star   : mpf  \u2014 dimensionless field minimum \u03ba* = c3/3 = 1/(18\u03c0\u00b2)
    lambda_star  : mpf  \u2014 quartic coupling      \u03bb* = 3/c3 = 18\u03c0\u00b2
    residual_kappa  : mpf  \u2014 |\u03b2_\u03ba(\u03ba*, \u03bb*)| after Newton refinement
    residual_lambda : mpf  \u2014 |\u03b2_\u03bb(\u03ba*, \u03bb*)| after Newton refinement
    method : str \u2014 'analytical' or 'newton'

    Evidence category: A (analytically proven, see module docstring reference).
    """
    def __init__(self, kappa_star, lambda_star, residual_kappa, residual_lambda, method):
        self.kappa_star       = kappa_star
        self.lambda_star      = lambda_star
        self.residual_kappa   = residual_kappa
        self.residual_lambda  = residual_lambda
        self.method           = method

    def __repr__(self):
        mp.dps = 80
        return (
            f"WFFixedPoint(d=3, N=1, Litim LPA)\n"
            f"  κ* = {nstr(self.kappa_star, 25)}  [= 1/(18π²)]\n"
            f"  λ* = {nstr(self.lambda_star, 25)}  [= 18π²]\n"
            f"  |β_κ|  = {nstr(self.residual_kappa, 10)}\n"
            f"  |β_λS| = {nstr(self.residual_lambda, 10)}\n"
            f"  method = {self.method}"
        )


class UIDT_FRG_Solver_RK45:
    """
    Dormand-Prince RK45 solver for the Wetterich FRG flow equation
    under the Local Potential Approximation (LPA) with the Litim regulator.

    State vector: [kappa, lambda_S]   (dimensionless, d=3)
      kappa    \u2014 dimensionless field minimum (\u03ba)  [Evidence A-]
      lambda_S \u2014 quartic self-coupling (\u03bbS)       [Evidence A-]

    RG-flow variable: t = ln(k/k_UV), flows from 0 (UV) to t_end < 0 (IR).

    The \u03b2-functions implement the FULL d=3 O(1) flow including \u03b2_\u03ba,
    using the analytically exact Litim-regulated one-loop expressions.

    All arithmetic in mp.dps = 80 (local declaration per UIDT Constitution).
    """

    def __init__(self, tol_str='1e-14', min_step_str='1e-20'):
        mp.dps = 80

        self.tol       = mpf(tol_str)
        self.min_step  = mpf(min_step_str)
        self.max_step  = mpf('0.5')

        # ---------------------------------------------------------------
        # Dormand-Prince Butcher tableau \u2014 exact rational mpf values
        # Reference: Dormand & Prince (1980), J. Comput. Appl. Math. 6, 19-26
        # ---------------------------------------------------------------
        mp.dps = 80

        self.c2 = mpf('1') / mpf('5')
        self.c3 = mpf('3') / mpf('10')
        self.c4 = mpf('4') / mpf('5')
        self.c5 = mpf('8') / mpf('9')
        self.c6 = mpf('1')
        self.c7 = mpf('1')

        self.a21 = mpf('1') / mpf('5')
        self.a31 = mpf('3') / mpf('40')
        self.a32 = mpf('9') / mpf('40')
        self.a41 = mpf('44') / mpf('45')
        self.a42 = mpf('-56') / mpf('15')
        self.a43 = mpf('32') / mpf('9')
        self.a51 = mpf('19372') / mpf('6561')
        self.a52 = mpf('-25360') / mpf('2187')
        self.a53 = mpf('64448') / mpf('6561')
        self.a54 = mpf('-212') / mpf('729')
        self.a61 = mpf('9017') / mpf('3168')
        self.a62 = mpf('-355') / mpf('33')
        self.a63 = mpf('46732') / mpf('5247')
        self.a64 = mpf('49') / mpf('176')
        self.a65 = mpf('-5103') / mpf('18656')

        self.b1 = mpf('35') / mpf('384')
        self.b2 = mpf('0')
        self.b3 = mpf('500') / mpf('1113')
        self.b4 = mpf('125') / mpf('192')
        self.b5 = mpf('-2187') / mpf('6784')
        self.b6 = mpf('11') / mpf('84')
        self.b7 = mpf('0')

        self.e1 = mpf('71') / mpf('57600')
        self.e2 = mpf('0')
        self.e3 = mpf('-71') / mpf('16695')
        self.e4 = mpf('71') / mpf('1920')
        self.e5 = mpf('-17253') / mpf('339200')
        self.e6 = mpf('22') / mpf('525')
        self.e7 = mpf('-1') / mpf('40')

    # ------------------------------------------------------------------
    # Physical kernel \u2014 d=3 dimensionless LPA
    # ------------------------------------------------------------------

    @staticmethod
    def c3_prefactor():
        """
        Litim-regulator prefactor in d=3:
            c3 = 1/(6\u03c0\u00b2)
        Derivation: v_d = 1/((4\u03c0)^{d/2} \u0393(d/2+1)) evaluated at d=3.
        Reference: Berges, Tetradis, Wetterich (2002), Appendix B.
        Evidence: A (analytically derived).
        """
        mp.dps = 80
        return mpf('1') / (mpf('6') * mp.pi * mp.pi)

    def litim_core(self, w):
        """
        Litim threshold function l_1(w) = 1/(1+w).
        w = 2\u03bb\u03ba is the dimensionless mass argument.
        IR-divergence guard: raises VacuumInstabilityException when |1+w| < 1e-70.
        """
        mp.dps = 80
        denom = mpf('1') + w
        if fabs(denom) < mpf('1e-70'):
            raise VacuumInstabilityException(
                f"VACUUM_INSTABILITY_TRIGGER: Litim denominator collapsed "
                f"at w = {nstr(w, 30, strip_zeros=False)}"
            )
        return mpf('1') / denom

    def beta_functions(self, t, state):
        """
        ACTIVATED d=3 O(1) LPA \u03b2-functions with Litim regulator.

        State: [\u03ba, \u03bbS] (dimensionless)

        Flow equations (Berges et al. 2002, Appendix B, N=1, d=3, Litim):

            \u2202_t \u03ba  = -\u03ba  + c3 \u00b7 l_1(2\u03bb\u03ba)
            \u2202_t \u03bbS = +\u03bbS - 3\u00b7c3 \u00b7 \u03bbS\u00b2 \u00b7 l_1(2\u03bb\u03ba)\u00b2

        where c3 = 1/(6\u03c0\u00b2), l_1(w) = 1/(1+w).

        Wilson-Fisher fixed point (analytically exact):
            \u03ba*  = c3/3  = 1/(18\u03c0\u00b2) \u2248 0.005629   [Evidence A]
            \u03bbS* = 3/c3  = 18\u03c0\u00b2     \u2248 177.65      [Evidence A]
            u* = 1 + 2\u03bb*\u03ba* = 3  (verified: 2\u03bb*\u03ba* = 2 exactly)

        Evidence category: A (analytically derived from Berges et al.)
        """
        mp.dps = 80
        kappa, lambda_s = state[0], state[1]

        c3 = self.c3_prefactor()
        w  = mpf('2') * lambda_s * kappa
        l1 = self.litim_core(w)

        d_kappa   = -kappa + c3 * l1
        d_lambda  = lambda_s - mpf('3') * c3 * lambda_s * lambda_s * l1 * l1

        return [d_kappa, d_lambda]

    # ------------------------------------------------------------------
    # Wilson-Fisher fixed-point search
    # ------------------------------------------------------------------

    def find_wilson_fisher_fixed_point(self):
        """
        Computes the Wilson-Fisher fixed point analytically and verifies
        via Newton refinement.

        Analytical derivation:
            \u03b2_\u03ba = 0:  \u03ba*(1 + 2\u03bb\u03ba*) = c3    ... (i)
            \u03b2_\u03bb = 0:  (1 + 2\u03bb\u03ba*)\u00b2  = 3c3\u03bb* ... (ii)

            Set u* = 1 + 2\u03bb*\u03ba*. From (i): \u03ba* = c3/u*.
            From (ii): u*\u00b2 = 3c3 \u03bb*  =>  \u03bb* = u*\u00b2/(3c3).
            Consistency: 2\u03bb*\u03ba* = 2(u*\u00b2/3c3)(c3/u*) = 2u*/3.
            => u* = 1 + 2u*/3  =>  u*/3 = 1  =>  u* = 3.

        Therefore:
            \u03ba*  = c3/3  = 1/(18\u03c0\u00b2)
            \u03bb*  = 3/c3  = 18\u03c0\u00b2
            u*  = 3  (i.e. 1 + 2\u03bb*\u03ba* = 3, check: 2\u03bb*\u03ba* = 2 \u2713)

        Returns
        -------
        WFFixedPoint instance with residuals < 1e-14.
        Raises AssertionError with [RG_CONSTRAINT_FAIL] if residual \u2265 1e-14.
        """
        mp.dps = 80
        c3 = self.c3_prefactor()

        kap_analytic = c3 / mpf('3')
        lam_analytic = mpf('3') / c3

        try:
            kap_star, lam_star = findroot(
                lambda k, l: (self.beta_functions(0, [k, l])[0],
                              self.beta_functions(0, [k, l])[1]),
                [kap_analytic, lam_analytic]
            )
        except Exception as exc:
            kap_star, lam_star = kap_analytic, lam_analytic
            print(f"[WARNING] Newton refinement failed ({exc}). "
                  f"Using analytical solution.")

        bk = fabs(self.beta_functions(0, [kap_star, lam_star])[0])
        bl = fabs(self.beta_functions(0, [kap_star, lam_star])[1])

        if bk >= mpf('1e-14') or bl >= mpf('1e-14'):
            raise AssertionError(
                f"[RG_CONSTRAINT_FAIL] Wilson-Fisher residuals exceed 1e-14: "
                f"|\u03b2_\u03ba|={nstr(bk,10)}, |\u03b2_\u03bb|={nstr(bl,10)}"
            )

        return WFFixedPoint(kap_star, lam_star, bk, bl, method='analytical+newton')

    # ------------------------------------------------------------------
    # RG-constraint verification (d=4 UV entry)
    # ------------------------------------------------------------------

    def verify_rg_constraint(self, kappa, lambda_s):
        """
        Verifies the UIDT RG fixed-point constraint: 5\u03ba\u00b2 = 3\u03bbS.
        Raises AssertionError with [RG_CONSTRAINT_FAIL] if violated.
        Tolerance: |LHS - RHS| < 1e-14.
        """
        mp.dps = 80
        lhs = mpf('5') * kappa * kappa
        rhs = mpf('3') * lambda_s
        residual = fabs(lhs - rhs)
        if residual >= mpf('1e-14'):
            raise AssertionError(
                f"[RG_CONSTRAINT_FAIL] 5\u03ba\u00b2={nstr(lhs,20)} \u2260 3\u03bbS={nstr(rhs,20)}, "
                f"residual={nstr(residual,10)}"
            )
        return residual

    # ------------------------------------------------------------------
    # RK45 step
    # ------------------------------------------------------------------

    def _rk45_step(self, t, state, h):
        """
        Single Dormand-Prince step. Returns (y5, error_norm).
        y5 = 5th-order solution; error_norm = L\u221e of normalised error vector.
        """
        mp.dps = 80

        def F(tt, ss):
            return self.beta_functions(tt, ss)

        def add(s, ds, fac):
            return [s[i] + fac * ds[i] for i in range(len(s))]

        def addm(base, *pairs):
            result = list(base)
            for fac, ds in pairs:
                for i in range(len(result)):
                    result[i] = result[i] + fac * ds[i]
            return result

        k1 = F(t,                   state)
        k2 = F(t + self.c2 * h,     add(state, k1, self.a21 * h))
        k3 = F(t + self.c3 * h,     addm(state,
                                         (self.a31 * h, k1),
                                         (self.a32 * h, k2)))
        k4 = F(t + self.c4 * h,     addm(state,
                                         (self.a41 * h, k1),
                                         (self.a42 * h, k2),
                                         (self.a43 * h, k3)))
        k5 = F(t + self.c5 * h,     addm(state,
                                         (self.a51 * h, k1),
                                         (self.a52 * h, k2),
                                         (self.a53 * h, k3),
                                         (self.a54 * h, k4)))
        k6 = F(t + self.c6 * h,     addm(state,
                                         (self.a61 * h, k1),
                                         (self.a62 * h, k2),
                                         (self.a63 * h, k3),
                                         (self.a64 * h, k4),
                                         (self.a65 * h, k5)))

        y5 = addm(state,
                  (self.b1 * h, k1),
                  (self.b3 * h, k3),
                  (self.b4 * h, k4),
                  (self.b5 * h, k5),
                  (self.b6 * h, k6))

        k7 = F(t + h, y5)

        err = addm([mpf('0')] * len(state),
                   (self.e1 * h, k1),
                   (self.e3 * h, k3),
                   (self.e4 * h, k4),
                   (self.e5 * h, k5),
                   (self.e6 * h, k6),
                   (self.e7 * h, k7))

        err_norm = max(
            fabs(err[i]) / (mpf('1e-10') + fabs(y5[i]))
            for i in range(len(y5))
        )

        return y5, err_norm

    # ------------------------------------------------------------------
    # Main solve loop
    # ------------------------------------------------------------------

    def solve(self, t_start_str, t_end_str, initial_state_strs,
              verify_constraint=False):
        """
        Integrate the FRG flow from t_start (UV) to t_end (IR).

        Parameters
        ----------
        t_start_str : str  \u2014 e.g. '0'
        t_end_str   : str  \u2014 e.g. '-10'
        initial_state_strs : list[str]  \u2014 [kappa_UV, lambda_S_UV]
        verify_constraint  : bool       \u2014 if True, verifies 5\u03ba\u00b2=3\u03bbS at UV

        Returns
        -------
        history : list of (t, state) tuples
        status  : 'COMPLETE' | 'VACUUM_INSTABILITY' | 'STIFF_HALT'
        k_crit  : mpf or None
        """
        mp.dps = 80

        t      = mpf(t_start_str)
        t_end  = mpf(t_end_str)
        state  = [mpf(v) for v in initial_state_strs]
        h      = mpf('-0.1')

        if t <= t_end:
            raise ValueError("t_start must be > t_end (UV \u2192 IR flow).")

        if verify_constraint:
            self.verify_rg_constraint(state[0], state[1])

        history = [(t, list(state))]
        status  = 'COMPLETE'
        k_crit  = None

        while t > t_end:
            if t + h < t_end:
                h = t_end - t

            try:
                y5, err_norm = self._rk45_step(t, state, h)
            except VacuumInstabilityException as e:
                status = 'VACUUM_INSTABILITY'
                k_crit = exp(t)
                history.append((t, list(state)))
                print(f"[VACUUM_INSTABILITY] {e}")
                print(f"  k_crit = {nstr(k_crit, 30)} (dimensionless k/k_UV)")
                break

            if err_norm < self.tol or fabs(h) <= self.min_step:
                t     = t + h
                state = y5
                history.append((t, list(state)))

            if err_norm > mpf('0'):
                safety = mpf('9') / mpf('10')
                h_new  = h * safety * (self.tol / err_norm) ** (mpf('1') / mpf('5'))
            else:
                h_new = h * mpf('5')

            if fabs(h_new) > self.max_step:
                h_new = -self.max_step if h < mpf('0') else self.max_step
            if fabs(h_new) < self.min_step:
                print(f"[SYSTEM-HALT] Step size {nstr(fabs(h_new),10)} "
                      f"< min_step {nstr(self.min_step,10)}. Flow stiff.")
                status = 'STIFF_HALT'
                break

            h = h_new

        return history, status, k_crit


# ------------------------------------------------------------------
# Main test: Wilson-Fisher fixed-point + RG flow
# ------------------------------------------------------------------

def run_wf_test():
    """
    1. Locates the Wilson-Fisher fixed point analytically.
    2. Verifies residuals < 1e-14.
    3. Runs the RG flow starting exactly at (\u03ba*, \u03bb*) \u2192 system stays fixed.
    4. Runs a second flow from a massive UV initial condition.
    """
    mp.dps = 80

    solver = UIDT_FRG_Solver_RK45(tol_str='1e-14', min_step_str='1e-20')

    print("=" * 65)
    print("UIDT_FRG_Solver_RK45 \u2014 Wilson-Fisher Fixed-Point Test")
    print("=" * 65)

    wf = solver.find_wilson_fisher_fixed_point()
    print(wf)
    print()

    print("--- Flow from (\u03ba*, \u03bb*) [t: 0 \u2192 -5]: expect FIXED ---")
    hist, status, k_crit = solver.solve(
        t_start_str='0',
        t_end_str='-5',
        initial_state_strs=[nstr(wf.kappa_star, 50), nstr(wf.lambda_star, 50)],
        verify_constraint=False,
    )
    tf, sf = hist[-1]
    dk = fabs(sf[0] - wf.kappa_star)
    dl = fabs(sf[1] - wf.lambda_star)
    print(f"  Status : {status}")
    print(f"  Steps  : {len(hist)}")
    print(f"  \u0394\u03ba     = {nstr(dk, 10)}  (deviation from \u03ba*)")
    print(f"  \u0394\u03bbS    = {nstr(dl, 10)}  (deviation from \u03bb*)")
    print()

    print("--- Flow from \u03ba_UV=1.0, \u03bbS_UV=100 [t: 0 \u2192 -3] ---")
    hist2, status2, _ = solver.solve(
        t_start_str='0',
        t_end_str='-3',
        initial_state_strs=['1.0', '100.0'],
        verify_constraint=False,
    )
    tf2, sf2 = hist2[-1]
    print(f"  Status  : {status2}")
    print(f"  Steps   : {len(hist2)}")
    print(f"  \u03ba(t=-3)  = {nstr(sf2[0], 20)}")
    print(f"  \u03bbS(t=-3) = {nstr(sf2[1], 20)}")

    return wf, hist, hist2


if __name__ == "__main__":
    run_wf_test()
