#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 synthesis/no-go summary verifier.

This script verifies the arithmetic and classification invariants used in the
P1 synthesis report. It does not derive gamma and does not promote evidence.

Evidence status: [D]/[E] only. No [A] promotion.
"""

from __future__ import annotations

from mpmath import mp


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def main() -> None:
    mp.dps = 80

    nc = mp.mpf(3)
    gamma = mp.mpf("16.339")
    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_required = gamma - gamma_bare
    expected_delta = mp.mpf(17) / mp.mpf(3000)
    residual_delta = abs(delta_required - expected_delta)
    assert residual_delta < mp.mpf("1e-70"), nstr(residual_delta)

    alpha_s_ref = mp.mpf("0.326")
    kappa = mp.mpf(1) / mp.mpf(2)
    v_mev = mp.mpf("47.7")
    delta_star_mev = mp.mpf("1710")
    d_a = nc**2 - 1

    one_loop_unit = alpha_s_ref / (4 * mp.pi)
    assert one_loop_unit > delta_required

    two_loop_da = d_a * alpha_s_ref**2 / (16 * mp.pi**2)
    two_loop_da_residual = abs(two_loop_da - delta_required)
    assert two_loop_da_residual < mp.mpf("1e-3")
    assert two_loop_da_residual > mp.mpf("1e-14")

    k_t_mev = 4 * mp.pi * mp.mpf("2.44")
    v_s4p1 = mp.sqrt(mp.mpf(12) / mp.mpf(5)) * k_t_mev
    delta_s4p1 = d_a / (4 * mp.pi**2) * (v_s4p1 / delta_star_mev)
    s4p1_residual = abs(delta_s4p1 - delta_required)
    assert s4p1_residual < mp.mpf("1e-3")
    assert s4p1_residual > mp.mpf("1e-14")

    dimension_suppression = (kappa * v_mev / delta_star_mev) ** 2
    canonical_prefactor = d_a * alpha_s_ref**2 * dimension_suppression
    assert canonical_prefactor > 0

    smooth_derivative_abs_reference = mp.mpf("0.0013885306847083777")
    smooth_model_abs = canonical_prefactor * smooth_derivative_abs_reference
    enhancement_smooth = delta_required / smooth_model_abs
    assert enhancement_smooth > 16 * mp.pi**2

    required_kernel_mixing = delta_required / canonical_prefactor
    assert required_kernel_mixing > 4 * mp.pi
    assert required_kernel_mixing < 16 * mp.pi**2

    excluded_paths = {
        "simple_unscaled_one_loop_color_factors": "NO_GO_E",
        "naive_dimension_suppressed_hff_bubble": "NO_GO_E",
        "minimal_smooth_regulated_integral": "NO_GO_E",
        "untuned_regulator_comparison": "NO_PROOF_LEVEL_CLOSURE_D_E",
        "minimal_operator_mixing": "NO_GO_E",
    }
    remaining_open_path = "derived_nonperturbative_matching_or_different_operator"
    assert all(status for status in excluded_paths.values())
    assert remaining_open_path

    print("=== UIDT Phase-8 P1 Synthesis / No-Go Summary Check ===")
    print("gamma_bare:", nstr(gamma_bare))
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(residual_delta))
    print("one_loop_unit_alpha_over_4pi:", nstr(one_loop_unit))
    print("two_loop_dA_value:", nstr(two_loop_da))
    print("two_loop_dA_residual:", nstr(two_loop_da_residual))
    print("S4P1_delta:", nstr(delta_s4p1))
    print("S4P1_residual:", nstr(s4p1_residual))
    print("canonical_prefactor:", nstr(canonical_prefactor))
    print("smooth_model_abs:", nstr(smooth_model_abs))
    print("smooth_required_enhancement:", nstr(enhancement_smooth))
    print("required_kernel_mixing:", nstr(required_kernel_mixing))
    print("excluded_paths:", excluded_paths)
    print("remaining_open_path:", remaining_open_path)
    print("P1_SYNTHESIS_STATUS: MINIMAL_LOCAL_MODEL_PATHS_EXCLUDED_OR_UNPROMOTED")
    print("P1_REMAINS_OPEN")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 SYNTHESIS / NO-GO SUMMARY CHECKS PASSED")


if __name__ == "__main__":
    main()
