#!/usr/bin/env python3
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import sys
import time
import re

def search_arxiv(query):
    # Using specific query format for arXiv API
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
            summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
            id_elem = entry.find('{http://www.w3.org/2005/Atom}id')

            title = title_elem.text if title_elem is not None else ""
            summary = summary_elem.text if summary_elem is not None else ""
            id_url = id_elem.text if id_elem is not None else ""
            results.append({"title": title, "summary": summary, "id": id_url})

        return results
    except urllib.error.HTTPError as e:
        # Graceful handling of 503 or 429
        if e.code in (429, 503):
            pass # Just continue silently as requested, or log without failing
        else:
            print(f"Error accessing arXiv API: HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error accessing arXiv API: {e}", file=sys.stderr)
        return []

def evaluate_findings(results):
    for r in results:
        summary = r.get('summary', '')
        paper_id = r.get('id', '')

        # Trigger 3: DESI reports w = -1.00 ± 0.01
        # Matching various representations of \pm, +/-, ±, etc.
        if re.search(r"w\s*=\s*-1\.00\s*(?:\\pm|±|\+/-)\s*0\.01", summary):
            print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        # Trigger 1: Lattice QCD mass gap != 1.710 GeV at >3\sigma
        if re.search(r"mass gap", summary, re.IGNORECASE) and re.search(r"(?:>|greater than)\s*3\s*(?:\\sigma|σ)", summary, re.IGNORECASE):
            if "1.710" not in summary:
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies Lattice QCD mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

if __name__ == "__main__":
    queries = [
        "\"Lattice QCD glueball spectrum continuum limit\"",
        "\"DESI dark energy equation of state\"",
        "\"Casimir effect anomaly precision measurement\""
    ]

    for q in queries:
        results = search_arxiv(q)
        evaluate_findings(results)
        time.sleep(3) # Respect arXiv rate limits
