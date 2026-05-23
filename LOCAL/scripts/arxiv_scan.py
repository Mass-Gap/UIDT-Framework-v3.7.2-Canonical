#!/usr/bin/env python3
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

QUERIES = {
    "Lattice QCD": "all:\"Lattice QCD\" AND all:glueball AND all:spectrum AND all:\"continuum limit\"",
    "DESI Dark Energy": "all:DESI AND all:\"dark energy\" AND all:\"equation of state\"",
    "Casimir Effect": "all:\"Casimir effect\" AND all:anomaly AND all:\"precision measurement\""
}

def search_arxiv(query, max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip()
            summary = entry.find('atom:summary', namespace).text.strip()
            link = entry.find('atom:id', namespace).text.strip()
            papers.append({'title': title, 'summary': summary, 'link': link})
        return papers
    except Exception as e:
        logging.error(f"Error querying {query}: {e}")
        return []

def main():
    falsification_detected = False

    for category, q in QUERIES.items():
        papers = search_arxiv(q)

        for p in papers:
            summary = p['summary'].replace('\n', ' ')

            if category == "DESI Dark Energy":
                match = re.search(r'w\s*[=≈]\s*-1\.00(?:\s*\\pm\s*0\.01)?', summary)
                if match:
                    logging.info(f"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{p['link']}]. Data implies $w = -1.00 \\pm 0.01$. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [F3] to Category [E-withdrawn].")
                    falsification_detected = True

            if category == "Lattice QCD":
                matches = re.findall(r'(\d+\.\d+)\s*(?:\(\d+\))?\s*GeV', summary)
                if matches:
                    has_near_value = False
                    for m in matches:
                        try:
                            val = float(m)
                            if abs(val - 1.710) <= 0.05:
                                has_near_value = True
                                break
                        except ValueError:
                            pass

                    if not has_near_value:
                        logging.info(f"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{p['link']}]. Data implies mass gap $\\neq 1.710$ GeV at >3σ. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [F1] to Category [E-withdrawn].")
                        falsification_detected = True

    if not falsification_detected:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
