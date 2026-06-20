# UIDT-Framework-V3.9-UNIVERSUM_SIM — Long-Term Roadmap

## Ausgangslage

Das Repository ist ein separates experimentelles Pregeometry-Workspace, nicht das kanonische UIDT-v3.9-Repository. Alle Arbeiten bleiben advisory und dürfen weder Merge-Autorisierung noch Evidenz-Upgrade ersetzen.

Aktueller Stand:

* PR #1: Null-ensemble diagnostics, Draft/Open, review-stabil als Draft. [A]
* PR #2: Spectral graph diagnostics pre-registration only, Draft/Open, review-stabil als Draft. [A]
* PR-2 implementation code: noch nicht implementiert. [A]
* Letzter bekannter lokaler Teststand aus PR #1/PR #2-Kontext: `43 passed in 4.30s`. [A]
* Alle physikalischen Interpretationen bleiben [D/E].
* Graphdiagnostiken bleiben [D].
* Software-Pfade, Guards und Tests dürfen nur als [A] für exakt ausgeführte Softwareinvarianten formuliert werden.

---

## Leitprinzip

Das Projekt soll nicht versuchen, früh physikalische Aussagen zu erzwingen. Der korrekte Weg ist:

1. Software-Harness stabilisieren. [A]
2. Graphdiagnostiken präregistrieren und implementieren. [D]
3. Nullmodelle und Falsifikationspfade erweitern. [D]
4. Observer-Map-Stabilität testen. [D]
5. Erst danach kontrollierte Interpretation als [D/E] zulassen.
6. Keine Evidenzklasse auf [A], [A-] oder [B] anheben ohne externe Gegenprüfung und formale Governance.

---

## Arbeitsstrang A — Governance und Repository-Hygiene

Ziel: Das Repository auditierbar halten.

Erlaubte Arbeiten:

* PR-Body-Hygiene.
* Guard-Skripte schärfen.
* Forbidden-label scans erweitern.
* Evidence-tag scanner erweitern.
* Root-artifact guard stabilisieren.
* PR templates härten.
* AI-agent policy und `AGENTS.md` minimal halten.

Nicht erlaubt:

* Merge-Autorisierung durch AI.
* Auto-merge.
* Approval durch AI.
* Änderungen an `main` oder `master` als direkte Agentenaktion.
* Evidence-Upgrades ohne Governance.

Exit-Kriterium:

* Jeder PR enthält Scope, Evidence-Klassen, Reproduktion, Grenzen, Guard-Status und explizite Nicht-Merge-Formulierung. [A]

---

## Arbeitsstrang B — PR-2 Implementation: Spectral Graph Diagnostics [D]

Ziel: PR-2 nach der Pre-Registration als reine Graphdiagnostik implementieren.

Erlaubte Diagnostiken:

* combinatorial graph Laplacian spectrum. [D]
* normalized Laplacian spectrum. [D]
* adjacency spectrum. [D]
* spectral gap as graph diagnostic, not physical mass gap. [D]
* eigenvalue summary statistics. [D]
* spectral entropy as graph statistic. [D]
* null-ensemble comparison. [D]
* observer-map stability diagnostic. [D]

Nicht erlaubt:

* Spacetime-dimension claim.
* metric-emergence claim.
* cosmology claim.
* gauge claim.
* Yang-Mills claim.
* empirical-validation claim.
* physical mass-gap claim.

Erwartete Dateien:

```text
verification/pregeometry/spectral_diagnostics.py
verification/pregeometry/observer_stability.py
verification/pregeometry/experiments/run_pr2_spectral_diagnostics.py
verification/pregeometry/reports/write_pr2_report.py
verification/tests/test_pregeometry_pr2.py
```

Output-Ort:

```text
verification/data/pregeometry/pr2/
```

Exit-Kriterium:

* Deterministische Spektraldiagnostiken laufen gegen PR-0 toy graph und PR-1 null ensembles. [A]
* Reports nennen alle Spektralgrößen ausschließlich Graphdiagnostiken [D].
* Keine verbotene physikalische Zielrhetorik im sichtbaren Text. [A]

---

## Arbeitsstrang C — PR-3 Causal Propagation Diagnostics [D]

Ziel: Die brauchbaren Teile aus dem eingefügten Modul-Text entkernen und repository-sicher machen.

