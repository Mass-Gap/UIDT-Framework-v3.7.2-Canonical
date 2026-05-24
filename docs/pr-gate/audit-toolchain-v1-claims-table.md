# PR Gate: feature/audit-toolchain-v1 — Claims Table (v2)

> **PR:** [#502](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/pull/502)  
> **Branch:** `feature/audit-toolchain-v1`  
> **Date:** 2026-05-24  
> **Compiled by:** Antigravity / UIDT-Assistant v4.1  
> **Status:** UPDATED — physical 1-loop β, UV matching, parametric f_n added (patch v2)

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|----------|-------|-------|--------------|---------|--------|--------|------------------------|
| C-AT-01 | RG canonical constraint \|5κ²−3λ_S\| < 1e-14 | Residual 2.0×10⁻⁵⁶ (dps=80) | [A] | I | `tools/rg_sanity.py` v2.0, `CANONICAL/CONSTANTS.md` v3.9.5 | PASS | Falsified if residual ≥ 1e-14 at dps=80 with exact κ=1/2 |
| C-AT-02 | Physical 1-loop β_κ vanishes at canonical point | β_κ = lf·κ·[4(λ_S+κ²)−g₃²·N_c]; non-zero unless g₃² = 4(λ_S+κ²)/N_c ≈ 1.46 GeV² | [D] | III | `tools/rg_sanity.py` v2.0, background-field derivation | [TENSION ALERT] requires g₃² consistency | Falsified if lattice g₃² at μ=m_S excludes value giving β_κ=0 |
| C-AT-03 | Physical 1-loop β_{λ_S} vanishes at canonical point | β_{λ_S} = lf·[20λ_S²−12κ⁴·dim_F+3κ⁴·N_c²]; numerically ~10⁻⁴/16π² | [D] | III | `tools/rg_sanity.py` v2.0 | [TENSION ALERT] non-zero; requires 2-loop for cancellation | Falsified if 2-loop calculation yields β_{λ_S} ≠ 0 at canonical values |
| C-AT-04 | UV Yukawa sector can generate κ=0.5 naturally | y ~ 0.8 for M_F = Λ_UV; perturbative (y < 4π) | [D] | III | `tools/uv_matching.py` v1.0, Sector 1 scan | PLAUSIBLE | Falsified if no UV completion with y<4π and M_F<10·Λ_UV yields κ=0.5 |
| C-AT-05 | UV Scalar Portal sector can generate κ=0.5 naturally | μ/M_Φ = 1.0 for λ_Φ = κ = 0.5; maximally natural | [D] | III | `tools/uv_matching.py` v1.0, Sector 2 scan | PLAUSIBLE | Falsified if portal coupling requires μ/M_Φ > 10 or < 0.01 |
| C-AT-06 | Stueckelberg sector: N_eff ~ 16 for e_S = π | N_eff = 16π²κ/e_S² ≈ 16 at e_S=π | [D] | III | `tools/uv_matching.py` v1.0, Sector 3 scan | MARGINAL | Falsified if spectrum cannot accommodate N_eff ~ O(10) anomaly contributors |
| C-AT-07 | Parametric f_n (Exponential family) reproduces ρ_obs for self-consistent a₀(g) | ρ_ratio = 1.0 by construction; Δ_FT quantified | [D] | III | `tools/vacuum_suppression.py` v2.0, Family A | CONSTRUCTED — not prediction | Falsified if explicit f_n from CLAIMS_ADDENDUM disagrees with any family |
| C-AT-08 | Barbieri-Giudice Δ_FT for vacuum suppression is large (> 10²) | Δ_FT ~ O(10²–10³) for g ∈ [0.5, 2.0], all families | [D] | III | `tools/vacuum_suppression.py` v2.0 | [TENSION ALERT] significant fine-tuning | Falsified only if Δ_FT < 10 demonstrated for physically motivated f_n |
| C-AT-09 | L1: 10¹⁰ geometric factor remains unexplained | Open issue from CONSTANTS.md | — | — | `CANONICAL/CONSTANTS.md` v3.9.5, L1 | OPEN | Cannot be closed until f_n explicitly derived from first principles |
| C-AT-10 | L4: γ=16.339 not derived from RG first principles | Algebraic closed-form gives γ ≈ 1.908 ≠ 16.339 | — | — | `CANONICAL/CONSTANTS.md` v3.9.5, L4 | OPEN | Would be resolved by FRG scheme-independent observable reproducing γ |
| C-AT-11 | Toolchain produces reproducible, hash-verified outputs | SHA256 hashes documented in repro_verification.sh | [A] | I | `tools/repro_verification.sh`, `docs/pr-gate/` | PASS | Falsified if re-run with same inputs produces different SHA256 |

---

## One-Command Reproduction

```bash
# From repository root (Python 3.10+, mpmath >= 1.3.0):
bash tools/repro_verification.sh

# Individual scripts:
python tools/claim_audit.py
python tools/rg_sanity.py
python tools/uv_matching.py
python tools/vacuum_suppression.py

# Expected outputs (verification/data/visualizations/):
#   rg_scan_physical.csv         rg_sanity_summary.json
#   uv_matching_scan.csv         uv_matching_summary.json
#   vacuum_suppression_scan.csv  vacuum_suppression_summary.json
#   audit_report.json
```

**Software stack:**
```
Python   >= 3.10
mpmath   >= 1.3.0  (pip install mpmath)
numpy    >= 1.24   (optional, for cross-checks)
```

---

## DOI / arXiv Resolvability

| DOI/arXiv | Status | Used For | Evidence Tag |
|-----------|--------|----------|--------------|
| 10.5281/zenodo.17835200 | Verified | UIDT v3.9 canonical source | [A]–[C] |
| zenodo.org/records/18072470 | Pending external verify | UIDT v3.9 extended | [C]–[D] |
| zenodo.org/records/18740600 | Pending external verify | CLAIMS_ADDENDUM | [D] |
| zenodo.org/records/19228489 | Pending external verify | Latest release | [D] |

> DOIs for CLAIMS_ADDENDUM_C054_C056.md not independently resolvable; f_n definitions cannot be promoted beyond [D] until DOI verified.

---

## Blocker Checklist (required before Merge)

- [ ] **L-β** Physical 1-loop β-functions validated by independent EFT theorist
- [ ] **L-UV** UV matching note or symmetry argument for κ=0.5 deposited as `docs/uv_mechanism_note.md`
- [ ] **L-fn** Explicit f_n(g) definitions extracted from CLAIMS_ADDENDUM_C054_C056.md and committed to `CANONICAL/`
- [ ] **L-ft** Sensitivity / Δ_FT report with physically motivated f_n (not parametric placeholder)
- [ ] **L4** γ=16.339 FRG derivation (TKT-20260403-FRG-NLO) remains open — not blocker for this PR, tracked separately
- [x] Toolchain runs end-to-end with SHA256-verified outputs
- [x] Claims Table complete with all Claim IDs, Evidence Tags, Strata, Falsification Exposure
- [x] One-command reproduction documented

---

## Mandatory Limitations Statement

> Per Space-Direktive §4 and CANONICAL/LIMITATIONS.md:
>
> **L1** (open): 10¹⁰ geometric factor between ρ_calc and ρ_obs is unexplained.  
> **L4** (open): γ = 16.339 is not derived from RG first principles; algebraic closed-form yields γ ≈ 1.908.  
> **L5** (open): N = 99 suppression steps is unjustified.  
> **L-β** (new): 1-loop β-functions derived here are [D]; 2-loop and lattice validation required for [B].  
> **L-UV** (new): No UV completion for κ=0.5 yet demonstrated beyond toy-model plausibility [D].  

All results in this PR are Stratum III interpretations unless explicitly tagged [A] or [C].
