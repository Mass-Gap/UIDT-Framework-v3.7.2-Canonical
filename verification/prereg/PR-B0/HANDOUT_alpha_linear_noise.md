# HANDOUT — PR-B0.2 Correction: α-Linear Noise Convention and Full Boundary Remeasurement

| Field | Value |
|---|---|
| Handout ID | `HANDOUT-PR-B0.2-001` |
| Target executor | Antigravity 2.0 (four-agent structure) |
| Auditor | Claude/Opus — advisory only; cannot sign PI sign-off (`AI_AUDIT_POLICY.md` Sec. 1) |
| Sign-off authority | PI (P. Rietz) only |
| Trigger | Gatekeeper CI found `(2,2,3)→(2,3)` cross-class leak; root cause traced (by Antigravity, confirmed by auditor) to a **unit mismatch in the noise spec authored by Claude/Opus** |
| Status | **DRAFT for PI sign-off. Supersedes the α² noise convention in HANDOFF-PR-B0-001 §2.3, HANDOFF-PR-B0.1-001, and SPEC-DELTA-MEAS-001.** |
| Scope | Green-line: noise-convention fix + full boundary remeasurement + δ-spec correction. No protected-path writes. |
| Evidence ceiling | [D]. Methodological; authorizes no claim. |

---

## 0. Root cause (binding audit record)

The cross-class leak `(2,2,3)→(2,3)` (~6.4% pooled, up to ~29% at α=4) is **not** a physical resolution limit and **not** a pipeline implementation error. The pipeline executed the spec faithfully. The defect is in the **spec**, authored by Claude/Opus:

**The noise amplitude was tied to `Δ_min = α²·¾`, a Casimir/energy scale (units of α²), but the noise lives on `X_a`, a field-amplitude scale (units of α).** Mixing the two scales is a unit mismatch. Antigravity's error-propagation analysis is correct and confirmed by the auditor:

- noise on `X_a` under the old convention scales as `α²`;
- `‖X_a‖` scales as `α`;
- so the Casimir perturbation `ΔC ≈ Σ(X_aΔX_a + ΔX_aX_a)` scales as `α·α² = α³`;
- after the detector's `/α²` normalization, the error in the assignment coordinate `jj` scales as `α`, while the tolerance `τ` is α-constant;
- at large α the n=2 block is pushed past tolerance and dropped, collapsing `(2,2,3)→(2,3)`.

Verified directly (auditor): under the old α² convention the noise/background ratio runs 0.08→0.15→0.30 for α=1,2,4 (the leak grows with α); under the corrected convention it is **constant at 0.09** across α, as a relative fluctuation must be.

**Consequence for prior conclusions (honest correction):** the earlier "UNSAT at δ=0.10" findings for `(2,3)` and the "structurally unresolvable" verdict for `(2,2,2)` were **artifacts of this unit mismatch**, not properties of the model. They are withdrawn.

## 1. The correction (frozen)

**Noise convention (replaces HANDOFF-PR-B0-001 §2.3):**
```
X_a → X_a + (δ · α · √¾) · H_a ,   H_a Hermitian, ‖H_a‖_op = 1 (normalized Wigner).
```
i.e. `‖noise‖_op = δ · α · √¾`, **linear in α** (field-amplitude scale), not `δ·α²·¾`.

**δ definition (replaces SPEC-DELTA-MEAS-001 §2):**
```
δ_measured = mean_{k,a} ‖ X_a^(k) − ⟨X_a⟩ ‖_op  /  ( α · √¾ )
```
normalized by the **field-amplitude** scale `α·√¾`, not the Casimir scale `α²·¾`. This makes injection and measurement use the **same** scale — closing the hidden unit inconsistency that would have made the detector-validation δ and the HMC δ diverge in production.

**Detector and τ:** unchanged (fixed grid, known α, raw multiset, projection). The fix is purely in the noise/δ scale; the detector logic is correct as-is.

## 2. Verified impact (auditor, this session — to be reproduced at production stats)

Recovery at δ=0.10, pooled over the ρ-band and α∈{1,2,4}, old vs new:

| Class | α² (old) | α-linear (new) |
|---|---|---|
| (2,3) primary | 0.84 | **1.00** |
| (2,4) | 0.83 | **1.00** |
| (2,2,3) | 0.87 | **1.00** |
| (2,2,2) | 0.56 | **1.00** |
| (3,3,3) | 0.85 | **1.00** |
| (3,4) | 1.00 | 1.00 |
| (4,4,4) | 0.99 | 1.00 |
| (3,6) | 1.00 | 1.00 |

Three long-standing problems dissolve simultaneously because they shared this single root: the CI leak (now 0% at every α), the `(2,3)` UNSAT (now resolvable at δ=0.10), and the `(2,2,2)` "unresolvable" verdict (now resolvable).

