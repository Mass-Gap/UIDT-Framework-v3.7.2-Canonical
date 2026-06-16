# MERGE PROTOCOL — Wave 0 Branches -> main (rev. 2026-06-15, ontology 005)

> **Created:** 2026-06-01  **Revised:** 2026-06-15 for ontology version 005 (appB-connes)
> **Owner:** P. Rietz (PI)
> **Authority:** `AI_AUDIT_POLICY.md` §2, the manuscript's Falsification Gate F8.
> **Scope:** Merge sequence for the three merge-ready Wave-0 branches, plus the
> ontology-canonicalisation prerequisite and the scope-limit for Wave-0-4.

This document is the authoritative recipe for moving the three Wave-0 branches
into `main`. Execute the steps verbatim. Do NOT skip §0 (pre-flight) — it is
how you verify that what you are about to merge is what was promised.

---

## 0. Pre-flight (PI does this before merging anything)

Six checks. All must pass.

### 0.1 Branches exist on remote
```bash
git fetch origin --prune
git branch -r | grep -E "(chore-wave0-honesty-pass|refactor-ledger-hygiene-v0|codex/epistemic-gatekeeper-ci)$"
```
Expected: all three branch names listed. If a branch is missing, STOP — you
cannot merge what does not exist.

### 0.2 No accidental physics changes on any of the three branches
```bash
for B in chore-wave0-honesty-pass refactor-ledger-hygiene-v0 codex/epistemic-gatekeeper-ci; do
  echo "=== $B ==="
  git diff --name-only origin/main...origin/$B \
    | grep -E "^(core/|modules/|simulation/)" \
    && echo "VIOLATION ON $B" || echo "ok: no physics-path changes"
done
```
Expected: three "ok" lines.

### 0.3 Ledger semantics on `refactor-ledger-hygiene-v0`
```bash
python -c "
import subprocess, json
content = subprocess.check_output(['git','show','origin/refactor-ledger-hygiene-v0:LEDGER/CLAIMS.json'], text=True, encoding='utf-8')
data = json.loads(content)
c001 = next(c for c in data['claims'] if c['id'] == 'UIDT-C-001')
print('UIDT-C-001 evidence:', c001.get('evidence'))
print('UIDT-C-001 has pi_override:', 'pi_override' in c001)
if 'pi_override' in c001:
    print('  pi_decision_ref:', c001['pi_override'].get('pi_decision_ref'))
print('metadata.total_claims:', data['metadata'].get('total_claims'))
print('actual claim count:', len(data['claims']))
"
```
Expected:
```
UIDT-C-001 evidence: B
UIDT-C-001 has pi_override: True
  pi_decision_ref: D18
metadata.total_claims: 59
actual claim count: 59
```

### 0.4 No protected-path leaks introduced by any branch
```bash
for B in chore-wave0-honesty-pass refactor-ledger-hygiene-v0 codex/epistemic-gatekeeper-ci; do
  echo "=== $B ==="
  git diff --name-status origin/main...origin/$B \
    | grep -E "^A.*\.(env|key|pem)$|^A.*UIDT-OS/|^A.*\.claude/|^A.*\.antigravity/" \
    && echo "SECRET-LEAK ON $B" || echo "ok: no secret-leak"
done
```
Expected: three "ok" lines.

### 0.5 The ontology manuscript (version 005) is canonicalised in main  [PREREQUISITE]
The §2.3 sign-off for PR #3 references the manuscript as the canonical PI
artefact. Therefore the manuscript MUST be committed to main under its stable
canonical name BEFORE PR #3 is merged.

```bash
git show origin/main:manuscript/UIDT_Ontology_v3_9_9.tex | head -3
```
Expected: TeX preamble lines. If "fatal: path not in tree", do the
canonicalisation step §0.5a first.

