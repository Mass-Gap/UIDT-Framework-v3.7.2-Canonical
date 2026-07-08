# HANDOFF — PR-B0 Preflight: Projected Grid-Assignment Detector and Separability Boundary

| Field | Value |
|---|---|
| Handoff ID | `HANDOFF-PR-B0-001` |
| Target executor | Antigravity 2.0 (multi-agent; no external Jules dependency required) |
| Auditor | Claude/Opus — advisory only, no merge/sign-off authority (`AI_AUDIT_POLICY.md` Sec. 1) |
| Sign-off authority | PI (P. Rietz) only |
| Parent | `PR-B0_Preflight_Protocol.md` (PI-harmonized); supersedes the KDE detector |
| Status | **DRAFT for PI sign-off. No production PR-B1 run until PR-B0 gate is green.** |
| Scope class | Green-line (tests, detector validation, calibration, no protected-path writes) |
| Evidence ceiling | All PR-B0 outcomes are methodological. PR-B0 authorizes **no** physics claim and **no** evidence-class change. |
| Repo paths | Code `verification/prereg/PR-B0/` · data `verification/data/prereg-PR-B0/` · this brief `verification/prereg/PR-B0/HANDOFF_PR-B0_001.md` |

---

## 0. Why this handoff exists (audit trail, binding)

PR-B1 v1 failed pilot at four nested layers, each found before any production trajectory:

1. **Bandwidth** — global Silverman oversmooths small α-stretched matrices (the original escalation; correct symptom).
2. **Method** — KDE peak-counting is N-unstable on every class, even after fixes. **KDE is abandoned.**
3. **Observable** — the Casimir `Q = Σ X_a²` is **non-injective**: spin-0 (n=1) blocks and vacuum padding both sit at `Q=0`. PI decision (conservative route): **n=1 blocks are declared unobservable; the candidate set is collapsed to positive-spin equivalence classes.** The original target `[1:2:3]` therefore exists only as its projection `(2,3)`.
4. **Measurement background** — under matrix fluctuations the large vacuum-padding block (`z = N − Σnᵢ` zero modes) generates a dense Wishart-type Casimir band whose top grows with the perturbation; it can swamp the small condensed levels. **This is the gap PR-B0 must close.**

PR-B0 closes layer 4 with a **non-kernel projection** before grid assignment, and it makes the **separability boundary a measured deliverable**, so the PR-B1 N-ladder and admissible partition range follow from the analysis rather than being assumed.

---

## 1. Objective

Establish, by deterministic detection on planted ensembles (no thermodynamics, no simulation of dynamics), the region of the `(fill ratio ρ, noise level δ)` plane in which the **Projected Grid-Assignment Detector** recovers the positive-spin ratio class of a planted condensed configuration at **≥95%**, uniformly over the collapsed candidate set. The boundary curve `ρ*(δ)` and the calibrated parameters `(τ, projection rule)` are the deliverables that PR-B1-002 will consume.

Definitions:
- `ρ = (Σ nᵢ) / N` — fill ratio (condensed dimension over matrix size).
- `δ = ‖noise‖_op / Δ_min` — noise level, operator-norm of the planted perturbation over the smallest absolute Casimir gap `Δ_min = α² · ¾`. **δ, not a per-entry σ, is the physical robustness axis** (a per-entry σ scales the operator norm by √N and is not scale-meaningful).

---

## 2. Frozen model and observable

### 2.1 Planted condensed background
For a positive-spin partition `(n₁,…,n_k)`, `nᵢ ≥ 2`, and matrix size `N`:
```
X_a = α · ( ⊕_i L_a^{(n_i)} ) ⊕ 0_z ,   z = N − Σ nᵢ ,   a = 1,2,3
```
with `L_a^{(n)}` the spin-`(n−1)/2` su(2) generators. Casimir grid (exact, verified):
```
Q_n = α² · (n² − 1)/4 = α² · j(j+1),  j=(n−1)/2.
```

### 2.2 Collapsed candidate set (Q-injective; frozen)
Positive-spin representatives only. Frozen set for PR-B0 validation:
```
P_B0 = { (2,3), (2,4), (2,2,3), (3,4), (2,2,2) }
```
`(2,2,2)` is retained deliberately as a **degenerate stress case** (all blocks equal spin); its boundary is expected worst and must be reported, not hidden. Additional classes may be added only by amending this frozen list before any run.

### 2.3 Planted noise (frozen definition)
Perturb each matrix by a Hermitian operator of **fixed operator norm**:
```
X_a → X_a + (δ · Δ_min) · H_a ,  H_a Hermitian, ‖H_a‖_op = 1 (Wigner, normalized).
```
Sweep `δ ∈ {0.05, 0.10, 0.20, 0.30}`. **Do not** use a per-entry σ.

