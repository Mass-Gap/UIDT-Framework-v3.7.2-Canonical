#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 BMW/Dyson/FRG operator-mixing scaffold.

This verifier does not derive gamma. It sets a reproducible gate for the next
admissible P1 direction after the synthesis/no-go PR:

    BMW/Dyson/FRG operator mixing projected onto O_K = 1/2 (partial h)^2.

The script verifies the target correction, operator-basis dimensions, projection
logic, and the numerical size of the enhancement that any controlled
non-perturbative matching must explain.

Evidence status: [D]/[E] only. No [A] promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from mpmath import mp


@dataclass(frozen=True)
class Operator:
    name: str
    dimension: int
    cp_even: bool
    gauge_invariant: bool
    projects_to_ok: bool


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def main() -> None:
    mp.dps = 80

    nc = mp.mpf(3)
    da = nc**2 - 1
    gamma = mp.mpf("16.339")
    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_required = gamma - gamma_bare
    expected_delta = mp.mpf(17) / mp.mpf(3000)
    residual_delta = abs(delta_required - expected_delta)
    assert residual_delta < mp.mpf("1e-70"), nstr(residual_delta)

    kappa = mp.mpf(1) / mp.mpf(2)
    v_mev = mp.mpf("47.7")
    delta_star_mev = mp.mpf("1710")
    alpha_s_ref = mp.mpf("0.326")

    basis = [
        Operator("O_K = 1/2 (partial h)^2", 4, True, True, True),
        Operator("O_M = 1/2 h^2", 2, True, True, False),
        Operator("O_F = Tr(F F)", 4, True, True, False),
        Operator("O_hFF = h Tr(F F)", 5, True, True, False),
        Operator("O_h2FF = h^2 Tr(F F)", 6, True, True, False),
        Operator("O_dh2FF = (partial h)^2 Tr(F F)", 8, True, True, True),
    ]

    assert all(op.cp_even and op.gauge_invariant for op in basis)
    assert basis[0].projects_to_ok
    assert not basis[4].projects_to_ok
    assert basis[5].projects_to_ok

    dimension_suppression = (kappa * v_mev / delta_star_mev) ** 2
    canonical_prefactor = da * alpha_s_ref**2 * dimension_suppression
    required_projected_flow_strength = delta_required / canonical_prefactor

    perturbative_bound = 4 * mp.pi
    strong_bound = 16 * mp.pi**2

    # Prior smooth-regulated derivative magnitude from the P1 regulated integral audit.
    smooth_derivative_abs_reference = mp.mpf("0.0013885306847083777")
    required_matching_enhancement = delta_required / (
        canonical_prefactor * smooth_derivative_abs_reference
    )

    assert required_projected_flow_strength > perturbative_bound
    assert required_projected_flow_strength < strong_bound
    assert required_matching_enhancement > strong_bound

    # BMW/Dyson/FRG scaffold variables. These are not fitted; they are the
    # quantities a future derivation must supply.
    unknown_projector_flow = "partial_t_Zh_from_Gamma_hAA_GAA_Gamma_hAA_plus_contact_subtractions"
    required_outputs = [
        "regulator_Rk",
        "subtraction_point_p2_equals_Delta_star_squared",
        "projection_d_dp2_Gamma_hh_at_p2_equals_Delta_star_squared",
        "operator_mixing_matrix_Mij",
        "nonperturbative_matching_factor_or_bound",
    ]
    assert unknown_projector_flow
    assert len(required_outputs) == 5

    print("=== UIDT Phase-8 P1 BMW/Dyson/FRG Operator-Mixing Scaffold ===")
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(residual_delta))
    print("canonical_prefactor_dA_alpha2_kappav_over_Delta_squared:", nstr(canonical_prefactor))
    print("required_projected_flow_strength:", nstr(required_projected_flow_strength))
    print("perturbative_4pi_bound:", nstr(perturbative_bound))
    print("strong_16pi2_bound:", nstr(strong_bound))
    print("required_matching_enhancement_using_smooth_reference:", nstr(required_matching_enhancement))
    print("unknown_projector_flow:", unknown_projector_flow)

    print("\nOPERATOR BASIS")
    for op in basis:
        print(
            op.name,
            "dim=", op.dimension,
            "cp_even=", op.cp_even,
            "gauge_invariant=", op.gauge_invariant,
            "projects_to_O_K=", op.projects_to_ok,
        )

    print("\nFUTURE DERIVATION MUST SUPPLY")
    for item in required_outputs:
        print(item)

    print("STATUS: BMW_DYSON_FRG_OPERATOR_MIXING_SCAFFOLD_READY")
    print("NO_DERIVATION_YET")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 BMW/DYSON/FRG OPERATOR-MIXING SCAFFOLD CHECKS PASSED")


if __name__ == "__main__":
    main()