Erlaubt:

* BFS arrival ticks. [A/D]
* shortest-path latency. [A/D]
* finite graph propagation rule: one tick crosses at most one edge. [A]
* shortcut-edge diagnostic. [D]
* degree-density proxy. [D]
* Jaccard redundancy forgetting candidate. [D/E]

Nicht erlaubt:

* Lichtgeschwindigkeit als bewiesen.
* Lieb-Robinson-Beweis ohne Hamiltonian.
* Entanglement-Signalübertragung.
* ER=EPR-Claim.
* Confinement.
* Hadronisierung.
* Yang-Mills.
* `gamma`, `Delta`, `E_T` als operative Inputs.
* `N=256` als Target-Matching-Cutoff.

Erwartete Dateien:

```text
verification/pregeometry/PRE_REGISTERED_PR3_CAUSAL_PROPAGATION_DIAGNOSTICS.md
verification/pregeometry/causal_diagnostics.py
verification/pregeometry/shortcut_diagnostics.py
verification/pregeometry/degree_density.py
verification/tests/test_pregeometry_causal_diagnostics.py
```

Exit-Kriterium:

* BFS arrival tick equals shortest-path distance for all node pairs in tested unweighted graphs. [A]
* Shortcut edge lowers graph distance only when the edge was absent before. [A]
* Degree-density proxy has mean one by construction. [A]
* All interpretation remains [D/E].

---

## Arbeitsstrang D — Nullmodelle und Falsifikation

Ziel: Das Projekt darf nicht nur UIDT-toy intern messen. Jede Diagnostik braucht robuste Gegenmodelle.

Ausbau:

* Erdős-Rényi null ensemble. [D]
* random DAG null ensemble. [D]
* degree-preserving shuffle preserving final PR-0 degree sequence. [A/D]
* preferential attachment null ensemble. [D]
* bounded-degree null ensemble. [D]
* lattice-like synthetic null without coordinate leakage, sofern rein graphisch definiert. [D]
* permutation diagnostics. [D]
* bootstrap uncertainty diagnostics. [D]

Exit-Kriterium:

* Jede neue Metrik wird gegen mehrere Nullensembles ausgewertet. [D]
* Nonzero separation wird nur als distinguishability from selected nulls formuliert. [D]

---

## Arbeitsstrang E — Observer-Map Stability

Ziel: Prüfen, ob Diagnostiken stabil bleiben, wenn der Beobachter die Graphdaten anders zusammenfasst.

Erlaubt:

* node relabeling invariance. [A]
* edge-order invariance. [A]
* coarse-graining stability. [D]
* subsampling stability. [D]
* observer-map perturbation stability. [D]
* report of instability as negative result. [D]

Nicht erlaubt:

* Beobachterkarte als physikalische Raumzeit interpretieren.
* Visualisierung als Metrikbeweis verwenden.
* Force-directed layout als physikalischen Raum darstellen.

Exit-Kriterium:

* Jede sichtbare Visualisierung trägt die Grenze: "topological debug layout, non-metric". [A/D]
* Keine Screenshots als Datenersatz.

---

## Arbeitsstrang F — Dashboard und Reports

Ziel: Das Dashboard bleibt read-only und dient nur der wissenschaftlichen Inspektion.

Erlaubt:

* Anzeige von PR-2 spectral graph diagnostics. [D]
* Anzeige von null-ensemble deltas. [D]
* Anzeige von invariants and test metadata. [A]
* SHA256 hashes von Run-Dateien. [A]
* passive report viewer. [A]

Nicht erlaubt:

* Dashboard erzeugt Simulationsergebnisse.
* Dashboard verändert Daten.
* Dashboard enthält physikalische Zielclaims.
* 3D-universe view.
* spacetime/metrische Renderer.

Exit-Kriterium:

* Dashboard bleibt rein passiver Reader. [A]
* Tests prüfen read-only boundary. [A]

---

## Arbeitsstrang G — Manuskript- und Ledger-Integration

Ziel: Nur reproduzierbare, korrekt getaggte Ergebnisse in Ledger oder Manuskript übernehmen.

Übernahmefähig:

* software-path invariants. [A]
* nullmodel distinguishability. [D]
* graph diagnostic separation. [D]
* negative results and failed checks. [D/E]
* limitations and open residuals. [D/E]

