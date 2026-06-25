/-
  Antigravit2.Filters.Enumeration
  =================================
  [D/E] — Combinatorial enumeration only. No physical claim.

  Phase 1: Explicit partition candidate lists for N = 4, 5, 6.
  Stufe 1 strategy: hard-coded reference lists with sum/positivity checks.
  Stufe 2 (later): generative enumerator with monotonicity invariant.

  Anti-Target-Leakage: all partitions listed uniformly; no partition
  is singled out in definitions. Filter results derived by proof.

  Reference: Matrix-Thermodynamik session notes
-/

import Antigravit2.MatrixThermo.BlockPartition
import Antigravit2.Filters.Admissibility
import Mathlib.Tactic

namespace Antigravit2
namespace Filters

open MatrixThermo

-- ═══════════════════════════════════════════════════════════════
-- Explicit reference lists (Stufe 1)
-- Partitions in decreasing order (canonical form)
-- ═══════════════════════════════════════════════════════════════

/-- All partitions of 4 (decreasing order). -/
def partitions4 : List (List ℕ) :=
  [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]

/-- All partitions of 5 (decreasing order). -/
def partitions5 : List (List ℕ) :=
  [[5], [4, 1], [3, 2], [3, 1, 1], [2, 2, 1], [2, 1, 1, 1], [1, 1, 1, 1, 1]]

/-- All partitions of 6 (decreasing order). -/
def partitions6 : List (List ℕ) :=
  [[6], [5, 1], [4, 2], [4, 1, 1], [3, 3], [3, 2, 1], [3, 1, 1, 1],
   [2, 2, 2], [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

-- ═══════════════════════════════════════════════════════════════
-- Sum checks: every candidate list sums correctly
-- ═══════════════════════════════════════════════════════════════

example : partitions4.Forall (fun xs => xs.sum = 4) := by decide
example : partitions5.Forall (fun xs => xs.sum = 5) := by decide
example : partitions6.Forall (fun xs => xs.sum = 6) := by decide

-- ═══════════════════════════════════════════════════════════════
-- Positivity checks: every element is positive
-- ═══════════════════════════════════════════════════════════════

example : partitions4.Forall (fun xs => xs.Forall (· > 0)) := by decide
example : partitions5.Forall (fun xs => xs.Forall (· > 0)) := by decide
example : partitions6.Forall (fun xs => xs.Forall (· > 0)) := by decide

-- ═══════════════════════════════════════════════════════════════
-- Completeness: correct count of partitions p(N)
-- p(4)=5, p(5)=7, p(6)=11
-- ═══════════════════════════════════════════════════════════════

example : partitions4.length = 5 := by decide
example : partitions5.length = 7 := by decide
example : partitions6.length = 11 := by decide

-- ═══════════════════════════════════════════════════════════════
-- Entropy/offDiag computation for all partitions of 6
-- (numerical regression, Anti-Target-Leakage: uniform treatment)
-- ═══════════════════════════════════════════════════════════════

-- Format: (partition, entropy, offDiag, entropy + 2*offDiag = 36?)
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

-- Identity check: S + 2·U = 36 for all partitions of 6
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
-- Filter verdicts for all 11 partitions of 6
-- spread, allEqual, admissible δ=1, admissible δ=2
-- ═══════════════════════════════════════════════════════════════

-- Spread values
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
-- Summary table for N=6 (as comments, derived from examples above)
--
-- Partition     | S  | U  | spread | allEq | adm δ=1 | adm δ=2
-- [6]           | 36 |  0 |   0    |  yes  |   no    |   no
-- [5,1]         | 26 |  5 |   4    |  no   |   no    |   no
-- [4,2]         | 20 |  8 |   2    |  no   |   no    |   yes
-- [4,1,1]       | 18 |  9 |   3    |  no   |   no    |   no
-- [3,3]         | 18 |  9 |   0    |  yes  |   no    |   no
-- [3,2,1]       | 14 | 11 |   2    |  no   |   no    |   yes  ← ATL target
-- [3,1,1,1]     | 12 | 12 |   2    |  no   |   no    |   yes
-- [2,2,2]       | 12 | 12 |   0    |  yes  |   no    |   no
-- [2,2,1,1]     | 10 | 13 |   1    |  no   |   yes   |   yes
-- [2,1,1,1,1]   |  8 | 14 |   1    |  no   |   yes   |   yes
-- [1,1,1,1,1,1] |  6 | 15 |   0    |  yes  |   no    |   no
-- ═══════════════════════════════════════════════════════════════

end Filters
end Antigravit2
