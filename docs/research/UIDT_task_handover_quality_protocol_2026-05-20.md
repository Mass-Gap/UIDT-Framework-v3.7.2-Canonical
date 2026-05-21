# UIDT Task Handover and Academic Quality Protocol

> **UIDT Framework:** v3.9 Canonical  
> **Date:** 2026-05-20  
> **Status:** Operational protocol for future UIDT tasks, reviews, manuscripts, derivation attempts, and PR handovers.  
> **Scope:** Process governance only. No evidence-category promotion. No `LEDGER/CLAIMS.json` mutation.

---

## 1. Purpose

This protocol defines the minimum handover and quality-control record that must be filled after every substantial UIDT task.

It is designed to prevent common AI failure modes in high-level academic work:

- hallucinated citations, sources, or theorem status;
- evidence-category inflation;
- hidden numerical approximations;
- stale repository assumptions;
- undocumented no-go results;
- ambiguous symbol reuse;
- accidental protected-path edits;
- narrative pressure overriding reproducibility;
- conflating Stratum I, II, and III;
- treating suggestive numerical hits as proof.

---

## 2. Mandatory Skill-Loading Decision

Before any UIDT task, classify the task and load the relevant skills from the local UIDT-OS skills inventory when available.

Expected local inventory root:

```text
C:\Users\badbu\Documents\github\UIDT-Framework-V3.9\UIDT-OS\SKILLS
```

If the local skills folder is not directly accessible in the active environment, use the uploaded skill descriptions already available in the session and explicitly mark any missing local access as a limitation.

### 2.1 Skill Selection Table

| Task type | Required skills |
|---|---|
| Ambiguous user request, chaotic notes, or multi-step task | `uidt-neural-architect`, `uidt-dispatcher` |
| PR creation, branch edits, file placement | `uidt-git-operations`, `uidt-filesystem-manager`, `uidt-quality-gate` |
| `CANONICAL/`, `LEDGER/`, `core/`, `modules/`, SSOT impact | `uidt-guardian-consensus`, `uidt-quality-gate`, `uidt-cove` |
| Numerical proof, residual, precision, script verification | `uidt-numerical-verifier`, `uidt-verification-engineer`, `uidt-test-runner`, `uidt-cove` |
| Manuscript, LaTeX, formatting, figure captions | `uidt-doc-formatter`, `uidt-latex-processor`, `uidt-quality-gate` |
| External scientific sources, DOI/arXiv, lattice/FRG/cosmology references | `uidt-literature-scanner`, `uidt-research-assistant`, `uidt-cove` |
| Data extraction, datasets, tables, raw visualization data | `uidt-data-curator`, `uidt-numerical-verifier`, `uidt-quality-gate` |
| Final adversarial review | `uidt-quality-gate`, `uidt-cove`, `uidt-guardian-consensus` if protected paths are involved |

---

## 3. Evidence and Stratum Rules

Every quantitative or physics-relevant statement must carry an evidence category or be explicitly declared contextual.

| Tag | Meaning |
|---|---|
| [A] | mathematical closure with proof engine / exact invariant / residual `< 1e-14` |
| [A-] | calibrated gamma-sector value, especially `gamma = 16.339` |
| [B] | external lattice or primary-source compatible result with verified source and uncertainty |
| [C] | calibrated cosmology cap; no tension claimed solved |
| [D] | UIDT prediction, conjecture, or structured internal derivation attempt |
| [E] | speculative, legacy, unsupported, or withdrawn |

Strata must remain separated:

| Stratum | Content |
|---|---|
| I | empirical values, measurements, uncertainties, lattice/cosmology numbers |
| II | standard QFT, lattice, FRG, or cosmology consensus context |
| III | UIDT interpretation, mapping, prediction, or conjecture |

---

## 4. Source Integrity Protocol

### 4.1 Allowed source hierarchy

Use the highest-evidence source available:

1. Repository SSOT files and active PR diffs for internal UIDT state.
2. Verified primary papers, DOI/arXiv records, journal metadata, or official collaboration releases.
3. High-quality secondary sources only for orientation, not claim promotion.
4. No unsourced memory, no invented citations, no inferred DOI/arXiv IDs.

### 4.2 Uncertainty handling

If a source, number, DOI/arXiv ID, PR status, or physical interpretation is unclear:

```text
Mark as [AUDIT_FAIL], [SEARCH_FAIL], [TENSION ALERT], or [REVIEW-REQUIRED].
Report the ambiguity to the PI.
Do not guess.
```

---

## 5. Numerical Protocol

All critical numerical scripts must obey:

```python
from mpmath import mp
mp.dps = 80
```

Never use for proof-critical values:

```text
float()
round()
unittest.mock
MagicMock
test doubles for physics engines
centralized hidden precision overrides
```

Use explicit residual gates:

```python
residual = abs(value - expected)
assert residual < mp.mpf("1e-14"), mp.nstr(residual, 80)
```

