# Phase 7: NCG-Axiom-Initialisierung — Roadmap-Spezifikation

**Projekt:** Antigravit 2.0  
**Phase:** 7 — NCG-Axiom-Initialisierung  
**Status:** Bereinigter Planungsstand (30.06.2026)  
**Abgrenzung:** Phase 7 baut das Axiomskelett; Phase 8 verbindet es mit finiter Geometrie und Krajewski-Diagrammen.

---

## Ziel

Die bisher rein semantisch markierten Axiom-Felder in `SpectralTriple.lean` in **prüfbare mathematische Bedingungen** überführen, ohne klassische Feldtheorie in die relationale Ontologie einzuschleusen und ohne `J⁻¹` oder vollständige Hilbertraum-Adjungierte vorauszusetzen.

**Anti-Target-Leakage bleibt aktiv:** Keine Definition schreibt gewünschte Zielpartitionen oder physikalische Sieger in die Logik ein.

---

## Dateistruktur

```
Antigravit2/NCG/
├── RealStructure.lean      [NEU]    Phase 7.1–7.2
├── SpectralTriple.lean     [MODIFY] Phase 7.3–7.4
├── Bridge.lean             [MODIFY] Phase 7.5
└── ...
```

---

## 7.1 — AntiLinearMap

**Datei:** `RealStructure.lean`  
**Evidenzklasse:** [D] definitional

```lean
import Mathlib.Data.Complex.Basic
import Mathlib.Algebra.Module.Basic
import Mathlib.Algebra.Star.Basic

namespace Antigravit2.NCG

/-- [D] Anti-linear map over field K (typically ℂ).
    J(a • x) = conj(a) • J(x). Uses starRingEnd for field conjugation.
    NOTE: Not yet equipped with isometry/unitarity — that is Phase 8. -/
structure AntiLinearMap (K H : Type _) [IsROrC K] [AddCommGroup H] [Module K H] where
  toFun   : H → H
  map_add : ∀ x y, toFun (x + y) = toFun x + toFun y
  map_smul : ∀ (a : K) x, toFun (a • x) = starRingEnd K a • toFun x

instance {K H} [IsROrC K] [AddCommGroup H] [Module K H] :
    CoeFun (AntiLinearMap K H) (fun _ => H → H) where
  coe := AntiLinearMap.toFun
```

**Invariante:** `AntiLinearMap` modelliert nur Additivität und konjugierte Skalierung.  
Keine Aussagen über Invertierbarkeit, Isometrie oder Adjungiertheit in Phase 7.

---

## 7.2 — RealStructure Typklasse

**Datei:** `RealStructure.lean`  
**Evidenzklasse:** [D] axiomatisches Reality-Schema

```lean
/-- [D] RealStructure: encapsulates J and the three sign relations for KO-dimension.
    Phase 7: J is anti-linear but NOT required to be invertible or unitary here.
    J⁻¹ is explicitly EXCLUDED from Phase 7.
    The sign integers eps, epsD, epsγ ∈ {±1} will be linked to koSignTable in SpectralTriple.lean. -/
class RealStructure (H : Type _) [AddCommGroup H] [Module ℂ H] where
  J   : AntiLinearMap ℂ H
  eps   : ℤ
  epsD  : ℤ
  epsγ  : ℤ
  J_involutive : ∀ x,     J (J x) = (eps  : ℂ) • x
  JD_relation  : ∀ D x,   J (D x) = (epsD : ℂ) • D (J x)
  Jγ_relation  : ∀ γ x,   J (γ x) = (epsγ : ℂ) • γ (J x)

variable {H} [AddCommGroup H] [Module ℂ H] [r : RealStructure H]

lemma reality_JJ (x : H)         : r.J (r.J x) = (r.eps  : ℂ) • x := r.J_involutive x
lemma reality_JD (D : H → H) x   : r.J (D x)   = (r.epsD : ℂ) • D (r.J x) := r.JD_relation D x
lemma reality_Jγ (γ : H → H) x   : r.J (γ x)   = (r.epsγ : ℂ) • γ (r.J x) := r.Jγ_relation γ x
```

