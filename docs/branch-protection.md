# Required GitHub branch-protection settings for `main`

These settings must be applied in the GitHub UI by a repository administrator;
the repository alone cannot enforce them.

## Required

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

## Rationale

Points 2 and 8 are the AI_AUDIT_POLICY §2.1 mechanism: deterministic CI must
pass and not even an admin can bypass it. This is the manuscript's
Falsification Gate F8 in operational form.

Point 5 prevents the PR #367 failure mode: an AI agent with push permissions
to main authorising itself.

Point 9 (signed commits) ensures every change is attributable to a verifiable
key — which matters when external counter-signatures are recorded.
