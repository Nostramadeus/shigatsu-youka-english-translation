"""gal_write.py - write a GaleX200 .gal from a PNG, reusing an original .gal as the header template.

Usage (from the project root):
    uv run --no-project --with pylivemaker python tools/images/gal_write.py ORIG.gal NEW.png OUT.gal \
        [--comp keep|jpeg|zip] [--quality N] [--frame 0] [--verify]

Two paths:
  FAST  - the original is unblocked (BlockWidth=0) and --comp keeps its CompType: the XML header is copied byte
          for byte, untouched frames are copied verbatim, only the chosen frame's blobs are rewritten.
  REENC - the original is block-compressed (BlockWidth>0), uses CompType 1 (raw), is an old "Gale106" file, or
          --comp changes the type: every frame is decoded with pylivemaker and re-encoded unblocked (BlockWidth
          and BlockHeight forced to 0, CompType 0 zip or 2 jpeg). Old-format originals get a fresh GaleX200 header.
Limits: one layer per frame (every UI file in this game), Bpp 24 (palette files are refused).

Layout (pylivemaker GalImagePlugin._galx_info/_galx_frames/GalImageDecoder):
    b"GaleX200" + int32 header_size + zlib(xml)
    per frame, per layer:  int32 layer_size + blob
                           CompType 0 -> zlib(raw rows, BGR 24bpp, stride 4-byte aligned)
                           CompType 2 -> a plain JPEG (decoded as RGB)
                           then ONLY IF AlphaOn=1: int32 alpha_size + zlib(8-bit plane, stride 4-byte aligned)
"""
import argparse
import io
import re
import struct
import sys
import zlib

from lxml import etree
from PIL import Image

import livemaker.GalImagePlugin  # noqa: F401  (registers the GAL opener for the REENC path and --verify)


def s32(b, o=0):
    return struct.unpack_from("<i", b, o)[0]


def p32(v):
    return struct.pack("<i", v)


def parse_galx(data):
    hs = s32(data, 8)
    xml = zlib.decompress(data[12:12 + hs])
    root = etree.fromstring(xml, parser=etree.XMLParser(encoding="shift-jis", recover=True))
    p = 12 + hs
    blobs = []  # (frame_idx, layer_elem, layers_elem, layer_blob, alpha_blob_or_None)
    for fi, frame in enumerate(root):
        for layers in frame:
            for layer in layers.iter("Layer"):
                ls = s32(data, p)
                p += 4
                lb = data[p:p + ls]
                p += ls
                # The alpha block is ALWAYS present, even when AlphaOn="0" (it is then usually empty, but
                # some files carry a real plane the engine ignores). Dropping it truncates the file by 4+ bytes
                # and the engine silently refuses the picture - that blanks the whole screen it belongs to.
                ab = None
                if p + 4 <= len(data):
                    as_ = s32(data, p)
                    if 0 <= as_ <= len(data) - p - 4:
                        ab = data[p + 4:p + 4 + as_]
                        p += 4 + as_
                if ab is None and int(layer.get("AlphaOn", 0)):
                    raise SystemExit("alpha plane missing for an AlphaOn=1 layer")
                blobs.append((fi, layer, layers, lb, ab))
    if p != len(data):
        print("warning: %d trailing bytes in the original" % (len(data) - p), file=sys.stderr)
    return xml, root, blobs


def encode_layer(im, comp, quality, level=9):
    w, h = im.size
    if comp == 2:
        buf = io.BytesIO()
        im.convert("RGB").save(buf, "JPEG", quality=quality, subsampling=0)
        return buf.getvalue()
    raw = im.convert("RGB").tobytes("raw", "BGR")
    row = w * 3
    stride = (row + 3) & ~3
    pad = b"\0" * (stride - row)
    rows = b"".join(raw[y * row:(y + 1) * row] + pad for y in range(h))
    return zlib.compress(rows, level)


def encode_alpha(im, level=9):
    w, h = im.size
    a = im.convert("RGBA").getchannel("A").tobytes()
    stride = (w + 3) & ~3
    pad = b"\0" * (stride - w)
    rows = b"".join(a[y * w:(y + 1) * w] + pad for y in range(h))
    return zlib.compress(rows, level)


def decode_frames(path):
    """Every frame of the original as RGBA PIL images (pylivemaker decodes frame by frame)."""
    im = Image.open(path)
    n = getattr(im, "n_frames", 1)
    out = []
    for i in range(n):
        im.seek(i)
        im.load()
        out.append(im.convert("RGBA").copy())
    return out


def fresh_xml(w, h, frames, alpha_on, comp):
    """Minimal GaleX200 header for an old-format original (mirrors the headers this game ships)."""
    fr = "".join(
        '<Frame Name="Frame%d" TransColor="-1" Delay="17" Disposal="2" Count="0" Count="1" L0="0" T0="0" R0="%d" B0="%d">'
        '<Layers Count="1" Width="%d" Height="%d" Bpp="24">'
        '<Layer Left="0" Top="0" Visible="1" TransColor="-1" Alpha="255" AlphaOn="%d" Name="Layer1" Lock="0"/>'
        "</Layers></Frame>" % (i + 1, w, h, w, h, alpha_on) for i in range(frames))
    return ('<Frames Version="200" Width="%d" Height="%d" Bpp="24" Count="%d" SyncPal="1" Randomized="0" '
            'CompType="%d" CompLevel="90" BGColor="16777215" BlockWidth="0" BlockHeight="0" NotFillBG="0">%s</Frames>'
            % (w, h, frames, comp, fr)).encode("shift-jis")


