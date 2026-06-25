/-
  Antigravit2.MatrixThermo.BlockPartition
  =========================================
  [D/E] — Combinatorial definitions only. No physical claim.

  Phase 1: List-level helpers + lifted BlockPartition definitions.
  Strategy: prove on lists first, then lift via simpa.

  Reference: Matrix-Thermodynamik session notes
  Reference: UIDT_Ontology_v3_9_9.tex, Part IV
-/

import Mathlib.Data.List.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Tactic

namespace Antigravit2
namespace MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- List-level helpers (prove here, lift to BlockPartition below)
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] Entropy on raw lists: Σ n_i². -/
def entropyList (xs : List ℕ) : ℕ :=
  (xs.map fun n => n * n).sum

/-- [D/E] Off-diagonal penalty on raw lists: Σ_{i<j} n_i · n_j. -/
def offDiagList : List ℕ → ℕ
  | [] => 0
  | n :: ns => n * ns.sum + offDiagList ns

-- ---------------------------------------------------------------
-- List-level lemmas
-- ---------------------------------------------------------------

@[simp] lemma entropyList_nil : entropyList [] = 0 := by
  simp [entropyList]

@[simp] lemma entropyList_cons (n : ℕ) (ns : List ℕ) :
    entropyList (n :: ns) = n * n + entropyList ns := by
  simp [entropyList, List.map_cons, List.sum_cons]

@[simp] lemma offDiagList_nil : offDiagList [] = 0 := rfl

@[simp] lemma offDiagList_cons (n : ℕ) (ns : List ℕ) :
    offDiagList (n :: ns) = n * ns.sum + offDiagList ns := rfl

lemma entropyList_singleton (n : ℕ) : entropyList [n] = n * n := by
  simp

lemma offDiagList_singleton (n : ℕ) : offDiagList [n] = 0 := by
  simp

lemma entropyList_replicate_one (N : ℕ) :
    entropyList (List.replicate N 1) = N := by
  induction N with
  | zero => simp
  | succ k ih => simp [List.replicate_succ, ih]

/-- The fundamental algebraic identity on lists:
    (Σ n_i)² = Σ n_i² + 2·Σ_{i<j} n_i·n_j -/
theorem square_sum_identity (xs : List ℕ) :
    xs.sum * xs.sum = entropyList xs + 2 * offDiagList xs := by
  induction xs with
  | nil => simp
  | cons a as ih =>
    simp [List.sum_cons]
    ring_nf
    rw [show a * a + (a * as.sum + as.sum * a) + as.sum * as.sum
        = a * a + 2 * (a * as.sum) + as.sum * as.sum from by ring]
    rw [ih]
    ring

-- ═══════════════════════════════════════════════════════════════
-- BlockPartition structure
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] A block partition of N: a list of positive naturals summing to N.
    Anti-Target-Leakage: generic over all partitions. -/
structure BlockPartition (N : ℕ) where
  blocks : List ℕ
  positive : ∀ n ∈ blocks, 0 < n
  sum_blocks : blocks.sum = N

/-- Number of blocks. -/
def BlockPartition.numBlocks {N : ℕ} (p : BlockPartition N) : ℕ :=
  p.blocks.length

-- ═══════════════════════════════════════════════════════════════
-- Lifted definitions (thin wrappers)
-- ═══════════════════════════════════════════════════════════════

/-- [D/E] Entropy: S ~ Σ n_i². -/
def entropy {N : ℕ} (p : BlockPartition N) : ℕ :=
  entropyList p.blocks

/-- [D/E] Off-diagonal penalty: U_off ~ Σ_{i<j} n_i · n_j. -/
def offDiagPenalty {N : ℕ} (p : BlockPartition N) : ℕ :=
  offDiagList p.blocks

-- ═══════════════════════════════════════════════════════════════
-- Lifted lemmas
-- ═══════════════════════════════════════════════════════════════

lemma entropy_nil :
    entropy (⟨[], by intro n hn; cases hn, by simp⟩ : BlockPartition 0) = 0 := by
  simp [entropy]

lemma offDiagPenalty_nil :
    offDiagPenalty (⟨[], by intro n hn; cases hn, by simp⟩ : BlockPartition 0) = 0 := by
  simp [offDiagPenalty]

lemma entropy_singleton (n : ℕ) (hpos : 0 < n) :
    entropy (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) = n * n := by
  simp [entropy, entropyList]

