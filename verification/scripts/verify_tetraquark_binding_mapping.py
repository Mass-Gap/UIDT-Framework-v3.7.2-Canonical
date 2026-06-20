#!/usr/bin/env python3
"""Verify UIDT v3.9 tetraquark-binding mapping arithmetic.

This script verifies only the documentation-level [E] arithmetic used in
	docs/predictions/tetraquark_binding.md

It does not validate the physical tetraquark interpretation, does not compute
a coupled-channel scattering amplitude, and does not replace unquenched lattice
QCD or heavy-hadron effective field theory.

Rules:
    - native mpmath only
    - mp.dps = 80 set locally inside the verification routine
    - no float conversion for proof-critical values
    - fail-fast assertions
"""

from __future__ import annotations

from dataclasses import dataclass
from mpmath import mp


@dataclass(frozen=True)
class TetraquarkMapping:
    delta3_gev: mp.mpf
    raw_mass_gev: mp.mpf
    threshold_gev: mp.mpf
    excess_gev: mp.mpf
    g_threshold: mp.mpf
    g_minus_273kev: mp.mpf


def unquenched_delta3(delta0_gev: mp.mpf = mp.mpf("1.710")) -> mp.mpf:
    """Return Delta*(3) = Delta*(0) * sqrt(27/33)."""
    with mp.workdps(80):
        assert delta0_gev > mp.mpf("0"), "Delta*(0) must be positive."
        value = delta0_gev * mp.sqrt(mp.mpf("27") / mp.mpf("33"))
        assert value > mp.mpf("0"), "Delta*(3) must be positive."
        assert value < delta0_gev, "Unquenched screening must reduce the pure-gauge anchor."
        return +value


def tetraquark_mapping() -> TetraquarkMapping:
    """Verify the benchmark tetraquark mapping arithmetic."""
    with mp.workdps(80):
        delta3 = unquenched_delta3()
        charm_mass = mp.mpf("1.275")
        light_proxy = mp.mpf("0.005")
        core_offset = mp.mpf("0.200")
        g_eff = mp.mpf("1.000")
        threshold = mp.mpf("1.8648") + mp.mpf("2.0102")
        target_offset = mp.mpf("0.000273")

        raw_mass = (
            mp.mpf("2") * charm_mass
            + mp.mpf("2") * light_proxy
            + g_eff * (delta3 - core_offset)
        )
        excess = raw_mass - threshold
        denominator = delta3 - core_offset
        assert denominator > mp.mpf("0"), "Diquark denominator must be positive."

        g_threshold = (threshold - mp.mpf("2") * charm_mass - mp.mpf("2") * light_proxy) / denominator
        g_minus_273kev = (
            threshold
            - target_offset
            - mp.mpf("2") * charm_mass
            - mp.mpf("2") * light_proxy
        ) / denominator

        assert raw_mass > threshold, "Raw benchmark is expected to lie above threshold."
        assert mp.mpf("0.031") < excess < mp.mpf("0.032"), (
            "[TCC_EXCESS_FAIL] raw-threshold excess outside documented interval: "
            f"{mp.nstr(excess, 80)}"
        )
        assert mp.mpf("0.97") < g_threshold < mp.mpf("0.98"), (
            "[TCC_GEFF_FAIL] threshold coupling outside documented interval: "
            f"{mp.nstr(g_threshold, 80)}"
        )
        assert g_minus_273kev < g_threshold, (
            "Sub-threshold coupling must be slightly below threshold coupling."
        )

        return TetraquarkMapping(
            delta3_gev=+delta3,
            raw_mass_gev=+raw_mass,
            threshold_gev=+threshold,
            excess_gev=+excess,
            g_threshold=+g_threshold,
            g_minus_273kev=+g_minus_273kev,
        )


def main() -> None:
    with mp.workdps(80):
        mapping = tetraquark_mapping()
        print("[UIDT_TETRAQUARK_BINDING_MAPPING_VERIFICATION]")
        print(f"Delta*(3) = {mp.nstr(mapping.delta3_gev, 50)} GeV [D]")
        print(f"M_raw(T_cc+) = {mp.nstr(mapping.raw_mass_gev, 50)} GeV [E]")
        print(f"D0 D*+ threshold = {mp.nstr(mapping.threshold_gev, 50)} GeV [B-context]")
        print(f"Raw excess = {mp.nstr(mapping.excess_gev, 50)} GeV [E]")
        print(f"g_eff(threshold) = {mp.nstr(mapping.g_threshold, 50)} [E]")
        print(f"g_eff(-273 keV) = {mp.nstr(mapping.g_minus_273kev, 50)} [E]")
        print("[PASS] Tetraquark mapping arithmetic verified at mp.dps=80.")


if __name__ == "__main__":
    main()
