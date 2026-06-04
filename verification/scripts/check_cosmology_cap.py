#!/usr/bin/env python3
"""Block cosmological parameters that are tagged above evidence class C."""
from __future__ import annotations

from os import getenv
import re
import subprocess
import sys
from pathlib import Path


SCAN_EXT = {".md", ".py", ".json", ".yaml", ".yml", ".tex", ".cff"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
ALLOWLIST_FILES = {
    "AI_AUDIT_POLICY.md",
    "verification/scripts/check_cosmology_cap.py",
}

COSMOLOGICAL_PARAMETER = re.compile(
    r"("
    r"\bH_?0\b|"
    r"\bS_?8\b|"
    r"\bw_?(?:0|a)\b|"
    r"(?:lambda|\\lambda)[_\-{]*UIDT|"
    r"(?:rho|\\rho)[_\-{]*vac|"
    r"\bE_?T\b|\\ETorsion|"
    r"Hubble|dark[- ]energy|cosmological constant"
    r")",
    re.IGNORECASE,
)
ABOVE_C_TAG = re.compile(
    r"(\[(?:A-|A|B(?:\s+pending)?)\]|\\catmark\{(?:A-|A|B(?:\\,?pending| pending)?)\})"
)


def changed_files() -> list[str]:
    base = getenv("GITHUB_BASE_REF")
    ref = f"origin/{base}" if base else "origin/main"
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", f"{ref}...HEAD"],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    return [line.strip() for line in out.splitlines() if line.strip()]


def window_has(pattern: re.Pattern[str], lines: list[str], index: int, radius: int = 3) -> bool:
    start = max(0, index - radius)
    stop = min(len(lines), index + radius + 1)
    return any(pattern.search(lines[pos]) for pos in range(start, stop))


def main() -> int:
    violations: list[str] = []
    for path in changed_files():
        p = Path(path)
        if p.suffix not in SCAN_EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if path in ALLOWLIST_FILES:
            continue
        if not p.exists():
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines):
            if COSMOLOGICAL_PARAMETER.search(line) and window_has(ABOVE_C_TAG, lines, i):
                violations.append(f"  {path}:{i + 1}  cosmological parameter tagged above [C] -- {line.strip()[:140]}")

    if violations:
        print("BLOCKED: cosmology evidence-cap violation", file=sys.stderr)
        for violation in violations:
            print(violation, file=sys.stderr)
        return 1

    print("[check_cosmology_cap] OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
