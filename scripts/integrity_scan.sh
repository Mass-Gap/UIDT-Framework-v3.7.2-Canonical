#!/bin/bash

# Wrapper for the Python integrity scan script
python "$(dirname "$0")/integrity_scan.py" "$@"
