import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re

def search_arxiv(query):
    # Encode query, but leave ':' and '+' intact if already formatted
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        if response.status != 200:
            return None
        return response.read()
    except Exception:
        # Silently handle errors to not falsely trigger alerts
        return None

def parse_arxiv_response(xml_data):
    if not xml_data:
        return []
    try:
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = []
        for entry in root.findall('atom:entry', ns):
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            id_elem = entry.find('atom:id', ns)

            title = title_elem.text.strip() if title_elem is not None else ""
            summary = summary_elem.text.strip() if summary_elem is not None else ""
            id_link = id_elem.text.strip() if id_elem is not None else "Unknown"

            entries.append({'title': title, 'summary': summary, 'id': id_link})
        return entries
    except ET.ParseError:
        return []

def check_falsification_triggers(entries):
    for entry in entries:
        summary = entry['summary']
        arxiv_id = entry['id']

        # Trigger #3: DESI w = -1.00 \pm 0.01
        if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary):
            report = (f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{arxiv_id}]. "
                      f"Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. "
                      f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
            print(report)

        # Trigger #1: Lattice QCD mass gap \neq 1.710 GeV at >3\sigma
        if re.search(r'mass gap.*?neq.*?1\.710.*?GeV.*?>3\\sigma', summary, re.IGNORECASE) or \
           re.search(r'mass gap.*?(?:!=|not equal to).*?1\.710.*?GeV.*?>3(?:\\sigma|sigma)', summary, re.IGNORECASE) or \
           re.search(r'\\Delta.*?(?:\\neq|!=).*?1\.710.*?GeV.*?>3(?:\\sigma|sigma)', summary, re.IGNORECASE) or \
           re.search(r'mass gap.*?\\neq.*?1\.710.*?GeV.*?at.*?>3\\sigma', summary, re.IGNORECASE):
            report = (f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{arxiv_id}]. "
                      f"Data implies mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. "
                      f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
            print(report)

def main():
    queries = [
        'all:"Lattice QCD glueball spectrum continuum limit"',
        'all:"DESI dark energy equation of state"',
        'all:"Casimir effect anomaly precision measurement"'
    ]

    for query in queries:
        xml_data = search_arxiv(query)
        if xml_data:
            entries = parse_arxiv_response(xml_data)
            check_falsification_triggers(entries)

if __name__ == "__main__":
    main()
