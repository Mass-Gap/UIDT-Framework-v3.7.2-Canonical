/-
  UIDT Phase 10c – Krajewski Core
  Status: [D] Structural Program. Combinatorial Kernel.
  Project: UIDT-Framework-Canonical
-/

import Mathlib.Data.Nat.Basic

namespace Antigravit2.NCG

/-- 
  [D] A Bimodule represents an edge in a Krajewski diagram,
  connecting a left block to a right block with a certain multiplicity.
  It is a pure structural record without physical labels.
-/
structure Bimodule where
  leftBlock  : ℕ
  rightBlock : ℕ
  multiplicity : ℕ

namespace Bimodule

/-- [D] Derived property: A bimodule is asymmetric (chiral) if it connects distinct blocks. -/
def asymmetric (b : Bimodule) : Prop :=
  b.leftBlock ≠ b.rightBlock

end Bimodule

/--
  [D] A Krajewski Diagram classifies the finite spectral triples.
  It is defined as a structure carrying a list of edges (bimodules).
  Purely combinatorial, without `FiniteAlgebra` dependencies.
-/
structure KrajewskiDiagram where
  edges : List Bimodule

namespace KrajewskiDiagram

/-- Structural property: No edges connect a block to itself. -/
def noSelfLoops (kd : KrajewskiDiagram) : Prop :=
  ∀ e ∈ kd.edges, e.asymmetric

/-- Admissible diagrams must have no self-loops at minimum. -/
def admissibleDiagram (kd : KrajewskiDiagram) : Prop :=
  kd.noSelfLoops

end KrajewskiDiagram

end Antigravit2.NCG
