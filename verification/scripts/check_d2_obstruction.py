#!/usr/bin/env python3
"""Verify F = d(dS) + dS wedge dS = 0 for an exact scalar one-form."""
from __future__ import annotations

import sys
from itertools import combinations

import sympy as sp


def exterior_derivative_of_one_form(one_form, coords):
    """Return two-form coefficients for d(alpha), keyed by coordinate index pairs."""
    coeffs = {}
    for i, j in combinations(range(len(coords)), 2):
        coeffs[(i, j)] = sp.simplify(
            sp.diff(one_form[j], coords[i]) - sp.diff(one_form[i], coords[j])
        )
    return coeffs


def wedge_one_forms(left, right, coords):
    """Return two-form coefficients for alpha wedge beta."""
    coeffs = {}
    for i, j in combinations(range(len(coords)), 2):
        coeffs[(i, j)] = sp.simplify(left[i] * right[j] - left[j] * right[i])
    return coeffs


def curvature_coefficients():
    x, y, z = sp.symbols("x y z")
    coords = (x, y, z)
    scalar = sp.Function("S")(*coords)
    d_scalar = {i: sp.diff(scalar, coord) for i, coord in enumerate(coords)}
    d_d_scalar = exterior_derivative_of_one_form(d_scalar, coords)
    wedge = wedge_one_forms(d_scalar, d_scalar, coords)
    return {key: sp.simplify(d_d_scalar[key] + wedge[key]) for key in d_d_scalar}


def main() -> int:
    curvature = curvature_coefficients()
    nonzero = {basis: coeff for basis, coeff in curvature.items() if coeff != 0}
    if nonzero:
        print("[AUDIT_FAIL] d2 obstruction check found nonzero curvature terms:", file=sys.stderr)
        for basis, coeff in nonzero.items():
            print(f"  dx{basis[0]}^dx{basis[1]}: {coeff}", file=sys.stderr)
        return 1
    print("[check_d2_obstruction] F = d(dS) + dS wedge dS = 0 identically", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
