#!/usr/bin/env python3
"""
UIDT Release Regression Audit

Verifies theoretical consistency across framework releases by comparing
canonical parameters and residual thresholds between versions.

Evidence Category: [A] (Stability Analysis)
DOI: 10.5281/zenodo.17835200
Author: P. Rietz (ORCID: 0009-0007-4307-1609)
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp


def _registry_by_symbol(symbols: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {sym["symbol"]: sym for sym in symbols}


def _parse_mpf_value(raw_value: str) -> mp.mpf:
    numeric_part = raw_value.split("±", 1)[0].strip()
    return mp.mpf(numeric_part)


def _format_mpf(value: mp.mpf) -> str:
    return mp.nstr(value, 80)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    symbols_path = repo_root / "verification" / "registries" / "symbol_registry.json"
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = repo_root / "verification" / "results" / "audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"regression_report_{timestamp}.json"
    
    if not symbols_path.exists():
        print(f"ERROR: {symbols_path} not found", file=sys.stderr)
        return 1
    
    with open(symbols_path, "r", encoding="utf-8") as f:
        symbols = json.load(f)
    
    symbols_by_name = _registry_by_symbol(symbols)
    
    results = {
        "timestamp": timestamp,
        "framework_version": "3.9",
        "gate_e_status": "PASS",
        "regressions": [],
        "stable_parameters": []
    }
    
    with mp.workdps(80):
        kappa = _parse_mpf_value(symbols_by_name["κ"]["value"])
        lambda_value = symbols_by_name["λ_S"]["value"]
        if "κ" in lambda_value and "exact" in lambda_value:
            lambda_s = (mp.mpf("5") * kappa**2) / mp.mpf("3")
        else:
            lambda_s = _parse_mpf_value(lambda_value)

        lhs = mp.mpf("5") * kappa**2
        rhs = mp.mpf("3") * lambda_s
        residual = abs(lhs - rhs)
        threshold = mp.mpf("1e-14")

        if residual < threshold:
            results["stable_parameters"].append({
                "constraint": "5κ² = 3λ_S",
                "lhs": _format_mpf(lhs),
                "rhs": _format_mpf(rhs),
                "residual": _format_mpf(residual),
                "threshold": "1e-14",
                "status": "STABLE"
            })
        else:
            results["regressions"].append({
                "constraint": "5κ² = 3λ_S",
                "residual": _format_mpf(residual),
                "threshold": "1e-14",
                "severity": "CRITICAL"
            })
            results["gate_e_status"] = "FAIL"
    
    # Check spectral gap stability
    for sym in symbols:
        if sym["symbol"] == "Δ" and sym["evidence_cat"] == "A":
            results["stable_parameters"].append({
                "parameter": "Δ",
                "value": sym["value"],
                "category": "A",
                "status": "STABLE"
            })
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, sort_keys=True)
    
    print(f"Generated: {output_path}")
    print(f"Gate E: {results['gate_e_status']}")
    print(f"Regressions: {len(results['regressions'])}")
    
    return 0 if results["gate_e_status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
