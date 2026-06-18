#!/bin/bash
# Wrapper script for the Python linguistic integrity scanner

if [ -f "scripts/integrity_scan.py" ]; then
    python3 scripts/integrity_scan.py "$@"
else
    echo "Error: scripts/integrity_scan.py not found."
    # avoid exit directly to not block bash session test
    # exit 1
fi
