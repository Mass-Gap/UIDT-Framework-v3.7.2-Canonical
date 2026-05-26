#!/usr/bin/env python3
"""UIDT v3.9 Phase-8 P1 BMW/Dyson/FRG flow-projection audit.

This verifier implements a bounded diagnostic projection for the next P1 step:

    partial_t Z_h = P_K[partial_t Gamma_k]

with projection onto O_K = 1/2 (partial h)^2 at p^2 = Delta*^2.

The regulator is an explicit dimensionless Litim single-scale diagnostic:

    R_k(q) = Z_A (k^2 - q^2) theta(k^2 - q^2)

used for the single-scale internal gauge line. This is a controlled diagnostic
bound, not a complete BMW solution and not a derivation of gamma.

Evidence status: [D]/[E] only. No [A] promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from mpmath import mp


DIM = 4


@dataclass(frozen=True)
class MixingEntry:
    source: str
    target: str
    value: mp.mpf | None
    status: str


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


def litim_denominator(s2: mp.mpf, mu2: mp.mpf) -> mp.mpf:
    """Dimensionless inverse propagator q^2 + R_k(q) + mu^2 for Z_A=1, k=1."""
    if s2 < 1:
        return mp.mpf(1) + mu2
    return s2 + mu2


def single_scale_weight_litim(q2: mp.mpf, mu2: mp.mpf) -> mp.mpf:
    """Dimensionless G(q)^2 partial_t R_k(q) with Litim support.

    The constant factor 2 corresponds to partial_t R_k inside q^2<k^2.
    Anomalous-dimension feedback is omitted and must be supplied by a later
    full BMW calculation.
    """
    if q2 < 1:
        return mp.mpf(2) / (mp.mpf(1) + mu2) ** 2
    return mp.mpf(0)


def flow_kernel_bmw_litim(
    y2: mp.mpf,
    mu_ir: mp.mpf,
    n_radial: int = 30,
    n_angle: int = 30,
) -> mp.mpf:
    """Dimensionless Litim single-scale BMW diagnostic kernel.

    y2 = p^2/k^2, k = Delta*, p^2 = Delta*^2 at subtraction y2=1.
    Angular reduction: dOmega_3 = 4*pi*sqrt(1-c^2) dc.
    Momentum support: single-scale q line has q^2<1.
    """
    assert y2 > 0
    assert mu_ir > 0
    y = mp.sqrt(y2)
    dx = mp.mpf(1) / mp.mpf(n_radial)
    dc = mp.mpf(2) / mp.mpf(n_angle)
    prefactor = mp.mpf(1) / (4 * mp.pi**3)
    p = [y, mp.mpf(0), mp.mpf(0), mp.mpf(0)]
    total = mp.mpf(0)
    mu2 = mu_ir**2

    for i in range(n_radial):
        x = (mp.mpf(i) + mp.mpf("0.5")) * dx
        for j in range(n_angle):
            c = -mp.mpf(1) + (mp.mpf(j) + mp.mpf("0.5")) * dc
            s = mp.sqrt(1 - c**2)
            q = [x * c, x * s, mp.mpf(0), mp.mpf(0)]
            kvec = [q[0] + p[0], q[1], mp.mpf(0), mp.mpf(0)]
            q2 = dot(q, q)
            k2 = dot(kvec, kvec)
            ss = single_scale_weight_litim(q2, mu2)
            if ss == 0:
                continue
            numerator = transverse_bubble_numerator(q, p)
            second_line = mp.mpf(1) / litim_denominator(k2, mu2)
            angular_weight = mp.sqrt(1 - c**2)
            total += x**3 * angular_weight * numerator * ss * second_line * dx * dc

    return prefactor * total


def derivative_wrt_y2(y2: mp.mpf, mu_ir: mp.mpf, step: mp.mpf) -> mp.mpf:
    assert y2 - step > 0
    return (flow_kernel_bmw_litim(y2 + step, mu_ir) - flow_kernel_bmw_litim(y2 - step, mu_ir)) / (2 * step)


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
    e_t_mev = mp.mpf("2.44")
    alpha_s_ref = mp.mpf("0.326")

    k_t_mev = 4 * mp.pi * e_t_mev
    mu_ir = k_t_mev / delta_star_mev
    y2_subtraction = mp.mpf(1)
    dy2 = mp.mpf("0.01")

    j_flow = flow_kernel_bmw_litim(y2_subtraction, mu_ir)
    projected_flow = derivative_wrt_y2(y2_subtraction, mu_ir, dy2)

    canonical_prefactor = da * alpha_s_ref**2 * (kappa * v_mev / delta_star_mev) ** 2
    delta_model_signed = canonical_prefactor * projected_flow
    delta_model_abs = abs(delta_model_signed)
    residual_abs = abs(delta_model_abs - delta_required)
    enhancement_required = delta_required / delta_model_abs if delta_model_abs != 0 else mp.inf

    reduced_mixing_entries = [
        MixingEntry("O_hFF x O_hFF", "O_K", projected_flow, "computed_D_diagnostic"),
        MixingEntry("O_h2FF", "O_K", mp.mpf(0), "contact_not_direct_kinetic"),
        MixingEntry("O_dh2FF", "O_K", None, "requires_external_matching"),
    ]

    assert j_flow >= 0
    assert delta_model_abs >= 0
    assert residual_abs > mp.mpf("1e-14")
    assert enhancement_required > mp.mpf(1)

    print("=== UIDT Phase-8 P1 BMW/Dyson/FRG Flow Projection Audit ===")
    print("regulator_Rk:", "Litim_Rk_ZA_k2_minus_q2_theta_k2_minus_q2")
    print("subtraction_y2_p2_over_k2:", nstr(y2_subtraction))
    print("k_identification:", "k_equals_Delta_star")
    print("projection:", "P_K_d_dp2_Gamma_hh_2_at_p2_equals_Delta_star_squared")
    print("Delta_gamma_required:", nstr(delta_required))
    print("Delta_gamma_required_residual_to_17_over_3000:", nstr(residual_delta))
    print("k_T_mev:", nstr(k_t_mev))
    print("mu_IR_kT_over_Delta:", nstr(mu_ir))
    print("BMW_Litim_flow_kernel_J:", nstr(j_flow))
    print("projected_flow_dJ_dy2:", nstr(projected_flow))
    print("canonical_prefactor_dA_alpha2_kappav_over_Delta_squared:", nstr(canonical_prefactor))
    print("Delta_gamma_model_signed:", nstr(delta_model_signed))
    print("Delta_gamma_model_abs:", nstr(delta_model_abs))
    print("residual_abs_to_17_over_3000:", nstr(residual_abs))
    print("enhancement_required_abs:", nstr(enhancement_required))

    print("\nREDUCED OPERATOR-MIXING SUBMATRIX")
    for entry in reduced_mixing_entries:
        value = "UNDETERMINED" if entry.value is None else nstr(entry.value)
        print(entry.source, "->", entry.target, "=", value, "status=", entry.status)

    if residual_abs < mp.mpf("1e-3"):
        print("STATUS: PARTIAL_SCALE_HIT_D_REQUIRES_FULL_BMW_DERIVATION")
    else:
        print("STATUS: BMW_LITIM_FLOW_PROJECTION_NO_GO_FOR_MINIMAL_MATCHING")

    print("SIGN_NOTE: projected_flow sign is scheme-dependent for Delta_Z convention")
    print("NO_EVIDENCE_PROMOTION")
    print("ALL PHASE-8 P1 BMW/DYSON/FRG FLOW PROJECTION CHECKS PASSED")


if __name__ == "__main__":
    main()
