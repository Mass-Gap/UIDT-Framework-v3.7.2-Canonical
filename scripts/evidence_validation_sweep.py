#!/usr/bin/env python3
import subprocess
import re
import os
from datetime import datetime, timezone
import json

def run_command(command, check=False):
    try:
        result = subprocess.run(command, shell=True, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='replace')
        return result.stdout.strip(), result.returncode, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout.strip(), e.returncode, e.stderr

def get_open_prs():
    stdout, rc, stderr = run_command("git branch -r --no-merged origin/main")
    if rc != 0:
        return []
    branches = []
    for line in stdout.split('\n'):
        branch = line.strip()
        if branch.startswith("origin/"):
            branch = branch[7:]
        if branch and branch != "main" and branch != "HEAD":
            branches.append(branch)
    return branches

def get_diff_files(branch):
    stdout, rc, stderr = run_command(f"git diff origin/main..origin/{branch} --name-only")
    if rc == 0 and stdout:
        return stdout.split('\n')
    return []

def get_file_content(branch, filepath):
    stdout, rc, stderr = run_command(f"git show origin/{branch}:{filepath}")
    if rc == 0:
        return stdout
    return ""

def load_claims():
    try:
        with open("LEDGER/CLAIMS.json") as f:
            return json.load(f)
    except:
        return {}

def analyze_diff(branch, files):
    needs_guardian = False
    reasons = []
    core_deletions = 0

    for f in files:
        if f.startswith('CANONICAL/') or f.startswith('LEDGER/'):
            needs_guardian = True
            reasons.append(f"Modified protected directory: {f}")

        if f.startswith('core/') or f.startswith('modules/'):
            stdout, _, _ = run_command(f"git diff origin/main..origin/{branch} --numstat -- {f}")
            if stdout:
                parts = stdout.split('\t')
                if len(parts) >= 2 and parts[1].isdigit():
                    deletions = int(parts[1])
                    if deletions > 10:
                        needs_guardian = True
                        reasons.append(f"Core file {f} has >10 lines deleted ({deletions})")
                        core_deletions += deletions

    return needs_guardian, reasons, core_deletions

def fix_mp_dps(branch, files):
    """
    Simulates checking if a PR can be auto-fixed by fixing mp.dps.
    We won't actually push to remote.
    """
    fixed_files = []
    return False # Simplified for simulation

def audit_epistemic(branch, files):
    fails = []
    stdout, rc, stderr = run_command(f"git diff origin/main..origin/{branch}")
    if "float(" in stdout or "np.float64" in stdout or "scipy.float" in stdout:
        fails.append("Introduces float() or np.float64 instead of mpmath.")

    # Check linguistic integrity using the integrity_scan.sh script output
    run_command("git checkout origin/" + branch)
    scan_stdout, scan_rc, scan_stderr = run_command("scripts/integrity_scan.sh")
    run_command("git checkout -")
    if scan_rc != 0:
        fails.append(f"Linguistic Integrity: Used forbidden words (see AUDIT_TRAIL/integrity_violations.txt)")

    # Check claims file modifications
    if "LEDGER/CLAIMS.json" in files:
        old_claims_str = get_file_content("main", "LEDGER/CLAIMS.json")
        new_claims_str = get_file_content(branch, "LEDGER/CLAIMS.json")

        try:
            old_claims = json.loads(old_claims_str).get("claims", [])
            new_claims = json.loads(new_claims_str).get("claims", [])

            old_dict = {c["id"]: c for c in old_claims}

            for c in new_claims:
                old_c = old_dict.get(c["id"])
                if not old_c:
                    continue

                # Is cosmology upgraded above [C]?
                if c.get("type") == "cosmology" and c.get("evidence") in ["A", "A-", "B"]:
                    fails.append(f"Cosmology claim upgraded above [C]: {c['id']}")

                # Is gamma claimed as [A]?
                if "gamma" in c.get("statement", "").lower() and c.get("evidence") == "A":
                    fails.append(f"Gamma claimed as [A] instead of [A-]: {c['id']}")

        except Exception as e:
            fails.append(f"Could not parse CLAIMS.json: {str(e)}")

    return fails

def check_branch_naming(branch):
    # Just flagging, but could auto-fix if needed
    if not branch.startswith("TKT-") or len(branch.split("-")) < 3:
        return False
    return True

def generate_report():
    print("Starting Daily PR Audit (Jules)...")
    branches = get_open_prs()
    tkt_branches = [b for b in branches if "TKT" in b]

    report_lines = [f"# Daily PR Audit & Delegation Report - {datetime.now(timezone.utc).strftime('%Y-%m-%d')} UTC", ""]

    processed = 0
    delegated = 0
    auto_fixed = 0

    # Process all to find the ones with issues
    for branch in tkt_branches:
        files = get_diff_files(branch)
        if not files:
            continue

        processed += 1
        needs_guardian, reasons, core_deletions = analyze_diff(branch, files)
        fails = audit_epistemic(branch, files)

        if needs_guardian or fails or core_deletions > 30:
            delegated += 1
            report_lines.append(f"### 🚨 ESCALATION TO OPUS 4.7: Guardian Rule Triggered")
            report_lines.append(f"**Branch:** `{branch}`")

            trigger_rule = "Multiple Rules Triggered"
            if fails:
                trigger_rule = "Epistemic / Anti-Tampering Failure"
            elif core_deletions > 30:
                trigger_rule = f"Condition B: Deletion of >30 lines in core/ ({core_deletions} lines)"
            elif needs_guardian:
                trigger_rule = "Condition A/D: Modifying protected CANONICAL/LEDGER files or new derivations"

            report_lines.append(f"**Trigger Rule:** {trigger_rule}")

            report_lines.append("\n**1. Scientific Conflict / Status:**")
            report_lines.append("The PR modifies core files or introduces epistemic violations that require manual review.")
            for r in reasons + fails:
                report_lines.append(f"- {r}")

            report_lines.append("\n**2. CoVe Stage 3 Data:**")
            report_lines.append("- Expected: strict compliance with precision rules and evidence strata.")
            report_lines.append("- Actual PR Output: Failed epistemic or structural constraints.")

            report_lines.append("\n**3. Jules's Hypothesis [E]:**")
            report_lines.append("The changes might be an attempt to update parameters or simplify core physics logic without properly satisfying the residual and evidence constraints.")

            report_lines.append("\n**4. Requested PI Action:**")
            report_lines.append("- [ ] Approve mathematical structure for evidence upgrade to [A].")
            report_lines.append("- [ ] Reject and close PR.")
            report_lines.append("- [ ] Refactor using Lean 4.")
            report_lines.append("\n---\n")

    report_lines.insert(2, f"**Summary:** Processed {processed} PRs. Delegated {delegated}. Auto-fixed {auto_fixed}.\n")

    os.makedirs("LOCAL/logs", exist_ok=True)
    report_file = f"LOCAL/logs/daily_pr_audit_{datetime.now(timezone.utc).strftime('%Y%m%d')}.md"

    with open(report_file, 'w') as f:
        f.write("\n".join(report_lines))

    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    generate_report()
