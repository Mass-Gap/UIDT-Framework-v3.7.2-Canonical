[UIDT-v3.9] Docs/Chore: Enforce canonical filesystem structure (Rule 02)

Evidence category: [N/A]
Limitation impact: [none]
DOI: 10.5281/zenodo.17835200

## Description
This PR enforces the canonical filesystem structure according to the hygiene sweep protocols:
- `Supplementary_Results/` removed and its contents moved to `verification/results/`.
- Schema compliance check for `LEDGER/CLAIMS.json` updated with correct `"status": "calibrated"` property instead of the invalid `"external"` property for claims UIDT-C-054 and UIDT-C-055 to pass JSON schema validation.
- Canonical state files `CANONICAL/CONSTANTS.md` and `CANONICAL/EVIDENCE_SYSTEM.md` remain unmodified.

## Quality-Gate Checklist
- [x] Claims Table (N/A)
- [x] Reproduction Note (N/A)
- [x] DOI/arXiv resolvability check (N/A)