**Konvention:**
- Jede Reality-Relation wird als Lemma aus der Typklasse extrahiert (kein manuelles Entpacken im Nutzungscode).
- `eps`, `epsD`, `epsγ` werden erst in `SpectralTriple.lean` über `koSignTable` mit der KO-Dimension verknüpft.

---

## 7.3 — SpectralTriple-Integration

**Datei:** `SpectralTriple.lean`  
**Evidenzklasse:** [D] für Props, [B] für triviale Instanzen

### RepRespectsStar

```lean
/-- [D] Representation respects the star: ρ(a*) = ρ(a)* in the operator algebra.
    CAVEAT: [Star (H → H)] is an ABSTRACT assumption in Phase 7.
    No concrete mathlib instance for general H → H is assumed to exist yet.
    Will be replaced by a proper B(H) operator space in Phase 8/9. -/
def RepRespectsStar {A H} [Star A] [AddCommGroup H] [Module ℂ H] [Star (H → H)]
    (ρ : AlgebraRep A H) : Prop :=
  ∀ a : A, ρ.act (star a) = star (ρ.act a)
```

### FirstOrderCondition (Phase-7-Hülle)

```lean
/-- [D] Abstract First-Order Condition envelope for Phase 7.
    The concrete commutator form [[D, ρ(a)], J ρ(b)* J^{-1}] = 0 is NOT encoded here.
    Reason: J⁻¹ is excluded from Phase 7 (Gap Localization Before Construction).
    The body will be replaced in Phase 8 by an explicit operator composition
    once the operator space for ρ(a) carries a suitable adjoint/inverse structure.

    Phase 8 target form (do NOT implement yet):
      ∀ a b, [D ∘ ρ(a) - ρ(a) ∘ D, J ∘ ρ(b*) - ρ(b*)^op ∘ J] = 0 -/
def FirstOrderCondition {A H} [Star A] [AddCommGroup H] [Module ℂ H] [Star (H → H)]
    (ρ : AlgebraRep A H) (D : H → H) (J : AntiLinearMap ℂ H) : Prop :=
  ∀ _a _b : A, True  -- Phase-7 placeholder; see docstring above
```

### SpectralTriple-Struktur

```lean
/-- [D] Finite spectral triple. Phase 7 version.
    Injects RealStructure as a typeclass parameter.
    realityCondition links the sign integers to koSignTable.
    firstOrderCondition is a placeholder (True) pending Phase 8.
    [Star (H → H)] is an abstract assumption, not a concrete mathlib instance. -/
structure SpectralTriple (A H : Type _)
    [Star A] [AddCommGroup H] [Module ℂ H] [Star (H → H)] where
  rep       : AlgebraRep A H
  D         : H → H
  gamma     : H → H
  KO_dim    : Fin 8
  signature : FiniteAlgebraSignature
  [realStruct : RealStructure H]
  repRespectsStar    : Prop := RepRespectsStar rep
  firstOrderCond     : Prop := FirstOrderCondition rep D realStruct.J
  orientable         : Prop := Orientable rep gamma
  realityCondition   : Prop :=
    let (e, eD, eG) := koSignTable KO_dim.val
    realStruct.eps = e ∧ realStruct.epsD = eD ∧ realStruct.epsγ = eG
```

---

## 7.4 — Triviales Tripel (Regression)

**Datei:** `SpectralTriple.lean` (Regressionsabschnitt)  
**Evidenzklasse:** [B] Kohärenzbeweis der Architektur

