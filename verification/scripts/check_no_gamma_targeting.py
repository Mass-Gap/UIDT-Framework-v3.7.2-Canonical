#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #2: block K_S backsolved from gamma, and forbidden target literals.
Implements the Target-Leakage Theorem of UIDT_Ontology_v3_9_9.tex (Proposition target-leakage)."""
from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path

BACKSOLVE = re.compile(
    r"K[_ ]?S\s*=\s*\(\s*(?:Delta|\u0394|D)\s*\*?\s*/\s*(?:gamma|\u03b3|16\.339)\s*\)",
    re.IGNORECASE,
)
TARGET_LITERAL = re.compile(
    r"(?:target|loss|objective|goal|kill[_\-\s]?switch)\s*[=:]\s*[\"']?\s*"
    r"(?:16\.339|49\s*/\s*3|17\s*/\s*3000)",
    re.IGNORECASE,
)

SCAN_EXT = {".py", ".yaml", ".yml", ".json", ".toml", ".ini"}
SKIP_DIRS = {".git","node_modules",".venv","__pycache__","historical_heuristics"}
ALLOWLIST = {
    "historical_heuristics.md",
    "AI_AUDIT_POLICY.md",
    "MERGE_PROTOCOL.md",
    "CANONICAL/ONTOLOGY_LINK.md",
    "verification/scripts/check_no_gamma_targeting.py",
    "verification/scripts/check_evidence_tags.py",
    "verification/scripts/check_ontology_consistency.py",
    "verification/tests/test_check_scripts.py",
    "scripts/epistemic_gatekeeper.py",
    ".antigravity/Plan_v-wave0-1___Repository_Honesty_Pass.md",
    ".antigravity/Plan_v-wave0-2___Ledger_Hygiene.md",
    ".antigravity/Plan_v-wave0-3___Gatekeeper_CI_Hardening.md",
    ".antigravity/Plan_v-wave0-4___Ontology_as_CoVe.md",
}

def changed_files() -> list[str]:
    base = os.environ.get("GITHUB_BASE_REF")
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
        if p.suffix not in SCAN_EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if path in ALLOWLIST:
            continue
        if not p.exists():
            continue
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
        print("BLOCKED: gamma-targeting violation (Target-Leakage Theorem)", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        print("\nSee UIDT_Ontology_v3_9_9.tex Proposition target-leakage.", file=sys.stderr)
        return 1
    print("[check_no_gamma_targeting] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