**Discriminating power retained (not trivialized):** the α-linear detector breaks cleanly and class-dependently as δ rises — `(2,2,2)` collapses at δ=0.20, `(2,3)` at δ=0.30, `(3,6)` holds to δ=0.50. The test has a real, physically sensible resolution ceiling; it is simply higher than the artifact-suppressed α² ceiling.

## 3. Remeasurement scope (Antigravity four-agent)

The correction shifts the **entire** boundary `ρ*(δ)`, not just one confusion cell. Therefore the full PR-B0.1 measurement must be **re-run**, not patched.

| Agent | Task |
|---|---|
| **A-impl** | Change the noise injector in `planted_ensemble.py` to `δ·α·√¾·H` (one constant). Change the δ estimator normalization to `/(α·√¾)`. No detector change. |
| **A-cal** | Re-run the τ-sweep under the corrected noise; confirm τ choice and the non-overlap ceiling. (Expect τ stable; verify.) |
| **A-map** | Re-measure `ρ*(δ)` for all 8 classes, δ∈{0.05,0.10,0.20,0.30}, ≥200 trials/cell; emit new admissible regions. |
| **A-audit** | Re-run exact grid + injectivity; **re-run the full confusion matrix** (expect 0% cross-class leak at every α); verify the α-linear scale and the matched injection/measurement normalization via CI; assemble new GATE_REPORT; **green the CI line**; advisory verdict only. |

## 4. Gate (updated pass criteria)

PR-B0.2 passes iff:
1. exact grid + injectivity green;
2. **confusion matrix clean at every α** (no ≥1% cross-class leak) — the specific check that failed before;
3. injection scale `δ·α·√¾` and δ-measurement scale `/(α·√¾)` are identical (no residual unit mismatch) — CI-verified;
4. non-empty admissible region at δ≤0.10 for the target classes (expect all 8 clear, per Sec. 2);
5. τ satisfies the non-overlap ceiling;
6. gatekeeper CI green.

## 5. Reproduction

```
python -m prb0 verify-grid
python -m prb0 verify-injective
python -m prb0 verify-confusion --alpha-sweep        # NEW: per-alpha, not pooled only
python -m prb0 calibrate --noise-scale alpha-linear
python -m prb0 boundary --noise-scale alpha-linear --set P_B0.1
python -m prb0 gate-report
```

Auditor reference (executed, float64): under `δ·α·√¾`, `(2,2,3)→(2,3)` leak is 0% at α∈{1,2,4,8}; all 8 classes recover 1.00 at δ=0.10; noise/background ratio constant at 0.09 across α.

## 6. Downstream documents to update after PR-B0.2 passes

- `HANDOFF-PR-B0-001` §2.3 → α-linear noise.
- `SPEC-DELTA-MEAS-001` §2 → δ normalized by `α·√¾`; re-verify class-independence under the corrected scale (expect cv still ≪0.05).
- `DRAFT_PR-B1-002` §4 → δ lookup uses the corrected scale; the "(2,3) only at δ≤0.05" caveat is **removed** (now resolvable at δ=0.10); outcome table O-C threshold updated to the new measured ceiling.

## 7. Claims table (delta)

| ID | Claim | Class | Falsification / downgrade |
|---|---|---|---|
| B0.2-01 | Noise must scale α-linearly (field amplitude), not α² (energy) | [A] | A physical argument that fluctuations of a coupling-α field scale as α² |
| B0.2-02 | Leak was a unit-mismatch artifact; 0% under corrected scale | [A] | Confusion matrix showing residual leak at any α under corrected scale |
| B0.2-03 | All 8 classes resolvable at δ=0.10 under corrected scale | [B] pending production | Production map below 0.95 for any class |
| B0.2-04 | Detector retains discriminating power (breaks at higher δ) | [B] | A δ where no class fails would indicate trivialization |
| B0.2-05 | Prior (2,3)/(2,2,2) UNSAT verdicts withdrawn as artifacts | [A] | None; superseded by corrected measurement |

## 8. Sign-off block

```
PI sign-off (required before PR-B1-002):        ____________________  date: ________
PR-B0.2 gate verdict (A-audit, advisory):       [ ] satisfiable  [ ] NOT-SATISFIABLE
Noise convention:                               [ ] α-linear (δ·α·√¾) confirmed in code
Injection/measurement scales identical:         [ ] yes
Confusion matrix clean at every α:              [ ] yes
Frozen τ (re-confirmed):                        τ = ____________
Admissible region per class (≥0.95@δ≤0.10):     __________________________________
Gatekeeper CI green:                            [ ] yes   run id: ____________
```

*Drafted by Claude/Opus, advisory capacity. This correction fixes a unit mismatch in the auditor's own prior spec, found by Antigravity's error-propagation analysis and confirmed by direct reproduction. The full boundary is remeasured, not patched, because the correction shifts ρ*(δ) for every class. This handout authorizes nothing; the PI signs.*
