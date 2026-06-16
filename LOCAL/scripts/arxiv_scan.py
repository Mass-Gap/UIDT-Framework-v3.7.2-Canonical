#!/usr/bin/env python3
"""
ArXiv Literature & Falsification Radar
Target Agent: Jules
Execution: Weekly (Monday 06:00 UTC)
Scope: ArXiv Monitor (Rule 4.1) & CoVe Data Parsing (Rule 4.2)
"""

import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import re
import sys

# Rule 4.1 Queries
QUERIES = [
    "Lattice QCD glueball spectrum continuum limit",
    "DESI dark energy equation of state",
    "Casimir effect anomaly precision measurement"
]

def build_arxiv_url(query, max_results=5):
    encoded_query = urllib.parse.quote(f'"{query}"')
    return f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

def fetch_papers(query):
    url = build_arxiv_url(query)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'UIDT-ArXiv-Radar/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        if e.code in [503, 429]:
            # Handle rate limiting / unavailability gracefully
            print(f"ArXiv API unavailable (HTTP {e.code}). Skipping query: {query}")
        else:
            print(f"HTTP Error {e.code} for query {query}")
        return None
    except Exception as e:
        print(f"Error fetching data for query {query}: {e}")
        return None

def analyze_summary(summary, query, paper_id):
    summary = summary.replace('\n', ' ')

    # Trigger #3: DESI w = -1.00 ± 0.01
    # Check for DESI query and regex for w = -1.00 ± 0.01
    # Be robust to spaces
    if "DESI" in query:
        w_pattern = re.compile(r'w\s*(?:=|≈|\\approx)\s*-1\.00\s*(?:\+/-|\\pm|±)\s*0\.01')
        if w_pattern.search(summary):
            trigger_opus(paper_id, "w = -1.00 ± 0.01", "Claim [X]")

    # Trigger #1: Lattice QCD confirms mass gap != 1.710 GeV at >3σ
    if "Lattice" in query:
        # We look for something that implies mass gap != 1.710 GeV at >3σ
        # A simple check: if we see ">3\sigma" or "> 3 \sigma" or ">3 sigma"
        # and a value different from 1.710 or directly stating tension.
        # But per the exact rule: "IF Lattice QCD confirms mass gap != 1.710 GeV at >3σ"
        # Let's use a regex looking for exclusion of 1.710
        gap_pattern = re.compile(r'(?:mass gap|spectral gap).*?(?:!=|\\neq|excludes).*?1\.710.*?(?:>3\\sigma|>3\s*sigma|> 3\\sigma|>3\s*σ)', re.IGNORECASE)

        # Alternatively, capture any mass gap value and see if it's explicitly tension
        if gap_pattern.search(summary) or ("1.710" in summary and ("exclude" in summary.lower() or "tension" in summary.lower() or ">3" in summary)):
             trigger_opus(paper_id, "Lattice QCD confirms mass gap != 1.710 GeV at >3σ", "Claim [X]")

def trigger_opus(paper_id, trigger_detail, claim_id):
    report = f"> 🚨 **FALSIFICATION TRIGGER DETECTED:** ArXiv scan identified paper [{paper_id}]. Data implies {trigger_detail}. This challenges the holographic scale factor mechanism. Requesting immediate Opus 4.7 evaluation for potential downgrade of {claim_id} to Category [E-withdrawn]."
    print(report)

def main():
    for query in QUERIES:
        data = fetch_papers(query)
        if data:
            try:
                root = ET.fromstring(data)
                # arXiv namespace
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('atom:entry', ns)
                for entry in entries:
                    id_element = entry.find('atom:id', ns)
                    summary_element = entry.find('atom:summary', ns)
                    if id_element is not None and summary_element is not None:
                        paper_id = id_element.text.split('/abs/')[-1]
                        summary = summary_element.text
                        analyze_summary(summary, query, paper_id)
            except ET.ParseError as e:
                print(f"Error parsing XML for query {query}: {e}")

if __name__ == "__main__":
    main()
