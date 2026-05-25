# Phase-8 P1 Delta-Gamma Self-Energy Scale Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-20-phase8-p1-delta-gamma-self-energy`  
> **Stacked on:** PR #467 → PR #461 → PR #460 → PR #459  
> **DOI:** `10.5281/zenodo.17835200`  
> **Status:** First P1 physics audit after cleanup. No evidence-category promotion.

---

## 1. Objective

The corrected Phase-8 P1 target is:

```text
Delta_gamma_required = gamma - gamma_bare = 16.339 - 49/3 = 17/3000
```

with:

```text
gamma = 16.339      [A-]
gamma_bare = 49/3  [D]
```

This audit asks whether simple perturbative self-energy scale structures can plausibly generate the required correction before a full diagrammatic `Pi_S(p^2)` computation is attempted.

This is not a derivation. It is a fail-fast scale audit.

---

## 2. Stratum Separation

### Stratum I — Empirical / Canonical Inputs

| Quantity | Value | Evidence |
|---|---:|---|
| `Delta*` | `1.710 GeV` | [A] |
| `gamma` | `16.339` | [A-] |
| `E_T` | `2.44 MeV` | [C] |
| `alpha_s_ref` | `0.326` | [D] audit input, not a promoted external measurement |

### Stratum II — Standard QFT Context

The audit uses standard perturbative normalization units:

```text
alpha_s/(4*pi)
alpha_s^2/(16*pi^2)
```

and SU(3) color quantities:

```text
C_A = 3
C_F = 4/3
d_A = 8
```

These are standard group-theory quantities. Their use here is a scale audit, not a complete self-energy calculation.

### Stratum III — UIDT Interpretation

All candidate mappings from these factors to `Delta_gamma_required` are [D]/[E] until an explicit `Pi_S(p^2)` derivation exists.

---

## 3. Numerical Results

At local `mp.dps = 80`:

```text
Delta_gamma_required = 0.0056666666666666666666666666666666666666666666666666666666666666666666666666666838
```

Residual to `17/3000`:

```text
1.7180488210608493317e-80
```

### 3.1 Required coefficients

For a one-loop normalization:

```text
Delta_gamma = C * alpha_s/(4*pi)
```

with `alpha_s = 0.326`, the required coefficient is:

```text
C = 0.21843384503487314950...
```

This coefficient is not a simple positive SU(3) color factor from the tested list.

For a two-loop normalization:

```text
Delta_gamma = C * alpha_s^2/(16*pi^2)
```

the required coefficient is:

```text
C = 8.42000199824452540028...
```

This is close to `d_A = 8` but not equal.

---

## 4. Attempt Register

### Attempt A — One-loop unscaled color factors

Tested structures:

```text
1, C_F, C_A, C_A-C_F, d_A, d_A/C_A, d_A/C_F
```

All one-loop candidates overshoot the required correction. The smallest one-loop unit is already:

```text
alpha_s/(4*pi) = 0.02594225572397893973...
```

which is larger than the target:

```text
17/3000 = 0.00566666666666666...
```

**Status:** `NO-GO_SCALE_MISMATCH_E` for simple unscaled one-loop color factors.

### Attempt B — Two-loop unscaled color factors

The two-loop unit is:

```text
alpha_s^2/(16*pi^2) = 0.00067300063204831806...
```

The `d_A = 8` candidate gives:

```text
d_A * alpha_s^2/(16*pi^2) = 0.00538400505638654449...
```

Residual:

```text
0.00028266161028012216...
```

Ratio to required correction:

```text
0.95011853936233138...
```

**Status:** partial scale hit [D], not a derivation.

The `d_A + 1/2 = 8.5` candidate gives a smaller residual:

```text
0.00005383870574403686...
```

but the extra `1/2` is not derived from a diagram. It is therefore a non-promotable fit-like observation [E]/[D-context].

### Attempt C — Threshold-log structures

The threshold logarithm:

```text
log(Delta*/k_T) = 4.02122636322230423...
```

