#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UIDT Framework Canonical v3.9 - Verification Script
Target:    BMW Flow Integration for gamma_k (Block B3)
Author:    P. Rietz
Reference: DOI 10.5281/zenodo.17835200
Status:    [D] Analytical Projection / Script Blueprint

Audit note (2026-05-27):
  The gamma* formula in the PI draft used:
      gamma_calc = Delta_final / sqrt(Z_final * v_vev**2)
  This is dimensionally incorrect. The correct formula is:
      gamma* = Delta_final / sqrt(K_S)
      K_S    = integral output of Z_k(v) flow, NOT Z_final * v_vev**2
  The corrected implementation is in evaluate_kill_switch() below.
  v_vev does NOT appear in the gamma* formula directly.
  See BC2-backreaction-resummation.md Section 4 for full derivation.
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
        'k_UV'       : mpf('1.705'),          # mu = m_S, D-19 matching scale [D]
        'kappa_bar'  : mpf('0.500'),          # gauge-scalar coupling [A]
        'lambda_S'   : mpf('5') / mpf('12'), # 5*kappa^2/3, exact RG relation [A]
        'v_vev'      : mpf('47.7e-3'),        # VEV in GeV [A]
        'N_c'        : mpf('3'),              # SU(3) colour number
        'Delta_ast'  : mpf('1.710'),          # spectral gap [A-]
        'Lambda_U'   : mpf('1.705'),          # UV cutoff = matching scale [D-19]
        # Derived targets from BC-2 resolution
        'TARGET_K_S' : mpf('1.710')**2 / mpf('16.339')**2,  # (Delta*/gamma)^2 [D]
        'TARGET_Z_0' : mpf('1.710')**2 / (mpf('16.339')**2 * mpf('1.705')**2),  # K_S/m_S^2 [D]
        'TARGET_gamma': mpf('16.339'),        # canonical gamma [A-]
    }


# =============================================================================
# 3. LITIM THRESHOLD FUNCTIONS
# =============================================================================
# These are the analytical results of the momentum integrals after applying
# the Litim optimised regulator R_k(q) = Z_k(k^2-q^2)*theta(k^2-q^2).
# See: Litim, Phys.Rev.D 64 (2001) 105007.
#
# Standard Litim threshold functions (d=4):
#   l^n_0(w) = 1/(1+w)^n  * (volume factor absorbed)
# where w = m^2_eff / k^2 is the dimensionless mass.

def litim_l0n(n, w):
    """
    Scalar Litim threshold function l^n_0(w) = 1/(1+w)^n.
    Enters the flow of U_k (potential sector).
    n: power (integer), w: dimensionless mass m^2/k^2 (mpf)
    """
    return mpf('1') / (mpf('1') + w)**n


def litim_m0n(n, w):
    """
    Derivative threshold function m^n_0(w) = 1/(1+w)^(n+1).
    Enters the flow of Z_k (wavefunction renormalization).
    n: power (integer), w: dimensionless mass (mpf)
    """
    return mpf('1') / (mpf('1') + w)**(n + 1)


# =============================================================================
# 4. FLOW EQUATIONS
# =============================================================================
# Full BMW-truncation flow equations for the UIDT system.
# See: vertex-Gamma4-SSAA.md Section 6 for derivation.
#
# State vector: [Z_k, Delta_k]
#   Z_k     : wavefunction renormalization of S at the VEV
#   Delta_k : running spectral gap (mass of the gap mode)
#
# RG time: t = ln(k/k_UV), so dk = k * dt
# Flow direction: k from k_UV down to 0  (t from 0 to -inf)

