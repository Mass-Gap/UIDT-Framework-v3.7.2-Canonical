#!/usr/bin/env python3
"""Block evidence-class inflation near known calibrated or heuristic literals."""
from __future__ import annotations
from os import getenv
import subprocess, sys, re
from pathlib import Path

INVALID_CLASSES = re.compile(r"\[(A\+|B\+|B\-|C\+|D\+)\]")
PROMOTED_TAG = re.compile(r"(\[(?:A-|A|B)\]|\\catmark\{(?:A-|A|B)\})")
PROMO_PATTERNS = (
    (re.compile(r"49\s*/\s*3"), "49/3"),
    (re.compile(r"16\.339"), "16.339"),
    (re.compile(r"17\s*/\s*3000"), "17/3000"),
    (re.compile(r"glueball", re.I), "glueball"),
)

SCAN_EXT = {".md", ".py", ".json", ".yaml", ".yml", ".tex", ".cff"}
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
ALLOWLIST_FILES = {
    "historical_heuristics.md",
    "AI_AUDIT_POLICY.md",
    "verification/scripts/check_evidence_tags.py",
    "scripts/epistemic_gatekeeper.py",
    ".antigravity/Plan_v-wave0-1___Repository_Honesty_Pass.md",
    ".antigravity/Plan_v-wave0-2___Ledger_Hygiene.md",
    ".antigravity/Plan_v-wave0-3___Gatekeeper_CI_Hardening.md",
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

def window_has(pattern: re.Pattern[str], lines: list[str], index: int, radius: int = 3) -> bool:
    start = max(0, index - radius)
    stop = min(len(lines), index + radius + 1)
    return any(pattern.search(lines[pos]) for pos in range(start, stop))

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
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            m = INVALID_CLASSES.search(line)
            if m:
                violations.append(f"  {path}:{i}  invented evidence class {m.group(0)} -- {line.strip()[:140]}")
        for i, line in enumerate(lines):
            for pattern, label in PROMO_PATTERNS:
                if pattern.search(line) and window_has(PROMOTED_TAG, lines, i):
                    violations.append(f"  {path}:{i + 1}  forbidden promoted evidence near {label} -- {line.strip()[:140]}")
                    break
    if violations:
        print("BLOCKED: evidence-tag violation", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("[check_evidence_tags] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
