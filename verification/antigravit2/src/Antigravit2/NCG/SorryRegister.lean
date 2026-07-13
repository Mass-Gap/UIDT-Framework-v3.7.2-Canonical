/-
  Antigravit2.NCG.SorryRegister
  ================================
  SORRY REGISTER — Phase 7
  
  Jeder Eintrag referenziert die Datei, das Lemma, den Grund und die Zielphase
  für die Auflösung des `sorry`-Markers. Dies stellt sicher, dass kein `sorry` 
  "stumm" im Code überlebt und unbeabsichtigte axiomatische Lücken reißt.

  [ALLOWED-P8] canonicalBlocks Regression (SpectralTriple.lean)
    Reason: `canonicalBlocks` basiert auf `List.mergeSort`. Der Elaborator 
            reduziert dies nicht rein strukturell in endlicher Zeit (non-computable 
            oder sehr tiefe rekursive Reduktion ohne simp/decide lemmas). 
    Scope:  Isolation in `Enumeration.lean`. `canonicalBlocks` taucht in 
            keinem Prop der NCG-Hierarchie (`toTrivialTriple`, `SpectralTriple`) auf. 
            (Transitiv verifiziert via `#print axioms toTrivialTriple` -> no `sorryAx`).
    Target: Phase 8 (Entwicklung spezifischer Decidability-Lemmas für Partitionen).

  [OPEN-P10] unique_321_N6 and its supporting decidability lemmas — NOT sorry-free
    Reason: The Phase 9 uniqueness statement `unique_321_N6` asserts that [3,2,1]
            is the sole admissible N=6 partition under H1 ∧ H2. As of 2026-07-13
            this statement is stated but not proved: `unique_321_N6`
            (EliminationN6.lean:226) is `:= sorry`, not `native_decide` as this
            register previously claimed. All 33 supporting per-partition example
            checks for `intersectionFilter`, `massNondeg`, and `phase9Admissible`
            (EliminationN6.lean:128-183) are likewise `:= sorry`. Total: 34 open
            `sorry` markers in EliminationN6.lean, none currently discharged.
    Scope:  The RNC conjecture (general-N staircase claim) remains correctly
            documented as open and out of scope for N=6. It is unaffected by
            this correction. `#print axioms Filters.unique_321_N6` (see
            AxiomAudit.lean:36) will report `sorryAx` until these are closed.
    Target: Phase 9 completion — discharge via `native_decide` or exhaustive
            `decide` over `partitions6` (finite, `p(6)=11`), then re-verify via
            `#print axioms` before this entry may be reclassified [ALLOWED].
    Audit:  Correction recorded 2026-07-13 (Sonnet role, mechanical hygiene,
            S-3). See PR TKT-2026-07-13-lean-f1-sorry-register-audit.

  [NONE] All RealStructure.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All Bridge.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All BlockPartition.lean lemmas — sorry-free as of 2026-06-30
-/

namespace Antigravit2
namespace NCG

-- Status: 5 instances in SpectralTriple.lean lines 98-103.

end NCG
end Antigravit2
