#!/usr/bin/env python3
"""Verify the exact RG constraint 5*kappa^2 = 3*lambda_S at 80 dps."""
from __future__ import annotations

import sys

from mpmath import mp


THRESHOLD_TEXT = "1e-14"


def compute_residual():
    """Compute the proof-critical residual in a local 80-dps mpmath scope."""
    with mp.workdps(80):
        kappa = mp.mpf(1) / 2
        lambda_s = mp.mpf(5) / 12
        residual = abs(5 * kappa**2 - 3 * lambda_s)
        return +residual


def main() -> int:
    residual = compute_residual()
    with mp.workdps(80):
        threshold = mp.mpf(THRESHOLD_TEXT)
    print(f"[check_rg_constraint] residual = {mp.nstr(residual, 80)}", file=sys.stderr)
    if not residual < threshold:
        print(
            f"[RG_CONSTRAINT_FAIL] residual {mp.nstr(residual, 80)} >= {mp.nstr(threshold, 80)}",
            file=sys.stderr,
        )
        return 1
    print("[check_rg_constraint] OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
