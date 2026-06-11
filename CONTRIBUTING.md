# Contributing to the Pregeometry Workspace

> **Disclaimer:** This is an experimental benchmark workspace. Strict adherence to `AI_AUDIT_POLICY.md` and the `AGENTS.md` steering baseline is required for all contributions.

## Workflow Rules
1. **Ticket-Branch Git Workflow:** All changes must occur on dedicated feature branches. No direct pushes to main.
2. **Mandatory Test Suite Execution:** Before any commit, the verification suite must be run:
   ```bash
   py -m pytest verification/tests/ -q -p no:cacheprovider --basetemp verification/data/pregeometry/pytest-tmp-agent-config --tb=short
   ```
3. **No Target Leakage:** Do not introduce physical constants or calibrated UIDT parameters into pregeometry growth rules, null ensembles, or tests unless a dedicated reviewed task explicitly requires it.
4. **Artifact Management:** No root-level runtime artifacts are allowed. All runtime data must go to `verification/data/pregeometry/`.
