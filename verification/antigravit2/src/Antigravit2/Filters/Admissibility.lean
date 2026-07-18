/-
  Antigravit2.Filters.Admissibility
  ===================================
  [D/E] — Combinatorial predicates only. No physical claim.

  Phase 2: Epistemically classified filter rules with formal status markers.

  Each filter rule is classified as one of:
  ┌──────────────────┬──────────────────────────────────────────────────────────┐
  │ Status           │ Meaning                                                │
  ├──────────────────┼──────────────────────────────────────────────────────────┤
  │ [DEFINITIONAL]   │ Pure combinatorial definition. No physical assumption. │
  │                  │ Proven properties are [A] within the formal system.    │
  │ [HEURISTIC]      │ Empirically motivated rule. Excludes classes of        │
  │                  │ partitions for physical reasons, but the exclusion     │
  │                  │ criterion is a modeling choice, not a theorem.         │
  │ [DESIGN-LEVEL]   │ Rule motivated by a higher theory (NCG, spectral      │
  │                  │ geometry) that is not yet formalized. Will be          │
  │                  │ replaced by a proper theorem when the NCG module      │
  │                  │ is complete.                                           │
  └──────────────────┴──────────────────────────────────────────────────────────┘

  Anti-Target-Leakage: [3,2,1] only in theorem conclusions / examples.

  Reference: Matrix-Thermodynamik session notes (Filter 1, Filter 2)
  Reference: UIDT_Ontology_v3_9_9.tex, Part IV (multiplicity verdicts)
  Reference: arXiv:0706.3690 (Chamseddine-Connes-Marcolli, NCG and SM)
-/

import Antigravit2.MatrixThermo.BlockPartition
import Mathlib.Data.List.Basic
import Mathlib.Tactic

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- [DEFINITIONAL] List-level utilities
-- Pure combinatorics, no physical assumption.
-- ═══════════════════════════════════════════════════════════════

/-- [DEFINITIONAL] All elements of a list are equal. -/
def allEqual : List ℕ → Prop
  | [] => True
  | x :: xs => ∀ y ∈ xs, y = x

/-- [DEFINITIONAL] Maximum element of a list (0 for empty). -/
def maxBlock : List ℕ → ℕ
  | [] => 0
  | x :: xs => xs.foldl Nat.max x

/-- [DEFINITIONAL] Minimum element of a list (0 for empty). -/
def minBlock : List ℕ → ℕ
  | [] => 0
  | x :: xs => xs.foldl Nat.min x

/-- [DEFINITIONAL] Spread: maxBlock - minBlock.
    Pure numerical measure. No physical content. -/
def spread (xs : List ℕ) : ℕ :=
  maxBlock xs - minBlock xs

-- ---------------------------------------------------------------
-- [DEFINITIONAL] List-level simp lemmas
-- ---------------------------------------------------------------

@[simp] lemma allEqual_nil : allEqual [] = True := rfl

@[simp] lemma allEqual_singleton (n : ℕ) : allEqual [n] ↔ True := by
  simp [allEqual]

lemma allEqual_cons_cons (a b : ℕ) (xs : List ℕ) :
    allEqual (a :: b :: xs) ↔ b = a ∧ allEqual (a :: xs) := by
  simp [allEqual]

/-- [DEFINITIONAL] A non-empty list with all elements equal has
    allEqual iff it consists of replicated copies of its head. -/
lemma allEqual_iff_head {n : ℕ} {ns : List ℕ} :
    allEqual (n :: ns) ↔ ∀ y ∈ ns, y = n := by
  simp [allEqual]

@[simp] lemma maxBlock_nil : maxBlock [] = 0 := rfl
@[simp] lemma minBlock_nil : minBlock [] = 0 := rfl
@[simp] lemma spread_nil : spread [] = 0 := rfl

@[simp] lemma maxBlock_singleton (n : ℕ) : maxBlock [n] = n := by
  simp [maxBlock]

@[simp] lemma minBlock_singleton (n : ℕ) : minBlock [n] = n := by
  simp [minBlock]

@[simp] lemma spread_singleton (n : ℕ) : spread [n] = 0 := by
  simp [spread]

/-- [DEFINITIONAL] Spread is zero iff maxBlock = minBlock. -/
lemma spread_eq_zero_iff (xs : List ℕ) :
    spread xs = 0 ↔ maxBlock xs ≤ minBlock xs := by
  simp [spread, Nat.sub_eq_zero_iff_le]

