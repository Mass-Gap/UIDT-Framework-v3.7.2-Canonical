import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import time
import re
import sys

def fetch_arxiv(query):
    url = f"http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&start=0&max_results=10&sortBy=submittedDate&sortOrder=desc"

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'UIDT-ArXiv-Scan/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    return response.read()
        except urllib.error.HTTPError as e:
            if e.code in [429, 503]:
                time.sleep((attempt + 1) * 2)
            else:
                break
        except urllib.error.URLError:
            break
        except Exception:
            break
    return None

def parse_entries(xml_data):
    if not xml_data:
        return []

    try:
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.replace('\n', ' ')
            id_url = entry.find('atom:id', ns).text
            entries.append({'title': title, 'summary': summary, 'id': id_url})
        return entries
    except ET.ParseError:
        return []

def main():
    queries = [
        "all:\"Lattice QCD\" AND all:\"glueball spectrum\" AND all:\"continuum limit\"",
        "all:\"DESI\" AND all:\"dark energy\" AND all:\"equation of state\"",
        "all:\"Casimir effect anomaly\" AND all:\"precision measurement\""
    ]

    reports = []

    for query in queries:
        xml_data = fetch_arxiv(query)
        entries = parse_entries(xml_data)

        for entry in entries:
            summary = entry['summary'].lower()

            # Check DESI trigger: w = -1.00 \pm 0.01
            if re.search(r'w\s*[=≈]\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary):
                reports.append(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{entry['id']}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

            # Check Lattice QCD trigger: mass gap != 1.710 at >3 sigma
            if re.search(r'(?:mass gap|glueball).*?(?:neq|≠|\\neq).*?1\.710.*?>\s*3\s*(?:\\sigma|sigma|σ|σ)', summary) or \
               re.search(r'(?:mass gap|glueball).*?(?:!=|is not).*?1\.710.*?>\s*3\s*(?:\\sigma|sigma|σ|σ)', summary):
                reports.append(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{entry['id']}]. Data implies Lattice QCD confirms mass gap ≠ 1.710 GeV at >3σ. This challenges the Yang-Mills mass gap proof. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

    for report in reports:
        print(report)

if __name__ == "__main__":
    main()
