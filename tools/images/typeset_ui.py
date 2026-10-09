"""typeset_ui.py - paint out the Japanese and set English on a UI image, driven by a JSON job file.

Usage (from the project root):
    uv run --no-project --with pillow --with numpy python tools/images/typeset_ui.py JOB.json

JOB.json = {"jobs": [job, job, ...]}, one job per image:
{
  "src":  "work/images/png/グラフィック/タイトル/了承する.png",   # PNG made by gal_to_png.py
  "out":  "work/images/demo/了承する.png",                       # English PNG (same size, keeps alpha)
  "erase": {"mode": "flat", "box": [x0, y0, x1, y1]},            # how the old text is removed (see below)
  "text": [{"string": "I consent", "font": "C:/Windows/Fonts/yumindb.ttf", "size": 0,
            "box": [x0, y0, x1, y1], "color": "#000000", "stroke": 0, "stroke_color": "#ffffff",
            "align": "center", "valign": "middle", "spacing": 0, "line_spacing": 1.1}]
}
erase modes:
  flat  - fill the box with the dominant colour of the box border ring (flat UI: yellow/red bars)
  alpha - make the box fully transparent (text drawn over nothing, e.g. logo strips)
  box   - fill the box with "color" given in erase (explicit colour)
  none  - draw over the original without erasing
  inpaint - mask the lettering by colour (thresh) inside the box and inpaint it (textured backgrounds)
size 0 = auto: the largest size that fits the box (width and height, wrapped on spaces).
font_index = face number inside a .ttc collection (BIZ-UDGothicB.ttc: 0 = fixed pitch, 1 = proportional).
The output must stay the same pixel size as the source (gal_write.py refuses anything else).
"""
import json
import sys
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

# Per-glyph fallback (IMAGES3C 2026-10-01): a glyph the chosen font lacks (Ink Free has no arrows, circled
# numbers or katakana middle dot) is drawn from the first fallback font that has it, at the same size and on the
# same baseline, instead of the font's empty box. Text that the font fully covers renders exactly as before.
FALLBACK_FONTS = ["C:/Windows/Fonts/seguisym.ttf", "C:/Windows/Fonts/ARIALUNI.TTF", "C:/Windows/Fonts/msgothic.ttc"]
SUBST = {"・": "•"}   # katakana middle dot used as a list bullet -> bullet, if the font has one
_HAS, _FB = {}, {}


def has_glyph(font, ch):
    key = (font.path, getattr(font, "index", 0), ch)
    if key not in _HAS:
        f = ImageFont.truetype(font.path, 40, index=getattr(font, "index", 0))
        m, nd = f.getmask(ch), f.getmask("􏿽")
        _HAS[key] = not (m.size == nd.size and bytes(m) == bytes(nd))
    return _HAS[key]


def _fallback(ch, size):
    for fp in FALLBACK_FONTS:
        if (fp, size) not in _FB:
            try:
                _FB[(fp, size)] = ImageFont.truetype(fp, size)
            except OSError:
                _FB[(fp, size)] = None
        fb = _FB[(fp, size)]
        if fb is not None and has_glyph(fb, ch):
            return fb
    return None


def runs(text, font):
    """split text into [segment, font] runs; the main font wherever it has the glyph."""
    out = []
    for ch in text:
        f = font
        if ord(ch) > 127 and not has_glyph(font, ch):
            if ch in SUBST and has_glyph(font, SUBST[ch]):
                ch = SUBST[ch]
            else:
                f = _fallback(ch, font.size) or font
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return out


def tlen(draw, text, font):
    return sum(draw.textlength(s, font=f) for s, f in runs(text, font))


def draw_runs(d, xy, text, font, **kw):
    """d.text with per-glyph fallback; xy = top-left as in d.text's default anchor."""
    x, y = xy
    asc = font.getmetrics()[0]
    for s, f in runs(text, font):
        if f is font:
            d.text((x, y), s, font=f, **kw)
        else:
            d.text((x, y + asc), s, font=f, anchor="ls", **kw)
        x += d.textlength(s, font=f)


def ring_colour(im, box, ring=3):
    x0, y0, x1, y1 = box
    px = im.load()
    c = Counter()
    for x in range(max(0, x0 - ring), min(im.size[0], x1 + ring)):
        for y in list(range(max(0, y0 - ring), y0)) + list(range(y1, min(im.size[1], y1 + ring))):
            c[px[x, y]] += 1
    for y in range(y0, y1):
        for x in list(range(max(0, x0 - ring), x0)) + list(range(x1, min(im.size[0], x1 + ring))):
            c[px[x, y]] += 1
    return c.most_common(1)[0][0]