def write_gal(orig_path, png_path, out_path, comp_mode="keep", quality=None, frame=0):
    data = open(orig_path, "rb").read()
    im = Image.open(png_path)
    im.load()
    old_format = data[:8] != b"GaleX200"

    if old_format:
        xml = root = blobs = None
        orig_comp = 0
        blocked = True
        bpp = 24
        comp_level = 90
    else:
        xml, root, blobs = parse_galx(data)
        orig_comp = int(root.get("CompType", 0))
        blocked = int(root.get("BlockWidth", 0)) > 0 or int(root.get("BlockHeight", 0)) > 0
        if int(root.get("Randomized", 0)):
            raise SystemExit("randomized (encrypted) original; not supported")
        bpp = int(root.get("Bpp", 24))
        comp_level = int(root.get("CompLevel", 70))
        if max(len(list(f.iter("Layer"))) for f in root) != 1:
            raise SystemExit("multi-layer frame; not supported")
    if bpp != 24:
        raise SystemExit("Bpp %d original (palette); not supported" % bpp)
    comp = {"keep": orig_comp if orig_comp in (0, 2) else 0, "jpeg": 2, "zip": 0}[comp_mode]
    q = quality if quality is not None else max(comp_level, 85)
    reenc = old_format or blocked or comp != orig_comp or orig_comp not in (0, 2)

    if not reenc:
        new_blobs = []
        replaced = False
        for fi, layer_el, layers_el, lb, ab in blobs:
            if fi == frame:
                lw = int(layers_el.get("Width", root.get("Width")))
                lh = int(layers_el.get("Height", root.get("Height")))
                if im.size != (lw, lh):
                    raise SystemExit("size mismatch: PNG %r vs layer %r" % (im.size, (lw, lh)))
                lb = encode_layer(im, comp, q)
                if int(layer_el.get("AlphaOn", 0)):
                    ab = encode_alpha(im)
                elif im.mode == "RGBA" and im.getextrema()[3][0] < 255:
                    print("warning: PNG has transparency but the original layer has AlphaOn=0; alpha dropped",
                          file=sys.stderr)
                replaced = True
            new_blobs.append((lb, ab if ab is not None else b""))
        if not replaced:
            raise SystemExit("frame %d not found" % frame)
        xml_out = xml
        path_used = "FAST"
    else:
        frames_px = decode_frames(orig_path)
        if frame >= len(frames_px):
            raise SystemExit("frame %d not found (%d frames)" % (frame, len(frames_px)))
        if im.size != frames_px[0].size:
            raise SystemExit("size mismatch: PNG %r vs original %r" % (im.size, frames_px[0].size))
        if old_format:
            alpha_flags = [1 if fp.getextrema()[3][0] < 255 or im.mode == "RGBA" else 0 for fp in frames_px]
            alpha_on = max(alpha_flags)
            xml_out = fresh_xml(im.size[0], im.size[1], len(frames_px), alpha_on, comp)
            alpha_per_frame = [alpha_on] * len(frames_px)
        else:
            xml_out = xml
            xml_out = re.sub(rb'BlockWidth="\d+"', b'BlockWidth="0"', xml_out, count=1)
            xml_out = re.sub(rb'BlockHeight="\d+"', b'BlockHeight="0"', xml_out, count=1)
            xml_out = re.sub(rb'CompType="\d+"', ('CompType="%d"' % comp).encode(), xml_out, count=1)
            alpha_per_frame = [int(layer_el.get("AlphaOn", 0)) for _, layer_el, _, _, _ in blobs]
        new_blobs = []
        for fi, fp in enumerate(frames_px):
            src = im if fi == frame else fp
            lb = encode_layer(src, comp, q)
            ab = encode_alpha(src) if alpha_per_frame[fi] else b""
            new_blobs.append((lb, ab))
        path_used = "REENC(%s)" % ("old-format" if old_format else ("blocked" if blocked else "comp-change"))

    zxml = zlib.compress(xml_out, 9)
    out = bytearray(b"GaleX200" + p32(len(zxml)) + zxml)
    for lb, ab in new_blobs:
        out += p32(len(lb)) + lb
        if ab is not None:
            out += p32(len(ab)) + ab
    open(out_path, "wb").write(out)
    print("wrote %s: %d bytes, %s, CompType=%d, quality=%s, %dx%d, frames=%d, alpha=%s" % (
        out_path, len(out), path_used, comp, q if comp == 2 else "-", im.size[0], im.size[1], len(new_blobs),
        "yes" if new_blobs[frame][1] else "no"))
    return im


def verify(out_path, im, frame=0):
    back = Image.open(out_path)
    back.seek(frame)
    back.load()
    ref = im.convert(back.mode)
    if back.size != ref.size:
        raise SystemExit("verify: size %r != %r" % (back.size, ref.size))
    diffs = []
    for i, name in enumerate(back.getbands()):
        b1 = back.getchannel(i).tobytes()
        b2 = ref.getchannel(i).tobytes()
        total = 0
        mx = 0
        for x, y in zip(b1, b2):
            d = abs(x - y)
            total += d
            if d > mx:
                mx = d
        diffs.append("%s: mean %.2f max %d" % (name, total / len(b1), mx))
    print("verify (re-read with pylivemaker, per channel): " + "; ".join(diffs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orig")
    ap.add_argument("png")
    ap.add_argument("out")
    ap.add_argument("--comp", choices=["keep", "jpeg", "zip"], default="keep")
    ap.add_argument("--quality", type=int, default=None, help="JPEG quality (default: max(CompLevel, 85))")
    ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--verify", action="store_true", help="re-read OUT with pylivemaker and compare to the PNG")
    args = ap.parse_args()
    im = write_gal(args.orig, args.png, args.out, args.comp, args.quality, args.frame)
    if args.verify:
        verify(args.out, im, args.frame)


if __name__ == "__main__":
    main()
