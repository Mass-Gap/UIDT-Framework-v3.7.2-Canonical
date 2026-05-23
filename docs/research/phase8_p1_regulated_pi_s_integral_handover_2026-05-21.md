# Phase-8 P1 Regulated Pi_S Integral — Handover

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-regulated-pi-s-integral`  
> **Status:** Handover note. No evidence-category promotion.

---

## Objective

Continue the P1 line after the kernel-structure audit by evaluating a minimal regulated Euclidean bubble model for:

```text
Pi_S(p^2) at p = Delta*
```

The target correction remains:

```text
Delta_gamma_required = 17/3000
```

---

## Files Added

| Path | Purpose |
|---|---|
| `verification/scripts/verify_phase8_p1_regulated_pi_s_integral.py` | Reproducible 80-dps smooth-regulated integral audit. |
| `docs/research/phase8_p1_regulated_pi_s_integral_2026-05-21.md` | Research report with regulator, subtraction point, claims table, and no-go result. |
| `docs/research/phase8_p1_regulated_pi_s_integral_handover_2026-05-21.md` | This handover note. |

---

## Regulator and Subtraction

Regulator:

```text
R(q,k) = exp[-(q^2 + k^2)/Delta*^2]
```

Subtraction point:

```text
y^2 = p^2/Delta*^2 = 1
```

Derivative diagnostic:

```text
dJ/dy^2 at y^2 = 1
```

---

## Main Findings

| Quantity | Result | Status |
|---|---:|---|
| `J(1)` | `~0.0016889013` | model diagnostic [D] |
| `dJ/dy^2` | `~-0.0013885307` | sign convention warning [D] |
| `|Delta_gamma_model|` | `~2.3e-7` | far below target |
| required enhancement | `~2.5e4` | fit-risk / no-go |

---

## Interpretation

The minimal smooth-regulated canonical bubble cannot generate `17/3000` under the tested dimension-suppressed matching. The sign of `Delta Z` still requires an explicit renormalization convention, but the magnitude deficit is already decisive for this minimal model.

Status:

```text
REGULATED MODEL NO-GO / P1 STILL OPEN
```

---

## Reproduction Command

```bash
python verification/scripts/verify_phase8_p1_regulated_pi_s_integral.py
```

Expected terminus:

```text
ALL PHASE-8 P1 REGULATED PI_S INTEGRAL CHECKS PASSED
```

---

## Remaining Work

The next task should compare regulator schemes or derive the missing matching factor:

```text
TKT-2026-05-21-phase8-p1-regulator-comparison
```

Required outputs:

1. same subtraction point;
2. smooth exponential, compact/Litim-style, and sharp-cutoff diagnostics;
3. residual table to `17/3000`;
4. no tuning of enhancement factors;
5. no evidence promotion without derived regulator-stable result.

---

## Acceptance Status

`REGULATED MODEL NO-GO / REGULATOR COMPARISON REQUIRED`
