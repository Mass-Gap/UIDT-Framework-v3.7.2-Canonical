#!/usr/bin/env python3
"""AI_AUDIT_POLICY §7 #4: block commits that add files under protected paths.
Deterministic. No LLM. Exit 0 on pass, 1 on violation, 2 on error."""
from __future__ import annotations
import os, re, subprocess, sys

PROTECTED_DIRS = (
    "UIDT-OS/", ".claude/", ".trae/", ".antigravity/", ".cursor/",
    ".kilo/", ".kilocode/", ".auxly/", ".traycer/", ".venv/",
)
LOCAL_ALLOWED = {"LOCAL/uidt-repo.cfg", "LOCAL/scripts/ralph_wiggum_loop.py"}
SECRET_FILES = re.compile(
    r"(?:^|/)(\.env|\.env\.[^/]+|[^/]+\.(?:key|pem)|credentials\.json|config\.local\.yaml)$"
)

def changed_files() -> list[str]:
    base = os.environ.get("GITHUB_BASE_REF")
    ref = f"origin/{base}" if base else "origin/main"
    try:
        out = subprocess.check_output(
            ["git","diff","--name-only","--diff-filter=AM",f"{ref}...HEAD"],
            text=True, encoding="utf-8", errors="replace",
        )
        return [l.strip() for l in out.splitlines() if l.strip()]
    except subprocess.CalledProcessError:
        out = subprocess.check_output(
            ["git","diff","--cached","--name-only","--diff-filter=AM"],
            text=True, encoding="utf-8", errors="replace",
        )
        return [l.strip() for l in out.splitlines() if l.strip()]

def main() -> int:
    violations: list[str] = []
    for path in changed_files():
        # Protected dirs
        if any(path.startswith(d) for d in PROTECTED_DIRS):
            violations.append(f"  {path}  (protected dir)")
            continue
        # LOCAL/ has exactly one allowed file
        if path.startswith("LOCAL/") and path not in LOCAL_ALLOWED:
            violations.append(f"  {path}  (LOCAL/ allows only: {sorted(LOCAL_ALLOWED)})")
            continue
        # Secret files anywhere
        if SECRET_FILES.search(path):
            violations.append(f"  {path}  (secret-file pattern)")
    if violations:
        print("BLOCKED: protected-path violation (AI_AUDIT_POLICY §7 #4)", file=sys.stderr)
        for v in violations:
            print(v, file=sys.stderr)
        return 1
    print("[check_protected_paths] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
