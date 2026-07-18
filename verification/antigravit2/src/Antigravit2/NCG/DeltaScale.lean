/-
  Antigravit2.NCG.DeltaScale
  ============================
  [D] — Documentary gap parameter stub.

  Phase 10a: Defines the spectral gap parameter Δ purely formally.
  Explicitly blocks physical assignment in the type system.
-/

import Mathlib.Data.Real.Basic

namespace Antigravit2.NCG

/-- [D] Formal spectral gap parameter.
    No physical value (like 1.710) is assigned here. -/
structure SpectralGapParam where
  delta : ℝ
  delta_pos : 0 < delta

/-- [D] Explicit blocker for premature physical identification.
    The glueball mass conjecture is stated as False in the formal core,
    preventing any theorem from accidentally relying on the identification
    Δ = M(0++). -/
def DeltaGlueballConjecture (Δ : ℝ) : Prop := False

end Antigravit2.NCG
