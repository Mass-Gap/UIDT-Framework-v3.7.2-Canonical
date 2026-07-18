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

  [CLOSED-P10] unique_321_N6 and its supporting decidability lemmas
    Reason: The Phase 9 uniqueness statement `unique_321_N6` and its supporting
            33 per-partition checks were successfully discharged via `by decide` and
            `rfl`. They are now completely sorry-free.
            The statement evaluates to [A] under the stated assumptions: H1 (intersectionFilter,
            DESIGN-LEVEL) and H2 (massNondeg, HEURISTIC) as defined in EliminationN6.lean.
            The [A] covers the formal implication, not the physical adequacy of the filters.
            The 2026-07-13 history is retained for auditing.
    Scope:  Axiom audit verifies this closure:
            `info: src/Antigravit2/NCG/AxiomAudit.lean:35:0: 'Antigravit2.Filters.unique_321_N6' depends on axioms: [propext]`
    Target: Completed.

  [ALLOWED-P10] List.Sorted Enumeration Regression (Enumeration.lean)
    Reason: The `List.Sorted (· ≥ ·)` decidability for partitions hangs the elaborator 
            infinitely without `native_decide` (which would introduce `Lean.ofReduceBool`). 
    Scope:  3 instances in Enumeration.lean lines 77-79. 
    Target: Phase 10 — Decidability optimizations for decreasing sorts.

  [NONE] All RealStructure.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All Bridge.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All BlockPartition.lean lemmas — sorry-free as of 2026-06-30
-/

namespace Antigravit2
namespace NCG

-- Status: 5 instances in SpectralTriple.lean lines 98-103.
-- Status: 3 instances in Enumeration.lean lines 77-79.

end NCG
end Antigravit2
