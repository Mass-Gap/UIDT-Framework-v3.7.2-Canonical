# Phase-8 P1 Regulator Comparison — Handover

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-regulator-comparison`  
> **Status:** Handover note. No evidence-category promotion.

---

## Objective

Compare three diagnostic regulators for the same `Pi_S` kernel model under a fixed subtraction point:

```text
y^2 = p^2/Delta*^2 = 1
```

The target remains:

```text
Delta_gamma_required = 17/3000
```

---

## Files Added

| Path | Purpose |
|---|---|
| `verification/scripts/verify_phase8_p1_regulator_comparison.py` | Reproducible 80-dps regulator comparison. |
| `docs/research/phase8_p1_regulator_comparison_2026-05-21.md` | Research report with claims table and no-promotion gate. |
| `docs/research/phase8_p1_regulator_comparison_handover_2026-05-21.md` | This handover note. |

---

## Regulators Compared

| Regulator | Definition |
|---|---|
| smooth exponential | `exp[-(q^2+k^2)]` |
| compact Litim-style | `(1-q^2)(1-k^2) theta(1-q^2) theta(1-k^2)` |
| sharp unit support | `theta(1-q^2) theta(1-k^2)` |

All use the same subtraction point and the same dimension-suppressed matching.

---

## Numerical Policy

```python
from mpmath import mp
mp.dps = 80
```

No `float()`, no `round()`, no mocks.

---

## Result Discipline

- No enhancement factors are fitted.
- No regulator output is promoted beyond [D]/[E].
- Proof-level closure would require residual `<1e-14` and a derivation, not just a numerical hit.
- P1 remains open unless the script and derivation both close.

---

## Reproduction Command

```bash
python verification/scripts/verify_phase8_p1_regulator_comparison.py
```

Expected terminus:

```text
ALL PHASE-8 P1 REGULATOR COMPARISON CHECKS PASSED
```

---

## Next Step

If no regulator closes the gap to `17/3000`, the next task is:

```text
TKT-2026-05-21-phase8-p1-operator-mixing-or-no-go
```

Required output:

1. operator basis;
2. allowed mixings;
3. sign and scaling of the mixing coefficient;
4. no-go if the needed enhancement remains unphysical.

---

## Acceptance Status

`REGULATOR COMPARISON READY / NO EVIDENCE PROMOTION`
