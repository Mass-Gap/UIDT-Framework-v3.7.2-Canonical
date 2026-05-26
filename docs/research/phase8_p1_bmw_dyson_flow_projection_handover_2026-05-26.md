# Phase-8 P1 BMW/Dyson/FRG Flow Projection — Handover

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-26  
> **Branch:** `TKT-2026-05-26-phase8-p1-bmw-dyson-flow-projection`  
> **Status:** Handover note. No evidence-category promotion.

---

## Objective

Perform the first bounded BMW/Dyson/FRG flow-projection diagnostic after PR #498.

Target:

```text
Delta_gamma_required = 17/3000
```

---

## Files Added

| Path | Purpose |
|---|---|
| `verification/scripts/verify_phase8_p1_bmw_dyson_flow_projection.py` | Reproducible 80-dps Litim single-scale flow-projection verifier. |
| `docs/research/phase8_p1_bmw_dyson_flow_projection_2026-05-26.md` | Research report with regulator, projection, submatrix, claims table. |
| `docs/research/phase8_p1_bmw_dyson_flow_projection_handover_2026-05-26.md` | This handover note. |

---

## Regulator and Projection

Regulator:

```text
R_k(q) = Z_A (k^2 - q^2) theta(k^2 - q^2)
```

Subtraction point:

```text
p^2 = k^2 = Delta*^2
```

Projection:

```text
P_K[Gamma_hh^(2)] = d/dp^2 Gamma_hh^(2)(p^2) |_{p^2 = Delta*^2}
```

Target operator:

```text
O_K = 1/2 (partial h)^2
```

---

## Reduced Mixing Submatrix

| Source | Target | Status |
|---|---|---|
| `O_hFF x O_hFF` | `O_K` | computed diagnostic [D] |
| `O_h2FF` | `O_K` | zero direct kinetic role at one contact insertion |
| `O_dh2FF` | `O_K` | undetermined; requires external matching |

---

## Reproduction Command

```bash
python verification/scripts/verify_phase8_p1_bmw_dyson_flow_projection.py
```

Expected terminus:

```text
ALL PHASE-8 P1 BMW/DYSON/FRG FLOW PROJECTION CHECKS PASSED
```

---

## Result Discipline

- No `gamma` derivation is claimed.
- No evidence category is promoted.
- The result is classified by residual to `17/3000`.
- If residual does not close, the conclusion is no-go for the minimal Litim single-scale matching.

---

## Next Work If No Closure

If the diagnostic does not close, the next task should be either:

1. add anomalous-dimension feedback and full BMW vertex dressing; or
2. formalize the no-go for the BMW minimal projection and move toward a rejection/downgrade decision for the `49/3` ansatz.

---

## Acceptance Status

`HANDOVER COMPLETE / FULL BMW DERIVATION STILL OPEN`
