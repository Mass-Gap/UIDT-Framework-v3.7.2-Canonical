# Phase-8 P1 Regulator Comparison Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-regulator-comparison`  
> **Stacked on:** PR #480 → PR #473 → PR #471 → PR #467 → PR #461 → PR #460 → PR #459  
> **Status:** Regulator-comparison audit. No evidence-category promotion.

---

## 1. Objective

This audit compares three diagnostic regulators for the same Euclidean `hFF` bubble model used in the regulated `Pi_S` integral audit.

The target remains:

```text
Delta_gamma_required = 17/3000
```

The comparison uses the same subtraction point:

```text
y^2 = p^2 / Delta*^2 = 1
```

No enhancement factor is fitted. No evidence category is promoted.

---

## 2. Regulator Set

| Regulator | Definition | Status |
|---|---|---|
| smooth exponential | `exp[-(q^2+k^2)]` | diagnostic [D] |
| compact Litim-style | `(1-q^2)(1-k^2) theta(1-q^2) theta(1-k^2)` | diagnostic [D] |
| sharp unit support | `theta(1-q^2) theta(1-k^2)` | diagnostic [D] |

All quantities are dimensionless in units of `Delta*`; `k=q+p`.

The compact regulator is called Litim-style because it uses compact support and polynomial suppression. It is not a full Wetterich-flow implementation.

---

## 3. Shared Kernel and Matching

The kernel is the same transverse Euclidean bubble structure used in PR #473 and PR #480:

```text
V_mu nu(q,k) = (q*k) delta_mu nu - q_nu k_mu
P_mu nu(q) = delta_mu nu - q_mu q_nu/q^2
```

The model diagnostic is:

```text
Delta_gamma_model = d_A * alpha_s^2 * (kappa*v/Delta*)^2 * dJ/dy^2
```

This is a conservative dimension-suppressed matching. It is not a derived physical renormalization prescription.

---

## 4. Expected Classification

The verifier classifies each regulator by the absolute residual:

| Residual condition | Classification |
|---|---|
| `< 1e-14` | numerical closure but derivation still required |
| `< 1e-3` | partial [D] scale hit |
| otherwise | [E]/NO-GO scale mismatch |

Any apparent improvement without a derived matching factor remains non-promotable.

---

## 5. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-RC-001 | Three explicit regulators are compared under one subtraction point. | smooth, compact, sharp | [D] | III | model comparison | Different kernel/matching may change results. |
| P8-P1-RC-002 | No regulator is allowed a tuned enhancement factor. | none fitted | process | III | pass | Any later enhancement must be derived. |
| P8-P1-RC-003 | The comparison uses the same dimension-suppressed matching as PR #480. | `d_A alpha_s^2 (kappa v/Delta*)^2` | [D] | III | diagnostic | Matching remains unproven. |
| P8-P1-RC-004 | Proof-level closure is not obtained in this diagnostic comparison. | residual not `<1e-14` | [E]/NO-GO if all fail | III | expected no-go unless script shows otherwise | Overturned only by reproducible residual closure plus derivation. |
| P8-P1-RC-005 | P1 remains open. | — | [D] | III | open | Requires derived regulator-stable self-energy correction. |

---

## 6. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_regulator_comparison.py
```

Expected terminus:

```text
ALL PHASE-8 P1 REGULATOR COMPARISON CHECKS PASSED
```

---

## 7. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| arXiv `hep-th/0103195` | verified | optimized-regulator context | no UIDT claim promotion |
| PR #480 | open / draft | prior smooth-regulated integral audit | [D] context |
| PR #473 | open / draft | kernel-structure audit | [D] context |

No external source is used to promote a UIDT claim in this PR.

---

## 8. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Citation hallucination | No new DOI/arXiv invented. |
| Evidence inflation | All regulator outputs remain [D]/[E]. |
| Hidden fitting | No enhancement factor is fitted. |
| Regulator ambiguity | Regulator definitions are explicit. |
| Subtraction ambiguity | Same `y^2=1` point used throughout. |
| Numerical precision | `from mpmath import mp`; local `mp.dps = 80`. |
| No-go honesty | Lack of proof-level closure is part of the expected result if residuals fail. |

---

## 9. Acceptance Status

`REGULATOR COMPARISON AUDIT / NO EVIDENCE PROMOTION`

This audit tests scheme sensitivity of the minimal model. It cannot solve P1 unless a regulator-stable, derived, proof-level correction emerges. Under the current model assumptions, P1 is expected to remain open.

---

## 10. Next Logical Step

If all tested regulators remain far below `17/3000`, the next step is not further regulator tuning. The next step is to identify whether the canonical v3.9 operator can produce a non-perturbative matching factor from a controlled FRG/BMW or operator-mixing calculation.

Recommended next task if no regulator closes:

```text
TKT-2026-05-21-phase8-p1-operator-mixing-or-no-go
```

Required output:

1. operator basis;
2. allowed mixings;
3. sign and scaling of the mixing coefficient;
4. no-go if the needed enhancement remains unphysical.
