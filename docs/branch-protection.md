# Required GitHub branch-protection settings for `main`

These settings cannot be enforced by repository content alone — they must be applied in
the GitHub UI by a repository administrator. This document is the authoritative checklist.
Auditing the actual settings against this file is part of every release-prep PR.

## Required (all of these, simultaneously)

1. Require a pull request before merging.
2. Require status checks to pass before merging:
   - `scientific-integrity / ai-audit-policy-checks`
   - `Epistemological Audit / epistemic-gatekeeper`
3. Require branches to be up to date before merging.
4. Require at least one review from CODEOWNERS.
5. Restrict who can push to matching branches: PI account only.
6. Do not allow force pushes.
7. Do not allow deletions.
8. Do not allow administrators to bypass these settings.
9. Require signed commits.

## Why these specific settings

Points 2 and 8 are the AI_AUDIT_POLICY §2.1 mechanism: deterministic CI must pass and not
even an admin can bypass it.

Point 5 prevents the PR #367 failure mode: an AI agent with push permissions to main
authorising itself.

Point 9 (signed commits) ensures we can attribute every change to a verifiable key — which
matters when external counter-signatures are recorded against PRs.

## Auditing

To verify settings without admin access, look at the PR merge UI: if you see "Merge without
review" or "Bypass required status checks", points 4 or 2/8 are misconfigured. Report to PI.
