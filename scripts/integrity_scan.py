import os
import re
import sys

def main():
    root_dir = "."
    # Broad exclusion patterns
    excludes = [
        "docs/research/", "docs/theory/", "docs/evidence/", "monitoring/",
        "CANONICAL/", "LEDGER/", "clay-submission/", "verification/",
        "simulation/", "agents.md", "docs/audits/", "docs/qa/", "CHANGELOG.md",
        "Supplementary_Results/", "docs/governance/", "best_practices.md",
        "scripts/integrity_scan.py"
    ]

    # Linguistic Integrity Rule: Purge terms unless verified as category [A] or [A-]
    banned_words = [r"\bholy"+" grail\b", r"\bult"+"imate\b", r"\bres"+"olved\b"]
    banned_pattern = re.compile("|".join(banned_words), re.IGNORECASE)
    allowed_pattern = re.compile(r"\[A\]|\[A-\]")

    violations_found = False

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories
        dirnames[:] = [d for d in dirnames if not any(os.path.join(dirpath, d).startswith(os.path.normpath(ex)) for ex in excludes)]

        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(dirpath, filename)

            # Exclude files
            if any(os.path.normpath(filepath).startswith(os.path.normpath(ex)) for ex in excludes):
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception as e:
                continue

            fixed_lines = []
            file_modified = False
            for line_idx, line in enumerate(lines):
                if banned_pattern.search(line) and not allowed_pattern.search(line):
                    print(f"Violation found in {filepath}:{line_idx + 1}")
                    print(f"  Line: {line.strip()}")
                    violations_found = True
                    if "--fix" in sys.argv:
                        line = banned_pattern.sub("", line)
                        file_modified = True
                fixed_lines.append(line)

            if file_modified and "--fix" in sys.argv:
                try:
                    with open(filepath, "w", encoding="utf-8") as f_out:
                        f_out.writelines(fixed_lines)
                except Exception:
                    pass

    if violations_found:
        sys.exit(1)
    else:
        print("Linguistic Integrity Check Passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
