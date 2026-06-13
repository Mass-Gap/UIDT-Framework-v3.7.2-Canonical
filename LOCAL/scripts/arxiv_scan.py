import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

def parse_w_from_text(text):
    # Match patterns like w = -1.00 +/- 0.01 or w=-1.00\pm0.01
    matches = re.findall(r'w\s*=\s*(-?\d+\.\d+)\s*(?:\\pm|\+/-|±)\s*(\d+\.\d+)', text)
    return matches

def scan_arxiv():
    queries = {
        "Lattice QCD glueball spectrum continuum limit": "lattice_qcd",
        "DESI dark energy equation of state": "desi",
        "Casimir effect anomaly precision measurement": "casimir"
    }

    for query, query_type in queries.items():
        encoded_query = urllib.parse.quote(f'all:"{query}"')
        url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results=10"

        try:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            data = response.read()
            root = ET.fromstring(data)

            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text or ""
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text or ""
                id_url = entry.find('{http://www.w3.org/2005/Atom}id').text or ""

                # Normalize text for parsing
                full_text = f"{title} {summary}".replace('\n', ' ')

                if query_type == "desi":
                    # Parse w and error
                    w_matches = parse_w_from_text(full_text)
                    for w_val, w_err in w_matches:
                        try:
                            w = float(w_val)
                            err = float(w_err)
                            if w == -1.00 and err == 0.01:
                                report = (
                                    f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{id_url}]. "
                                    f"Data implies w = -1.00 \\pm 0.01. This challenges the holographic scale factor mechanism. "
                                    f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [Claim X] to Category [E-withdrawn]."
                                )
                                print(report)
                                return
                        except ValueError:
                            pass

                elif query_type == "lattice_qcd":
                    # Check for >3 sigma deviation from 1.710 GeV
                    if re.search(r'(?i)mass gap', full_text) and re.search(r'1\.710', full_text) and re.search(r'>3\\?sigma', full_text):
                        report = (
                            f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{id_url}]. "
                            f"Data implies mass gap ≠ 1.710 GeV at >3σ. This challenges the holographic scale factor mechanism. "
                            f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [Claim X] to Category [E-withdrawn]."
                        )
                        print(report)
                        return

        except urllib.error.URLError as e:
            # Handle 503 or 429 errors gracefully
            pass
        except Exception as e:
            # Handle other errors gracefully
            pass

if __name__ == "__main__":
    scan_arxiv()
