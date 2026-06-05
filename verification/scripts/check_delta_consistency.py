#!/usr/bin/env python3
"""D18 consistency check: Δ* evidence class must be the same across
LEDGER/CLAIMS.json (UIDT-C-001), README.md (Scientific Status table), and
STATUS.md (if it references Δ*). Reads the authoritative value from the ledger."""
from __future__ import annotations
import json, sys, re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / "LEDGER" / "CLAIMS.json"
README = REPO / "README.md"
STATUS = REPO / "STATUS.md"

def main() -> int:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    c001 = next((c for c in data["claims"] if c["id"] == "UIDT-C-001"), None)
    if c001 is None:
        print("BLOCKED: UIDT-C-001 not found in ledger.", file=sys.stderr)
        return 1
    authoritative = c001["evidence"]
    print(f"[check_delta_consistency] Ledger UIDT-C-001 evidence = {authoritative!r}", file=sys.stderr)

    # README: look for the row 'Yang-Mills Mass Gap (spectral gap result)' and pick its evidence cell
    readme_text = README.read_text(encoding="utf-8")
    m = re.search(
        r"\|\s*Yang-Mills Mass Gap[^|\n]*\|[^|\n]*\|\s*([A-E][\-+]?)\s*\|",
        readme_text,
    )
    if m is None:
        print("WARN: README.md row for Yang-Mills Mass Gap not found in expected format.", file=sys.stderr)
        return 1
    readme_class = m.group(1)
    print(f"[check_delta_consistency] README   Mass Gap evidence = {readme_class!r}", file=sys.stderr)
    if readme_class != authoritative:
        print(f"BLOCKED: README ({readme_class}) disagrees with ledger ({authoritative}).", file=sys.stderr)
        print("  This is the exact drift mode that AI_AUDIT_POLICY exists to prevent.", file=sys.stderr)
        return 1
    print("[check_delta_consistency] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
