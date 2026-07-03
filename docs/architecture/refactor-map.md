# Refactor Map: `src/` Layout Migration

**Date:** 2026-07-03  
**Event:** Migration to standard Lean 4 library layout.

This document serves as proof of source integrity for the layout migration. It maps the old file paths to the new file paths. No semantic, logical, or mathematical changes were introduced to the code during this migration.

| Old Path | New Path | Status |
|---|---|---|
| `verification/antigravit2/Antigravit2.lean` | `verification/antigravit2/src/Antigravit2.lean` | Moved (`git mv`) |
| `verification/antigravit2/Antigravit2/*` | `verification/antigravit2/src/Antigravit2/*` | Moved (`git mv`) |

**Integrity Verification:**
The imports internally already used the `Antigravit2.` prefix. By setting `srcDir := "src"` in `lakefile.lean`, the module resolution remains identical. The `lake build` output remains deterministically identical and `sorry`-free.
