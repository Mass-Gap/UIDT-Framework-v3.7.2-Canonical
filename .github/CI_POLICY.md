# UIDT CI Policy

This repository uses GitHub Actions as an audit and reproducibility layer for UIDT v3.9. The workflows do not replace the canonical physics source of truth.

## Workflow Responsibilities

- `ci.yml`: validates workflow syntax with actionlint and runs the verification test suite.
- `uidt-pr-review.yml`: performs the PR-level UIDT gate for commit format, protected paths, numerical discipline, and core verification scripts.
- `latex_build_check.yml`: compiles the public manuscript LaTeX targets and uploads build logs.
- `citation-check.yml`: resolves DOI and arXiv references changed by a PR.
- `governance.yml`: enforces repository hygiene, protected-path discipline, evidence tags, and numerics rules.
- `global-sync.yml`: reports SSoT and canonical source drift without committing or pushing changes.

## Local Reproduction

Run these commands before preparing a CI-sensitive PR:

```bash
actionlint .github/workflows/*.yml
python -m pip install -r verification/requirements.txt
python -m pytest verification/tests -q --tb=short
python verification/scripts/UIDT-3.6.1-Verification.py
python verification/scripts/UIDT_Master_Verification.py
python verification/scripts/verify_csf_unification.py
```

For LaTeX checks:

```bash
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error CSF_UIDT_Unification.tex
pdflatex -interaction=nonstopmode -halt-on-error CSF_UIDT_Unification.tex
pdflatex -interaction=nonstopmode -halt-on-error topological_quantization.tex
pdflatex -interaction=nonstopmode -halt-on-error topological_quantization.tex
```

## Governance Rules

- Do not push directly to `main`.
- Use `[UIDT-v3.9] <component>: <summary>` commit subjects.
- Include an evidence category marker in commit bodies for scientific or verification-sensitive changes.
- Treat protected source, ledger, release, UIDT-OS, and manuscript submission paths as protected unless explicit human authorization is present.
- Keep global sync workflows report-only; they must never auto-commit, push, merge, or rewrite canonical sources.
