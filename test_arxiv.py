import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

queries = [
    "all:\"Lattice QCD glueball spectrum continuum limit\"",
    "all:\"DESI dark energy equation of state\"",
    "all:\"Casimir effect anomaly precision measurement\""
]

for q in queries:
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&max_results=5'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                print(f"QUERY: {q}\nTitle: {title}\nSummary: {summary}\n---\n")
    except Exception as e:
        print(f"Error for {q}: {e}")
