# Refactor Map: `src/` Layout Migration

**Date:** 2026-07-03  
**Event:** Migration to standard Lean 4 library layout.

This document serves as proof of source integrity for the layout migration. It maps the old file paths to the new file paths. No semantic, logical, or mathematical changes were introduced to the code during this migration.

| Altpfad | Neupfad | Inhaltlich unverändert | Audit |
|---|---|---|---|
| `Antigravit2/Antigravit2.lean` | `src/Antigravit2/Antigravit2.lean` | ja | `lake build Antigravit2` ok |
| `Antigravit2/*` | `src/Antigravit2/*` | ja | `lake build Antigravit2` ok |
| `Antigravit2/NCG/AxiomAudit.lean` | `src/Antigravit2/NCG/AxiomAudit.lean` | ja | `lake build Antigravit2.NCG.AxiomAudit` ok |
