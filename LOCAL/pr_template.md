[UIDT-v3.9] feat: Implement ArXiv Literature Scan Script
### Objective
Implement the weekly ArXiv monitor (`LOCAL/scripts/arxiv_scan.py`) to parse abstracts for DESI and Lattice QCD falsification triggers. Outputs Emergency Epistemic Reports directly to stdout upon detection. Handled external API edge-cases (503/429) safely.

### Evidence Status & Claims
- Affected Constants: \Delta, w
- Evidence Category: Category A+, Category C
- Residual Check: N/A

Author: P. Rietz
Mode: OUTPUT-MODE
