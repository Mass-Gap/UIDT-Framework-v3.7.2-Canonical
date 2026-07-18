/-
  UIDT Phase 10c – Krajewski Core
  Status: [D] Structural Program. Combinatorial Kernel.
  Project: UIDT-Framework-Canonical
-/

import Mathlib.Data.Nat.Basic
import Antigravit2.NCG.Bimodule

namespace Antigravit2.NCG

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
