"""Sanity tests for the check scripts. No physics, just regex behaviour.
Run: python -m pytest verification/tests/test_check_scripts.py -v"""
from __future__ import annotations
import importlib.util, pathlib

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"

def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# check_evidence_tags
def test_evidence_tags_blocks_49_over_3_with_A():
    m = load("check_evidence_tags")
    pat = m.PROMO_PATTERNS[0][0]
    assert pat.search("Color algebra: 49/3 is [A] proven")
    assert pat.search("[A] result for 49/3 confirmed")

def test_evidence_tags_blocks_glueball_B():
    m = load("check_evidence_tags")
    pat = next(p for p, lbl in m.PROMO_PATTERNS if "glueball" in lbl)
    assert pat.search("Glueball resonance at 1.705 GeV [B] lattice-consistent")

def test_evidence_tags_blocks_invented_classes():
    m = load("check_evidence_tags")
    assert m.INVALID_CLASSES.search("evidence [A+]")
    assert m.INVALID_CLASSES.search("status [B+]")
    assert m.INVALID_CLASSES.search("class [C+]")
    assert not m.INVALID_CLASSES.search("evidence [A]")
    assert not m.INVALID_CLASSES.search("evidence [A-]")  # A- is valid

# check_no_gamma_targeting
def test_gamma_targeting_blocks_backsolve():
    m = load("check_no_gamma_targeting")
    assert m.BACKSOLVE.search("K_S = (Delta*/gamma)**2")
    assert m.BACKSOLVE.search("K_S = (Delta/gamma)")
    assert m.BACKSOLVE.search("K_S = (\u0394*/\u03b3)")

def test_gamma_targeting_blocks_target_literals():
    m = load("check_no_gamma_targeting")
    assert m.TARGET_LITERAL.search("target = 16.339")
    assert m.TARGET_LITERAL.search("loss: 49/3")
    assert m.TARGET_LITERAL.search("kill_switch = 17/3000")

# check_protected_paths
def test_protected_paths_secret_file_pattern():
    m = load("check_protected_paths")
    assert m.SECRET_FILES.search(".env")
    assert m.SECRET_FILES.search("src/.env.local")
    assert m.SECRET_FILES.search("path/to/private.key")
    assert m.SECRET_FILES.search("credentials.json")
    assert not m.SECRET_FILES.search("env.py")  # not .env

def test_protected_paths_protected_dirs():
    m = load("check_protected_paths")
    for d in m.PROTECTED_DIRS:
        assert "UIDT-OS/" in m.PROTECTED_DIRS or ".claude/" in m.PROTECTED_DIRS
