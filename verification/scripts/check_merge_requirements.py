#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #3: PRs touching CANONICAL/, LEDGER/CLAIMS.json, core/, modules/,
or manuscript/ must include a Claims Table, a Reproduction Note, and a DOI Check."""
from __future__ import annotations
import os, subprocess, sys

TRIGGER_PATHS = ("CANONICAL/", "LEDGER/CLAIMS.json", "core/", "modules/", "manuscript/")
REQUIRED_HEADINGS = ("## Claims Table", "## Reproduction Note", "## DOI Check")

def changed_files() -> list[str]:
    base = os.environ.get("GITHUB_BASE_REF")
    ref = f"origin/{base}" if base else "origin/main"
    try:
        out = subprocess.check_output(
            ["git","diff","--name-only","--diff-filter=AMD",f"{ref}...HEAD"],
            text=True, encoding="utf-8", errors="replace",
        )
    except subprocess.CalledProcessError:
        return []
    return [l.strip() for l in out.splitlines() if l.strip()]

def main() -> int:
    triggered = [p for p in changed_files() if any(p.startswith(t) for t in TRIGGER_PATHS)]
    if not triggered:
        print("[check_merge_requirements] no trigger paths touched -- OK", file=sys.stderr)
        return 0
    pr_body = os.environ.get("PR_BODY", "")
    if not pr_body:
        print("BLOCKED: PR body unavailable; cannot verify required headings.", file=sys.stderr)
        print("  Triggered paths:", triggered, file=sys.stderr)
        print("  Pass PR_BODY env var in the workflow step.", file=sys.stderr)
        return 1
    missing = [h for h in REQUIRED_HEADINGS if h not in pr_body]
    if missing:
        print("BLOCKED: PR body missing required headings (AI_AUDIT_POLICY §7 #3)", file=sys.stderr)
        for h in missing:
            print(f"  Missing: {h}", file=sys.stderr)
        for p in triggered:
            print(f"  Touched: {p}", file=sys.stderr)
        return 1
    print("[check_merge_requirements] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