### 2.4 Numerics
Float64 (detector validation, not proof-critical identities). The `mp.dps=80` rule does **not** apply and must not be imported. Exact arithmetic (`fractions`) only for the ratio-class reduction (gcd) and the candidate-vector bookkeeping.

---

## 3. The Projected Grid-Assignment Detector (frozen algorithm)

Two calibrated parameters only: the projection rule (gap-based, parameter-light) and the grid tolerance `τ`. No bandwidth, no density estimation.

```
INPUT: X_1, X_2, X_3  (N×N Hermitian)
1. C ← (X_1² + X_2² + X_3²) ; symmetrize ; w ← eigvalsh(C) sorted ascending.
2. PROJECTION (kill the padding band):
     logs ← log(clip(w, 1e-9·w_max, ∞))
     cut  ← argmax(diff(logs))          # largest multiplicative gap
     Q⁺   ← w[cut+1:]                    # retained non-kernel spectrum
   If Q⁺ empty → return ()  (pure vacuum / unresolved).
3. SCALE: estimate α² by best global grid fit:
     for each admissible smallest level n₀: a2 ← min(Q⁺)/Q_{n₀};
       score ← Σ_q (nearest_grid(q/a2) − q/a2)²  ; pick a2 minimizing score.
4. ASSIGN: for each q in Q⁺:
     jj ← q/a2 ; n* ← argmin_n |Q_n_bare − jj|
     if |Q_n*_bare − jj| ≤ τ · max(Q_n*_bare, ¾):  count[n*] += 1
     else: drop (defect/mismatch)
5. BLOCKS: blocks ← Σ_n  [n] × round(count[n]/n)
6. OUTPUT: ratio-class reduce(blocks)   # gcd-normalized, n≥2 only
```

`τ` is calibrated in PR-B0 (Sec. 5), frozen as a single class-symmetric scalar, and never tuned per class or per N.

---

## 4. Measured separability boundary (the central deliverable)

The auditor's reference run (8 independent reproductions, operator-norm-calibrated noise, τ=0.12) establishes the qualitative law PR-B0 must confirm at production resolution:

| Regime | Behaviour (reference run) |
|---|---|
| `ρ = 1` (no padding) | **Fails for all classes.** The projection needs a kernel band to define the cut; with no padding there is no gap. Admissible region therefore **excludes ρ near 1**. |
| `ρ ∈ [0.14, 0.40]`, `δ ≤ 0.10` | **≥0.95 for (2,3), (2,4), (3,4)**; ~0.95 for (2,2,3) at the low-ρ end. |
| `δ ≥ 0.20` | Degrades; only the lowest-ρ, well-separated classes hold ≥0.95. |
| `(2,2,2)` | Worst case: ≤0.53 already at `δ=0.10`. Degenerate classes have a **structurally tighter** boundary. |

**Mandated finding for PR-B0:** report `ρ*(δ)`, the minimal fill ratio achieving ≥0.95 recovery, **per class**, on the production grid. The PR-B1-002 N-ladder and admissible partition range are then **defined as** `{ (partition, N) : ρ = Σnᵢ/N lies in the ≥0.95 region for that class at the target δ }`. This inverts the v1 error: resolution analysis fixes the ladder, not the reverse.

---

## 5. PR-B0 validation gate (frozen pass criteria)

1. **Grid-formula check** (exact): `Q_n = α²(n²−1)/4` for n=1..8 — machine-verified (Sec. 8).
2. **Injectivity check** (exact): `P_B0` has pairwise-distinct positive-Casimir signatures — machine-verified.
3. **τ calibration:** sweep `τ ∈ {0.05,…,0.20}`; select the single `τ` maximizing the area of the ≥0.95 region over `P_B0` at `δ=0.10`, with a stability requirement (chosen τ remains ≥0.95-optimal under ±0.02 perturbation). Freeze `τ`. **τ is an output of PR-B0, never a preset.**
4. **Boundary map:** produce `ρ*(δ)` per class on the production grid (Sec. 6), `δ ∈ {0.05,0.10,0.20,0.30}`.
5. **Pass condition:** PR-B0 **passes** iff there exists a non-empty admissible region (some class, some ρ-band) with ≥0.95 recovery at `δ ≤ 0.10` and the chosen frozen `τ`. **If no class clears ≥0.95 anywhere at δ≤0.10, PR-B0 returns NOT-SATISFIABLE** and PR-B1-002 does not start; the attractor programme records this honestly (the matrix observable cannot resolve the condensed structure at the achievable noise floor).

The reference run indicates the gate is satisfiable for non-degenerate classes; PR-B0 must confirm at production statistics and freeze the numbers.

---

## 6. Multi-agent execution plan (Antigravity 2.0)

No external Jules dependency. Antigravity spawns four cooperating agents with a strict data contract; no agent reinterprets physics.

