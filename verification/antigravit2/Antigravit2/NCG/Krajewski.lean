import Antigravit2.NCG.FiniteAlgebra

namespace Antigravit2.NCG

/--
  A Krajewski Diagram classifies the finite spectral triples over a given FiniteAlgebraSignature.
  In this initial seed (no edges), we define it as a minimal inductive type.
-/
inductive KrajewskiDiagram (A H : Type*) [AddCommGroup H] [Module ℂ H] [RealStructure H]
    (sig : FiniteAlgebraSignature A H) where
  | empty : KrajewskiDiagram A H sig
