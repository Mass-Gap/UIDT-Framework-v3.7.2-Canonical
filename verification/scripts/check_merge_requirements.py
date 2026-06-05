#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #3: PRs touching CANONICAL/, LEDGER/CLAIMS.json, core/, modules/,
or manuscript/ must include a Claims Table, a Reproduction Note, and a DOI check.
Operates on PR description (via gh CLI if available) and on file presence."""
from __future__ import annotations
from os import getenv
import subprocess, sys, re
from pathlib import Path

TRIGGER_PATHS = ("CANONICAL/", "LEDGER/CLAIMS.json", "core/", "modules/", "manuscript/")
REQUIRED_HEADINGS = ("## Claims Table", "## Reproduction Note", "## DOI Check")

def changed_files() -> list[str]:
    base = getenv("GITHUB_BASE_REF")
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
        print("[check_merge_requirements] no trigger paths touched — OK", file=sys.stderr)
        return 0
    pr_body = getenv("PR_BODY", "")
    # When run in GitHub Actions on a PR, PR_BODY can be passed via the workflow.
    missing = [h for h in REQUIRED_HEADINGS if h not in pr_body]
    if not pr_body:
        print("BLOCKED: PR body unavailable to check_merge_requirements.", file=sys.stderr)
        print("  Triggered paths:", triggered, file=sys.stderr)
        print("  Required headings in PR body:", REQUIRED_HEADINGS, file=sys.stderr)
        print("  Pass PR_BODY env var in the workflow step.", file=sys.stderr)
        return 1
    if missing:
        print("BLOCKED: PR is missing required headings (AI_AUDIT_POLICY §7 #3)", file=sys.stderr)
        for h in missing:
            print(f"  Missing: {h}", file=sys.stderr)
        for p in triggered:
            print(f"  Touched: {p}", file=sys.stderr)
        return 1
    print("[check_merge_requirements] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
