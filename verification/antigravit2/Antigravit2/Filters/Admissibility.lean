/-
  Antigravit2.Filters.Admissibility
  ===================================
  [D/E] — Combinatorial predicates only. No physical claim.

  Phase 1: List-level filter helpers, lifted to BlockPartition,
  with concrete test-case examples.

  Strategy: allEqual/maxBlock/minBlock/spread on lists first,
  then filter1/filter2/admissible on BlockPartition as thin wrappers.

  Anti-Target-Leakage: [3,2,1] only in theorem conclusions / examples.

  Reference: Matrix-Thermodynamik session notes (Filter 1, Filter 2)
  Reference: UIDT_Ontology_v3_9_9.tex, Part IV (multiplicity verdicts)
-/

import Antigravit2.MatrixThermo.BlockPartition
import Mathlib.Data.List.Basic
import Mathlib.Tactic

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- List-level utilities
-- ═══════════════════════════════════════════════════════════════

/-- All elements of a list are equal. -/
def allEqual : List ℕ → Prop
  | [] => True
  | x :: xs => ∀ y ∈ xs, y = x

/-- Maximum element of a list (0 for empty). -/
def maxBlock : List ℕ → ℕ
  | [] => 0
  | x :: xs => xs.foldl Nat.max x

/-- Minimum element of a list (0 for empty). -/
def minBlock : List ℕ → ℕ
  | [] => 0
  | x :: xs => xs.foldl Nat.min x

/-- Spread: maxBlock - minBlock. -/
def spread (xs : List ℕ) : ℕ :=
  maxBlock xs - minBlock xs

-- ---------------------------------------------------------------
-- List-level lemmas
-- ---------------------------------------------------------------

@[simp] lemma allEqual_nil : allEqual [] = True := rfl

@[simp] lemma allEqual_singleton (n : ℕ) : allEqual [n] ↔ True := by
  simp [allEqual]

lemma allEqual_cons_cons (a b : ℕ) (xs : List ℕ) :
    allEqual (a :: b :: xs) ↔ b = a ∧ allEqual (a :: xs) := by
  simp [allEqual]
  constructor
  · intro h; exact ⟨h b (List.mem_cons_self b xs), fun y hy => h y (List.mem_cons_of_mem b hy)⟩
  · intro ⟨hba, hrest⟩ y hy
    rcases List.mem_cons.mp hy with rfl | hys
    · exact hba
    · exact hrest y hys

@[simp] lemma maxBlock_nil : maxBlock [] = 0 := rfl
@[simp] lemma minBlock_nil : minBlock [] = 0 := rfl
@[simp] lemma spread_nil : spread [] = 0 := rfl

@[simp] lemma maxBlock_singleton (n : ℕ) : maxBlock [n] = n := by
  simp [maxBlock]

@[simp] lemma minBlock_singleton (n : ℕ) : minBlock [n] = n := by
  simp [minBlock]

@[simp] lemma spread_singleton (n : ℕ) : spread [n] = 0 := by
  simp [spread]

-- ═══════════════════════════════════════════════════════════════
-- Filters on BlockPartition
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] Filter 1: spread ≤ δ.
    Motivated by NCG intersection-form non-degeneracy. [D] hypothesis.
    Reference: arXiv:0706.3690 -/
def filter1 {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  spread p.blocks ≤ δ

/-- [D/E] Filter 2: NOT all blocks equal.
    Fully symmetric → mass degeneracy → dynamically unstable.
    Reference: Matrix-Thermodynamik (Massendegeneration) -/
def filter2 {N : ℕ} (p : BlockPartition N) : Prop :=
  ¬ allEqual p.blocks

/-- [D/E] Admissible = filter1 ∧ filter2.
    Anti-Target-Leakage: generic definition, no specific partition. -/
def admissible {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  filter1 p δ ∧ filter2 p

-- ═══════════════════════════════════════════════════════════════
-- Sanity lemmas
-- ═══════════════════════════════════════════════════════════════

/-- Single-block [N] is always allEqual. -/
lemma singleton_allEqual (n : ℕ) (hpos : 0 < n) :
    allEqual [n] := by simp

/-- Single-block [N] fails Filter 2. -/
lemma singleton_fails_filter2 (n : ℕ) (hpos : 0 < n) :
    ¬ filter2 (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) := by
  simp [filter2, allEqual]

/-- Single-block [N] is never admissible. -/
theorem singleton_not_admissible (n : ℕ) (hpos : 0 < n) (δ : ℕ) :
    ¬ admissible (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) δ := by
  intro ⟨_, hf2⟩
  exact singleton_fails_filter2 n hpos hf2

/-- Single-block [N] passes Filter 1 for any δ (spread = 0). -/
lemma singleton_passes_filter1 (n : ℕ) (hpos : 0 < n) (δ : ℕ) :
    filter1 (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) δ := by
  simp [filter1, spread]

-- ═══════════════════════════════════════════════════════════════
-- Concrete test cases: spread, allEqual, filters
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
example : ¬ allEqual [2, 1] := by simp [allEqual]; omega
example : ¬ allEqual [3, 2, 1] := by simp [allEqual]; omega

-- ═══════════════════════════════════════════════════════════════
-- Admissibility verdicts for test partitions
-- ═══════════════════════════════════════════════════════════════

-- p21 = [2,1]: spread=1, not allEqual → admissible δ=1 ✓
theorem p21_admissible : admissible p21 (δ := 1) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p21]
  · simp [filter2, allEqual, p21]; omega

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

-- p321 = [3,2,1]: spread=2, not allEqual → admissible δ=2 ✓, NOT admissible δ=1 ✗
theorem p321_admissible_delta2 : admissible p321 (δ := 2) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p321]
  · simp [filter2, allEqual, p321]; omega

theorem p321_not_admissible_delta1 : ¬ admissible p321 (δ := 1) := by
  intro ⟨hf1, _⟩
  simp [filter1, spread, maxBlock, minBlock, p321] at hf1

-- p2211 = [2,2,1,1]: spread=1, not allEqual → admissible δ=1 ✓
theorem p2211_admissible : admissible p2211 (δ := 1) := by
  constructor
  · simp [filter1, spread, maxBlock, minBlock, p2211]
  · simp [filter2, allEqual, p2211]; omega

end Filters
end Antigravit2
