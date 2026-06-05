# External peer counter-signatures (AI_AUDIT_POLICY §2.3)

Per AI_AUDIT_POLICY.md §2.3, any PR that introduces, modifies, or upgrades a claim with
evidence class [A], [A-], or [B] requires a counter-signature from an externally peer-reviewed
physicist who is not the PI and who is not an AI agent.

Counter-signatures are recorded here, one block per signature.

## Format

```
- date: YYYY-MM-DD
  pr: <number>
  claim_ids: [UIDT-C-XXX, ...]
  reviewer:
    name: <name>
    affiliation: <institution>
    orcid_or_equivalent: <ID>
    contact: <e-mail or stable handle>
  statement: |
    One paragraph in the reviewer's own words confirming what they reviewed and what their
    judgement is. No AI-generated text. The reviewer attests this is their own writing.
  scope_notes: |
    What the signature does and does NOT cover.
```

## Signatures

(none yet — to be filled by Wave-2+ research PRs)
