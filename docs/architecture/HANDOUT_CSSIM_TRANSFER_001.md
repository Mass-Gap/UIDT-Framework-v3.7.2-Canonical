# HANDOUT — Transfer `cs-sim` from Private Repo into the 3.9 Canonical Repo (PR-CS-SIM-TRANSFER)

| Field | Value |
|---|---|
| Handout ID | `HANDOUT-CSSIM-TRANSFER-001` |
| Executor | Antigravity 2.0 (mechanical steps only) |
| Source | Private `cs-sim` repository (PR-B1 matrix HMC) + root `verification/pregeometry` (PR-0 toy model) |
| Target | `github.com/Mass-Gap/UIDT-Framework-v3.9-Canonical` |
| Auditor | Claude/Opus — advisory; **cannot sign or merge** (`AI_AUDIT_POLICY.md` Sec. 1) |
| Non-negotiable core | **Private → public transfer is the highest-risk step in the whole project. A gitleaks scan that returns clean is a precondition for EVERY file. On ANY finding: HALT, report to PI, transfer nothing.** |
| PI gates | The PR is opened/updated in **DRAFT**. Marking ready, signing, and merging are PI-only. |

---

## 0. What this handout does and does NOT do

**Does (mechanical, Antigravity):** confirm real paths, run the leak guard, copy only clean and non-sensitive code/results into the correct public locations with elite folder structure, wire them into the existing session branch, update the open PR description, run deterministic CI.

**Does NOT (PI only):** mark the PR ready, sign any gate, merge to `main`, or decide whether a borderline result file is safe to publish. Borderline → HALT and ask.

## 1. The two simulation paradigms (scope; from the verified architecture comparison)

Two distinct simulations exist and must land in distinct, correctly-named locations:

| | Root simulation | `cs-sim` simulation |
|---|---|---|
| Phase | PR-0 (pregeometry toy model) | PR-B1 (metastability / matrix model) |
| Model | discrete graph / DAG growth | continuous matrix QM, SU(2) |
| Observables | $N$, $E$, components, $\beta_1$ | Casimir/$X_3$ spectra, action density, Myers value, ESS |
| Numerics | combinatorial orchestrator, leakage audits | numpy / float64, parameter-grid "Cells", `.npz` output |
| Physical-scope discipline | "[D/E]; no universe simulation claimed" | spectral/thermalization dynamics of the math framework only |

Both carry the same governance: physical interpretation capped at [D]/[E]; no overclaim of "universe simulation."

## 2. STEP 1 — Confirm real paths before touching anything

Do not assume the paths below; verify them in both repos first.

```bash
# in the private cs-sim checkout:
git -C cs-sim ls-files | grep -E 'prb1|sim|\.py$|\.npz$' | head -50
# in the public repo:
git -C UIDT-Framework-v3.9-Canonical ls-files | grep -E 'verification|pregeometry' | head -50
```
If the actual layout differs from §4, use the real paths and report the mapping to the PI. Do not invent paths.

## 3. STEP 2 — The leak guard (MANDATORY; precondition for every file)

This runs **before** any copy, on the source tree, and again on the staged result.

```bash
# 2a. Scan the entire private source
gitleaks detect --source cs-sim --no-banner --redact
echo "exit=$?"   # MUST be 0 (no leaks). Non-zero -> HALT, report, transfer nothing.

# 2b. Explicit forbidden-content scan (belt and suspenders)
grep -RInE 'ghp_[A-Za-z0-9]{36}|gho_|github_pat_|BEGIN [A-Z ]*PRIVATE KEY|C:\\\\Users|/home/[a-z]+/|\.env|GITHUB_PAT|password|secret|token *=' cs-sim \
  && echo "FORBIDDEN MARKERS FOUND -> HALT" || echo "no forbidden markers"

# 2c. Confirm no internal project files are in the transfer set
git -C cs-sim ls-files | grep -E 'UIDT-OS/|LOCAL/|\.env|\.claude|\.trae|\.mcp\.json|AGENTS\.md|\.key$|\.pem$|credentials' \
  && echo "INTERNAL FILES PRESENT -> HALT, exclude them" || echo "no internal files"
```

**Rule:** any non-empty result in 2a/2b/2c → **HALT**, write a short report naming the offending path(s) (redacted), transfer nothing until the PI clears it. Never transfer "most of it" past a finding.

## 4. STEP 3 — Transfer map (only clean files; correct elite locations)

