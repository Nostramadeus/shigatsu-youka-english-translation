"""compare_gal.py - structural diff of an original .gal against the shipped replacement.

Usage: compare_gal.py REL_PATH [REL_PATH ...]   (paths relative to グラフィック/, forward slashes)
Prints size, header XML, frame names, Bpp/alpha/layers and the trailing-byte count for both files.
"""
import struct
import sys
import zlib

ORIG = "work/images/gal/グラフィック/"
NEW = "work/グラフィック/"


def read(p):
    d = open(p, "rb").read()
    assert d[:8] == b"GaleX200", (p, d[:8])
    hsz = struct.unpack("<I", d[8:12])[0]
    xml = zlib.decompress(d[12:12 + hsz]).decode("cp932", "replace")
    off = 12 + hsz
    blobs = []
    while off + 4 <= len(d):
        n = struct.unpack("<I", d[off:off + 4])[0]
        if n == 0 or off + 4 + n > len(d):
            break
        blobs.append(n)
        off += 4 + n
    return {"size": len(d), "hsz": hsz, "xml": xml, "blobs": blobs, "tail": len(d) - off,
            "tailbytes": d[off:off + 8].hex()}


def brief(x):
    import re
    f = re.search(r"<Frames ([^>]*)>", x["xml"]).group(1)
    keep = dict(re.findall(r'(\w+)="([^"]*)"', f))
    names = re.findall(r'<Frame Name="([^"]*)"', x["xml"])
    lay = re.findall(r'<Layer [^>]*AlphaOn="(\d)"[^>]*Name="([^"]*)"', x["xml"])
    return ("size=%-8d hsz=%-4d blobs=%s tail=%d(%s) | W=%s H=%s Bpp=%s Count=%s CompType=%s CompLevel=%s "
            "Block=%sx%s Rand=%s | frames=%s | layers=%s" % (
                x["size"], x["hsz"], x["blobs"], x["tail"], x["tailbytes"], keep.get("Width"), keep.get("Height"),
                keep.get("Bpp"), keep.get("Count"), keep.get("CompType"), keep.get("CompLevel"),
                keep.get("BlockWidth"), keep.get("BlockHeight"), keep.get("Randomized"), names, lay))


for rel in sys.argv[1:]:
    try:
        a = read(ORIG + rel)
    except Exception as e:
        print("== %s\n   ORIG MISSING/ERR %s" % (rel, e))
        continue
    print("== %s" % rel)
    print("   orig %s" % brief(a))
    try:
        b = read(NEW + rel)
    except FileNotFoundError:
        print("   new  NOT SHIPPED")
        continue
    print("   new  %s" % brief(b))
    flags = []
    if a["xml"] != b["xml"]:
        flags.append("XML DIFFERS")
    if len(a["blobs"]) != len(b["blobs"]):
        flags.append("BLOB COUNT %d -> %d" % (len(a["blobs"]), len(b["blobs"])))
    if a["tail"] != b["tail"]:
        flags.append("TRAILING BYTES %d -> %d" % (a["tail"], b["tail"]))
    print("   %s" % ("; ".join(flags) if flags else "structurally identical"))
