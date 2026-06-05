"""Sanity tests for the gatekeeper check scripts. No physics, just regex behaviour.
Run locally: python -m pytest verification/tests/test_check_scripts.py -v"""
from __future__ import annotations
import sys, importlib.util
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"

def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_evidence_tags_blocks_49_over_3_with_A():
    mod = load("check_evidence_tags")
    lines = ["Color algebra: 49/3", "note", "[A] proven"]
    assert mod.PROMO_PATTERNS[0][0].search(lines[0])
    assert mod.window_has(mod.PROMOTED_TAG, lines, 0)
    assert mod.PROMOTED_TAG.search(r"\catmark{A-}")

def test_evidence_tags_blocks_glueball_B():
    mod = load("check_evidence_tags")
    pat = next(p for p, lbl in mod.PROMO_PATTERNS if "glueball" in lbl)
    lines = ["Glueball resonance at 1.705 GeV", "candidate [B]"]
    assert pat.search(lines[0])
    assert mod.window_has(mod.PROMOTED_TAG, lines, 0)

def test_evidence_tags_blocks_invented_classes():
    mod = load("check_evidence_tags")
    assert mod.INVALID_CLASSES.search("evidence [A+]")
    assert mod.INVALID_CLASSES.search("status [B-]")
    assert not mod.INVALID_CLASSES.search("evidence [A]")
    assert not mod.INVALID_CLASSES.search("evidence [A-]")  # A- is valid in UIDT system

def test_no_gamma_targeting_blocks_backsolve():
    mod = load("check_no_gamma_targeting")
    assert mod.BACKSOLVE.search("K_S = (Delta*/gamma)**2")
    assert mod.BACKSOLVE.search("K_S = (Delta/gamma)")
    assert mod.BACKSOLVE.search("K_S = (\u0394*/\u03b3)")

def test_no_gamma_targeting_blocks_target_literals():
    mod = load("check_no_gamma_targeting")
    assert mod.TARGET_LITERAL.search("target = 16.339")
    assert mod.TARGET_LITERAL.search("loss: 49/3")
    assert mod.TARGET_LITERAL.search("kill_switch = 17/3000")
    assert mod.TARGET_LITERAL.search("kill-switch on |gamma - 16.339|")

def test_rg_constraint_residual_is_zero():
    mod = load("check_rg_constraint")
    assert mod.compute_residual() == 0

def test_d2_obstruction_curvature_coefficients_vanish():
    mod = load("check_d2_obstruction")
    assert all(coeff == 0 for coeff in mod.curvature_coefficients().values())

def test_lambda_s_anchor_is_exact_rounding():
    mod = load("check_lambda_s_exact")
    assert mod.LAMBDA_S == mod.Fraction(5, 12)
    assert abs(mod.REGRESSION_ANCHOR - mod.LAMBDA_S) < mod.ROUNDING_TOLERANCE

def test_cosmology_cap_blocks_above_c_tags():
    mod = load("check_cosmology_cap")
    lines = ["H_0 calibrated input", "[B] claimed closure"]
    assert mod.COSMOLOGICAL_PARAMETER.search(lines[0])
    assert mod.window_has(mod.ABOVE_C_TAG, lines, 0)