| Source (`cs-sim` / root) | Public destination | Condition (all must hold) |
|---|---|---|
| `cs-sim/prb1/sim/**.py` (HMC matrix code) | `verification/prb1/sim/` | gitleaks clean; no tokens/paths; float64 only; no internal imports |
| `cs-sim/prb1/**` config/grid ("Cells") definitions | `verification/prb1/config/` | clean; parameters only, no credentials |
| `cs-sim` `.npz` result arrays | `verification/data/visualizations/` | **only if** demonstrably non-sensitive (no personal/internal data); **borderline → HALT + ask PI** |
| root `verification/pregeometry/**` (PR-0 toy model) | `verification/pregeometry/` | gitleaks clean; leakage-audit asserts intact |
| any `UIDT-OS/`, `LOCAL/`, `.env`, `*.key`, configs with paths | — | **FORBIDDEN — never transfer** |

**Folder hygiene (elite standard):** code under `verification/prb1/sim/`, configs under `verification/prb1/config/`, raw arrays under `verification/data/visualizations/`, never anything at repo root. Add a `verification/prb1/README.md` stating phase (PR-B1), model (SU(2) matrix QM), observables, and the [D]/[E] physical-scope disclaimer verbatim from §1.

## 5. STEP 4 — Numerical-integrity preservation (do not "improve" the code)

The transfer is a **move, not a refactor**. Binding red lines (from the threat matrix):
- Do **not** change float64 → other precision, or "optimize" the numerics.
- Do **not** DRY-refactor physical constants or remove "unused" imports.
- Do **not** alter solver logic, initial conditions, step-size tuning, or observable definitions.
- Preserve the leakage audits (`assert_no_leakage`) in the pregeometry code exactly.
- A scale/observable must never be hard-wired; the PR-B1 physical floor stays a measured observable per the δ-spec v3 (do not bake in a δ threshold).

If the code does not run as-is in the public repo's environment, report the failure to the PI; do not silently modify it.

## 6. STEP 5 — Wire into the branch and update the open PR (DRAFT)

```bash
git checkout session/2026-06-17-detector-preflight-and-gsm-gap   # the existing session branch
git add verification/prb1/ verification/pregeometry/ verification/data/visualizations/
git commit -m "chore(verification): transfer cs-sim PR-B1 HMC code + PR-0 pregeometry (gitleaks clean)"
git push origin session/2026-06-17-detector-preflight-and-gsm-gap
```

Update the existing DRAFT PR body (do not open a second PR) to add a section:
```
## Simulation Transfer (cs-sim → public)
- PR-B1 matrix HMC code: verification/prb1/sim/  [D/E scope]
- PR-0 pregeometry toy model: verification/pregeometry/  [D/E scope]
- gitleaks: clean (scan logged)
- Numerics: float64 preserved, no refactor, observables unchanged
- No internal paths/tokens transferred; .npz arrays included only if non-sensitive
```
Keep the three mandatory headings already required on this PR (`## Claims Table`, `## Reproduction Note`, `## DOI Check`) intact.

## 7. STEP 6 — Deterministic CI (necessary, not sufficient)

```bash
gitleaks detect --source . --no-banner --redact      # MUST be clean on the whole staged repo
python -m verification.prb1.sim --selftest 2>/dev/null || echo "report run status to PI, do not modify"
actionlint                                            # workflow hygiene
```
CI green does not authorize merge. Merge needs PI sign-off (§8).

## 8. STEP 7 — HALT for the PI

Antigravity stops here and posts a comment listing the PI-only actions:
1. Review the leak-scan log and the transferred file set.
2. Decide on any borderline `.npz` result files (publish vs. keep private).
3. Confirm the [D]/[E] physical-scope disclaimer is present and accurate.
4. Mark the PR ready (`gh pr ready`) and merge under your authenticated (GPG) account — only after CI is green and the session's other signature gates are complete.

## 9. What NOT to do (recap)

- Do **not** transfer anything before a clean gitleaks scan.
- Do **not** transfer `UIDT-OS/`, `LOCAL/`, `.env`, keys, or any path-bearing config.
- Do **not** refactor, re-precision, or "optimize" the simulation code.
- Do **not** open a second PR; update the existing DRAFT.
- Do **not** mark ready, sign, or merge — PI only.
- Do **not** publish a borderline result file on your own judgement — HALT and ask.
- Do **not** fabricate a scan result or a CI status; report actual output only.

---

*Drafted by Claude/Opus, advisory capacity. Antigravity executes Sections 2–7 (mechanical) and HALTS at Section 8. The gitleaks guard is a precondition for every file; any finding halts the transfer. The simulation is moved, not refactored; numerical integrity is preserved exactly. No AI marks the PR ready, signs, or merges — those are the PI's, by governance. Authorizes nothing.*
