/-
  Antigravit2.NCG.Krajewski
  ==========================
  [D] — Krajewski Diagram Structure.

  Phase 10a: Defines Krajewski diagrams as a structure carrying edges
  over a finite algebra signature. Extensibility added for future props.
-/

import Antigravit2.NCG.FiniteAlgebra
import Antigravit2.NCG.Bimodule

namespace Antigravit2.NCG

/--
  [D] A Krajewski Diagram classifies the finite spectral triples over a given FiniteAlgebraSignature.
  It is defined as a structure carrying a list of edges (bimodules).
  Future phases will add `validBlocks`, `poincareDual`, and `firstOrderCompatible` as fields.
-/
structure KrajewskiDiagram (A H : Type*) [AddCommGroup H] [Module ℂ H] [RealStructure H]
    (sig : FiniteAlgebraSignature A H) where
  edges : List Bimodule

end Antigravit2.NCG
