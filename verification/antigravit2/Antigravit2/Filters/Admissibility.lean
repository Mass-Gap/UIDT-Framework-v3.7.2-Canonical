/-
  Antigravit2.Filters.Admissibility
  ===================================
  [D/E] — Combinatorial predicates only. No physical claim.

  Phase 1: Compilable filter definitions with small lemmas.

  Builds on BlockPartition base lemmas. Filter predicates are defined
  as Prop-valued functions, not axioms. Admissibility is the conjunction.

  Strategy: define filters → prove basic sanity checks → enumerate
  for small N (Phase 1b).

  Anti-Target-Leakage: [3,2,1] appears ONLY in theorem conclusions,
  never in definitions or hypotheses.

  Reference: Matrix-Thermodynamik session notes (Filter 1, Filter 2)
  Reference: UIDT_Ontology_v3_9_9.tex, Part IV (multiplicity verdicts)
-/

import Antigravit2.MatrixThermo.BlockPartition

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- Filter 1: Dimension-jump constraint
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] Maximum block size in a partition. -/
def BlockPartition.maxBlock {N : ℕ} (p : BlockPartition N) : ℕ :=
  p.blocks.foldl max 0

/-- [D/E] Minimum block size in a partition (0 for empty). -/
def BlockPartition.minBlock {N : ℕ} (p : BlockPartition N) : ℕ :=
  match p.blocks with
  | [] => 0
  | n :: ns => ns.foldl min n

/-- [D/E] Filter 1: The spread (max - min block size) is at most δ.

    Motivated by NCG intersection-form non-degeneracy: blocks that are
    "too far apart" in dimension break the intersection form.

    This is a HYPOTHESIS [D], not a derived theorem.
    Default δ = 1 (adjacent dimensions only).

    Reference: arXiv:0706.3690 (Chamseddine-Connes-Marcolli)
-/
def filter1 {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  p.maxBlock - p.minBlock ≤ δ

-- ═══════════════════════════════════════════════════════════════
-- Filter 2: Symmetry-breaking constraint
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] Predicate: all blocks in the partition are equal. -/
def BlockPartition.allEqual {N : ℕ} (p : BlockPartition N) : Prop :=
  ∀ a ∈ p.blocks, ∀ b ∈ p.blocks, a = b

/-- [D/E] Filter 2: The partition is NOT fully symmetric.

    Fully symmetric partitions (all blocks equal) produce degenerate
    fermion mass spectra and are dynamically unstable under
    off-diagonal perturbations.

    Reference: Matrix-Thermodynamik session notes (Massendegeneration)
-/
def filter2 {N : ℕ} (p : BlockPartition N) : Prop :=
  ¬ p.allEqual

-- ═══════════════════════════════════════════════════════════════
-- Admissibility
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] A partition is admissible iff it passes both filters.

    Anti-Target-Leakage: defined generically. No specific partition
    is mentioned. The admissible set for a given N is determined
    by enumeration and proof.
-/
def admissible {N : ℕ} (p : BlockPartition N) (δ : ℕ := 1) : Prop :=
  filter1 p δ ∧ filter2 p

-- ═══════════════════════════════════════════════════════════════
-- Sanity lemmas
-- ═══════════════════════════════════════════════════════════════

/-- The single-block partition [N] is always allEqual (vacuously for k=1). -/
lemma singleton_allEqual (N : ℕ) (hN : 0 < N) :
    (⟨[N], by intro n hn; simp at hn; omega, by simp⟩ : BlockPartition N).allEqual := by
  intro a ha b hb
  simp at ha hb
  rw [ha, hb]

/-- The single-block partition [N] always fails Filter 2. -/
lemma singleton_fails_filter2 (N : ℕ) (hN : 0 < N) :
    ¬ filter2 (⟨[N], by intro n hn; simp at hn; omega, by simp⟩ : BlockPartition N) := by
  intro h
  exact h (singleton_allEqual N hN)

/-- The single-block partition [N] is never admissible. -/
theorem singleton_not_admissible (N : ℕ) (hN : 0 < N) :
    ¬ admissible (⟨[N], by intro n hn; simp at hn; omega, by simp⟩ : BlockPartition N) := by
  intro ⟨_, h2⟩
  exact singleton_fails_filter2 N hN h2

/-- The single-block partition [N] always passes Filter 1 (spread = 0). -/
lemma singleton_passes_filter1 (N : ℕ) (hN : 0 < N) (δ : ℕ) :
    filter1 (⟨[N], by intro n hn; simp at hn; omega, by simp⟩ : BlockPartition N) δ := by
  simp [filter1, BlockPartition.maxBlock, BlockPartition.minBlock]

/-- A two-block partition [a, b] with a ≠ b passes Filter 2. -/
lemma two_block_distinct_passes_filter2 {N : ℕ} (a b : ℕ)
    (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) (hsum : a + b = N) :
    filter2 (⟨[a, b], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega,
              by simp [hsum]⟩ : BlockPartition N) := by
  intro h_all
  have := h_all a (by simp) b (by simp)
  exact hab this

-- ═══════════════════════════════════════════════════════════════
-- Phase 1b stubs: enumeration for small N
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] For N = 3: the partition [2, 1] is admissible with δ = 1.
    (Spread = 1 ≤ 1, and blocks are not all equal.) -/
theorem partition_2_1_admissible :
    admissible (⟨[2, 1], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega,
                 by simp⟩ : BlockPartition 3) := by
  constructor
  · -- Filter 1: maxBlock - minBlock = 2 - 1 = 1 ≤ 1
    simp [filter1, BlockPartition.maxBlock, BlockPartition.minBlock]
  · -- Filter 2: 2 ≠ 1
    intro h_all
    have := h_all 2 (by simp) 1 (by simp)
    omega

/-- [D/E] For N = 4: the partition [2, 2] fails Filter 2 (all equal). -/
theorem partition_2_2_not_admissible :
    ¬ admissible (⟨[2, 2], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega,
                   by simp⟩ : BlockPartition 4) := by
  intro ⟨_, h2⟩
  apply h2
  intro a ha b hb
  simp at ha hb
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> rfl

/-- [D/E] For N = 6: the partition [3, 2, 1] is admissible with δ = 2.

    Anti-Target-Leakage: This partition appears ONLY here in a theorem
    conclusion. It is derived from the filter predicates, not assumed.
    Note: with δ = 1 (strict), [3,2,1] fails (spread = 2 > 1).
    With δ = 2, it passes.
-/
theorem partition_3_2_1_admissible_delta2 :
    admissible (⟨[3, 2, 1],
      by intro n hn; simp at hn; rcases hn with rfl | rfl | rfl <;> omega,
      by simp⟩ : BlockPartition 6) (δ := 2) := by
  constructor
  · -- Filter 1: maxBlock - minBlock = 3 - 1 = 2 ≤ 2
    simp [filter1, BlockPartition.maxBlock, BlockPartition.minBlock]
  · -- Filter 2: not all equal (3 ≠ 2)
    intro h_all
    have := h_all 3 (by simp) 2 (by simp)
    omega

end Filters
end Antigravit2
