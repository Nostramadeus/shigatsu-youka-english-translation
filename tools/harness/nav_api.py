"""Resolve 選択シナリオ -> scene .lsb. THE ADDRESSING RULE, verified 2026-09-25:

    LabelReference.Label is a 0-BASED INDEX into the page's command list
    (LMScript.commands, in file order). It is NOT a LineNo and NOT a label id.

Proof: every probe of `PCReset Page=<f> Label=<n>` lands on cmds[n] == a `Label` command,
followed by `Call <self>:1` (変数削除) and then `Jump <scene>.lsb:0` - the triplet the
engine uses for every scene entry. e.g. 000015E3 idx 16 -> Label/Call/Jump 000001DB;
idx 1815 -> Label(LineNo 2045)/Call/Jump 00002450; 0000001C idx 2928 -> Jump 000013B5.

Why LineNo does not work: LineNo is not unique. WhileInit/While/WhileLoop all carry the
same LineNo, so LineNo and index coincide early in a file and drift apart later
(000015E3: 2182 commands, max LineNo 2408).
"""
import json, re
from livemaker.lsb import LMScript
from livemaker.project import PylmProject

pylm = PylmProject("000000F2.lsb")
CACHE = {}

def page(name):
    if name not in CACHE:
        CACHE[name] = LMScript.from_file(name, call_name=pylm.call_name(name), pylm=pylm).commands
    return CACHE[name]

def ref_of(c):
    try:
        r = c.get("Page")
    except Exception:
        return None
    return r if r is not None and hasattr(r, "Page") else None

def resolve(fname, idx, seen=None, depth=0):
    if depth > 8:
        return None, "depth"
    seen = seen or set()
    if (fname, idx) in seen:
        return None, "loop"
    seen.add((fname, idx))
    try:
        cmds = page(fname)
    except Exception as e:
        return None, "load-fail:%s" % e
    for j in range(idx, min(idx + 12, len(cmds))):
        c = cmds[j]
        if j > idx and c.type.name == "Label":
            return None, "block-end@%d" % j
        if c.type.name not in ("Jump", "PCReset"):
            continue          # Call returns; it must not be followed
        r = ref_of(c)
        if r is None or not isinstance(r.Label, int):
            continue
        tgt = str(r.Page)
        if tgt.lower() != fname.lower():
            if r.Label == 0 and c.type.name == "Jump":
                return tgt[:-4] if tgt.lower().endswith(".lsb") else tgt, "%s[%d]" % (fname, j)
            return resolve(tgt, r.Label, seen, depth + 1)
        if r.Label != j:
            return resolve(fname, r.Label, seen, depth + 1)
    return None, "fell-off"

chain = {}
for fname in ("000015E3.lsb", "0000001C.lsb"):
    cmds = page(fname)
    for i, c in enumerate(cmds):
        if c.type.name not in ("If", "Elseif"):
            continue
        try:
            calc = str(c.get("Calc")).strip()
        except Exception:
            continue
        m = re.search(r"選択シナリオ == (\d+)", calc)
        if not m:
            continue
        num = int(m.group(1))
        if i + 1 >= len(cmds):
            continue
        r = ref_of(cmds[i + 1])
        if r is None or not isinstance(r.Label, int):
            continue
        lsb, via = resolve(str(r.Page), r.Label)
        chain.setdefault(num, []).append(
            {"lsb": lsb, "via": via, "cond": calc, "from": "%s[%d]" % (fname, i)})

ok = {k: v for k, v in chain.items() if any(x["lsb"] for x in v)}
tg = {}
for k, v in ok.items():
    for x in v:
        if x["lsb"]:
            tg.setdefault(x["lsb"], set()).add(k)
print("entries with a condition:", len(chain), "| resolved:", len(ok))
print("distinct scene files:", len(tg), "| claimed by >1 entry:", sum(1 for v in tg.values() if len(v) > 1))
for n in (195, 85, 99, 13, 1):
    print(" ", n, "->", [(x["lsb"], x["via"]) for x in chain.get(n, [])])
json.dump(chain, open("../tools/harness/work/nav_chain.json", "w", encoding="utf-8"), ensure_ascii=False)
