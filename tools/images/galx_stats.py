"""Walk a folder of .gal files and tabulate the GaleX header properties that matter for re-encoding.

Usage: uv run --no-project --with pylivemaker python tools/images/galx_stats.py DIR [--list-blocked]
Columns: CompType (0 zip / 2 jpeg), Bpp, BlockWidth>0, frame count, max layers per frame, AlphaOn, Randomized.
"""
import os
import struct
import sys
import zlib
from collections import Counter

from lxml import etree


def s32(b, o=0):
    return struct.unpack_from("<i", b, o)[0]


root_dir = sys.argv[1]
list_blocked = "--list-blocked" in sys.argv
c = Counter()
blocked = []
total = 0
old = 0
for root, _, names in os.walk(root_dir):
    for n in names:
        if not n.lower().endswith(".gal"):
            continue
        total += 1
        p = os.path.join(root, n)
        with open(p, "rb") as f:
            head = f.read(12)
            if head[:8] != b"GaleX200":
                old += 1
                c[("old-format", head[:7].decode("latin1", "replace"))] += 1
                continue
            hs = s32(head, 8)
            xml = zlib.decompress(f.read(hs))
        r = etree.fromstring(xml, parser=etree.XMLParser(encoding="shift-jis", recover=True))
        frames = len(r)
        layers = max((len(list(fr.iter("Layer"))) for fr in r), default=0)
        alpha = max((int(l.get("AlphaOn", 0)) for l in r.iter("Layer")), default=0)
        key = ("comp%s" % r.get("CompType"), "bpp%s" % r.get("Bpp"),
               "block" if int(r.get("BlockWidth", 0)) > 0 else "noblock",
               "frames=%s" % ("1" if frames == 1 else ("2-4" if frames <= 4 else "5+")),
               "layers=%d" % layers, "alpha%d" % alpha, "rnd%s" % r.get("Randomized"))
        c[key] += 1
        if int(r.get("BlockWidth", 0)) > 0:
            blocked.append((os.path.relpath(p, root_dir), r.get("BlockWidth"), r.get("BlockHeight"), frames, layers))
print("files: %d (old GAL format: %d)" % (total, old))
for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
    print("%6d  %s" % (v, " ".join(k)))
if list_blocked:
    for row in blocked:
        print("blocked: %s  bw=%s bh=%s frames=%d layers=%d" % row)
