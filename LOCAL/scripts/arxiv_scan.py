import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

QUERIES = [
    "all:\"Lattice QCD glueball spectrum continuum limit\"",
    "all:\"DESI dark energy equation of state\"",
    "all:\"Casimir effect anomaly precision measurement\""
]

def search_arxiv(query):
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&max_results=10&sortBy=submittedDate&sortOrder=descending"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status in [503, 429]:
                return []
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = []
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)

                title = title_elem.text.replace('\n', ' ') if title_elem is not None else "No Title"
                summary = summary_elem.text.replace('\n', ' ') if summary_elem is not None else "No Summary"
                id_url = id_elem.text if id_elem is not None else "No ID"

                entries.append({'title': title, 'summary': summary, 'id': id_url})
            return entries
    except urllib.error.HTTPError as e:
        return []
    except Exception as e:
        return []

def analyze_entries(entries):
    for entry in entries:
        summary = entry['summary']
        id_str = entry['id']

        # Check DESI trigger: w = -1.00 \pm 0.01
        if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-)\s*0\.01', summary) or 'w = -1.00 \\pm 0.01' in summary or 'w = -1.00 +/- 0.01' in summary:
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{id_str}]. Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        # Check Lattice QCD trigger: mass gap != 1.710 GeV at >3σ
        match = re.search(r'mass gap.*?\b(\d+\.\d+)\b.*?GeV.*?>\s*3\s*(?:\\sigma|sigma|σ)', summary, re.IGNORECASE)
        if match:
            mass_gap = float(match.group(1))
            if abs(mass_gap - 1.710) > 0.001:  # Using a small delta for float comparison
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{id_str}]. Data implies mass gap \\neq 1.710 GeV at >3\\sigma. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

def main():
    for q in QUERIES:
        entries = search_arxiv(q)
        analyze_entries(entries)

if __name__ == "__main__":
    main()
