#!/usr/bin/env python3
"""Verify UIDT v3.9 unquenched-QCD screening ansatz numerics.

This script verifies only the documentation-level [D] ansatz

    Delta*(N_f) = Delta*(0) * sqrt((33 - 2 N_f) / 33)

for the representative values used in docs/predictions/unquenched_qcd.md.
It does not prove the physical validity of the ansatz, does not derive full
QCD, and does not compute a physical pion-sector mass gap.

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
class UnquenchedPoint:
    n_flavors: mp.mpf
    beta0_ratio: mp.mpf
    delta_gev: mp.mpf


def beta0_ratio_su3(n_flavors: mp.mpf) -> mp.mpf:
    """Return beta0(N_f)/beta0(0) for SU(3)."""
    with mp.workdps(80):
        assert n_flavors >= mp.mpf("0"), "N_f must be non-negative."
        ratio = (mp.mpf("33") - mp.mpf("2") * n_flavors) / mp.mpf("33")
        assert ratio > mp.mpf("0"), "Asymptotic-freedom proxy requires positive beta0 ratio."
        return +ratio


def screened_gap(n_flavors: mp.mpf, delta0_gev: mp.mpf = mp.mpf("1.710")) -> UnquenchedPoint:
    """Return Delta*(N_f) for the UIDT unquenched screening ansatz."""
    with mp.workdps(80):
        assert delta0_gev > mp.mpf("0"), "Delta*(0) must be positive."
        ratio = beta0_ratio_su3(n_flavors)
        delta = delta0_gev * mp.sqrt(ratio)
        assert delta > mp.mpf("0"), "Screened gap must remain positive in ansatz domain."
        assert delta <= delta0_gev, "Screening ansatz must not increase the pure-gauge anchor."
        return UnquenchedPoint(n_flavors=+n_flavors, beta0_ratio=+ratio, delta_gev=+delta)


def representative_points() -> tuple[UnquenchedPoint, ...]:
    """Return representative N_f = 0, 2, 3 ansatz points."""
    with mp.workdps(80):
        points = tuple(screened_gap(mp.mpf(nf)) for nf in ("0", "2", "3"))
        assert points[0].delta_gev == mp.mpf("1.710"), "N_f=0 must reproduce the anchor."
        assert points[0].delta_gev > points[1].delta_gev > points[2].delta_gev, (
            "Screened gap must decrease monotonically for N_f = 0, 2, 3."
        )
        assert abs(points[1].delta_gev - mp.mpf("1.6030170418194674837411278273038086697555174792815281268884690359677061204104183")) < mp.mpf("1e-70")
        assert abs(points[2].delta_gev - mp.mpf("1.5467531976839273841781459035564202444132694762612167229919126735979605651440359")) < mp.mpf("1e-70")
        return points


def main() -> None:
    with mp.workdps(80):
        points = representative_points()
        print("[UIDT_UNQUENCHED_QCD_ANSATZ_VERIFICATION]")
        for point in points:
            print(
                "N_f = "
                f"{mp.nstr(point.n_flavors, 20)}, "
                "beta0 ratio = "
                f"{mp.nstr(point.beta0_ratio, 50)}, "
                "Delta*(N_f) = "
                f"{mp.nstr(point.delta_gev, 50)} GeV [D]"
            )
        print("[PASS] Unquenched-QCD screening ansatz numerics verified at mp.dps=80.")


if __name__ == "__main__":
    main()
