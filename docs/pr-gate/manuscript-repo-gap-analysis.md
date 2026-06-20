# Manuscript → Repository Gap Analysis
## UIDT v3.9 — Systematic Coverage Audit

**Date:** 2026-05-24  
**Branch:** `feature/audit-toolchain-v1`  
**Manuscript source:** Rietz, P. (2026). *Vacuum Information Density as the Fundamental Geometric Scalar.* DOI: [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)  
**Method:** Cross-reference of all manuscript appendices, figures, tables, and scripts against current repository tree on `main`.

---

## Summary

| Category | Manuscript Items | Repo-Present | Missing |
|---|---|---|---|
| Verification scripts | 7 named | 3 | **4** |
| Figures (numbered) | 9 | 2 | **7** |
| Appendix derivations as code | 8 | 1 | **7** |
| Data files (Monte Carlo) | 3 named | 0 | **3** |
| CSF-UIDT unification module | 1 | 0 | **1** |
| Falsification matrix (machine-readable) | 1 | 0 | **1** |
| **Total gaps** | | | **≥ 23** |

---

## 1. Verification Scripts — Missing

| ID | Manuscript Reference | Expected Path | Status |
|---|---|---|---|
| G-01 | App. K.1: *UIDTMasterVerification.py* | `verification/scripts/UIDTMasterVerification.py` | ❌ Missing |
| G-02 | App. K.1: *geometric_operator.py* | `core/geometric_operator.py` | ❌ Missing |
| G-03 | App. K.3: *UIDT-3.6.1-Verification-visual.py* | `verification/scripts/UIDT-3.6.1-Verification-visual.py` | ❌ Missing |
| G-04 | App. E (Visualization Engine): full script inventory | `verification/scripts/` (multiple) | ❌ Inventory listed but scripts absent |

**Impact:** Reproduction protocol (Section 14.4) cannot be executed without `UIDTMasterVerification.py`. This is a **Critical** reproducibility defect.

---

## 2. Figures — Missing (manuscript Figs. 1–9)

| Fig. | Caption | Expected Path | Status |
|---|---|---|---|
| Fig. 1 | Contractive mapping / mass gap convergence | `manuscript/figures/fig01_massgap_convergence.pdf` | ❌ |
| Fig. 2 | Vacuum energy hierarchy 99-step cascade | `manuscript/figures/fig02_vacuum_hierarchy.pdf` | ❌ |
| Fig. 3 | Dark energy w(z) vs DESI DR2 | `manuscript/figures/fig03_dark_energy_wz.pdf` | ❌ |
| Fig. 4 | Quadratic fit f(z) from DESI DR2 | `manuscript/figures/fig04_fz_quadratic.pdf` | ❌ |
| Fig. 5 | UIDT Architecture four-pillar | `manuscript/figures/fig05_architecture.pdf` | ❌ |
| Figs. 6–9 | Appendix D Monte Carlo posteriors | `manuscript/figures/fig06–09_mcmc.pdf` | ❌ |

**Impact:** Figures referenced in the manuscript are not reproducible from the repo; this violates Section 14.6 (Figure Regeneration).

---

## 3. Appendix Derivations — No Corresponding Script

| App. | Topic | Canonical Script Needed | Status |
|---|---|---|---|
| App. F (all 8 steps) | Gamma invariant RG derivation | `verification/tests/test_gamma_rg_derivation.py` | ❌ Missing |
| App. H.1–H.2 | Two-loop beta functions | `verification/tests/test_two_loop_beta.py` | ❌ Missing |
| App. I.1–I.4 | Kinetic VEV and gamma extraction | `verification/tests/test_kinetic_vev.py` | ❌ Missing |
| App. J (full) | Detailed vacuum calculation all steps | `verification/tests/test_vacuum_full.py` | ❌ Missing |
| App. Q | Osterwalder-Schrader axiom verification | `verification/tests/test_os_axioms.py` | ❌ Missing |
| App. G | BRST gauge consistency | `verification/tests/test_brst.py` | ❌ Missing |
| App. D.1–D.5 | Monte Carlo extended results | `verification/tests/test_mcmc_extended.py` | ❌ Missing |

