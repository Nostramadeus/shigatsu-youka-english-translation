"""Map every scene .lsb to the image files it references (paths ending .gal/.lcm/.png/.jpg/.bmp).

Covers both command arguments (ImgNew, Cinema, ...) and the LiveNovel text blocks (TextIns bodies, where the
scene tags {CREATECG ...} {CHANGECG ...} live), decompiled with pylivemaker's LNSDecompiler.

Run (one process for all 461 files, a few minutes):
    PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/images/scene_images.py orig notes/_db/_image-usage.tsv
Output TSV: lsb_id, image_path, count. Also prints per-folder totals. Agents-only file.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.command import CommandType
from livemaker.lsb.novel import LNSDecompiler

root = Path(sys.argv[1])
out = Path(sys.argv[2])
pat = re.compile(r'"([^"]+?\.(?:gal|lcm|png|jpg|bmp))"', re.IGNORECASE)

rows = []
per_lsb = {}
dec = LNSDecompiler()
for p in sorted(root.glob("*.lsb")):
    try:
        lsb = LMScript.from_file(str(p))
    except Exception as e:
        print("skip", p.name, e, file=sys.stderr)
        continue
    c = Counter()
    for cmd in lsb.commands:
        texts = []
        try:
            texts.append(str(cmd))
        except Exception:
            pass
        if cmd.type == CommandType.TextIns:
            try:
                texts.append(dec.decompile(cmd.get("Text")))
            except Exception as e:
                print("textins fail", p.name, cmd.LineNo, e, file=sys.stderr)
        for s in texts:
            for m in pat.findall(s):
                c[m] += 1
    per_lsb[p.stem] = c
    for k, v in c.items():
        rows.append((p.stem, k, v))

out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write("lsb\timage\tcount\n")
    for lsb_id, k, v in rows:
        f.write("%s\t%s\t%d\n" % (lsb_id, k, v))

folders = defaultdict(set)
for lsb_id, k, v in rows:
    parts = k.split("\\")
    folders["\\".join(parts[:2])].add(k)
print("lsb files:", len(per_lsb), "distinct images:", len({k for _, k, _ in rows}))
for k in sorted(folders, key=lambda x: -len(folders[x])):
    print("%6d  %s" % (len(folders[k]), k))
