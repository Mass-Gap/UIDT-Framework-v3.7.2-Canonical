#!/bin/bash
set -e
ROOT=$(git rev-parse --show-toplevel)
git config core.hooksPath .githooks
chmod +x "$ROOT/.githooks/"*
echo "Hooks installed via core.hooksPath=.githooks. Active hooks:"
ls -la "$ROOT/.githooks/"
