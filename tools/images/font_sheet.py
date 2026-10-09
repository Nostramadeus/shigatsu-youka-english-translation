"""font_sheet.py - the font sheet for the owner: candidate installed Latin fonts set on the demo samples.

Run (project root):
    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --with pillow --with numpy --with opencv-python-headless python tools/images/font_sheet.py
Writes review/images/FONTS.html (self-contained, every image embedded as a data URI),
work/images/fonts-preview.png (grid of all candidates) and work/images/fonts-jp-preview.png (the JP usage crops),
both for a quick agent Read.
Samples are exactly the demo ones: the two notice buttons ("I consent" / "I do not consent") and the reading line
"SHIGATSU YOUKA" over the wallpaper logo crop. Only the font changes between candidates.
Each style row also carries a strip of cropped JAPANESE originals showing where that lettering style is used, taken
only from the earliest screens (boot notices, title menu, first navigator view, in-scene chrome, scene end) and
cropped to UI labels: no scene art, no story text.
"""
import base64
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
import typeset_ui as T  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
F = "C:/Windows/Fonts/"
G = "work/images/png/グラフィック/"

# owner picks so far (label per style); None = still open
PICKS = {"Heavy gothic": "C", "Serif": None, "Rounded": None, "Handwriting": None, "Brush": None}

STYLES = [
    ("Heavy gothic", "notice-gate buttons, the Watch / Skip prompt buttons in scenes, save-screen labels", "", [
        ("A", "Segoe UI Black", "seguibl.ttf", 0),
        ("B", "Arial Black", "ariblk.ttf", 0),
        ("C", "HGP Soei Kaku Gothic UB (the Japanese family the original buttons use)", "HGRSGU.TTC", 1),
        ("D", "BIZ UDPGothic Bold", "BIZ-UDGothicB.ttc", 1),
    ]),
    ("Serif", "scenario-navigator buttons, encyclopedia and reference banners and filters", "", [
        ("A", "Georgia Bold", "georgiab.ttf", 0),
        ("B", "Cambria Bold", "cambriab.ttf", 0),
        ("C", "Times New Roman Bold", "timesbd.ttf", 0),
        ("D", "BIZ UDPMincho Medium (the Japanese mincho family)", "BIZ-UDMinchoM.ttc", 1),
    ]),
    ("Rounded", "the engine option menu, the scene-end buttons (their coloured outline is added at typesetting time and is not shown here)", "", [
        ("A", "Arial Rounded MT Bold", "ARLRDBD.TTF", 0),
        ("B", "HG Maru Gothic M-PRO (the Japanese rounded family)", "HGRSMP.TTF", 0),
        ("C", "Segoe UI Semibold", "seguisb.ttf", 0),
        ("D", "Century Gothic Bold", "GOTHICB.TTF", 0),
    ]),
    ("Handwriting", "document-mode buttons and tags", "", [
        ("A", "Segoe Print Bold", "segoeprb.ttf", 0),
        ("B", "Ink Free", "Inkfree.ttf", 0),
        ("C", "Yasashisa Antique (Japanese handwriting family)", "07YasashisaAntique.ttf", 0),
        ("D", "Comic Sans MS Bold", "comicbd.ttf", 0),
    ]),
    ("Brush", "title-menu buttons, the content-warning words, logos",
     "NO INSTALLED CANDIDATE. Nothing on this machine has the Japanese brush-stroke look. The four below are the "
     "nearest installed script and rough fonts, shown only so the row is not empty. A real brush look needs a font "
     "download (free brush fonts under the SIL Open Font License exist) or a Clip Studio hand pass by the owner.", [
        ("A", "Brush Script MT (a cursive script, not a brush)", "BRUSHSCI.TTF", 0),
        ("B", "Mistral (marker script)", "MISTRAL.TTF", 0),
        ("C", "TrashHand (rough handwriting)", "TrashHand.TTF", 0),
        ("D", "Chiller (rough display face)", "CHILLER.TTF", 0),
    ]),
]

