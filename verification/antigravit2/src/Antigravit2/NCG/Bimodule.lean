/-
  Antigravit2.NCG.Bimodule
  ==========================
  [D] — Bimodule structural data for Krajewski diagrams.

  Phase 10a: Defines the edge structure of a finite NCG diagram.
  Asymmetry is a derived property, not a free boolean.
-/

import Mathlib.Data.Nat.Basic

namespace Antigravit2
namespace NCG

/-- [D] A Bimodule represents an edge in a Krajewski diagram,
    connecting a left block to a right block with a certain multiplicity.
    It corresponds to the off-diagonal entries in the Dirac operator. -/
structure Bimodule where
  leftBlock  : ℕ
  rightBlock : ℕ
  multiplicity : ℕ

namespace Bimodule

/-- [D] Derived property: A bimodule is asymmetric (chiral) if it connects distinct blocks. -/
def asymmetric (b : Bimodule) : Prop :=
  b.leftBlock ≠ b.rightBlock

end Bimodule

end NCG
end Antigravit2
