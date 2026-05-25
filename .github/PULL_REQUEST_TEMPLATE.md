## UIDT v3.9 Pull Request

**Thank you for contributing!** This repository maintains strict scientific standards. Please complete this checklist before submitting your PR.

---

## ✅ Pre-Submission Checklist

### Commit Message Format
- [ ] Commit message follows format: `[UIDT-v3.9] <component>: <summary>`
  - Components: `ci`, `docs`, `verification`, `manuscript`, `governance`, `numerics`, `citation`
  - Example: `[UIDT-v3.9] docs: update falsification criteria`
- [ ] Evidence category tag included: `[A]`, `[A-]`, `[B]`, `[C]`, `[D]`, or `[E]`
- [ ] DOI included where relevant: `10.5281/zenodo.17835200`
- [ ] Limitation impact documented if applicable: `L1`, `L2`, `L3`, `L4`, `L5`, `L6`, `L7`

### Code Changes
- [ ] **No changes to core constants:** Δ (1.710 GeV), γ (16.339), κ (0.500), λ_S (0.417)
  - Exception: Only if mathematical error in derivation is proven in PR description
- [ ] **mp.dps = 80** set in all modified modules (precision guard)
  - Never mocked, never centralised, always local
- [ ] **No deletions > 10 lines** in `core/` or `modules/` directories
- [ ] **Protected paths untouched:** `releases/`, `docs/`, `CANONICAL/` (read-only)

### Physics Claims
- [ ] **New physics claims** documented in PR description with:
  - Evidence category [A-E]
  - If Category A/B/C: cited data source
  - If Category D: prediction method
- [ ] **Cosmology claims** are Category C or below (never A or B)
- [ ] **γ parameter** never labelled as "derived" — always "calibrated [A-]"

### Verification
- [ ] Local verification passed:
  ```bash
  python verification/scripts/UIDT_Master_Verification.py
  pytest verification/ -v --tb=short
  ```
- [ ] Residuals remain < 10⁻¹⁴ for Category A claims
- [ ] No regression in numerical precision (80-digit arithmetic)

### Files Changed
**Summary of modified files:**
(List the files changed above in "Files changed" — approved types listed below)

| File Path | Change Type | Reason |
|---|---|---|
| | Code Optimization / Documentation / Test / Visualization | |

---

## 📋 Change Type Classification

**AUTO-APPROVED categories:**
- Typo fixes, formatting, comment clarifications
- Docstring improvements, type hints
- Documentation translations
- New visualization scripts

**REVIEW-REQUIRED categories:**
- Code optimization in `simulation/` or `scripts/`
- New tests in `verification/`
- New validation scripts

**ESCALATION-REQUIRED categories:**
- Any changes to `core/` directory
- Any changes to `modules/` directory
- Parameter changes (without proven derivation error)
- New physics claims

---

## 📝 Description

**What problem does this PR solve?**

**Implementation approach:**

**Testing method:**

---

## 🔗 Related Issues

Closes #

---

## ⚠️ Known Issues

(If any, list here — helps Claude's review)

---

**By submitting this PR, you agree:**
- Your contribution will be licensed under CC BY 4.0
- The UIDT-OS standards apply to all code changes
- Scientific integrity is maintained at all times
