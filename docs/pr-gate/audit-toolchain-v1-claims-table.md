# PR Gate — Claims Table (Updated)
## Branch: `feature/audit-toolchain-v1`
**Revision:** 2 — 2026-05-24 (post manuscript audit)  
**DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Status | Falsification Exposure |
|---|---|---|---|---|---|---|
| C-VS-01 | Yang-Mills spectral gap Δ | 1.710 ± 0.015 GeV | [B] | II | ✅ Verified (z ≈ 0.37σ vs lattice) | Lattice excludes Δ by >3σ → Kill Switch F1 |
| C-VS-02 | Canonical RG constraint `\|5κ²−3λ_S\|` | 2.0×10⁻⁵⁶ (dps=80) | [A] | I | ✅ PASS | Residual >1e-14 → [RG_CONSTRAINT_FAIL] |
| C-VS-03 | γ invariant | 16.339 [A-] | [A-] | I | ✅ Calibrated | Photonic test n_crit≠16.339 →Kill Switch F4 |
| C-VS-04 | κ coupling | 0.500 ± 0.008 | [A] | I | ✅ Verified | >3σ lattice deviation falsifies |
| C-VS-05 | Vacuum energy 3-sector suppression (primary path) | ρ_UIDT ≈ 1.05×10⁻⁴⁸ GeV⁴ | [C] | III | ✅ Manuscript-aligned (App. B.3/N.1.2) | Residual factor 2.3 open — L1 |
| C-VS-06 | 99-step geometric cascade cross-check | ρ_cascade = ρ_QCD × γ⁻¹⁹⁸ | [C] | III | ✅ Manuscript N.1.1 Eq.290 | Same as C-VS-05 |
| C-VS-07 | π⁻² holographic normalisation | π⁻² ≈ 0.1013 | [C] | III | ✅ App. K.2 confirmed in manuscript | No independent derivation |
| C-VS-08 | f_n(g) as 99 individually defined functions | — | [E] | — | ❌ NOT FOUND IN MANUSCRIPT | LEDGER §2 inconsistency — see gap analysis |
| C-RG-01 | 1-loop beta_kappa(g) — explicit form | — | [D] | — | ❌ Open (App. I.4, Open Question 6) | Scan [RG_CONSTRAINT_FAIL] expected |
| C-UV-01 | UV toy matching κ=0.500 | 5 scenarios all fail | [D] | III | [TENSION ALERT] | Yukawa or shift-symmetry argument needed |
| C-GAP-01 | UIDTMasterVerification.py present in repo | — | — | — | ❌ MISSING (Critical) | Reproduction protocol blocked |
| C-GAP-02 | geometric_operator.py present in repo | — | — | — | ❌ MISSING (Critical) | Core module reference broken |
| C-GAP-03 | UIDTHighPrecisionmeanvalues.csv present | — | — | — | ❌ MISSING (Critical) | Eq.(253) kinetic VEV unverifiable |
| C-GAP-04 | All 9 manuscript figures regenerable from repo | — | — | — | ❌ 7/9 missing scripts | §14.6 figure regeneration not satisfied |
| C-GAP-05 | Falsification matrix machine-readable JSON | — | — | — | ❌ MISSING | Kill-switch monitoring not automatable |

---

## Mandatory Limitations (§4 Space-Direktive)

| Code | Description | Status |
|---|---|---|
| L1 | 10¹⁰-factor (manuscript: factor 2.3 after 3-sector suppression) | ⚠️ Open — App. J.4/J.5 documents 4 possible resolutions |
| L-β | Explicit 1-loop beta_kappa not derived in manuscript | ⚠️ Open — App. H.2, I.4, Open Question 6 |
| L-UV | UV matching fails for all toy scenarios | ⚠️ Open — needs Yukawa or shift-symmetry |
| L4 | γ RG-gap δγ=0.0047 unherleitet | ⚠️ Open — App. F.9 "empirical value and open problem" |

---

## One-Command Reproduction

```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
cd UIDT-Framework-v3.9-Canonical
git checkout feature/audit-toolchain-v1
pip install mpmath
python tools/vacuum_suppression.py
python tools/rg_sanity.py
python tools/claim_audit.py
bash tools/repro_verification.sh
```

Expected results:
- `vacuum_suppression.py` → `[TENSION ALERT] Residual factor ≈ 0.43` (factor 2.3 open, L1)
- `rg_sanity.py` → `[PASS]` (a) + `[RG_CONSTRAINT_FAIL]` (b) expected, L-β documented

---

## DOI / arXiv Resolvability

| DOI/arXiv | Status | Used for | Evidence Tag |
|---|---|---|---|
| 10.5281/zenodo.17835200 | ✅ Resolves | Primary manuscript | [A-][B][C][D] |
| Morningstar & Peardon 1999 | ✅ Published | Lattice z-score [B] | [B] |
| DESI DR2 (2025) | ✅ Published | H₀, w₀ calibration | [C] |
| Song et al. 2025 (photonic) | Requires verification | Pillar IV analog | [D] |

---

*Prepared per PR-Gate rules, Space-Direktive §6.  
See also: `docs/pr-gate/manuscript-repo-gap-analysis.md`*
