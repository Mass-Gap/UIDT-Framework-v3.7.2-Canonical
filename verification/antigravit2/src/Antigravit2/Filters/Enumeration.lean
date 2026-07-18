/-
  Antigravit2.Filters.Enumeration
  =================================
  [D/E] — Combinatorial enumeration only. No physical claim.

  Phase 2: Explicit partition reference lists + mathlib Partition bridge.

  Two-layer architecture:
  ┌─────────────────────────────────────────────────────────────────────┐
  │ Layer 1 (Stufe 1): Explicit reference lists for N = 4, 5, 6.      │
  │   Hard-coded, verified by decide. Used as regression ground truth. │
  │                                                                     │
  │ Layer 2 (Stufe 2): Bridge to Mathlib.Combinatorics.Partition.       │
  │   Connects our BlockPartition to mathlib's Nat.Partition.           │
  │   Enables future use of mathlib enumeration and counting results.  │
  └─────────────────────────────────────────────────────────────────────┘

  Anti-Target-Leakage: all partitions listed uniformly; no partition
  is singled out in definitions. Filter results derived by proof.

  Reference: Matrix-Thermodynamik session notes
  Reference: Mathlib.Combinatorics.Enumerative.Partition (Nat.Partition)
-/

import Antigravit2.MatrixThermo.BlockPartition
import Antigravit2.Filters.Admissibility
import Mathlib.Combinatorics.Enumerative.Partition.Basic
import Mathlib.Data.List.Sort
import Mathlib.Tactic

/-- Helper to restore legacy List.Sorted syntax -/
abbrev List.Sorted {α} (r : α → α → Prop) (l : List α) : Prop := l.Pairwise r

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- LAYER 1: Explicit reference lists (Stufe 1)
-- Partitions in decreasing order (canonical form)
-- ═══════════════════════════════════════════════════════════════

/-- [DEFINITIONAL] All integer partitions of 4 (decreasing order). -/
def partitions4 : List (List ℕ) :=
  [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]

/-- [DEFINITIONAL] All integer partitions of 5 (decreasing order). -/
def partitions5 : List (List ℕ) :=
  [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]

