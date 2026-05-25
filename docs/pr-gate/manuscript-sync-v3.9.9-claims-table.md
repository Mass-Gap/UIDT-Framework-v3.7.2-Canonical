# PR-Gate Claims Table — manuscript-sync-v3.9.9

**Branch:** `feature/manuscript-sync-v3.9.9`  
**Date:** 2026-05-25  
**PI:** Philipp Rietz  
**DOI:** [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200)

---

## Scope

This PR resolves 5 priority discrepancies between the UIDT v3.9 manuscript
(`UIDT_v3.9-Complete-Framework.pdf`) and the repository ledger/codebase.
No physics constants are modified. No `core/` or `modules/` files are touched.
`main` branch is read-only; all changes on `feature/manuscript-sync-v3.9.9`.

---

## Claims Table (PR-Gate §6)

| Claim ID | Claim Statement | Value / Change | Evidence Tag | Stratum | Status | Falsification Exposure |
|---|---|---|---|---|---|---|
| **UIDT-C-018** | 10¹⁰ geometric factor derivation | Notes updated: §4.1 Eq.(10) overclaim documented; `calibrated scaffold [C], L1 open` | E | III | open | Analytical derivation from L_UIDT outside scaffold range refutes C-018 scaffold |
| **UIDT-C-042** | 10¹⁰ geometric factor (v3.7 duplicate) | Same as C-018; notes now reference `derive_fn_vacuum_suppression.py` (PR #507) | E | III | open | Idem C-018 |
| **UIDT-C-017** | N=99 RG steps justification | Notes updated: N=99 manuscript-faithful scaffold in script; C-046 superseded | E | III | open | N≠99 yielding better ρ_vac match |
| **UIDT-C-039** | N=99 RG steps (v3.7 duplicate) | Notes updated: N=94.05 superseded, see C-017 | E | III | open | Idem C-017 |
| **UIDT-C-046** | N=94.05 proposed replacement | `status: superseded`, `superseded_by: UIDT-C-050 / Eq.291 / PR #505` | E | III | superseded | Contradiction C-017/C-046 resolved |
| **UIDT-C-052** | SU(3) γ = 49/3 conjecture | Evidence clarified: `E (scaffold [D])`; script `su3_gamma_conjecture_test.py` added | E | III | conjectured | Analytical derivation yields γ ≠ 49/3 |
| **UIDT-C-056** | χ_top tension z=4.2σ | Notes: **L6 missing from manuscript §13** explicitly flagged for pre-arXiv fix | D | III | predicted | NLO result outside [140,220] MeV |
| **NEW SCRIPT** | `verification/tests/su3_gamma_conjecture_test.py` | Tests C-052; mp.dps=80; RG-PASS verified; no mock physics | E (scaffold [D]) | III | scaffold | γ_SU3 ≠ 49/3 from first principles |
| **NEW SCRIPT** | `verification/scripts/derive_fn_vacuum_suppression.py` | Scaffold f_n(g); mp.dps=80; documents §4.1 overclaim explicitly | E (scaffold [D]) | III | scaffold | Product outside [1e-12,1e-8] for physical g refutes scaffold |

---

## One-Command Reproduction

```bash
# Clone and run both scripts (Python 3 + mpmath required)
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
pip install mpmath

python verification/tests/su3_gamma_conjecture_test.py
python verification/scripts/derive_fn_vacuum_suppression.py
```

Expected output:
- `PASS — su3_gamma_conjecture_test completed without RG violation`
- `PASS — derive_fn_vacuum_suppression completed`

---

## DOI / arXiv Resolvability

| Source | Status | Used for | Evidence Tag |
|---|---|---|---|
| [10.5281/zenodo.17835200](https://doi.org/10.5281/zenodo.17835200) | ✅ resolvable | Framework DOI | All claims |
| [arXiv:2501.08217](https://arxiv.org/abs/2501.08217) (Dürr et al. 2025) | ✅ resolvable | C-056 lattice reference | B→D override |
| PDG 2024 α_s | ✅ public | C-055 external input | E |

---

## Mandatory Limitations (Space-Directive §4)

- **L1:** 10¹⁰ factor open — f_n(g) not derived from L_UIDT (this PR adds scaffold only)
- **L4:** γ RG-gap δγ=0.0047 unresolved — C-052 remains [E] conjecture
- **L6:** C-056 χ_top z=4.2σ tension — **manuscript §13 must add this before arXiv submission**
- **L-β:** Physical 1-loop β-functions not derived from ℒ_UIDT

---

## Acceptance Criteria

- [x] No physics constants modified
- [x] No `core/` or `modules/` files touched
- [x] `main` branch read-only (feature branch only)
- [x] Both scripts pass with `mp.dps=80`, no `float()`, no mocks
- [x] RG constraint `|5κ²−3λ_S| < 1e-14` verified in both scripts
- [x] All evidence tags per Space-Directive §2/§3
- [x] C-046 status → superseded (contradiction resolved)
- [ ] **Manuscript §4.1 Eq.(10) text correction** — required before arXiv (Philipp's action)
- [ ] **Manuscript §13 L6 addition** — required before arXiv (Philipp's action)