def compute_dZk_dk(k, Z_k, Delta_k, c):
    """
    Partial_k Z_k from BMW flow equation (vertex-Gamma4-SSAA.md eq. BMW-2).

    Two contributions:
      I_scalar: from Gamma^(4)_SSSS (pure scalar loop)
      I_gauge:  from Gamma^(4)_SSAA (critical scalar-gauge mixing)

    Litim regulator with massless transverse gluons (Landau gauge).
    """
    kappa_bar = c['kappa_bar']
    Lambda_U  = c['Lambda_U']
    N_c       = c['N_c']
    lambda_S  = c['lambda_S']
    v_vev     = c['v_vev']

    # Dimensionless running mass of scalar
    # M_eff from self-consistent gap equation (BC2-backreaction-resummation.md)
    m2_scalar = mpf('2') * lambda_S * v_vev**2  # free part [A]
    # Full resummed M^2_eff (fixed at BMW matching point; in full BMW this runs)
    # For the blueprint: use the resummed value M_eff = 283.4 MeV
    M2_eff = mpf('0.08034')  # GeV^2, from 80-digit verified BC-2 result [D]
    w_S = M2_eff / k**2  # dimensionless scalar mass

    # Volume factor for d=4: k^4/(32*pi^2) (Litim, standard normalization)
    vol4 = k**4 / (mpf('32') * pi**2)

    # I_scalar: (U'''_k(v))^2 contribution
    # U'''_k(v) = lambda_S * v  (from the scalar quartic at the VEV)
    U3_sq = (lambda_S * v_vev)**2
    I_scalar = vol4 * U3_sq * litim_m0n(2, w_S)

    # I_gauge: (kappa_bar/Lambda)^2 * N_c * 9 contribution
    # Tensor factor 9 from transverse Lorentz contraction (vertex-Gamma4-SSAA.md Section 4)
    # Massless gluon: w_A = 0 in Landau gauge
    w_A = mpf('0')
    prefactor_gauge = (kappa_bar / Lambda_U)**2 * N_c * mpf('9')
    # q^4 weight in the integral gives an extra k^2 factor (Litim)
    I_gauge = vol4 * k**2 * prefactor_gauge * litim_m0n(2, w_A) * litim_m0n(2, w_S)

    # Total flow: partial_k Z_k
    # Negative sign: Z_k decreases from UV to IR (anomalous dimension)
    dZk_dk = -(I_scalar + I_gauge) / (Z_k * k**2)

    return dZk_dk


def compute_dDeltak_dk(k, Z_k, Delta_k, c):
    """
    Partial_k Delta_k from the running mass gap equation.
    At leading order in the BMW system: Delta_k tracks U''_k(v) flow.
    """
    lambda_S = c['lambda_S']
    v_vev    = c['v_vev']
    N_c      = c['N_c']
    kappa_bar= c['kappa_bar']
    Lambda_U = c['Lambda_U']

    M2_eff = mpf('0.08034')  # GeV^2 [D]
    w_S    = M2_eff / k**2
    vol4   = k**4 / (mpf('32') * pi**2)

    # Running of the scalar mass: driven by gauge-scalar mixing
    # delta(Delta^2)_k ~ (kappa_bar/Lambda)^2 * N_c * threshold
    w_A = mpf('0')
    prefactor = (kappa_bar / Lambda_U)**2 * N_c * mpf('6')
    dM2_dk    = vol4 * prefactor * litim_m0n(1, w_A) * litim_m0n(1, w_S)

    # Delta_k ~ sqrt(M^2_eff(k) + Delta^2_gap)
    # At leading truncation: treat Delta_k as running with half the M^2 flow
    dDelta_dk = dM2_dk / (mpf('2') * Delta_k)

    return dDelta_dk


# =============================================================================
# 5. RK4 INTEGRATOR
# =============================================================================

def rk4_step(k, state, dk, c):
    """
    One 4th-order Runge-Kutta step.
    state = [Z_k, Delta_k]
    dk: negative step size (flowing toward IR)
    """
    Z_k, Delta_k = state[0], state[1]

    k1_Z = compute_dZk_dk(k,           Z_k,                         Delta_k,               c)
    k1_D = compute_dDeltak_dk(k,        Z_k,                         Delta_k,               c)

    k2_Z = compute_dZk_dk(k + dk/2,    Z_k + dk/2 * k1_Z,          Delta_k + dk/2 * k1_D, c)
    k2_D = compute_dDeltak_dk(k + dk/2, Z_k + dk/2 * k1_Z,          Delta_k + dk/2 * k1_D, c)

    k3_Z = compute_dZk_dk(k + dk/2,    Z_k + dk/2 * k2_Z,          Delta_k + dk/2 * k2_D, c)
    k3_D = compute_dDeltak_dk(k + dk/2, Z_k + dk/2 * k2_Z,          Delta_k + dk/2 * k2_D, c)

    k4_Z = compute_dZk_dk(k + dk,      Z_k + dk * k3_Z,            Delta_k + dk * k3_D,   c)
    k4_D = compute_dDeltak_dk(k + dk,   Z_k + dk * k3_Z,            Delta_k + dk * k3_D,   c)

    Z_new     = Z_k     + dk * (k1_Z + mpf('2')*k2_Z + mpf('2')*k3_Z + k4_Z) / mpf('6')
    Delta_new = Delta_k + dk * (k1_D + mpf('2')*k2_D + mpf('2')*k3_D + k4_D) / mpf('6')

    return [Z_new, Delta_new]


