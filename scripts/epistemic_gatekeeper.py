#!/usr/bin/env python3
"""
UIDT Canonical Epistemic Gatekeeper.

Blocks circular dependencies, target hunting, unsupported evidence promotion,
and prestige language in repository text and code.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TARGET_EXTENSIONS = {".py", ".md", ".json"}
DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".cache",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "historical_heuristics",
}

# Audit/test tooling that legitimately contains the forbidden patterns as
# detection regexes or negative test fixtures. These are not physics claims;
# excluding them prevents the gatekeeper from blocking its own tooling.
AUDIT_TOOL_ALLOWLIST = {
    "scripts/epistemic_gatekeeper.py",
    "verification/scripts/check_evidence_tags.py",
    "verification/scripts/check_no_gamma_targeting.py",
    "verification/scripts/check_protected_paths.py",
    "verification/scripts/check_merge_requirements.py",
    "verification/scripts/check_ontology_consistency.py",
    "verification/tests/test_check_scripts.py",
    "AI_AUDIT_POLICY.md",
    "MERGE_PROTOCOL.md",
    "CANONICAL/ONTOLOGY_LINK.md",
}

VALUE_49_OVER_3 = r"49\s*/\s*3"
EVIDENCE_AB = r"\[[AB](?:[+\-\u2212])?\]"
TARGET_KEYWORDS = r"(?:target|zielwert|loss|objective|minimi[sz]e|fit)"
DELTA_PATTERN = r"(?:Delta\*?|delta\*?|\u0394\*?|1\.710)"
GAMMA_PATTERN = r"(?:gamma|\u03b3|16\.339)"
PRESTIGE_PHRASES = (
    r"holy\s+" + "grail",
    "welt" + "formel",
    "def" + r"initive\s+solution",
    "ult" + r"imate\s+answer",
)


@dataclass(frozen=True)
class EpistemicRule:
    rule_id: str
    description: str
    regex: re.Pattern[str]
    error_message: str


@dataclass(frozen=True)
class Violation:
    path: Path
    line_number: int
    content: str
    rule: EpistemicRule


EPISTEMIC_RULES = (
    EpistemicRule(
        rule_id="RULE-01-NUMEROLOGY-PROMOTION",
        description="Blocks association of 49/3 with evidence class A or B.",
        regex=re.compile(
            rf"(?:{VALUE_49_OVER_3}).*{EVIDENCE_AB}|{EVIDENCE_AB}.*(?:{VALUE_49_OVER_3})"
        ),
        error_message=(
            "49/3 is numerological in UIDT audit context and must not be promoted "
            "to evidence class A or B. Use an explicit speculative or withdrawn "
            "classification when applicable."
        ),
    ),
    EpistemicRule(
        rule_id="RULE-02-TARGET-HUNTING",
        description="Blocks 17/3000 as a target, loss, fit, or objective.",
        regex=re.compile(
            rf"(?:{TARGET_KEYWORDS}).*17\s*/\s*3000|"
            rf"17\s*/\s*3000.*(?:{TARGET_KEYWORDS})",
            re.IGNORECASE,
        ),
        error_message=(
            "17/3000 is a diagnostic residual only. It must not be used as a "
            "loss, target, fit value, or optimization objective."
        ),
    ),
    EpistemicRule(
        rule_id="RULE-03-CIRCULAR-KS-INIT",
        description="Blocks back-solving K_S from Delta and gamma.",
        regex=re.compile(
            rf"K_S\s*(?:=|:=)\s*.*{DELTA_PATTERN}\s*/\s*{GAMMA_PATTERN}",
            re.IGNORECASE,
        ),
        error_message=(
            "Circular initialization detected. K_S must not be preinitialized "
            "from Delta/gamma; the flow must derive K_S blindly."
        ),
    ),
    EpistemicRule(
        rule_id="RULE-04-PRESTIGE-LANGUAGE",
        description="Blocks prestige or closure language.",
        regex=re.compile(
            "|".join(PRESTIGE_PHRASES),
            re.IGNORECASE,
        ),
        error_message=(
            "Prestige or closure language detected. UIDT artifacts must use "
            "descriptive, auditable terminology."
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan UIDT repository files for epistemic guardrail violations."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Repository root or subdirectory to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--diff",
        metavar="RANGE",
        help=(
            "Scan only added lines in a git diff range, for example "
            "origin/main...HEAD."
        ),
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Scan only staged added lines.",
    )
    return parser.parse_args()


def should_skip_dir(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in DEFAULT_EXCLUDED_DIRS for part in relative_parts)


def iter_target_files(root: Path) -> Iterable[Path]:
    self_path = Path(__file__).resolve()

    tracked_files = list(iter_git_tracked_files(root))
    if tracked_files:
        for path in tracked_files:
            if path.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            if path.resolve() == self_path:
                continue
            if is_audit_tool(path, root):
                continue
            yield path
        return

    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not should_skip_dir(current_path / dirname, root)
        ]

        for filename in filenames:
            path = current_path / filename
            if path.suffix.lower() not in TARGET_EXTENSIONS:
                continue
            if path.resolve() == self_path:
                continue
            if is_audit_tool(path, root):
                continue
            yield path


def iter_git_tracked_files(root: Path) -> Iterable[Path]:
    repo_root = git_repo_root(root)
    if repo_root is None:
        return ()

    result = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ()

    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = (repo_root / line).resolve()
        if should_skip_dir(path.parent, repo_root):
            continue
        try:
            path.relative_to(root)
        except ValueError:
            continue
        paths.append(path)
    return paths


def git_repo_root(path: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def scan_file(path: Path) -> list[Violation]:
    violations: list[Violation] = []
    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line_number, line in enumerate(handle, start=1):
            violations.extend(scan_line(path, line_number, line))
    return violations


def scan_line(path: Path, line_number: int, line: str) -> list[Violation]:
    violations: list[Violation] = []
    for rule in EPISTEMIC_RULES:
        if rule.regex.search(line):
            violations.append(
                Violation(
                    path=path,
                    line_number=line_number,
                    content=line.strip(),
                    rule=rule,
                )
            )
    return violations


def scan_files(root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for path in iter_target_files(root):
        violations.extend(scan_file(path))
    return violations


def scan_added_lines(root: Path, diff_args: list[str]) -> list[Violation]:
    repo_root = git_repo_root(root)
    if repo_root is None:
        print("[ERROR] Added-line scan requires a git repository.", file=sys.stderr)
        return [
            Violation(
                path=root,
                line_number=0,
                content="",
                rule=EpistemicRule(
                    rule_id="RULE-00-GIT-REQUIRED",
                    description="Git repository required.",
                    regex=re.compile(r"$^"),
                    error_message="Added-line scan requires a git repository.",
                ),
            )
        ]

    result = subprocess.run(
        ["git", "-C", str(repo_root), *diff_args, "--no-color", "--unified=0", "--"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return [
            Violation(
                path=repo_root,
                line_number=0,
                content="",
                rule=EpistemicRule(
                    rule_id="RULE-00-DIFF-FAILED",
                    description="Git diff failed.",
                    regex=re.compile(r"$^"),
                    error_message="Unable to read git diff for added-line scan.",
                ),
            )
        ]

    return scan_unified_added_lines(repo_root, root, result.stdout)


def scan_unified_added_lines(repo_root: Path, root: Path, diff_text: str) -> list[Violation]:
    violations: list[Violation] = []
    self_path = Path(__file__).resolve()
    current_path: Path | None = None
    new_line_number: int | None = None

    for raw_line in diff_text.splitlines():
        if raw_line.startswith("diff --git "):
            current_path = None
            new_line_number = None
            continue

        if raw_line.startswith("+++ "):
            current_path = parse_diff_path(repo_root, root, raw_line[4:])
            if current_path is not None and current_path.resolve() == self_path:
                current_path = None
            if current_path is not None and is_audit_tool(current_path, repo_root):
                current_path = None
            new_line_number = None
            continue

        if raw_line.startswith("@@ "):
            match = re.search(r"\+(\d+)(?:,\d+)?", raw_line)
            new_line_number = int(match.group(1)) if match else None
            continue

        if current_path is None or new_line_number is None:
            continue

        if raw_line.startswith("+"):
            violations.extend(scan_line(current_path, new_line_number, raw_line[1:]))
            new_line_number += 1
        elif raw_line.startswith("-"):
            continue
        elif raw_line.startswith(" "):
            new_line_number += 1

    return violations


def is_audit_tool(path: Path, base: Path) -> bool:
    """True if the path is audit/test tooling allowed to contain forbidden patterns.
    Matches by suffix against the allowlist so it works regardless of the base dir."""
    posix = path.resolve().as_posix()
    return any(posix.endswith(entry) for entry in AUDIT_TOOL_ALLOWLIST)


def parse_diff_path(repo_root: Path, root: Path, diff_path: str) -> Path | None:
    if diff_path == "/dev/null":
        return None
    if diff_path.startswith("b/"):
        diff_path = diff_path[2:]

    path = (repo_root / diff_path).resolve()
    if path.suffix.lower() not in TARGET_EXTENSIONS:
        return None
    if should_skip_dir(path.parent, repo_root):
        return None
    try:
        path.relative_to(root)
    except ValueError:
        return None
    return path


def print_violations(violations: list[Violation], root: Path) -> None:
    print(
        f"\n[FAIL] Scan found {len(violations)} epistemic guardrail "
        "violation(s).\n"
    )
    for violation in violations:
        try:
            display_path = violation.path.relative_to(root)
        except ValueError:
            display_path = violation.path
        print(f"File:   {display_path}:{violation.line_number}")
        print(f"Rule:   {violation.rule.rule_id}")
        print(f"Reason: {violation.rule.error_message}")
        print(f"Code:   {violation.content}")
        print("-" * 72)
    print("\nPull request blocked. Remove the circular or target-hunting pattern.")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")

    args = parse_args()
    root = Path(args.root).resolve()
    if args.diff and args.staged:
        print("[ERROR] Use either --diff or --staged, not both.", file=sys.stderr)
        return 2
    if not root.exists():
        print(f"[ERROR] Scan root does not exist: {root}", file=sys.stderr)
        return 2

    if args.staged:
        print(f"Starting UIDT Epistemic Gatekeeper staged-added-line scan at {root}...")
        violations = scan_added_lines(root, ["diff", "--cached"])
    elif args.diff:
        print(
            "Starting UIDT Epistemic Gatekeeper added-line scan "
            f"for {args.diff} at {root}..."
        )
        violations = scan_added_lines(root, ["diff", args.diff])
    else:
        print(f"Starting UIDT Epistemic Gatekeeper full-tree scan at {root}...")
        violations = scan_files(root)

    if violations:
        print_violations(violations, root)
        return 1

    print("\n[PASS] No target-hunting, circularity, or promotion patterns found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
