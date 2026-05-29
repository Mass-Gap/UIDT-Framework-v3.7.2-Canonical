import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

QUERIES = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def check_trigger_desi(summary):
    # Looking for w = -1.00 \pm 0.01
    pattern = r"w\s*=\s*-1\.00\s*(?:\\pm|±)\s*0\.01"
    if re.search(pattern, summary, re.IGNORECASE):
        return True, "$w = -1.00 \\pm 0.01$"
    return False, None

def check_trigger_lattice(summary):
    # Looking for mass gap != 1.710 GeV at >3\sigma
    # We can be a bit flexible in the regex
    if "1.710" in summary and ("≠" in summary or "\\neq" in summary or "!=" in summary) and (">3σ" in summary or ">3\\sigma" in summary or "> 3\\sigma" in summary or "> 3σ" in summary):
        return True, "mass gap $\\neq 1.710$ GeV at >3$\\sigma$"

    # Or just a broad regex
    pattern = r"mass\s*gap.*?1\.710.*?GeV.*?>\s*3\s*(?:\\sigma|σ)"
    if re.search(pattern, summary, re.IGNORECASE):
        return True, "mass gap $\\neq 1.710$ GeV at >3$\\sigma$"
    return False, None

def generate_report(paper_id, trigger_detail, claim_x):
    report = (f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. "
              f"Data implies {trigger_detail}. This challenges the holographic scale factor mechanism. "
              f"Requesting immediate Opus 4.7 evaluation for potential downgrade of Claim [{claim_x}] to Category [E-withdrawn].")
    print(report)

def main():
    for q in QUERIES:
        url = 'http://export.arxiv.org/api/query?search_query=all:' + urllib.parse.quote(q) + '&max_results=10'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            data = response.read()
            root = ET.fromstring(data)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                id_el = entry.find('{http://www.w3.org/2005/Atom}id')
                paper_id = id_el.text if id_el is not None else "Unknown"

                summary_el = entry.find('{http://www.w3.org/2005/Atom}summary')
                summary = summary_el.text if summary_el is not None else ""

                if "DESI" in q:
                    hit, detail = check_trigger_desi(summary)
                    if hit:
                        generate_report(paper_id, detail, "UIDT-C-020")
                elif "Lattice QCD" in q:
                    hit, detail = check_trigger_lattice(summary)
                    if hit:
                        generate_report(paper_id, detail, "UIDT-C-030")

        except urllib.error.HTTPError as e:
            if e.code in [429, 503]:
                # Handled gracefully as requested by system directive
                pass
            else:
                logging.error(f"HTTPError {e.code} for query: {q}")
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
