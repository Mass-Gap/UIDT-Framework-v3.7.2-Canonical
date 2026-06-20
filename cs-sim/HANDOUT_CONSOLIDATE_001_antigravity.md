# HANDOUT — Session Consolidation into a Single Pull Request (PR-SESSION-CONSOLIDATE)

| Field | Value |
|---|---|
| Handout ID | `HANDOUT-CONSOLIDATE-001` |
| Executor | Antigravity 2.0 (mechanical steps only) |
| Target repo | `github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical` |
| Source | Session outputs (`/mnt/user-data/outputs/`) + private `cs-sim` repo |
| Auditor | Claude/Opus — advisory; **cannot sign or merge** (`AI_AUDIT_POLICY.md` Sec. 1) |
| Hard rule | Antigravity performs **mechanical** work only: branch, folders, file moves, PR open. **Every PI-signature gate HALTS for human action.** No AI signs; no AI merges to `main`. |
| Privacy rule | Mandatory gitleaks scan before every file enters the public repo. Internal paths (`UIDT-OS/`, `LOCAL/`, `.env`, `*.key`, `ghp_*`, `C:\Users`) are **forbidden** in commits. |

---

## 0. What this PR does and does NOT do

**Does (mechanical, Antigravity):** create one feature branch, build an elite-standard folder structure, place every session artifact in its correct location with consistent naming, version-supersede stale files, open **one** pull request against `main` with a complete description, run all deterministic CI gates.

**Does NOT (PI only — the PR stays in DRAFT until these are done by hand):**
- sign the PR-B0.2 gate;
- enter/sign the PR-B1 O-C ledger record;
- approve the PR-B2 charter;
- merge to `main` (requires green CI + PI sign-off + external counter-signature for any [B] physics change — none here, all artifacts are [D]/[E]/methodological/audit).

---

## 1. Branch and naming convention (elite standard)

```
git checkout main && git pull
git checkout -b session/2026-06-17-detector-preflight-and-gsm-gap
```

Naming convention (enforce repo-wide for the new files):
- Specs/protocols: `PREREG-<id>`, `SPEC-<id>`, `HANDOFF-<id>` — kebab-case IDs, English.
- Audit memos: `AUDIT-<topic>-<nnn>`.
- Manuscript patches: `PATCH-APP-<topic>-<nnn>`.
- Ledger drafts: `LEDGER-<claim>-<nnn>` (draft only; never written to `LEDGER/` by Antigravity).
- Reports: keep pipeline-generated names; do not hand-edit.

## 2. Target folder structure (create if absent)

```
verification/
  prereg/
    PR-B0/                         # detector preflight
      HANDOFF_projected_grid_detector.md          # HANDOFF-PR-B0-001 (alpha-linear corrected)
      HANDOUT_alpha_linear_noise.md               # HANDOUT-PR-B0.2-001
      GATE_REPORT.md                              # PR-B0.2, pipeline-generated, admissible row FILLED (§5)
    PR-B1/
      PREREG_blinded_matrix_condensation.md       # PREREG-PR-B1 (v1, superseded note)
      PREREG_metastability_pre.md                 # PREREG-PR-B1-PRE-001 (PI-signed PRE-O1)
      SPEC_delta_measurement.md                   # SPEC-DELTA-MEAS-001 v3 (alpha-linear, scale-as-observable)
      DRAFT_framework.md                          # DRAFT PR-B1-002 (alpha-linear corrected)
      RESEARCH_HANDOUT_YMCS_metastability.md
    PR-B2/
      CHARTER.md                                  # PR-B2-CHARTER-001 (open [D]/[E])
  audit/
    AUDIT_MEMO_scale_layers.md                    # AUDIT-SCALE-LAYERS-001
  data/
    visualizations/                               # any .npz / figures (NONE with internal data)
manuscript/
  appendix/
    PATCH_appendix_gsm_gap.md                     # PATCH-APP-GSM-GAP-001 (Track1/2, G1-G4, Cor 4.2, division-algebra [D])
  ledger-drafts/
    LEDGER_ENTRY_PR-B1-OC_draft.md                # draft only; PI transcribes into LEDGER/CLAIMS.json by hand
docs/
  methodology/                                    # optional, if PI approves the [E] methodology note
    (gap-localization-before-construction.md)     # [E], philosophy/method — only if PI requests
```

