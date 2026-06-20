# PR-Gate Claims Table — `feature/audit-toolchain-v1`

**DOI:** `10.5281/zenodo.17835200`  
**Branch:** `feature/audit-toolchain-v1` → `main`  
**Date:** 2026-05-24  
**Author:** P. Rietz / Antigravity Assistant v4.1  
**UIDT Version:** v3.9 Canonical  
**Status:** READY FOR REVIEW (non-physics; claims table + reproduction note only)

---

## Summary

This PR contributes **no new physics code**. All verification scripts referenced
below already exist in `verification/scripts/` under their canonical names.
The sole new artifact is this PR-Gate documentation file, which:

1. maps each active script to its Claim ID and evidence tag,
2. provides a one-command reproduction note referencing existing paths,
3. records DOI/arXiv resolvability status per §6 rules.

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source (script) | Status | Falsification Exposure |
|---|---|---|---|---|---|---|---|
| C-RG-01 | RG constraint `5κ²=3λ_S` holds exactly | Residual < 1×10⁻¹⁴ | [A] Mathematical | I | `verification/scripts/rg_flow_analysis.py` | PASS | Violated if residual ≥ 1×10⁻¹⁴ at mp.dps=80 → `[RG_CONSTRAINT_FAIL]` |
| C-RG-02 | γ = 16.339 [A-] calibrated | 16.339 ± 0.0047 | [A-] Calibrated | I | `verification/scripts/derive_rg_gamma_extended.py` | ACTIVE | Falsified if photonic test at n=16.339 fails |
| C-RG-03 | 1-loop β fixed-point consistent with κ=0.500 | Fixed-point confirmed | [A-] Calibrated | III | `verification/scripts/verify_2loop_beta_fixpoint.py` | OPEN — physical β not yet derived from ℒ_UIDT | Physical β from ℒ_UIDT derivation required |
| C-GAP-01 | Yang-Mills spectral gap Δ = 1.710 ± 0.015 GeV | 1.710 GeV | [B] Lattice-compatible | II | `verification/scripts/hybrid_uidt_raumzeit_spectral_gap.py` | ACTIVE (z≈0.37σ from lattice) | Falsified if lattice excludes by >3σ |
| C-VAC-01 | Vacuum suppression: ρ_vac^obs = ρ_vac^QFT × π⁻² × ∏f_n(g) | ρ_vac ≈ 2.45×10⁻⁴⁷ GeV⁴ | [C] Calibrated cosmology | III | `verification/scripts/verify_kissing_number_suppression.py` | OPEN — f_n(g) placeholder; 10¹⁰ factor open (L1) | f_n from CLAIMS_ADDENDUM_C054_C056 required |
| C-VAC-02 | Dilaton source contributes to vacuum energy | Δρ < ρ_obs | [C] Calibrated cosmology | III | `verification/scripts/solve_dilaton_source.py` | ACTIVE | Falsified if dilaton field excluded by CMB constraints |
| C-TOR-01 | Torsion E_T = 2.44 MeV; if E_T=0 then Σ_T=0 exactly | 2.44 MeV | [C] Calibrated cosmology | III | `verification/scripts/s4_p4_p5_p6_torsion_verification.py` | ACTIVE | `[TORSION_CONSTRAINT_FAIL]` if E_T=0 but Σ_T≠0 |
| C-BRST-01 | BRST/Kugo-Ojima confinement criterion satisfied | Operator norm < 1 (Banach L<1) | [A] Mathematical | I | `verification/scripts/verify_brst_dof_reduction.py`, `verify_brst_kugo_ojima_audit.py` | PASS | Violated if operator norm ≥ 1 |
| C-FRG-01 | FRG flow consistent with Δ and γ in IR | IR fixed-point reached | [A-] Calibrated | III | `verification/scripts/frg_solver_rk45.py`, `verify_frg_gamma_path_b.py` | ACTIVE | Falsified if FRG flow diverges in IR sector |
| C-COSMO-01 | H₀ = 70.4 ± 0.16 km/s/Mpc calibrated mapping | 70.4 km/s/Mpc | [C] Calibrated cosmology | III | `verification/scripts/verify_desi_dr2_integration.py` | ACTIVE — calibrated mapping only, not resolution of H₀ tension | Falsified if DESI/equivalent confirms exact w=−1.00 |
| C-GAMMA-01 | γ-constraint test: γ∞ = 16.3437, δγ = 0.0047 | 16.3437 | [A-] Calibrated | I/III | `verification/scripts/gamma_constraint_test.py` | ACTIVE — L4 δγ RG-gap unherleitet | Falsified if independent derivation gives δγ > 0.01 |
| C-AUDIT-01 | Daily audit passes all parameter ledger checks | All CLAIMS.json hashes match | [A] Mathematical | I | `verification/scripts/daily_audit.py`, `audit_graph.py` | PASS | Broken if CLAIMS.json SHA256 mismatch detected |

---

## Mandatory Limitations (§4)

| ID | Description | Status |
|---|---|---|
| L1 | 10¹⁰ open factor in vacuum suppression; f_n(g) not derived | **OPEN** |
| L2 | Electron-mass discrepancy ≈23% | **OPEN** |
| L4 | δγ = 0.0047 RG-gap unherleitet | **OPEN** |
| L-β | Physical 1-loop β-functions not derived from ℒ_UIDT | **OPEN** |

---

## One-Command Reproduction Note

All scripts referenced above are already present in the canonical repository.
No installation of new scripts is required.

```bash
# Clone and run from repository root
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical.git
cd UIDT-Framework-v3.9-Canonical
pip install mpmath numpy scipy

# Full verification suite (existing entry point)
python verification/scripts/verify_all.py

# Individual canonical checks (existing scripts)
python verification/scripts/rg_flow_analysis.py
python verification/scripts/gamma_constraint_test.py
python verification/scripts/hybrid_uidt_raumzeit_spectral_gap.py
python verification/scripts/verify_kissing_number_suppression.py
python verification/scripts/s4_p4_p5_p6_torsion_verification.py
python verification/scripts/verify_brst_dof_reduction.py
python verification/scripts/daily_audit.py
```

> **Note:** `verify_all.py` calls `verification/tests/` via pytest.
> Scripts not found are skipped with `[WARNING]`; no fatal exit unless
> a found script returns non-zero.

---

## DOI / arXiv Resolvability

| DOI / arXiv | Status | Used for | Evidence Tag |
|---|---|---|---|
| `10.5281/zenodo.17835200` | ✅ Resolvable (Zenodo) | UIDT v3.9 Canonical primary reference | [A]/[B]/[C] |
| `zenodo.org/records/18072470` | ✅ Resolvable | Supporting cosmology calibration | [C] |
| `zenodo.org/records/18740600` | ✅ Resolvable | Supplementary lattice analysis | [B] |
| `zenodo.org/records/19228489` | ✅ Resolvable | Extended γ-sector documentation | [A-] |

No arXiv preprint currently registered for v3.9 Canonical.
`No verified arXiv source available. Claim cannot be promoted beyond current tags without peer review.`

---

## Acceptance Status

- **Physics claims:** No new physics introduced. All values from `CANONICAL/` ledger.
- **Code:** No new scripts. All reproduction paths point to existing `verification/scripts/`.
- **Open items before merge:** L1, L2, L4, L-β remain open — documented, not blocking this PR.
- **Recommendation:** ✅ READY TO MERGE (documentation-only PR)
