#!/usr/bin/env python3
"""
claim_audit.py — UIDT LEDGER Claim Audit Tool v1.0
Checks CLAIMS.json against the v3.9 Canonical Parameter Ledger.
Output: audit_report.json

Evidence Tags: [A] exact proof | [A-] calibrated | [B] lattice | [C] cosmology | [D] prediction
Stratum: I=empirical | II=QFT consensus | III=UIDT mapping
"""
import json, hashlib, argparse
from pathlib import Path
from mpmath import mp, mpf, fabs

mp.dps = 80  # local precision block only

# ── Immutable Parameter Ledger (v3.9 Canonical) ─────────────────────────────
LEDGER = {
    "kappa":      mpf("0.500"),
    "lambda_S":   mpf("0.41666666666666666666666666666666666666666666666666666666"),
    "gamma":      mpf("16.339"),
    "gamma_inf":  mpf("16.3437"),
    "delta_gamma":mpf("0.0047"),
    "Delta":      mpf("1.710"),
    "v":          mpf("47.7e-3"),
    "m_S":        mpf("1.705"),
    "E_T":        mpf("2.44e-3"),
    "H0":         mpf("70.4"),
    "w0":         mpf("-0.99"),
}
RG_TOLERANCE    = mpf("1e-14")
CALIB_TOLERANCE = mpf("1e-3")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def check_rg_constraint() -> dict:
    kappa = LEDGER["kappa"]
    lam   = LEDGER["lambda_S"]
    residual = fabs(5 * kappa**2 - 3 * lam)
    ok = residual < RG_TOLERANCE
    return {
        "claim_id":  "RG-CANONICAL",
        "formula":   "5*kappa^2 - 3*lambda_S",
        "kappa":     mp.nstr(kappa, 20),
        "lambda_S":  mp.nstr(lam, 20),
        "residual":  mp.nstr(residual, 20),
        "tolerance": mp.nstr(RG_TOLERANCE, 5),
        "status":    "PASS" if ok else "[RG_CONSTRAINT_FAIL]",
        "evidence_tag": "[A]",
        "stratum":   "I",
    }


def audit_claims_json(path: Path) -> list:
    data = json.loads(path.read_text(encoding="utf-8"))
    claims = data if isinstance(data, list) else data.get("claims", [])
    results = []
    for claim in claims:
        cid   = claim.get("id", claim.get("claim_id", "?"))
        value = claim.get("value", claim.get("numerical_value", None))
        param = claim.get("parameter", claim.get("quantity", None))
        etag  = claim.get("evidence_tag", "?")
        stratum = claim.get("stratum", "?")
        if param and param in LEDGER and value is not None:
            try:
                v_claim  = mpf(str(value))
                v_ledger = LEDGER[param]
                diff = fabs(v_claim - v_ledger)
                tol  = RG_TOLERANCE if param in ("kappa", "lambda_S") else CALIB_TOLERANCE
                status = "MATCH" if diff < tol else "[TENSION ALERT]"
                results.append({
                    "claim_id":     cid,
                    "parameter":    param,
                    "claim_value":  mp.nstr(v_claim, 15),
                    "ledger_value": mp.nstr(v_ledger, 15),
                    "abs_diff":     mp.nstr(diff, 8),
                    "tolerance":    mp.nstr(tol, 5),
                    "evidence_tag": etag,
                    "stratum":      stratum,
                    "status":       status,
                })
            except Exception as e:
                results.append({"claim_id": cid, "parameter": param,
                                 "status": f"[AUDIT_FAIL] {e}"})
    return results


def main():
    parser = argparse.ArgumentParser(description="UIDT LEDGER Claim Audit v1.0")
    parser.add_argument("--claims", default="LEDGER/CLAIMS.json")
    parser.add_argument("--out",    default="audit_report.json")
    args = parser.parse_args()

    claims_path = Path(args.claims)
    assert claims_path.exists(), f"[BLOCKED] {claims_path} not found"

    report = {
        "manifest_version": "1.0",
        "framework":        "UIDT v3.9 Canonical",
        "doi":              "10.5281/zenodo.17835200",
        "ledger_sha256":    sha256_file(claims_path),
        "rg_check":         check_rg_constraint(),
        "claim_audits":     audit_claims_json(claims_path),
    }

    statuses = [c["status"] for c in report["claim_audits"]]
    report["summary"] = {
        "total":   len(statuses),
        "match":   statuses.count("MATCH"),
        "tension": sum(1 for s in statuses if "TENSION" in s),
        "fail":    sum(1 for s in statuses if "FAIL" in s or "BLOCKED" in s),
    }

    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Audit written → {args.out}")
    print(f"RG-Check: {report['rg_check']['status']}")
    print(f"Claims:   {report['summary']}")
    if report['rg_check']['status'] != 'PASS':
        raise SystemExit(1)


if __name__ == "__main__":
    main()