**Rationale (elite-standard):** preregistrations, specs, and gate reports live under `verification/prereg/` by phase (PR-B0/B1/B2); audit memos separate from specs; manuscript patches under `manuscript/appendix/`; ledger entries are **drafts** under `manuscript/ledger-drafts/` and never auto-written to the protected `LEDGER/`.

## 3. File mapping (source → destination, with version hygiene)

| Source (outputs) | Destination | Action |
|---|---|---|
| `HANDOFF_PR-B0_001_projected_grid_detector.md` | `verification/prereg/PR-B0/HANDOFF_projected_grid_detector.md` | move |
| `HANDOUT_PR-B0.2_001_alpha_linear_noise.md` | `verification/prereg/PR-B0/HANDOUT_alpha_linear_noise.md` | move |
| `GATE_REPORT_3_.md` (PI upload) | `verification/prereg/PR-B0/GATE_REPORT.md` | move + fill admissible row (§5) |
| `PREREG_PR-B1_blinded_matrix_condensation.md` | `verification/prereg/PR-B1/PREREG_blinded_matrix_condensation.md` | move + add "superseded by PRE-001" note |
| `PREREG_PR-B1-PRE-001_metastability_1_.md` (PI upload, signed) | `verification/prereg/PR-B1/PREREG_metastability_pre.md` | move |
| `SPEC_delta_measurement_PR-B1-002_v3.md` | `verification/prereg/PR-B1/SPEC_delta_measurement.md` | move (v3 active) |
| `SPEC_delta_measurement_PR-B1-002.md` (v2) | — | **do not transfer**; mark superseded by v3 |
| `DRAFT_PR-B1-002_framework.md` | `verification/prereg/PR-B1/DRAFT_framework.md` | move |
| `RESEARCH_HANDOUT_YMCS_metastability.md` | `verification/prereg/PR-B1/RESEARCH_HANDOUT_YMCS_metastability.md` | move |
| `PR-B2_CHARTER_001.md` | `verification/prereg/PR-B2/CHARTER.md` | move |
| `AUDIT_MEMO_scale_layers_001.md` | `verification/audit/AUDIT_MEMO_scale_layers.md` | move |
| `PATCH_DRAFT_appendix_gsm_gap_001.md` | `manuscript/appendix/PATCH_appendix_gsm_gap.md` | move |
| `LEDGER_ENTRY_PR-B1-OC-001_draft.md` | `manuscript/ledger-drafts/LEDGER_ENTRY_PR-B1-OC_draft.md` | move |
| `HANDOFF_PR-B0.1_001_correction.md` | `verification/prereg/PR-B0/HANDOFF_B0.1_correction.md` | move (historical) |

**Note on the two operator-norm upload documents** (`Auditbericht...`, `Wissenschaftliche-Datenextraktion...`): do **not** transfer to the public repo as current. If retained at all, place under `verification/audit/historical/` with a header tag `[historical / partially superseded by alpha-linear correction]` per AUDIT-SCALE-LAYERS-001 §4.

## 4. Private `cs-sim` → public repo transfer (GUARDED)

The simulation lives in a private repo. Only **code and non-sensitive results** may cross to public, and only after a leak scan.

| `cs-sim` path | public destination | condition |
|---|---|---|
| `cs-sim/prb1/sim/` (HMC matrix code) | `verification/prb1/sim/` | gitleaks clean; no tokens/paths; float64 numerics only |
| `cs-sim` `.npz` outputs (non-sensitive) | `verification/data/visualizations/` | only if no internal/personal data; else leave private |
| `verification/pregeometry` (PR-0 toy model) | `verification/pregeometry/` | gitleaks clean |
| any `UIDT-OS/`, `LOCAL/`, `.env`, configs | — | **FORBIDDEN — never transfer** |

