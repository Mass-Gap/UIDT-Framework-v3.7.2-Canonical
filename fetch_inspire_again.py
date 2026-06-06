import urllib.request
import json
import time

queries = [
    "Yang-Mills mass gap",
    "spectral gap SU(3)",
    "functional renormalization group",
    "vacuum energy density",
    "lattice QCD gluon propagator",
]

all_papers = []

for q in queries:
    url = f"https://inspirehep.net/api/literature?sort=mostrecent&size=10&page=1&q={urllib.parse.quote(q)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        for hit in data.get('hits', {}).get('hits', []):
            metadata = hit.get('metadata', {})
            title = metadata.get('titles', [{}])[0].get('title', 'Unknown')
            arxiv = next((e['value'] for e in metadata.get('arxiv_eprints', [])), None)
            doi = next((e['value'] for e in metadata.get('dois', [])), None)
            abstract = metadata.get('abstracts', [{}])[0].get('value', '')
            date = metadata.get('preprint_date', '')

            if date and date.startswith(('2024', '2025', '2026')):
                all_papers.append({
                    'title': title,
                    'arxiv': arxiv,
                    'doi': doi,
                    'date': date,
                    'abstract': abstract,
                })
    except Exception as e:
        print(f"Error fetching {q}: {e}")
    time.sleep(1)

unique_papers = {p['title']: p for p in all_papers}.values()
with open('tmp_papers.json', 'w') as f:
    json.dump(list(unique_papers), f)
