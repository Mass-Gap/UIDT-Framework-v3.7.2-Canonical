import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

def search_arxiv(query):
    url = f'http://export.arxiv.org/api/query?search_query=all:{urllib.parse.quote(query)}&start=0&max_results=5'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)

        results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            doi_element = entry.find('{http://arxiv.org/schemas/atom}doi')
            doi = doi_element.text if doi_element is not None else None
            id_element = entry.find('{http://www.w3.org/2005/Atom}id')
            arxiv_id = id_element.text if id_element is not None else None

            results.append({
                'title': title.strip().replace('\n', ' '),
                'summary': summary.strip().replace('\n', ' '),
                'doi': doi,
                'arxiv_id': arxiv_id
            })
        return results
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def scan_and_report():
    queries = [
        "Lattice QCD glueball spectrum continuum limit",
        "DESI dark energy equation of state",
        "Casimir effect anomaly precision measurement"
    ]

    reports = []

    for query in queries:
        results = search_arxiv(query)
        for r in results:
            summary = r['summary']
            paper_id = r['doi'] if r['doi'] else r['arxiv_id']

            # Rule 4.2: Data Parsing & CoVe
            # IF DESI reports w = -1.00 +/- 0.01
            if "DESI" in query:
                # Basic regex for w = -1.00 +/- 0.01 or similar variations
                if re.search(r'w\s*=\s*-1\.00\s*(?:\\pm|\+/-|±)\s*0\.01', summary):
                    reports.append(
                        rf"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. "
                        rf"Data implies $w = -1.00 \pm 0.01$. This challenges the holographic scale factor mechanism. "
                        rf"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                    )

            # IF Lattice QCD confirms mass gap != 1.710 GeV at >3 sigma
            elif "Lattice" in query:
                # We would parse the mass gap. If it says e.g. mass gap is 1.85 GeV +/- 0.01 GeV
                # This is a placeholder for actual complex parsing
                match = re.search(r'mass gap.*?\s+([\d\.]+)\s*(?:\\pm|\+/-|±)\s*([\d\.]+)\s*GeV', summary, re.IGNORECASE)
                if match:
                    val = float(match.group(1))
                    err = float(match.group(2))
                    if abs(val - 1.710) / err > 3.0:
                        reports.append(
                            rf"🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper {paper_id}. "
                            rf"Data implies mass gap = {val} ± {err} GeV (>{abs(val - 1.710)/err:.1f}σ deviation from 1.710 GeV). "
                            rf"This challenges the spectral gap proof. "
                            rf"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn]."
                        )

    return reports

if __name__ == '__main__':
    reports = scan_and_report()
    for report in reports:
        print(report)
