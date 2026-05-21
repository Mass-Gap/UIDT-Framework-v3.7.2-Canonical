#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 Pi_S kernel-structure audit.

This script checks structural consequences of the canonical v3.9 coupling

    L_int = -(kappa/4) S^2 Tr(F_{mu nu} F^{mu nu})

expanded around S = v + h.  It does not derive gamma.  It verifies:

1. the required correction Delta_gamma_required = 17/3000;
2. the h F F and h^2 F F coefficient hierarchy;
3. positivity of the Euclidean transverse two-gluon bubble numerator on a
   deterministic angular grid;
4. the scale mismatch of a dimension-suppressed canonical hFF bubble estimate;
5. the need for an explicit regulator/renormalization/matching prescription.

Evidence status: [D]/[E] only.  No [A] promotion.
"""

from __future__ import annotations

from mpmath import mp


DIM = 4


def nstr(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def dot(a: list[mp.mpf], b: list[mp.mpf]) -> mp.mpf:
    return mp.fsum(a[i] * b[i] for i in range(DIM))


def projector(q: list[mp.mpf]) -> list[list[mp.mpf]]:
    q2 = dot(q, q)
    assert q2 > 0, "projector requires non-zero momentum"
    return [
        [
            (mp.mpf(1) if mu == nu else mp.mpf(0)) - q[mu] * q[nu] / q2
            for nu in range(DIM)
        ]
        for mu in range(DIM)
    ]


def hff_vertex_tensor(q: list[mp.mpf], k: list[mp.mpf]) -> list[list[mp.mpf]]:
    qk = dot(q, k)
    return [
        [
            qk * (mp.mpf(1) if mu == nu else mp.mpf(0)) - q[nu] * k[mu]
            for nu in range(DIM)
        ]
        for mu in range(DIM)
    ]


def transverse_bubble_numerator(q: list[mp.mpf], p: list[mp.mpf]) -> mp.mpf:
    k = [q[i] + p[i] for i in range(DIM)]
    v = hff_vertex_tensor(q, k)
    pq = projector(q)
    pk = projector(k)
    total = mp.mpf(0)
    for mu in range(DIM):
        for nu in range(DIM):
            for alpha in range(DIM):
                for beta in range(DIM):
                    total += v[mu][nu] * pq[mu][alpha] * pk[nu][beta] * v[alpha][beta]
    return total


def classify_residual(value: mp.mpf, target: mp.mpf) -> str:
    r = abs(value - target)
    if r < mp.mpf("1e-14"):
        return "PROOF_LEVEL_NUMERICAL_CLOSURE_REQUIRES_DERIVATION"
    if r < mp.mpf("1e-3"):
        return "PARTIAL_SCALE_HIT_D"
    return "NO_GO_SCALE_MISMATCH_E"


def main() -> None:
    mp.dps = 80

    nc = mp.mpf(3)
    d_a = nc**2 - 1
    gamma = mp.mpf("16.339")
    gamma_bare = (2 * nc + 1) ** 2 / nc
    delta_required = gamma - gamma_bare
    delta_expected = mp.mpf(17) / mp.mpf(3000)
    delta_residual = abs(delta_required - delta_expected)
    assert delta_residual < mp.mpf("1e-70"), nstr(delta_residual)

    kappa = mp.mpf(1) / mp.mpf(2)
    v_mev = mp.mpf("47.7")
    delta_star_mev = mp.mpf("1710")
    alpha_s_ref = mp.mpf("0.326")

    hff_coeff = kappa * v_mev / mp.mpf(2)
    hhff_coeff = kappa / mp.mpf(4)
    coeff_ratio = hff_coeff / hhff_coeff
    assert coeff_ratio == 2 * v_mev

    unit_2loop = alpha_s_ref**2 / (16 * mp.pi**2)
    dimension_suppression = (kappa * v_mev / delta_star_mev) ** 2
    canonical_dim6_bubble_estimate = d_a * unit_2loop * dimension_suppression
    canonical_dim6_residual = abs(canonical_dim6_bubble_estimate - delta_required)
    canonical_dim6_enhancement_required = delta_required / canonical_dim6_bubble_estimate

    linear_audit_required_coefficient = delta_required / unit_2loop

    p_mag = delta_star_mev
    p = [p_mag, mp.mpf(0), mp.mpf(0), mp.mpf(0)]
    q_magnitudes = [p_mag / 4, p_mag, 4 * p_mag]
    cos_values = [mp.mpf("-0.75"), mp.mpf("-0.25"), mp.mpf("0.25"), mp.mpf("0.75")]
    min_num = None
    max_num = None
    for q_mag in q_magnitudes:
        for c in cos_values:
            s = mp.sqrt(1 - c**2)
            q = [q_mag * c, q_mag * s, mp.mpf(0), mp.mpf(0)]
            num = transverse_bubble_numerator(q, p)
            if min_num is None or num < min_num:
                min_num = num
            if max_num is None or num > max_num:
                max_num = num
            assert num >= -mp.mpf("1e-40"), nstr(num)

    assert min_num is not None
    assert max_num is not None
    assert canonical_dim6_bubble_estimate > 0
    assert canonical_dim6_residual > mp.mpf("1e-3")
    assert canonical_dim6_enhancement_required > mp.mpf(1000)
    assert linear_audit_required_coefficient > d_a

    print("=== UIDT Phase-8 P1 Pi_S Kernel-Structure Audit ===")
    print("gamma_bare:", nstr(gamma_bare))
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(delta_residual))
    print("hFF_coefficient_kappa_v_over_2_MeV:", nstr(hff_coeff))
    print("hhFF_coefficient_kappa_over_4:", nstr(hhff_coeff))
    print("hFF_to_hhFF_ratio:", nstr(coeff_ratio))
    print("Euclidean_transverse_numerator_min_grid:", nstr(min_num))
    print("Euclidean_transverse_numerator_max_grid:", nstr(max_num))
    print("unit_alpha_s2_over_16pi2:", nstr(unit_2loop))
    print("dimension_suppression_(kappa_v_over_Delta)^2:", nstr(dimension_suppression))
    print("canonical_dim6_bubble_estimate:", nstr(canonical_dim6_bubble_estimate))
    print("canonical_dim6_bubble_residual:", nstr(canonical_dim6_residual))
    print("canonical_dim6_status:", classify_residual(canonical_dim6_bubble_estimate, delta_required))
    print("canonical_dim6_enhancement_required:", nstr(canonical_dim6_enhancement_required))
    print("linear_audit_required_coefficient_if_no_dim6_suppression:", nstr(linear_audit_required_coefficient))
    print("TENSION_ALERT: v3.9 S^2F^2 and v4.1 SFF audit forms must not be silently merged")
    print("CONTACT_TADPOLE_NOTE: h^2AA contact is p-independent at this level and cannot by itself fix wave-function Delta_gamma")
    print("P1_PI_S_KERNEL_NOT_DERIVED")
    print("ALL PHASE-8 P1 PI_S KERNEL STRUCTURE CHECKS PASSED")


if __name__ == "__main__":
    main()
