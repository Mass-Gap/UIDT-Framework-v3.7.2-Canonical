# Phase-8 P1 BMW/Dyson/FRG Flow Projection Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-26  
> **Branch:** `TKT-2026-05-26-phase8-p1-bmw-dyson-flow-projection`  
> **Stacked on:** PR #498 → PR #495 → PR #487 → PR #481 → PR #480 → PR #473 → PR #471 → PR #467 → PR #461 → PR #460 → PR #459  
> **Status:** Bounded flow-projection audit. No evidence-category promotion.

---

## 1. Objective

This branch performs the first explicit BMW/Dyson/FRG flow-projection diagnostic after the operator-mixing scaffold.

Target:

```text
Delta_gamma_required = gamma - 49/3 = 17/3000
```

with:

```text
gamma = 16.339      [A-]
gamma_bare = 49/3  [D]
```

The task is to define an explicit regulator, subtraction point, flow kernel, projection onto `O_K`, reduced mixing submatrix, coefficient bound, and residual to `17/3000`.

This is not a proof of `gamma`. It is a bounded diagnostic.

---

## 2. Regulator and Subtraction Scheme

The diagnostic regulator is a dimensionless Litim single-scale form:

```text
R_k(q) = Z_A (k^2 - q^2) theta(k^2 - q^2)
```

with:

```text
k = Delta*
p^2 = Delta*^2
subtraction point: y^2 = p^2/k^2 = 1
```

The internal single-scale weight is:

```text
G_k(q)^2 partial_t R_k(q) = 2 / (1 + mu_IR^2)^2
```

inside `q^2 < k^2`, and zero outside. Anomalous-dimension feedback is omitted in this bounded diagnostic and must be supplied by a later full BMW calculation.

---

## 3. Flow Projection

The projection target is:

```text
O_K = 1/2 (partial h)^2
```

The diagnostic projection is:

```text
partial_t Z_h = P_K[partial_t Gamma_k]
```

implemented as:

```text
P_K[Gamma_hh^(2)] = d/dp^2 Gamma_hh^(2)(p^2) |_{p^2 = Delta*^2}
```

The schematic BMW/Dyson channel is:

```text
Gamma_hAA * G_AA * (partial_t R_k) * G_AA * Gamma_hAA
```

with contact/subtraction channels separated.

---

## 4. Reduced Operator-Mixing Submatrix

| Source | Target | Status |
|---|---|---|
| `O_hFF x O_hFF` | `O_K` | computed diagnostic [D] |
| `O_h2FF` | `O_K` | zero direct kinetic role at one contact insertion |
| `O_dh2FF` | `O_K` | undetermined; requires external matching |

This is not a full operator-mixing matrix. It is the minimal submatrix needed for the P1 projection gate.

---

## 5. Coefficient and Residual Gate

The model coefficient is:

```text
Delta_gamma_model = d_A * alpha_s^2 * (kappa*v/Delta*)^2 * projected_flow
```

where `projected_flow = dJ/dy^2` under the diagnostic Litim single-scale kernel.

Classification rule:

| Residual to `17/3000` | Classification |
|---|---|
| `< 1e-14` | proof-level numerical closure still requiring derivation |
| `< 1e-3` | partial [D] scale hit |
| otherwise | [E]/NO-GO for minimal matching |

The verifier reports the signed and absolute result. Sign interpretation remains scheme-dependent for `Delta Z_h`, but the residual controls whether a closure exists.

---

## 6. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-FLOW-001 | Litim single-scale diagnostic regulator is explicit. | `R_k=Z_A(k^2-q^2)theta(k^2-q^2)` | [D] | III | pass | Full BMW anomalous-dimension feedback may change result. |
| P8-P1-FLOW-002 | Subtraction point is fixed. | `p^2=k^2=Delta*^2` | [D] | III | pass | Different subtraction point must be justified. |
| P8-P1-FLOW-003 | Projection target is `O_K`. | `d Gamma_hh^(2)/dp^2` | [D] | III | pass | No P1 closure without kinetic projection. |
| P8-P1-FLOW-004 | Reduced mixing submatrix is defined. | three channels | [D] | III | bounded diagnostic | Full matrix may add channels. |
| P8-P1-FLOW-005 | Minimal Litim single-scale coefficient is computed/bounded. | script output | [D]/[E] | III | diagnostic | Fails if full BMW flow supplies large derived enhancement. |
| P8-P1-FLOW-006 | No evidence promotion follows from this branch. | — | process | III | enforced | Separate Guardian-gated proof would be required. |

---

## 7. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_bmw_dyson_flow_projection.py
```

Expected terminus:

```text
ALL PHASE-8 P1 BMW/DYSON/FRG FLOW PROJECTION CHECKS PASSED
```

---

## 8. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| DOI `10.1016/j.physrep.2021.01.001` / arXiv `2006.04853` | verified via scholar search | non-perturbative FRG/BMW context | no UIDT claim promotion |
| arXiv `hep-th/0103195` | verified | optimized/Litim regulator context | no UIDT claim promotion |
| PR #498 | open / draft | BMW/Dyson/FRG scaffold | [D]/[E] context |
| PR #495 | open / draft | P1 synthesis baseline | [D]/[E] context |

---

## 9. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Citation hallucination | DOI/arXiv sources verified; irrelevant search results not used. |
| Evidence inflation | All new conclusions remain [D]/[E]. |
| Proof-language overreach | No derivation of `gamma` is claimed. |
| Hidden fitting | No enhancement factor is tuned. |
| Regulator ambiguity | `R_k` is explicit. |
| Subtraction ambiguity | `p^2=k^2=Delta*^2` is explicit. |
| Operator ambiguity | Reduced submatrix and projection target are explicit. |
| Precision context | Verifier uses `from mpmath import mp`, local `mp.dps=80`. |
| No-go honesty | Minimal result is classified by residual gate. |

---

## 10. Acceptance Status

`FLOW PROJECTION AUDIT COMPLETE / FULL BMW DERIVATION STILL OPEN`

This branch performs the first bounded flow-projection calculation. If the residual does not close, the correct conclusion is a no-go for the minimal Litim single-scale matching, not a failure to tune.
