"""Verification test suite for modules/torsion_eos_coupling_v3_9_corrected.py

Tests the Patch v3.9.1 torsion-EOS coupling module against the UIDT v3.9
ledger-canonical constants and stratum firewall requirements.

Evidence tags:
    [A]  Delta = 1.710 GeV  -- Yang-Mills spectral gap, NOT particle mass
    [A-] gamma_inf = 16.3437  -- thermodynamic limit
    [C]  E_T = 2.44 MeV      -- torsion basis energy
    [C]  w_0 = -0.99          -- DESI-calibrated dark-energy EOS
    [D]  w_BRST = -8.12       -- Stratum III local model input only

Filesystem law: tests MUST reside in verification/tests/ (never in repo root).
Precision law:  mp.dps = 80 declared LOCALLY; no global override; no mocking.
"""

import subprocess
import sys

# Ensure mpmath is available; install if absent (CI-safe, no mocking fallback)
try:
    import mpmath as mp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mpmath"])
    import mpmath as mp

import sys
import os

# ---------------------------------------------------------------------------
# Path resolution: allow running from repo root or from verification/tests/
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from modules.torsion_eos_coupling_v3_9_corrected import compute_calibrated_torsion_eos  # noqa: E402


# ---------------------------------------------------------------------------
# Shared precision block
# ---------------------------------------------------------------------------
def _dps() -> int:
    mp.dps = 80
    return 80


DPS = _dps()


# ---------------------------------------------------------------------------
# Ledger-canonical reference values (read-only; never altered by tests)
# ---------------------------------------------------------------------------
GAMMA_REF    = mp.mpf("16.339")       # [A-]
DELTA_GAMMA  = mp.mpf("0.0047")       # [A-]
GAMMA_INF    = GAMMA_REF + DELTA_GAMMA  # = 16.3437 [A-]
ET_GEV       = mp.mpf("0.00244")      # [C]  2.44 MeV
W0_LEDGER    = mp.mpf("-0.99")        # [C]
DELTA_STAR   = mp.mpf("1.710")        # [A]
W_BRST       = mp.mpf("-8.12")        # [D]  Stratum III only
TOLERANCE    = mp.mpf("0.05")

# Residual threshold for [A]-class assertions
RESIDUAL_THRESHOLD = mp.mpf("1e-14")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def _call(topological_shift_str: str = "-7.52743042387e-121",
          steps_str: str = "99.0",
          tolerance_str: str = "0.05") -> dict:
    """Invoke module with mpf-constructed shift to avoid binary-float artefacts."""
    _dps()
    shift = mp.mpf(topological_shift_str)
    return compute_calibrated_torsion_eos(shift, steps_str, tolerance_str)


# ===========================================================================
# Test 1 — Canonical constant propagation
# ===========================================================================
def test_gamma_inf_construction():
    """gamma_inf returned by the module must equal gamma_ref + delta_gamma [A-]."""
    _dps()
    result = _call()
    residual = mp.fabs(result["gamma_inf_used"] - GAMMA_INF)
    assert residual < RESIDUAL_THRESHOLD, (
        f"[FAIL] gamma_inf residual {mp.nstr(residual, 10)} >= 1e-14"
    )
    print(f"PASS test_gamma_inf_construction | residual = {mp.nstr(residual, 20)}")


# ===========================================================================
# Test 2 — ET ledger anchor
# ===========================================================================
def test_et_ledger_anchor():
    """E_T returned must equal the ledger value 0.00244 GeV [C]."""
    _dps()
    result = _call()
    residual = mp.fabs(result["ET_ledger_GeV"] - ET_GEV)
    assert residual < RESIDUAL_THRESHOLD, (
        f"[FAIL] E_T residual {mp.nstr(residual, 10)} >= 1e-14"
    )
    print(f"PASS test_et_ledger_anchor | residual = {mp.nstr(residual, 20)}")


# ===========================================================================
# Test 3 — DESI kill-switch inactive for near-zero topological shift
# ===========================================================================
def test_desi_killswitch_inactive_for_small_shift():
    """A near-zero topological shift must not trigger the DESI kill-switch [C]."""
    result = _call(topological_shift_str="-7.52743042387e-121")
    assert result["desi_kill_switch_triggered"] is False, (
        "[FAIL] kill-switch triggered for negligible topological shift"
    )
    print("PASS test_desi_killswitch_inactive_for_small_shift")


