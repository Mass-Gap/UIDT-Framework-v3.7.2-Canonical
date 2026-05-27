#!/bin/bash
# scripts/integrity_scan.sh
# Purges banned linguistic terms ("holy grail", "ultimate", "resolved") unless [A] verified.

FILE_PATH=$1

if [ -z "$FILE_PATH" ]; then
    echo "Usage: \$0 <file_path>"
    # Use standard shell exit by wrapping in a subshell or a function, but since it's an executable script:
    bash -c 'exit 1'
    return 1 2>/dev/null
fi

# Check if [A] is in the file. If so, skip purging.
if grep -q "\[A\]" "$FILE_PATH"; then
    echo "[integrity_scan.sh] Skipping $FILE_PATH: [A] evidence found."
    return 0 2>/dev/null || bash -c 'exit 0'
else
    # We use perl or sed to remove banned words case-insensitively. We replace them with [REDACTED].
    # Using perl for robust word boundary and case insensitivity replacement in-place
    perl -pi -e 's/\b(holy grail|ultimate|resolved)\b/[REDACTED]/gi' "$FILE_PATH"

    echo "[integrity_scan.sh] Scanned and purged $FILE_PATH"
fi
