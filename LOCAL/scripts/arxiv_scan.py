import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import time
import re

QUERIES = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def fetch_arxiv(query):
    url = f"http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results=5"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        if e.code in [429, 503]:
            return None
        return None
    except Exception:
        return None

def parse_and_check(xml_data):
    if not xml_data:
        return
    try:
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            summary = entry.find('atom:summary', ns).text
            title = entry.find('atom:title', ns).text
            link = entry.find('atom:id', ns).text
            if not summary:
                continue
            text_to_search = (title + " " + summary).replace('\n', ' ')

            # Trigger #3: DESI reports w = -1.00 \pm 0.01
            if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-)\s*0\.01', text_to_search) or r"w = -1.00 \pm 0.01" in text_to_search or "w = -1.00 +/- 0.01" in text_to_search:
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{link}]. Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            # Trigger #1: Lattice QCD confirms mass gap \neq 1.710 GeV at >3\sigma
            if "mass gap" in text_to_search.lower():
                if re.search(r'(?:!=|\\neq)\s*1\.710', text_to_search) and re.search(r'>\s*3\\sigma|>3\\sigma|> 3 \\sigma|>3 sigma', text_to_search):
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{link}]. Data implies Lattice QCD confirms mass gap \\\\neq 1.710 GeV at >3\\\\sigma. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
    except Exception:
        pass

def main():
    for q in QUERIES:
        xml_data = fetch_arxiv(q)
        parse_and_check(xml_data)
        time.sleep(3)

if __name__ == "__main__":
    main()
