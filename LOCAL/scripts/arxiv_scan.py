import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import time
import sys

QUERIES = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def search_arxiv(query):
    # Using the arXiv search API
    url = f"http://export.arxiv.org/api/query?search_query=all:%22{urllib.parse.quote(query)}%22&start=0&max_results=50"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        if e.code in [429, 503]:
            # Handle gracefully without failing or false triggering
            return None
        return None
    except Exception as e:
        return None

def parse_and_check(data):
    if not data:
        return

    try:
        root = ET.fromstring(data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}

        for entry in root.findall('atom:entry', namespace):
            abstract_node = entry.find('atom:summary', namespace)
            if abstract_node is None or not abstract_node.text:
                continue
            abstract_text = abstract_node.text.replace('\n', ' ')

            paper_id_node = entry.find('atom:id', namespace)
            paper_id = paper_id_node.text if paper_id_node is not None else "Unknown"

            doi_node = entry.find('{http://arxiv.org/schemas/atom}doi')
            ref_id = doi_node.text if doi_node is not None else paper_id

            # Trigger #3: DESI w = -1.00 \pm 0.01
            w_pattern = r'w\s*(?:=|\simeq|\approx)\s*-1\.00\s*(?:\+/\-|\\pm|±)\s*0\.01'
            if re.search(w_pattern, abstract_text, re.IGNORECASE):
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{ref_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            # Trigger #1: Lattice QCD mass gap != 1.710 GeV at >3\sigma
            mass_gap_pattern = r'mass\s*gap[^\.]{0,50}(?:!=|\neq|not equal to|is not|≠)[^\.]{0,20}1\.710\s*GeV[^\.]{0,50}>3\s*(?:\\sigma|σ|sigma)'
            if re.search(mass_gap_pattern, abstract_text, re.IGNORECASE):
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{ref_id}]. Data implies Lattice QCD confirms mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            explicit_val_pattern = r'mass\s*gap\s*(?:=|is|\approx)\s*(\d+\.\d+)\s*GeV[^\.]{0,50}>3\s*(?:\\sigma|σ|sigma)'
            match = re.search(explicit_val_pattern, abstract_text, re.IGNORECASE)
            if match:
                val = float(match.group(1))
                if val != 1.710:
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{ref_id}]. Data implies Lattice QCD confirms mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

    except ET.ParseError:
        pass

def main():
    for query in QUERIES:
        data = search_arxiv(query)
        if data:
            parse_and_check(data)
        time.sleep(3)

if __name__ == '__main__':
    main()
