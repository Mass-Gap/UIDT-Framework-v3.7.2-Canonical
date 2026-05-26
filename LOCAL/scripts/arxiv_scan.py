import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

# Constants
ARXIV_API_URL = 'http://export.arxiv.org/api/query'

QUERIES = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def check_falsification_triggers(abstract):
    triggers_detected = []

    # Check DESI Trigger #3
    # Look for w = -1.00 \pm 0.01
    # Simple regex to catch this:
    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', abstract) or re.search(r'w\s*=\s*-1\.00\s*\(\s*1\s*\)', abstract):
        triggers_detected.append({
            'type': 'DESI',
            'detail': 'w = -1.00 ± 0.01',
            'claim': 'Claim [C]'
        })

    # Check Lattice QCD Trigger #1
    if re.search(r'1\.710', abstract) and re.search(r'3\\sigma|3\s*sigma|3σ', abstract, re.IGNORECASE):
        triggers_detected.append({
            'type': 'Lattice QCD',
            'detail': 'mass gap != 1.710 GeV at >3σ',
            'claim': 'Claim [A]'
        })
    elif re.search(r'mass gap.*?excludes 1\.710', abstract, re.IGNORECASE):
        triggers_detected.append({
            'type': 'Lattice QCD',
            'detail': 'mass gap != 1.710 GeV at >3σ',
            'claim': 'Claim [A]'
        })

    return triggers_detected

def scan_arxiv():
    for query in QUERIES:
        # Use simpler search query for exact phrasing or keywords
        # The prompt says: "search for new papers related to: [phrases]"
        # Let's search with AND
        keywords = query.split()
        search_query = "all:" + " AND all:".join(keywords)
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': 10,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        query_string = urllib.parse.urlencode(params)
        url = f"{ARXIV_API_URL}?{query_string}"

        try:
            response = urllib.request.urlopen(url)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()
                id_element = entry.find('atom:id', ns).text.strip()

                arxiv_id = id_element.split('/abs/')[-1]

                triggers = check_falsification_triggers(summary)

                for trigger in triggers:
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {arxiv_id}. Data implies {trigger['detail']}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of {trigger['claim']} to Category [E-withdrawn].")

        except Exception as e:
            print(f"Error fetching data for query '{query}': {e}", file=sys.stderr)

if __name__ == "__main__":
    scan_arxiv()
