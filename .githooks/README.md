# Versioned git hooks for UIDT-Framework-v3.9-Canonical

This directory contains the canonical hooks used by all clones of this
repository. They are versioned so they survive `git clone` and can be reviewed
in PRs.

## Install once per clone

Unix/macOS:    `./scripts/install-hooks.sh`
Windows cmd:   `scripts\install-hooks.bat`

This sets `git config core.hooksPath .githooks`. The Git client then uses
these versioned hooks instead of the per-clone `.git/hooks/` directory.

## Why this directory exists

Before this directory, hooks lived only in `.git/hooks/`. That meant:
1. Fresh clones had no hooks (silent loss of governance).
2. AI agents pushing via API bypassed the hooks entirely. This is exactly
   how the PR #367 numerology was committed; see `AI_AUDIT_POLICY.md §6`.

This directory closes both gaps. The hooks are now reviewable, shareable, and
auditable. Weakening a hook now requires a PR.

## Files

- `pre-commit` — runs AI_AUDIT_POLICY §7 checks before allowing a commit
- `commit-msg` — enforces `[UIDT] <type>: <summary>` format
- `pre-push` — optional; currently a passthrough