-- ═══════════════════════════════════════════════════════════════
-- Filter definitions with epistemic classification
-- ═══════════════════════════════════════════════════════════════

/-- [DESIGN-LEVEL] Filter 1: spread ≤ δ.

    STATUS: Design-level assumption.
    MOTIVATION: NCG intersection-form non-degeneracy constrains how
    "far apart" summands of a direct-sum matrix algebra can be.
    FORMALIZATION GAP: The precise bound δ is a modeling parameter,
    not derived from first principles. The NCG literature (arXiv:0706.3690)
    motivates such constraints but does not prove a general dimension-jump
    theorem in this exact form.
    UPGRADE PATH: When SpectralTriple.lean formalizes intersection-form
    axioms, this filter should be DERIVED from those axioms, not assumed.

    Reference: arXiv:0706.3690 (Chamseddine-Connes-Marcolli)
    Reference: arXiv:1805.08582 (classification of finite spectral triples)
-/
def filter1 {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  spread p.blocks ≤ δ

/-- [HEURISTIC] Filter 2: NOT all blocks equal.

    STATUS: Heuristic exclusion rule.
    MOTIVATION: Fully symmetric block partitions (all n_i equal) produce
    degenerate fermion mass spectra. Degenerate partitions are dynamically
    unstable under off-diagonal perturbations in the matrix-thermodynamic
    free energy landscape.
    EVIDENCE: Supported by the observation that the Standard Model
    has three generations with DISTINCT masses (not degenerate).
    FORMALIZATION GAP: "Dynamical instability" is a physical claim about
    the free energy landscape, not a combinatorial theorem. The exclusion
    is a heuristic proxy for a stability analysis.
    UPGRADE PATH: When the free energy functional F = -αS + βU_off is
    formalized, this filter should be replaced by a proper saddle-point
    or stability theorem.

    Reference: Matrix-Thermodynamik session notes (Massendegeneration)
-/
def filter2 {N : ℕ} (p : BlockPartition N) : Prop :=
  ¬ allEqual p.blocks

/-- [DEFINITIONAL] Admissible = filter1 ∧ filter2.

    STATUS: Definitional conjunction of the two filter rules.
    This definition is combinatorially clean but inherits the epistemic
    status of its components: the conjunction itself is [DEFINITIONAL],
    but its physical meaning depends on filter1 [DESIGN-LEVEL] and
    filter2 [HEURISTIC].

    Anti-Target-Leakage: generic definition, no specific partition.
-/
def admissible {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  filter1 p δ ∧ filter2 p

-- ═══════════════════════════════════════════════════════════════
-- [DEFINITIONAL] Sanity lemmas — proven within formal system [A]
-- ═══════════════════════════════════════════════════════════════

/-- Single-block [N] is always allEqual (trivially). -/
lemma singleton_allEqual (n : ℕ) (hpos : 0 < n) :
    allEqual [n] := by simp

/-- Single-block [N] fails Filter 2 (is allEqual). -/
lemma singleton_fails_filter2 (n : ℕ) (hpos : 0 < n) :
    ¬ filter2 (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) := by
  simp [filter2, allEqual]

/-- Single-block [N] is never admissible (for any δ). -/
theorem singleton_not_admissible (n : ℕ) (hpos : 0 < n) (δ : ℕ) :
    ¬ admissible (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) δ := by
  intro ⟨_, hf2⟩
  exact singleton_fails_filter2 n hpos hf2

/-- Single-block [N] passes Filter 1 for any δ (spread = 0). -/
lemma singleton_passes_filter1 (n : ℕ) (hpos : 0 < n) (δ : ℕ) :
    filter1 (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) δ := by
  simp [filter1, spread]

/-- [DEFINITIONAL] allEqual partitions always fail filter2 (and hence admissible). -/
lemma allEqual_fails_filter2 {N : ℕ} (p : BlockPartition N) (h : allEqual p.blocks) :
    ¬ filter2 p := by
  intro hf2; exact hf2 h

/-- [DEFINITIONAL] If spread > δ, filter1 fails. -/
lemma spread_too_large {N : ℕ} (p : BlockPartition N) {δ : ℕ}
    (h : δ < spread p.blocks) :
    ¬ filter1 p δ := by
  intro hf1
  dsimp [filter1] at hf1
  omega

-- ═══════════════════════════════════════════════════════════════
-- [DEFINITIONAL] Regression examples — spread and allEqual
-- These secure the semantics of the combinatorial definitions.
-- ═══════════════════════════════════════════════════════════════

-- Spread computations
example : spread [2, 1] = 1 := by simp [spread, maxBlock, minBlock]
example : spread [2, 2] = 0 := by simp [spread, maxBlock, minBlock]
example : spread [3, 2, 1] = 2 := by simp [spread, maxBlock, minBlock]
example : spread [2, 2, 1, 1] = 1 := by simp [spread, maxBlock, minBlock]
example : spread [3, 3] = 0 := by simp [spread, maxBlock, minBlock]
example : spread [2, 2, 2] = 0 := by simp [spread, maxBlock, minBlock]

-- allEqual checks
example : allEqual [2, 2] := by simp [allEqual]
example : allEqual [3, 3] := by simp [allEqual]
example : allEqual [2, 2, 2] := by simp [allEqual]
example : ¬ allEqual [2, 1] := by simp [allEqual]
example : ¬ allEqual [3, 2, 1] := by simp [allEqual]

-- ═══════════════════════════════════════════════════════════════
-- [DEFINITIONAL] Admissibility verdicts for test partitions
-- These are proven consequences of the definitions above.
-- The proofs inherit the epistemic status of filter1 and filter2,
-- but the LOGICAL DERIVATION is [A] within the formal system.
-- ═══════════════════════════════════════════════════════════════

-- p21 = [2,1]: spread=1, not allEqual → admissible δ=1 ✓
theorem p21_admissible : admissible p21 (δ := 1) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p21]
  · simp [filter2, allEqual, p21]

-- p22 = [2,2]: spread=0, allEqual → NOT admissible (any δ)
theorem p22_not_admissible (δ : ℕ) : ¬ admissible p22 δ := by
  intro ⟨_, hf2⟩
  apply hf2
  simp [allEqual, p22]

-- p33 = [3,3]: spread=0, allEqual → NOT admissible
theorem p33_not_admissible (δ : ℕ) : ¬ admissible p33 δ := by
  intro ⟨_, hf2⟩
  apply hf2
  simp [allEqual, p33]

-- p222 = [2,2,2]: spread=0, allEqual → NOT admissible
theorem p222_not_admissible (δ : ℕ) : ¬ admissible p222 δ := by
  intro ⟨_, hf2⟩
  apply hf2
  simp [allEqual, p222]

-- p321 = [3,2,1]: spread=2, not allEqual → admissible δ=2 ✓
theorem p321_admissible_delta2 : admissible p321 (δ := 2) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p321]
  · simp [filter2, allEqual, p321]