**Mandatory before transfer:**
```
gitleaks detect --source cs-sim --no-banner
# if ANY finding -> HALT, report to PI, do not transfer that file
```
If unsure whether a result file contains sensitive data → **HALT and ask the PI.** Do not guess.

## 5. The one mechanical content edit Antigravity MAY make

Fill the empty admissible-region line in `GATE_REPORT.md` from its own §3 table (pipeline-regenerate via `report.py`, do not hand-type):
```
Admissible region per class (≥0.95@δ≤0.10):
  (2,3): ρ≥0.1351; (2,4): ρ≥0.1579; (2,2,3): ρ≥0.1795; (3,4): ρ≥0.1795;
  (2,2,2): ρ≥0.1579; (3,3,3): ρ≥0.2195; (4,4,4): ρ≥0.2727; (3,6): ρ≥0.2195
```
Leave the **PI sign-off line blank** — that is the human's.

## 6. CI gates to run on the branch (deterministic, advisory)

```
python -m prb0 verify-grid
python -m prb0 verify-injective
python -m prb0 verify-confusion --alpha-sweep      # expect 0% cross-class leak at every alpha
gitleaks detect --source . --no-banner             # MUST be clean
actionlint                                          # workflow hygiene
```
CI green is necessary, **not sufficient**, for merge. Merge still needs PI sign-off (§7).

## 7. Open the PR (DRAFT) — and HALT

```
gh pr create --draft \
  --base main \
  --head session/2026-06-17-detector-preflight-and-gsm-gap \
  --title "Detector preflight (PR-B0.2, alpha-linear) + PR-B1 O-C null + PR-B2 charter + G_SM gap appendix" \
  --body-file .github/PR_BODY_session_consolidate.md
```

PR body must contain the three mandatory headings (repo rule for anything touching `manuscript/`):
- `## Claims Table` — aggregate of all delta-claims tables (B0.2, SPEC v3, B2, GAP).
- `## Reproduction Note` — the CI commands in §6 + the symbolic-results note.
- `## DOI Check` — the division-algebra + Azuma + NCG references, flagged for sweep.

**Then STOP.** The PR stays in **DRAFT**. Antigravity posts a comment listing the PI gates below and does nothing further.

## 8. PI action checklist (human only — Antigravity HALTS here)

These are the "open commits" — every one is a signature, none can be delegated:

1. **PR-B0.2 gate:** review `GATE_REPORT.md` (admissible row now filled), fill the PI sign-off line, confirm `[x] satisfiable`. → your signature.
2. **PR-B1 O-C ledger:** transcribe the `CLAIMS.json` block from `LEDGER_ENTRY_PR-B1-OC_draft.md` into `LEDGER/CLAIMS.json`, set `pi_signoff`, mark PR-B1-002 base run CANCELLED. → your edit + commit to the protected path.
3. **PR-B2 charter:** review `CHARTER.md`, confirm premise ((2,3)-stabilizer UNSOLVED; Dirac open thread; `Symmetriebrechung.txt` [E]/over-read). → your sign-off.
4. **Appendix patch:** decide whether `PATCH_appendix_gsm_gap.md` is included in the manuscript. → your decision.
5. **Methodology note ([E]):** decide whether the gap-localization methodology doc is wanted. → your decision.
6. **Mark PR ready + merge:** only after 1–4, with CI green. `gh pr ready` then merge under your authenticated account (GPG-signed commit recommended). → your action.

## 9. Commit message convention (for Antigravity's mechanical commits)

```
docs(prereg): consolidate PR-B0.2/B1/B2 session artifacts onto branch
docs(manuscript): add G_SM gap appendix patch draft (advisory)
chore(verification): transfer cs-sim PR-B1 HMC code (gitleaks clean)
```
No commit by Antigravity may touch `LEDGER/`, `CANONICAL/`, `core/`, or `main`.

---

*Drafted by Claude/Opus, advisory capacity. Antigravity executes Sections 1–7 and 9 (mechanical) and HALTS at every signature gate in Section 8. No AI signs the gate, enters the ledger, approves the charter, or merges to main — those are the PI's, by governance. The PR is opened in DRAFT and stays there until the PI completes Section 8. Authorizes nothing.*
