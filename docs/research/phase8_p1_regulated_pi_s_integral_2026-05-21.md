# Phase-8 P1 Regulated Pi_S Integral Audit

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-21  
> **Branch:** `TKT-2026-05-21-phase8-p1-regulated-pi-s-integral`  
> **Stacked on:** PR #473 → PR #471 → PR #467 → PR #461 → PR #460 → PR #459  
> **Status:** Regulated integral audit. No evidence-category promotion.

---

## 1. Objective

This audit continues the P1 line from the diagrammatic-kernel PR. It evaluates a minimal Euclidean regulated `hFF` bubble model and asks whether the resulting wave-function-scale correction can reach:

```text
Delta_gamma_required = 17/3000
```

This is not a derivation of `gamma = 16.339`. It is a regulated no-go / scale test.

---

## 2. Regulator and Subtraction Point

The audit uses a smooth Euclidean exponential regulator:

```text
R(q,k) = exp[-(q^2 + k^2)/Delta*^2]
```

with:

```text
k = q + p
Lambda = Delta*
y^2 = p^2 / Delta*^2
subtraction point: y^2 = 1
finite-difference step: delta y^2 = 0.01
```

The IR denominator uses:

```text
mu_IR = k_T / Delta*
k_T = 4*pi*E_T
```

This is a model regulator. It is not claimed to be regulator-independent.

---

## 3. Kernel Definition

The dimensionless regulated kernel is:

```text
J(y^2) = integral d^4q/(2*pi)^4
         N(q,p) exp[-(q^2+(q+p)^2)]
         /[(q^2+mu_IR^2)((q+p)^2+mu_IR^2)]
```

with the transverse numerator inherited from the previous kernel audit:

```text
N(q,p) = V_{mu nu}(q,q+p) P_mu alpha(q) P_nu beta(q+p) V_alpha beta(q,q+p)
```

and:

```text
V_{mu nu}(q,k) = (q*k) delta_{mu nu} - q_nu k_mu
P_mu nu(q) = delta_mu nu - q_mu q_nu/q^2
```

The wave-function-scale diagnostic is:

```text
dJ/dy^2 at y^2 = 1
```

computed by a symmetric finite difference.

---

## 4. Numerical Result

The verifier gives:

```text
J(1) ≈ 0.0016889012917009859
dJ/dy^2|_{1} ≈ -0.0013885306847083777
```

The sign is convention-sensitive because the translation from `dJ/dy^2` to `Delta Z` depends on the renormalization convention. The audit therefore compares both signed and absolute scales.

The canonical dimension-prefactor model is:

```text
d_A * alpha_s^2 * (kappa*v/Delta*)^2
```

and yields an absolute correction scale around:

```text
|Delta_gamma_model| ≈ 2.3e-7
```

against:

```text
Delta_gamma_required = 5.6666e-3
```

The required enhancement is approximately:

```text
~2.5e4
```

---

## 5. Interpretation

The regulated integral strengthens the no-go result from the previous kernel audit:

1. The kernel is well-defined as a model integral.
2. The derivative has a stable negative sign in this convention.
3. The sign of `Delta Z` still requires an explicit renormalization convention.
4. The magnitude is far too small under the canonical dimension-suppressed matching.
5. Therefore the minimal smooth-regulated canonical bubble does not produce `17/3000`.

Status: [E]/NO-GO for the minimal regulated model as a direct P1 solution.

---

## 6. Claims Table

| Claim ID | Claim | Value | Evidence | Stratum | Status | Falsification Exposure |
|---|---:|---:|---|---|---|---|
| P8-P1-REG-001 | Smooth-regulated model kernel is explicitly defined. | `R=exp[-(q^2+k^2)/Delta*^2]` | [D] | III | PASS model definition | Different regulator may change the result. |
| P8-P1-REG-002 | Subtraction point is fixed at `p^2=Delta*^2`. | `y^2=1` | [D] | III | PASS model definition | Different subtraction point may change the derivative. |
| P8-P1-REG-003 | `dJ/dy^2` is negative in this convention. | about `-0.00138853` | [D] | III | numerical diagnostic | Sign of `Delta Z` depends on renormalization convention. |
| P8-P1-REG-004 | Minimal dimension-suppressed model is too small. | `~2.3e-7` vs `5.666e-3` | [E]/NO-GO | III | NO-GO | Overturned only by derived enhancement/matching. |
| P8-P1-REG-005 | Required enhancement is very large. | about `2.5e4` | [E]/NO-GO | III | fit-risk warning | Any enhancement must be derived, not fitted. |
| P8-P1-REG-006 | P1 remains open. | — | [D] | III | open | Requires regulator-independent or explicitly matched derivation. |

---

## 7. Reproduction Note

Single command:

```bash
python verification/scripts/verify_phase8_p1_regulated_pi_s_integral.py
```

Expected terminus:

```text
ALL PHASE-8 P1 REGULATED PI_S INTEGRAL CHECKS PASSED
```

---

## 8. Verified References

| DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|
| DOI `10.5281/zenodo.17835200` | project DOI | UIDT project identity | n/a |
| arXiv `hep-th/0103195` | verified | optimized regulator / FRG context | no UIDT claim promotion |
| arXiv `hep-lat/0404008` | verified | future SU(N)/SU(4) lattice comparison context | no [B] claim here |
| PR #473 | open / draft | prior kernel-structure audit | [D] context |

---

## 9. AI-Failure Audit

| Failure mode | Check |
|---|---|
| Citation hallucination | No invented DOI/arXiv; external arXiv IDs verified before use. |
| Evidence inflation | Result is [E]/NO-GO or [D] model diagnostic only. |
| Proof-language overreach | No derivation of `gamma` claimed. |
| Hidden fitting | Required enhancement is marked fit-risk, not introduced as a solution. |
| Numerical precision | `from mpmath import mp`; local `mp.dps = 80`. |
| Regulator ambiguity | Regulator and subtraction point explicitly stated. |
| Sign ambiguity | Sign convention warning included. |
| No-go documentation | Minimal regulated model documented as no-go. |

---

## 10. Result

`REGULATED MODEL NO-GO / P1 STILL OPEN`

The minimal smooth-regulated Euclidean bubble cannot generate the required correction under the canonical dimension-suppressed matching. A future path would need a derived non-perturbative matching enhancement, an alternative regulator with justified scheme dependence, or a different physical operator. None is established here.

---

## 11. Next Logical Step

The next task should not tune the enhancement. It should compare regulator schemes or derive the missing matching factor.

Recommended next task:

```text
TKT-2026-05-21-phase8-p1-regulator-comparison
```

Required output:

1. Litim-style compact regulator;
2. smooth exponential regulator;
3. sharp cutoff diagnostic;
4. same subtraction point;
5. residual table to `17/3000`;
6. no evidence promotion unless the result is regulator-stable and derived.