---

## 4. Data Files — Missing

| File | Referenced In | Expected Path | Status |
|---|---|---|---|
| `UIDTHighPrecisionmeanvalues.csv` | App. I.1 (Eq. 253), F.7.1 | `verification/data/UIDTHighPrecisionmeanvalues.csv` | ❌ Missing |
| Monte Carlo posterior CSV | App. D.3 | `verification/data/mcmc_posteriors.csv` | ❌ Missing |
| DESI DR2 integration data | Section 8.2, Fig. 4 | `verification/data/desi_dr2_hz.csv` | ❌ Missing |

**Impact:** `kinetic_vev = 0.305 ± 0.008 GeV^4` (Eq. 253) is cited from this CSV but the file is absent — the claim cannot be independently verified.

---

## 5. CSF-UIDT Unification Module

Section 10 (16 pages) presents a complete CSF-UIDT unification with 33 numbered equations. No corresponding Python module exists in `core/` or `modules/`.

| Item | Expected | Status |
|---|---|---|
| `modules/csf_uidt_unification.py` | CSF potential, tensor equivalence, 5th-force | ❌ Missing |

---

## 6. Falsification Matrix — Not Machine-Readable

Table 8 (Section 9.7) defines 6 kill-switch criteria F1–F6. These exist as markdown in `CANONICAL/` but are not machine-readable for automated monitoring.

| Item | Expected | Status |
|---|---|---|
| `LEDGER/falsification_matrix.json` | F1–F6 with threshold, method, timeline, status | ❌ Missing |

---

## 7. LEDGER Inconsistency: f_n(g) Formula

The LEDGER (Space-Direktive §2) states:
$$\rho_{\mathrm{vac}}^{\mathrm{obs}} = \rho_{\mathrm{vac}}^{\mathrm{QFT}} \times \pi^{-2} \times \prod_{n=1}^{99} f_n(g)$$

**Finding:** This product form is **not present in the manuscript**. The manuscript specifies:
- App. N.1.1: uniform geometric cascade $f_n = \gamma^{-2}$ for all $n$ (Eq. 290)
- App. N.1.2: three aggregate sector factors (QCD, EW, holographic)
- App. K.2: $\pi^{-2}$ as standalone holographic normalisation

**Recommendation:** LEDGER §2 should be updated to align with Eqs. (290–294) of the manuscript. Proposed replacement:
$$\rho_{\mathrm{vac}} = \Delta^4 \cdot \gamma^{-12} \cdot \left(\frac{M_W}{M_{\mathrm{Pl}}}\right)^2 \cdot \pi^{-2} \qquad [\text{C, open: factor 2.3}]$$

---

## 8. Prioritised Action Plan

### Priority 1 — Reproducibility-Critical (blocker for §14.4)

1. **Recover or reconstruct `UIDTMasterVerification.py`** (G-01) — cited as canonical runner
2. **Recover `geometric_operator.py`** (G-02) — referenced as core implementation
3. **Add `UIDTHighPrecisionmeanvalues.csv`** — underpins kinetic VEV claim (Eq. 253)

### Priority 2 — Figure Regeneration (§14.6)

4. Add figure generation scripts for Figs. 1–5 to `verification/scripts/`
5. Add Monte Carlo posterior scripts + data for Figs. 6–9

### Priority 3 — Open Physics (documented limitations)

6. **Formal beta_kappa derivation** (App. H, I.4, Open Question 6) → enables `test_two_loop_beta.py`
7. **Full kinetic VEV derivation** (App. I, Open Question 5) → enables `test_kinetic_vev.py`
8. **CSF-UIDT module** (Section 10) → `modules/csf_uidt_unification.py`

### Priority 4 — Infrastructure

9. **Falsification matrix JSON** → enables automated kill-switch monitoring
10. **LEDGER §2 f_n(g) clarification** → align with manuscript Eq. (290)

---

*Generated by audit-toolchain-v1 on `feature/audit-toolchain-v1`.  
All findings reference DOI: 10.5281/zenodo.17835200.*
