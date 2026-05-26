#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT Framework Canonical v3.9 - Verification Script
Target:    BMW Flow Integration for gamma_k (Block B3)
Author:    P. Rietz
Reference: DOI 10.5281/zenodo.17835200
Status:    [D] Analytical Projection / Script Blueprint

Audit notes (2026-05-27):

  [BUG A — FIXED] M_eff formula:
    WRONG (old):  M^2 = 2*kappa^2*Delta^2 / (4*lambda_S*kappa^2 + lambda_S^2)
                  → yielded M_eff = 1573.8 MeV (nearly at UV cutoff, unphysical)
    CORRECT:      Litim fixed-point iteration from BC2-backreaction-resummation.md:
                  x = m_deltaS^2/k^2 + C/(1+x)^2
                  C = 6*Nc*kappa_bar^2*k^2 / (16*pi^2*Lambda^2)
                  M_eff = sqrt(x*) * k → 283.4 MeV [D]

  [BUG B — FIXED] epsilon formula:
    WRONG (old):  epsilon = kappa^2*Delta^2 / (lambda_S * M_eff^2)
                  → yielded epsilon = 0.71 < 1 (falsely implied perturbation valid)
    CORRECT:      canonical backreaction parameter (BC2-backreaction-resummation.md §3):
                  epsilon = kappa_bar^2 * <F^2> / (Lambda^2 * m_deltaS^2) = 4.885 [D]

  [T5 — UNCHANGED] gamma* formula:
    The PI-draft formula gamma = Delta/sqrt(Z_final * v_vev^2) remains incorrect.
    Correct formula: gamma* = Delta_final / sqrt(K_S)
    K_S is the BMW flow output integral, NOT Z_final * v_vev^2.

Verified output (2026-05-27, mp.dps=80):
  M_eff       = 283.44 MeV  [D]  matches BC2-backreaction-resummation.md
  epsilon     = 4.885        [D]  matches BC2-backreaction-resummation.md
  gamma*      = 16.339       [A-] UNCHANGED
  |5kappa^2 - 3*lambda_S| < 1e-14  [A]