lemma offDiagPenalty_singleton (n : ℕ) (hpos : 0 < n) :
    offDiagPenalty (⟨[n], by intro m hm; simp at hm; omega, by simp⟩ : BlockPartition n) = 0 := by
  simp [offDiagPenalty]

/-- The finest partition [1,...,1] has entropy = N. -/
lemma entropy_finest (N : ℕ) :
    entropy (⟨List.replicate N 1,
      by intro n hn; simp at hn; omega,
      by simp⟩ : BlockPartition N) = N := by
  simp [entropy, entropyList_replicate_one]

/-- N² = entropy(p) + 2·offDiagPenalty(p).
    Lifted from the list-level square_sum_identity. -/
theorem entropy_offDiag_identity {N : ℕ} (p : BlockPartition N) :
    N * N = entropy p + 2 * offDiagPenalty p := by
  have h := square_sum_identity p.blocks
  rw [p.sum_blocks] at h
  exact h

-- ═══════════════════════════════════════════════════════════════
-- Concrete test partitions
-- ═══════════════════════════════════════════════════════════════

/-- Partition [2, 1] of 3. -/
def p21 : BlockPartition 3 :=
  ⟨[2, 1], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega, by simp⟩

/-- Partition [2, 2] of 4. -/
def p22 : BlockPartition 4 :=
  ⟨[2, 2], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega, by simp⟩

/-- Partition [3, 2, 1] of 6. -/
def p321 : BlockPartition 6 :=
  ⟨[3, 2, 1], by intro n hn; simp at hn; rcases hn with rfl | rfl | rfl <;> omega, by simp⟩

/-- Partition [2, 2, 1, 1] of 6. -/
def p2211 : BlockPartition 6 :=
  ⟨[2, 2, 1, 1], by intro n hn; simp at hn; rcases hn with rfl | rfl | rfl | rfl <;> omega, by simp⟩

/-- Partition [3, 3] of 6. -/
def p33 : BlockPartition 6 :=
  ⟨[3, 3], by intro n hn; simp at hn; rcases hn with rfl | rfl <;> omega, by simp⟩

/-- Partition [2, 2, 2] of 6. -/
def p222 : BlockPartition 6 :=
  ⟨[2, 2, 2], by intro n hn; simp at hn; rcases hn with rfl | rfl | rfl <;> omega, by simp⟩

-- ═══════════════════════════════════════════════════════════════
-- Numerical regression examples
-- ═══════════════════════════════════════════════════════════════

-- [2, 1]: entropy = 4+1 = 5, offDiag = 2·1 = 2, identity: 9 = 5 + 2·2
example : entropy p21 = 5 := by simp [entropy, entropyList, p21]
example : offDiagPenalty p21 = 2 := by simp [offDiagPenalty, offDiagList, p21]
example : entropy p21 + 2 * offDiagPenalty p21 = 9 := by
  simp [entropy, entropyList, offDiagPenalty, offDiagList, p21]

-- [2, 2]: entropy = 4+4 = 8, offDiag = 2·2 = 4, identity: 16 = 8 + 2·4
example : entropy p22 = 8 := by simp [entropy, entropyList, p22]
example : offDiagPenalty p22 = 4 := by simp [offDiagPenalty, offDiagList, p22]

-- [3, 2, 1]: entropy = 9+4+1 = 14, offDiag = 3·3 + 2·1 = 11, identity: 36 = 14 + 22
example : entropy p321 = 14 := by simp [entropy, entropyList, p321]
example : offDiagPenalty p321 = 11 := by simp [offDiagPenalty, offDiagList, p321]
example : entropy p321 + 2 * offDiagPenalty p321 = 36 := by
  simp [entropy, entropyList, offDiagPenalty, offDiagList, p321]

-- [2, 2, 1, 1]: entropy = 4+4+1+1 = 10, offDiag = 2·4+2·2+1·1 = 13
example : entropy p2211 = 10 := by simp [entropy, entropyList, p2211]
example : offDiagPenalty p2211 = 13 := by simp [offDiagPenalty, offDiagList, p2211]

-- [3, 3]: entropy = 9+9 = 18, offDiag = 9
example : entropy p33 = 18 := by simp [entropy, entropyList, p33]
example : offDiagPenalty p33 = 9 := by simp [offDiagPenalty, offDiagList, p33]

-- [2, 2, 2]: entropy = 12, offDiag = 12
example : entropy p222 = 12 := by simp [entropy, entropyList, p222]
example : offDiagPenalty p222 = 12 := by simp [offDiagPenalty, offDiagList, p222]

end MatrixThermo
end Antigravit2
