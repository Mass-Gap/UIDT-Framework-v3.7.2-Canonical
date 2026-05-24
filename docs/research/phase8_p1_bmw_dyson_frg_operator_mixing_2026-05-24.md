# Phase-8 P1 BMW/Dyson/FRG Operator-Mixing Scaffold

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-24  
> **Branch:** `TKT-2026-05-24-phase8-p1-bmw-dyson-frg-operator-mixing`  
> **Stacked on:** PR #495 → PR #487 → PR #481 → PR #480 → PR #473 → PR #471 → PR #467 → PR #461 → PR #460 → PR #459  
> **Status:** Scaffold for the next admissible P1 direction. No evidence-category promotion.

---

## 1. Objective

This branch implements the selected next P1 direction from Issue #496:

```text
Option B — BMW/Dyson/FRG operator-mixing calculation
```

The target remains:

```text
Delta_gamma_required = gamma - 49/3 = 17/3000
```

This document does not derive the correction. It defines the operator basis, projection target, required matching strength, and the minimum outputs required for a later controlled BMW/Dyson/FRG calculation.

---

## 2. Operator Basis

The minimal basis for the P1 projection is:

| Operator | Dimension | Role | Projects to `O_K`? |
|---|---:|---|---|
| `O_K = 1/2 (partial h)^2` | 4 | scalar kinetic operator | yes |
| `O_M = 1/2 h^2` | 2 | scalar mass operator | no |
| `O_F = Tr(F F)` | 4 | gauge kinetic operator | no |
| `O_hFF = h Tr(F F)` | 5 | loop-induced scalar-gauge vertex | indirect |
| `O_h2FF = h^2 Tr(F F)` | 6 | contact / tadpole sector | not directly |
| `O_dh2FF = (partial h)^2 Tr(F F)` | 8 | higher-dimensional kinetic mixing | yes after matching |

The projection target is:

```text
O_K = 1/2 (partial h)^2
```

The BMW/Dyson/FRG task must compute or bound the flow contribution to this operator.

---

## 3. Projection Object

The future derivation must supply a controlled expression of the form:

```text
partial_t Z_h = P_K[partial_t Gamma_k]
```

or equivalently a Dyson/proper-vertex projection:

```text
Delta Z_h = d/dp^2 Gamma_hh^(2)(p^2) |_{p^2 = Delta*^2}
```

The relevant schematic channel is:

```text
Gamma_hAA * G_AA * G_AA * Gamma_hAA + contact/subtraction terms
```

with projection onto `O_K`.

This branch does not pretend that the projection has already been evaluated.

---

## 4. Quantitative Gate

Using the same canonical scale factors from the P1 no-go stack:

```text
canonical_prefactor = d_A * alpha_s^2 * (kappa*v/Delta*)^2
```

one needs:

```text
required_projected_flow_strength = Delta_gamma_required / canonical_prefactor
```

The verifier checks:

```text
required_projected_flow_strength > 4*pi
required_projected_flow_strength < 16*pi^2
```

Using the smooth-regulated derivative reference from PR #480, the required matching enhancement exceeds:

```text
16*pi^2
```

Therefore the later BMW/Dyson/FRG calculation must derive a genuinely non-perturbative matching effect or report a no-go.

---

## 5. Required Future Outputs

The next derivation PR must supply:

| Output | Required content |
|---|---|
| `regulator_Rk` | explicit regulator and scheme |
| subtraction point | default `p^2 = Delta*^2`, unless justified otherwise |
| projection | `d/dp^2 Gamma_hh^(2)` or `P_K[partial_t Gamma_k]` |
| operator-mixing matrix | at least the subspace containing `O_K`, `O_hFF`, `O_h2FF`, `O_dh2FF` |
| non-perturbative matching | computed coefficient or upper/lower bound |
| residual | comparison to `17/3000` |
| no-go gate | explicit if coefficient cannot close naturally |

---

## 6. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-BMW-001 | Option B is the selected next P1 path. | BMW/Dyson/FRG operator mixing | process | III | selected | Superseded if PI selects another option. |
| P8-P1-BMW-002 | Minimal operator basis for `O_K` projection is defined. | six operators | [D] | III | scaffold pass | Fails if canonical coupling changes. |
| P8-P1-BMW-003 | The future calculation must project onto `O_K`. | `1/2(partial h)^2` | [D] | III | required | No P1 closure without kinetic projection. |
| P8-P1-BMW-004 | Required projected flow strength exceeds `4*pi`. | `>4*pi` | [E]/warning | III | scale warning | Overturned by controlled non-perturbative flow. |
| P8-P1-BMW-005 | Smooth-reference matching enhancement exceeds `16*pi^2`. | `>16*pi^2` | [E]/NO-GO warning | III | no-go for minimal smooth model | Overturned only by derived matching. |
| P8-P1-BMW-006 | No derivation is obtained in this scaffold. | — | [D] | III | open | Requires later BMW/Dyson/FRG computation. |

---

## 7. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_bmw_dyson_frg_operator_mixing.py
```

Expected terminus:

```text
ALL PHASE-8 P1 BMW/DYSON/FRG OPERATOR-MIXING SCAFFOLD CHECKS PASSED
```

---

## 8. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| DOI `10.1016/j.physrep.2021.01.001` / arXiv `2006.04853` | verified context | non-perturbative FRG context | no UIDT claim promotion |
| arXiv `hep-th/0103195` | verified context | optimized-regulator context | no UIDT claim promotion |
| PR #495 | open / draft | P1 synthesis/no-go baseline | [D]/[E] context |
| Issue #496 | open | selected next direction | process context |

No external source is used to promote a UIDT claim.

---

## 9. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Citation hallucination | DOI/arXiv identifiers are listed only as verified context. |
| Evidence inflation | New statements remain [D]/[E] or process. |
| Proof-language overreach | No derivation of `gamma` is claimed. |
| Hidden fitting | Required enhancement is a gate, not a fitted solution. |
| Operator confusion | Projection target `O_K` is explicit. |
| Numerical precision | Verifier uses `from mpmath import mp`; local `mp.dps=80`. |
| No-go honesty | Future no-go condition is explicit. |

---

## 10. Acceptance Status

`BMW/DYSON/FRG SCAFFOLD READY / DERIVATION NOT YET PERFORMED`

This branch prepares the next serious P1 calculation. It does not solve P1 and does not authorize evidence promotion.
