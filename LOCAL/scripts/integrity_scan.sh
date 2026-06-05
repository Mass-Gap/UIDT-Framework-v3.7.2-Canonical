#!/bin/bash
# Script to enforce the Linguistic Integrity Rule (purging "holy grail", "ultimate", "resolved")
# Exceptions: docs/qa/*, verification/scripts/checks/*, verification/tests/*

BRANCH=$1

if [ -z "$BRANCH" ]; then
    echo "Usage: $0 <branch>"
else
    echo "Running Linguistic Integrity Scan on branch: $BRANCH"

    # Patterns to ban
    BANNED_WORDS="holy grail|ultimate|resolved"

    # Find all text files modified in the branch compared to main
    FILES=$(git diff --name-only origin/main...$BRANCH 2>/dev/null)

    for FILE in $FILES; do
        # Skip exceptions
        if [[ "$FILE" == docs/qa/* ]] || [[ "$FILE" == verification/scripts/checks/* ]] || [[ "$FILE" == verification/tests/* ]]; then
            continue
        fi

        # Check if the file contains banned words using grep
        if git show $BRANCH:$FILE 2>/dev/null | grep -iE "$BANNED_WORDS" > /dev/null; then
            echo "Linguistic Integrity Violation found in: $FILE"
            # In a full implementation, we might try to auto-replace or flag for manual review
            # Here we just output the violation
        fi
    done

    echo "Linguistic Integrity Scan completed."
fi
