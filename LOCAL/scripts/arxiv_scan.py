import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

def fetch_arxiv(query):
    # Search arXiv using the API
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:%22{encoded_query}%22&start=0&max_results=5"
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        return data
    except Exception as e:
        print(f"Error fetching arXiv for query '{query}': {e}", file=sys.stderr)
        return None

def parse_and_check(data, mock_summary=None, mock_id=None):
    if mock_summary:
        summary = mock_summary
        paper_id = mock_id or "Mock ID"

        # Check Falsification Trigger #3 (DESI)
        if re.search(r'w\s*=\s*-1\.00\s*(?:\\[pP]m|±|\+/-)\s*0\.01', summary):
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        # Check Falsification Trigger #1 (Lattice QCD)
        if re.search(r'mass gap.*(?:neq|≠|!=).*1\.710\s*GeV', summary, re.IGNORECASE) and re.search(r'>\s*3\s*(?:\\[sS]igma|σ|sigma)', summary, re.IGNORECASE):
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
        return

    if not data:
        return
    root = ET.fromstring(data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}

    for entry in root.findall('atom:entry', namespace):
        id_element = entry.find('atom:id', namespace)
        paper_id = id_element.text if id_element is not None else "Unknown ID"

        summary_element = entry.find('atom:summary', namespace)
        summary = summary_element.text if summary_element is not None else ""

        # Check Falsification Trigger #3 (DESI)
        if re.search(r'w\s*=\s*-1\.00\s*(?:\\[pP]m|±|\+/-)\s*0\.01', summary):
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        # Check Falsification Trigger #1 (Lattice QCD)
        if re.search(r'mass gap.*(?:neq|≠|!=).*1\.710\s*GeV', summary, re.IGNORECASE) and re.search(r'>\s*3\s*(?:\\[sS]igma|σ|sigma)', summary, re.IGNORECASE):
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

def run_scan(mock=False):
    if mock:
        # Test Trigger 3
        mock_summary_1 = r"The DESI Year 1 results show w = -1.00 \pm 0.01, which is pure LCDM."
        parse_and_check(None, mock_summary=mock_summary_1, mock_id="arXiv:2405.00001")

        # Test Trigger 1
        mock_summary_2 = r"Lattice QCD confirms mass gap != 1.710 GeV at >3\sigma confidence."
        parse_and_check(None, mock_summary=mock_summary_2, mock_id="arXiv:2405.00002")
        return

    queries = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    for query in queries:
        data = fetch_arxiv(query)
        parse_and_check(data)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mock":
        run_scan(mock=True)
    else:
        run_scan()
