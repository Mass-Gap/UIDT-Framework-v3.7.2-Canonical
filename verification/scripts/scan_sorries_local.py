import pathlib, re
d = pathlib.Path(__file__).resolve().parent / "wt-TKT-2026-07-13-lean-f1\verification\antigravit2\src"
files = sorted(d.glob("*.lean"))
tot = 0
for f in files:
    t = f.read_text(encoding="utf-8", errors="ignore")
    s = len(re.findall(r"\bsorry\b", t))
    tot += s
    if s or "native_decide" in t or "by decide" in t:
        print(f.name.replace("verification__antigravit2__src__Antigravit2__", ""),
              "| sorry:", s,
              "| native_decide:", t.count("native_decide"),
              "| by decide:", t.count("by decide"))
print("TOTAL sorry across snapshot:", tot)
print("---target-literal scan (definitions risk)---")
for f in files:
    t = f.read_text(encoding="utf-8", errors="ignore")
    for pat in ("16.339", "1.710", "49/3", "17/3000"):
        if pat in t:
            print("LITERAL", pat, "in", f.name)