was tested in simple multiplicative and divisive combinations. None provides proof-level closure. The best simple tested log form remains [D]/[E] depending on whether a future diagram supplies the normalization.

### Attempt D — Corrected S4-P1 non-perturbative shift

The staged S4-P1 shift is:

```text
Delta_gamma_S4P1 = 0.00562910631489145085...
```

Residual to the required correction:

```text
0.00003756035177521581...
```

**Status:** partial numerical hit [D], not [A].

---

## 5. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-SE-001 | Required correction remains `17/3000`. | `0.005666666...` | [D] | III | PASS arithmetic | Fails if corrected `gamma_bare` is rejected. |
| P8-P1-SE-002 | Simple one-loop unscaled color factors are too large. | smallest unit `0.025942...` | [E]/NO-GO | III | NO-GO | Overturned only by a derived suppressing coefficient. |
| P8-P1-SE-003 | Required one-loop coefficient is not a simple tested positive color factor. | `C=0.218433845...` | [D] | III | OPEN | Could be derived by an explicit diagram, but not shown here. |
| P8-P1-SE-004 | Two-loop `d_A` scale is near the target. | `0.005384005...` | [D] | III | PARTIAL SCALE HIT | Fails if a true self-energy diagram gives different sign/scale. |
| P8-P1-SE-005 | `d_A+1/2` improves residual but is not derived. | residual `5.3839e-5` | [E]/fit-risk | III | NOT PROMOTABLE | Requires diagrammatic origin for the `1/2`. |
| P8-P1-SE-006 | S4-P1 remains the closest staged partial hit. | residual `3.7560e-5` | [D] | III | PARTIAL HIT | Fails if regulator-independence test fails. |

---

## 6. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_delta_gamma_self_energy.py
```

Expected terminus:

```text
ALL PHASE-8 P1 DELTA-GAMMA SELF-ENERGY SCALE CHECKS PASSED
```

---

## 7. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| PR #459 | open / draft | corrected Phase-8 assumptions | [D] context |
| PR #460 | open / draft | prior delta-gamma/SU(4) audit | [D] context |
| PR #467 | open / draft | cleanup and alignment precondition | process context |
| arXiv `hep-th/0103195` | verified search result | optimized regulator context | no claim promotion |
| arXiv `hep-lat/0404008` | verified search result | future SU(N)/SU(4) lattice comparison | no [B] claim here |

No external source is used to promote the P1 result. The present PR is an internal scale audit.

---

## 8. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Citation hallucination | No DOI invented; only project DOI and verified arXiv IDs used. |
| Evidence inflation | All new physics claims remain [D]/[E]. |
| Proof-language overreach | No result is called a proof or derivation. |
| Hidden fitting | `d_A+1/2` explicitly marked fit-risk / not promotable. |
| Numerical brittleness | Uses `from mpmath import mp`; local `mp.dps = 80`; residual gates. |
| Strata mixing | Inputs, standard context, and UIDT interpretation separated. |
| Symbol collision | Uses `k_T`, not ambiguous `k_crit`. |
| No-go documentation | One-loop color factors documented as no-go scale mismatch. |

---

## 9. Result

`P1 SCALE AUDIT COMPLETE / SELF-ENERGY DERIVATION STILL OPEN`

The audit does not solve P1. It narrows the next calculation:

1. Simple one-loop color-factor structures are not sufficient.
2. A two-loop or non-perturbative normalization is more plausible by scale.
3. The exact source of the required correction remains uncomputed.
4. The next task must be an explicit `Pi_S(p^2)` diagrammatic or FRG calculation, not another coefficient scan.

---

## 10. Next Logical Step

Open a follow-up derivation task:

```text
TKT-2026-05-21-phase8-p1-pi-s-diagrammatic-kernel
```

Required output:

- symbolic definition of the scalar-gluon mixed kernel;
- sign of the correction;
- scale dependence at `p=Delta*`;
- residual to `17/3000`;
- honest NO-GO if the coefficient cannot be derived.
