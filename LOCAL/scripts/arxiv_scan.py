import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

def scan_abstract(text):
    # Check for DESI Trigger: w = -1.00 \pm 0.01
    # Match various ways it could be written, e.g. w = -1.00 \pm 0.01, w = -1.00 +/- 0.01, w=-1.00\pm0.01
    match_desi = re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', text)
    if match_desi:
        return {"trigger": "DESI", "detail": match_desi.group(0).strip()}

    # Check for Lattice QCD Trigger: confirms mass gap != 1.710 GeV at >3\sigma
    # We look for explicit mentions of 1.710 in combination with exclusions >3\sigma
    # or explicit values that would exclude 1.710 at >3 sigma
    # Simplified approach for checking the regex for ">3\sigma" or ">3 sigma" with 1.710
    match_lattice = re.search(r'1\.710.*?(?:>|&gt;)\s*3\s*(?:\\sigma|sigma|σ)|(?:>|&gt;)\s*3\s*(?:\\sigma|sigma|σ).*?1\.710', text, re.IGNORECASE | re.DOTALL)
    if match_lattice:
        return {"trigger": "Lattice", "detail": "mass gap != 1.710 GeV at >3σ"}

    return None

def fetch_arxiv(query):
    # arXiv API endpoints
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=5'

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        if e.code in [503, 429]:
            # Graceful handle
            print(f"arXiv API unavailable or rate limited (HTTP {e.code}). Skipping query.")
            return None
        else:
            print(f"HTTP error {e.code}. Skipping query.")
            return None
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}. Skipping query.")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}. Skipping query.")
        return None

def process_results(data):
    if not data:
        return

    try:
        root = ET.fromstring(data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', namespace):
            abstract = entry.find('atom:summary', namespace)
            if abstract is not None:
                text = abstract.text
                result = scan_abstract(text)
                if result:
                    # Extract DOI or ArXiv ID
                    arxiv_id = entry.find('atom:id', namespace)
                    paper_id = arxiv_id.text if arxiv_id is not None else "Unknown ID"
                    paper_id = paper_id.split('/')[-1] # clean up url to just id

                    if result["trigger"] == "DESI":
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. Data implies {result['detail']}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
                    elif result["trigger"] == "Lattice":
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. Data implies {result['detail']}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
    except ET.ParseError:
        print("Failed to parse arXiv XML response.")

def main():
    queries = [
        'all:"Lattice QCD" AND all:"glueball" AND all:"continuum limit"',
        'all:"DESI" AND all:"dark energy" AND all:"equation of state"',
        'all:"Casimir effect" AND all:"anomaly" AND all:"precision measurement"'
    ]

    for query in queries:
        data = fetch_arxiv(query)
        if data:
            process_results(data)

if __name__ == "__main__":
    main()
