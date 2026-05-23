# Phase-8 P1 Operator-Mixing / No-Go Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-operator-mixing-or-no-go`  
> **Stacked on:** PR #481 → PR #480 → PR #473 → PR #471 → PR #467 → PR #461 → PR #460 → PR #459  
> **Status:** Operator-mixing audit. No evidence-category promotion.

---

## 1. Objective

This audit follows the regulator-comparison task. It asks whether the missing enhancement in the P1 self-energy path can be attributed to an allowed operator mixing rather than to an arbitrary fit.

The target remains:

```text
Delta_gamma_required = 17/3000
```

This audit does not derive the correction. It classifies the operator basis and quantifies the required mixing scale.

---

## 2. Operator Basis

The canonical v3.9 interaction is:

```text
L_int = -(kappa/4) S^2 Tr(F F)
```

After `S=v+h`, the relevant operators are:

| Operator | Dimension | Role | Direct kinetic mixing? |
|---|---:|---|---|
| `O_K = 1/2 (partial h)^2` | 4 | scalar kinetic term | yes |
| `O_M = 1/2 h^2` | 2 | scalar mass term | no |
| `O_F = Tr(F F)` | 4 | gauge kinetic operator | no direct h kinetic mixing |
| `O_hFF = h Tr(F F)` | 5 | two-vertex bubble channel | indirect via loop |
| `O_h2FF = h^2 Tr(F F)` | 6 | contact/tadpole channel | not direct at one insertion |
| `O_dh2FF = (partial h)^2 Tr(F F)` | 8 | higher-dimensional kinetic mixing | yes after background/matching |

The `O_hFF x O_hFF -> O_K` channel is allowed as a loop-induced wave-function channel, but it requires a regulator and matching prescription. The `O_h2FF` contact term is p-independent at this level and is not a direct source of `Delta_gamma`.

---

## 3. Quantitative Mixing Requirement

Using the same conservative dimension-suppressed prefactor as the regulated integral audits:

```text
canonical_prefactor = d_A * alpha_s^2 * (kappa*v/Delta*)^2
```

The required order-one derivative-kernel mixing is:

```text
M_required = Delta_gamma_required / canonical_prefactor
```

The verifier shows:

```text
M_required > 4*pi
M_required < 16*pi^2
```

Thus the required mixing is already beyond a conservative perturbative `4*pi` audit bound. It is not automatically impossible, but it is not a natural order-one perturbative coefficient.

Using the smooth-regulated derivative from the previous audit, the required enhancement is even larger:

```text
enhancement_required_smooth > 16*pi^2
```

This is a no-go for the minimal smooth-regulated model unless a non-perturbative matching factor is derived.

---

## 4. Sign and Scaling

The `O_hFF x O_hFF` bubble channel can have a sign compatible with a wave-function correction depending on the renormalization convention, but the sign is not sufficient. The magnitude is the limiting issue.

Scaling summary:

| Channel | Scaling | Status |
|---|---|---|
| `O_hFF x O_hFF -> O_K` | loop-induced, dimension-suppressed by `(kappa*v/Delta*)^2` | allowed [D], too small in minimal model |
| `O_h2FF -> O_K` | single contact insertion | not direct at this level |
| `O_dh2FF -> O_K` | higher-dimensional explicit kinetic mixing | possible only if new matching is derived |
| arbitrary enhancement | fit | not allowed |

---

## 5. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-MIX-001 | The minimal operator basis is explicitly classified. | six operators | [D] | III | pass | Fails if canonical interaction changes. |
| P8-P1-MIX-002 | `O_hFF x O_hFF -> O_K` is allowed but requires matching. | allowed loop channel | [D] | III | open | Requires explicit regulator/matching derivation. |
| P8-P1-MIX-003 | `O_h2FF` contact is not a direct kinetic correction at one insertion. | p-independent | [D] | III | no-go for direct kinetic role | Regulator tadpoles may affect mass-like terms. |
| P8-P1-MIX-004 | Required order-one derivative-kernel mixing exceeds `4*pi`. | `M_required > 4*pi` | [E]/NO-GO warning | III | unnatural perturbative scale | Overturned only by derived non-perturbative enhancement. |
| P8-P1-MIX-005 | Smooth-regulated enhancement exceeds `16*pi^2`. | `>16*pi^2` | [E]/NO-GO | III | no-go for minimal smooth model | Requires derived matching, not tuning. |
| P8-P1-MIX-006 | P1 remains open. | — | [D] | III | open | Needs a controlled operator-mixing derivation. |

---

## 6. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_operator_mixing_no_go.py
```

Expected terminus:

```text
ALL PHASE-8 P1 OPERATOR-MIXING / NO-GO CHECKS PASSED
```

---

## 7. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| PR #481 | open / draft | regulator comparison context | [D] context |
| PR #480 | open / draft | smooth regulated integral context | [D]/[E] context |
| PR #473 | open / draft | kernel-structure context | [D] context |
| arXiv `hep-th/0103195` | verified | regulator context | no UIDT claim promotion |

No external source is used to promote the P1 operator-mixing result.

---

## 8. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Evidence inflation | All results remain [D]/[E]. |
| Hidden fitting | Required enhancement is not inserted as a solution. |
| Proof-language overreach | No derivation of `gamma` is claimed. |
| Operator confusion | Contact and kinetic channels are separated. |
| Precision context | `from mpmath import mp`; local `mp.dps = 80`. |
| No-go honesty | Minimal perturbative/mixing route is flagged as no-go unless matching is derived. |

---

## 9. Result

`OPERATOR-MIXING NO-GO FOR MINIMAL MODEL / P1 STILL OPEN`

The operator basis does not yield a natural perturbative explanation for `Delta_gamma_required = 17/3000`. The only remaining plausible route in this branch is a derived non-perturbative matching or a different physical operator, neither of which is established here.

---

## 10. Next Logical Step

The next step is a Phase-8 P1 synthesis/no-go summary, not another local model variant:

```text
TKT-2026-05-21-phase8-p1-synthesis-no-go-summary
```

Required output:

1. summarize P1 scale audit, kernel audit, regulated integral, regulator comparison, and operator-mixing audit;
2. state which paths are excluded;
3. state which path remains open;
4. update roadmap without evidence promotion.
