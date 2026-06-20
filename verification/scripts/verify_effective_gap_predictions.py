#!/usr/bin/env python3
"""Verify UIDT v3.9 effective-gap documentation numerics.

This script verifies only the reduced-model documentation numerics introduced
for the hybrid effective gap derivation. It does not prove pure Yang--Mills
existence or a Clay-level mass-gap theorem.

Evidence scope:
    - RG algebraic closure in the reduced model: [A]
    - Tensor glueball Regge estimate: [D]
    - Thermal screening ansatz: [D]

Rules:
    - native mpmath only
    - mp.dps = 80 set locally inside the verification routine
    - no float conversion for proof-critical values
    - fail-fast assertions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from mpmath import mp


@dataclass(frozen=True)
class TensorPrediction:
    delta_gev: mp.mpf
    sqrt_sigma_gev: mp.mpf
    spin_j: int
    mass_gev: mp.mpf
    ratio: mp.mpf


@dataclass(frozen=True)
class ThermalPoint:
    temperature_mev: mp.mpf
    tc_mev: mp.mpf
    gap_gev: mp.mpf
    normalized_gap: mp.mpf


def verify_reduced_rg_closure() -> mp.mpf:
    """Return |5 kappa^2 - 3 lambda_S| for exact canonical closure."""
    with mp.workdps(80):
        kappa = mp.mpf(1) / mp.mpf(2)
        lambda_s = mp.mpf(5) / mp.mpf(12)
        residual = abs(mp.mpf(5) * kappa**2 - mp.mpf(3) * lambda_s)
        assert residual == mp.mpf("0"), (
            "[RG_CONSTRAINT_FAIL] exact rational closure failed: "
            f"{mp.nstr(residual, 80)}"
        )
        return +residual


def tensor_glueball_prediction() -> TensorPrediction:
    """Compute the UIDT-Regge tensor-glueball estimate."""
    with mp.workdps(80):
        delta = mp.mpf("1.710")
        sqrt_sigma = mp.mpf("0.440")
        sigma = sqrt_sigma**2
        spin_j = 2
        mass_squared = delta**2 + mp.mpf(2) * mp.pi * sigma * mp.mpf(spin_j)
        assert mass_squared > mp.mpf("0"), "Tensor mass squared must be positive."
        mass = mp.sqrt(mass_squared)
        ratio = mass / delta
        assert mp.mpf("2.30") < mass < mp.mpf("2.33"), (
            "[TENSOR_PREDICTION_FAIL] mass outside documented interval: "
            f"{mp.nstr(mass, 80)}"
        )
        assert mp.mpf("1.34") < ratio < mp.mpf("1.37"), (
            "[TENSOR_RATIO_FAIL] ratio outside documented interval: "
            f"{mp.nstr(ratio, 80)}"
        )
        return TensorPrediction(
            delta_gev=+delta,
            sqrt_sigma_gev=+sqrt_sigma,
            spin_j=spin_j,
            mass_gev=+mass,
            ratio=+ratio,
        )


def thermal_gap(delta_gev: mp.mpf, temperature_mev: mp.mpf, tc_mev: mp.mpf) -> mp.mpf:
    """Return Delta(T) = Delta(0) * sqrt(max(0, 1 - (T/Tc)^4))."""
    with mp.workdps(80):
        assert tc_mev > mp.mpf("0"), "Critical temperature must be positive."
        assert temperature_mev >= mp.mpf("0"), "Temperature must be non-negative."
        ratio = temperature_mev / tc_mev
        kernel = mp.mpf("1") - ratio**4
        if kernel < mp.mpf("0"):
            kernel = mp.mpf("0")
        return +(delta_gev * mp.sqrt(kernel))


def thermal_points(
    temperatures_mev: Iterable[str] = ("100", "200", "250", "270"),
) -> tuple[ThermalPoint, ...]:
    """Compute representative thermal points for the documentation table."""
    with mp.workdps(80):
        delta = mp.mpf("1.710")
        tc = mp.mpf("270")
        points: list[ThermalPoint] = []
        for item in temperatures_mev:
            temperature = mp.mpf(item)
            gap = thermal_gap(delta, temperature, tc)
            normalized = gap / delta if delta != 0 else mp.mpf("0")
            assert gap >= mp.mpf("0"), "Thermal ansatz produced negative gap."
            assert normalized <= mp.mpf("1"), "Thermal normalized gap exceeded unity."
            points.append(
                ThermalPoint(
                    temperature_mev=+temperature,
                    tc_mev=+tc,
                    gap_gev=+gap,
                    normalized_gap=+normalized,
                )
            )

        assert points[0].gap_gev > mp.mpf("1.69")
        assert points[-1].gap_gev == mp.mpf("0")
        return tuple(points)


def main() -> None:
    with mp.workdps(80):
        residual = verify_reduced_rg_closure()
        tensor = tensor_glueball_prediction()
        points = thermal_points()

        print("[UIDT_EFFECTIVE_GAP_VERIFICATION]")
        print(f"RG residual |5 kappa^2 - 3 lambda_S| = {mp.nstr(residual, 80)} [A]")
        print(
            "Tensor glueball estimate m_2++ = "
            f"{mp.nstr(tensor.mass_gev, 50)} GeV [D]"
        )
        print(
            "Tensor/scalar ratio m_2++/m_0++ = "
            f"{mp.nstr(tensor.ratio, 50)} [D]"
        )
        for point in points:
            print(
                "Thermal ansatz: T = "
                f"{mp.nstr(point.temperature_mev, 20)} MeV, "
                "Delta(T) = "
                f"{mp.nstr(point.gap_gev, 50)} GeV, "
                "Delta(T)/Delta(0) = "
                f"{mp.nstr(point.normalized_gap, 50)} [D]"
            )
        print("[PASS] Effective-gap documentation numerics verified at mp.dps=80.")


if __name__ == "__main__":
    main()