Nicht übernahmefähig:

* Chat-basierte Modul-Resultate ohne Code.
* Platzhalterzahlen.
* Werte mit Musterfolgen.
* Post-hoc Treffer.
* Overclaiming aus Sandbox-Läufen.
* "N=256 hit" als Evidenz.

Exit-Kriterium:

* Jeder Ledger-Eintrag enthält Claim, method, exact code path, evidence class, residuals, limitations and reproduction command. [A/D]

---

## Arbeitsstrang H — External Audit und Literatur

Ziel: Externe Claims nur nach Audit nutzen.

Regeln:

* DOI/arXiv/journal/authors/status prüfen.
* Keine fake DOI/arXiv akzeptieren.
* Keine unmöglichen Unsicherheiten akzeptieren.
* Keine externen Werte ohne Herkunft.
* Bei Konflikt mit UIDT ledger: `[TENSION ALERT]`.

Exit-Kriterium:

* Jeder externe Bezug ist auditierbar und getrennt von UIDT-Interpretation. [B/C/D]

---

## Arbeitsstrang I — Release-Disziplin

Ziel: Releases nicht als wissenschaftliche Autorisierung missverstehen.

Release-Typen:

* `experimental-pregeometry-alpha`: Software-Harness. [A]
* `diagnostic-null-ensemble-alpha`: Nullmodell-Diagnostik. [D]
* `spectral-graph-diagnostics-alpha`: PR-2 Graphdiagnostik. [D]
* `causal-propagation-diagnostics-alpha`: PR-3 Graphlatenz. [D]
* `observer-stability-alpha`: Observer-map robustness. [D]

Jeder Release muss enthalten:

* scope.
* evidence class.
* reproduction command.
* known limitations.
* forbidden claims.
* no merge/approval equivalence.
* no canonical UIDT-v3.9 claim.

---

## Arbeitsstrang J — Langfristige Forschungsgrenze

Erst wenn die Graphdiagnostik, Nullmodelle, Observer-Stabilität und Falsifikationsberichte robust sind, darf ein separater Research-Branch spekulative physikalische Interpretation strukturieren.

Dort weiterhin verboten:

* "solves".
* "proves".
* "derived from first principles".
* "closes the tension".
* "physical validation".
* "Yang-Mills confirmed".
* "spacetime dimension derived".

Zulässig:

* "consistent with internal axioms". [D/E]
* "distinguishable from selected nulls". [D]
* "software invariant under tested path". [A]
* "calibrated, not derived". [C/D]
* "residual limitation remains open". [D/E]

---

## Empfohlene PR-Sequenz

1. Keep PR #1 as review-stable Draft until human review. [A]
2. Keep PR #2 as review-stable Draft pre-registration. [A]
3. Implement PR-2 spectral graph diagnostics only after working-tree hygiene. [D]
4. Review PR-2 implementation read-only. [A/D]
5. Add PR-3 causal propagation diagnostics pre-registration. [D]
6. Implement PR-3 graph-latency diagnostics. [D]
7. Expand null ensembles and observer-map stability. [D]
8. Integrate only tagged, reproducible results into reports or ledger. [A/D]
9. Prepare an experimental alpha release only after all guards and human review complete. [A/D]
10. Defer physical interpretation to a separate, explicitly speculative research track. [D/E]

---

## Nicht verhandelbare Stop-Bedingungen

Stop immediately if any of the following occurs:

* A diagnostic is described as physical proof.
* A graph spectral quantity is described as spacetime dimension.
* A shortcut edge is described as entanglement signaling.
* A null-model separation is described as empirical validation.
* A dashboard visualization is used as evidence.
* A calibrated physical value enters a pregeometry growth rule.
* An AI-generated review is treated as merge authorization.
* A PR modifies protected paths without explicit governance.
* Root runtime artifacts are created.
* Tests or guards are bypassed without documented review acknowledgement.

---

## Endzustand der Roadmap

Das Projekt ist erfolgreich geführt, wenn es weniger behauptet und mehr falsifizierbar macht:

* deterministic software harness. [A]
* reproducible graph diagnostics. [D]
* null-model comparison. [D]
* observer-map stability. [D]
* honest limitations. [D/E]
* no unauthorized evidence upgrades.
* no merge authorization by AI.
* no physical overclaiming.
