# Phase-8 P1 BMW/Dyson/FRG Operator-Mixing — Handover

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-24  
> **Branch:** `TKT-2026-05-24-phase8-p1-bmw-dyson-frg-operator-mixing`  
> **Status:** Handover note. No evidence-category promotion.

---

## Objective

Create the scaffold for the selected next P1 direction:

```text
BMW/Dyson/FRG operator-mixing calculation
```

This handover records the preparation layer only. It does not claim a derivation of `Delta_gamma_required = 17/3000`.

---

## Files Added

| Path | Purpose |
|---|---|
| `verification/scripts/verify_phase8_p1_bmw_dyson_frg_operator_mixing.py` | Reproducible 80-dps scaffold verifier. |
| `docs/research/phase8_p1_bmw_dyson_frg_operator_mixing_2026-05-24.md` | Scaffold report and claims table. |
| `docs/research/phase8_p1_bmw_dyson_frg_operator_mixing_handover_2026-05-24.md` | This handover note. |

---

## Main Result

```text
BMW/DYSON/FRG SCAFFOLD READY / DERIVATION NOT YET PERFORMED
```

The operator basis, projection target, and required future outputs are defined.

---

## Reproduction Command

```bash
python verification/scripts/verify_phase8_p1_bmw_dyson_frg_operator_mixing.py
```

Expected terminus:

```text
ALL PHASE-8 P1 BMW/DYSON/FRG OPERATOR-MIXING SCAFFOLD CHECKS PASSED
```

---

## Required Next Work

A later derivation PR must supply:

1. explicit regulator `R_k`;
2. subtraction point;
3. projection onto `O_K = 1/2(partial h)^2`;
4. operator-mixing matrix;
5. non-perturbative matching factor or bound;
6. residual to `17/3000`;
7. NO-GO if the coefficient cannot close naturally.

---

## Evidence Status

- `gamma = 16.339` remains [A-].
- `gamma_bare = 49/3` remains [D].
- `Delta_gamma_required = 17/3000` remains [D].
- No [A], [B], or [C] promotion.
- No `LEDGER/CLAIMS.json` mutation.

---

## Acceptance Status

`HANDOVER COMPLETE / P1 DERIVATION STILL OPEN`
