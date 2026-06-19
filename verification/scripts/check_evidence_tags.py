#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #1: block invented evidence classes and forbidden [A]/[B] promotions.
Source of truth for valid classes: UIDT_Ontology_v3_9_9.tex (subsec:evidence-grammar).
Allowed: [A], [A-], [B], [C], [D], [E]. Plus optional 'pending' marker for [B pending]."""
from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path

# Invented classes that contradict the manuscript's grammar
INVALID_CLASSES = re.compile(r"\[(A\+|B\+|B-(?!\])|C\+|D\+|E\+|F)\]")
# Note: [A-] is valid; [B-] alone is not (the manuscript uses 'B pending' instead).

# [A] or [B] within 80 chars (~3 lines) of forbidden numerology constants
PROMO_PATTERNS = (
    (re.compile(r"49\s*/\s*3.{0,80}\[[AB]\]|\[[AB]\].{0,80}49\s*/\s*3"), "49/3 + [A]/[B]"),
    (re.compile(r"16\.339.{0,80}\[[AB]\]|\[[AB]\].{0,80}16\.339"), "16.339 + [A]/[B]"),
    (re.compile(r"17\s*/\s*3000.{0,80}\[[AB]\]|\[[AB]\].{0,80}17\s*/\s*3000"), "17/3000 + [A]/[B]"),
    (re.compile(r"glueball.{0,80}\[B\]", re.I), "glueball + [B] (L12 violation)"),
)

SCAN_EXT = {".md", ".py", ".json", ".yaml", ".yml", ".tex", ".cff"}
SKIP_DIRS = {".git","node_modules",".venv","__pycache__"}
ALLOWLIST = {
    "historical_heuristics.md",
    "AI_AUDIT_POLICY.md",
    "MERGE_PROTOCOL.md",
    "CANONICAL/ONTOLOGY_LINK.md",
    "manuscript/UIDT_Ontology_v3_9_9.tex",
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
            m = INVALID_CLASSES.search(line)
            if m:
                violations.append(f"  {path}:{i}  invented class {m.group(0)} -- {line.strip()[:140]}")
            for pat, label in PROMO_PATTERNS:
                if pat.search(line):
                    violations.append(f"  {path}:{i}  forbidden combo ({label}) -- {line.strip()[:140]}")
                    break
    if violations:
        print("BLOCKED: evidence-tag violation (UIDT_Ontology_v3_9_9 evidence grammar)", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("[check_evidence_tags] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
