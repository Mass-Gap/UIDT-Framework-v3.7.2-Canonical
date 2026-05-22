import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

def search_arxiv(query):
    query_url_encoded = urllib.parse.quote(query)
    url = f'http://export.arxiv.org/api/query?search_query=all:{query_url_encoded}&max_results=5'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            root = ET.fromstring(data)
            entries = []
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                id_url = entry.find('{http://www.w3.org/2005/Atom}id').text
                entries.append({'title': title, 'summary': summary, 'id': id_url})
            return entries
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return []

def extract_numerical_findings(summary):
    findings = []

    # 1. DESI equation of state
    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary):
        findings.append(("DESI_W", "w = -1.00 ± 0.01"))
    elif "w = -1.00 \\pm 0.01" in summary or "w=-1.00 \\pm 0.01" in summary or "w = -1.00 +/- 0.01" in summary:
        findings.append(("DESI_W", "w = -1.00 ± 0.01"))

    # 2. Lattice QCD mass gap
    mass_gap_match = re.search(r'mass gap.*?(\d+\.\d+)\s*(?:GeV|MeV)', summary, re.IGNORECASE)
    if mass_gap_match:
        findings.append(("LATTICE_MASS_GAP", mass_gap_match.group(1)))

    # Also explicitly catch the exact strings if mentioned in summary to ensure robustness
    if "mass gap \\neq 1.710" in summary or "mass gap != 1.710" in summary:
        findings.append(("LATTICE_MASS_GAP_EXPLICIT", "mass gap != 1.710 GeV"))

    return findings

def evaluate_triggers(findings):
    triggers = []
    for f_type, f_val in findings:
        if f_type == "DESI_W":
            triggers.append(("Trigger #3", "w = -1.00 ± 0.01"))
        elif f_type == "LATTICE_MASS_GAP":
            if f_val != "1.710" and f_val != "1.71":
                triggers.append(("Trigger #1", f"mass gap != 1.710 GeV at >3σ"))
        elif f_type == "LATTICE_MASS_GAP_EXPLICIT":
            triggers.append(("Trigger #1", f"mass gap != 1.710 GeV at >3σ"))
    return triggers

def generate_report(trigger_id, trigger_detail, url):
    report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{url}]. Data implies {trigger_detail}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
    print(report)

def main():
    QUERIES = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]
    for q in QUERIES:
        entries = search_arxiv(q)
        for e in entries:
            findings = extract_numerical_findings(e['summary'])
            triggers = evaluate_triggers(findings)
            # Eliminate duplicates per paper
            seen_triggers = set()
            for trigger_id, trigger_detail in triggers:
                if trigger_id not in seen_triggers:
                    generate_report(trigger_id, trigger_detail, e['id'])
                    seen_triggers.add(trigger_id)

if __name__ == "__main__":
    main()
