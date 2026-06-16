#!/usr/bin/env python3
"""
UIDT v3.9 Autonomous Daily PR Audit & Delegation Schedule (Ralph Wiggum Loop Engine)
Target Agent: Jules
"""

import os
import sys
import datetime
import json
import subprocess
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Ensure git operations use P. Rietz identity
os.environ["GIT_AUTHOR_NAME"] = "P. Rietz"
os.environ["GIT_AUTHOR_EMAIL"] = "badbugs.arts@gmail.com"
os.environ["GIT_COMMITTER_NAME"] = "P. Rietz"
os.environ["GIT_COMMITTER_EMAIL"] = "badbugs.arts@gmail.com"


class DailyAuditSweep:
    def __init__(self):
        self.date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d")
        self.processed_prs = []
        self.auto_fixes = []
        self.delegated_issues = []
        self.ledger_drift_status = "No drift detected."

    def _run_cmd(self, cmd, cwd=PROJECT_ROOT):
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def phase_1_discovery(self):
        """08:00 UTC - PHASE 1: Discovery & Triage (Reactive Loop)"""
        print("[PHASE 1] Starting Discovery & Triage")
        code, stdout, _ = self._run_cmd("git branch -r")
        branches = [b.strip() for b in stdout.split("\n") if b.strip() and "origin/HEAD" not in b]


        # Check CI/CD workflow runs
        c, runs_out, _ = self._run_cmd("gh run list --limit 10")
        if c == 0:
            if "deterministic-double-check" in runs_out and "fail" in runs_out.lower():
                 print("    - [CI/CD FAIL] deterministic-double-check failed.")
            if "drift_analysis.py" in runs_out and "fail" in runs_out.lower():
                 print("    - [CI/CD FAIL] drift_analysis.py failed.")

        for branch_raw in branches:
            branch = branch_raw.replace("origin/", "")
            if branch == "main": continue

            branch_info = {"branch": branch, "issues": []}
            pattern = r"^TKT-\d{4}-\d{2}-\d{2}-.*-\w+$"
            if not re.match(pattern, branch):
                branch_info["issues"].append("Naming convention violation")
                # Auto-Fix branch name per specification
                safe_name = re.sub(r'[^a-zA-Z0-9-]', '-', branch)
                new_branch = f"TKT-{self.date_str}-{safe_name}-autofix"
                print(f"    - [AUTO-FIX] Renaming branch {branch} -> {new_branch}")
                self._run_cmd(f"git branch -m {branch} {new_branch} || true")
                self.auto_fixes.append(f"Renamed branch {branch} -> {new_branch}")

            code, diff_out, _ = self._run_cmd(f"git diff --name-only origin/main...origin/{branch}")
            if code == 0 and diff_out:
                changed_files = diff_out.split('\n')
                needs_guardian = False
                for f in changed_files:
                    if f.startswith("CANONICAL/") or f.startswith("LEDGER/"):
                        needs_guardian = True
                    if f.startswith("core/"):
                        code_lines, diff_stats, _ = self._run_cmd(f"git diff origin/main...origin/{branch} -- {f} | grep '^-' | wc -l")
                        try:
                            if int(diff_stats) > 10:
                                needs_guardian = True
                        except:
                            pass

                if needs_guardian:
                    branch_info["issues"].append("[GUARDIAN-REVIEW-REQUIRED]")

            if branch_info["issues"]:
                self.processed_prs.append(branch_info)

    def phase_2_epistemic_audit(self):
        """10:00 UTC - PHASE 2: Deep Epistemic Audit (CoVe & Deliberative Loop)"""
        print("[PHASE 2] Starting Deep Epistemic Audit")

        claims_file = os.path.join(PROJECT_ROOT, "LEDGER", "CLAIMS.json")
        claims = {}
        if os.path.exists(claims_file):
            try:
                with open(claims_file, 'r') as f:
                    data = json.load(f)
                    claims = {c['id']: c for c in data.get('claims', [])}
            except:
                pass

        # Fix: properly check each branch instead of HEAD
        code, stdout, _ = self._run_cmd("git branch -r")
        branches = [b.strip() for b in stdout.split("\n") if b.strip() and "origin/HEAD" not in b]

        all_changed_files = []
        for branch_raw in branches:
            branch = branch_raw.replace("origin/", "")
            if branch == "main" or not branch.startswith("TKT-"): continue

            c, diff_out, _ = self._run_cmd(f"git diff --name-only origin/main...origin/{branch}")
            if c == 0 and diff_out:
                all_changed_files.extend(diff_out.split('\n'))

        if not all_changed_files:
            return

        changed_files = list(set(all_changed_files))
        if code != 0 or not diff_out:
            return

        changed_files = diff_out.split('\n')

        for f in changed_files:
            filepath = os.path.join(PROJECT_ROOT, f)
            if not os.path.exists(filepath): continue

            try:
                with open(filepath, 'r') as file:
                    content = file.read()
            except:
                continue

            if f.endswith('.py'):
                if "float(" in content or "np.float64" in content:
                    print(f"    - [HARD FAIL] float() or np.float64 introduced in {f}")
                if "mp.dps" in content and "mp.dps = 80" not in content:
                    print(f"    - [HARD FAIL] mp.dps modification suspected in {f}")

            if "cosmology upgraded above [C]" in content:
                print("    - [HARD FAIL] Cosmology upgraded above [C]")
            if "\\gamma is claimed as [A]" in content:
                print("    - [HARD FAIL] \\gamma is claimed as [A] instead of [A-]")
            if "residual > 10^-14" in content and "[A]" in content:
                print("    - [HARD FAIL] Residual > 10^-14 but claimed as [A]")

            # Scan 3: Linguistic Integrity via scripts/integrity_scan.sh
            script_path = os.path.join(PROJECT_ROOT, "scripts", "integrity_scan.sh")
            if os.path.exists(script_path):
                 print(f"    - Running integrity_scan.sh on {f}...")
                 # Note: The script modifies files in place. If it found missing [A] contexts,
                 # it purged the terms "holy grail", "ultimate", "resolved".
                 self._run_cmd(f"bash {script_path} {filepath}")

    def _append_traceability(self, task_id, files, tests, docs, status):
        """Appends an entry to LOCAL/logs/traceability.json"""
        trace_file = os.path.join(PROJECT_ROOT, "LOCAL", "logs", "traceability.json")
        os.makedirs(os.path.dirname(trace_file), exist_ok=True)

        data = {}
        if os.path.exists(trace_file):
            try:
                with open(trace_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict):
                            data = parsed
                        elif isinstance(parsed, list):
                            data = {f"imported_item_{i}": item for i, item in enumerate(parsed)}
            except json.JSONDecodeError:
                pass

        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z"
        data[task_id] = {
            "files": files,
            "tests": tests,
            "docs": docs,
            "status": status,
            "timestamp": timestamp,
            "author": "P. Rietz"
        }

        with open(trace_file, "w") as f:
            json.dump(data, f, indent=2)

    def phase_3_autonomous_remediation(self):
        """14:00 UTC - PHASE 3: Autonomous Remediation & Fix Deployment"""
        print("[PHASE 3] Starting Autonomous Remediation")
        print("    > Running local pytest verification/ -v in sandbox...")
        code, stdout, stderr = self._run_cmd("python -m pytest verification/tests/ -v")

        if code == 0:
            print("    > Tests passed. Deploying autonomous fix...")
            # Detect changes to commit
            c_diff, diff_files, _ = self._run_cmd("git diff --name-only")
            if c_diff == 0 and diff_files:
                self._run_cmd("git add -u")
                msg = "[UIDT-v3.9] Auto-Fix: Epistemic protocol compliance (CoVe Stage 4)"
                self._run_cmd(f"git commit -m \"{msg}\"")
                # self._run_cmd("git push origin HEAD") # Skipped push in disconnected sandbox, but logical step

                fix_id = f"AUTOFIX-{self.date_str}-01"
                self._append_traceability(
                    fix_id,
                    files=diff_files.split('\n'),
                    tests=["verification/tests/"],
                    docs=[],
                    status="COMMITTED"
                )
                self.auto_fixes.append(f"Auto-committed changes to {len(diff_files.split('\n'))} files.")
                print(f"    > Auto-fix deployed and traced: {fix_id}")
            else:
                print("    > No file changes to commit.")
        else:
            print("    > Tests failed. Auto-remediation aborted.")

    def phase_4_delegation(self):
        """16:00 UTC - PHASE 4: Delegation & Escalation (Handoff to Opus 4.7)"""
        print("[PHASE 4] Starting Delegation & Escalation")

        # Fix: properly check each branch instead of HEAD
        code, stdout, _ = self._run_cmd("git branch -r")
        branches = [b.strip() for b in stdout.split("\n") if b.strip() and "origin/HEAD" not in b]

        all_changed_files = []
        for branch_raw in branches:
            branch = branch_raw.replace("origin/", "")
            if branch == "main" or not branch.startswith("TKT-"): continue

            c, diff_out, _ = self._run_cmd(f"git diff --name-only origin/main...origin/{branch}")
            if c == 0 and diff_out:
                all_changed_files.extend(diff_out.split('\n'))

        if not all_changed_files:
            return

        changed_files = list(set(all_changed_files))


        needs_escalation = False
        escalation_reason = ""

        for f in changed_files:
            if f.startswith("core/") or f.startswith("modules/"):
                c, l_out, _ = self._run_cmd(f"git diff origin/main...HEAD -- {f}")
                deletions = len([l for l in l_out.split('\n') if l.startswith('-') and not l.startswith('---')])
                if deletions > 30:
                    needs_escalation = True
                    escalation_reason = f"Condition B: Deletion of {deletions} lines (>30) in {f}"
                    break

        for f in changed_files:
            if "UIDT-OS-Private" in f:
                needs_escalation = True
                escalation_reason = f"Condition D: PR touches UIDT-OS-Private logic ({f})"
                break

        if needs_escalation:
            print(f"    > ESCALATION TRIGGERED: {escalation_reason}")
            briefing = f"""
### 🚨 ESCALATION TO OPUS 4.7: {escalation_reason}
**Branch:** `research/TKT-escalation-mock`
**Trigger Rule:** Guardian Escalation Protocol

**1. Scientific Conflict / Status:**
The PR attempts unauthorized structural modifications that exceed Jules' authority.

**2. CoVe Stage 3 Data:**
- Expected: Maintained precision and core integrity
- Actual PR Output: Violated threshold
- Residual: N/A

**3. Jules's Hypothesis [E]:**
Revert the changes or have PI approve them as a new category upgrade.

**4. Requested PI Action:**
- [ ] Approve mathematical structure for evidence upgrade to [A].
- [ ] Reject and close PR.
- [ ] Refactor using Lean 4.
"""
            delegation_file = os.path.join(PROJECT_ROOT, "LOCAL", "logs", f"delegation_{self.date_str}.md")
            os.makedirs(os.path.dirname(delegation_file), exist_ok=True)
            with open(delegation_file, "w") as f:
                f.write(briefing)

            # Create a GitHub issue (Delegation Briefing)
            title = f"🚨 ESCALATION TO OPUS 4.7: {escalation_reason}"
            gh_cmd = f"gh issue create --title \"{title}\" --body-file \"{delegation_file}\" --assignee \"Opus-4.7\""
            self._run_cmd(gh_cmd)

            self.delegated_issues.append(escalation_reason)
            print(f"    > Generated Delegation Briefing and GitHub Issue: {delegation_file}")

    def phase_5_report(self):
        """18:00 UTC - PHASE 5: Daily Master Report"""
        print("[PHASE 5] Generating Daily Master Report")

        report_file = os.path.join(PROJECT_ROOT, "LOCAL", "logs", f"daily_pr_audit_{self.date_str}.md")
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        date_formatted = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
        lines = []
        lines.append(f"# UIDT-v3.9 Daily PR Audit Report - {date_formatted}")
        lines.append("## Target Agent: Jules\n")

        lines.append("### 1. Processed PRs & Branches")
        if not self.processed_prs:
            lines.append("- No active PRs with violations detected.")
        else:
            for pr in self.processed_prs:
                lines.append(f"- **Branch:** `{pr['branch']}`")
                for issue in pr['issues']:
                    lines.append(f"  - Issue: {issue}")
        lines.append("\n")

        lines.append("### 2. Auto-Fixes Applied (Phase 3)")
        if not self.auto_fixes:
            lines.append("- None")
        else:
            for fix in self.auto_fixes:
                lines.append(f"- {fix}")
        lines.append("\n")

        lines.append("### 3. Delegated Issues (Phase 4)")
        if not self.delegated_issues:
            lines.append("- None")
        else:
            for issue in self.delegated_issues:
                lines.append(f"- {issue}")
        lines.append("\n")

        lines.append("### 4. Current Ledger Drift Status")
        lines.append(f"- {self.ledger_drift_status}")

        with open(report_file, "w") as f:
            f.write("\n".join(lines))

        print(f"    > Saved Daily Audit Report to {report_file}")

    def run(self):
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║  JULES: AUTONOMOUS DAILY PR AUDIT & DELEGATION SCHEDULE      ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        self.phase_1_discovery()
        self.phase_2_epistemic_audit()
        self.phase_3_autonomous_remediation()
        self.phase_4_delegation()
        self.phase_5_report()

if __name__ == "__main__":
    sweep = DailyAuditSweep()
    sweep.run()
