import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import datetime

def fetch_arxiv(query):
    url = f"http://export.arxiv.org/api/query?search_query=all:%22{urllib.parse.quote(query)}%22&start=0&max_results=5"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            return response.read()
    except urllib.error.HTTPError as e:
        if e.code in [429, 503]:
            return None
        return None
    except Exception as e:
        return None

def extract_doi_or_arxiv(entry_id, links):
    # Try to find a DOI link
    for link in links:
        title = link.attrib.get('title', '')
        if title == 'doi':
            return link.attrib.get('href', entry_id)
    return entry_id

def check_triggers(text, ref_id):
    # Trigger 3: DESI
    text_lower = text.lower()
    has_desi = "desi" in text_lower
    has_w = bool(re.search(r'w\s*(?:=|\simeq|\approx)\s*-1\.00\s*(?:\\\\pm|\\pm|\+/-|±)\s*0\.01', text_lower))

    if has_desi and has_w:
        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{ref_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
        return True

    # Trigger 1: Lattice QCD
    has_lattice = "lattice" in text_lower or "qcd" in text_lower
    has_1710 = "1.710" in text_lower
    has_sigma = bool(re.search(r'>\s*3\s*(?:\\\\sigma|\\sigma|sigma|σ)', text_lower))
    has_ineq = bool(re.search(r'(?:!=|\\\\neq|\\neq|not equal|deviation)', text_lower))

    if has_lattice and has_1710 and has_sigma and has_ineq:
        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{ref_id}]. Data implies Lattice QCD confirms mass gap \\neq 1.710 GeV at >3σ. This challenges the Yang-Mills mass gap proof. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")
        return True

    return False

def main():
    queries = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    for query in queries:
        xml_data = fetch_arxiv(query)
        if not xml_data:
            continue

        try:
            root = ET.fromstring(xml_data)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                entry_id = entry.find('{http://www.w3.org/2005/Atom}id').text
                links = entry.findall('{http://www.w3.org/2005/Atom}link')
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                title = entry.find('{http://www.w3.org/2005/Atom}title').text

                ref_id = extract_doi_or_arxiv(entry_id, links)
                check_triggers(summary + " " + title, ref_id)
        except Exception:
            continue

if __name__ == '__main__':
    main()
