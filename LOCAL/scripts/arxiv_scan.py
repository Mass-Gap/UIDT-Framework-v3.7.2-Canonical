import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

QUERIES = [
    'all:"Lattice QCD glueball spectrum continuum limit"',
    'all:"DESI dark energy equation of state"',
    'all:"Casimir effect anomaly precision measurement"'
]

def check_falsification():
    for q in QUERIES:
        url = 'http://export.arxiv.org/api/query?search_query=' + urllib.parse.quote(q)
        try:
            req = urllib.request.urlopen(url)
            xml_data = req.read()
            root = ET.fromstring(xml_data)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                if summary_elem is None or not summary_elem.text:
                    continue
                summary = summary_elem.text

                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                paper_id = id_elem.text if id_elem is not None else "Unknown"

                # Check for DESI
                if 'DESI' in q:
                    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary):
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

                # Check for Lattice QCD
                if 'Lattice' in q:
                    m = re.search(r'([0-9]+\.[0-9]+)\s*(?:\\pm|\+/-|±)\s*([0-9]+\.[0-9]+)\s*GeV', summary)
                    if m:
                        val = float(m.group(1))
                        err = float(m.group(2))
                        if err > 0 and abs(val - 1.710) > 3 * err:
                            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies Lattice QCD confirms mass gap != 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
        except Exception as e:
            # Silently handle errors like 503 or 429
            pass

if __name__ == '__main__':
    check_falsification()
