#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 delta-gamma self-energy scale audit.

This script does not derive gamma. It tests whether simple perturbative
coefficient structures can reproduce the required correction
Delta_gamma_required = 17/3000 from gamma_bare = 49/3 to gamma = 16.339.

Evidence status: [D]/[E] only. No [A] promotion.
"""

from __future__ import annotations

from mpmath import mp


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def residual(value: mp.mpf, target: mp.mpf) -> mp.mpf:
    return abs(value - target)


def classify(value: mp.mpf, target: mp.mpf) -> str:
    r = residual(value, target)
    if r < mp.mpf("1e-14"):
        return "PROOF-LIKE_NUMERICAL_CLOSURE_BUT_DIAGRAM_REQUIRED"
    if r < mp.mpf("1e-3"):
        return "PARTIAL_SCALE_HIT_D"
    return "NO_GO_SCALE_MISMATCH_E"


def main() -> None:
    mp.dps = 80

    nc = mp.mpf(3)
    gamma_ledger = mp.mpf("16.339")
    alpha_s_ref = mp.mpf("0.326")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")

    ca = nc
    cf = (nc**2 - 1) / (2 * nc)
    da = nc**2 - 1

    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_required = gamma_ledger - gamma_bare
    delta_required_expected = mp.mpf(17) / mp.mpf(3000)
    delta_required_residual = residual(delta_required, delta_required_expected)
    assert delta_required_residual < mp.mpf("1e-70"), nstr(delta_required_residual)
    assert delta_required > 0

    unit_1loop = alpha_s_ref / (4 * mp.pi)
    unit_2loop = alpha_s_ref**2 / (16 * mp.pi**2)
    coefficient_required_1loop = delta_required / unit_1loop
    coefficient_required_2loop = delta_required / unit_2loop

    # Candidate family A: unscaled one-loop color factors.
    one_loop_candidates = {
        "1": mp.mpf(1),
        "C_F": cf,
        "C_A": ca,
        "C_A_minus_C_F": ca - cf,
        "d_A": da,
        "d_A_over_C_A": da / ca,
        "d_A_over_C_F": da / cf,
    }

    # Candidate family B: unscaled two-loop color factors.
    two_loop_candidates = {
        "1": mp.mpf(1),
        "C_F": cf,
        "C_A": ca,
        "C_A_minus_C_F": ca - cf,
        "d_A": da,
        "d_A_plus_half": da + mp.mpf(1) / mp.mpf(2),
        "d_A_plus_C_F": da + cf,
        "d_A_plus_C_A": da + ca,
    }

    # Candidate family C: threshold-log structures.
    k_t_mev = 4 * mp.pi * e_t_mev
    threshold_log = mp.log(delta_star_mev / k_t_mev)
    log_candidates = {
        "alpha_over_4pi_times_log": unit_1loop * threshold_log,
        "alpha_over_16pi2_times_log": alpha_s_ref / (16 * mp.pi**2) * threshold_log,
        "alpha2_over_16pi2_times_log": unit_2loop * threshold_log,
        "alpha_over_4pi_div_log": unit_1loop / threshold_log,
        "d_A_alpha2_over_16pi2_div_log": da * unit_2loop / threshold_log,
    }

    # Candidate family D: corrected S4-P1 non-perturbative shift already staged in PR #460.
    v_s4p1_mev = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_t_mev
    delta_gamma_s4p1 = (da) / (4 * mp.pi**2) * (v_s4p1_mev / delta_star_mev)

    print("=== UIDT Phase-8 P1 Delta-Gamma Self-Energy Scale Audit ===")
    print("gamma_bare:", nstr(gamma_bare))
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(delta_required_residual))
    print("alpha_s_ref:", nstr(alpha_s_ref))
    print("unit_1loop_alpha_over_4pi:", nstr(unit_1loop))
    print("unit_2loop_alpha2_over_16pi2:", nstr(unit_2loop))
    print("coefficient_required_1loop:", nstr(coefficient_required_1loop))
    print("coefficient_required_2loop:", nstr(coefficient_required_2loop))
    print("k_T_mev:", nstr(k_t_mev))
    print("threshold_log_Delta_over_kT:", nstr(threshold_log))

    print("\n[Attempt A] One-loop unscaled color factors")
    for name, coeff in one_loop_candidates.items():
        value = coeff * unit_1loop
        print(name, "coeff=", nstr(coeff), "value=", nstr(value), "residual=", nstr(residual(value, delta_required)), "status=", classify(value, delta_required))

    print("\n[Attempt B] Two-loop unscaled color factors")
    for name, coeff in two_loop_candidates.items():
        value = coeff * unit_2loop
        print(name, "coeff=", nstr(coeff), "value=", nstr(value), "residual=", nstr(residual(value, delta_required)), "status=", classify(value, delta_required))

    print("\n[Attempt C] Threshold-log structures")
    for name, value in log_candidates.items():
        print(name, "value=", nstr(value), "residual=", nstr(residual(value, delta_required)), "status=", classify(value, delta_required))

    print("\n[Attempt D] Corrected S4-P1 non-perturbative shift")
    print("Delta_gamma_S4P1:", nstr(delta_gamma_s4p1))
    print("S4P1_residual:", nstr(residual(delta_gamma_s4p1, delta_required)))
    print("S4P1_status:", classify(delta_gamma_s4p1, delta_required))

    # Fail-fast scientific invariants.
    assert coefficient_required_1loop > 0
    assert coefficient_required_2loop > 0
    assert delta_gamma_s4p1 > 0
    assert residual(delta_gamma_s4p1, delta_required) > mp.mpf("1e-14")
    assert residual(delta_gamma_s4p1, delta_required) < mp.mpf("1e-3")

    print("\nSUMMARY")
    print("P1_SELF_ENERGY_NOT_DERIVED")
    print("ONE_LOOP_SIMPLE_COLOR_FACTORS_NO_GO")
    print("TWO_LOOP_dA_SCALE_PARTIAL_HIT_D")
    print("S4P1_PARTIAL_HIT_D")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 DELTA-GAMMA SELF-ENERGY SCALE CHECKS PASSED")


if __name__ == "__main__":
    main()