#### 0.5a Canonicalise the 005 manuscript (one-time, PI does this)
The working file is named with a DEWRAPPED/appB-connes suffix. The canonical
repository name is stable and suffix-free. On a short branch off main:
```bash
git checkout main && git pull --ff-only
git checkout -b chore/canonicalise-ontology-005
# copy the 005 source to the stable canonical name
cp "<path>/UIDT_Ontology_v3_9_9_..._DEWRAPPED-005-appB-connes_1_.tex" \
   manuscript/UIDT_Ontology_v3_9_9.tex
# (compile and copy the PDF too if you build locally)
git add manuscript/UIDT_Ontology_v3_9_9.tex manuscript/UIDT_Ontology_v3_9_9.pdf
git commit -F - <<'MSG'
[UIDT] docs: canonicalise ontology v3.9.9 (version 005, appB-connes)

Promotes the 005 manuscript (d2=0 obstruction, G_SM-origin fork,
Appendix-B / NCG-Connes programme, Insertion-Points theorem) to the
stable canonical filename manuscript/UIDT_Ontology_v3_9_9.tex.

No physics changed beyond what the manuscript itself records. The
manuscript is the canonical source per CANONICAL/ONTOLOGY_LINK.md.
MSG
git push origin chore/canonicalise-ontology-005
```
Open and merge this PR FIRST (before PR #1-#3). It is a docs-only change;
§2.3 not required (the manuscript records claims at their own classes; the
LEDGER is not touched here).

### 0.6 CANONICAL/ONTOLOGY_LINK.md and check_ontology_consistency.py reflect 005
The patched `CANONICAL/ONTOLOGY_LINK.md` (with the d2=0 / fork / Appendix-B
rows) and the patched `verification/scripts/check_ontology_consistency.py`
(with the APP-B leak guard) are produced separately. ONTOLOGY_LINK.md may
ride along with §0.5a or PR #2; the checker rides with PR #1 (Wave-0-4) or
the gatekeeper PR. Confirm both contain the 005 additions:
```bash
grep -c "APP-B" CANONICAL/ONTOLOGY_LINK.md          # expect >= 4
grep -c "APP-B" verification/scripts/check_ontology_consistency.py  # expect >= 2
```

If all pre-flight checks pass, proceed.

---

## 1. Merge order (this is the order, do not deviate)

```
0.5a  chore/canonicalise-ontology-005   -> main   (manuscript becomes canonical; prerequisite)
1.    codex/epistemic-gatekeeper-ci      -> main   (CI gates first, so they are armed)
2.    chore-wave0-honesty-pass           -> main   (surface entgift; gates inspect it)
3.    refactor-ledger-hygiene-v0         -> main   (ledger + D18; needs §2.3 via manuscript)
```

Rationale: the manuscript must be canonical before the ledger PR cites it for
§2.3. The CI gates must be live before they can inspect the surface/ledger PRs.
The ledger PR is the only one needing §2.3, so it is last.

Each is its own PR. Do not bundle them.

---

## 2. PR #1 — `codex/epistemic-gatekeeper-ci` -> `main`

### Why first
Arms the deterministic gates so the next PRs are actually inspected. This is
the LIMITED version (RULE-01 + RULE-02). Wave-0-4 extends it after these merges.

### §2.3 applicability
Not required. Tooling only; introduces, modifies, upgrades no claim.

### Procedure
```bash
git checkout main && git pull --ff-only
git checkout -b prep/merge-pr1-gatekeeper-ci
git merge --no-ff --no-commit origin/codex/epistemic-gatekeeper-ci
git diff --cached --stat   # expect 2 files: epistemic_ci.yml + epistemic_gatekeeper.py
git merge --abort
```
If clean, open the PR (GitHub UI), squash-merge. Ensure
`Epistemological Audit / epistemic-gatekeeper` is a required status check.
After merge: push a tiny test PR (typo) and confirm the workflow runs+passes.

### PR #1 body
```markdown
## Summary
First deterministic CI gates against PR #367-style numerology promotion.
Limited scope; Wave-0-4 extends with the remaining checks, versioned hooks,
ontology-consistency cross-validator, branch-protection docs.

## What this PR adds
- .github/workflows/epistemic_ci.yml — runs the gatekeeper on PRs
- scripts/epistemic_gatekeeper.py (268 lines, no LLM):
  - RULE-01: blocks 49/3 association with evidence class [A] or [B]
  - RULE-02: blocks 17/3000 as target/loss/objective
  - prestige-phrase detection

## Claims Table
(none — no claim introduced)

## Reproduction Note
`python scripts/epistemic_gatekeeper.py .`  -> 0 on clean tree, 1 on a forbidden pattern.

## DOI Check
(none required)

## §2.3
Not applicable.
```

---

## 3. PR #2 — `chore-wave0-honesty-pass` -> `main`

### Why second
Surface layer (README/STATUS/CITATION/CONTRIBUTING) brought into agreement
with the LEDGER. Removes prestige language; does not touch the ledger. The
PR #1 gate now inspects this diff.

### §2.3 applicability
Not required (removes overclaim language; upgrades nothing).

### Expected CI interaction
The gate should PASS: every "49/3 + [A]" this PR removes is a removal, not an
addition, so RULE-01 does not fire. If the gate fails, the gate is doing its
job — investigate before bypassing.

### Procedure
```bash
git checkout main && git pull --ff-only
git checkout -b prep/merge-pr2-honesty-pass
git merge --no-ff --no-commit origin/chore-wave0-honesty-pass
git diff --cached --stat   # expect ~16 files; +386/-629 lines
git merge --abort
```
Open PR (GitHub UI), squash-merge, workflow must be green.

### PR #2 body
```markdown
## Summary
Wave-0-1 honesty pass + Wave-0-1b cleanup. Surface text aligned with
LEDGER/CLAIMS.json. No claim introduced or upgraded; only prestige language
removed for claims already recorded [E] or open.

## What this PR changes
- STATUS.md "Recent Breakthroughs" — 49/3 [A] and Kill-switch [A] removed; banner added
- README.md — Glueball [B]->WITHDRAWN [E]; m_S [B]->[D]; "derives"/"Constructive proof"/
  "Internal proof complete" rewritten as internal-consistency language; "Missing Link" ->
  "Torsion Component"; cosmology framing aligned with L1
- CITATION.cff — "missing link" -> "torsion component"
- CONTRIBUTING.md — references AI_AUDIT_POLICY.md
- NEW: AI_AUDIT_POLICY.md, historical_heuristics.md
- NEW: clay-submission/WITHDRAWN_NOTICE.md (directory NOT deleted)
- NEW: docs/OPEN_QUESTION_OPERATOR_CHOICE.md
- NEW: verification/scripts/check_*.py (four stubs; Wave-0-4 implements them)
- NEW: .github/workflows/scientific-integrity.yml
- Untracked from index: 3 LOCAL/ files (preserved on disk via .gitignore)

## Claims Table
(none — no claim introduced or upgraded)

## Reproduction Note
```
grep -rn '49/3.*\[A\]' README.md STATUS.md   # empty
grep -rn 'Glueball.*\[B\]' README.md         # empty
test -f AI_AUDIT_POLICY.md && test -f historical_heuristics.md
```

## DOI Check
(no new external citations)

## §2.3
Not applicable.
```

---

## 4. PR #3 — `refactor-ledger-hygiene-v0` -> `main`

### Why third
Only PR touching a claim's evidence class (Delta*: [A] -> [B], PI Decision D18).
Only PR needing §2.3 — now resolvable via the canonicalised 005 manuscript.

### §2.3 applicability
Required. Downgrades UIDT-C-001 from [A] to [B]. The policy is symmetric: any
[A]/[A-]/[B] change triggers §2.3, even a downgrade.

### The §2.3 sign-off path for D18 (via ontology 005)
The 005 manuscript records the PI override at claim ONT-05
(Table~\ref{tab:claims}) and in the pi-override-delta box
(\ref{subsec:delta-glueball-l12}). The manuscript is PI-authored and
PI-released, and was canonicalised into main in §0.5a. Therefore the §2.3
sign-off for PR #3 is satisfied by reference to the canonical manuscript,
recorded in `LEDGER/external_contributions.md` entry D18-MANUSCRIPT-2026-06.
This is a ONE-TIME path; future evidence-class changes need an external human
peer reviewer.

### Procedure
Before opening the PR, append the D18 record to `external_contributions.md`
on the branch (block in §5), commit:
```
[UIDT] docs: record D18 §2.3 sign-off via ontology reference
```
Then open the PR (GitHub UI), squash-merge; both workflows green.

### PR #3 body
```markdown
## Summary
Wave-0-2 ledger hygiene. Two changes:
1. Mechanical cleanup of LEDGER/CLAIMS.json (metadata 60->59, statistics
   regenerated, 7 duplicate-statement claims marked superseded_by, 2 phantom
   claims flagged).
2. PI Decision D18: Delta* evidence class [A] -> [B] (UIDT-C-001 + UIDT-C-030),
   with full pi_override block on C-001.

## §2.3 sign-off
Per the canonical ontology manuscript v3.9.9 version 005
(manuscript/UIDT_Ontology_v3_9_9.tex, claim ONT-05; pi-override-delta box)
the D18 decision is canonical. See LEDGER/external_contributions.md entry
D18-MANUSCRIPT-2026-06.

## Claims Table

| ID | Statement | Before | After | Stratum |
|---|---|---|---|---|
| UIDT-C-001 | Mass Gap Delta = 1.710 ± 0.015 GeV | [A] verified | [B] verified (pi_override) | I/III |
| UIDT-C-030 | Delta* = 1.710 ± 0.015 GeV (dup of C-001) | [A] verified | [B] verified | I/III |
| metadata.total_claims | — | 60 (wrong) | 59 (actual) | — |
| metadata.version | — | 3.9.8 | 3.9.9 | — |
| statistics block | — | stale | regenerated | — |
| 7 duplicate-statement claims | C-028..042 | active | superseded_by annotated | — |
| 2 phantom claims | C-050, C-051 | open | phantom_retained_for_xref | — |

## Reproduction Note
```
python -c "
import json
data = json.loads(open('LEDGER/CLAIMS.json',encoding='utf-8').read())
c001 = next(c for c in data['claims'] if c['id']=='UIDT-C-001')
assert c001['evidence']=='B'
assert c001['pi_override']['pi_decision_ref']=='D18'
assert data['metadata']['total_claims']==len(data['claims'])==59
print('OK')
"
```

## DOI Check
References the ontology manuscript via Zenodo DOI 10.5281/zenodo.20319634
(Ontology). Delta* external lattice reference (Chen et al. 2006) already in
main; no new external citation.

## §2.3
Required. Satisfied by ontology-005 reference; see external_contributions.md
D18-MANUSCRIPT-2026-06.
```

---

## 5. The `external_contributions.md` entry for D18

```markdown
---

### D18-MANUSCRIPT-2026-06 — Delta* evidence class [A] -> [B] (PI Decision D18)

- **Date:** 2026-06-15
- **PR:** (link filled when PR #3 is opened)
- **Claim IDs affected:** UIDT-C-001, UIDT-C-030

#### Sign-off path
This is a §2.3 manuscript-reference sign-off, not an external peer review.

The PI Override is recorded as a canonical artefact in the ontology manuscript
v3.9.9 (version 005, appB-connes):

> "Delta = 1.710 ± 0.015 GeV: internally consistent, lattice-compatible;
> PI-overridden to B (box:pi-override-delta); not externally peer-confirmed,
> not derived."
> — manuscript/UIDT_Ontology_v3_9_9.tex, Claim ONT-05 in Table tab:claims,
>   and the pi-override-delta box in subsec:delta-glueball-l12

The manuscript is PI-authored, PI-released, and was canonicalised into main
(§0.5a). The record below ratifies the LEDGER change as derived from it.

#### Reviewer (manuscript reference)
- **Name:** Philipp Rietz (PI, manuscript author)
- **Affiliation:** UIDT-Framework-v3.9-Canonical
- **ORCID:** 0009-0007-4307-1609
- **Contact:** via repository CODEOWNERS
- **Statement (PI):** This entry records that the manuscript explicitly
  establishes Delta* as evidence class [B] under the pi-override-delta box.
  The LEDGER change [A] -> [B] in PR #3 is the mechanical reflection of that
  established manuscript position into the claim register. The substantive
  epistemic decision was made and documented in the manuscript, not in the
  LEDGER edit; the LEDGER edit only records it.
- **Scope notes:** Covers ONLY the [A] -> [B] downgrade of UIDT-C-001 and
  UIDT-C-030. Does NOT cover any other evidence-class change, any other claim,
  or any future change to Delta*. Any subsequent movement of Delta* must carry
  its own §2.3 record with an external peer reviewer.

#### One-time-path declaration
The "manuscript itself as §2.3 record" path is exercised here exactly once,
for D18, because: (1) the manuscript was the origin of the decision, not its
consequence; (2) the manuscript is PI-authored and explicitly states the
override; (3) the decision is a downgrade (smaller risk than an upgrade).
The PI commits, by this entry, that future evidence-class changes — including
any future change to Delta* — require an external human peer reviewer,
regardless of whether the manuscript records them.
```

---

## 6. After all PRs merged — verification on main

```bash
git checkout main && git pull --ff-only

# Manuscript canonical
git show origin/main:manuscript/UIDT_Ontology_v3_9_9.tex | head -3

# Surface
grep -rn '49/3.*\[A\]' README.md STATUS.md     # empty
grep -rn 'Glueball.*\[B\]' README.md           # empty
grep -rn 'MASTER CLASS APPROVED' .             # empty
test -f AI_AUDIT_POLICY.md
test -f historical_heuristics.md
test -f CANONICAL/ONTOLOGY_LINK.md

# Ledger
python -c "
import json
d = json.loads(open('LEDGER/CLAIMS.json',encoding='utf-8').read())
c001 = next(c for c in d['claims'] if c['id']=='UIDT-C-001')
assert c001['evidence']=='B' and c001['pi_override']['pi_decision_ref']=='D18'
print('ledger consistent')
"

# Ontology consistency cross-check (after Wave-0-4 lands the checker)
python verification/scripts/check_ontology_consistency.py   # expect: OK, exit 0

# CI
gh run list --workflow=epistemic_ci.yml --limit=5
```

If all succeed, Wave 0 is in main. Proceed to Wave-0-4 (ontology-as-CoVe).

---

## 7. What is NOT done by these PRs (honest gap list)

- The four `verification/scripts/check_*.py` are still STUBS (from PR #2).
  Real logic is added by Wave-0-4.
- The pre-commit hook is still in `.git/hooks/` only (not versioned).
  Wave-0-4 versionises it.
- `check_ontology_consistency.py` (the CoVe cross-validator, incl. the 005
  Appendix-B leak guard) lands in Wave-0-4. This is the most important
  remaining deliverable.
- `docs/branch-protection.md` not yet present.
- `LEDGER/external_contributions.md` exists only with the D18 entry until
  Wave-0-4 turns it into a permanent registry.

Wave-0-4 plan: `.antigravity/Plan_v-wave0-4___Ontology_as_CoVe.md`.
Wave-0-4 execution handout (GPT-5.5 API edition): `HANDOUT_v-wave0-4_GPT55-API.md`.

— END OF MERGE_PROTOCOL —
