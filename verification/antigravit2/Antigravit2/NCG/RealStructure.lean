/-
  Antigravit2.NCG.RealStructure
  ================================
  [D] — Axiomatic RealStructure Schema. No physical claim.

  Phase 7: Anti-linear map definition and RealStructure typeclass.
  J is anti-linear but NOT required to be invertible or unitary here.
  J⁻¹ is explicitly EXCLUDED from Phase 7.
-/

import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Star.Basic

namespace Antigravit2
namespace NCG

/-- [D] Anti-linear map over field ℂ.
    J(a • x) = conj(a) • J(x). Uses starRingEnd for field conjugation.
    NOTE: Not yet equipped with isometry/unitarity — that is Phase 8. -/
structure AntiLinearMap (H : Type _) [AddCommGroup H] [Module ℂ H] where
  toFun   : H → H
  map_add : ∀ x y, toFun (x + y) = toFun x + toFun y
  map_smul : ∀ (a : ℂ) x, toFun (a • x) = starRingEnd ℂ a • toFun x

instance {H} [AddCommGroup H] [Module ℂ H] :
    CoeFun (AntiLinearMap H) (fun _ => H → H) where
  coe := AntiLinearMap.toFun

/-- [D] RealStructure: encapsulates J and the three sign relations for KO-dimension.
    Phase 7: J is anti-linear but NOT required to be invertible or unitary here.
    J⁻¹ is explicitly EXCLUDED from Phase 7.
    The sign integers eps, epsD, epsγ ∈ {±1} will be linked to koSignTable in SpectralTriple.lean. -/
class RealStructure (H : Type _) [AddCommGroup H] [Module ℂ H] where
  J   : AntiLinearMap H
  eps   : ℤ
  epsD  : ℤ
  epsγ  : ℤ
  J_involutive : ∀ x,     J (J x) = (eps  : ℂ) • x

variable {H : Type _} [AddCommGroup H] [Module ℂ H] [r : RealStructure H]

lemma reality_JJ (x : H)         : r.J (r.J x) = (r.eps  : ℂ) • x := r.J_involutive x

end NCG
end Antigravit2
