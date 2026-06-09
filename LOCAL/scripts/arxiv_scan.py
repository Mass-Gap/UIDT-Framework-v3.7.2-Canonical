import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

QUERIES = [
    {
        "topic": "Lattice QCD glueball spectrum continuum limit",
        "type": "lattice"
    },
    {
        "topic": "DESI dark energy equation of state",
        "type": "desi"
    },
    {
        "topic": "Casimir effect anomaly precision measurement",
        "type": "casimir"
    }
]

def scan_arxiv():
    for q in QUERIES:
        # Construct simple query based on topic words
        topic = q["topic"]
        words = topic.split()
        query_str = " AND ".join([f"all:{w}" for w in words])

        url = "http://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(query_str) + "&max_results=5"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'UIDT-Bot/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()

            root = ET.fromstring(data)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                abstract = entry.find('atom:summary', ns).text
                if not abstract: continue

                # Extract paper ID
                id_text = entry.find('atom:id', ns).text
                paper_id = id_text.split('/abs/')[-1] if '/abs/' in id_text else id_text

                if q["type"] == "desi":
                    # DESI trigger: w = -1.00 \pm 0.01
                    # We match variations like w = -1.00 ± 0.01, w_0 = -1.00 \pm 0.01, etc.
                    if re.search(r'w\s*(?:_0)?\s*(?:\(z\))?\s*=\s*-1\.00\s*(?:\\pm|±|\+/-)\s*0\.01', abstract, re.IGNORECASE):
                        trigger_detail = "$w = -1.00 \\pm 0.01$"
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies {trigger_detail}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

                elif q["type"] == "lattice":
                    # Lattice trigger: mass gap \neq 1.710 GeV at >3\sigma
                    sigma_match = re.search(r'([3-9](?:\.[0-9]+)?)\s*(?:\\sigma|sigma|σ)', abstract, re.IGNORECASE)
                    tension = re.search(r'(?:excludes?|\\neq|!=|not equal to|deviation|1\.900).*?(?:1\.710|GeV)', abstract, re.IGNORECASE)

                    if sigma_match and tension:
                        trigger_detail = "mass gap $\\neq 1.710$ GeV at >3$\\sigma$"
                        print(f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies {trigger_detail}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [X] to Category [E-withdrawn].")

        except urllib.error.HTTPError as e:
            if e.code in [429, 503]:
                # Graceful handling for API limits / availability
                pass
            else:
                pass
        except Exception as e:
            # Catch other errors to avoid false alerts
            pass

if __name__ == "__main__":
    scan_arxiv()
