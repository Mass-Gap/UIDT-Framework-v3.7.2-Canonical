# Effective Gap Derivation Dossier

**UIDT Framework:** v3.9 Canonical  
**Purpose:** Clay-facing epistemic correction and hybrid-method documentation  
**Status:** Active, not a formal Clay submission

---

## Boundary Statement

This directory exists to prevent ambiguity between:

1. the internally closed reduced UIDT gap equation [A], and
2. the open pure Yang--Mills existence and mass-gap problem [E boundary].

The hybrid UIDT construction is scientifically useful only if this boundary is kept explicit.

---

## Required Reading Order

1. `docs/theory/effective_gap_derivation.md`
2. `clay-submission/GAP_ANALYSIS_CLAY.md`
3. `docs/predictions/glueball_spectrum.md`
4. `docs/predictions/thermal_vacuum.md`
5. `verification/scripts/verify_effective_gap_predictions.py`

---

## Claims Table

| Claim ID | Claim | Evidence | Stratum | Status |
|---|---|---:|---:|---|
| GAP-REDUCED-001 | Reduced algebraic map has local Banach closure | [A] | III | internally verified |
| GAP-PROJECTION-001 | Effective scalar projection is equivalent to pure Yang--Mills | [E] | III | open |
| GAP-GAMMA-001 | `gamma = 16.339` enters as calibrated kinetic invariant | [A-] | III | calibrated |
| PRED-GB-001 | Tensor-glueball Regge estimate | [D] | III | falsifiable prediction |
| PRED-TH-001 | Thermal screening ansatz | [D] | III | falsifiable prediction |

---

## Reproduction Note

```bash
python verification/scripts/verify_effective_gap_predictions.py
```

No file in this directory may be used to claim that UIDT has solved the Clay Yang--Mills problem.
