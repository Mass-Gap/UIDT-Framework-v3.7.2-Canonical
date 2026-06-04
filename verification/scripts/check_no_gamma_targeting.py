#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #2: block K_S backsolved from gamma, and forbidden target literals.
Deterministic regex. Scans both Python and YAML/JSON in the diff."""
from __future__ import annotations
from os import getenv
import subprocess, sys, re
from pathlib import Path

# Patterns that constitute circular construction
BACKSOLVE = re.compile(
    r"K[_ ]?S\s*=\s*\(\s*(?:Delta|\u0394|D)\s*\*?\s*/\s*(?:gamma|\u03b3|16\.339)\s*\)",
    re.IGNORECASE,
)
TARGET_LITERAL = re.compile(
    r"(?:target|loss|objective|goal|kill[_\-\s]?switch)[^\n]*"
    r"(?:16\.339|49\s*/\s*3|17\s*/\s*3000)",
    re.IGNORECASE,
)

SCAN_EXT = {".py", ".yaml", ".yml", ".json", ".toml", ".ini"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "historical_heuristics"}
ALLOWLIST_FILES = {
    # Files that are *about* the forbidden patterns and may legitimately contain them
    "historical_heuristics.md",
    "AI_AUDIT_POLICY.md",
    "verification/scripts/check_no_gamma_targeting.py",
    "verification/scripts/check_evidence_tags.py",
    "verification/tests/test_check_scripts.py",
    "scripts/epistemic_gatekeeper.py",
}

def changed_files() -> list[str]:
    base = getenv("GITHUB_BASE_REF")
    ref = f"origin/{base}" if base else "origin/main"
    try:
        out = subprocess.check_output(
            ["git","diff","--name-only","--diff-filter=AM",f"{ref}...HEAD"],
            text=True, encoding="utf-8", errors="replace",
        )
    except subprocess.CalledProcessError:
        out = subprocess.check_output(
            ["git","diff","--cached","--name-only","--diff-filter=AM"],
            text=True, encoding="utf-8", errors="replace",
        )
    return [l.strip() for l in out.splitlines() if l.strip()]

def main() -> int:
    violations: list[str] = []
    for path in changed_files():
        p = Path(path)
        if not any(p.suffix == e for e in SCAN_EXT):
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if path in ALLOWLIST_FILES:
            continue
        if not p.exists():
            continue  # deleted file
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if BACKSOLVE.search(line):
                violations.append(f"  {path}:{i}  K_S backsolved from gamma -- {line.strip()[:140]}")
            if TARGET_LITERAL.search(line):
                violations.append(f"  {path}:{i}  forbidden target literal -- {line.strip()[:140]}")
    if violations:
        print("BLOCKED: gamma-targeting violation (AI_AUDIT_POLICY §7 #2)", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        print("\nIf this is in a historical-record or audit context, add the file to ALLOWLIST_FILES.", file=sys.stderr)
        return 1
    print("[check_no_gamma_targeting] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