# ===========================================================================
# Test 4 — DESI kill-switch activates when deviation > tolerance
# ===========================================================================
def test_desi_killswitch_active_for_large_shift():
    """A large artificial shift must trigger the DESI kill-switch [C]."""
    _dps()
    # shift large enough so |w_0_macro - w_0_ledger| > 0.05
    large_shift = mp.mpf("1.0")
    result = compute_calibrated_torsion_eos(large_shift)
    assert result["desi_kill_switch_triggered"] is True, (
        "[FAIL] kill-switch did not trigger for large topological shift"
    )
    print("PASS test_desi_killswitch_active_for_large_shift")


# ===========================================================================
# Test 5 — Evidence tag ceiling: must contain '[C]'
# ===========================================================================
def test_evidence_tag_ceiling():
    """Evidence tag must remain at [C] ceiling; no [A], [B], or higher inflation."""
    result = _call()
    tag = result["evidence_tag"]
    assert "[C]" in tag, f"[FAIL] evidence_tag does not contain '[C]': {tag}"
    assert "[A]" not in tag, f"[FAIL] evidence_tag illegally contains '[A]': {tag}"
    assert "[B]" not in tag, f"[FAIL] evidence_tag illegally contains '[B]': {tag}"
    print(f"PASS test_evidence_tag_ceiling | tag = {tag!r}")


# ===========================================================================
# Test 6 — Zero topological shift yields w_0_macro == w_0_ledger
# ===========================================================================
def test_zero_shift_baseline():
    """Zero topological shift: w_0_macroscopic must equal w_0_ledger [C].

    With shift=0, modulation_amplitude=0, torsion_energy_modulated = ET_ledger.
    The BRST correction omega_n * (ET/Delta) is negligible but non-zero;
    therefore we verify |w_0_macro - w_0_ledger| < tolerance rather than
    exact equality, consistent with the DESI kill-switch definition.
    """
    _dps()
    result = compute_calibrated_torsion_eos(mp.mpf("0.0"))
    deviation = mp.fabs(result["w_0_macroscopic"] - W0_LEDGER)
    assert deviation < TOLERANCE, (
        f"[FAIL] zero-shift deviation {mp.nstr(deviation, 10)} >= tolerance {TOLERANCE}"
    )
    assert result["desi_kill_switch_triggered"] is False, (
        "[FAIL] kill-switch triggered for zero topological shift"
    )
    print(f"PASS test_zero_shift_baseline | deviation = {mp.nstr(deviation, 20)}")


# ===========================================================================
# Test 7 — w_BRST isolation: Stratum III value must not equal w_0_macro [D]
# ===========================================================================
def test_w_brst_stratum_isolation():
    """w_BRST must not equal w_0_macroscopic: stratum firewall is active [D]."""
    _dps()
    result = _call()
    residual = mp.fabs(result["w_BRST_stratum_III"] - result["w_0_macroscopic"])
    assert residual > mp.mpf("1.0"), (
        f"[FAIL] w_BRST == w_0_macro within 1.0: stratum firewall may be breached. "
        f"residual = {mp.nstr(residual, 10)}"
    )
    print(f"PASS test_w_brst_stratum_isolation | |w_BRST - w_0_macro| = {mp.nstr(residual, 20)}")


# ===========================================================================
# Runner
# ===========================================================================
if __name__ == "__main__":
    tests = [
        test_gamma_inf_construction,
        test_et_ledger_anchor,
        test_desi_killswitch_inactive_for_small_shift,
        test_desi_killswitch_active_for_large_shift,
        test_evidence_tag_ceiling,
        test_zero_shift_baseline,
        test_w_brst_stratum_isolation,
    ]
    failures = []
    for t in tests:
        try:
            t()
        except AssertionError as exc:
            failures.append((t.__name__, str(exc)))
            print(f"FAIL {t.__name__}: {exc}")

    print(f"\n{'=' * 60}")
    if failures:
        print(f"FAILED {len(failures)}/{len(tests)} tests")
        for name, msg in failures:
            print(f"  - {name}: {msg}")
        sys.exit(1)
    else:
        print(f"ALL {len(tests)} TESTS PASSED")
        sys.exit(0)
