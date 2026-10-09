"""Resolve 選択シナリオ -> target scene .lsb across 000015E3.lsb and 0000001C.lsb."""
import io, re, json
from pathlib import Path

D = Path("tools/harness/work/dumps")

def load(name):
    out = {}
    for raw in io.open(D / name, encoding="utf-8"):
        m = re.match(r"^(\s*)(\d+):(.*)$", raw.rstrip("\n"))
        if m:
            out.setdefault(int(m.group(2)), []).append((len(m.group(1)), m.group(3)))
    return out

FILES = {"000015E3.lsb": load("000015E3.txt"), "0000001C.lsb": load("0000001C.txt")}

def txt(f, n):
    return " ".join(t for _, t in FILES[f].get(n, []))

PC = re.compile(r"PCReset.*?Page = u'([^']+)'.*?Label = (\d+)")
JMP = re.compile(r"Jump ([0-9A-F]{8})\.lsb:0")
SELF = re.compile(r"Jump (000015E3|0000001C)\.lsb:(\d+) 1\s*$")

def resolve(f, label, seen=None, depth=0):
    if depth > 6:
        return None, "depth"
    seen = seen or set()
    if (f, label) in seen:
        return None, "loop"
    seen.add((f, label))
    for n in range(label, label + 40):
        t = txt(f, n)
        if not t.strip():
            continue
        m = JMP.search(t)
        if m:
            return m.group(1), "%s:%d" % (f, n)
        m = PC.search(t)
        if m:
            return resolve(m.group(1), int(m.group(2)), seen, depth + 1)
        m = SELF.search(t.strip())
        if m:
            return resolve(m.group(1) + ".lsb", int(m.group(2)), seen, depth + 1)
    return None, "no-jump"

chain = {}
for f in FILES:
    tbl = FILES[f]
    for n in sorted(tbl):
        for indent, t in tbl[n]:
            m = re.match(r"^(?:If|Elseif) 選択シナリオ == (\d+)\s*$", t.strip())
            if not m:
                continue
            num = int(m.group(1))
            nxt = txt(f, n + 1)
            p = PC.search(nxt)
            if p:
                lsb, via = resolve(p.group(1), int(p.group(2)))
                if lsb:
                    chain.setdefault(num, []).append({"lsb": lsb, "from": "%s:%d" % (f, n), "via": via})

print("scenarios resolved:", len(chain))
print("195 ->", chain.get(195))
print("who maps to 000004A7:", [k for k, v in chain.items() if any(x["lsb"] == "000004A7" for x in v)])
print("who maps to 00000024:", [k for k, v in chain.items() if any(x["lsb"] == "00000024" for x in v)])
json.dump(chain, io.open("tools/harness/work/nav_chain.json", "w", encoding="utf-8"), ensure_ascii=False)
