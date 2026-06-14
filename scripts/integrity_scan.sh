#!/bin/bash
# scripts/integrity_scan.sh
# Purges "holy grail", "ultimate", "resolved" from Markdown files
# Excludes docs/governance/, best_practices.md, and core audit logs.
# Enforces the Linguistic Integrity Rule (CoVe Stage 4).

# Use python to perform context-aware line-by-line parsing as required.

python3 -c '
import os
import re

exclude_paths = ["docs/governance", "best_practices.md", "logs", "LOCAL/logs"]
prohibited = ["holy grail", "ultimate", "resolved"]
pattern = re.compile(r"\b(" + "|".join(prohibited) + r")\b", re.IGNORECASE)

def should_exclude(filepath):
    for exc in exclude_paths:
        if exc in filepath:
            return True
    return False

def scan_and_purge():
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".archive" in root:
            continue

        for file in files:
            if not file.endswith(".md"):
                continue

            filepath = os.path.join(root, file)
            if should_exclude(filepath):
                continue

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                modified = False
                new_lines = []
                for line in lines:
                    if "[A]" in line or "[A-]" in line:
                        # Skip line if verified as Category [A]
                        new_lines.append(line)
                        continue

                    new_line, num_subs = pattern.subn("", line)
                    if num_subs > 0:
                        modified = True
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)

                if modified:
                    print(f"Purged prohibited terms from {filepath}")
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

scan_and_purge()
'
