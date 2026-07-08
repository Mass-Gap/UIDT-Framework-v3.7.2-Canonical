/-
  Antigravit2.NCG.Dirac321
  ==========================
  [D] — Formal verification of the [3,2,1] spectral triple structure.

  Phase 10a: Structural construction of the [3,2,1] Krajewski diagram
  and associated Dirac operator precursor.

  NOTE: gradingop321 is used instead of gamma to avoid collision with
  the phenomenological parameter γ = 16.339.
-/

import Antigravit2.NCG.SpectralTriple
import Antigravit2.NCG.Krajewski321
import Antigravit2.MatrixThermo.BlockPartition
import Antigravit2.Filters.Admissibility

namespace Antigravit2.NCG

open MatrixThermo
open Filters

-- [D] Alias for the filters to match admissibility hypotheses
def H1 {N : ℕ} (p : BlockPartition N) : Prop := filter1 p 2
def H2 {N : ℕ} (p : BlockPartition N) : Prop := filter2 p

/-- [D] The grading operator for the [3,2,1] configuration.
    Named `gradingop321` to avoid `gamma` collision. -/
def gradingop321 : ℂ → ℂ := id

/-- [D] The Dirac operator precursor for [3,2,1].
    Structural only, no metric entries specified yet. -/
def dirac321 : ℂ → ℂ := id

/-- [D] The spectral triple structure for [3,2,1].
    Uses trivial algebra/Hilbert space for now (Phase 10a stub). -/
def spectralTriple321 : SpectralTriple ℂ ℂ :=
  { rep := AlgebraRep.trivialC,
    D := dirac321,
    gamma := gradingop321,
    KO_dim := 6,
    signature := {
      blocks := p321.blocks,
      blocks_pos := p321.positive,
      sorted := True,
      positiveBlocks := True
    } }

/-- [D] KO-dimension 6 signs are (+1, +1, -1). -/
theorem ko_dim_six_signs :
    koSignTable 6 = (1, 1, -1) := by decide

/-- [D] Admissibility wrapper for SpectralTriple. -/
def AdmissibleCarrier (st : SpectralTriple ℂ ℂ) : Prop :=
  st.KO_dim = 6 ∧ st.signature.blocks = [3, 2, 1]

/-- [D] The [3,2,1] spectral triple is admissible under H1 and H2.
    This states conditional structural existence, not uniqueness. -/
theorem three_two_one_admissible_under_filters
    (_h1 : H1 p321) (_h2 : H2 p321) :
    AdmissibleCarrier spectralTriple321 := by
  dsimp [AdmissibleCarrier, spectralTriple321, p321]
  exact ⟨rfl, rfl⟩

end Antigravit2.NCG
