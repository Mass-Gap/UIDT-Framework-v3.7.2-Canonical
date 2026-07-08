# SPEC MODULE — Blind Ensemble δ-Measurement for PR-B1-002 (v2, α-linear)

| Field | Value |
|---|---|
| Module ID | `SPEC-DELTA-MEAS-001` |
| Version | **2 — corrected to α-linear noise convention (supersedes v1)** |
| Status | Auditor-verified under the corrected scale. For integration into PR-B1-002. |
| Supersedes | v1 (α² normalization, withdrawn with the HANDOUT-PR-B0.2 unit-mismatch fix) |
| Dependency | PR-B0.2 GATE_REPORT (signed); α-linear noise convention `δ·α·√¾` |
| Evidence ceiling | [D]. Measurement infrastructure; authorizes no claim. |

---

## 1. What this resolves

The δ-convention question is answered by **measurement**, not by setting (PI decision: δ not set a priori). The realized noise floor is read directly from the HMC ensemble, blind to the partition, and the admissible region is looked up from the PR-B0.2 boundary map at that measured δ. This holds the anti-target-leakage line: the detector never sees the target partition, and δ never enters as a tuning knob.

## 2. The measured quantity (corrected, frozen)

For an HMC ensemble of `K` configurations `{X_a^(k)}`, `a=1,2,3`, sampling fluctuations around a condensed background at known coupling `α`:

```
δ_measured  =  mean_{k,a} || X_a^(k) − <X_a> ||_op   /   ( α · sqrt(3/4) )
```

where `<X_a> = (1/K) Σ_k X_a^(k)` is the ensemble mean and **`α·sqrt(3/4)` is the field-amplitude scale** (units of α), matching the corrected injection convention `||noise||_op = δ·α·sqrt(3/4)`.

**Critical correction from v1:** the normalization is `α·sqrt(3/4)` (field-amplitude scale), NOT `α²·(3/4)` (Casimir/energy scale). v1 tied the measurement to the energy scale; under the corrected α-linear injection this would have made the validation δ and the production HMC δ diverge with α. Injection and measurement now use the **same** scale.

Design points, both re-verified under the corrected scale:
- Fluctuation taken around the **ensemble mean** (removes the condensed background regardless of partition -> class-independent).
- Normalization by the **field-amplitude** scale `α·sqrt(3/4)` (matches injection -> α-independent).

## 3. Re-verification results (auditor, under α-linear scale)

| Property | v1 (α²) | v2 (α-linear) |
|---|---|---|
| Faithfulness δ_meas/δ_true | 0.988 | **0.987** |
| Class-independence cv (8 classes) | 0.0012 | **0.0012** |
| **α-independence** (α=1,2,4,8) | not isolated in v1 | **0.987 constant (std 0.0014)** <- key new check |
| K-convergence | K=40->0.0988 | K=40->0.0988, K=80->0.0993 |

The α-independence test is the decisive new verification: under v1's α² scale the estimator coupled to the wrong scale (the same unit mismatch that produced the detector cross-class leak); under the corrected scale the calibration factor is **flat across α=1->8**. Injection and measurement are scale-consistent.

**Recommended K >= 40** for ~1% accuracy; K >= 80 to drive the finite-K bias below 1%. The 1.3% low bias is monotone in K; PI decision (freeze pre-production): apply the 1/0.987 correction to round δ **up** (conservative — a low δ over-states resolution) or leave raw. Auditor recommendation: apply the correction.

## 4. Decorrelation requirement (verified)

The estimator assumes independent samples. HMC configurations are autocorrelated; the ensemble mean is contaminated and the fluctuation norm under-reads δ if raw K is used (verified: at τ_int=20, K=40 reads 35% low). Requirement:

```
K_eff = K / (2·τ_int) >= 40        (τ_int = integrated autocorrelation time of Tr(X_a²)/N)
```

Verified: with `K = 80·τ_int`, δ_measured returns to 0.0987 independent of τ_int. The HMC spec must measure τ_int and size the ensemble accordingly.

## 5. How PR-B1-002 consumes it

```
1. HMC equilibrium ensemble {X_a^(k)} at (α, couplings, T), decorrelated (K_eff >= 40).
2. δ_measured <- Sec. 2 formula (blind, no partition), normalized by α·sqrt(3/4).
3. Look up PR-B0.2 admissible region at the nearest δ-grid point >= δ_measured (conservative).
4. Classify with the frozen grid detector (τ=0.14) ONLY for classes admissible at δ_measured;
   non-admissible classes -> "below detector resolution at the measured noise floor".
5. Primary target (2,3): under the corrected scale it is admissible at δ=0.10 (ρ>=0.1351),
   no longer restricted to δ<=0.05. Reported resolved/unresolved per its PR-B0.2 admissibility
   at the measured δ. A measurement outcome, never engineered.
```

## 6. Anti-target-leakage compliance

- δ measured from the ensemble, never set to favour any partition.
- Measurement receives only `α` (a coupling, class-independent) and raw configurations; no partition literal, no target value, no δ-threshold literal.
- Admissibility lookup is post-hoc against the frozen PR-B0.2 boundary.
- Gatekeeper CI confirms no partition/δ-threshold literal in measurement or lookup paths, and that injection scale `α·sqrt(3/4)` = measurement scale `α·sqrt(3/4)`.

## 7. Reproduction

```
python -m prb1 measure-delta --ensemble <run> --alpha <a>    # δ_measured, normalized by α·sqrt(3/4)
python -m prb1 lookup-region --delta <δ_measured>            # PR-B0.2 boundary lookup
```

Auditor reference (executed, float64): under the corrected scale, δ_meas/δ_true = 0.987 uniformly across 8 classes (cv=0.0012) and across α in {1,2,4,8} (std 0.0014).

## 8. Open items for PR-B1-002 (not this module)

- HMC sampler, action, temperature grid — separate spec, finalized post PR-B0.2 sign-off (now done).
- 1/0.987 finite-K correction — PI choice, freeze pre-production.
- Ensemble decorrelation: K_eff >= 40, τ_int measured (Sec. 4).

---

*v2 by Claude/Opus, advisory capacity. The α-linear correction and its α-independence are auditor-verified. Integration follows the PR-B0.2 sign-off (completed). Authorizes nothing.*
