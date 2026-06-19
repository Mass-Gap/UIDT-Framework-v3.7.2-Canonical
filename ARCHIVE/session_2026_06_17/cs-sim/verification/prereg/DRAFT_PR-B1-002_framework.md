# DRAFT FRAMEWORK — PR-B1-002: Blind HMC Matrix Condensation with Measured Noise Floor

| Field | Value |
|---|---|
| Protocol ID | `PREREG-PR-B1-002` (framework draft) |
| Status | **DRAFT — finalizable. PR-B0.2 signed; depends on the signed PR-B0.2 boundary map and `SPEC-DELTA-MEAS-001` v2 (α-linear).** |
| Supersedes | `PREREG-PR-B1-001` (v1, withdrawn at pilot O5; KDE/observable/projection/noise defects all resolved upstream, incl. the α-linear noise correction PR-B0.2) |
| Auditor | Claude/Opus — advisory only; no merge/sign-off authority |
| Sign-off | PI (P. Rietz) + external counter-signature for any [B]-direction reading |
| Evidence ceiling | [D]. No outcome upgrades ONT-08 or any manuscript claim. |
| Dependencies | (1) PR-B0.2 GATE_REPORT signed ✓; (2) `SPEC-DELTA-MEAS-001` v2 integrated; (3) δ measured, not set (PI decision Option 1) |

---

## 0. What is already settled (do not re-open)

This protocol inherits four resolved upstream findings; none is to be re-litigated here:

1. **Observable:** conservative route — Casimir `Q`, positive-spin block multiset, raw (no gcd). Spin-0 (n=1) blocks are unobservable; the target `[1:2:3]` is tested only as its projection `(2,3)`.
2. **Detector:** fixed-grid assignment with known α (no α-estimation), τ frozen by PR-B0.2 at **0.14**, projection onto the non-kernel subspace.
3. **Admissibility:** the signed PR-B0.2 boundary map `ρ*(δ)` per class (α-linear noise). Under the corrected scale **all 8 classes are admissible at δ=0.10**, including `(2,3)` (ρ≥0.1351) and `(2,2,2)` (ρ≥0.1579). The earlier "(2,3) only at δ≤0.05" and "(2,2,2) unresolvable" findings were α²-unit-mismatch artifacts and are withdrawn.
4. **Noise floor:** measured, not set (`SPEC-DELTA-MEAS-001` v2, α-linear), blind ensemble estimator, class-independent (cv=0.0012), **α-independent (verified α=1→8)**, faithful to ~1%.

## 1. Objective

Simulate matrix condensation thermodynamically, **measure** the realized operator-norm noise floor δ from the equilibrium ensemble, and read out the condensed Wedderburn partition **only where the measured δ places the class inside the PR-B0.2 admissible region**. Determine whether the condensation enters the positive-spin class `(2,3)` — and report honestly "below detector resolution at the measured noise floor" wherever it does not.

This tests Programme Requirement PR-B1 (Appendix B) at the partition-selection level only. It does not test PR-B2 (real structure), the freezing gap, chirality, or any physical identification with `G_SM`.

## 2. Model (to be frozen at finalization)

Primary: the bosonic YMCS / Myers matrix model (the literature-anchored arena of Appendix B §B.2):
```
S[X] = N · Tr( −¼ [X_a,X_b][X_a,X_b] + (2/3) i α ε_abc X_a X_b X_c )
```
Hermitian `N×N` matrices, `a=1,2,3`. Classical extrema are su(2) block backgrounds; the order parameter is the condensed Wedderburn partition. Couplings and the optional mass/double-trace deformation (M1) are frozen at finalization, in the PR-B0.1-admissible ρ-band (Sec. 5).

**Anti-target-leakage (binding):** no partition value, no `(2,3)` literal, and no δ threshold enters the action, the sampler, the initial condition, the stopping rule, or any tuning routine. The CI gatekeeper enforces this on the PR-B1-002 directory.

## 3. HMC sampler (framework)

- Hybrid Monte Carlo, leapfrog, trajectory length and step size auto-tuned during thermalization only (frozen after), acceptance in [0.65, 0.85].
- Thermalization: discard until `S/N²` running mean is stable to <0.5 SE over 200-trajectory windows, minimum 2000 trajectories.
- **Decorrelation requirement (verified, Sec. 7):** the δ estimator needs independent samples. Measure the integrated autocorrelation time `τ_int` of `Tr(X_a²)/N`; the ensemble used for δ must satisfy **K_eff = K / (2 τ_int) ≥ 40** independent-equivalent samples. Raw K is insufficient; under autocorrelation the fluctuation norm under-reads δ (verified: at τ_int=20, K=40 reads 35% low; K=80·τ_int restores it).
- Initial conditions: hot (Gaussian) and cold (symmetric / zero); never seeded from a block configuration.

