"""scan_tail.py - every shipped picture vs its original: structural check (size, frames, layers, alpha block)."""
import os
import re
import struct
import zlib

ORIG = "work/images/gal/"
NEW = "work/"


def parse(p):
    d = open(p, "rb").read()
    if d[:8] != b"GaleX200":
        return None
    hs = struct.unpack("<I", d[8:12])[0]
    xml = zlib.decompress(d[12:12 + hs]).decode("cp932", "replace")
    fr = re.search(r"<Frames ([^>]*)>", xml).group(1)
    at = dict(re.findall(r'(\w+)="([^"]*)"', fr))
    names = re.findall(r'<Frame Name="([^"]*)"', xml)
    alphas = [int(a) for a in re.findall(r'<Layer [^>]*AlphaOn="(\d)"', xml)]
    off = 12 + hs
    blocks = []
    for _ in alphas:
        sz = struct.unpack("<I", d[off:off + 4])[0]
        off += 4 + sz
        asz = struct.unpack("<I", d[off:off + 4])[0]
        off += 4 + asz
        blocks.append((sz, asz))
    return {"wh": (at.get("Width"), at.get("Height")), "bpp": at.get("Bpp"), "count": at.get("Count"),
            "names": names, "alphas": alphas, "layers": len(alphas), "tail": len(d) - off, "size": len(d)}


bad = []
old = []
noorig = []
n = 0
for root, _, names in os.walk(NEW + "グラフィック"):
    for f in names:
        if not f.endswith(".gal"):
            continue
        rel = os.path.relpath(os.path.join(root, f), NEW).replace("\\", "/")
        o, b = ORIG + rel, os.path.join(root, f)
        if not os.path.exists(o):
            noorig.append(rel)   # shipped by another lane; its original was never extracted here
            continue
        n += 1
        A, B = parse(o), parse(b)
        if A is None:
            old.append(rel)   # old Gale10x original: rebuilt with a fresh GaleX200 header, nothing to compare
            continue
        if B is None:
            bad.append((rel, "replacement is not GaleX200"))
            continue
        for k in ("wh", "bpp", "count", "names", "alphas", "layers"):
            if A[k] != B[k]:
                bad.append((rel, "%s %r -> %r" % (k, A[k], B[k])))
        if B["tail"] != 0:
            bad.append((rel, "replacement has %d leftover bytes" % B["tail"]))
        if A["tail"] != 0:
            bad.append((rel, "ORIGINAL has %d leftover bytes (parser incomplete)" % A["tail"]))
print("shipped pictures checked: %d (of which %d had an old Gale10x original: header rebuilt)" % (n, len(old)))
print("not comparable (no original extracted here): %d %s" % (len(noorig), noorig))
print("MISMATCHES: %d" % len(bad))
for rel, m in bad[:20]:
    print("   %-72s %s" % (rel, m))