For decimal/rational mixed comparisons, avoid exact `mpmath.mpf` equality. Use residual checks.

---

## 6. Protected-Path Protocol

The following paths require elevated caution:

| Path | Rule |
|---|---|
| `CANONICAL/` | read-only unless explicitly authorized; changes require Guardian review |
| `LEDGER/` | SSOT-adjacent; direct `CLAIMS.json` mutation requires Guardian review |
| `core/` | no numerical behavior changes without formal review |
| `modules/` | no proof-engine or physics-logic changes without formal review |
| `UIDT-OS/` | protected operational layer |
| repository root | no stray scripts, tests, figures, or scratch files |

Scripts belong under:

```text
verification/scripts/
verification/tests/
LOCAL/scripts/
```

Raw visualization data belongs under:

```text
verification/data/visualizations/
```

Publication figures belong under:

```text
manuscript/figures/
docs/assets/
```

---

## 7. AI-Failure Detection Checklist

Every substantive output must be checked for:

| Failure mode | Required detection action |
|---|---|
| Citation hallucination | Verify DOI/arXiv/journal or mark `[SEARCH_FAIL]`. |
| Evidence inflation | Compare statement to tag rules and downgrade if needed. |
| Proof-language overreach | Replace `proved/solved/resolved` unless [A] or [A-] gate is satisfied. |
| Stale repository state | Check active branch/PR status before reporting. |
| Symbol collision | Search for reused symbols such as `k_crit`; define context explicitly. |
| Hidden fitting | Count free parameters and mark as non-first-principles if unjustified. |
| Numerical brittleness | Replace exact decimal/rational equality with residual gates. |
| Precision illusion | Ensure `from mpmath import mp`, not ineffective context assignment. |
| Strata mixing | Split empirical, consensus, and UIDT interpretation. |
| Missing no-go | Document failed paths honestly. |
| Over-polished narrative | Prefer limitations and falsification exposure over rhetorical strength. |

---

## 8. Delegation Decision Protocol

Before starting work, decide whether the current environment is sufficient.

| Situation | Preferred executor |
|---|---|
| Remote-visible GitHub PR/document cleanup | ChatGPT with GitHub connector and UIDT skills |
| Full local reflog/worktree/cache forensics | Local UIDT-OS agent or desktop full-repo environment |
| Long-running numerical solver | Local Python environment or agent-mode shell |
| Large manuscript audit | UIDT manuscript audit workflow with chunking protocol |
| External literature survey | Literature scanner / scholar tool plus primary-source verification |
| Publication figure generation | Local Python / Jules-style visualization workflow with raw data preservation |

If a different model, local agent, or desktop environment is better suited, explicitly state that and open or update a delegation issue rather than pretending the current environment can do it.

---

## 9. Mandatory Handover Template

Fill this template after every substantial task.

```markdown
# UIDT Task Handover

## Task ID / PR / Branch
- Task:
- PR / issue:
- Branch:
- Date:
- Executor environment:

## Objective
- Original objective:
- Adjusted objective, if any:
- Reason for adjustment:

## Skills Loaded
- Dispatcher / neural architect:
- Git operations:
- Guardian / SSOT:
- Numerical verifier / test runner:
- CoVe:
- Literature scanner:
- Doc / LaTeX formatter:
- Quality gate:

## Files / Artifacts Changed
| Path | Change | Protected? | Notes |
|---|---|---|---|

## Claims and Evidence
| Claim | Value | Evidence | Stratum | Status | Falsification exposure |
|---|---:|---|---|---|---|

## Numerical Checks
| Check | Command / method | Residual | Threshold | Status |
|---|---|---:|---:|---|

## Source Checks
| Source | DOI/arXiv/PR | Status | Used for | Evidence impact |
|---|---|---|---|---|

## Tensions / Risks
| ID | Risk | Severity | Required action |
|---|---|---:|---|

## AI-Failure Audit
- Citation hallucination checked:
- Evidence inflation checked:
- Symbol collision checked:
- Precision context checked:
- Strata separation checked:
- No-go documentation checked:
- Protected-path compliance checked:

## Result
- PASS / REVIEW-REQUIRED / BLOCK:
- What is solved:
- What remains open:
- What must not be claimed:

## Next Logical Step
- Next PR / issue:
- Reason:
- Delegation required:
```

---

## 10. Current Standing Reminders

- `gamma = 16.339` remains [A-].
- `gamma_bare = 49/3` remains [D] as a physical UIDT identification.
- `Delta_gamma_required = 17/3000` remains [D] until derived.
- S4-P1 remains [D].
- SU(4) N-definition remains `[TENSION ALERT]`.
- L1, L4, and L5 remain open.
- No merge, approval, ready-for-review transition, or direct `main` operation is authorized by this protocol.

---

## 11. Acceptance Status

`PROTOCOL ACTIVE / MUST BE FILLED AFTER SUBSTANTIAL TASKS`

This protocol is an operational guardrail. It does not change physics claims and does not update the claims ledger.
