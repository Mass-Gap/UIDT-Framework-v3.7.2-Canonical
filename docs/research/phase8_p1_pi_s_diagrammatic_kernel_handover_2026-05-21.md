# Phase-8 P1 Pi_S Diagrammatic Kernel — Handover

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-pi-s-diagrammatic-kernel`  
> **Status:** Handover note. No evidence-category promotion.

---

## Objective

Start the actual P1 kernel step after the scale audit in PR #471:

```text
Pi_S(p^2) at p = Delta*
```

This task defines and checks the diagrammatic kernel structures implied by the canonical v3.9 coupling. It does not compute a renormalized self-energy correction.

---

## Files Added

| Path | Purpose |
|---|---|
| `verification/scripts/verify_phase8_p1_pi_s_kernel_structure.py` | Reproducible 80-dps kernel-structure verifier. |
| `docs/research/phase8_p1_pi_s_diagrammatic_kernel_2026-05-21.md` | Research report and claims table. |
| `docs/research/phase8_p1_pi_s_diagrammatic_kernel_handover_2026-05-21.md` | This handover note. |

---

## Main Result

The canonical v3.9 interaction:

```text
L_int = -(kappa/4) S^2 Tr(F F)
```

expanded around `S = v + h` gives:

```text
hFF coefficient   = kappa*v/2
h^2FF coefficient = kappa/4
```

The `hFF` bubble is the relevant momentum-dependent kernel candidate. The `h^2FF` contact term is p-independent at this level and cannot by itself fix the kinetic correction.

---

## Numerical Findings

| Check | Result | Status |
|---|---:|---|
| `Delta_gamma_required = 17/3000` | residual `<1e-70` | PASS |
| Euclidean transverse bubble numerator | non-negative on deterministic grid | structural [D] pass |
| naive dimension-suppressed canonical bubble | too small by `>1000` enhancement factor | [E]/NO-GO |
| self-energy derivation | not obtained | OPEN |

---

## Tension Alert

The canonical v3.9 interaction is quadratic in `S`. The v4.1 audit form is sometimes written as a linear `S Tr(F F)` structure. These forms must not be silently merged. Any later derivation must explicitly state its matching map.

---

## Reproduction Command

```bash
python verification/scripts/verify_phase8_p1_pi_s_kernel_structure.py
```

Expected terminus:

```text
ALL PHASE-8 P1 PI_S KERNEL STRUCTURE CHECKS PASSED
```

---

## Next Required Task

The next step is a regulated integral:

```text
TKT-2026-05-21-phase8-p1-regulated-pi-s-integral
```

Required outputs:

1. regulator definition;
2. subtraction point;
3. derivative `d Pi_S(p^2)/d p^2` or equivalent wave-function correction;
4. residual to `17/3000`;
5. honest NO-GO if no coefficient is derived.

---

## Acceptance Status

`KERNEL STRUCTURE AUDIT COMPLETE / RENORMALIZED SELF-ENERGY STILL OPEN`
