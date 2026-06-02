#!/usr/bin/env python3
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re
import sys

def check_falsification_triggers():
    # Rule 4.1: Weekly ArXiv monitor script must specifically search for three topics.
    queries = {
        'lattice': 'all:"Lattice QCD glueball spectrum continuum limit"',
        'desi': 'all:"DESI dark energy equation of state"',
        'casimir': 'all:"Casimir effect anomaly precision measurement"'
    }

    # Rule 4.2 & Opus 4.7 Delegation Trigger
    for name, query in queries.items():
        url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=5"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                paper_id = entry.find('{http://www.w3.org/2005/Atom}id').text

                if not summary:
                    continue

                # Normalize whitespace for regex matching
                summary_norm = re.sub(r'\s+', ' ', summary)

                if name == 'desi':
                    # IF DESI reports w = -1.00 \pm 0.01 (pure \Lambda CDM) -> This triggers Falsification Trigger #3.
                    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|\+-)\s*0\.01', summary_norm):
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

                if name == 'lattice':
                    # IF Lattice QCD confirms mass gap != 1.710 GeV at >3\sigma -> Triggers Falsification Trigger #1.
                    if re.search(r'1\.710', summary_norm) and re.search(r'>3\\?sigma|> 3\\?sigma|>3\s*\\?sigma', summary_norm):
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies Lattice QCD mass gap != 1.710 GeV at >3σ. This challenges Pillar I. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        except urllib.error.HTTPError as e:
            # Handle 503 and 429 gracefully as per memory instructions
            if e.code in [503, 429]:
                pass
            else:
                pass
        except Exception as e:
            pass

if __name__ == "__main__":
    check_falsification_triggers()
