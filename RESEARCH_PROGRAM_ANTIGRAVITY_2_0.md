# Antigravity 2.0 — Forschungsprogramm und Handout

## 1. Zielsetzung

Antigravity 2.0 ist ein **offenes Forschungsprogramm** zur formalen Untersuchung der Frage, ob und wie prägeometrische Strukturen, Matrixmodelle und nichtkommutative Geometrie zu einer effektiven Raumzeit und zur Standardmodell-Struktur führen können. 
Das Programm behauptet **nicht**, dass diese Ableitung bereits bewiesen ist; vielmehr isoliert es die offenen Brücken zwischen kombinatorischer Vorstruktur, Spektralgeometrie und physikalischer Zielstruktur als präzise prüfbare mathematische Probleme.

Die Leitidee ist dabei deflationär: Jede stark motivierte, aber noch nicht bewiesene Ableitung wird als **Arbeits-Hypothese** behandelt, nicht als bereits gesicherte Theorie. Der biologische Beobachter- bzw. Forgetful-Functor-Block bleibt ausdrücklich spekulativ und gehört in Evidenzklasse **[E]**.

## 2. Was die Literatur stützt

Die Literatur bestätigt, dass **prägeometrische Konzepte** wie Matrixmodelle, Tensor-Netzwerke und Hintergrund-unabhängige Ansätze seit Jahrzehnten ernsthaft untersucht werden. 
Sie bestätigt auch, dass die nichtkommutative Spektralgeometrie die Standardmodell-Algebra \(A=\mathbb C \oplus \mathbb H \oplus M_3(\mathbb C)\) als konsistente Lösung hervorbringt, insbesondere unter starken Axiomen und in der Analyse finiter Spektraltripel.

Für Matrixmodelle zeigt die Literatur, dass emergente \((3+1)\)-Dimensionen und Signaturwechsel in IKKT-/BFSS-ähnlichen Systemen **möglich** sind, jedoch modellabhängig, numerisch und mit zusätzlichen Annahmen verbunden.
Für Lean 4 ist ebenfalls klar: mathlib4 enthält bereits tragfähige Bausteine wie `CStarAlgebra`, doch Spektraltripel und NCG-Kernobjekte sind noch nicht als fertige Standardbibliothek verfügbar.

## 3. Was offen bleibt

Es gibt bis heute **kein allgemein anerkanntes Theorem**, das aus einem rein prägeometrischen Fundament zwingend die effektive \((3+1)\)-Raumzeit und genau die Standardmodell-Algebra herleitet.
Die Literatur liefert starke Einschränkungen, Klassifikationen und Spezialfälle, aber keinen target-unabhängigen Selektionssatz, der alle Alternativen eliminiert.

Der zentrale „**Origin Gap**“ besteht daher in drei Brücken:
1. Prägeometrische Algebra \(\to\) Spektraltripel.
2. Spektraltripel \(\to\) eindeutige Standardmodell-Algebra.
3. Spektraltripel \(\to\) effektive Lorentz-Signatur \((3+1)\).

## 4. Gap-Localization

Die Deep-Research-Literatur lokalisiert die Beweislücke genauer in vier Transitionsstufen:

### Transition 1: Matrixdynamik \(\to\) Thermodynamik
Matrixmodelle können im Hochtemperaturlimes thermische effektive Beschreibungen zeigen, aber der thermische Zustand selbst ist in der Regel **ein externer Rahmen**, nicht automatisch eine Lösung der reinen Dynamik.
Die spontane Symmetriebrechung zu drei großen Raumdimensionen ist beobachtet oder numerisch unterstützt, aber nicht als universeller, rein kombinatorischer Zwang bewiesen.

### Transition 2: Thermodynamik \(\to\) kanonische Signatur
Die Thermal-Time-Hypothese und Tomita-Takesaki-Modulartheorie liefern eine intrinsische algebraische Zeitentwicklung, aber kein allgemeines Theorem, das daraus zwingend eine physikalische Lorentz-Signatur erzeugt.
Der Schritt von modularer Dynamik zur konkreten Raumzeit-Signatur bleibt daher eine offene Brücke, auch wenn Rindler-/Unruh-artige Spezialfälle mathematisch gut kontrolliert sind.

### Transition 3: Signatur \(\to\) Spektralgeometrie
Pseudo-Riemannsche und getwistete Spektraltripel zeigen, dass Signatureffekte formal modellierbar sind, aber die Wahl des Twist-Operators bleibt ein zusätzlicher Freiheitsgrad und kein aus den vorigen Schichten zwingend abgeleiteter Satz.
Der Übergang von euklidischer NCG zu lorentzscher Struktur ist daher weiterhin eine offene Konstruktion und kein allgemein erzwungener Schluss.

