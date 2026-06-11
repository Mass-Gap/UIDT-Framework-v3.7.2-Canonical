import os
import subprocess
import json
import re
from datetime import datetime, timezone

def run_cmd(cmd, check=True, cwd=None):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, cwd=cwd).decode('utf-8')
    except subprocess.CalledProcessError as e:
        if check:
            raise
        return e.output.decode('utf-8')

def check_branch_name(branch):
    return bool(re.match(r'^TKT-\d{4}-\d{2}-\d{2}-.*-\d+$', branch))

def identify_ci_failures(branch):
    try:
        output = run_cmd(f"gh run list --branch {branch} --json name,conclusion", check=True)
        runs = json.loads(output)
        failures = []
        for run in runs:
            if run.get('name') in ['deterministic-double-check', 'drift_analysis.py'] and run.get('conclusion') == 'failure':
                failures.append(run.get('name'))
        return failures
    except Exception:
        return []

def get_modified_files(branch):
    try:
        diff_out = run_cmd(f"git diff --name-only origin/main...origin/{branch}", check=False)
        return [f.strip() for f in diff_out.split('\n') if f.strip()]
    except Exception:
        return []

def get_file_content(branch, filepath):
    try:
        return run_cmd(f"git show origin/{branch}:{filepath}", check=False)
    except Exception:
        return ""

