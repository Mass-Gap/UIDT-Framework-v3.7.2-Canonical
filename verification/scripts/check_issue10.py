"""check_issue11.py — read-only remote check. No writes."""
import json, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
def tok():
    for p in (ROOT.parent / ".env", ROOT / ".env"):
        if p.exists():
            for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                s = line.strip()
                if s.startswith("GITHUB_PAT"):
                    return s.split("=", 1)[1].strip().strip('"').strip("'")
    return None

TOKEN = tok()
OWNER, REPO = "badbugsarts-hue", "UIDT-Framework-V3.9-UNIVERSUM_SIM"

def get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "uidt-audit"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

issue = get(f"https://api.github.com/repos/{OWNER}/{REPO}/issues/10")
print("STATE:", issue["state"], "| comments:", issue["comments"], "| updated_at:", issue["updated_at"])
print("assignees:", [a["login"] for a in issue.get("assignees", [])])

comments = get(f"https://api.github.com/repos/{OWNER}/{REPO}/issues/10/comments")
print(f"\n{len(comments)} comment(s) on remote:")
for c in comments:
    print(f"  - {c['user']['login']} @ {c['created_at']}: {c['body'][:120]!r}")

# Check for any recent branches/PRs referencing extraction/module-b/module-e work
prs = get(f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=all&sort=updated&direction=desc&per_page=10")
print(f"\nMost recent PRs (top 10):")
for p in prs:
    print(f"  #{p['number']} [{p['state']}] {p['title'][:70]} (updated {p['updated_at']})")
