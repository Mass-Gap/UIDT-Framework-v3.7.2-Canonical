#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 regulated Pi_S integral audit.

This script evaluates a minimal Euclidean regulated hFF bubble model for the
canonical v3.9 interaction

    L_int = -(kappa/4) S^2 Tr(F F),  S = v + h.

It does not derive gamma. It checks the sign and scale of a regulated kernel
under an explicit smooth cutoff and documents whether the result can reach
Delta_gamma_required = 17/3000 without an additional matching enhancement.

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


def regulated_kernel_j(
    y2: mp.mpf,
    mu_ir: mp.mpf,
    n_radial: int = 24,
    n_angle: int = 24,
    x_max: mp.mpf = mp.mpf(6),
) -> mp.mpf:
    """Dimensionless smooth-cutoff Euclidean bubble kernel.

    y2 = p^2 / Lambda^2, x = |q| / Lambda, Lambda = Delta*.
    Regulator: exp[-(q^2 + (q+p)^2)/Lambda^2].
    IR denominator: (q^2 + mu_ir^2)((q+p)^2 + mu_ir^2).

    The four-dimensional angular measure is reduced to
    dOmega_3 = 4*pi*sqrt(1-c^2) dc.
    """
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
            numerator = transverse_bubble_numerator(q, p)
            denominator = (q2 + mu_ir**2) * (k2 + mu_ir**2)
            regulator = mp.exp(-(q2 + k2))
            angular_weight = mp.sqrt(1 - c**2)
            total += x**3 * angular_weight * numerator * regulator / denominator * dx * dc

    return prefactor * total


def derivative_wrt_y2(y2: mp.mpf, mu_ir: mp.mpf, step: mp.mpf) -> mp.mpf:
    assert y2 - step > 0
    return (regulated_kernel_j(y2 + step, mu_ir) - regulated_kernel_j(y2 - step, mu_ir)) / (2 * step)


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
    j0 = regulated_kernel_j(y2_subtraction, mu_ir)
    j_prime = derivative_wrt_y2(y2_subtraction, mu_ir, finite_difference_step)

    dimension_prefactor = d_a * alpha_s_ref**2 * (kappa * v_mev / delta_star_mev) ** 2
    delta_gamma_model = dimension_prefactor * j_prime
    delta_gamma_model_abs = abs(delta_gamma_model)
    residual_signed = abs(delta_gamma_model - delta_required)
    residual_abs = abs(delta_gamma_model_abs - delta_required)
    enhancement_required_abs = delta_required / delta_gamma_model_abs

    assert j0 > 0
    assert j_prime < 0
    assert delta_gamma_model < 0
    assert delta_gamma_model_abs > 0
    assert residual_abs > mp.mpf("1e-3")
    assert enhancement_required_abs > mp.mpf("1000")

    print("=== UIDT Phase-8 P1 Regulated Pi_S Integral Audit ===")
    print("regulator:", "smooth_exp_exp_minus_q2_plus_k2_over_Lambda2")
    print("subtraction_y2_p2_over_Delta2:", nstr(y2_subtraction))
    print("finite_difference_step_y2:", nstr(finite_difference_step))
    print("gamma_bare:", nstr(gamma_bare))
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(delta_residual))
    print("k_T_mev:", nstr(k_t_mev))
    print("mu_IR_kT_over_Delta:", nstr(mu_ir))
    print("J_y2_equals_1:", nstr(j0))
    print("dJ_dy2_at_y2_equals_1:", nstr(j_prime))
    print("dimension_prefactor_dA_alpha2_kappav_over_Delta_squared:", nstr(dimension_prefactor))
    print("Delta_gamma_model_signed:", nstr(delta_gamma_model))
    print("Delta_gamma_model_abs:", nstr(delta_gamma_model_abs))
    print("residual_signed_to_required:", nstr(residual_signed))
    print("residual_abs_to_required:", nstr(residual_abs))
    print("enhancement_required_abs:", nstr(enhancement_required_abs))
    print("SIGN_NOTE: dJ/dy2 is negative in this convention; DeltaZ sign requires explicit renormalization convention")
    print("NO_GO: minimal smooth-regulated canonical bubble is far below 17/3000 without extra matching enhancement")
    print("P1_REGULATED_PI_S_INTEGRAL_NOT_DERIVED")
    print("ALL PHASE-8 P1 REGULATED PI_S INTEGRAL CHECKS PASSED")


if __name__ == "__main__":
    main()
