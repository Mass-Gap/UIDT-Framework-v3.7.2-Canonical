#!/usr/bin/env python3
"""
JULES: AUTONOMOUS DAILY PR AUDIT & DELEGATION SCHEDULE (Ralph Wiggum Loop Engine)
Target Agent: Jules (Junior Lead Research Agent)
Framework Version: UIDT v3.9 (v5.0 OS Protocols)
Authority Level: Branch Write Access / Draft PRs / NO DIRECT MERGE TO MAIN
"""

import datetime
import json
import os
import subprocess
import re
import sys

LOGS_DIR = "LOCAL/logs"
LOCAL_SCRIPTS_DIR = "LOCAL/scripts"
LEDGER_PATH = "LEDGER/CLAIMS.json"

def run_cmd(cmd, check=True):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"[SYSTEM-ERROR: Execution Unavailable] Command failed: {cmd}")
            print(f"Stderr: {e.stderr}")
            sys.exit(1)
        return e.stdout.strip() + "\n" + e.stderr.strip()

def setup_env():
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(LOCAL_SCRIPTS_DIR, exist_ok=True)
    if not os.path.exists(os.path.join(LOGS_DIR, "traceability.json")):
        with open(os.path.join(LOGS_DIR, "traceability.json"), "w") as f:
            json.dump({}, f)

def parse_pr_list():
    branches_output = run_cmd("git branch -a", check=False)
    prs = []
    for line in branches_output.split("\n"):
        line = line.strip()
        if not line or line.startswith("*") or "HEAD ->" in line:
            continue
        if "remotes/origin/" in line:
            branch = line.replace("remotes/origin/", "")
            if branch != "main":
                prs.append(branch)
    return prs

def check_branch_name(branch):
    pattern = r"^TKT-\d{4}-\d{2}-\d{2}-.+-\d+$"
    return bool(re.match(pattern, branch))

def phase1_discovery(prs):
    print("--- PHASE 1: Discovery & Triage (Reactive Loop) ---")
    processed_prs = []
    for pr in prs:
        status_info = {"branch": pr, "tags": [], "issues": []}
        if not check_branch_name(pr):
            status_info["issues"].append("Invalid branch name")

        diff_stats = run_cmd(f"git diff --numstat origin/main...origin/{pr} 2>/dev/null", check=False)
        guardian_required = False
        for line in diff_stats.split('\n'):
            if not line: continue
            parts = line.split('\t')
            if len(parts) >= 3:
                added = int(parts[0]) if parts[0] != '-' else 0
                deleted = int(parts[1]) if parts[1] != '-' else 0
                file_path = parts[2]
                if file_path.startswith('CANONICAL/') or file_path.startswith('LEDGER/') or file_path.startswith('core/'):
                    if added + deleted > 10:
                        guardian_required = True
                        break

        if guardian_required:
            status_info["tags"].append("[GUARDIAN-REVIEW-REQUIRED]")

        processed_prs.append(status_info)
    return processed_prs

def phase2_deep_audit(prs):
    print("--- PHASE 2: Deep Epistemic Audit (CoVe & Deliberative Loop) ---")
    for pr in prs:
        diff_text = run_cmd(f"git diff origin/main...origin/{pr['branch']} 2>/dev/null", check=False)
        if diff_text:
            if "float(" in diff_text or "np.float64" in diff_text:
                 pr["issues"].append("HARD FAIL: float() or np.float64 introduced.")

            # Scan 1 checks:
            # mp.dps = 80 must be localized. We can check if it's placed at the module scope vs function scope.
            # (A simplistic mock check for demonstration, actual AST parsing may be needed)

        integrity_scan_script = os.path.join(LOCAL_SCRIPTS_DIR, "integrity_scan.sh")
        if os.path.exists(integrity_scan_script):
             run_cmd(f"bash {integrity_scan_script} origin/{pr['branch']}", check=False)
    return prs

def phase3_autonomous_remediation(prs):
    print("--- PHASE 3: Autonomous Remediation & Fix Deployment ---")
    return prs

def create_delegation_briefing(pr, reason, conflict_status, expected, actual, residual, hypothesis):
    content = f"""### 🚨 ESCALATION TO OPUS 4.7: {reason}
**Branch:** `{pr['branch']}`
**Trigger Rule:** Guardian Escalation Protocol

**1. Scientific Conflict / Status:**
{conflict_status}

**2. CoVe Stage 3 Data:**
- Expected: {expected}
- Actual PR Output: {actual}
- Residual: {residual}

**3. Jules's Hypothesis [E]:**
{hypothesis}

**4. Requested PI Action:**
- [ ] Approve mathematical structure for evidence upgrade to [A].
- [ ] Reject and close PR.
- [ ] Refactor using Lean 4.
"""
    print(content)

def phase4_delegation(prs):
    print("--- PHASE 4: Delegation & Escalation (Handoff to Opus 4.7) ---")
    for pr in prs:
        diff_stats = run_cmd(f"git diff --numstat origin/main...origin/{pr['branch']} 2>/dev/null", check=False)
        core_deleted = 0
        for line in diff_stats.split('\n'):
            if not line: continue
            parts = line.split('\t')
            if len(parts) >= 3:
                deleted = int(parts[1]) if parts[1] != '-' else 0
                file_path = parts[2]
                if file_path.startswith('core/') or file_path.startswith('modules/'):
                     core_deleted += deleted

        if core_deleted > 30:
            create_delegation_briefing(
                pr,
                reason="Core Code Mutation > 30 lines",
                conflict_status="Deletion of >30 lines in core/ or modules/. Escalation to Opus 4.7 required.",
                expected="<= 30 lines deleted",
                actual=str(core_deleted),
                residual="N/A",
                hypothesis="Refactoring or removal of critical components."
            )

def phase5_daily_report(processed_prs):
    print("--- PHASE 5: Daily Master Report ---")
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
    report_path = os.path.join(LOGS_DIR, f"daily_pr_audit_{date_str}.md")

    report_content = f"# Daily PR Audit Report\n**Date:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n**Agent:** Jules\n\n## Processed PRs\n"
    for pr in processed_prs:
         issues_str = ", ".join(pr['issues']) if pr['issues'] else "None"
         tags_str = ", ".join(pr['tags']) if pr['tags'] else "None"
         report_content += f"- **{pr['branch']}**\n  - Issues: {issues_str}\n  - Tags: {tags_str}\n"

    with open(report_path, "w") as f:
         f.write(report_content)
    print(f"Generated {report_path}")

def main():
    print("Starting Ralph Wiggum Loop Engine...")
    setup_env()
    prs_mock = ["research/L4-BMW-gamma-derivation", "jules-arxiv-falsification-radar-14967929050804959967"]
    prs_status = phase1_discovery(prs_mock)
    prs_status = phase2_deep_audit(prs_status)
    prs_status = phase3_autonomous_remediation(prs_status)
    phase4_delegation(prs_status)
    phase5_daily_report(prs_status)
    print("Ralph Wiggum Loop Engine completed.")

if __name__ == "__main__":
    main()
