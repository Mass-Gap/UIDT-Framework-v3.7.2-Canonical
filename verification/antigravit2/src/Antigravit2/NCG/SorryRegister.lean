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

  [ALLOWED-P10] RNC Conjecture Seed
    Reason: The Phase 9 uniqueness proof `unique_321_N6` explicitly verifies 
            that [3,2,1] is the sole admissible N=6 partition under H1 ∧ H2.
            The general Relocation Necessity Conjecture (RNC) for arbitrary N 
            remains an open structural question (staircase topologies).
    Scope:  `unique_321_N6` itself is sorry-free (via native_decide). The 
            conjecture merely documents the boundary of the formalization.
    Target: Future phases mapping the RNC for higher moduli (N=10, 15).

  [NONE] All RealStructure.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All Bridge.lean lemmas — sorry-free as of 2026-06-30
  [NONE] All BlockPartition.lean lemmas — sorry-free as of 2026-06-30
-/

namespace Antigravit2
namespace NCG

-- Status: 5 instances in SpectralTriple.lean lines 98-103.

end NCG
end Antigravit2
