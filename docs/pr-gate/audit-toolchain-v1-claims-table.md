# PR Gate — Audit Toolchain v1 Claims Table

**PR:** `feature/audit-toolchain-v1`  
**Date:** 2026-05-24  
**Framework:** UIDT v3.9 Canonical  
**DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)  
**Space Directive §6 compliance:** ✅

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|---|---|---|---|---|---|---|---|
| C-RG-01 | RG constraint satisfied | \|5κ²−3λ_S\| < 1e-14 | [A] | I | LEDGER/CLAIMS.json + mp.dps=80 | **PASS** residual=2.0e-56 | Violation >1e-14 → `[RG_CONSTRAINT_FAIL]` |
| C-RG-SCAN | 1-loop RG stability under running | \|5κ²−3λ_S\| stable over μ∈[1,10⁶] GeV | [D] | III | tools/rg_sanity.py (placeholder β) | **[RG_CONSTRAINT_FAIL]** 500/500 steps — placeholder β only | Physical β-functions must be derived from UIDT Lagrangian |
| C-κ-01 | Coupling κ canonical value | κ = 0.500 | [A] | I | LEDGER/CLAIMS.json | Canonical | LHC S-coupling inconsistent with κ=0.500 |
| C-λS-01 | Self-coupling λ_S = 5/12 | λ_S = 5/12 ≈ 0.41667 | [A] | I | LEDGER/CLAIMS.json | Canonical | Physical β drives λ_S off RG trajectory |
| C-γ-01 | Geometric coupling γ | γ = 16.339 | [A-] | I | LEDGER/CLAIMS.json | Calibrated | Photonic test at n=16.339 fails |
| C-Δ-01 | Yang-Mills spectral gap | Δ = 1.710 ± 0.015 GeV | [B] | II | Lattice 2024 quenched; ERRATUM confirmed | Lattice-compatible z≈0.37σ | Lattice excludes Δ by >3σ |
| C-UV-01 | Heavy-fermion UV completion | κ̄/Λ ~ y²/(16π²M) | [D] | III | tools/uv_match.py | **[TENSION ALERT]** rel. diff. ≈99% — κ̄ ≪ κ_canonical | No UV model reproduces κ=0.500 without large y or symmetry argument |
| C-VAC-01 | 99-stage vacuum suppression | ρ_vac=2.45e-47 GeV⁴ | [C] calibrated | I | LEDGER/CLAIMS_ADDENDUM_C054_C056 | **[TENSION ALERT]** f_n placeholder | Casimir \|ΔF/F\|<0.1%; DESI exact w=-1.00 |
| C-ET-01 | Torsion energy threshold | E_T = 2.44 MeV | [C] | I | LEDGER/CLAIMS.json | Canonical | E_T→0 with Σ_T≠0 → `[TORSION_CONSTRAINT_FAIL]` |

---

## Mandatory Limitations

- **L1:** Open ~10¹⁰ factor in vacuum energy suppression (f_n placeholder used)
- **L2:** Electron-mass discrepancy ≈23% — not addressed in this toolchain
- **L4:** Unresolved γ RG-gap: γ=16.339 [A-] vs γ∞=16.3437
- **UV:** No explicit UV completion reproduces κ=0.500 in toy model
- **β:** Physical UIDT 1-loop β-functions not yet derived — rg_sanity.py uses placeholders

---

## One-Command Reproduction

```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
git checkout feature/audit-toolchain-v1
pip install mpmath numpy
bash tools/repro_verification.sh
```

Expected outputs: `audit_report.json`, `verification/data/visualizations/rg_scan.csv`,  
`verification/data/visualizations/uv_matching.md`, `verification/data/visualizations/vacuum_suppression.csv`,  
`repro_report.md`

---

## DOI / arXiv Resolvability

| Reference | Status | Used For | Evidence Tag |
|---|---|---|---|
| doi:10.5281/zenodo.17835200 | ✅ Canonical DOI | Parameter ledger source | [A]/[C] |
| LEDGER/CLAIMS.json SHA:4352e2e | ✅ Verified | Claim values | [A]/[B]/[C] |
| Lattice 2024 quenched (ERRATUM) | ✅ Applied | Δ=1.710 GeV [B] | [B] |

---

## Reviewer Attack Surface Summary

1. **RG-SCAN failure** — Expected with placeholders; physical β derivation is the open action item.
2. **UV matching tension** — Fundamental: κ=0.500 requires either O(1) Yukawa, compositeness, or shift symmetry.
3. **f_n(g) undefined** — L1 limitation acknowledged; canonical definition must be extracted from CLAIMS_ADDENDUM.
4. **RG-gap L4** — γ=16.339 [A-] vs γ∞=16.3437 remains open; δγ=0.0047 documented.
