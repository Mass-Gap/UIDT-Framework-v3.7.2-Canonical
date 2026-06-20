## PR Template: [UIDT-v3.9] ALPHA-03: RG constraint check and type fix

### Task Reference
- Task ID: ALPHA-03
- Branch: research/TKT-20260605-RG-CONSTRAINT
- Ticket: TKT-20260605-RG-CONSTRAINT

### Claims Table
| Claim ID | Claim | Evidence Category | Source (DOI/arXiv) |
|----------|-------|-------------------|-------------------|
| UIDT-C-010 | RG Fixed Point: 5κ² = 3λ_S = 1.250 | [A] | 10.5281/zenodo.17835200 |

### Affected Constants
| Constant | Previous Value | New Value | Evidence Change |
|----------|---------------|-----------|----------------|
| λ_S | 5/12 [A] | unchanged | — |

### Reproduction Note
One-command verification:
`python verification/scripts/checks/chk08_numerics.py` (and test suite `pytest verification/tests/`)
Expected output: residual < 1e-14

### DOI/arXiv Verification
- [x] All cited papers have verified DOI or arXiv ID
- [x] No [AUDIT_FAIL] papers cited

### Pre-flight Checklist
- [x] No float() introduced
- [x] mp.dps = 80 local in all functions
- [x] RG constraint maintained
- [x] No deletion > 10 lines in /core or /modules
- [x] Ledger constants unchanged
- [x] λ_S = 5/12 (exact, not 0.417)

### Stratum Declaration
- Stratum I content: N/A
- Stratum II content: N/A
- Stratum III content: N/A
