import os
import re
import sys
from pathlib import Path

# Terms restricted to [A] or [A-] categories
RESTRICTED_TERMS = ["holy grail", "ultimate", "resolved"]
# Valid evidence tags
EVIDENCE_TAGS = ["[A]", "[A-]"]

# Excluded paths (governance, QA, audit logs)
EXCLUDED_PATTERNS = [
    r"docs/governance/.*",
    r"best_practices\.md",
    r"agents\.md"
]

def is_excluded(filepath):
    path_str = str(filepath).replace('\\', '/')
    for pattern in EXCLUDED_PATTERNS:
        if re.search(pattern, path_str):
            return True
    return False

def scan_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                lower_line = line.lower()
                for term in RESTRICTED_TERMS:
                    if term in lower_line:
                        # Check if line contains a valid tag
                        has_tag = any(tag in line for tag in EVIDENCE_TAGS)
                        if not has_tag:
                            violations.append((line_num, term, line.strip()))
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return violations

def main():
    root_dir = Path(".")
    total_violations = 0
    for md_file in root_dir.rglob("*.md"):
        if is_excluded(md_file):
            continue
        violations = scan_file(md_file)
        if violations:
            print(f"Violations found in {md_file}:")
            for line_num, term, line in violations:
                print(f"  Line {line_num}: Restricted term '{term}' used without [A] or [A-] tag.")
                print(f"    Content: {line}")
                total_violations += 1
            print("-" * 40)

    if total_violations > 0:
        print(f"Total violations: {total_violations}")
        # Re-enabling the exit 1 failure logic for the review.
        sys.exit(1)
    else:
        print("Linguistic integrity check passed. No violations.")
        sys.exit(0)

if __name__ == "__main__":
    main()
