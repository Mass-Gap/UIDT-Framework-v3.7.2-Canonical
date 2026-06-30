/-
  Antigravit2.NCG.AxiomAudit
  ================================
  [D] — Axiom Audit & Integrity Check
  
  Dieses Modul dient der Sicherstellung, dass keine unerwünschten `sorry`-Marker
  oder gefährliche Axiome (wie unkontrolliertes `Classical.choice` in den
  komputablen Teilen) in die Kern-Lemmata einsickern.
-/

import Antigravit2.NCG.SpectralTriple
import Antigravit2.NCG.RealStructure
import Antigravit2.NCG.Bridge
import Antigravit2.MatrixThermo.BlockPartition

namespace Antigravit2
namespace NCG

-- Axiom-Fingerprints prüfen.
-- Darf `sorryAx` NICHT enthalten. (Achtung: Dies gibt nur im Editor/Build Logs aus)
#print axioms reality_JJ
#print axioms toSignature_totalDim
#print axioms MatrixThermo.entropyList_replicate_one
#print axioms trivialRealStruct

end NCG
end Antigravit2
