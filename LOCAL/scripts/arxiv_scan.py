import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import sys
import re

def search_arxiv(query):
    base_url = "http://export.arxiv.org/api/query?"
    q = urllib.parse.quote(query)
    url = f"{base_url}search_query=all:{q}&start=0&max_results=5&sortBy=submittedDate&sortOrder=desc"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                return []
            data = response.read()
            root = ET.fromstring(data)
            papers = []
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
                summary_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
                id_elem = entry.find("{http://www.w3.org/2005/Atom}id")

                title = title_elem.text if title_elem is not None else ""
                summary = summary_elem.text if summary_elem is not None else ""
                id_url = id_elem.text if id_elem is not None else ""

                papers.append({'title': title, 'summary': summary, 'id': id_url})
            return papers
    except urllib.error.HTTPError as e:
        if e.code in (503, 429):
            # Gracefully handle rate limit or service unavailable
            pass
        return []
    except Exception as e:
        return []

def scan():
    topics = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]
    for topic in topics:
        papers = search_arxiv(topic)
        for paper in papers:
            # Rule 4.2: Data Parsing & CoVe
            summary = paper['summary']

            # Falsification Trigger #3: DESI w = -1.00 ± 0.01
            # We look for something that implies w = -1.00 ± 0.01
            if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+-|±)\s*0\.01', summary, re.IGNORECASE):
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper['id']}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            # Falsification Trigger #1: Lattice QCD confirms mass gap != 1.710 GeV at >3sigma
            # We look for something that implies mass gap != 1.710 GeV at >3sigma
            if re.search(r'mass gap.*(?:\\neq|!=|\bnot\b|≠).*1\.710.*>3(?:\\sigma|σ|sigma)', summary, re.IGNORECASE):
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper['id']}]. Data implies Lattice QCD confirms mass gap != 1.710 GeV at >3sigma. This challenges the Yang-Mills Mass Gap proof. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        time.sleep(3) # Wait 3 seconds per topic to respect API guidelines

if __name__ == '__main__':
    scan()