## 4. δ measurement and admissibility lookup (`SPEC-DELTA-MEAS-001`)

Per cell, on the decorrelated equilibrium ensemble:
```
δ_measured = mean_{k,a} ‖ X_a^(k) − ⟨X_a⟩ ‖_op  /  ( α · √¾ )      # blind, no partition; α-linear (SPEC v2)
class       = fixed-grid-detector( representative config, α, τ_frozen )   # raw multiset
admissible  = PR-B0.1.lookup( class, δ_measured, ρ )                 # post-hoc, frozen boundary
```
Conservative rounding: round `δ_measured` toward the larger (harder) δ-grid point; round any finite-K correction so δ is read **up**, not down (honesty: a low δ over-states resolution). The 1/0.988 finite-K factor is a PI choice, frozen pre-production.

## 5. Production grid (to be frozen)

`N`, α, and the temperature grid are chosen so the condensed ρ = Σnᵢ/N lands in the PR-B0.2 admissible band for the classes under test. Under the corrected α-linear scale `(2,3)` is admissible at δ=0.10 (ρ≥0.1351), so a primary-target run no longer requires reaching δ≤0.05; it requires reaching a thermal regime whose **measured** δ places `(2,3)` inside its admissible region. Whether such a regime exists for this action is a measured outcome, not an assumption. ≥200 trajectories/cell after thermalization, deterministic seeds per the PR-B0 seed rule.

## 6. Outcomes (frozen, exhaustive)

| ID | Pattern | Decision | Evidence action |
|---|---|---|---|
| O-A | δ_measured places `(2,3)` inside its admissible region (ρ≥0.1351 at the measured δ) AND condensation is modal `(2,3)` there, stable across the N-ladder, no null class modal | **CANDIDATE SIGNAL for (2,3)** | [D] pending: independent re-implementation + PI review + external replication. No upgrade authorized. |
| O-B | δ_measured admissible, condensation modal in another admissible class (e.g. `(3,4)`, `(2,2,3)`) | Measured condensation result for that class | [D]; `(2,3)` neither confirmed nor excluded if it is not the modal class |
| O-C | δ_measured exceeds the admissible region of `(2,3)` throughout the accessible thermal range (`(2,3)` breaks near δ≈0.30 under the α-linear scale) | **`(2,3)` UNRESOLVABLE at the model's noise floor** | Honest null: the matrix observable cannot resolve `(2,3)` at the achievable δ. Reinforces Appendix B Rem. B-moduli-restated. ONT-08 stays [D]. |
| O-D | no stable condensation, or modal class non-admissible everywhere | Non-discriminative | Methods/model revision only via new prereg ID |

Hard statement (binding): under O-C the programme records that **entropy/free-energy condensation in this model does not isolate `(2,3)` at a resolvable noise floor** — the central honest outcome the whole chain has been built to be able to reach. Partial patterns default to O-D; the default is never confirmatory.

## 7. Verified building blocks (auditor, this session)

| Block | Status |
|---|---|
| Fixed-grid detector, α known, raw multiset | verified collision-free on 8-class set (PR-B0.1) |
| Projection onto non-kernel subspace | verified; requires padding (ρ<1) |
| Blind ensemble δ estimator | verified: cv=0.0012, faithful to 1%, partition-blind |
| Decorrelation rule K_eff≥40 | verified: K=80·τ_int restores δ to 0.0987 independent of τ_int |
| Separability boundary ρ*(δ) | measured & signed in PR-B0.2 (α-linear); all 8 classes admissible at δ=0.10 |

## 8. Open items requiring PI decision before finalization

1. PR-B0.1 sign-off (CI green, sign-off line regenerated from pipeline, τ-curve documented).
2. Finite-K correction: apply 1/0.988 (rounds δ up, conservative) or leave raw — freeze pre-production.
3. Model couplings and temperature grid — frozen so the admissible ρ-band is reached; subject to the constraint that δ is *measured*, never tuned to reach any value.
4. `(2,2,2)` disposition (from PR-B0.1): admitted in its tighter band or dropped.

## 9. What this protocol cannot do (honest scope)

Even O-A (clean `(2,3)` signal) establishes only that this matrix action has a thermal window condensing into the `(2,3)` positive-spin class. It does **not** establish emergence of the Connes algebra (PR-B2 untouched, blocks are complex unitary), does not derive `G_SM`, and does not move ONT-08 above [D]. The `[1:2:3]` hypothesis itself is, under the conservative route, permanently inaccessible — only its projection `(2,3)` is testable.

---

*Framework draft by Claude/Opus, advisory capacity. All building blocks auditor-verified this session; the thermodynamic layer (action, temperatures) is finalized only after PR-B0.1 sign-off. This draft authorizes nothing.*
