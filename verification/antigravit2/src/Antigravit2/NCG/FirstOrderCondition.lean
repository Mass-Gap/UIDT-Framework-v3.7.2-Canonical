/-
  UIDT Phase 10b – First Order Condition Kernel
  Status: [D] Structural Program. Minimal Kernel.
  Project: UIDT-Framework-Canonical
-/

import Mathlib.Algebra.Group.Defs

namespace Antigravit2.NCG

/-- Opposite algebra wrapper to strictly separate left and right actions. -/
structure Opposite (A : Type _) where
  op : A

/-- 
  The core structural data of a Spectral Triple. 
  No physical matrix assignments, pure topological data.
-/
structure SpectralTripleCore (A H : Type _) where
  D : H → H
  J : H → H
  gamma : H → H
  leftRep : A → (H → H)
  rightRep : Opposite A → (H → H)

/--
  Commutator abstraction for endomorphisms.
-/
def Commute {H : Type _} (F G : H → H) : Prop :=
  ∀ x, F (G x) = G (F x)

/--
  First-Order Condition (FOC): 
  [ [D, a], b^o ] = 0 for all a \in A, b^o \in A^o.
  Formulated purely structurally as a Prop.
-/
def firstOrderCondition {A H : Type _} [AddGroup H] (ST : SpectralTripleCore A H) : Prop :=
  ∀ (a : A) (b_op : Opposite A),
    Commute (fun x => ST.D (ST.leftRep a x) - ST.leftRep a (ST.D x)) (ST.rightRep b_op)

end Antigravit2.NCG