### Transition 4: Spektralgeometrie \(\to\) Standardmodell-Algebra
Krajewski-Diagramme und Klassifikationen endlicher Spektraltripel zeigen starke Restriktionen und reproduzieren die Standardmodell-Struktur als zulässige Lösung, aber nicht als abschließend bewiesene **einzige** Lösung.
Neuere Ansätze wie Accessibility Theory oder Universal Accessibility Balance werden hier als target-leaky behandelt: Die Zielfunktion ist maßgeschneidert und erhält deshalb keine höhere Evidenzklasse.

## 5. Phasenkarte 1–10

| Phase | Fokus | Kernartefakte | Status | Bewertung |
|---|---|---|---|---|
| 1 | Kombinatorischer Kern | `BlockPartition`, `entropy`, `offDiagPenalty` | Abgeschlossen | Fundament für spätere Filter. |
| 2 | Admissibility | `filter1`, `filter2`, `admissible` | Abgeschlossen | Definitionale und heuristische Regeln getrennt. |
| 3 | Enumeration | kleine Partitionen, mathlib-Parallelmodell | Abgeschlossen | Innerhalb der Lean-Pipeline formal definiert und regressionstauglich. |
| 4 | Repräsentation | `AlgebraRep`, `FiniteAlgebraSignature`, `Bridge` | Abgeschlossen | Strukturträger für spätere Axiome. |
| 5 | Axiom-Schicht | Prop-Marker, Kanonizität, `SpectralTriple`-Props | Abgeschlossen | Semantische Platzhalter. |
| 6 | Marker → Hüllen | `RepUnital`, `FirstOrderCondition`, `Orientable`, `Reality` | Abgeschlossen | Erste formale NCG-Hüllen. |
| 7 | NCG-Axiom-Initialisierung | `SpectralTriple`, `AlgebraRep` als Constraints | Geplant | Echte NCG-Bedingungen aufbauen. |
| 8 | Endliche Geometrie | `KrajewskiDiagram` | Geplant | Zulässige finite Geometrien auditieren. |
| 9 | Dualität / Index | `IntersectionForm`, `PoincaréDuality`, KO-Abgleich | Geplant | Nichtentartung und KO-Konsistenz prüfen. |
| 10 | Target-Mapping | \((3,2,1)\), \(\mathbb C \oplus \mathbb H \oplus M_3(\mathbb C)\) | Geplant | Origin Gap target-unabhängig testen. |

Wichtig: Phase 3 ist **innerhalb der Lean-Pipeline formal definiert und regressionstauglich**, aber nicht als allgemeines physikalisches Theorem zu lesen.
Phase 7 bis 10 sind die eigentliche offene Forschungsfront, auf der Target-Leakage und Eindeutigkeitsfragen geprüft werden müssen.

## 6. Teilclaims für die Bearbeitung

Die Arbeit sollte in stratifizierte Teilclaims zerlegt werden:

- **S1:** Matrixdynamik \(\Rightarrow\) Thermodynamik. Modellabhängig und derzeit nur \(D\).
- **S2:** Thermodynamik \(\Rightarrow\) Blockpartition. Formal in Lean vorbereitet, aber physikalisch noch handbasiert \(D\).
- **S3:** Blockpartition \(\Rightarrow\) kanonische Signatur. Innerhalb der Pipeline formal definiert und regressionstauglich, aber kein Naturgesetz.
- **S4:** Signatur \(\Rightarrow\) NCG-Filter. Noch unbewiesen; Lean-Statements über `SpectralTriple`, `KrajewskiDiagram`, `IntersectionForm` sind hier zentral.
- **S5:** Forgetful Functor. Spekulativ; Evidenzklasse **[E]**.

## 7. Lean 4 als Prüfstein

Lean 4 ist für dieses Programm kein Ersatz für Mathematik, sondern ein **deflationärer Prüfstein**.
Die Bibliothek bietet bereits wichtige Grundlagen wie `CStarAlgebra`, aber keine fertigen NCG-Spektraltripel; genau deshalb ist Lean geeignet, die Lücken sichtbar zu machen statt sie zu überdecken.

Das Programm nutzt Lean in drei Rollen:
1. **Regression:** Kleine Beispiele und Enumerationen absichern.
2. **Audit:** Target-Leakage, zusätzliche Annahmen und versteckte Gewichtungen aufdecken.
3. **Brückenbau:** Die schrittweise Verknüpfung der Ebenen mathematisch rigoros nachvollziehen.
