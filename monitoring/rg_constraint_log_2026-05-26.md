# RG Constraint Log 2026-05-26
Operator: Jules (ALPHA-03)

## Constraint: 5κ² = 3λ_S
- κ = 1/2 (exact)
- λ_S = 5/12 (exact)
- LHS = 1.25 (exact)
- RHS = 1.25 (exact)
- Residual = 0.0
- Status: ✅ PASS

## Source Scan Results
- grep "0.417": 57 matches ❌
- grep "float(kappa": 0 matches ✅

## Files Checked
- core/*.py: 1 files with violations
- modules/*.py: 0 files with violations
- verification/scripts/*.py: 8 files with violations
- verification/tests/*.py: 2 files with violations
- docs/: Multiple files with violations
- CANONICAL/: 1 file with violations
- LEDGER/: 2 files with violations
