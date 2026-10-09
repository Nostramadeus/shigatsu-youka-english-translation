"""refbg_preview.py - IMG2: review/images/preview-backgrounds/index.html (stdlib + Pillow for the crops).

Reads work/_img2/out/blocks.json (written by refbg.py) and, per picture: a whole-picture before | after, then per
translated block a before | after crop at 2x (block rect + 12 px margin) and the block table (JP, English, glyph
size in the picture and on the 960x540 screen, legible yes/no, reason when left as texture).
Run: uv run --no-project --python 3.12 --with pillow python tools/images/refbg_preview.py
"""
import html
import json
import os
import re

from PIL import Image

ROOT = "F:/Projects/shigatsu-youka-en/"
SRC = ROOT + "work/images/png/グラフィック/リファレンス/背景/%s.png"
NEW = ROOT + "work/_img2/out/%s.png"
OUTD = ROOT + "review/images/preview-backgrounds/"


def zoom_max(z):
    nums = [float(v) for v in re.findall(r"\d+(?:\.\d+)?", z.split("(")[0])]
    return max(nums) if nums else 1.0


def pair(a, b, box, scale, path):
    x0, y0, x1, y1 = box
    ca, cb = a.crop(box), b.crop(box)
    w, h = int((x1 - x0) * scale), int((y1 - y0) * scale)
    ca, cb = ca.resize((w, h), Image.LANCZOS), cb.resize((w, h), Image.LANCZOS)
    out = Image.new("RGB", (w * 2 + 8, h), (20, 20, 20))
    out.paste(ca.convert("RGB"), (0, 0))
    out.paste(cb.convert("RGB"), (w + 8, 0))
    out.save(path)


def main():
    os.makedirs(OUTD, exist_ok=True)
    table = json.load(open(ROOT + "work/_img2/out/blocks.json", encoding="utf-8"))
    toc, body = [], []
    tot_t = tot_x = 0
    for n in sorted(table):
        pic = table[n]
        a = Image.open(SRC % n)
        changed = pic.get("changed") and os.path.exists(NEW % n)
        b = Image.open(NEW % n) if changed else a
        zmax = zoom_max(pic["zoom"])
        whole = "p%s_whole.png" % n
        sc = min(1.0, 700 / a.width)
        pair(a, b, (0, 0, a.width, a.height), sc, OUTD + whole)
        nt = sum(1 for r in pic["rows"] if r["legible"])
        nx = sum(1 for r in pic["rows"] if not r["legible"])
        tot_t += nt
        tot_x += nx
        toc.append('<li><a href="#p%s">%s.gal</a> - %d translated, %d left as texture%s</li>'
                   % (n, n, nt, nx, "" if pic["rows"] else " (no text)"))
        body.append('<section id="p%s"><h2>%s.gal <small>%dx%d, cinema zoom %s</small></h2>'
                    % (n, n, pic["size"][0], pic["size"][1], html.escape(pic["zoom"])))
        body.append('<p class="st">%s</p>' % ("changed: English set" if changed else "unchanged (not shipped)"))
        body.append('<figure><img src="%s" alt=""><figcaption>before | after (whole picture, %d%%)</figcaption></figure>'
                    % (whole, round(sc * 100)))
        if pic["rows"]:
            body.append("<table><tr><th>block</th><th>Japanese</th><th>English</th><th>glyph px (picture / screen at %sx)</th>"
                        "<th>legible</th></tr>" % zmax)
            for r in pic["rows"]:
                body.append("<tr class='%s'><td>%s</td><td class='jp'>%s</td><td>%s</td><td>%s / %s</td><td>%s</td></tr>" % (
                    "ok" if r["legible"] else "tx", html.escape(r["id"]), html.escape(r["jp"]),
                    html.escape(r["en"]) if r["legible"] else "<i>left as texture: %s</i>" % html.escape(r.get("why", "")),
                    r["glyph"] or "-", round(r["glyph"] * zmax) if r["glyph"] else "-", "yes" if r["legible"] else "no"))
            body.append("</table>")
        for r in pic["rows"]:
            if not r["legible"] or not changed:
                continue
            x0, y0, x1, y1 = r["rect"]
            m = 12
            box = (max(0, x0 - m), max(0, y0 - m), min(a.width, x1 + m), min(a.height, y1 + m))
            sc2 = 2.0 if (box[2] - box[0]) <= 560 else 1100 / (box[2] - box[0]) * 1.0
            fn = "b_%s.png" % r["id"]
            pair(a, b, box, sc2, OUTD + fn)
            body.append('<figure class="blk"><img src="%s" alt=""><figcaption>%s - before | after at %sx</figcaption></figure>'
                        % (fn, html.escape(r["id"]), "2" if sc2 == 2.0 else "%.2f" % sc2))
        body.append("</section>")
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Reference-list backgrounds - before / after</title>
<style>
body{font:15px/1.5 "Segoe UI",sans-serif;background:#111;color:#ddd;margin:0;padding:24px 32px;max-width:1500px}
h1{font-size:22px}h2{font-size:18px;margin-top:40px;border-top:1px solid #333;padding-top:16px}small{color:#999;font-weight:normal}
a{color:#8cf}table{border-collapse:collapse;margin:12px 0;width:100%%}td,th{border:1px solid #333;padding:4px 8px;vertical-align:top;text-align:left}
th{background:#222}.jp{font-family:"Yu Mincho","MS PMincho",serif}tr.tx td{color:#999}.st{color:#9c9}
figure{margin:12px 0}figcaption{color:#999;font-size:13px}img{max-width:100%%;display:block}
.bright img{filter:brightness(2.6) contrast(1.1)}button{background:#333;color:#ddd;border:1px solid #555;padding:6px 12px;cursor:pointer}
</style></head><body>
<h1>Reference-list backgrounds (グラフィック\\リファレンス\\背景) - before | after</h1>
<p>The References list plays the cinema リファレンス背景.lcm behind the grid; it pans over these 7 pictures at 0.75x-3.5x.
Legible blocks got English; the rest stay as texture. Totals: %d blocks translated, %d left as texture.
Pictures are dark in the game too; the button brightens the images on this page only.</p>
<p><button onclick="document.body.classList.toggle('bright')">brighten images</button></p>
<ul>%s</ul>
%s
</body></html>""" % (tot_t, tot_x, "\n".join(toc), "\n".join(body))
    open(OUTD + "index.html", "w", encoding="utf-8").write(page)
    print("wrote", OUTD + "index.html", "translated", tot_t, "texture", tot_x)


if __name__ == "__main__":
    main()
