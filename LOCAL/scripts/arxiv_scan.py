import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import json
import os

# URLs for arXiv API
BASE_URL = "http://export.arxiv.org/api/query?"

# Search topics
QUERIES = {
    "Lattice QCD glueball spectrum continuum limit": "all:\"Lattice QCD\" AND all:\"glueball spectrum\" AND all:\"continuum limit\"",
    "DESI dark energy equation of state": "all:DESI AND all:\"dark energy\" AND all:\"equation of state\"",
    "Casimir effect anomaly precision measurement": "all:\"Casimir effect\" AND all:anomaly AND all:\"precision measurement\""
}

def fetch_arxiv(query):
    params = urllib.parse.urlencode({
        "search_query": query,
        "start": 0,
        "max_results": 10,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    })
    url = BASE_URL + params
    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except urllib.error.HTTPError as e:
        if e.code in [503, 429]:
            # Handle rate limiting or service unavailable gracefully
            pass
        return None
    except Exception as e:
        return None


def check_triggers(xml_data, topic):
    triggers_found = []
    if not xml_data:
        return triggers_found

    try:
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', namespace)

        for entry in entries:
            summary_elem = entry.find('atom:summary', namespace)
            id_elem = entry.find('atom:id', namespace)
            if summary_elem is None or id_elem is None:
                continue

            abstract = summary_elem.text
            paper_id = id_elem.text.split('/')[-1]

            if "DESI" in topic:
                if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|±|\+/-)\s*0\.01', abstract) or "w = -1.00 \\pm 0.01" in abstract:
                    triggers_found.append({
                        "id": paper_id,
                        "trigger": "w = -1.00 \\pm 0.01",
                        "claim": "Claim [X]"
                    })
            elif "Lattice QCD" in topic:
                if re.search(r'mass gap.*(?:neq|\\neq|!=|not equal to).*1\.710', abstract, re.IGNORECASE) and re.search(r'>3\s*(?:\\sigma|sigma|σ)', abstract, re.IGNORECASE):
                    triggers_found.append({
                        "id": paper_id,
                        "trigger": "mass gap \\neq 1.710 GeV at >3\\sigma",
                        "claim": "Claim [X]"
                    })

    except ET.ParseError:
        pass

    return triggers_found


def generate_report(trigger_data):
    # Print the specified Emergency Epistemic Report format to standard output.
    report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{trigger_data['id']}]. Data implies {trigger_data['trigger']}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of {trigger_data['claim']} to Category [E-withdrawn]."
    print(report)

def main():
    for topic, query in QUERIES.items():
        xml_data = fetch_arxiv(query)
        triggers = check_triggers(xml_data, topic)
        for trigger in triggers:
            generate_report(trigger)

if __name__ == "__main__":
    main()
