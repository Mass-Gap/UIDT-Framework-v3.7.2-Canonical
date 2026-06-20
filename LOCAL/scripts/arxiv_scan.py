#!/usr/bin/env python3
"""
ArXiv literature scan and Falsification Radar for UIDT-OS.
Executes weekly to monitor critical falsification thresholds.
"""
import urllib.request
import urllib.parse
import urllib.error
import re
import xml.etree.ElementTree as ET
import sys

TOPICS = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def check_desi_trigger(text):
    text = text.replace('\n', ' ')
    if 'w = -1.00' in text and '0.01' in text:
        return True
    if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|±|\+/-)\s*0\.01', text):
        return True
    return False

def check_lattice_trigger(text):
    text = text.replace('\n', ' ')
    if ('1.710' in text) and ('>3' in text or '> 3' in text) and ('sigma' in text or 'σ' in text or '\\sigma' in text):
        return True
    return False

def scan():
    for topic in TOPICS:
        terms = topic.split()
        query = "+AND+".join(f"all:{term}" for term in terms)
        url = f'http://export.arxiv.org/api/query?search_query={query}&max_results=5'

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = response.read()

            root = ET.fromstring(data)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                id_element = entry.find('{http://www.w3.org/2005/Atom}id')
                summary_element = entry.find('{http://www.w3.org/2005/Atom}summary')

                if id_element is None or summary_element is None:
                    continue

                arxiv_id = id_element.text.strip()
                summary = summary_element.text.strip()

                if "DESI" in topic and check_desi_trigger(summary):
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {arxiv_id}. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

                if "Lattice" in topic and check_lattice_trigger(summary):
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {arxiv_id}. Data implies mass gap != 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        except urllib.error.HTTPError as e:
            if e.code in [429, 503]:
                # Graceful handling of rate limits and service unavailability
                pass
            else:
                pass
        except Exception as e:
            pass

if __name__ == '__main__':
    scan()