# Where each style is used: (caption, [source PNGs to show side by side]). Earliest screens only, UI labels only.
USED = {
    "Heavy gothic": [
        ("notice gate at boot (in-game crop)", ["work/images/jp-notice-buttons.png"]),
        ("reference prompt inside a scene", [G + "システム/リファレンス見る.png", G + "システム/リファレンス見ない.png"]),
        ("pull-out menu bar inside a scene", [G + "システム/メニューバー.png"]),
    ],
    "Serif": [
        ("scenario navigator, first view", [G + "シナリオナビ/このシナリオを開始.png"]),
        ("scenario navigator", [G + "シナリオナビ/最初から.png", G + "シナリオナビ/分岐直前から.png"]),
        ("scenario navigator", [G + "シナリオナビ/確認.png", G + "シナリオナビ/キャンセル.png"]),
    ],
    "Rounded": [
        ("end of a scene", [G + "システム/シナリオ終わり/終わりシナリオの続きへ.png", G + "システム/シナリオ終わり/終わりシナリオナビへ.png"]),
        ("end of a scene", [G + "システム/シナリオ終わり/終わりあらすじ.png", G + "システム/シナリオ終わり/終わりリファレンスへ.png"]),
        ("engine option menu", [G + "インターフェース/システムメニュー/オプション.png", G + "インターフェース/システムメニュー/セーブ.png", G + "インターフェース/システムメニュー/ロード.png"]),
    ],
    "Handwriting": [
        ("document mode (from the title menu)", [G + "ドキュメント/はい.png", G + "ドキュメント/いいえ.png"]),
        ("document mode", [G + "ドキュメント/キャンセル.png", G + "ドキュメント/メモタグ.png"]),
        ("document mode, header", [G + "ドキュメント/タイトル.png"]),
    ],
    "Brush": [
        ("title menu", [G + "タイトル/開始.png"]),
        ("title menu", [G + "タイトル/中断.png"]),
        ("content-warning screen at boot (one word)", [G + "タイトル/残酷/暴力.png"]),
    ],
}

CSS = (
    "body{font-family:Segoe UI,Arial,sans-serif;background:#f4f4f4;color:#222;margin:0;padding:24px 32px}"
    "h1{font-size:1.5em;margin:0 0 6px}h2{font-size:1.2em;margin:34px 0 4px}p{max-width:960px;line-height:1.45}"
    "table{border-collapse:collapse;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.15);margin-top:8px}"
    "th,td{border:1px solid #ddd;padding:8px 12px;vertical-align:middle;text-align:center}th{background:#e9e9e9;font-weight:600}"
    "td.k{font-size:1.6em;font-weight:700;width:2em}td.n{text-align:left;min-width:14em}small{color:#666}"
    "tr.pick td{background:#e6f4ea}tr.pick td.k{color:#0a7a2a}"
    ".warn{background:#fff3cd;border:1px solid #e0c36a;padding:8px 12px;max-width:960px}"
    "table.jp td{background:#343434;color:#ddd;padding:6px 10px}table.jp td small{color:#bbb}"
    "img{background:repeating-conic-gradient(#ccc 0 25%,#eee 0 50%) 0 0/16px 16px}table.jp img{background:#343434}"
)


def b64(im, fmt):
    buf = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(buf, "JPEG", quality=88)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def img(uri, w, h):
    return '<img src="%s" width="%d" height="%d">' % (uri, w, h)


