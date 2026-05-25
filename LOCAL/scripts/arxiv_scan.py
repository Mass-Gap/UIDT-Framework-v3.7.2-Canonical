import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

def search_arxiv(query):
    url = f'http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&max_results=50'
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        root = ET.fromstring(data)

        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', namespace)

        results = []
        for entry in entries:
            title_node = entry.find('atom:title', namespace)
            summary_node = entry.find('atom:summary', namespace)
            id_node = entry.find('atom:id', namespace)

            title = title_node.text if title_node is not None else ""
            summary = summary_node.text if summary_node is not None else ""
            id_url = id_node.text if id_node is not None else ""

            results.append({
                'title': title,
                'summary': summary,
                'id': id_url
            })
        return results
    except Exception as e:
        print(f"Error fetching from arXiv: {e}", file=sys.stderr)
        return []

def scan_for_triggers():
    queries = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    # regex to find w = -1.00 \pm 0.01 (or variations)
    desi_regex = re.compile(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01')

    # regex to find mass gap != 1.710 GeV at >3sigma (or variations)
    lattice_regex = re.compile(r'mass gap\s*(?:\\neq|!=|≠)\s*1\.710\s*GeV\s*at\s*>3(?:\\sigma|σ)')

    for query in queries:
        papers = search_arxiv(query)
        for paper in papers:
            summary = paper['summary'].replace('\n', ' ')

            desi_match = desi_regex.search(summary)
            if desi_match:
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper['id']}]. Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            lattice_match = lattice_regex.search(summary)
            if lattice_match:
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper['id']}]. Data implies mass gap \\neq 1.710 GeV at >3\\sigma. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

if __name__ == '__main__':
    scan_for_triggers()
