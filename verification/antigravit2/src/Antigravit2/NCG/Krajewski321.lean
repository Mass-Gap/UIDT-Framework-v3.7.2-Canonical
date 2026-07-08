/-
  UIDT Phase 10c – Krajewski 321 Instance
  Status: [D] Structural Program. Specific Instance.
  Project: UIDT-Framework-Canonical
-/

import Antigravit2.NCG.KrajewskiCore

namespace Antigravit2.NCG.SM

/-- The partition blocks for the [3,2,1] instance. -/
def smBlocks : List ℕ := [3, 2, 1]

/-- 
  The specific diagram connecting blocks [3], [2], [1].
  Purely combinatorial, decoupled from H1/H2 and physical constants.
-/
def smDiagram321 : KrajewskiDiagram := {
  edges := [
    { leftBlock := 3, rightBlock := 2, multiplicity := 1 },
    { leftBlock := 2, rightBlock := 1, multiplicity := 1 },
    { leftBlock := 3, rightBlock := 1, multiplicity := 1 }
  ]
}

/-- 
  Unconditional Theorem: smDiagram321 is an admissible diagram 
  (no self loops). H1/H2 are not needed for this purely structural property.
-/
theorem smDiagram321_admissible : smDiagram321.admissibleDiagram := by
  intro e he
  dsimp [smDiagram321, KrajewskiDiagram.admissibleDiagram, KrajewskiDiagram.noSelfLoops] at *
  cases he with
  | head _ => simp [Bimodule.asymmetric]
  | tail _ h1 =>
    cases h1 with
    | head _ => simp [Bimodule.asymmetric]
    | tail _ h2 =>
      cases h2 with
      | head _ => simp [Bimodule.asymmetric]
      | tail _ h3 => contradiction

end Antigravit2.NCG.SM
