"""
Blinding Check — Forbidden Pattern Scanner
===========================================
CI-equivalent enforcement of the blinding protocol (Sec. 5.2).
Scans simulation modules and eval/detector.py for forbidden patterns.
eval/scoring.py is exempt ONLY for the public symmetric set P.

Usage:
    python -m verification.prereg.PR-B1.blinding_check

Exit code 0 = clean; exit code 1 = violation found (blocks production).
"""

from __future__ import annotations

import pathlib
import re
import sys

from .config import FORBIDDEN_PATTERNS


def _scan_file(filepath: pathlib.Path, patterns: tuple[str, ...]) -> list[str]:
    """Scan a single file for forbidden patterns.

    Returns list of violation descriptions.
    """
    violations: list[str] = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        violations.append(f"  CANNOT READ: {filepath} ({exc})")
        return violations

    for line_no, line in enumerate(content.splitlines(), start=1):
        # Skip comments that document the ban itself
        stripped = line.strip()
        if stripped.startswith("#") and ("forbidden" in stripped.lower()
                                         or "banned" in stripped.lower()
                                         or "blinding" in stripped.lower()):
            continue

        for pattern in patterns:
            if pattern in line:
                violations.append(
                    f"  VIOLATION: '{pattern}' found in "
                    f"{filepath.name}:{line_no}: {stripped[:120]}"
                )
    return violations


def check_blinding(base_dir: pathlib.Path | None = None) -> tuple[bool, list[str]]:
    """Run the full blinding check.

    Parameters
    ----------
    base_dir : Path, optional
        Root of the PR-B1 package.  Defaults to this file's parent.

    Returns
    -------
    (passed, violations) : (bool, list[str])
    """
    if base_dir is None:
        base_dir = pathlib.Path(__file__).resolve().parent

    sim_dir = base_dir / "sim"
    eval_dir = base_dir / "eval"

    all_violations: list[str] = []

    # 1. Scan ALL .py files in sim/ — full pattern set
    print("[BLINDING] Scanning sim/ for forbidden patterns...")
    if sim_dir.is_dir():
        for py_file in sorted(sim_dir.glob("*.py")):
            violations = _scan_file(py_file, FORBIDDEN_PATTERNS)
            all_violations.extend(violations)
    else:
        all_violations.append(f"  WARNING: sim/ directory not found at {sim_dir}")

    # 2. Scan eval/detector.py — full pattern set
    detector_file = eval_dir / "detector.py"
    print("[BLINDING] Scanning eval/detector.py for forbidden patterns...")
    if detector_file.is_file():
        violations = _scan_file(detector_file, FORBIDDEN_PATTERNS)
        all_violations.extend(violations)
    else:
        all_violations.append(
            f"  WARNING: eval/detector.py not found at {detector_file}"
        )

    # 3. eval/scoring.py is EXEMPT for the public symmetric set P.
    #    But we still check for the non-P forbidden patterns:
    scoring_file = eval_dir / "scoring.py"
    print("[BLINDING] Scanning eval/scoring.py (restricted check)...")
    # In scoring.py, only the P-unrelated patterns are forbidden.
    # The scoring module MUST reference the candidate set P, which includes
    # class labels. We exclude the P-related patterns from the scan.
    scoring_exempt = {"(1,2,3)", "[1,2,3]", "1:2:3"}
    scoring_patterns = tuple(p for p in FORBIDDEN_PATTERNS if p not in scoring_exempt)
    if scoring_file.is_file():
        violations = _scan_file(scoring_file, scoring_patterns)
        all_violations.extend(violations)

    # 4. Report
    if all_violations:
        print("\n[BLINDING] *** VIOLATIONS DETECTED ***")
        for v in all_violations:
            print(v)
        print(f"\n[BLINDING] Total violations: {len(all_violations)}")
        print("[BLINDING] PRODUCTION IS BLOCKED.")
        return False, all_violations
    else:
        print("[BLINDING] All checks passed. No forbidden patterns found.")
        return True, []


def main() -> None:
    """Entry point for blinding check."""
    passed, _ = check_blinding()
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
