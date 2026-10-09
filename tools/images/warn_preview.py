"""warn_preview.py - review/images/preview-warnings/index.html: original | first pass | fixed, per warning word,
with the sampled colours beside each row. No story content: single words and the composite only (agents+owner:
the words ARE the content warnings, so this page is agents-only by the same rule as the inventory)."""
import html
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = "work/images/png/グラフィック/タイトル/残酷/"
BEFORE = "work/images/warn-before/"
AFTER = "work/images/out/グラフィック/タイトル/残酷/"
OUT = "review/images/preview-warnings/"
WORDS = ["児童惨殺", "薬物", "触手", "死体", "カニバリズム", "殺人", "虫", "いじめ", "死姦", "監禁", "血",
         "暴力", "人体実験", "内臓", "人体欠損", "怪異", "下ネタ", "脅かし", "残酷"]
os.makedirs(OUT, exist_ok=True)
font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)


def mean_visible(im):
    a = np.array(im.convert("RGBA"))
    rgb, al = a[:, :, :3], a[:, :, 3]
    vis = (al > 0) & (rgb.astype(int).sum(axis=2) > 60)
    return rgb[vis].mean(axis=0) if vis.sum() else np.zeros(3)


rows = []
for w in WORDS:
    ims = []
    for base in (SRC, BEFORE, AFTER):
        p = base + w + ".png"
        ims.append(Image.open(p).convert("RGBA") if os.path.exists(p) else None)
    labels = [t for t, i in zip(("original", "first pass", "fixed"), ims) if i is not None]
    ims = [i for i in ims if i is not None]
    if len(ims) < 2:   # work/images/warn-before/ is scratch: without it the page is original | fixed
        continue
    scale = 1.0 if ims[0].size[0] <= 500 else 500.0 / ims[0].size[0]
    ims = [i.resize((int(i.size[0] * scale), int(i.size[1] * scale)), Image.LANCZOS) if scale < 1 else i for i in ims]
    gap, lab = 14, 18
    cw = max(i.size[0] for i in ims)
    ch = max(i.size[1] for i in ims)
    canvas = Image.new("RGB", (cw * len(ims) + gap * (len(ims) + 1), ch + lab + 8), (18, 18, 18))
    d = ImageDraw.Draw(canvas)
    for k, (i, t) in enumerate(zip(ims, labels)):
        x = gap + k * (cw + gap)
        canvas.paste(i.convert("RGB"), (x, lab), i)
        d.text((x, 2), t, fill=(120, 220, 255), font=font)
    name = "%02d-%s.png" % (WORDS.index(w), w)
    canvas.save(OUT + name)
    means = [(t, mean_visible(Image.open(b + w + ".png")))
             for t, b in (("original", SRC), ("first pass", BEFORE), ("fixed", AFTER))
             if os.path.exists(b + w + ".png")]
    rows.append((w, name, means))

with open(OUT + "index.html", "w", encoding="utf-8") as f:
    f.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>content-warning words: colour fix</title>'
            '<style>body{background:#161616;color:#ddd;font-family:Segoe UI,sans-serif;padding:18px;max-width:1200px}'
            'h1{font-size:20px}img{display:block;margin:6px 0 4px;max-width:100%}'
            'table{border-collapse:collapse;margin:4px 0 26px;font-size:13px}td,th{padding:3px 10px;text-align:left}'
            'th{color:#9cf}.sw{display:inline-block;width:13px;height:13px;vertical-align:-2px;margin-right:6px;'
            'border:1px solid #555}</style></head><body>')
    f.write("<h1>Content-warning words: text colour taken from the original</h1>"
            "<p>The first pass let the analyser pick the colour and added a 1&nbsp;px white stroke, which washed "
            "every word out and turned the pink one red. The colour is now sampled from each original "
            "(tools/images/warn_colors.py) and set with no stroke. Numbers are the mean colour of the visible "
            "pixels.</p>")
    for w, name, means in rows:
        f.write("<h3>%s</h3><img src=\"%s\">" % (html.escape(w), name))
        f.write("<table><tr><th></th><th>mean R,G,B</th></tr>")
        for lbl, m in means:
            f.write("<tr><td>%s</td><td><span class=sw style=\"background:rgb(%d,%d,%d)\"></span>%d, %d, %d</td></tr>"
                    % (lbl, m[0], m[1], m[2], m[0], m[1], m[2]))
        f.write("</table>")
    f.write("</body></html>")
print("wrote %s%s (%d rows)" % (OUT, "index.html", len(rows)))
