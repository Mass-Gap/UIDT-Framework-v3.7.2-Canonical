#!/usr/bin/env bash
# repro_verification.sh — UIDT v3.9 Full Verification Suite
# Runs all audit scripts sequentially and produces repro_report.md
# Requirements: Python 3.10+, mpmath, numpy
# Paths: tools/, verification/data/visualizations/

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REPORT="repro_report.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PYTHON=${PYTHON:-python3}
EXIT_CODE=0

cd "$REPO_ROOT"

echo "# UIDT v3.9 Reproduction Report" > "$REPORT"
echo "Generated: $TIMESTAMP" >> "$REPORT"
echo "Python: $($PYTHON --version 2>&1)" >> "$REPORT"
echo "mpmath: $($PYTHON -c 'import mpmath; print(mpmath.__version__)')" >> "$REPORT"
echo "Framework DOI: 10.5281/zenodo.17835200" >> "$REPORT"
echo "" >> "$REPORT"

# ── SHA256 LEDGER hashes ───────────────────────────────────────────────────
echo "## LEDGER File Hashes" >> "$REPORT"
for f in LEDGER/CLAIMS.json LEDGER/claims.schema.json \
          LEDGER/OPEN_QUESTIONS_GEOMETRY.md \
          LEDGER/CLAIMS_ADDENDUM_C054_C056.md \
          LEDGER/tickets_new.json \
          LEDGER/external_contributions.md; do
  if [ -f "$f" ]; then
    HASH=$(sha256sum "$f" 2>/dev/null || shasum -a 256 "$f" | awk '{print $1}')
    echo "- \`$f\`: \`$HASH\`" >> "$REPORT"
  else
    echo "- \`$f\`: [MISSING]" >> "$REPORT"
  fi
done
echo "" >> "$REPORT"

# ── Claim Audit ────────────────────────────────────────────────────────────
echo "## Claim Audit" >> "$REPORT"
if $PYTHON tools/claim_audit.py --claims LEDGER/CLAIMS.json --out audit_report.json 2>&1 | tee -a "$REPORT"; then
  $PYTHON - <<'PY' >> "$REPORT" 2>&1
import json
r = json.load(open('audit_report.json'))
s = r['summary']
rg = r['rg_check']
print(f"RG Status: {rg['status']}, Residual: {rg['residual']}")
print(f"Claims: total={s['total']}, match={s.get('match',0)}, tension={s['tension']}, fail={s['fail']}")
PY
else
  echo "[BLOCKED] claim_audit.py failed" >> "$REPORT"
  EXIT_CODE=1
fi
echo "" >> "$REPORT"

# ── RG Sanity Scan ─────────────────────────────────────────────────────────
echo "## RG Sanity Scan" >> "$REPORT"
if $PYTHON tools/rg_sanity.py 2>&1 | tee -a "$REPORT"; then
  echo "RG scan: PASS" >> "$REPORT"
else
  echo "RG scan: [RG_CONSTRAINT_FAIL] — placeholder β-functions used; physical β required" >> "$REPORT"
  EXIT_CODE=1
fi
echo "" >> "$REPORT"

# ── UV Matching ────────────────────────────────────────────────────────────
echo "## UV Matching" >> "$REPORT"
$PYTHON tools/uv_match.py 2>&1 | tee -a "$REPORT"
echo "" >> "$REPORT"

# ── Vacuum Suppression ─────────────────────────────────────────────────────
echo "## Vacuum Suppression (L1 open)" >> "$REPORT"
$PYTHON tools/vacuum_suppression.py 2>&1 | tee -a "$REPORT"
echo "" >> "$REPORT"

echo "## Reproduction Status" >> "$REPORT"
if [ $EXIT_CODE -eq 0 ]; then
  echo "PASS — all checks completed. See audit_report.json for detailed results." >> "$REPORT"
else
  echo "PARTIAL — see above for failures. Physical β-functions and canonical f_n(g) required." >> "$REPORT"
fi

echo ""
echo "repro_report.md written."
echo "Artifacts: audit_report.json, rg_scan.csv, uv_matching.md, vacuum_suppression.csv"
exit $EXIT_CODE