def compose(paths, gap=8, pad=6, bg=(52, 52, 52, 255)):
    """Side-by-side strip of the given images at 1:1, on a dark background (many originals are transparent)."""
    ims = [Image.open(p).convert("RGBA") for p in paths]
    w = sum(i.size[0] for i in ims) + gap * (len(ims) - 1) + 2 * pad
    h = max(i.size[1] for i in ims) + 2 * pad
    out = Image.new("RGBA", (w, h), bg)
    x = pad
    for i in ims:
        out.alpha_composite(i, (x, pad + (h - 2 * pad - i.size[1]) // 2))
        x += i.size[0] + gap
    return out.convert("RGB")


def bases():
    acc = Image.open(G + "タイトル/了承する.png").convert("RGBA")
    T.erase(acc, {"mode": "flat", "box": [6, 8, 144, 59]})
    dec = Image.open(G + "タイトル/了承しない.png").convert("RGBA")
    T.erase(dec, {"mode": "flat", "box": [6, 8, 144, 59]})
    wall = Image.open(G + "システム/壁紙.png").convert("RGBA")
    T.erase(wall, {"mode": "inpaint", "box": [430, 28, 900, 59], "thresh": [140, 255, 0, 90, 0, 90],
                   "dilate": 2, "radius": 4})
    return acc, dec, wall


def render(acc0, dec0, wall0, font, index):
    acc = acc0.copy()
    s1, _ = T.draw_text(acc, {"string": "I consent", "font": font, "font_index": index, "size": 0,
                              "box": [10, 12, 140, 55], "color": "#000000", "align": "center", "valign": "middle"})
    dec = dec0.copy()
    s2, l2 = T.draw_text(dec, {"string": "I do not consent", "font": font, "font_index": index, "size": 0,
                               "box": [10, 10, 140, 57], "color": "#000000", "align": "center", "valign": "middle",
                               "line_spacing": 1.0})
    wall = wall0.copy()
    s3, _ = T.draw_text(wall, {"string": "SHIGATSU YOUKA", "font": font, "font_index": index, "size": 0,
                               "box": [445, 31, 885, 58], "color": "#e40000", "stroke": 1, "stroke_color": "#7a0000",
                               "align": "center", "valign": "middle", "spacing": 8})
    return acc, dec, wall.crop((400, 20, 940, 150)), (s1, s2, len(l2), s3)


def answer_line():
    parts = []
    for style, _, _, _ in STYLES:
        key = style.lower()
        pick = PICKS.get(style)
        if pick:
            parts.append("%s = %s" % (key, pick))
        elif style == "Brush":
            parts.append("%s = _ (or: download)" % key)
        else:
            parts.append("%s = _" % key)
    return ", ".join(parts)


def main():
    acc0, dec0, wall0 = bases()
    orig_acc = Image.open("review/images/demo/before-accept.png")
    orig_dec = Image.open("review/images/demo/before-decline.png")
    orig_line = Image.open("review/images/demo/before-reading-line.png")
    h = []
    h.append('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
             "<title>Font sheet: candidate Latin fonts for the picture text</title><style>" + CSS + "</style></head><body>")
    h.append("<h1>Font sheet: candidate Latin fonts for the picture text</h1>")
    h.append("<p>Each style below covers a group of pictures in the game. Above each style table, a dark strip shows "
             "cropped Japanese originals of that lettering style, from the earliest screens only (boot notices, title "
             "menu, first navigator view, in-scene chrome, scene end), so the match can be judged. Every candidate is "
             "then set on the same three samples from the demo, at the real in-game pixel size: the two notice buttons "
             "(150 x 67) and the reading line above the title logo (a 540 x 130 crop of the notice-screen wallpaper). "
             "Only the font changes between rows; the type size is the largest that fits the box, so a font that comes "
             "out small is a font whose letters are wide.</p>")
    h.append("<p><b>How to answer:</b> one letter per style. Your pick so far is filled in; the blanks are still open: "
             "<code>%s</code>. A style you do not care about can be left to me.</p>" % answer_line())
    h.append("<h2>Reference: the Japanese originals of the three samples</h2><table><tr><th>accept</th><th>decline</th><th>reading line</th></tr><tr>"
             "<td>" + img(b64(orig_acc, "PNG"), 150, 67) + "</td><td>" + img(b64(orig_dec, "PNG"), 150, 67) + "</td>"
             "<td>" + img(b64(orig_line, "JPEG"), 540, 130) + "</td></tr></table>")
    rows_preview = []
    jp_preview = []
    for style, used_for, note, cands in STYLES:
        pick = PICKS.get(style)
        h.append("<h2>%s%s</h2><p><small>Used for: %s.</small></p>" % (style, (" (your pick: %s)" % pick) if pick else "", used_for))
        if note:
            h.append('<p class="warn">%s</p>' % note)
        strip = USED.get(style, [])
        if strip:
            h.append("<p><small>Where it is used (Japanese originals, cropped to the label):</small></p>"
                     '<table class="jp"><tr>')
            for caption, paths in strip:
                im = compose(paths)
                jp_preview.append((style + ": " + caption, im))
                h.append("<td>" + img(b64(im, "PNG"), im.size[0], im.size[1]) + "<br><small>%s</small></td>" % caption)
            h.append("</tr></table>")
        h.append("<table><tr><th></th><th>font</th><th>accept</th><th>decline</th><th>reading line</th></tr>")
        for label, name, fname, index in cands:
            path = F + fname
            if not os.path.exists(path):
                h.append('<tr><td class="k">%s</td><td class="n">%s<br><small>%s: NOT INSTALLED</small></td>'
                         '<td colspan="3">-</td></tr>' % (label, name, fname))
                continue
            acc, dec, line, sizes = render(acc0, dec0, wall0, path, index)
            face = (" face %d" % index) if index else ""
            plural = "" if sizes[2] == 1 else "s"
            is_pick = (pick == label)
            h.append('<tr%s><td class="k">%s%s</td><td class="n">%s<br><small>%s%s; sizes %d / %d px (%d line%s) / %d px</small></td>'
                     % (' class="pick"' if is_pick else "", label, "<br><small>your pick</small>" if is_pick else "",
                        name, fname, face, sizes[0], sizes[1], sizes[2], plural, sizes[3])
                     + "<td>" + img(b64(acc, "PNG"), 150, 67) + "</td><td>" + img(b64(dec, "PNG"), 150, 67) + "</td>"
                     + "<td>" + img(b64(line, "JPEG"), 540, 130) + "</td></tr>")
            rows_preview.append(("%s %s: %s" % (style, label, name), acc, dec, line))
            print("%-14s %s %-62s sizes %s" % (style, label, name, sizes))
        h.append("</table>")
    h.append("<p><small>Rendered by tools/images/font_sheet.py from the demo job files; the chosen fonts are then "
             "used by the batch typesetter.</small></p></body></html>")
    out = "review/images/FONTS.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(h))
    print("wrote %s: %d bytes" % (out, os.path.getsize(out)))

    try:
        lf = ImageFont.truetype(F + "segoeui.ttf", 13)
    except Exception:
        lf = ImageFont.load_default()
    rh = 136
    grid = Image.new("RGB", (880, rh * len(rows_preview)), (50, 50, 50))
    d = ImageDraw.Draw(grid)
    for i, (lab, acc, dec, line) in enumerate(rows_preview):
        y = i * rh
        d.text((4, y + 2), lab, fill=(255, 255, 0), font=lf)
        grid.paste(acc.convert("RGB"), (4, y + 20))
        grid.paste(dec.convert("RGB"), (164, y + 20))
        grid.paste(line.convert("RGB"), (330, y + 3))
    grid.save("work/images/fonts-preview.png")
    print("wrote work/images/fonts-preview.png", grid.size)

    y = 0
    wmax = max(im.size[0] for _, im in jp_preview) + 8
    hsum = sum(im.size[1] + 22 for _, im in jp_preview)
    jp = Image.new("RGB", (wmax, hsum), (30, 30, 30))
    d = ImageDraw.Draw(jp)
    for lab, im in jp_preview:
        d.text((4, y + 2), lab, fill=(255, 255, 0), font=lf)
        jp.paste(im, (4, y + 18))
        y += im.size[1] + 22
    jp.save("work/images/fonts-jp-preview.png")
    print("wrote work/images/fonts-jp-preview.png", jp.size)


if __name__ == "__main__":
    main()
