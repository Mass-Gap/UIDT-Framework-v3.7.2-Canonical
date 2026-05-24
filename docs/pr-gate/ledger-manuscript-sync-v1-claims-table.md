# PR-Gate: `feature/ledger-manuscript-sync-v1`

> Manuscript/ledger synchronisation for λ_S, N=99 ladder, and C-017/C-018/C-039/C-046/C-052.  
> No numerical values changed beyond rationalising existing identities.

---

## Claims Table

| Claim ID | Claim | Value | Evidence Tag | Stratum | Source (manuscript/notes) | Status | Falsification Exposure |
|---|---|---|---|---|---|---|---|
| UIDT-C-006 | Self-coupling λ_S = 5κ²/3 = 5/12 ≈ 0.41̄6̄ | 5/12 | [A] | II | OPEN_QUESTIONS_GEOMETRY.md, Eq. (RG identity) | **Code synchronized** — scripts now use 5/12 exact | Any script using 0.417 hard-coded violates RG identity |
| UIDT-C-017 | N=99 RG steps from N = 120/log₁₀(γ²) | 99 | [C] | III | Appendix N.1.1, Eq. 291 | **Clarified** — still open derivation, but encoded as scaffold | A first-principles derivation yielding N≠99 |
| UIDT-C-018 | 10¹⁰ geometric factor hierarchical ladder | structured, no closed form | [D] | III | Appendix J.3, N.1.2 | **Scaffold encoded** in derive_fn_vacuum_suppression.py | First-principles ℒ_UIDT derivation or contradiction |
| UIDT-C-039 | N=99 RG ladder as phenomenological scaffold | 99 | [C] | III | Appendix N.1.1, Eq. 291 | **Clarified** — scaffold only | Same as C-017 |
| UIDT-C-046 | N=94.05 cascade baseline | 94.05 | [E] | III | theoretical_notes §12 | **Flagged SUPERSEDED** by Eq. 291; kept historical | A future replacement of Eq. 291 favouring N≠99 |
| UIDT-C-052 | SU(3) Gamma Conjecture γ = (2Nc+1)²/Nc | 49/3 | [E]→[D] (with script) | III | su3_gamma_conjecture_audit.md | **Scaffold script added** — no promotion above [E] in ledger text | Any analytical derivation from ℒ_UIDT yielding γ ≠ 49/3 |

---

## One-Command Reproduction Note

```bash
git clone https://github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical
cd UIDT-Framework-v3.9-Canonical
pip install mpmath

# L1 ladder / λ_S sync
python verification/scripts/derive_fn_vacuum_suppression.py
python -m pytest verification/tests/test_fn_vacuum_suppression.py -v

# SU(3) gamma conjecture scaffold
python verification/scripts/su3_gamma_conjecture_test.py
```

Expected:
- RG check in `derive_fn_vacuum_suppression.py` prints residual = 0.0… | [A]
- `pytest` all green (λ_S=5/12 enforced)
- `su3_gamma_conjecture_test.py` prints γ_SU(3)=49/3 and Δγ ≈ −0.006… w.r.t. canonical γ=16.339.

---

## DOI / arXiv Resolvability

| DOI/arXiv | Status | Used for | Evidence Tag |
|---|---|---|---|
| 10.5281/zenodo.17835200 | ✅ Resolves | Manuscript Eq. 291, J.3, N.1.1–N.1.2, SU(3) remark | [A-/B/C/D] |
| arXiv:1807.06209 (Planck 2018) | ✅ Resolves | ρ_obs reference | [C] |
| arXiv:2501.08217 (Dürr et al. 2025) | ✅ Resolves | χ_top tension context (C-056/C-096) | [C] |

---

## Evidence Promotion Summary

- No Category-A/B value changed.  
- λ_S was already defined as 5/12; this PR only enforces it in scripts and clarifies the CLAIMS notes.  
- C-052 remains a conjecture [E] in narrative, but gains a `[D]`-level scaffold script for reproducibility.

> **Acceptance condition:** Tests pass, scripts use λ_S=5/12 exactly, Claims notes reflect manuscript structure (Eq. 291 & J.3), and no overclaiming is introduced.
