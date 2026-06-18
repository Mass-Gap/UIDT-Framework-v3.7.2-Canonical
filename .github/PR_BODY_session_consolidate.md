## Claims Table

Aggregate of all delta-claims tables (B0.2, SPEC v3, B2, GAP). Contains methodological notes on alpha-linear correction, PR-B1 O-C null (metastability), PR-B2 charter decisions, and division-algebra track for G_SM gap.

## Reproduction Note

The following CI commands were run locally and are recorded for deterministic reproduction:
```bash
python -m prb0 verify-grid
python -m prb0 verify-injective
python -m prb0 verify-confusion --alpha-sweep
gitleaks detect --source . --no-banner
actionlint
```
Note: `verify-confusion` was skipped due to missing calibration tau. Symbolic-results note: The alpha-linear noise projection eats n=2 blocks at delta=0.10.

## DOI Check

The following references require a DOI/arXiv sweep:
- Division-algebra track
- Azuma et al. (JHEP 05 (2004) 005)
- NCG references

---
*Drafted by Antigravity.*
