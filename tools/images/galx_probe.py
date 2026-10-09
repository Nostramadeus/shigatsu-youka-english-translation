"""Print the XML header and blob layout of GaleX200 .gal files.

Run: uv run --no-project --with pylivemaker python tools/images/galx_probe.py FILE [FILE...]
Layout (pylivemaker GalImagePlugin._galx_info/_galx_frames): "GaleX200", int32 header_size, zlib(XML),
then per frame per layer: int32 layer_size + blob, and ONLY if AlphaOn: int32 alpha_size + blob.
"""
import struct
import sys
import zlib

from lxml import etree


def s32(b, o=0):
    return struct.unpack_from("<i", b, o)[0]


for path in sys.argv[1:]:
    data = open(path, "rb").read()
    if data[:8] != b"GaleX200":
        print(f"{path}: not GaleX200 ({data[:8]!r})")
        continue
    hs = s32(data, 8)
    xml = zlib.decompress(data[12:12 + hs])
    root = etree.fromstring(xml, parser=etree.XMLParser(encoding="shift-jis", recover=True))
    print(f"== {path}  file={len(data)}  header_size={hs}  xml_len={len(xml)}")
    print("  " + etree.tostring(root, encoding="unicode").replace("\n", "\n  ")[:1500])
    p = 12 + hs
    comp = int(root.get("CompType", 0))
    bw, bh = int(root.get("BlockWidth", 0)), int(root.get("BlockHeight", 0))
    for fi, frame in enumerate(root):
        for layers in frame:
            for li, layer in enumerate(layers.iter("Layer")):
                ls = s32(data, p); p += 4
                blob = data[p:p + ls]; p += ls
                line = f"  frame{fi} layer{li}: layer_size={ls}"
                if comp == 0:
                    try:
                        raw = zlib.decompress(blob)
                        line += f" unpacked={len(raw)}"
                        if bw > 0 and bh > 0:
                            w = int(layers.get("Width", root.get("Width")))
                            h = int(layers.get("Height", root.get("Height")))
                            nb = ((w + bw - 1) // bw) * ((h + bh - 1) // bh)
                            refs = [(s32(raw, i * 8), s32(raw, i * 8 + 4)) for i in range(nb)]
                            kinds = {}
                            for fr, lr in refs:
                                k = "raw" if fr == -1 else ("self" if fr == -2 else "other")
                                kinds[k] = kinds.get(k, 0) + 1
                            line += f" blocks={nb} refs={kinds} first_refs={refs[:4]}"
                    except Exception as e:
                        line += f" zlib-fail={e}"
                elif comp == 2:
                    line += f" jpeg magic={blob[:3].hex()}"
                if int(layer.get("AlphaOn", 0)):
                    as_ = s32(data, p); p += 4
                    ablob = data[p:p + as_]; p += as_
                    line += f" | alpha_size={as_}"
                    try:
                        araw = zlib.decompress(ablob)
                        line += f" alpha_unpacked={len(araw)}"
                    except Exception as e:
                        line += f" alpha-zlib-fail={e}"
                print(line)
    print(f"  bytes_after={len(data) - p}")
