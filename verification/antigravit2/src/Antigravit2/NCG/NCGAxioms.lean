/-
  UIDT Phase 10b – NCG Axioms Layer
  Status: [D] Structural Program.
  Project: UIDT-Framework-Canonical
-/

import Antigravit2.NCG.FirstOrderCondition

namespace Antigravit2.NCG

/--
  Order Zero Condition: left and right actions commute.
-/
def orderZeroCondition {A H : Type _} (ST : SpectralTripleCore A H) : Prop :=
  ∀ (a : A) (b_op : Opposite A), Commute (ST.leftRep a) (ST.rightRep b_op)

/--
  Reality Condition: Commutativity (or anti-commutativity up to signs) between J and D.
  For structural topology at Phase 10b, we abstract this as an uninterpreted commuting constraint,
  often J D = \epsilon D J. We simplify to general structural commute for the Kernel.
-/
def realityCondition {A H : Type _} (ST : SpectralTripleCore A H) : Prop :=
  -- abstract representation of J and D interacting
  Commute ST.J ST.D

/--
  Grading Involution: gamma^2 = 1.
-/
def gradingInvolution {A H : Type _} (ST : SpectralTripleCore A H) : Prop :=
  ∀ x, ST.gamma (ST.gamma x) = x

/--
  Grading Anti-Commutes with D: D gamma + gamma D = 0.
-/
def gradingAnticommutesWithD {A H : Type _} [AddGroup H] (ST : SpectralTripleCore A H) : Prop :=
  ∀ x, ST.D (ST.gamma x) + ST.gamma (ST.D x) = 0

/--
  Orientability Condition: Conjunction of grading involution and anti-commutativity with D.
-/
def orientabilityCondition {A H : Type _} [AddGroup H] (ST : SpectralTripleCore A H) : Prop :=
  gradingInvolution ST ∧ gradingAnticommutesWithD ST

/--
  Admissible Spectral Triple Moduli-Filter.
  Requires FOC, Order Zero, Reality, and Orientability.
-/
structure AdmissibleSpectralTriple {A H : Type _} [AddGroup H] (ST : SpectralTripleCore A H) : Prop where
  foc : firstOrderCondition ST
  orderZero : orderZeroCondition ST
  reality : realityCondition ST
  orientability : orientabilityCondition ST

end Antigravit2.NCG
