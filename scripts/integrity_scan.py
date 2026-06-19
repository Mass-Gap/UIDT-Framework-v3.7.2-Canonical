import os
import re
import sys
from pathlib import Path

# Linguistic Integrity Rule Enforcement
# Terms to purge unless verified as category [A]
FORBIDDEN_TERMS = ["holy" + " " + "grail", "ulti" + "mate", "resol" + "ved"]
FORBIDDEN_PATTERN = re.compile(r'\b(?:' + '|'.join(FORBIDDEN_TERMS) + r')\b', re.IGNORECASE)

EVIDENCE_PATTERN = re.compile(r'\[A\]|\[A-\]')

# Broad exclusion patterns for directories
EXCLUDED_PATHS = [
    "docs/research/", "docs/theory/", "docs/evidence/", "monitoring/", "CANONICAL/", "LEDGER/", "clay-submission/", "verification/", "simulation/", "agents.md",
    "docs/audits/",
    "docs/qa/",
    "CHANGELOG.md",
    "Supplementary_Results/",
    "docs/governance/",
    "best_practices.md",
    "scripts/integrity_scan.py"
]

def should_exclude(filepath):
    # Ensure filepath is treated correctly against exclusions
    path_str = str(filepath)
    for exclusion in EXCLUDED_PATHS:
        if exclusion in path_str:
            return True
    return False

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if FORBIDDEN_PATTERN.search(line):
                    # Check if line has [A] or [A-] tag
                    if not EVIDENCE_PATTERN.search(line):
                        violations.append((i+1, line.strip()))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return violations

def main():
    root_dir = Path(".")
    if len(sys.argv) > 1:
        root_dir = Path(sys.argv[1])

    all_violations = {}

    for md_file in root_dir.rglob("*.md"):
        if should_exclude(md_file):
            continue

        violations = scan_file(md_file)
        if violations:
            all_violations[md_file] = violations

    if all_violations:
        print("Linguistic Integrity Rule Violations Found:")
        for file, violations in all_violations.items():
            for line_num, line in violations:
                print(f"{file}:{line_num}: {line}")
        sys.exit(1)
    else:
        print("Linguistic Integrity Check Passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
