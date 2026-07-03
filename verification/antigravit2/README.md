# Antigravit 2.0 — Lean 4 Formalization of UIDT Ontological Structures

> **Evidence Tag: [D/E] — Formal software project. No physical claims. No reality assertions.**

| Field | Value |
|---|---|
| Project | Antigravit 2.0 |
| Purpose | Lean 4 / mathlib4 formalization of UIDT ontological structures and filters |
| Scope | Type-theoretic encoding of DIR-S-01, Matrix Thermodynamics, NCG structures |
| Status | **Phase 0 — Scaffold** |
| Author | P. Rietz (PI), with AI-assisted code generation |
| Evidence | [D/E] throughout; no physical proof is claimed |

---

## Goal

This project does **not** attempt to prove UIDT physics in Lean. Instead, it:
- Codifies the **ontological structures and filters** as cleanly typed Lean definitions and theorems.
- Provides a **formal test laboratory** for Matrix Thermodynamics, NCG filters, and the Primitive Operator Directive (DIR-S-01).

## Governance & Audit

> [!IMPORTANT]
> **Layout Refactor Only, No Evidence-Class Upgrade:** The recent restructuring to the `src/` layout is purely organizational. It does not alter the mathematical or physical claims of the framework.
> **Privacy:** The `.uidt-local/` directory is strictly excluded from version control and remains private.
> **Axiom Audit:** The target `AxiomAudit.lean` is a mandatory CI governance step to ensure no unapproved `sorry` markers leak into the repository.

To build and audit the project locally, run exactly:
```bash
cd verification/antigravit2
lake build Antigravit2
lake build Antigravit2.NCG.AxiomAudit
```

## Module Structure

```
src/Antigravit2/
├── Foundation/          -- PrimitiveOperator class (DIR-S-01), base axioms
│   └── PrimitiveOperator.lean
├── MatrixThermo/        -- BlockPartition, entropy, off-diagonal penalty
│   └── BlockPartition.lean
├── Filters/             -- Filter 1 (dimension jump), Filter 2 (symmetry break), admissibility
│   └── Admissibility.lean
├── NCG/                 -- SpectralTriple stub, KO-dimension, real structure
│   └── SpectralTriple.lean
└── Meta/                -- Evidence tags, anti-target-leakage discipline
    └── EvidenceTags.lean
```

## Key Design Principles

1. **DIR-S-01**: The primitive is a pre-geometric operator **S**, not a classical field S(x). Coordinates and metric emerge at a later level. Routes via A = dS(x) on a smooth manifold are excluded (d²=0 obstruction).

2. **Anti-Target-Leakage**: No proof may contain its own target as input. The "desired partition" (3,2,1) must only emerge as a *result* of search/proofs over all partitions — never hard-coded in definitions.

3. **Evidence Tags**: Every definition and theorem carries its evidence classification as a docstring comment: `[A]` through `[E]`, following the canonical UIDT evidence system.

## Prerequisites

- **Lean 4** (toolchain leanprover/lean4:stable)
- **mathlib4** (C*-algebras, Hilbert spaces, Spectrum)

## Relation to Canonical Repository

This subfolder is part of `verification/` in the UIDT-Framework-V3.9-UNIVERSUM_SIM workspace. It does not modify any canonical claim, constant, or manuscript. All outputs are [D/E] diagnostic software.

## References

- `UIDT_Ontology_v3_9_9.tex` — Axioms, evidence discipline, d²=0 obstruction, GSM-Origin-Gap
- `METHODOLOGY_GLBC_001.md` — Gap Localization before Construction methodology
- `RESEARCH_MODULI_G1G4_001.md` — Moduli space analysis (G1–G4 conditions)
- Matrix-Thermodynamik session notes (block condensation, S ~ Σn_i², U_off ~ Σ_{i<j} n_i n_j)
- Deep-Research vectors (NCG/SM-Algebra, Lean spectral triple sketches, Thermal Time)
