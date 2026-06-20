import json

with open('tmp_papers.json', 'r') as f:
    papers = json.load(f)

keywords_critical = ["Yang-Mills mass gap", "spectral gap SU(3)", "gluon mass dynamical", "functional renormalization group", "FRG gluon", "LPA prime", "BMW scheme", "Δ = 1.7", "1.71", "string tension SU(3)", "confinement mass gap"]
keywords_important = ["vacuum energy density", "dark energy equation of state", "lattice QCD gluon propagator", "Landau gauge propagator", "Schwinger mechanism", "IR fixed point", "Kugo-Ojima"]
keywords_monitor = ["holographic Yang-Mills", "AdS/QCD confinement", "1/Nc expansion gauge theory", "large N limit"]

print(f"Total: {len(papers)}")

for p in papers:
    text = (p['title'] + " " + p['abstract']).lower()

    critical = [k for k in keywords_critical if k.lower() in text]
    important = [k for k in keywords_important if k.lower() in text]
    monitor = [k for k in keywords_monitor if k.lower() in text]

    if critical or important or monitor:
        print(f"\nTitle: {p['title']}")
        print(f"ArXiv: {p['arxiv']}")
        print(f"Abstract: {p['abstract']}")
        if critical: print(f"CRITICAL: {critical}")
        if important: print(f"IMPORTANT: {important}")
        if monitor: print(f"MONITOR: {monitor}")
