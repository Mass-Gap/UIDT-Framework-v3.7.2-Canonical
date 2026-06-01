#!/bin/bash
# Linguistic Integrity Rule: Purge terms like 'holy grail', 'ultimate', and 'resolved'
# from text unless verified as category [A].

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <file_to_scan>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File $FILE not found."
    exit 1
fi

# Use sed to remove the forbidden words (case-insensitive) on lines that do NOT contain "[A]"
sed -i -E '/\[A\]/! s/\b(holy grail|ultimate|resolved)\b//gI' "$FILE"

echo "Linguistic integrity scan complete for $FILE."
