#!/bin/bash
set -e
git config core.hooksPath .githooks
chmod +x .githooks/*
echo "Hooks installed (core.hooksPath=.githooks)."
ls -la .githooks/
