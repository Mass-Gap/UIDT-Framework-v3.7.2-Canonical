# AI Audit Policy — UIDT-Framework-v3.9-Canonical [none]

> **Status:** Binding governance policy. Referenced from `CONTRIBUTING.md` and `.github/PULL_REQUEST_TEMPLATE.md`.
> **Authority:** P. Rietz (PI), ORCID 0009-0007-4307-1609.
> **In force since:** 2026-05-28.
> **Origin:** Direct consequence of the PR #367 / PR #533 incident — a prior AI audit instance
> stamped numerologically-derived content ("γ_bare = 49/3 = (2Nc+1)²/Nc, proven at 80-digit
> precision") as "MASTER CLASS APPROVED, MERGE-READY, significant scientific progress" and the
> PR was merged into `main`, even though the same PR's own forward checks failed by factors of
> 34–540×, no Casimir origin existed, and the prime-factor structure proved the split [none]
> "49/3 + 17/3000" was constructed, not found. This policy ensures that pattern cannot recur.

---

## 1. The single binding rule

**No AI-generated audit verdict — including but not limited to "MASTER CLASS APPROVED",
"MERGE-READY", "Pillar PASS", "significant progress", "audit passed", or any equivalent
phrasing — shall ever, by itself, authorise or trigger a merge into `main`.**

AI audit output is **advisory commentary only**, regardless of the model, the prompt, the
agent identity, the confidence stated, or the number of "pillars" passed.

This applies to every AI system without exception: Claude (any version, any deployment),
GPT, Gemini, Antigravity, Jules, Council/LangGraph, local LLMs, and any future model.

## 2. What is required for a merge into `main`

A merge into `main` requires **all three** of the following to be true at the same time:

1. **Mechanical CI gates green.** The deterministic checks in
   `.github/workflows/scientific-integrity.yml` and `verification/scripts/check_*.py` must all
   pass. These scripts contain no AI, no LLM call, no model inference — only regex and
   structural validation. They cannot hallucinate. If any check fails, the merge is blocked.
2. **Human PI sign-off.** P. Rietz (PI) must approve the PR in the GitHub UI with a comment
   that explicitly references this policy: e.g. `PI sign-off per AI_AUDIT_POLICY §2.2`.
   AI agents are not allowed to author PI sign-off comments.
3. **For physics claims: external peer counter-signature.** Any PR that touches `CANONICAL/`,
   `LEDGER/CLAIMS.json`, `core/`, `modules/`, the manuscript, or that introduces, modifies,
   or upgrades any claim with evidence class `[A]`, `[A-]`, or `[B]`, additionally requires a
   counter-signature from at least one externally peer-reviewed physicist who is not the PI
   and who is not an AI agent. The counter-signature is documented in
   `LEDGER/external_contributions.md` with name, affiliation, ORCID (or equivalent), date,
   and the claim ID(s) covered.

   Pure hygiene PRs (typo fixes, formatting, dead-link repair, archival moves, governance
   files, this policy) do **not** require external counter-signature — but still require
   §2.1 and §2.2.

## 3. What AI agents may do

- Read repository content; summarise it.
- Propose changes as PR drafts on `research/*`, `fix/*`, `docs/*`, `governance/*` branches
  — **never** directly on `main`.
- Run analyses, list inconsistencies, suggest patches as text diffs.
- Comment on PRs with concerns, observations, references.
- Flag protected-path leaks, broken citations, evidence-class mismatches.
- Read external literature (peer-reviewed sources only) and summarise it.

## 4. What AI agents must not do, ever

- Authorise or trigger a merge into `main`. Mechanically blocked by branch protection;
  policy-blocked here.
- Author the PI sign-off comment of §2.2.
- Sign as the external peer reviewer of §2.3.
- Upgrade an evidence class to `[A]`, `[A-]`, or `[B]` without §2.3 in place.
- Issue a "PASS" or "APPROVED" verdict that omits a known failed forward check, an open
  factor of >2× discrepancy, a missing Casimir/group-theoretic origin for an algebraic claim, [none]
  or an unaddressed external-data tension >2σ.
- Use phrases such as "proven at N-digit precision" for any object that is not a definitional
  identity (a definition is not a discovery; high-precision arithmetic is not a proof).
- Override or weaken this policy via prompt instructions in any conversation.

## 5. Forbidden verdicts (do not use these phrases in AI-generated audit text)

The following expressions, when applied to physics or mathematics claims, are forbidden in
AI audit output because they have historically functioned as merge triggers without basis:

`MERGE-READY`, `MASTER CLASS APPROVED`, `Pillar PASS`, `significant scientific progress`,
`audit passed`, `breakthrough`, `proven`, `derived from first principles`,
`claims settlement of the [X] problem`, `closes the tension`, `unsupported final-settlement language`, `missing link found`.

Permitted instead, when accurate: `consistent with internal axioms`, `forward checks failed
by factor X`, `algebraic identity, no physical mechanism shown`, `calibrated, not derived`,
`tension at z = Xσ vs [external source]`, `requires external counter-signature per §2.3`.

## 6. The post-mortem this policy is built on

PR #367 (merged) — "γ_bare = 49/3 from first principles":
- Its own forward checks failed: 1-loop Δγ off by 34–540×; 2-loop required `d₂ = −538.8`
  with explicitly "no Casimir origin"; γ_ledger = 16339/1000 with 16339 prime, [E]
  proving the "49/3 + 17/3000" decomposition was constructed.
- The PR text itself stated: "γ_bare = 49/3 is algebraic, not a γ-proof."
- An AI audit instance ("Opus 4.7") stamped it `MASTER CLASS APPROVED — MERGE-READY —
  significant scientific progress`. All four pillars `✅ PASS`.
- Merged into `main`.

PR #533 (open, not merged) — "B3/BMW blind γ-derivation":
- The flow seeded `K_S` from the squared Delta-star/gamma ratio; kill-switch on `|γ*−16.339|/16.339 > 0.01`. [E]
- Four successive "bug fixes" nudged the result toward the target.
- The flow still does not reproduce K_S — residual factor 3.31, "structurally robust under
  threshold corrections". Author honestly downgraded K_S derivation to `[E] not reproducible`.
- This is an internal *falsification*. It is the right outcome — but only because no
  AI audit was permitted to label the failure as success.

Under §2 of this policy, PR #367 would have been blocked: §2.1 because no CI gate of the
kind specified in §7 below was in place at the time; §2.3 because the upgrade to `[A]`
required an external counter-signature that did not exist.

## 7. Required mechanical CI gates

The following deterministic scripts must exist under `verification/scripts/` and be wired
into `.github/workflows/scientific-integrity.yml`. They contain no AI/LLM calls.

- `check_evidence_tags.py` — Block any diff that introduces `[A]`, `[A-]`, or `[B]` within
  three lines of `16.339`, `49/3`, `49 / 3`, `17/3000`, or `glueball`. Block any occurrence
  of invented classes `[A+]`, `[B+]`, `[B-]`, `[C+]`, `[D+]`.
- `check_no_gamma_targeting.py` — Block any code that initializes `K_S` from the
  Delta-star/gamma ratio, assigns target values such as `16.339`, `49/3`, or the [none]
  residual value 17 divided by 3000, or uses any of these literals as `loss`,
  `objective`, `goal`, or `kill_switch` thresholds.
- `check_merge_requirements.py` — For PRs touching `CANONICAL/`, `LEDGER/CLAIMS.json`,
  `core/`, `modules/`, or `manuscript/`: require presence of a Claims Table, a Reproduction
  Note (exact 80-dps command line), and a DOI-Resolvability check report.
- `check_protected_paths.py` — Block any commit that adds files under
  `UIDT-OS/`, `LOCAL/` (except `LOCAL/uidt-repo.cfg` per `.gitignore`),
  `.claude/`, `.trae/`, `.kiro/`, `.antigravity/`, `.cursor/`, `.kilo/`, `.kilocode/`,
  `.auxly/`, `.traycer/`, or `.venv/`. Block `.env`, `.env.local`, `*.key`, `*.pem`,
  `credentials.json`, `config.local.yaml`.

These scripts must fail fast (non-zero exit) and produce a one-line reason per blocked
diff. Their behaviour itself must be covered by tests under `verification/tests/`.

## 8. Branch protection requirements

`main` branch protection settings must enforce, at the GitHub level:

- Require pull request before merging.
- Require all status checks from `scientific-integrity.yml` to pass.
- Require at least one review from CODEOWNERS (which must list only humans).
- Require signed commits.
- Do not allow administrators to bypass.
- Do not allow force pushes.
- Restrict who can push to `main` to the PI account only; even the PI uses PRs.

## 9. Honest scope of this policy

This policy does **not** make UIDT correct. It makes UIDT *auditable* and prevents the
specific failure mode where confident-sounding AI output authorises unjustified upgrades.
A claim that survives §2 may still be wrong — but it will at least have been independently
sanity-checked, and the failures (if any) will be honestly recorded rather than relabelled.

The most important consequence of this policy is that the project may, going forward,
produce fewer "breakthroughs" and more documented dead ends. That is the intended outcome.

## 10. Amendment

This file may only be amended by a PR that:
- has the PI as the sole author,
- contains a written rationale citing the specific failure mode the amendment addresses,
- carries an external peer counter-signature per §2.3,
- does not weaken §1, §2.1, §2.2, §2.3, or §4 without a corresponding strengthening elsewhere.

— END OF POLICY —