-- p321 = [3,2,1]: spread=2 > 1 → NOT admissible δ=1
theorem p321_not_admissible_delta1 : ¬ admissible p321 (δ := 1) := by
  intro ⟨hf1, _⟩
  simp [filter1, spread, maxBlock, minBlock, p321] at hf1

-- p2211 = [2,2,1,1]: spread=1, not allEqual → admissible δ=1 ✓
theorem p2211_admissible : admissible p2211 (δ := 1) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p2211]
  · simp [filter2, allEqual, p2211]

-- ═══════════════════════════════════════════════════════════════
-- Phase 2 epistemic status summary
--
-- ┌──────────────────────┬───────────────┬───────────────────────────────┐
-- │ Entity               │ Status        │ Upgrade path                  │
-- ├──────────────────────┼───────────────┼───────────────────────────────┤
-- │ allEqual, spread     │ DEFINITIONAL  │ Stable.                       │
-- │ maxBlock, minBlock   │ DEFINITIONAL  │ Stable.                       │
-- │ filter1 (spread ≤ δ) │ DESIGN-LEVEL  │ Derive from NCG axioms.       │
-- │ filter2 (¬allEqual)  │ HEURISTIC     │ Derive from F-landscape.      │
-- │ admissible           │ DEFINITIONAL  │ Inherits from filter1/filter2.│
-- │ Sanity lemmas        │ [A] formal    │ Stable.                       │
-- │ Test verdicts        │ [A] formal    │ Stable.                       │
-- └──────────────────────┴───────────────┴───────────────────────────────┘
-- ═══════════════════════════════════════════════════════════════

end Filters
end Antigravit2
