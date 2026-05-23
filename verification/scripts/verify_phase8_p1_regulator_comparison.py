#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 regulator-comparison audit.

This script compares three explicitly defined diagnostic regulators for the
same Euclidean hFF bubble model used in the regulated Pi_S audit:

1. smooth exponential: exp[-(q^2 + k^2)/Delta*^2]
2. compact Litim-style support: (1-q^2)(1-k^2) theta(1-q^2) theta(1-k^2)
3. sharp unit support: theta(1-q^2) theta(1-k^2)

The subtraction point is fixed at y^2 = p^2/Delta*^2 = 1.

This script does not derive gamma. It tests regulator sensitivity and the
magnitude deficit relative to Delta_gamma_required = 17/3000.

Evidence status: [D]/[E] only. No [A] promotion.
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
    vtx = hff_vertex_tensor(q, k)
    pq = projector(q)
    pk = projector(k)
    total = mp.mpf(0)
    for mu in range(DIM):
        for nu in range(DIM):
            for alpha in range(DIM):
                for beta in range(DIM):
                    total += vtx[mu][nu] * pq[mu][alpha] * pk[nu][beta] * vtx[alpha][beta]
    return total


def regulator_weight(name: str, q2: mp.mpf, k2: mp.mpf) -> mp.mpf:
    if name == "smooth_exponential":
        return mp.exp(-(q2 + k2))
    if name == "compact_litim_style":
        if q2 < 1 and k2 < 1:
            return (1 - q2) * (1 - k2)
        return mp.mpf(0)
    if name == "sharp_unit_support":
        if q2 < 1 and k2 < 1:
            return mp.mpf(1)
        return mp.mpf(0)
    raise ValueError(f"unknown regulator: {name}")


def regulated_kernel_j(
    regulator: str,
    y2: mp.mpf,
    mu_ir: mp.mpf,
    n_radial: int = 24,
    n_angle: int = 24,
    x_max: mp.mpf = mp.mpf(6),
) -> mp.mpf:
    """Dimensionless Euclidean bubble kernel for one diagnostic regulator."""
    assert y2 > 0
    assert mu_ir > 0
    y = mp.sqrt(y2)
    dx = x_max / mp.mpf(n_radial)
    dc = mp.mpf(2) / mp.mpf(n_angle)
    prefactor = mp.mpf(1) / (4 * mp.pi**3)
    p = [y, mp.mpf(0), mp.mpf(0), mp.mpf(0)]
    total = mp.mpf(0)

    for i in range(n_radial):
        x = (mp.mpf(i) + mp.mpf("0.5")) * dx
        for j in range(n_angle):
            c = -mp.mpf(1) + (mp.mpf(j) + mp.mpf("0.5")) * dc
            s = mp.sqrt(1 - c**2)
            q = [x * c, x * s, mp.mpf(0), mp.mpf(0)]
            k = [q[0] + p[0], q[1], mp.mpf(0), mp.mpf(0)]
            q2 = dot(q, q)
            k2 = dot(k, k)
            weight = regulator_weight(regulator, q2, k2)
            if weight == 0:
                continue
            numerator = transverse_bubble_numerator(q, p)
            denominator = (q2 + mu_ir**2) * (k2 + mu_ir**2)
            angular_weight = mp.sqrt(1 - c**2)
            total += x**3 * angular_weight * numerator * weight / denominator * dx * dc

    return prefactor * total


def derivative_wrt_y2(regulator: str, y2: mp.mpf, mu_ir: mp.mpf, step: mp.mpf) -> mp.mpf:
    assert y2 - step > 0
    j_plus = regulated_kernel_j(regulator, y2 + step, mu_ir)
    j_minus = regulated_kernel_j(regulator, y2 - step, mu_ir)
    return (j_plus - j_minus) / (2 * step)


def classify(model_abs: mp.mpf, target: mp.mpf) -> str:
    r = abs(model_abs - target)
    if r < mp.mpf("1e-14"):
        return "NUMERICAL_CLOSURE_BUT_DERIVATION_REQUIRED"
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
    expected_delta = mp.mpf(17) / mp.mpf(3000)
    delta_residual = abs(delta_required - expected_delta)
    assert delta_residual < mp.mpf("1e-70"), nstr(delta_residual)

    kappa = mp.mpf(1) / mp.mpf(2)
    v_mev = mp.mpf("47.7")
    delta_star_mev = mp.mpf("1710")
    e_t_mev = mp.mpf("2.44")
    alpha_s_ref = mp.mpf("0.326")
    k_t_mev = 4 * mp.pi * e_t_mev
    mu_ir = k_t_mev / delta_star_mev

    y2_subtraction = mp.mpf(1)
    finite_difference_step = mp.mpf("0.01")
    dimension_prefactor = d_a * alpha_s_ref**2 * (kappa * v_mev / delta_star_mev) ** 2

    regulators = [
        "smooth_exponential",
        "compact_litim_style",
        "sharp_unit_support",
    ]

    print("=== UIDT Phase-8 P1 Regulator Comparison Audit ===")
    print("gamma_bare:", nstr(gamma_bare))
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(delta_residual))
    print("subtraction_y2_p2_over_Delta2:", nstr(y2_subtraction))
    print("finite_difference_step_y2:", nstr(finite_difference_step))
    print("k_T_mev:", nstr(k_t_mev))
    print("mu_IR_kT_over_Delta:", nstr(mu_ir))
    print("dimension_prefactor_dA_alpha2_kappav_over_Delta_squared:", nstr(dimension_prefactor))

    best_abs_residual = None
    best_name = "none"
    for name in regulators:
        j0 = regulated_kernel_j(name, y2_subtraction, mu_ir)
        j_prime = derivative_wrt_y2(name, y2_subtraction, mu_ir, finite_difference_step)
        delta_model_signed = dimension_prefactor * j_prime
        delta_model_abs = abs(delta_model_signed)
        residual_signed = abs(delta_model_signed - delta_required)
        residual_abs = abs(delta_model_abs - delta_required)
        enhancement = mp.inf if delta_model_abs == 0 else delta_required / delta_model_abs
        status = classify(delta_model_abs, delta_required)

        if best_abs_residual is None or residual_abs < best_abs_residual:
            best_abs_residual = residual_abs
            best_name = name

        print("\nREGULATOR", name)
        print("J_y2_equals_1:", nstr(j0))
        print("dJ_dy2_at_y2_equals_1:", nstr(j_prime))
        print("Delta_gamma_model_signed:", nstr(delta_model_signed))
        print("Delta_gamma_model_abs:", nstr(delta_model_abs))
        print("residual_signed_to_required:", nstr(residual_signed))
        print("residual_abs_to_required:", nstr(residual_abs))
        print("enhancement_required_abs:", nstr(enhancement))
        print("status:", status)

        assert j0 >= 0
        assert delta_model_abs >= 0
        assert residual_abs > mp.mpf("1e-14")

    assert best_abs_residual is not None

    print("\nSUMMARY")
    print("best_regulator_by_abs_residual:", best_name)
    print("best_abs_residual:", nstr(best_abs_residual))
    print("REGULATOR_COMPARISON_NO_PROOF_LEVEL_CLOSURE")
    print("P1_REMAINS_OPEN")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 REGULATOR COMPARISON CHECKS PASSED")


if __name__ == "__main__":
    main()
