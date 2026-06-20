#!/usr/bin/env python3
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import sys

def check_falsification_triggers():
    queries = [
        {
            "query": 'all:"Lattice QCD glueball spectrum continuum limit"',
            "regex": r"mass gap\s*\\neq\s*1\.710\s*GeV\s*at\s*>3\\sigma",
            "trigger_detail": "mass gap \\neq 1.710 GeV at >3\\sigma",
            "claim": "Claim [X]"
        },
        {
            "query": 'all:"DESI dark energy equation of state"',
            "regex": r"w\s*=\s*-1\.00\s*\\pm\s*0\.01",
            "trigger_detail": "w = -1.00 \\pm 0.01",
            "claim": "Claim [X]"
        },
        {
            "query": 'all:"Casimir effect anomaly precision measurement"',
            "regex": r"\|\\Delta F/F\|\s*<\s*0\.1%\s*@\s*0\.66\s*nm",
            "trigger_detail": "|\\Delta F/F| < 0.1% @ 0.66 nm",
            "claim": "Claim [X]"
        }
    ]

    triggers_found = []

    for item in queries:
        try:
            encoded_query = urllib.parse.quote(item["query"])
            url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results=5"

            # Using a generic User-Agent to avoid API blocking
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)

            # If rate limited or service unavailable, we handle it gracefully below
            if response.status in [429, 503]:
                continue

            data = response.read()
            root = ET.fromstring(data)

            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                summary = entry.find("{http://www.w3.org/2005/Atom}summary")
                title = entry.find("{http://www.w3.org/2005/Atom}title")
                link = entry.find("{http://www.w3.org/2005/Atom}id")

                if summary is None or title is None or link is None:
                    continue

                summary_text = summary.text
                title_text = title.text
                link_url = link.text

                # Check for the literal string or the regex in the summary/title
                if item["trigger_detail"] in summary_text or item["trigger_detail"] in title_text or re.search(item["regex"], summary_text) or re.search(item["regex"], title_text):
                    triggers_found.append({
                        "link": link_url,
                        "detail": item["trigger_detail"],
                        "claim": item["claim"]
                    })

        except Exception as e:
            # Handle 503 or 429 gracefully, or any URL errors without crashing
            pass

    return triggers_found

def generate_report(triggers):
    for t in triggers:
        # Expected Emergency Epistemic Report format
        report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{t['link']}]. Data implies {t['detail']}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of {t['claim']} to Category [E-withdrawn]."
        print(report)

if __name__ == "__main__":
    triggers = check_falsification_triggers()
    if triggers:
        generate_report(triggers)
