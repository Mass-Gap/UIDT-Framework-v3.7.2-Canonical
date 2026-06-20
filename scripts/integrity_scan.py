import re
import sys
import os
import glob

# Words to flag (obfuscated)
FORBIDDEN_WORDS = [
    chr(104) + chr(111) + chr(108) + chr(121) + " " + chr(103) + chr(114) + chr(97) + chr(105) + chr(108),
    chr(117) + chr(108) + chr(116) + chr(105) + chr(109) + chr(97) + chr(116) + chr(101),
    chr(114) + chr(101) + chr(115) + chr(111) + chr(108) + chr(118) + chr(101) + chr(100)
]

ALLOWED_TAGS = ["[A]", "[A-]"]

# Exclusions
EXCLUDE_DIRS = [
    "docs/research/",
    "docs/audits/",
    "docs/qa/",
    "Supplementary_Results/",
]
EXCLUDE_FILES = [
    "CHANGELOG.md",
    "best_practices.md"
]
EXCLUDE_GLOBS = [
    "docs/governance/*"
]

def should_exclude(filepath):
    filepath = filepath.replace("\\", "/")

    for ex_dir in EXCLUDE_DIRS:
        if filepath.startswith(ex_dir):
            return True

    for ex_file in EXCLUDE_FILES:
        if filepath.endswith(ex_file) or os.path.basename(filepath) == ex_file:
            return True

    for ex_glob in EXCLUDE_GLOBS:
        import fnmatch
        if fnmatch.fnmatch(filepath, ex_glob):
            return True

    return False

def check_file(filepath, purge=False):
    violations = []
    if should_exclude(filepath):
        return violations

    try:
        lines = []
        modified = False
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            lower_line = line.lower()
            line_has_violation = False
            for word in FORBIDDEN_WORDS:
                if word in lower_line:
                    if "[A]" in line or "[A-]" in line:
                        continue
                    else:
                        violations.append(f"{filepath}:{i+1} Violation found without tag.")
                        line_has_violation = True

            if purge and line_has_violation:
                # remove words
                for word in FORBIDDEN_WORDS:
                    pattern = re.compile(re.escape(word), re.IGNORECASE)
                    lines[i] = pattern.sub("", lines[i])
                modified = True

        if purge and modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)

    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return violations

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "--purge":
        files_to_check = [f for f in sys.argv[1:] if f != "--purge"]
    else:
        files_to_check = glob.glob("**/*.md", recursive=True)

    all_violations = []
    for filepath in files_to_check:
        if os.path.isfile(filepath):
            violations = check_file(filepath, purge=('--purge' in sys.argv))
            all_violations.extend(violations)

    if all_violations:
        for v in all_violations:
            print(v)
        sys.exit(1)
    else:
        print("Linguistic Integrity Check Passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
