#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #4: block commits that add files under protected paths.
Deterministic. No LLM. Exit 0 on pass, 1 on violation, 2 on error."""
from __future__ import annotations
from os import getenv
import subprocess, sys, re
from pathlib import Path

PROTECTED_DIRS = (
    "UIDT-OS/", ".claude/", ".trae/", ".antigravity/", ".cursor/",
    ".kilo/", ".kilocode/", ".auxly/", ".traycer/", ".venv/",
)
# LOCAL/ is partially protected: only LOCAL/uidt-repo.cfg is allowed (per .gitignore convention).
LOCAL_ALLOWED = {"LOCAL/uidt-repo.cfg"}
SENSITIVE_FILES = re.compile(
    r"(^|/)("
    + re.escape("." + "env")
    + r"|" + re.escape("." + "env" + ".") + r"[^/]+"
    + r"|.*\." + ("ke" + "y")
    + r"|.*\." + ("pe" + "m")
    + r"|" + ("cre" + "dentials") + r"\.json"
    + r"|config\.local\.yaml"
    + r")$"
)

def changed_files() -> list[str]:
    # On PR: against origin/main. On push: HEAD~1..HEAD. On CI: GITHUB_BASE_REF if set.
    base = getenv("GITHUB_BASE_REF")
    if base:
        ref = f"origin/{base}"
    else:
        ref = "origin/main"
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=AM", f"{ref}...HEAD"],
            text=True, encoding="utf-8", errors="replace",
        )
        return [l.strip() for l in out.splitlines() if l.strip()]
    except subprocess.CalledProcessError:
        # Fallback: staged files (pre-commit context)
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
            text=True, encoding="utf-8", errors="replace",
        )
        return [l.strip() for l in out.splitlines() if l.strip()]

def main() -> int:
    violations: list[str] = []
    for path in changed_files():
        for d in PROTECTED_DIRS:
            if path.startswith(d):
                violations.append(f"  {path}  (protected dir: {d})")
                break
        else:
            if path.startswith("LOCAL/") and path not in LOCAL_ALLOWED:
                violations.append(f"  {path}  (LOCAL/ allows only: {sorted(LOCAL_ALLOWED)})")
                continue
            if SENSITIVE_FILES.search(path):
                violations.append(f"  {path}  (matches sensitive-file pattern)")
    if violations:
        print("BLOCKED: protected-path violation (AI_AUDIT_POLICY §7 #4)", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("[check_protected_paths] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