| Agent | Role | Writes | Forbidden |
|---|---|---|---|
| **A-impl** | Implements `detector.py` (Sec. 3) + planted-ensemble generator (Sec. 2). Pure functions; no class literals in control flow. | `verification/prereg/PR-B0/src/` | any `(2,3)`/`1:2:3`/`target` literal in a conditional |
| **A-cal** | Runs τ-sweep (Sec. 5.3) on synthetic planted data only; emits frozen τ + stability report. | `…/data/prereg-PR-B0/calibration/` | choosing τ to favour any single class |
| **A-map** | Produces the `ρ*(δ)` boundary per class over the production grid; emits the admissibility region. | `…/data/prereg-PR-B0/boundary/` | trimming the grid after seeing results |
| **A-audit** | Re-runs grid-formula + injectivity exact checks; verifies no class-literal leakage via the gatekeeper CI; assembles the gate verdict for PI. | `…/PR-B0/GATE_REPORT.md` | issuing PASS/APPROVED (advisory verdict only; PI signs) |

Production grid: `N ∈ {sum, sum+4, sum+8, sum+16, sum+32}` per class (so ρ spans 1.0→~0.15); `α ∈ {1,2,4}`; `δ ∈ {0.05,0.10,0.20,0.30}`; **≥200 planted trials per cell** (reference used 15–30; production tightens CIs). Deterministic seeds:
```
seed(class, N, α, δ, trial) = int(SHA256(f"PR-B0-001|{class}|{N}|{α}|{δ}|{trial}").hexdigest()[:16], 16)
```

Stage order (frozen): A-impl → A-audit(exact checks) → A-cal(freeze τ) → A-map(boundary) → A-audit(verdict). A-cal must complete and freeze τ **before** A-map runs; A-map must not feed back into τ.

---

## 7. Forbidden operations (any one voids PR-B0)

1. Reintroducing KDE or any density-estimation detector.
2. Introducing a fluctuation-coupling observable to resurrect n=1 blocks (PI decision: conservative route).
3. Per-class or per-N tuning of τ; any data-dependent detector parameter beyond the single frozen τ and the gap-based projection.
4. Trimming/extending the grid, classes, or δ-set after inspecting recovery.
5. Writing to protected paths (`CANONICAL/`, `LEDGER/`, `core/`, `modules/`, `manuscript/`) or repo root; all artifacts under `verification/`.
6. Any agent emitting a PASS/MERGE-READY/APPROVED verdict; only PI signs off.
7. Starting PR-B1-002 before the PR-B0 gate report carries PI sign-off.

---

## 8. Reproduction (one command per stage)

```
python -m prb0 verify-grid        # exact: Q_n=α²(n²-1)/4, n=1..8  -> all match
python -m prb0 verify-injective   # exact: P_B0 positive-Casimir signatures distinct
python -m prb0 calibrate          # τ-sweep on synthetic planted data; freezes τ
python -m prb0 boundary           # ρ*(δ) per class on the production grid
python -m prb0 gate-report        # assembles GATE_REPORT.md for PI sign-off
```

Auditor reference checks (already executed, exact arithmetic):
```
python3 -c "print(all(abs(((n-1)/2*((n-1)/2+1)) - (n*n-1)/4) < 1e-12 for n in range(1,9)))"
# -> True   (grid formula)
```

---

## 9. PR-B0 claims table

| ID | Claim | Class | Falsification / downgrade |
|---|---|---|---|
| B0-01 | Casimir grid `Q_n=α²(n²−1)/4` exact | [A] | Machine check (verify-grid) |
| B0-02 | `P_B0` is Q-injective | [A] | Machine check (verify-injective) |
| B0-03 | Projection requires padding; ρ=1 unresolvable | [A] re method | A projection rule resolving ρ=1 would revise the admissible region |
| B0-04 | Non-degenerate classes reach ≥0.95 for ρ∈[~0.14,0.40], δ≤0.10 | [B] pending production stats | Production map below 0.95 ⇒ tighten admissible region or NOT-SATISFIABLE |
| B0-05 | Degenerate `(2,2,2)` has structurally tighter boundary | [B] | Production map; report regardless |
| B0-06 | τ is an output, frozen post-calibration | [A] governance | Any per-class τ voids PR-B0 |
| B0-07 | PR-B1-002 ladder = admissible (partition,N) region from B0-04 | [A] governance | Ladder chosen outside the measured region voids the inversion principle |

---

## 10. Sign-off block

```
PI sign-off (required before PR-B1-002):     ____________________  date: ________
PR-B0 gate verdict (A-audit, advisory):      [ ] satisfiable  [ ] NOT-SATISFIABLE
Frozen τ (calibration output):               τ = ____________
Admissible region (per class, ≥0.95@δ≤0.10): __________________________________
Gatekeeper CI green on PR-B0 dir:            [ ] yes   run id: ____________
```

*Drafted by Claude/Opus, advisory capacity, under `AI_AUDIT_POLICY.md` Sec. 1. The separability boundary is a measured finding, not a target; this brief authorizes nothing and constrains everything downstream of it.*
