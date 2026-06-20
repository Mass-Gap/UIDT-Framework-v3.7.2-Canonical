import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import time
import re
import sys

def query_arxiv(query, max_results=10):
    base_url = 'http://export.arxiv.org/api/query?'
    # Clean the query for better arXiv results, but use words separated by AND
    query_terms = query.replace('"', '').split()
    search_query = " AND ".join([f'all:"{term}"' for term in query_terms])

    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    url = base_url + urllib.parse.urlencode(params)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            # Add a user-agent to be polite and avoid blocks
            req.add_header('User-Agent', 'UIDT-Framework-Literature-Monitor/1.0')
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    return response.read()
        except urllib.error.HTTPError as e:
            if e.code in [503, 429]:
                # Graceful handling of rate limits
                time.sleep(5 * (attempt + 1))
                continue
            else:
                # Other HTTP errors
                break
        except urllib.error.URLError as e:
            # Handle connection errors gracefully without failing
            break
        except Exception as e:
            break

    return None

def parse_and_check_triggers(xml_data):
    if not xml_data:
        return

    # Use arXiv namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    try:
        root = ET.fromstring(xml_data)
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
            id_url = entry.find('atom:id', ns).text.strip()
            # Try to find DOI if it exists
            doi_element = entry.find('{http://arxiv.org/schemas/atom}doi')
            if doi_element is not None:
                paper_id = doi_element.text.strip()
            else:
                paper_id = id_url.split('/')[-1]

            text_to_search = f"{title} {summary}"

            # Check DESI trigger: w = -1.00 \pm 0.01 (pure \Lambda CDM) -> Falsification Trigger #3
            # Allow variations like w=-1.00 \pm 0.01, w = -1.00 +- 0.01, etc.
            desi_match = re.search(r'w\s*(?:=|≈|\\approx)\s*-1\.00\s*(?:\\pm|\+-|±)\s*0\.01', text_to_search, re.IGNORECASE)
            if desi_match:
                print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies w = -1.00 ± 0.01. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim UIDT-C-068 to Category [E-withdrawn].")

            # Check Lattice QCD trigger: mass gap != 1.710 GeV at >3\sigma -> Falsification Trigger #1
            # We look for a mass gap that is NOT 1.710 and mentions >3\sigma or > 3 sigma.
            # This is complex to regex purely, but we can look for mass gap and sigma.
            # A strict regex might be hard, so we look for "mass gap" and a value, then sigma.
            # Let's look for explicit falsification text or combinations.
            mass_gap_match = re.search(r'mass gap.*(?:=|≈|is)\s*([0-9\.]+)\s*GeV', text_to_search, re.IGNORECASE)
            sigma_match = re.search(r'(?:>|greater than)\s*3\s*(?:\\sigma|sigma|σ)', text_to_search, re.IGNORECASE)

            if mass_gap_match and sigma_match:
                value = float(mass_gap_match.group(1))
                if abs(value - 1.710) > 0.015: # Not 1.710
                    print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies Lattice QCD mass gap = {value} GeV at >3σ. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim UIDT-C-001 to Category [E-withdrawn].")

    except ET.ParseError:
        pass


def main():
    queries = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    for query in queries:
        # We don't want to spam stdout unless there's a trigger.
        xml_data = query_arxiv(query, max_results=10)
        if xml_data:
            parse_and_check_triggers(xml_data)

if __name__ == "__main__":
    main()