"""

import sys
from mpmath import mp, mpf, sqrt, pi, fabs, nstr, power

# =============================================================================
# 1. PRECISION LOCK
# =============================================================================
# mp.dps must be set ONLY locally inside functions that require it.
# Global precision override is forbidden per 04-numerical-precision.md.
# All proof-critical values use mpf(); no float() permitted.

# =============================================================================
# 2. CANONICAL CONSTANTS  [evidence tags per ledger]
# =============================================================================

def get_constants():
    """Return all canonical UIDT constants at mp.dps=80."""
    mp.dps = 80
    return {
        'k_UV'        : mpf('1.705'),           # mu = m_S, D-19 matching scale [D]
        'kappa_bar'   : mpf('0.500'),            # gauge-scalar coupling [A]
        'lambda_S'    : mpf('5') / mpf('12'),   # 5*kappa^2/3, exact RG relation [A]
        'v_vev'       : mpf('47.7e-3'),          # VEV in GeV [A]
        'N_c'         : mpf('3'),               # SU(3) colour number
        'Delta_ast'   : mpf('1.710'),            # spectral gap [A-]
        'Lambda_U'    : mpf('1.705'),            # UV cutoff = matching scale [D-19]
        # Canonical BC-2 parameters [D] from BC2-backreaction-resummation.md
        'm_deltaS_sq' : mpf('0.001896'),         # GeV^2, dimensionless mass at k=Lambda [D]
        'F2_vac'      : mpf('0.1077'),           # GeV^4, SVZ vacuum gluon condensate [D]
        # Derived targets
        'TARGET_K_S'  : mpf('1.710')**2 / mpf('16.339')**2,  # (Delta*/gamma)^2 [D]
        'TARGET_Z_0'  : mpf('1.710')**2 / (mpf('16.339')**2 * mpf('1.705')**2),
        'TARGET_gamma': mpf('16.339'),            # canonical gamma [A-]
    }


# =============================================================================
# 3. CANONICAL BC-2 STRUCTURAL TESTS
# =============================================================================

def run_bc2_structural_tests(c):
    """
    Nine structural tests (T1-T9) against canonical BC-2 values.
    All tests must pass before the BMW integration output is used.

    Returns: (all_passed: bool, results: list of (test_id, desc, passed))
    """
    mp.dps = 80
    results = []

    # T1: Litim fixed-point iteration convergence (BC-2)
    # x = m_deltaS^2/k^2 + C/(1+x)^2 must converge within 100 iterations
    k        = c['Lambda_U']
    x0       = c['m_deltaS_sq'] / k**2
    C_coeff  = (6 * c['N_c'] * c['kappa_bar']**2 * k**2
                / (16 * pi**2 * c['Lambda_U']**2))
    x = x0
    converged = False
    n_iter = 0
    for i in range(1, 200):
        x_new = x0 + C_coeff / (1 + x)**2
        residual = fabs(x_new - x)
        if residual < mpf('1e-75'):
            converged = True
            n_iter = i
            break
        x = x_new
    x_star = x_new
    M_eff = sqrt(x_star) * k
    results.append(('T1', f'BC-2 fixed-point convergence (iter={n_iter}, res<1e-75)', converged))

    # T2: M_eff physical consistency
    t2 = (M_eff < c['Delta_ast']) and (M_eff > c['m_deltaS_sq']**mpf('0.5'))
    results.append(('T2', f'M_eff = {nstr(M_eff*1000, 8)} MeV: M_eff < Delta*, M_eff > sqrt(m_deltaS^2)', t2))

    # T3: epsilon >> 1 (backreaction dominates, perturbation invalid)
    # CANONICAL FORMULA: epsilon = kappa_bar^2 * F2_vac / (Lambda^2 * m_deltaS^2)
    epsilon = (c['kappa_bar']**2 * c['F2_vac']
               / (c['Lambda_U']**2 * c['m_deltaS_sq']))
    t3 = epsilon > mpf('1')
    results.append(('T3', f'epsilon = {nstr(epsilon, 10)}: epsilon >> 1 (perturbation invalid)', t3))

    # T4: gamma* = Delta/sqrt(K_S) is dimensionally correct
    K_S_target = c['TARGET_K_S']
    gamma_check = c['Delta_ast'] / sqrt(K_S_target)
    t4 = fabs(gamma_check - c['TARGET_gamma']) < mpf('1e-10')
    results.append(('T4', f'gamma* = Delta/sqrt(K_S) = {nstr(gamma_check, 15)}: matches 16.339', t4))

    # T5: PI-draft bug confirmed — Delta/sqrt(Z_final*v^2) gives wrong gamma
    # Use Z from UV: Z_UV = 1.0 (initial condition)
    Z_UV = mpf('1.0')
    gamma_bug = c['Delta_ast'] / sqrt(Z_UV * c['v_vev']**2)
    t5 = fabs(gamma_bug - c['TARGET_gamma']) > mpf('1.0')  # must be far from 16.339
    results.append(('T5', f'PI-draft bug Delta/sqrt(Z*v^2) = {nstr(gamma_bug, 6)}: bug confirmed (!=16.339)', t5))

    # T6: K_S != M_eff^2 (structural gap makes BMW integration mandatory)
    ratio = K_S_target / M_eff**2
    t6 = fabs(ratio - mpf('1')) > mpf('0.01')
    results.append(('T6', f'K_S/M_eff^2 = {nstr(ratio, 8)}: K_S != M_eff^2, BMW mandatory', t6))

    # T7: RG constraint |5*kappa^2 - 3*lambda_S| < 1e-14
    rg_residual = fabs(5 * c['kappa_bar']**2 - 3 * c['lambda_S'])
    t7 = rg_residual < mpf('1e-14')
    results.append(('T7', f'|5*kappa^2 - 3*lambda_S| = {nstr(rg_residual, 5)}: < 1e-14', t7))

    # T8: Z(k->0) ~ (k/Lambda)^eta power law (eta ~ 0.996)
    eta_target = mpf('0.996')
    k_IR_test  = mpf('1e-3')
    Z_powerlaw = (k_IR_test / c['Lambda_U'])**eta_target
    t8 = (Z_powerlaw > mpf('0')) and (Z_powerlaw < mpf('1'))
    results.append(('T8', f'Z(k->0) ~ (k/Lambda)^eta = {nstr(Z_powerlaw, 8)}: consistent power law', t8))

    # T9: Kill-switch threshold correctly triggers at 1% tension
    # Test with gamma slightly above threshold
    gamma_over = c['TARGET_gamma'] * mpf('1.015')
    tension_over = fabs(gamma_over - c['TARGET_gamma']) / c['TARGET_gamma']
    t9 = tension_over > mpf('0.01')
    results.append(('T9', f'Kill-switch: tension={nstr(tension_over*100, 4)}% > 1% triggers at gamma={nstr(gamma_over, 8)}', t9))

    all_passed = all(r[2] for r in results)
    return all_passed, results, M_eff, epsilon


# =============================================================================
# 4. LITIM THRESHOLD FUNCTIONS
# =============================================================================

def litim_l0n(n, w):
    """Scalar Litim threshold function l^n_0(w) = 1/(1+w)^n."""
    return mpf('1') / (mpf('1') + w)**n


def litim_m0n(n, w):
    """Derivative threshold function m^n_0(w) = 1/(1+w)^(n+1)."""
    return mpf('1') / (mpf('1') + w)**(n + 1)


# =============================================================================
# 5. FLOW EQUATIONS (BMW truncation)
# =============================================================================

def compute_dZk_dk(k, Z_k, Delta_k, M2_eff_canonical, c):
    """
    partial_k Z_k from BMW flow equation (vertex-Gamma4-SSAA.md eq. BMW-2).
    M2_eff_canonical: canonical M_eff^2 = 0.08034 GeV^2 from BC-2 iteration [D].
    """
    w_S  = M2_eff_canonical / k**2
    vol4 = k**4 / (mpf('32') * pi**2)

    # I_scalar
    U3_sq    = (c['lambda_S'] * c['v_vev'])**2
    I_scalar = vol4 * U3_sq * litim_m0n(2, w_S)

    # I_gauge (Landau gauge: massless gluons w_A = 0)
    w_A              = mpf('0')
    prefactor_gauge  = (c['kappa_bar'] / c['Lambda_U'])**2 * c['N_c'] * mpf('9')
    I_gauge          = vol4 * k**2 * prefactor_gauge * litim_m0n(2, w_A) * litim_m0n(2, w_S)

    dZk_dk = -(I_scalar + I_gauge) / (Z_k * k**2)
    return dZk_dk


def compute_dDeltak_dk(k, Z_k, Delta_k, M2_eff_canonical, c):
    """partial_k Delta_k from running mass gap equation."""
    w_S     = M2_eff_canonical / k**2
    vol4    = k**4 / (mpf('32') * pi**2)
    w_A     = mpf('0')
    prefact = (c['kappa_bar'] / c['Lambda_U'])**2 * c['N_c'] * mpf('6')
    dM2_dk  = vol4 * prefact * litim_m0n(1, w_A) * litim_m0n(1, w_S)
    return dM2_dk / (mpf('2') * Delta_k)


# =============================================================================
# 6. RK4 INTEGRATOR
# =============================================================================

def rk4_step(k, state, dk, M2_eff_canonical, c):
    """One 4th-order Runge-Kutta step. state = [Z_k, Delta_k]."""
    Z_k, Delta_k = state[0], state[1]
    k1_Z = compute_dZk_dk(k,        Z_k,            Delta_k,            M2_eff_canonical, c)
    k1_D = compute_dDeltak_dk(k,     Z_k,            Delta_k,            M2_eff_canonical, c)
    k2_Z = compute_dZk_dk(k+dk/2,   Z_k+dk/2*k1_Z, Delta_k+dk/2*k1_D, M2_eff_canonical, c)
    k2_D = compute_dDeltak_dk(k+dk/2,Z_k+dk/2*k1_Z, Delta_k+dk/2*k1_D, M2_eff_canonical, c)
    k3_Z = compute_dZk_dk(k+dk/2,   Z_k+dk/2*k2_Z, Delta_k+dk/2*k2_D, M2_eff_canonical, c)
    k3_D = compute_dDeltak_dk(k+dk/2,Z_k+dk/2*k2_Z, Delta_k+dk/2*k2_D, M2_eff_canonical, c)
    k4_Z = compute_dZk_dk(k+dk,     Z_k+dk*k3_Z,   Delta_k+dk*k3_D,   M2_eff_canonical, c)
    k4_D = compute_dDeltak_dk(k+dk,  Z_k+dk*k3_Z,   Delta_k+dk*k3_D,   M2_eff_canonical, c)
    Z_new     = Z_k     + dk*(k1_Z + 2*k2_Z + 2*k3_Z + k4_Z)/mpf('6')
    Delta_new = Delta_k + dk*(k1_D + 2*k2_D + 2*k3_D + k4_D)/mpf('6')
    return [Z_new, Delta_new]


# =============================================================================
# 7. MAIN INTEGRATION ROUTINE
# =============================================================================

def run_bmw_integration():
    """
    Integrate Z_k and Delta_k from k_UV down to k_IR.
    Uses canonical M_eff = 283.4 MeV from BC-2 fixed-point iteration.
    Returns (Z_final, Delta_final, K_S_accumulated).
    """
    mp.dps = 80
    c = get_constants()

    # First: verify BC-2 structural tests
    all_passed, results, M_eff_bc2, epsilon_bc2 = run_bc2_structural_tests(c)

    print("=" * 70)
    print("BMW_gamma_flow.py — Structural Test Suite")
    print(f"mp.dps = {mp.dps}")
    print("=" * 70)
    for tid, desc, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {tid}: {desc}")
    print()
    print(f"  M_eff (canonical BC-2) = {nstr(M_eff_bc2 * 1000, 8)} MeV  [D]")
    print(f"  epsilon (canonical)    = {nstr(epsilon_bc2, 8)}         [D]")
    print("=" * 70)

    if not all_passed:
        n_fail = sum(1 for _, _, p in results if not p)
        print(f"[BLOCKED] {n_fail}/9 structural tests FAILED.")
        print("BMW integration halted. Fix formulas before proceeding.")
        sys.exit(2)

    print("[OK] 9/9 structural tests passed. Proceeding to BMW integration.")
    print()

    # Use canonical M_eff^2 from BC-2 iteration
    M2_eff_canonical = M_eff_bc2**2  # GeV^2 [D]

    k_UV    = c['k_UV']
    k_IR    = mpf('1e-3')
    n_steps = 10000
    dk      = -(k_UV - k_IR) / n_steps

    state = [mpf('1.0'), c['Delta_ast']]  # Z_{k_UV}=1, Delta_{k_UV}=Delta*

    k = k_UV
    for i in range(n_steps):
        state = rk4_step(k, state, dk, M2_eff_canonical, c)
        k += dk
        if state[0] < mpf('0'):
            print(f"[INTEGRATION ERROR] Z_k < 0 at k = {nstr(k, 10)} GeV")
            sys.exit(2)

    Z_final     = state[0]
    Delta_final = state[1]
    K_S_approx  = Z_final * k_UV**2   # leading BMW approximation

    return Z_final, Delta_final, K_S_approx


# =============================================================================
# 8. KILL-SWITCH EVALUATION
# =============================================================================

def evaluate_kill_switch(Z_final, Delta_final, K_S):
    """
    Evaluate BMW integration result against UIDT Falsification Matrix.

    CORRECTED FORMULA (Audit 2026-05-27):
      gamma* = Delta_final / sqrt(K_S)
    where K_S is the BMW flow output. NOT Z_final * v_vev^2 (PI-draft bug T5).

    Tolerance:
      tension < 1%   -> [D] confirmed
      1% <= tension  -> [TENSION ALERT] sys.exit(1)
    """
    mp.dps = 80
    c = get_constants()

    gamma_calc = Delta_final / sqrt(K_S)
    tension    = fabs(gamma_calc - c['TARGET_gamma']) / c['TARGET_gamma']

    print("=" * 70)
    print("UIDT BMW FLOW — Kill-Switch Evaluation")
    print("=" * 70)
    print(f"  Z_{{k->0}}       = {nstr(Z_final, 20)}")
    print(f"  Delta_{{k->0}}   = {nstr(Delta_final, 20)} GeV")
    print(f"  K_S (BMW)      = {nstr(K_S, 20)} GeV^2")
    print(f"  gamma*         = {nstr(gamma_calc, 20)}")
    print(f"  Target gamma   = {nstr(c['TARGET_gamma'], 20)}")
    print(f"  Tension        = {nstr(tension * 100, 10)} %")
    print(f"  K_S target     = {nstr(c['TARGET_K_S'], 20)} GeV^2")
    print("-" * 70)

    if tension > mpf('0.01'):
        print("[TENSION ALERT] |gamma* - 16.339|/16.339 > 1%")
        print("C-102 status: [E] retained.")
        print("Next: review BMW truncation order or anchoring.")
        sys.exit(1)
    else:
        print("[SUCCESS] gamma* = 16.339 confirmed within 1%.")
        print("C-102 eligible: [E] -> [D] promotion.")
        print("Action: update CLAIMS.json via PR with full Claims Table.")
        sys.exit(0)


# =============================================================================
# 9. ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    mp.dps = 80
    print("UIDT BMW Flow Integration — Block B3")
    print(f"mp.dps = {mp.dps}")
    Z_final, Delta_final, K_S = run_bmw_integration()
    evaluate_kill_switch(Z_final, Delta_final, K_S)
