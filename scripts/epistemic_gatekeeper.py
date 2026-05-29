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
    if not root.exists():
        print(f"[ERROR] Scan root does not exist: {root}", file=sys.stderr)
        return 2

    print(f"Starting UIDT Epistemic Gatekeeper scan at {root}...")
    violations = scan_files(root)

    if violations:
        print_violations(violations, root)
        return 1

    print("\n[PASS] No target-hunting, circularity, or promotion patterns found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