```lean
/-- Trivial RealStructure on ℂ: J = complex conjugation, all signs = 1.
    Used to verify that the Phase-7 architecture is self-consistent. -/
instance : RealStructure ℂ where
  J := {
    toFun    := fun x => starRingEnd ℂ x
    map_add  := by intros; simp
    map_smul := by intros; simp [starRingEnd, map_mul]
  }
  eps := 1; epsD := 1; epsγ := 1
  J_involutive := by intros; simp [starRingEnd]
  JD_relation  := by intros; simp [starRingEnd]
  Jγ_relation  := by intros; simp [starRingEnd]

/-- Regression: trivial triple on ℂ satisfies realityCondition for KO_dim with all signs 1. -/
example : (trivialTriple.realStruct.eps  = 1) ∧
          (trivialTriple.realStruct.epsD = 1) ∧
          (trivialTriple.realStruct.epsγ = 1) := by decide
```

---

## 7.5 — Bridge.lean Anpassungen

**Datei:** `Bridge.lean`

- `BlockPartition.toTrivialTriple` erhält `[RealStructure ℂ]` als implizite Instanz.
- Alle bisherigen `rfl`-Regressionen zu `p321` etc. bleiben unverändert (kombinatorische Ebene ist von Phase 7 unberührt).
- Kommentar ergänzen: „RealStructure-Instanz wird in Phase 8 gegen eine echte endlich-dimensionale Darstellung ausgetauscht."

---

## Evidenzklassen-Übersicht

| Definition / Lemma           | Klasse | Begründung                                         |
|------------------------------|--------|----------------------------------------------------|
| `AntiLinearMap`              | [D]    | Reine algebraische Struktur, kein physikalischer Inhalt |
| `RealStructure`              | [D]    | Axiomatisches Schema aus NCG-Literatur             |
| `reality_JJ/JD/Jγ`          | [D]    | Direkte Extraktion aus Typklasse                   |
| `RepRespectsStar`            | [D]    | Star-Kompatibilität der Darstellung                |
| `FirstOrderCondition`        | [D]    | Phase-7-Hülle; Konkretisierung in Phase 8          |
| `[Star (H → H)]`             | [E]    | Heuristische Annahme; kein konkretes mathlib-Objekt |
| Triviale RealStructure auf ℂ | [B]    | Kohärenz-Regression; beweist Architektur-Konsistenz |

**Legende:** [D] definitional · [E] heuristisch/abstrakt · [B] Regressionsbeweis

---

## Explizit ausgeschlossen in Phase 7

1. `J⁻¹` in jeder Form (weder über `ε • J` noch als Isomorphismus).
2. Konkrete `Star (H → H)`-Implementierung (nur als Annahme).
3. Volle NCG-Kommutatorform in `FirstOrderCondition`.
4. Isometrie/Unitarizität von `J`.
5. Unbeschränkte Operatoren / Domänenfragen.
6. Krajewski-Diagramme und Poincaré-Dualität (→ Phase 8).

---

## Übergabe an Phase 8

Phase 8 übernimmt genau dort, wo Phase 7 aufhört:

| Phase 7 Platzhalter                     | Phase 8 Konkretisierung                                  |
|-----------------------------------------|----------------------------------------------------------|
| `[Star (H → H)]` abstrakt              | Konkreter Operatorraum `B(H)` oder `End_fin H`           |
| `FirstOrderCondition := True`           | Explizite Kommutatorgleichung ohne `J⁻¹`                 |
| `RealStructure` unabhängig von Geometrie | Verknüpfung mit Krajewski-Diagrammen                     |
| `koSignTable` nur als Prop-Link         | Klassifikation aller 8 KO-Dimensionen                    |
| Triviale Tripel auf `ℂ`                | Endlich-dimensionale Matrixdarstellungen                  |

---

## Verifikationsplan

```
lake build Antigravit2.NCG.RealStructure
lake build Antigravit2.NCG.SpectralTriple
lake build Antigravit2.NCG.Bridge
```

Erwartetes Ergebnis:
- Keine `sorry` in Kernlemmas von `RealStructure.lean`.
- Triviale-Tripel-Regression beweisbar durch `decide` oder `simp`.
- Bestehende `p321`-Regressionen in `Bridge.lean` unverändert grün.