# =============================================================================
# 6. MAIN INTEGRATION ROUTINE
# =============================================================================

def run_bmw_integration():
    """
    Integrate Z_k and Delta_k from k_UV down to k_IR.
    Returns (Z_final, Delta_final, K_S_accumulated).
    """
    mp.dps = 80
    c = get_constants()

    k_UV   = c['k_UV']
    k_IR   = mpf('1e-3')   # IR cutoff (GeV); below this the flow is frozen
    n_steps = 10000        # number of RK4 steps
    dk     = -(k_UV - k_IR) / n_steps  # negative: flow toward IR

    # UV initial conditions (D-19)
    state = [mpf('1.0'), c['Delta_ast']]  # Z_{k_UV} = 1, Delta_{k_UV} = Delta*

    k = k_UV
    # Accumulate K_S via trapezoidal integration of the Z_k flow
    # K_S = integral_0^Lambda dk (-d/dk)[Z_k(v) * I_kin(k)]
    # Leading approximation: K_S ~ Z_{k->0}(v) * k_UV^2 (IR dominated)
    # Full BMW gives this as a flow output; here we track Z_k and extract at IR.

    for i in range(n_steps):
        state = rk4_step(k, state, dk, c)
        k += dk
        # Guard against unphysical Z_k < 0
        if state[0] < mpf('0'):
            print(f"[INTEGRATION ERROR] Z_k went negative at k = {nstr(k, 10)} GeV")
            sys.exit(2)

    Z_final     = state[0]
    Delta_final = state[1]

    # K_S at IR: leading BMW approximation
    # In the full BMW system K_S is extracted from the integrated Z_k flow.
    # Here: K_S_approx = Z_final * k_UV^2 (lower bound; full integral gives more)
    K_S_approx = Z_final * k_UV**2

    return Z_final, Delta_final, K_S_approx


# =============================================================================
# 7. KILL-SWITCH EVALUATION
# =============================================================================

def evaluate_kill_switch(Z_final, Delta_final, K_S):
    """
    Evaluate integration result against UIDT Falsification Matrix.

    CORRECTED FORMULA (see module docstring):
      gamma* = Delta_final / sqrt(K_S)
    where K_S is the BMW flow output, NOT Z_final * v_vev**2.

    Tolerance levels:
      < 1%   -> [D] confirmed, promote C-102 to [D]
      1-3%   -> [TENSION ALERT], keep [E]
      > 3sigma -> formal review required
    """
    mp.dps = 80
    c = get_constants()

    gamma_calc = Delta_final / sqrt(K_S)
    tension    = fabs(gamma_calc - c['TARGET_gamma']) / c['TARGET_gamma']

    print("=" * 60)
    print("UIDT BMW FLOW VERIFICATION REPORT")
    print("=" * 60)
    print(f"Z_{{k->0}}          = {nstr(Z_final, 20)}")
    print(f"Delta_{{k->0}}      = {nstr(Delta_final, 20)} GeV")
    print(f"K_S (BMW output)   = {nstr(K_S, 20)} GeV^2")
    print(f"gamma*             = {nstr(gamma_calc, 20)}")
    print(f"Target gamma       = {nstr(c['TARGET_gamma'], 20)}")
    print(f"Tension metric     = {nstr(tension, 20)}")
    print(f"Target Z_{{k->0}}   = {nstr(c['TARGET_Z_0'], 20)}")
    print(f"Target K_S         = {nstr(c['TARGET_K_S'], 20)} GeV^2")
    print("-" * 60)

    if tension > mpf('0.01'):
        print("[TENSION ALERT] |gamma* - 16.339|/16.339 > 1%")
        print("C-102 status: [E] retained.")
        print("Next step: review BMW truncation order or anchoring scheme.")
        sys.exit(1)
    else:
        print("[SUCCESS] BMW flow confirms gamma* = 16.339 within 1%.")
        print("C-102 eligible for promotion [E] -> [D].")
        print("Action required: update CLAIMS.json via PR with full Claims Table.")
        sys.exit(0)


# =============================================================================
# 8. ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    mp.dps = 80
    print("UIDT BMW Flow Integration — Block B3")
    print(f"Running at mp.dps = {mp.dps}")
    Z_final, Delta_final, K_S = run_bmw_integration()
    evaluate_kill_switch(Z_final, Delta_final, K_S)
