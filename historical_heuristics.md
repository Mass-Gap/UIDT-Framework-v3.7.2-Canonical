# Historical Heuristics — UIDT Museum of Superseded Methods

> **Status:** Non-canonical archive. Documents methods and numerical constructs that were
> explored and are now classified as overcome, withdrawn, or diagnostic-only.
> **Purpose:** Transparency. These are kept as documented negative results — not deleted —
> to record the methodological maturation of the project.
> **Hard rule of this file:** Nothing listed here may be cited as evidence, used as a
> target/loss/objective in any script, or upgraded — without an independent, blind,
> first-principles derivation that reproduces it without prior knowledge of the value.

## Why this file exists

Several constructs in UIDT's history were attractive because they produced a number close to
a desired value (most often the calibrated γ = 16.339). On direct inspection — including in the
project's own pull requests and claims ledger — none survived as a derivation.

**The single governing lesson:** *numerical precision is never evidence of physical existence.*
A residual < 10⁻¹⁴, or a value reproduced to 80 digits, proves algorithmic convergence and
arithmetic — not that the underlying operator, number, or mechanism exists in nature.

---

## 1. γ_bare = (2N_c+1)²/N_c = 49/3 — color-algebra numerology

**Claimed:** an algebraic "first-principles" origin for γ ≈ 16.333, close to calibrated γ = 16.339.
**Why overcome:**
- It was the *single hit* of a combinatorial scan over Casimir-like expressions (PR #367) —
  selecting a near-miss is not a derivation.
- (2N_c+1)²/N_c does not appear in standard SU(N) invariant theory; the quadratic Casimirs are
  C₂(F) = 4/3 and C₂(A) = 3.
- Every forward check failed: 1-loop Δγ overshoots by 34–540×; 2-loop needs d₂ = −538.8 with
  "no Casimir origin"; γ_ledger = 16339/1000 and 16339 is prime, so the "49/3 + 17/3000" split
  is constructed, not found.
- The PR itself states: "γ_bare = 49/3 is algebraic, not a γ-proof."

**Ledger:** UIDT-C-052 = [E] conjectured. **Reference:** PR #367; docs/su3_gamma_conjecture_audit.md.

## 2. Δγ = 17/3000 — target residual

**Claimed:** the small gap γ_ledger − 49/3 equals 17/3000.
**Why overcome:** the candidate formula gives 0.005652… vs target 0.005666… (0.247% off);
α_s corrections make the match worse; no independent derivation of v exists. Permitted only as
a *diagnostic residual*, never as a target/loss/objective.
**Reference:** docs/S3_P1_alphas_running_analysis_2026-04-29.md.

## 3. The 10¹⁰ geometric factor — vacuum-energy hierarchy

**Claimed:** a ~10¹⁰ suppression bridging the 10¹²⁰ cosmological-constant problem.
**Why overcome:** the actual ratio λ_UIDT/r_conf ≈ 3.35×10⁶ ≈ 10^6.5, not 10¹⁰; the repo itself
states "no energy ratio in the Standard Model yields exactly 10¹⁰" (CANONICAL/LIMITATIONS.md L1).
The "3.3% solution of Λ" rests on this factor and is therefore not supported as stated.
**Ledger:** UIDT-C-018 / UIDT-C-042 = [E] open.

## 4. N = 99 RG cascade

**Claimed:** a 99-step cascade producing the vacuum-energy suppression.
**Why overcome:** empirically chosen; the repo itself lists "accidental numerical coincidence?"
as a live hypothesis (LIMITATIONS L5). A replacement N = 94.05 was proposed (PR #87) but never
reconciled with production code, leaving a self-contradiction.
**Ledger:** UIDT-C-017 / C-039 / C-046 / C-050 = [E] / open.

## 5. Glueball identification at 1.71 GeV

**Claimed:** Δ* = 1.710 GeV is the scalar glueball mass.
**Why overcome:** Δ* is the spectral gap of the Yang-Mills Hamiltonian, not a particle mass.
**Ledger:** UIDT-C-015 / C-041 = [E], WITHDRAWN 2025-12-25.
**Note:** README.md still presents this as "[B] lattice-consistent" — that line contradicts the
ledger and must be corrected (see PATCH_ANALYSIS B.2).

## 6. B3 / BMW "blind" γ-derivation

**Claimed:** a functional-RG (BMW) flow that derives K_S and hence γ.
**Why overcome:** the flow target K_S = (Δ*/γ)² was *back-solved from γ*, with a kill-switch on
|γ*−16.339|/16.339 > 0.01. Even after four successive "bug fixes" nudging the result toward the
target, the flow does **not** reproduce K_S — residual factor 3.31, described as "structurally
robust, invariant under threshold corrections" → K_S derivation downgraded to [E] not
reproducible. This is an internal *falsification*, not a derivation.
**Reference:** PR #533; research/L4-gamma/.

## 7. "World formula" / TOE / Mass-Gap-solution framing

**Why overcome:** as long as γ is calibrated (not blindly derived), no Yang-Mills-mass-gap
*solution* claim is defensible. Calibration matched to data is not an ab-initio result. Such
framing is removed from public-facing texts and from repository topics/metadata.

---

## What is NOT in this museum (still active, legitimately)

- **Δ* = 1.710 GeV** as an internally consistent, lattice-compatible spectral gap.
  *(Evidence classification under review: [A] "internal mathematical consistency" vs the more
  conservative [B] "lattice-compatible". See PATCH_ANALYSIS B.3.)*
- **γ = 16.339** as a calibrated phenomenological constant **[A-]** — kept, but never "derived".
- **5κ² = 3λ_S** as an exact *definition* (λ_S := 5κ²/3) — internally consistent, no predictive
  content; retained as a definition, not advertised as a discovery.
- The **external-ratio falsification programme** (m_0++·√8t₀, χ_top^{1/4}/Λ_MS vs Dürr/Fuwa 2025,
  Hasenfratz 2023) and the **GFERG learning path** — the honest forward directions.

---

*Maintained as a transparency record. Additions require only that the construct was genuinely
explored and is now overcome; removals require an explicit PI decision.*
