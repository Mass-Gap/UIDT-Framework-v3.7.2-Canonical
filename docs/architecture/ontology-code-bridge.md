# Ontology Code Bridge

This document establishes the conceptual links between the formal equations in the canonical LaTeX manuscripts (e.g., `UIDT_Ontology_v4_0_0.tex`) and the Lean 4 type-theoretic implementations.

## Mapping

| Ontology Concept | Lean Module | Key Type/Theorem |
|---|---|---|
| Primitive Operator $S$ | `Foundation/PrimitiveOperator.lean` | `PrimitiveOperator` |
| Spectral Triple | `NCG/SpectralTriple.lean` | `SpectralTriple` |
| KO-Dimension | `NCG/FiniteAlgebra.lean` | `FiniteAlgebraSignature.koDim` |
| Matrix Partitioning | `MatrixThermo/BlockPartition.lean` | `BlockPartition` |
