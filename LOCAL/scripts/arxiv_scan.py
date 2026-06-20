import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re
import sys

def search_arxiv(query, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results={max_results}"
    try:
        response = urllib.request.urlopen(url)
        data = response.read()
        return ET.fromstring(data)
    except urllib.error.HTTPError as e:
        if e.code in [503, 429]:
            # Handle 503/429 gracefully without failing
            return None
        return None
    except Exception:
        return None

def scan():
    topics = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    for topic in topics:
        root = search_arxiv(topic)
        if root is None:
            continue

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            abstract = entry.find('{http://www.w3.org/2005/Atom}summary').text
            paper_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]

            # DESI w = -1.00 +/- 0.01
            if "DESI" in topic or "dark energy" in topic.lower():
                if re.search(r'w\s*[=≈]\s*-1\.00\s*(?:\\pm|\+-|±)\s*0\.01', abstract) or \
                   re.search(r'w\s*[=≈]\s*-1\.00\s*(?:\\pm|\+-|±)\s*0\.01', title):
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            # Lattice QCD mass gap != 1.710 GeV at >3\sigma
            if "Lattice QCD" in topic or "mass gap" in abstract.lower():
                match = re.search(r'(?:mass gap|glueball|mass).*?([0-9]\.[0-9]+)\s*GeV.*?>\s*([3-9]|\d{2,})\s*(?:\\sigma|σ|sigma)', abstract, re.IGNORECASE | re.DOTALL)
                if match:
                    val = float(match.group(1))
                    if abs(val - 1.710) > 0.001:
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. Data implies mass gap = {val} GeV (>3σ). This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

if __name__ == '__main__':
    scan()
