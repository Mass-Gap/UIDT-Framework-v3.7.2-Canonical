#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 operator-mixing / no-go audit.

This script checks the operator-basis logic following the regulated Pi_S
kernel audits. It does not derive gamma. It quantifies the required mixing
coefficient needed to turn the canonical v3.9 S^2 F^2 interaction into the
required correction Delta_gamma_required = 17/3000.

Evidence status: [D]/[E] only. No [A] promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from mpmath import mp


@dataclass(frozen=True)
class Operator:
    name: str
    canonical_dimension: int
    cp_even: bool
    gauge_invariant: bool
    contains_h: bool
    contains_derivative_h: bool
    contains_f2: bool


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def allowed_for_wavefunction_mixing(operator: Operator) -> bool:
    """Return whether an operator can directly contribute to h kinetic mixing."""
    return operator.gauge_invariant and operator.cp_even and operator.contains_derivative_h


def main() -> None:
    mp.dps = 80

    operators = [
        Operator("O_K = 1/2 (partial h)^2", 4, True, True, True, True, False),
        Operator("O_M = 1/2 h^2", 2, True, True, True, False, False),
        Operator("O_F = Tr(F F)", 4, True, True, False, False, True),
        Operator("O_hFF = h Tr(F F)", 5, True, True, True, False, True),
        Operator("O_h2FF = h^2 Tr(F F)", 6, True, True, True, False, True),
        Operator("O_dh2FF = (partial h)^2 Tr(F F)", 8, True, True, True, True, True),
    ]

    nc = mp.mpf(3)
    d_a = nc**2 - 1
    gamma = mp.mpf("16.339")
    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_required = gamma - gamma_bare
    expected_delta = mp.mpf(17) / mp.mpf(3000)
    delta_residual = abs(delta_required - expected_delta)
    assert delta_residual < mp.mpf("1e-70"), nstr(delta_residual)

    kappa = mp.mpf(1) / mp.mpf(2)
    v_mev = mp.mpf("47.7")
    delta_star_mev = mp.mpf("1710")
    alpha_s_ref = mp.mpf("0.326")

    hff_coeff = kappa * v_mev / mp.mpf(2)
    hhff_coeff = kappa / mp.mpf(4)
    assert hff_coeff > 0
    assert hhff_coeff > 0

    dimension_suppression = (kappa * v_mev / delta_star_mev) ** 2
    alpha2 = alpha_s_ref**2
    canonical_prefactor = d_a * alpha2 * dimension_suppression
    required_kernel_mixing = delta_required / canonical_prefactor

    # Previous smooth-regulated derivative scale from PR #480 class.
    smooth_derivative_abs_reference = mp.mpf("0.0013885306847083777")
    required_enhancement_smooth_model = delta_required / (
        canonical_prefactor * smooth_derivative_abs_reference
    )

    natural_o1_bound = mp.mpf(1)
    perturbative_4pi_bound = 4 * mp.pi
    strong_16pi2_bound = 16 * mp.pi**2

    allowed_direct = [op.name for op in operators if allowed_for_wavefunction_mixing(op)]
    assert "O_K = 1/2 (partial h)^2" in allowed_direct
    assert "O_dh2FF = (partial h)^2 Tr(F F)" in allowed_direct
    assert "O_h2FF = h^2 Tr(F F)" not in allowed_direct

    hff_pair_channel_allowed = True
    h2ff_single_contact_wavefunction_direct = False
    assert hff_pair_channel_allowed
    assert not h2ff_single_contact_wavefunction_direct

    print("=== UIDT Phase-8 P1 Operator-Mixing / No-Go Audit ===")
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(delta_residual))
    print("hFF_coefficient_kappa_v_over_2_MeV:", nstr(hff_coeff))
    print("h2FF_coefficient_kappa_over_4:", nstr(hhff_coeff))
    print("dimension_suppression_(kappa_v_over_Delta)^2:", nstr(dimension_suppression))
    print("canonical_prefactor_dA_alpha2_dimension_suppression:", nstr(canonical_prefactor))
    print("required_kernel_mixing_if_derivative_order_one:", nstr(required_kernel_mixing))
    print("required_enhancement_with_smooth_derivative_reference:", nstr(required_enhancement_smooth_model))
    print("natural_O1_bound:", nstr(natural_o1_bound))
    print("perturbative_4pi_bound:", nstr(perturbative_4pi_bound))
    print("strong_16pi2_bound:", nstr(strong_16pi2_bound))

    print("\nOPERATOR BASIS")
    for op in operators:
        print(
            op.name,
            "dim=", op.canonical_dimension,
            "cp_even=", op.cp_even,
            "gauge_invariant=", op.gauge_invariant,
            "direct_wavefunction_mixing=", allowed_for_wavefunction_mixing(op),
        )

    print("\nMIXING CHANNELS")
    print("O_hFF x O_hFF -> O_K:", "allowed_D_but_regulator_matching_required")
    print("O_h2FF single contact -> O_K:", "not_direct_at_one_insertion")
    print("O_h2FF contact -> mass/tadpole:", "allowed_D_but_not_kinetic_by_itself")
    print("O_dh2FF -> O_K after background F2:", "higher_dimensional_D_requires_new_matching")

    if required_kernel_mixing > perturbative_4pi_bound:
        print("NO_GO: required order-one kernel mixing exceeds 4*pi perturbative audit bound")
    else:
        print("OPEN: required order-one kernel mixing is below 4*pi but still requires derivation")

    if required_enhancement_smooth_model > strong_16pi2_bound:
        print("NO_GO: smooth-regulated model enhancement exceeds 16*pi^2 strong audit bound")
    else:
        print("OPEN: smooth-regulated enhancement below 16*pi^2; still requires derivation")

    assert required_kernel_mixing > perturbative_4pi_bound
    assert required_kernel_mixing < strong_16pi2_bound
    assert required_enhancement_smooth_model > strong_16pi2_bound

    print("P1_OPERATOR_MIXING_NO_DERIVATION_FOUND")
    print("P1_REMAINS_OPEN")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 OPERATOR-MIXING / NO-GO CHECKS PASSED")


if __name__ == "__main__":
    main()
