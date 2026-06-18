#!/usr/bin/env python3
"""Chain-of-Verification: validate that LEDGER/CLAIMS.json and key surface files
agree with manuscript/UIDT_Ontology_v3_9_9.tex on the Δ* evidence class.

Authoritative source: the ontology manuscript. All consumers must match.
This is the operationalisation of CANONICAL/ONTOLOGY_LINK.md."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ONTOLOGY = REPO / "manuscript" / "UIDT_Ontology_v3_9_9.tex"
LEDGER = REPO / "LEDGER" / "CLAIMS.json"
README = REPO / "README.md"

def extract_delta_class_from_ontology() -> str:
    """Parse the manuscript for the canonical Δ* evidence class.
    Source: \\newcommand{\\DeltaGap}{1.710 ± 0.015\\GeV} % [B] PI-override"""
    text = ONTOLOGY.read_text(encoding="utf-8")
    # Look for: \newcommand{\DeltaGap}{...} % [B] PI-override
    m = re.search(r"\\newcommand\{\\DeltaGap\}\{[^}]+\}\s*%\s*\[([A-E][\-+]?)\]", text)
    if m:
        return m.group(1)
    # Fallback: claim ONT-05 in tab:claims should have the class
    m = re.search(r"ONT-05[^\n]*\\catmark\{([A-E][\-+]?)\}", text)
    if m:
        return m.group(1)
    return ""

def main() -> int:
    if not ONTOLOGY.exists():
        print(f"[check_ontology_consistency] WARN: {ONTOLOGY} not found; skipping.", file=sys.stderr)
        return 0  # don't block if the manuscript isn't there yet
    ontology_class = extract_delta_class_from_ontology()
    if not ontology_class:
        print(f"[check_ontology_consistency] WARN: could not parse Δ* class from manuscript.", file=sys.stderr)
        return 0
    print(f"[check_ontology_consistency] Ontology says Δ* = [{ontology_class}]", file=sys.stderr)

    failures: list[str] = []

    # Check LEDGER UIDT-C-001
    if LEDGER.exists():
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        c001 = next((c for c in data["claims"] if c["id"] == "UIDT-C-001"), None)
        if c001:
            if c001.get("evidence") != ontology_class:
                failures.append(
                    f"LEDGER UIDT-C-001 evidence = {c001.get('evidence')!r}, "
                    f"ontology says {ontology_class!r}"
                )
            else:
                print(f"[check_ontology_consistency] LEDGER C-001 matches: [{c001['evidence']}]", file=sys.stderr)

    # Check README Scientific Status table row
    if README.exists():
        rt = README.read_text(encoding="utf-8")
        m = re.search(
            r"\|\s*Yang-Mills Mass Gap[^|\n]*\|[^|\n]*\|\s*([A-E][\-+]?)\s*\|",
            rt,
        )
        if m:
            readme_class = m.group(1)
            if readme_class != ontology_class:
                failures.append(
                    f"README Yang-Mills Mass Gap row class = {readme_class!r}, "
                    f"ontology says {ontology_class!r}"
                )
            else:
                print(f"[check_ontology_consistency] README matches: [{readme_class}]", file=sys.stderr)

    if failures:
        print("BLOCKED: ontology consistency violation", file=sys.stderr)
        for f in failures:
            print(f"  {f}", file=sys.stderr)
        print("\nThe manuscript is the canonical source (CANONICAL/ONTOLOGY_LINK.md).", file=sys.stderr)
        print("Adjust the surface files to match the manuscript, not the other way around.", file=sys.stderr)
        return 1
    print("[check_ontology_consistency] OK", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(main())
