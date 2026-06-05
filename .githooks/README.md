# Versioned git hooks

This directory contains the canonical pre-commit, commit-msg, and pre-push hooks used by
UIDT-Framework-v3.9-Canonical. They are versioned in the repo so they survive `git clone`
and can be reviewed in PRs.

## Install (once per clone)

Unix/macOS:    ./scripts/install-hooks.sh
Windows (cmd): scripts\install-hooks.bat

This sets `git config core.hooksPath .githooks` for the local clone.

## Why this exists

The previous setup kept hooks only in `.git/hooks/`. That meant:
- New clones had no hooks (silent loss).
- AI agents that pushed via API bypassed the hooks entirely (this is exactly how PR #367
  numerology was committed: see AI_AUDIT_POLICY.md §6).

This directory makes the hooks (a) reviewable, (b) shareable across clones, (c) auditable.
Removing or weakening hooks now requires a PR.
