/-
  Antigravit2.Meta.EvidenceTags
  ===============================
  [D/E] — Meta-discipline module. No physical claim.

  Formalizes the UIDT evidence classification system and the
  Anti-Target-Leakage discipline as Lean types and documentation
  conventions.

  Every definition and theorem in Antigravit2 MUST carry an evidence
  tag in its docstring, following this classification:

  | Tag  | Name                        | Threshold / Criterion           |
  |------|-----------------------------|---------------------------------|
  | [A]  | Mathematically Proven       | Residuals < 10⁻¹⁴              |
  | [A-] | Phenomenologically Determined | Calibrated to data             |
  | [B]  | Lattice QCD Consistent      | z ≈ 0.37σ agreement            |
  | [C]  | Calibrated                  | DESI/JWST/ACT anchored          |
  | [D]  | Predicted / Diagnostic      | Unconfirmed                     |
  | [E]  | Withdrawn / Speculative     | Retracted or motivational only  |

  For Antigravit2, ALL definitions are [D/E] unless a Lean proof
  is provided, in which case the proven statement is [A] (within
  the formal system — not a physics claim).

  Reference: UIDT_Ontology_v3_9_9.tex, Evidence System
  Reference: UIDT-OS RULES/02-evidence-system.md
-/

namespace Antigravit2.Meta

/-- [D/E] Evidence classification for UIDT claims and definitions.

    Used as documentation markers. In Lean, these serve as structured
    comments — the type checker does not enforce evidence grades,
    but human reviewers and CI tools can grep for them.
-/
inductive EvidenceGrade where
  | A      -- Mathematically proven (within formal system)
  | AMinus -- Phenomenologically determined
  | B      -- Lattice QCD consistent
  | C      -- Calibrated (DESI/JWST/ACT)
  | D      -- Predicted / unconfirmed / diagnostic
  | E      -- Withdrawn / speculative / motivational
  deriving Repr, DecidableEq

/-- [D/E] Anti-Target-Leakage discipline.

    Core principle: No proof may contain its own target as input.

    In Antigravit2, this means:
    1. The "desired" partition (e.g. [3,2,1] for N=6) MUST NOT appear
       in any definition, axiom, or hypothesis.
    2. It may only appear in the CONCLUSION of a theorem, derived
       from generic filter predicates applied to the full partition space.
    3. Any hard-coded "magic number" matching a known physical quantity
       is a red flag and must be justified by derivation.

    This cannot be enforced by the Lean type checker, but it CAN be
    enforced by code review and grep-based CI checks:
      grep -n "3, 2, 1" Antigravit2/**/*.lean
    should return results ONLY in theorem conclusions and test assertions,
    never in definitions or hypotheses.

    Reference: UIDT_Ontology_v3_9_9.tex (Anti-Target-Leakage, GSM-Origin-Gap)
-/
def antiTargetLeakagePolicy : String :=
  "No proof may contain its own target as input. " ++
  "The partition [3,2,1] must emerge as a RESULT, not an ASSUMPTION."

end Antigravit2.Meta
