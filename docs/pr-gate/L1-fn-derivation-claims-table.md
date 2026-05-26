# PR-Gate: `feature/L1-fn-derivation`

> Space-Directive §6 — Claims Table mandatory for every scientific change.  
> DOI source: `10.5281/zenodo.17835200`

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source (manuscript) | Status | Falsification Exposure |
|---|---|---|---|---|---|---|---|
| L1-FN-001 | N_eff = 99 RG steps follows from N = 120/log₁₀(γ²) | 99 | [A-] | II (standard RG counting) | Appendix N.1.1, Eq. 291 | **Encoded, not promoted** | γ measurement shifts N |
| L1-FN-002 | Holographic normalization factor is π⁻² | π⁻² ≈ 0.1013 | [C] | III (UIDT cosmological mapping) | Theorem 8.1, Eq. 48–50 | **Calibrated** | Casimir null at 0.66 nm → anchor lost |
| L1-FN-003 | Product π⁻² · ∏ f_n(g) is testable structure | open | [D] | III (scaffold) | Appendix N.1.2, Eq. 292–294 | **Open — scaffold only** | No Casimir/cosmological anchor survives |
| L1-FN-004 | Model A (f_n=1): reproduces plain γ⁻¹² · EW suppression | rho ~ 1e-48 GeV⁴ | [D] | III | J.3 Steps 1–3 | **Scaffold** | n/a — this is the null model |
| L1-FN-005 | Model B (geometric): uniform per-step suppression | prod ~ g^{-2.97} | [D] | III | Remark 8.2 speculation | **Scaffold** | No first-principles justification |
| L1-FN-006 | Model C (sector-decomposed): three physical sectors | QCD/EW/grav blocks | [D] | III | N.1.2 Eq. 292–294 | **Scaffold** | Sector boundaries are an ansatz |
| L1-FN-007 | RG self-consistency |5κ²−3λ_S| < 1e-14 | < 1e-14 | [A] | II | Space-Directive §2 | **Tested in suite** | Violation → [RG_CONSTRAINT_FAIL] |
| L1-FN-008 | L1 limitation: O(10¹⁰) factor remains unresolved | 10¹⁰ | — | III | Sec. 13.1.1, Limitation 13.1 | **Open — NOT resolved here** | Resolution would require dedic. PR + new Evidence [B/C] |

---

## Mandatory Limitations

- **L1**: The O(10¹⁰) geometric scaling factor connecting QCD to cosmological scales has no first-principles derivation.  **This PR does not resolve L1.**  
- **L-β**: Physical 1-loop β-functions from ℒ_UIDT are not derived here.  
- **L4**: γ RG-gap δγ = 0.0047 remains open.  

---

## One-Command Reproduction Note

```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
cd UIDT-Framework-v3.9-Canonical
pip install mpmath
python verification/scripts/derive_fn_vacuum_suppression.py
python -m pytest verification/tests/test_fn_vacuum_suppression.py -v
```

Expected exit: `pytest` all green; script prints `PASS` for RG check and `[TENSION ALERT]` for all three models (they do **not** match observation — this is expected and correct behaviour for scaffold code).

---

## DOI / arXiv Resolvability

| DOI/arXiv | Status | Used for | Evidence Tag |
|---|---|---|---|
| 10.5281/zenodo.17835200 | ✅ Resolves | Primary source — all eq. numbers above | [A-/B/C/D] |
| arXiv:2503.14738 (DESI DR2) | ✅ Resolves | ρ_obs calibration | [C] |
| arXiv:1807.06209 (Planck 2018) | ✅ Resolves | ρ_obs reference value | [C] |

---

## Evidence Promotion Summary

No ledger value is changed.  No Evidence tag is promoted.  
All new code is `[D] scaffold` only.

> **Acceptance condition**: Tests pass, claims table complete, limitations stated, no overclaiming. Physics promotion blocked until independent verification exists.