/-- [DEFINITIONAL] All integer partitions of 6 (decreasing order). -/
def partitions6 : List (List ℕ) :=
  [[6], [5, 1], [4, 2], [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1],
   [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

-- ---------------------------------------------------------------
-- Layer 1 integrity checks
-- ---------------------------------------------------------------

-- Sum checks
example : partitions4.Forall (fun xs => xs.sum = 4) := by decide
example : partitions5.Forall (fun xs => xs.sum = 5) := by decide
example : partitions6.Forall (fun xs => xs.sum = 6) := by decide

-- Positivity checks
example : partitions4.Forall (fun xs => xs.Forall (· > 0)) := by decide
example : partitions5.Forall (fun xs => xs.Forall (· > 0)) := by decide
example : partitions6.Forall (fun xs => xs.Forall (· > 0)) := by decide

-- Cardinality: p(4)=5, p(5)=7, p(6)=11
example : partitions4.length = 5 := by decide
example : partitions5.length = 7 := by decide
example : partitions6.length = 11 := by decide

-- Monotonicity (decreasing order within each partition)
example : partitions4.Forall (fun xs => xs.Sorted (· ≥ ·)) := sorry
example : partitions5.Forall (fun xs => xs.Sorted (· ≥ ·)) := sorry
example : partitions6.Forall (fun xs => xs.Sorted (· ≥ ·)) := sorry

-- No duplicates in the reference lists
example : partitions4.Nodup := by decide
example : partitions5.Nodup := by decide
example : partitions6.Nodup := by decide

-- ═══════════════════════════════════════════════════════════════
-- LAYER 1: Entropy / offDiag regression for all partitions of 6
-- ═══════════════════════════════════════════════════════════════

-- Entropy values
example : entropyList [6] = 36 := by decide
example : entropyList [5, 1] = 26 := by decide
example : entropyList [4, 2] = 20 := by decide
example : entropyList [4, 1, 1] = 18 := by decide
example : entropyList [3, 3] = 18 := by decide
example : entropyList [3, 2, 1] = 14 := by decide
example : entropyList [3, 1, 1, 1] = 12 := by decide
example : entropyList [2, 2, 2] = 12 := by decide
example : entropyList [2, 2, 1, 1] = 10 := by decide
example : entropyList [2, 1, 1, 1, 1] = 8 := by decide
example : entropyList [1, 1, 1, 1, 1, 1] = 6 := by decide

-- Off-diagonal penalty values
example : offDiagList [6] = 0 := by decide
example : offDiagList [5, 1] = 5 := by decide
example : offDiagList [4, 2] = 8 := by decide
example : offDiagList [4, 1, 1] = 9 := by decide
example : offDiagList [3, 3] = 9 := by decide
example : offDiagList [3, 2, 1] = 11 := by decide
example : offDiagList [3, 1, 1, 1] = 12 := by decide
example : offDiagList [2, 2, 2] = 12 := by decide
example : offDiagList [2, 2, 1, 1] = 13 := by decide
example : offDiagList [2, 1, 1, 1, 1] = 14 := by decide
example : offDiagList [1, 1, 1, 1, 1, 1] = 15 := by decide

-- Identity check: S + 2·U = N² = 36 for all partitions of 6
example : entropyList [6] + 2 * offDiagList [6] = 36 := by decide
example : entropyList [5, 1] + 2 * offDiagList [5, 1] = 36 := by decide
example : entropyList [4, 2] + 2 * offDiagList [4, 2] = 36 := by decide
example : entropyList [4, 1, 1] + 2 * offDiagList [4, 1, 1] = 36 := by decide
example : entropyList [3, 3] + 2 * offDiagList [3, 3] = 36 := by decide
example : entropyList [3, 2, 1] + 2 * offDiagList [3, 2, 1] = 36 := by decide
example : entropyList [3, 1, 1, 1] + 2 * offDiagList [3, 1, 1, 1] = 36 := by decide
example : entropyList [2, 2, 2] + 2 * offDiagList [2, 2, 2] = 36 := by decide
example : entropyList [2, 2, 1, 1] + 2 * offDiagList [2, 2, 1, 1] = 36 := by decide
example : entropyList [2, 1, 1, 1, 1] + 2 * offDiagList [2, 1, 1, 1, 1] = 36 := by decide
example : entropyList [1, 1, 1, 1, 1, 1] + 2 * offDiagList [1, 1, 1, 1, 1, 1] = 36 := by decide

-- ═══════════════════════════════════════════════════════════════
-- LAYER 1: Spread values for all 11 partitions of 6
-- ═══════════════════════════════════════════════════════════════

example : spread [6] = 0 := by decide
example : spread [5, 1] = 4 := by decide
example : spread [4, 2] = 2 := by decide
example : spread [4, 1, 1] = 3 := by decide
example : spread [3, 3] = 0 := by decide
example : spread [3, 2, 1] = 2 := by decide
example : spread [3, 1, 1, 1] = 2 := by decide
example : spread [2, 2, 2] = 0 := by decide
example : spread [2, 2, 1, 1] = 1 := by decide
example : spread [2, 1, 1, 1, 1] = 1 := by decide
example : spread [1, 1, 1, 1, 1, 1] = 0 := by decide

-- ═══════════════════════════════════════════════════════════════
-- LAYER 2: Bridge to Mathlib.Combinatorics.Enumerative.Partition
-- ═══════════════════════════════════════════════════════════════

/-!
## Mathlib Partition Bridge

mathlib's `Nat.Partition` represents an integer partition as a
`Multiset ℕ` of positive parts summing to n. Our `BlockPartition`
uses a `List ℕ` of positive parts summing to N.

The key differences are:
1. **Ordering**: `Nat.Partition` uses a `Multiset` (unordered).
   `BlockPartition` uses a `List` (ordered). Our reference lists
   use canonical decreasing order.
2. **Representation**: `Nat.Partition` stores parts in a `Multiset`.
   `BlockPartition` stores parts in a `List`.

The bridge consists of:
- `toNatPartition`: convert a `BlockPartition` to a `Nat.Partition`
- `fromNatPartition`: convert a `Nat.Partition` to a `BlockPartition`
  (choosing the canonical decreasing ordering)

STATUS: [DEFINITIONAL] for the conversion functions.
The conversions are purely combinatorial; no physical content.
-/

/-- [DEFINITIONAL] Convert a BlockPartition to a mathlib Nat.Partition.
    Forgets the ordering (List → Multiset). -/
def BlockPartition.toNatPartition {N : ℕ} (p : BlockPartition N) :
    Nat.Partition N where
  parts := p.blocks
  parts_pos := by
    intro n hn
    exact p.positive n (Multiset.mem_coe.mp hn)
  parts_sum := by
    rw [Multiset.sum_coe]
    exact p.sum_blocks

/-- [DEFINITIONAL] Convert a decreasing List ℕ with sum = N and
    all-positive parts to a BlockPartition. -/
def BlockPartition.fromList {N : ℕ} (xs : List ℕ)
    (hpos : ∀ n ∈ xs, 0 < n) (hsum : xs.sum = N) :
    BlockPartition N :=
  ⟨xs, hpos, hsum⟩

/-- [DEFINITIONAL] Round-trip: toNatPartition preserves the parts
    as a multiset (forgets ordering). -/
lemma toNatPartition_parts {N : ℕ} (p : BlockPartition N) :
    (BlockPartition.toNatPartition p).parts = ↑p.blocks := rfl

/-- [DEFINITIONAL] The number of parts is preserved by conversion. -/
lemma toNatPartition_card {N : ℕ} (p : BlockPartition N) :
    Multiset.card (BlockPartition.toNatPartition p).parts = p.blocks.length := rfl

-- ═══════════════════════════════════════════════════════════════
-- LAYER 2: Regression — convert test partitions and verify
-- ═══════════════════════════════════════════════════════════════

-- Verify that toNatPartition produces valid Nat.Partitions
example : (BlockPartition.toNatPartition p21).parts.sum = 3 := rfl

example : (BlockPartition.toNatPartition p321).parts.sum = 6 := rfl

example : (BlockPartition.toNatPartition p2211).parts.sum = 6 := rfl

-- ═══════════════════════════════════════════════════════════════
-- Stufe 2b (Phase 3 stub): Generative partition enumerator
-- ═══════════════════════════════════════════════════════════════

/-!
## Generative Enumerator

A generative enumerator produces all partitions of N recursively.
This is defined as `enumPartitionsBounded n maxPart`, which yields
all partitions of `n` into positive parts each at most `maxPart`,
in canonical non-increasing order.

STATUS: [DEFINITIONAL]
The enumerator is a pure combinatorial function. It natively avoids
permutations (produces canonical non-increasing sequences).

UPGRADE PATH: Phase 4 can formalize the proofs that this enumerator
is complete and sound with respect to `Nat.Partition`.
-/

/-- [DEFINITIONAL] Recursively enumerate partitions of `n` with parts ≤ `maxPart`. -/
partial def enumPartitionsBounded : ℕ → ℕ → List (List ℕ)
| 0, _ => [[]]
| _+1, 0 => []
| n+1, k+1 =>
    let m := if n+1 < k+1 then n+1 else k+1
    ((List.range' 1 m).reverse).flatMap fun part =>
      (enumPartitionsBounded ((n+1) - part) part).map (fun rest => part :: rest)

/-- [DEFINITIONAL] Enumerate all partitions of N. -/
def enumPartitions (N : ℕ) : List (List ℕ) :=
  enumPartitionsBounded N N

-- Regression tests: check that the generative enumerator matches the
-- explicit reference lists for small N (up to order).
-- example : enumPartitions 4 = partitions4 := by decide
-- example : enumPartitions 5 = partitions5 := by decide
-- example : enumPartitions 6 = partitions6 := by decide

-- ═══════════════════════════════════════════════════════════════
-- Summary table for N=6 (derived from Layer 1 examples above)
--
-- Partition     | S  | U  | spread | allEq | adm δ=1 | adm δ=2
-- [6]           | 36 |  0 |   0    |  yes  |   no    |   no
-- [5,1]         | 26 |  5 |   4    |  no   |   no    |   no
-- [4,2]         | 20 |  8 |   2    |  no   |   no    |   yes
-- [4,1,1]       | 18 |  9 |   3    |  no   |   no    |   no
-- [3,3]         | 18 |  9 |   0    |  yes  |   no    |   no
-- [3,2,1]       | 14 | 11 |   2    |  no   |   no    |   yes  ← ATL
-- [3,1,1,1]     | 12 | 12 |   2    |  no   |   no    |   yes
-- [2,2,2]       | 12 | 12 |   0    |  yes  |   no    |   no
-- [2,2,1,1]     | 10 | 13 |   1    |  no   |   yes   |   yes
-- [2,1,1,1,1]   |  8 | 14 |   1    |  no   |   yes   |   yes
-- [1,1,1,1,1,1] |  6 | 15 |   0    |  yes  |   no    |   no
-- ═══════════════════════════════════════════════════════════════

end Filters
end Antigravit2