def erase_inpaint(im, spec):
    """Mask the old lettering by colour and inpaint it away (Telea). Needs numpy + opencv-python-headless.

    spec: box [x0,y0,x1,y1]; thresh [rmin,rmax,gmin,gmax,bmin,bmax] selects the lettering colour inside the box;
    dilate (px, default 2) grows the mask over anti-aliased edges; radius (default 4) is the inpaint radius.
    """
    import numpy as np
    import cv2
    x0, y0, x1, y1 = spec["box"]
    rgba = np.array(im)
    rgb = rgba[:, :, :3].astype(int)
    t = spec.get("thresh", [140, 255, 0, 90, 0, 90])
    sel = ((rgb[:, :, 0] >= t[0]) & (rgb[:, :, 0] <= t[1]) & (rgb[:, :, 1] >= t[2]) & (rgb[:, :, 1] <= t[3])
           & (rgb[:, :, 2] >= t[4]) & (rgb[:, :, 2] <= t[5]))
    mask = np.zeros(rgb.shape[:2], np.uint8)
    mask[y0:y1, x0:x1] = sel[y0:y1, x0:x1].astype(np.uint8) * 255
    k = int(spec.get("dilate", 2))
    if k:
        mask = cv2.dilate(mask, np.ones((2 * k + 1, 2 * k + 1), np.uint8))
    bgr = rgba[:, :, :3][:, :, ::-1].copy()
    out = cv2.inpaint(bgr, mask, int(spec.get("radius", 4)), cv2.INPAINT_TELEA)
    rgba[:, :, :3] = out[:, :, ::-1]
    im.paste(Image.fromarray(rgba, "RGBA"), (0, 0))
    return int((mask > 0).sum())


def erase(im, spec):
    mode = spec.get("mode", "flat")
    box = spec["box"]
    d = ImageDraw.Draw(im)
    if mode == "flat":
        col = ring_colour(im, box)
        d.rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=col)
    elif mode == "alpha":
        d.rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=(0, 0, 0, 0))
    elif mode == "box":
        d.rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=spec["color"])
    elif mode == "inpaint":
        n = erase_inpaint(im, spec)
        print("inpainted %d px" % n)
    elif mode == "none":
        pass
    else:
        raise SystemExit("unknown erase mode %s" % mode)


def wrap(draw, text, font, max_w, spacing):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tlen(draw, t, font) + spacing * max(0, len(t) - 1) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, font_path, box, spacing, line_spacing, size, index=0, max_size=0):
    bw, bh = box[2] - box[0], box[3] - box[1]
    if size:
        font = ImageFont.truetype(font_path, size, index=index)
        return font, wrap(draw, text, font, bw, spacing)
    best = None
    for s in range(6, int(max_size) + 1 if max_size else 200):
        font = ImageFont.truetype(font_path, s, index=index)
        lines = wrap(draw, text, font, bw, spacing)
        ascent, descent = font.getmetrics()
        lh = (ascent + descent) * line_spacing
        widest = max(tlen(draw, l, font) + spacing * max(0, len(l) - 1) for l in lines)
        if widest > bw or lh * len(lines) > bh:
            break
        best = (font, lines)
    if best is None:
        raise SystemExit("text does not fit at any size: %r" % text)
    return best


def draw_text(im, spec):
    box = spec["box"]
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    spacing = spec.get("spacing", 0)
    line_spacing = spec.get("line_spacing", 1.1)
    font, lines = fit(d, spec["string"], spec["font"], box, spacing, line_spacing, spec.get("size", 0),
                      spec.get("font_index", 0), spec.get("max_size", 0))
    ascent, descent = font.getmetrics()
    lh = (ascent + descent) * line_spacing
    total_h = lh * len(lines)
    valign = spec.get("valign", "middle")
    if valign == "top":
        y = box[1]
    elif valign == "bottom":
        y = box[3] - total_h
    else:
        y = box[1] + (box[3] - box[1] - total_h) / 2
    stroke = spec.get("stroke", 0)
    for line in lines:
        w = tlen(d, line, font) + spacing * max(0, len(line) - 1)
        align = spec.get("align", "center")
        if align == "left":
            x = box[0]
        elif align == "right":
            x = box[2] - w
        else:
            x = box[0] + (box[2] - box[0] - w) / 2
        if spacing:
            cx = x
            for ch in line:
                draw_runs(d, (cx, y), ch, font, fill=spec.get("color", "#000000"), stroke_width=stroke,
                          stroke_fill=spec.get("stroke_color", "#ffffff"))
                cx += tlen(d, ch, font) + spacing
        else:
            draw_runs(d, (x, y), line, font, fill=spec.get("color", "#000000"), stroke_width=stroke,
                      stroke_fill=spec.get("stroke_color", "#ffffff"))
        y += lh
    im.alpha_composite(layer)
    return font.size, lines


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    for job in spec["jobs"]:
        im = Image.open(job["src"]).convert("RGBA")
        if "erase" in job:
            erase(im, job["erase"])
        for t in job.get("text", []):
            size, lines = draw_text(im, t)
            print("%s: %r at %dpx, %d line(s)" % (job["out"], t["string"], size, len(lines)))
        im.save(job["out"])
        print("wrote", job["out"], im.size)


if __name__ == "__main__":
    main()
