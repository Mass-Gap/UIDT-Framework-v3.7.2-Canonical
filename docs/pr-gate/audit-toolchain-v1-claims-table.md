# PR Gate: feature/audit-toolchain-v1 — Claims Table (v3)

> **PR:** [#502](https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical/pull/502)  
> **Branch:** `feature/audit-toolchain-v1`  
> **Date:** 2026-05-24  
> **Compiled by:** Antigravity / UIDT-Assistant v4.1  
> **Patch:** v3 — [AUDIT_FAIL] f_n documented; vacuum_suppression v3; rg_2loop; uv_mechanism_note; Dockerfile

---

## [AUDIT_FAIL] Critical Finding: f_n Definitions Not Found

> **CLAIMS_ADDENDUM_C054_C056** (SHA `3928923c`) contains three emergent-geometry claims
> (gradient bilinear metric seed, information-geometric distance, renormalisation scale μ).
> **No f_n(g) vacuum suppression function definitions are present in any committed file.**
> L1 (10¹⁰ factor) and L5 (N=99 unjustified) remain at evidence level **[E]**.
> Required action: P. Rietz must supply explicit f_n derivation with DOI/arXiv backing.

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source | Status | Falsification Exposure |
|----------|-------|-------|--------------|---------|--------|--------|------------------------|
| C-AT-01 | RG canonical constraint \|5κ²−3λ_S\| < 1e-14 | Residual < 10⁻⁵⁶ (dps=80) | [A] | I | `tools/rg_sanity.py` v2.0, `CANONICAL/CONSTANTS.md` v3.9.5 | PASS | Falsified if residual ≥ 1e-14 at dps=80 with exact κ=1/2 |
| C-AT-02 | Physical 1-loop β_κ at canonical point | β_κ = lf·κ·[4(λ_S+κ²)−g₃²N_c]; zero iff g₃²≈1.46 GeV² | [D] | III | `tools/rg_sanity.py` v2.0 | [TENSION ALERT] g₃² self-consistency required | Falsified if lattice g₃² at μ=m_S excludes value giving β_κ=0 |
| C-AT-03 | Physical 1-loop β_λ at canonical point | Non-zero at 1-loop; 2-loop partial cancellation expected | [D] | III | `tools/rg_sanity.py` v2.0 | [TENSION ALERT] | Falsified if 2-loop gives β_λ=0 or confirmed non-zero |
| C-AT-04 | 2-Loop β_κ at canonical values | β_κ^(2) = lf²·κ·[−48κ²λ_S+32λ_S²−12κ²g₃²N_c+3g₃⁴N_c²] | [D] | III | `tools/rg_2loop.py` v1.0 | COMPUTED | Falsified by independent diagrammatic 2-loop calculation |
| C-AT-05 | 2-Loop β_λ at canonical values | β_λ^(2) = lf²·[−144λ_S³+96λ_Sκ⁴−24κ⁶dim_F−24λ_S²g₃²N_c] | [D] | III | `tools/rg_2loop.py` v1.0 | COMPUTED | Same; regression test PASS (phi^4 limit) |
| C-AT-06 | 2-Loop canonical point stability | Eigenvalues of stability matrix at (κ,λ_S)=(0.5,5κ²/3) | [D] | III | `tools/rg_2loop.py` v1.0 | COMPUTED [D] | Falsified if independent diagrammatic calc yields opposite sign |
| C-AT-07 | UV Yukawa: κ=0.5 natural for N_f=10, y~0.72 | y²=16π²κM_F/(N_f T_F Λ_UV); Δ_FT=2 | [D] | III | `tools/uv_matching.py` v1.0, `docs/uv_mechanism_note.md` | PLAUSIBLE | Falsified if no perturbative Yukawa (y<4π) found |
| C-AT-08 | UV Scalar Portal: κ=0.5 natural for λ_Φ=κ | μ/M_Φ=1.0 for λ_Φ=0.5; Δ_FT~O(1) | [D] | III | `tools/uv_matching.py` v1.0 | PLAUSIBLE | Falsified if hierarchy μ/M_Φ > 10 required |
| C-AT-09 | Discrete Shift Symmetry: κ as anomaly coefficient | κ = g₃²T_R N_species/(16π²); N_species~36 for T_R=1/2 | [D] | III | `docs/uv_mechanism_note.md` Mechanism 1 | PLAUSIBLE | Falsified if no Z_N-consistent spectrum with N_species~36 exists |
| C-AT-10 | Vacuum suppression parametric Δ_FT | Δ_FT ~ O(10²–10³) for all families, g∈[0.5,2.0] | [D] | III | `tools/vacuum_suppression.py` v3 | [TENSION ALERT] large FT | Falsified only if Δ_FT<10 for physically motivated f_n |
| C-AT-11 | [AUDIT_FAIL] f_n not found in CLAIMS_ADDENDUM | C054–C056 are emergent-geometry claims; no f_n present | — | — | `LEDGER/CLAIMS_ADDENDUM_C054_C056.md` SHA `3928923c` | OPEN — author action required | Resolved when explicit f_n derivation committed with DOI |
| C-AT-12 | L1: 10¹⁰ geometric factor unexplained | Open since CONSTANTS.md v3.9.5 | — | — | `CANONICAL/CONSTANTS.md` L1 | OPEN [E] | Closed only by first-principles derivation of f_n |
| C-AT-13 | L5: N=99 steps unjustified | Open since CONSTANTS.md v3.9.5 S1-02 | — | — | `CANONICAL/CONSTANTS.md` L5 | OPEN [E] | Closed by physical derivation of step count |
| C-AT-14 | Toolchain SHA256-verified reproducible | Docker + repro_verification.sh | [A] | I | `Dockerfile`, `tools/repro_verification.sh` | PASS | Falsified if re-run yields different SHA256 |

---

## Blocker Checklist

- [ ] **L-fn** [AUDIT_FAIL] Explicit f_n(g) definitions — **HARD BLOCKER** — author action required
- [ ] **L-ft** Δ_FT with physically motivated f_n (not parametric) — blocked by L-fn
- [x] **L-β** 1-loop β physical derivation hinterlegt (`tools/rg_sanity.py` v2)
- [x] **2-loop** 2-loop β implemented + regression test (`tools/rg_2loop.py` v1)
- [x] **L-UV** UV mechanism note with 3 mechanisms + O(1) benchmarks (`docs/uv_mechanism_note.md`)
- [x] Toolchain SHA256-verified (Dockerfile + repro_verification.sh)
- [x] Claims Table v3 complete (14 claims, all Evidence Tags + Falsification Exposure)
- [ ] **Review** Independent RG reviewer + Lattice reviewer assigned
- [ ] **L4** γ=16.339 FRG derivation (TKT-20260403-FRG-NLO) — separate track

---

## One-Command Reproduction

```bash
# Docker (exact environment):
docker build -t uidt-audit . && docker run --rm uidt-audit

# Local (Python 3.11+, mpmath==1.3.0):
bash tools/repro_verification.sh

# Individual scripts:
python tools/claim_audit.py
python tools/rg_sanity.py
python tools/rg_2loop.py
python tools/uv_matching.py
python tools/vacuum_suppression.py --profile parametric --mc-samples 10000
python tools/vacuum_suppression.py --profile extracted    # -> [AUDIT_FAIL] expected

# Expected outputs (verification/data/visualizations/):
#   rg_scan_physical.csv       rg_sanity_summary.json
#   rg_2loop.csv               rg_2loop_summary.json
#   uv_matching_scan.csv       uv_matching_summary.json
#   vacuum_suppression_scan.csv
#   vacuum_mc_summary.csv      (if --mc-samples used)
#   suppression_extracted.json (contains [AUDIT_FAIL] record)
#   audit_report.json
```

**Software stack (pinned):**
```
Python  3.11.9
mpmath  1.3.0
sympy   1.13.3  (optional, for symbolic checks)
```

---

## DOI / arXiv Resolvability

| DOI/arXiv | Status | Used For | Evidence Tag |
|-----------|--------|----------|--------------|
| 10.5281/zenodo.17835200 | Verified | UIDT v3.9 canonical | [A]–[C] |
| zenodo.org/records/18072470 | Pending | UIDT v3.9 extended | [C]–[D] |
| zenodo.org/records/18740600 | Pending | CLAIMS_ADDENDUM | [D] — [AUDIT_FAIL] no f_n found |
| zenodo.org/records/19228489 | Pending | Latest release | [D] |

> No verified DOI/arXiv source for f_n definitions.
> Claim C-AT-11 cannot be promoted until explicit derivation with DOI is committed.

---

## Mandatory Limitations Statement

> **L1** (open [E]): 10¹⁰ geometric factor unexplained — f_n undefined.  
> **L4** (open): γ=16.339 not derived from RG first principles.  
> **L5** (open [E]): N=99 suppression steps unjustified.  
> **L-fn** ([AUDIT_FAIL]): f_n not found in CLAIMS_ADDENDUM_C054_C056.  
> **2-loop coefficients**: operator-topology derivation [D]; diagrammatic verification required.  
> All results in this PR are Stratum III [D] unless explicitly tagged [A] or [C].
