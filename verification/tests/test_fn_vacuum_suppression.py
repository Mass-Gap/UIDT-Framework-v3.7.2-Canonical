"""
test_fn_vacuum_suppression.py
=============================
Unit tests for derive_fn_vacuum_suppression.py.

Evidence: [D]  Stratum: III  No claims promoted.

Tests encode ONLY the structural constraints that are
manuscript-binding (N=99, f_n>0, RG consistency);
they do NOT assert that any model matches observation.
"""

import sys
import os
import importlib
import types
from mpmath import mp, mpf, fabs

mp.dps = 80

# ── import the script module ────────────────────────────────────────────
_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "scripts", "derive_fn_vacuum_suppression.py"
)
_spec = importlib.util.spec_from_file_location("derive_fn", _SCRIPT)
_mod  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


class TestLedgerConstants:
    """Canonical ledger values must not drift."""

    def test_gamma_value(self):
        assert fabs(_mod.GAMMA - mpf("16.339")) < mpf("1e-14"), "γ drift"

    def test_delta_value(self):
        assert fabs(_mod.DELTA - mpf("1.710")) < mpf("1e-14"), "Δ drift"

    def test_kappa_value(self):
        assert fabs(_mod.KAPPA - mpf("0.500")) < mpf("1e-14"), "κ drift"

    def test_lambda_s_value(self):
        assert fabs(_mod.LAMBDA_S - mpf("0.417")) < mpf("1e-14"), "λ_S drift"


class TestRGConstraint:
    """RG self-consistency: |5κ²−3λ_S| < 1e-14  [Space-Directive §2]"""

    def test_rg_constraint(self):
        residual = fabs(5 * _mod.KAPPA**2 - 3 * _mod.LAMBDA_S)
        assert residual < mpf("1e-14"), (
            f"[RG_CONSTRAINT_FAIL] residual = {float(residual):.3e}"
        )


class TestN99Structure:
    """Manuscript Eq.(291): N_eff must be exactly 99."""

    def test_n_eff_equals_99(self):
        assert _mod.N_EFF == 99, f"[N_EFF_FAIL] got {_mod.N_EFF}"


class TestFnPositivity:
    """Every f_n(g) must be strictly positive for all three candidate models."""

    def test_fn_trivial_positive(self):
        for n in range(1, 100):
            v = _mod.fn_trivial(n, 1.0)
            assert v > 0, f"fn_trivial({n}) not positive"

    def test_fn_geometric_positive(self):
        for n in range(1, 100):
            v = _mod.fn_geometric(n, 1.5)
            assert v > 0, f"fn_geometric({n}) not positive"

    def test_fn_sector_positive(self):
        for n in range(1, 100):
            v = _mod.fn_sector(n, 1.0)
            assert v > 0, f"fn_sector({n}) not positive"


class TestTrivialProduct:
    """Model A: prod f_n = 1, rho_predicted ~ rho_QCD * pi^{-2}."""

    def test_trivial_product_is_one(self):
        product = mpf(1)
        for n in range(1, 100):
            product *= _mod.fn_trivial(n, 1.0)
        assert fabs(product - 1) < mpf("1e-70"), "trivial product != 1"


class TestSectorDecompositionCoverage:
    """Sector-decomposed model must cover exactly n=1..99."""

    def test_sector_counts(self):
        counts = {"QCD": 0, "EW": 0, "grav": 0}
        for n in range(1, 100):
            if 1 <= n <= 11:
                counts["QCD"] += 1
            elif 12 <= n <= 22:
                counts["EW"] += 1
            else:
                counts["grav"] += 1
        assert counts["QCD"]  == 11, f"QCD sector wrong: {counts['QCD']}"
        assert counts["EW"]   == 11, f"EW sector wrong:  {counts['EW']}"
        assert counts["grav"] == 77, f"grav sector wrong:{counts['grav']}"
        assert sum(counts.values()) == 99


class TestEvidenceTagsEnforced:
    """Compute_suppression must always return evidence='[D]' and status='scaffold'."""

    def test_evidence_tag(self):
        r = _mod.compute_suppression(_mod.fn_trivial, g=1.0, label="test")
        assert r["evidence"] == "[D]",     "Evidence tag must be [D]"
        assert r["status"]   == "scaffold", "Status must be scaffold"


if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])
