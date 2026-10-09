"""Scan every LSB for writes to the per-scenario state variables st<N>.

0000001C.lsb reads st<連番> for each navigator record (LineNo 3953,
`AssignTemp("st" ++ DBGetStr("連番"))`), so these writes are the unlock graph.
"""
import re, sys
from pathlib import Path
from livemaker.lsb import LMScript

pat = re.compile(r"\bst(\d+)\s*=\s*([0-9]+)")
root = Path("orig")
hits = []
for p in sorted(root.rglob("*.lsb")):
    try:
        lsb = LMScript.from_file(str(p))
    except Exception:
        continue
    for cmd in lsb.commands:
        try:
            s = str(cmd)
        except Exception:
            continue
        if "st" not in s:
            continue
        for m in pat.finditer(s):
            hits.append((p.as_posix(), cmd.LineNo, cmd.type.name, m.group(1), m.group(2), s[:90].replace("\n", " ")))
print("total st<N> writes:", len(hits))
for h in hits:
    print("\t".join(str(x) for x in h))