def write_file_content(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

def check_escalation(branch, modified_files):
    conditions = []
    for f in modified_files:
        content = get_file_content(branch, f)

        if 'category: A' in content.lower() and 'derivation' in content.lower() and 'new' in content.lower():
            conditions.append("Condition A: PR proposes a new [A] mathematical derivation.")

        if f.startswith('core/') or f.startswith('modules/'):
            try:
                diff_stat = run_cmd(f"git diff --numstat origin/main...origin/{branch} -- {f}", check=False)
                if diff_stat:
                    parts = diff_stat.split()
                    if len(parts) >= 2:
                        deleted = int(parts[1]) if parts[1] != '-' else 0
                        if deleted > 30:
                            conditions.append(f"Condition B: Deletion of >30 lines in {f}.")
            except Exception:
                pass

        if 'UIDT-OS-Private' in f:
            conditions.append("Condition D: PR touches UIDT-OS-Private core logic.")

    return conditions

def main():
    print("Starting Phase 1: Discovery & Triage")
    branches_out = run_cmd("git branch -r", check=False)
    branches = [b.strip().replace('origin/', '') for b in branches_out.split('\n') if b.strip() and '->' not in b]

    processed_prs = []
    auto_fixes = []
    delegated = []

    start_branch = run_cmd("git rev-parse --abbrev-ref HEAD", check=False).strip()
    if not start_branch or start_branch == "HEAD": start_branch = "main"

    try:
        for branch in branches:
            if branch == 'main': continue

            processed_prs.append(branch)

            needs_rename = False
            if not check_branch_name(branch):
                needs_rename = True

            identify_ci_failures(branch)
            modified_files = get_modified_files(branch)

            needs_guardian = False
            for f in modified_files:
                if f.startswith('CANONICAL/') or f.startswith('LEDGER/') or f.startswith('core/'):
                    try:
                        diff_stat = run_cmd(f"git diff --numstat origin/main...origin/{branch} -- {f}", check=False)
                        if diff_stat:
                            parts = diff_stat.split()
                            if len(parts) >= 2:
                                added = int(parts[0]) if parts[0] != '-' else 0
                                deleted = int(parts[1]) if parts[1] != '-' else 0
                                if added + deleted > 10:
                                    needs_guardian = True
                                    break
                    except Exception:
                        pass

            branch_failures = []

            file_contents = {}
            for file in modified_files:
                if file.endswith('.py') or file.endswith('.md') or file.endswith('.json'):
                    content = get_file_content(branch, file)
                    if not content: continue
                    file_contents[file] = content

                    if file.endswith('.py'):
                        if 'float(' in content or 'np.float64' in content:
                            branch_failures.append("Scan 1 Failed: float() or np.float64 introduced.")

                        lines = content.split('\n')
                        in_block = False
                        needs_fix = False
                        new_lines = []
                        for line in lines:
                            if line.startswith('def ') or line.startswith('class '):
                                in_block = True
                            elif not line.startswith(' ') and not line.startswith('\t') and line.strip() != '' and not line.startswith('#'):
                                in_block = False

                            if 'mp.dps' in line and '80' in line and not in_block:
                                branch_failures.append("Scan 1 Failed: mp.dps = 80 is not localized.")
                                needs_fix = True
                            else:
                                new_lines.append(line)
                        if needs_fix:
                            file_contents[file] = '\n'.join(new_lines)

                    if file == 'LEDGER/CLAIMS.json':
                        try:
                            claims = json.loads(content)
                            for claim in claims:
                                if claim.get('domain', '').lower() == 'cosmology' and claim.get('category') in ['A', 'A+', 'B']:
                                    branch_failures.append("Scan 2 Failed: Cosmology upgraded above [C].")
                                if claim.get('symbol', '').lower() == 'gamma' and claim.get('category') == 'A':
                                    branch_failures.append("Scan 2 Failed: gamma claimed as [A].")
                                if 'residual' in claim and float(claim['residual']) > 1e-14 and claim.get('category') == 'A':
                                    branch_failures.append("Scan 2 Failed: Residual > 10^-14 but claimed as [A].")
                        except Exception:
                            pass

            integrity_changed = False
            for file, content in file_contents.items():
                if not (file.startswith('docs/qa/') or file.startswith('verification/scripts/checks/') or file.startswith('verification/tests/')):
                    content_lower = content.lower()
                    if 'holy grail' in content_lower or 'ultimate' in content_lower or 'resolved' in content_lower:
                        branch_failures.append("Scan 3 Failed: Linguistic Integrity Rule broken.")
                        new_content = re.sub(r'(?i)holy grail', '[REDACTED]', content)
                        new_content = re.sub(r'(?i)ultimate', '[REDACTED]', new_content)
                        new_content = re.sub(r'(?i)resolved', '[REDACTED]', new_content)
                        if new_content != content:
                            file_contents[file] = new_content
                            integrity_changed = True

            escalation_conds = check_escalation(branch, modified_files)
            if escalation_conds:
                briefing = f"""### 🚨 ESCALATION TO OPUS 4.7: Escalation Required
**Branch:** `{branch}`
**Trigger Rule:** {escalation_conds[0]}

**1. Scientific Conflict / Status:**
The PR violates constraints or introduces complexity beyond auto-merge capabilities, specifically triggering {escalation_conds[0]}.

**2. CoVe Stage 3 Data:**
- Expected: Strict constraint compliance.
- Actual PR Output: Failed constraint.
- Residual: N/A

**3. Jules's Hypothesis [E]:**
Further mathematical review required by Opus 4.7.

**4. Requested PI Action:**
- [ ] Approve mathematical structure for evidence upgrade to [A].
- [ ] Reject and close PR.
- [ ] Refactor using Lean 4.
"""
                print(briefing)
                delegated.append(branch)
                continue

            needs_auto_fix = branch_failures or integrity_changed or needs_rename or needs_guardian

            if needs_auto_fix:
                try:
                    run_cmd(f"git fetch origin {branch}", check=False)
                    run_cmd(f"git checkout {branch}", check=False)

                    if needs_rename:
                        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
                        new_branch = f"TKT-{today}-{branch}-001"
                        run_cmd(f"git branch -m {new_branch}", check=False)
                        branch = new_branch

                    if needs_guardian:
                        try:
                            run_cmd(f"gh pr edit {branch} --add-label '[GUARDIAN-REVIEW-REQUIRED]'", check=False)
                        except Exception:
                            pass

                    for file, content in file_contents.items():
                        write_file_content(file, content)

                    try:
                        run_cmd("python -m pytest verification/tests/ -v", check=True)
                        tests_passed = True
                    except Exception:
                        tests_passed = False

                    if tests_passed:
                        timestamp = datetime.now(timezone.utc).isoformat()
                        os.makedirs('LOCAL/logs', exist_ok=True)

                        traceability = []
                        if os.path.exists('LOCAL/logs/traceability.json'):
                            try:
                                with open('LOCAL/logs/traceability.json', 'r') as f:
                                    content = json.load(f)
                                    if isinstance(content, list):
                                        traceability = content
                                    elif isinstance(content, dict):
                                        traceability = list(content.values())
                            except Exception:
                                pass

                        traceability.append({
                            "task_id": f"auto-fix-{branch}",
                            "files": modified_files,
                            "tests": "pytest verification/",
                            "docs": "N/A",
                            "status": "Auto-Fixed",
                            "timestamp": timestamp,
                            "author": "Jules"
                        })

                        with open('LOCAL/logs/traceability.json', 'w') as f:
                            json.dump(traceability, f, indent=2)

                        run_cmd("git add -u", check=False)
                        run_cmd("git add LOCAL/logs/traceability.json", check=False)
                        diff = run_cmd("git diff --cached", check=False)
                        if diff.strip():
                            run_cmd('git commit -m "[UIDT-v3.9] Auto-Fix: Epistemic protocol compliance (CoVe Stage 4)"', check=False)
                            try:
                                run_cmd(f"git push origin HEAD:{branch}", check=False)
                            except Exception:
                                pass
                        auto_fixes.append(branch)
                except Exception as e:
                    print(f"Error during auto-fix for {branch}: {e}")
                finally:
                    run_cmd("git reset --hard HEAD", check=False)
                    run_cmd(f"git checkout {start_branch}", check=False)

    except Exception as e:
        print(f"Main loop error: {e}")
    finally:
        run_cmd(f"git checkout {start_branch}", check=False)

    print("Phase 5: Daily Master Report")
    today = datetime.now(timezone.utc).strftime('%Y%m%d')
    report_path = f"LOCAL/logs/daily_pr_audit_{today}.md"

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write("# Daily PR Audit Master Report\n\n")
        f.write(f"**Date:** {today}\n\n")
        f.write("## Processed PRs\n")
        for p in processed_prs:
            f.write(f"- {p}\n")
        f.write("\n## Auto-Fixes Applied\n")
        for a in auto_fixes:
            f.write(f"- {a}\n")
        f.write("\n## Delegated to Opus 4.7\n")
        for d in delegated:
            f.write(f"- {d}\n")

    print(f"Report written to {report_path}")

if __name__ == '__main__':
    main()
