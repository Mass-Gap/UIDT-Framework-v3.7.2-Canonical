# Ontology Link — Canonical Source-of-Truth Marker (v3.9.9)

> **Status:** Canonical pointer file.
> **In force since:** 2026-06-01.
> **Updated:** 2026-06-15 for ontology version 005 (appB-connes).
> **Authority:** P. Rietz (PI).

## What this file declares

Starting with v3.9.9, the authoritative ontological, epistemic, and axiomatic
source of truth for the UIDT-Framework-v3.9-Canonical repository is the
manuscript:

```
manuscript/UIDT_Ontology_v3_9_9.tex   (TeX source)
manuscript/UIDT_Ontology_v3_9_9.pdf   (compiled artefact)
```

In any case of conflict between this manuscript and any other file in the
repository (including `LEDGER/CLAIMS.json`, `CANONICAL/CONSTANTS.md`,
`CANONICAL/LIMITATIONS.md`, `STATUS.md`, `README.md`, or any research note),
the manuscript wins. All other files are derived artefacts and must be brought
into agreement with it.

## What the manuscript contains, and where to find it

| Element | Location in manuscript | Repository mirror / consumer |
|---|---|---|
| The four Axioms | `\subsection{The Four Axioms}` (\ref{subsec:four-axioms}) | quoted in `CANONICAL/CONSTANTS.md` and in `README.md` Pillar~I |
| Evidence-class grammar A / A- / B / C / D / E | `\subsection{Evidence-Class Grammar and Stratum Separation}` | enforced by `verification/scripts/check_evidence_tags.py` |
| Target-Leakage Theorem | `\begin{proposition}[Target Leakage]` (\ref{prop:target-leakage}) | enforced by `verification/scripts/check_no_gamma_targeting.py` |
| Final Allowed Claims ONT-01..ONT-10 | `\subsection{Final Allowed Claims}` (Table~\ref{tab:claims}) | must match `LEDGER/CLAIMS.json` for the corresponding claim IDs |
| Final Forbidden Claims (7) | `\subsection{Final Forbidden Claims}` | enforced by `verification/scripts/check_evidence_tags.py` + governance review |
| The 8 Falsification Gates F1..F8 | `\subsection{The Falsification Gates}` (\ref{subsec:falsification-gates}) | F8 = `AI_AUDIT_POLICY.md §1`; F1-F7 implemented in `verification/scripts/check_*.py` |
| Tension Ledger T1..T7 | `\subsection{The Tension Ledger}` (Table~\ref{tab:tensions}) | mirrored conceptually in `LEDGER/CLAIMS.json` `tension_alert` fields |
| Limitation Register L1..L12 | `\subsection{The Limitation Register (L1-L12)}` | mirrored in `CANONICAL/LIMITATIONS.md` |
| Museum of refuted constructions | referenced via the Forbidden Claim (7) | documented in `historical_heuristics.md` |
| PI Override Box for $\Delta^*$ (D18) | `\begin{box}[pi-override-delta]` referenced from claim ONT-05 | applied in `LEDGER/CLAIMS.json` UIDT-C-001 `pi_override` block |
| d2=0 Obstruction (gauge-origin no-go, construction-specific) | `\section{The d2=0 Obstruction}` (sec:d2-obstruction) | no surface file may claim S(x) derives G_SM |
| G_SM-Origin Fork (Arm 1 / Arm 2, S(x) -> A -> G_SM) | `\section{...Algebraic Fork}` (sec:algebraic-fork) | ledger fields `SCALAR_ONLY_COMPATIBLE` + `GROUP_SELECTION_MECHANISM` mandatory |
| Minimal-Algebra Catalogue (string-net, quantum-link, NCG, tensor-net) | subsec:minimal-algebra-catalogue | all [D]; none a closure; mirrored in literature matrix |
| Appendix B — NCG / Connes programme | app:connes-attractor ... app:b-claims-register | SEPARATE register APP-B-01..08; must NOT merge into core ONT-claims |
| Appendix B Claims Register (APP-B-01..08) | app:b-claims-register | core CLAIMS.json may carry APP-B-* only at [D]/[E] (except B-02/04/07 structural [A]) |
| Insertion-Points Theorem (earliest noncommutative insertion) | app:insertion-points | [A] for current corpus; any G_SM route must replace abelian single-mode local algebra |

## The five values that are now constants of the manuscript

These are no longer subject to ad-hoc revision; changing any of them requires
amending the manuscript itself, and the manuscript may only be amended under
`AI_AUDIT_POLICY.md §10`.

| Symbol | TeX command | Value | Evidence | Status |
|---|---|---|---|---|
| $\gamma$ (calibrated) | `\GammaGeom` | 16.339 | [A-] | calibrated, NEVER derived |
| $\gamma$ (Monte-Carlo) | `\GammaMC` | 16.374 ± 1.005 | [A-] | tension entry T1, displayed not merged |
| $\Delta^*$ (spectral gap) | `\DeltaGap` | 1.710 ± 0.015 GeV | [B] | PI-override D18 (was [A-]) |
| $\kappa$ | `\KappaRG` | 1/2 (exact) | [A] | exact framework input; closes 5κ²=3λ_S to <1e-14 |
| $\lambda_S$ | `\lambdaS` | 5/12 | [A] | exact, definitional |
| $v$ (VEV) | `\vVEV` | 47.7 MeV | [A] | exact, definitional |

## What this file is NOT

This file is not the ontology. It is a pointer. It contains no axioms of its
own, no claims of its own, no constants of its own. Anything that looks like
a claim here is a quotation or summary of the manuscript and is only as
authoritative as the corresponding manuscript section.

**On the Appendix-B programme (NCG/Connes).** The manuscript maintains a
SEPARATE claims register for the noncommutative-geometry research programme
(APP-B-01 through APP-B-08). These are NOT core UIDT claims. They live at
predictive/speculative status ([D]/[E]) except for the structural negative
results APP-B-02, APP-B-04, APP-B-07, which the manuscript marks [A] "re
current corpus" (proven for the present corpus, not claims about nature).
The core ledger `LEDGER/CLAIMS.json` must keep this separation: no APP-B-*
claim may appear as established physics ([A]/[B] in the physics sense) in the
core register. The automated guard is
`verification/scripts/check_ontology_consistency.py`.

## Consumers (files that depend on this pointer)

- `LEDGER/CLAIMS.json` — claim IDs and evidence classes
- `CANONICAL/CONSTANTS.md` — numerical values
- `CANONICAL/LIMITATIONS.md` — L1..L12
- `STATUS.md`, `README.md` — public-facing summary
- `verification/scripts/check_ontology_consistency.py` — automated cross-validator (Wave 0-4)
- `historical_heuristics.md` — list of refuted constructs (Forbidden Claim 7)
- `AI_AUDIT_POLICY.md` — §1 corresponds to F8 of the manuscript

## Amendment procedure

The manuscript itself is amended via `AI_AUDIT_POLICY.md §10`. This pointer
file is amended only when the manuscript's filename, location, or canonical
status changes — any other change here is a category error. The 2026-06-15
update added the d2=0 obstruction, the G_SM-origin fork, and the Appendix-B
(NCG/Connes) programme rows after the manuscript advanced to version 005.
