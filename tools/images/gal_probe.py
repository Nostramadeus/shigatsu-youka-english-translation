"""Print the header fields of one or more .gal files (LiveMaker/GraphicsGale format, version >102 layout).

Run: uv run --no-project --with pylivemaker python tools/images/gal_probe.py FILE [FILE...]
Fields follow pylivemaker's GalImagePlugin._gal_info / _gal_frames; unknown bytes are printed as hex so an
encoder can copy them verbatim.
"""
import struct
import sys
import zlib


def u32(b, o=0):
    return struct.unpack_from("<I", b, o)[0]


def s32(b, o=0):
    return struct.unpack_from("<i", b, o)[0]


def probe(path):
    with open(path, "rb") as f:
        data = f.read()
    magic = data[:4]
    if magic == b"Gale" and data[4:5] == b"X":
        print(f"{path}: GaleX (XML header) — not handled here")
        return
    if magic != b"Gale":
        print(f"{path}: not a GAL ({magic!r})")
        return
    version = int(data[4:7])
    hs = s32(data, 7)
    h = data[11:11 + hs]
    out = {
        "version": version,
        "header_size": hs,
        "hdr[0:4]": h[0:4].hex(),
        "width": u32(h, 4),
        "height": u32(h, 8),
        "bpp": s32(h, 0xC),
        "frame_count": s32(h, 0x10),
        "hdr[0x14]": h[0x14:0x15].hex(),
        "randomized": h[0x15],
        "compression": h[0x16],
        "hdr[0x17]": h[0x17:0x18].hex(),
        "bg_color": hex(u32(h, 0x18)),
        "block_w": s32(h, 0x1C),
        "block_h": s32(h, 0x20),
        "hdr[0x24:]": h[0x24:].hex(),
    }
    p = 11 + hs
    # first frame
    nl = u32(data, p); p += 4
    fname = data[p:p + nl].decode("cp932", "replace"); p += nl
    mask = u32(data, p); p += 4
    nine = data[p:p + 9]; p += 9
    layer_count = s32(data, p); p += 4
    fw = s32(data, p); fh = s32(data, p + 4); fbpp = s32(data, p + 8); p += 12
    out.update({"frame_name": fname, "mask": hex(mask), "frame_9bytes": nine.hex(), "layer_count": layer_count,
                "frame_w": fw, "frame_h": fh, "frame_bpp": fbpp})
    if fbpp <= 8:
        p += (1 << fbpp) * 4
    layers = []
    for j in range(layer_count):
        left = s32(data, p); top = s32(data, p + 4); p += 8
        visible = data[p]; p += 1
        trans = s32(data, p); alpha = s32(data, p + 4); p += 8
        alpha_on = data[p]; p += 1
        nl = u32(data, p); p += 4
        lname = data[p:p + nl].decode("cp932", "replace"); p += nl
        lock = None
        if version >= 107:
            lock = data[p]; p += 1
        lsize = s32(data, p); p += 4
        layer_blob = data[p:p + lsize]; p += lsize
        asize = s32(data, p); p += 4
        alpha_blob = data[p:p + asize]; p += asize
        info = {"left": left, "top": top, "visible": visible, "trans": hex(trans & 0xffffffff), "alpha": alpha,
                "alpha_on": alpha_on, "name": lname, "lock": lock, "layer_size": lsize, "alpha_size": asize}
        if out["compression"] == 0:
            try:
                info["layer_unpacked"] = len(zlib.decompress(layer_blob))
            except Exception as e:
                info["layer_unpacked"] = f"zlib fail {e}"
            if asize:
                try:
                    info["alpha_unpacked"] = len(zlib.decompress(alpha_blob))
                except Exception as e:
                    info["alpha_unpacked"] = f"zlib fail {e}"
        layers.append(info)
    out["layers"] = layers
    out["bytes_after_frame1"] = len(data) - p
    out["file_size"] = len(data)
    print(path)
    for k, v in out.items():
        print(f"  {k}: {v}")


for a in sys.argv[1:]:
    probe(a)
