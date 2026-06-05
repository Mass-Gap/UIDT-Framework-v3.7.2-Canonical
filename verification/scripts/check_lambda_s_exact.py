#!/usr/bin/env python3
"""Verify lambda_S = 5/12 exactly and the rounded 0.417 regression anchor."""
from __future__ import annotations

import sys
from fractions import Fraction


LAMBDA_S = Fraction(5, 12)
REGRESSION_ANCHOR = Fraction(417, 1000)
ROUNDING_TOLERANCE = Fraction(1, 2000)


def main() -> int:
    if LAMBDA_S != Fraction(5, 12):
        print("[AUDIT_FAIL] lambda_S is not exactly 5/12", file=sys.stderr)
        return 1

    residual = abs(REGRESSION_ANCHOR - LAMBDA_S)
    print(f"[check_lambda_s_exact] lambda_S = {LAMBDA_S}", file=sys.stderr)
    print(f"[check_lambda_s_exact] anchor residual = {residual}", file=sys.stderr)
    if not residual < ROUNDING_TOLERANCE:
        print(
            "[AUDIT_FAIL] 0.417 regression anchor is outside the exact rounding tolerance",
            file=sys.stderr,
        )
        return 1

    print("[check_lambda_s_exact] OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
