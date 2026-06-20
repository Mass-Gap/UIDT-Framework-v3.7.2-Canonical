import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

def query_arxiv(search_query):
    # Construct ArXiv API URL
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&sortBy=submittedDate&sortOrder=desc&max_results=5"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = response.read()
        root = ET.fromstring(data)

        entries = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title_node = entry.find('{http://www.w3.org/2005/Atom}title')
            summary_node = entry.find('{http://www.w3.org/2005/Atom}summary')
            id_node = entry.find('{http://www.w3.org/2005/Atom}id')

            title = title_node.text.replace('\n', ' ') if title_node is not None else ""
            summary = summary_node.text.replace('\n', ' ') if summary_node is not None else ""
            doi_link = id_node.text if id_node is not None else ""
            entries.append({'title': title, 'summary': summary, 'doi': doi_link})
        return entries
    except Exception as e:
        # Avoid crashing on 503 or 429 errors per instructions
        # Do not output mock reports when querying fails
        pass
        return []

def scan_for_triggers():
    # Use exact phrases but with standard query format
    queries = [
        "all:\"Lattice QCD glueball spectrum continuum limit\"",
        "all:\"DESI dark energy equation of state\"",
        "all:\"Casimir effect anomaly precision measurement\""
    ]

    for q_str in queries:
        query = urllib.parse.quote(q_str)
        entries = query_arxiv(query)
        for entry in entries:
            summary = entry['summary']
            title = entry['title']
            doi = entry['doi']
            content = title + " " + summary

            # Check DESI trigger (Trigger #3)
            # Match variations of w = -1.00 +/- 0.01
            if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', content):
                report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{doi}]. Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                print(report)

            # Check Lattice QCD trigger (Trigger #1)
            # Falsification Threshold: Continuum limit excludes 1.710 GeV at >3σ confidence
            if "1.710" in content and re.search(r'>\s*3\s*(?:\\sigma|sigma|σ)', content) and ("neq" in content or "not equal" in content or "\neq" in content or "exclude" in content or "!=" in content):
                report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{doi}]. Data implies Lattice QCD mass gap \\neq 1.710 GeV at >3\\sigma. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                print(report)

if __name__ == '__main__':
    scan_for_triggers()
