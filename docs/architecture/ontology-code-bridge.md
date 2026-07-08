# Ontology Code Bridge

This document establishes the conceptual links between the formal equations in the canonical LaTeX manuscripts (e.g., `UIDT_Ontology_v4_0_0.tex`) and the Lean 4 type-theoretic implementations.

## Mapping

| Ontology Concept | Lean Module | Key Type/Theorem |
|---|---|---|
| Primitive Operator $S$ | `Foundation/PrimitiveOperator.lean` | `PrimitiveOperator` |
| Spectral Triple | `NCG/SpectralTriple.lean` | `SpectralTriple` |
| KO-Dimension | `NCG/FiniteAlgebra.lean` | `FiniteAlgebraSignature.koDim` |
| Krajewski Diagram | `NCG/Krajewski.lean` | `KrajewskiDiagram`, `Bimodule` |
| Dirac 321 Model | `NCG/Dirac321.lean` | `dirac321`, `spectralTriple321` |
| Spectral Gap $\Delta$ | `NCG/DeltaScale.lean` | `SpectralGapParam`, `DeltaGlueballConjecture` |
| Matrix Partitioning | `MatrixThermo/BlockPartition.lean` | `BlockPartition` |
| NCG Filters / Partition Admissibility | `Filters/EliminationN6.lean` | `phase9Admissible`, `unique_321_N6` |
| Moduli Space & RNC | `NCG/ModuliStub.lean` | `ModuliDatum`, `rnc_conjecture` |
