#!/usr/bin/env python3
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Search queries
QUERIES = [
    "all:\"Lattice QCD glueball spectrum continuum limit\"",
    "all:\"DESI dark energy equation of state\"",
    "all:\"Casimir effect anomaly precision measurement\""
]

def check_falsification_triggers(text, doc_id):
    """
    Checks the text (abstract/title) for known falsification triggers.
    Returns a formatted Emergency Epistemic Report if a trigger is detected.
    """
    reports = []

    # Trigger 3: DESI reports w = -1.00 +/- 0.01
    desi_pattern = re.compile(r'w\s*(?:=|\simeq|\approx)\s*-1\.00\s*(?:\+/-|\\pm|\\pm\s*)\s*0\.01')
    if desi_pattern.search(text):
        report = (
            f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {doc_id}. "
            f"Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. "
            f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [Claim ID] to Category [E-withdrawn]."
        )
        reports.append(report)

    # Trigger 1: Lattice QCD confirms mass gap != 1.710 GeV at >3sigma
    # Example match: "mass gap is 1.65 GeV" or "\Delta = 1.65 GeV"
    # Note: We are looking for values significantly different from 1.710
    lattice_pattern = re.compile(r'(?:mass\s*gap|\Delta)\s*(?:=|\simeq|\approx)\s*(\d+\.\d+)\s*GeV')
    for match in lattice_pattern.finditer(text):
        try:
            val = float(match.group(1))
            if abs(val - 1.710) > 0.045: # Proxy for >3sigma assuming 0.015 sigma
                report = (
                    f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {doc_id}. "
                    f"Data implies Lattice QCD mass gap = {val} GeV (!= 1.710 GeV). "
                    f"This challenges the Yang-Mills mass gap proof. "
                    f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [Claim ID] to Category [E-withdrawn]."
                )
                reports.append(report)
        except ValueError:
            pass

    return reports

def scan_arxiv():
    all_reports = []
    for q in QUERIES:
        url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&start=0&max_results=5"
        try:
            response = urllib.request.urlopen(url)
            data = response.read()
            root = ET.fromstring(data)

            # XML namespaces
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                doc_id = entry.find('atom:id', ns).text
                summary = entry.find('atom:summary', ns).text
                title = entry.find('atom:title', ns).text

                text_to_search = f"{title} {summary}"
                reports = check_falsification_triggers(text_to_search, doc_id)
                all_reports.extend(reports)

        except urllib.error.URLError as e:
            logger.warning(f"Network error querying arXiv for {q}: {e}")
            continue
        except Exception as e:
            logger.warning(f"Error processing query {q}: {e}")
            continue

    for report in all_reports:
        print(report)

if __name__ == "__main__":
    scan_arxiv()
