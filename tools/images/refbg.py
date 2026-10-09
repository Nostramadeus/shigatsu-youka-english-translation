"""refbg.py - IMG2: English for the reference-list background collage (グラフィック\\リファレンス\\背景\\0-6.gal).

The References list screen plays the cinema リファレンス背景.lcm behind the grid: it pans over seven pictures at
0.75x-3.5x (0.gal 2x, 5.gal 2.75-3x). Mouse run 1 caught two strings (F29 366.png, F30 381-383.png); FIX1-Q2 and the
owner ruling: set small English over every block that can be read at game size, leave the rest as texture.

Usage (project root):
    uv run --no-project --python 3.12 --with pillow --with numpy --with opencv-python-headless python tools/images/refbg.py [--only 0,5] [--no-encode]
Then (separate process, needs pylivemaker): gal_write.py ORIG.gal work/_img2/out/N.png work/グラフィック/リファレンス/背景/N.gal --comp keep --verify

Writes: work/_img2/out/<n>.png (the English picture, RGBA, original alpha kept), work/_img2/out/blocks.json (block
table for the preview), the preview page via tools/images/refbg_preview.py.

Per block: rect = the erase box (text + paper only, table rules stay outside it), kind = para | line | stack | rot |
texture (texture = left in Japanese on purpose, with the reason), erase = paper | black | tile.
Ink = the median of the dark pixels inside the rect (paper blocks) or of the light pixels (the black banner),
hatched with the picture's diagonal print hatch (period 7 px, '/' direction) and softened 0.5 px like the scan.
Font: Cambria (batch.py's serif = the newspaper class; owner pick 2026-09-26).
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = "F:/Projects/shigatsu-youka-en/"
SRC = ROOT + "work/images/png/グラフィック/リファレンス/背景/%s.png"
OUT = ROOT + "work/_img2/out/"
FONT = "C:/Windows/Fonts/cambria.ttc"
FONT_B = "C:/Windows/Fonts/cambriab.ttf"

P0_TIER1 = ("Shortly after 5 a.m. on April 8, the brutally murdered body of a man was found in Chuo Park. "
            "The victim was Ryoji Kogori (42), a resident of Motoki-cho. He was found by a man who was setting "
            "up a food stall for the 70th Motoki Cherry Blossom Festival.")
P0_TIER2 = ("The day before the incident, Mr. Kogori had told his family he was leaving on a business trip, and "
            "he had been missing since that night. His body was found with the skin stripped from head to toe. "
            "He was reportedly still breathing when he was found.")
P0_LOWER = [
    "At around 9 p.m. the same day, Erina Goto (15), a local resident, was found murdered by an unknown "
    "assailant near Jogaoka Nursery School. The cause of death was a crushed brain from a violent blow to the "
    "head. Then, at around 11 p.m., Akane Kogori (42) and Natsumi Kogori (16), who lived nearby, were also "
    "found murdered in their home.",
    "Ryoji Kogori, found early in the morning, and Akane and Natsumi, killed that night, were one family, and "
    "it is believed that someone targeted the Kogori family. Police stated that Ms. Goto, who was also killed, "
    "was close to the Kogoris and had been caught up in some kind of trouble.",
    "Mifuyu Niimura (42) and Haruka Niimura (17), also residents of the town and believed to be connected to "
    "the case, are missing. Police are investigating a link to the Chuo Park incident on the morning of April 8.",
]

PICS = {
    "0": dict(
        zoom="2x (cinema record 0.gal, measured on run-1 366.png)",
        paper_patch=(100, 240, 640, 282),
        # table rules the erase boxes cross, redrawn afterwards: (x0, x1, y, rgb) per row, sampled from 0.png
        rules=[(705, 968, 456, (35, 39, 23)), (705, 968, 457, (26, 30, 13))],
        blocks=[
            dict(id="0-masthead-strip", jp="元　木　日　報", rect=(495, 14, 840, 50), glyph=22, kind="line",
                 en="T H E   M O T O K I   D A I L Y", size=17, erase="paper"),
            dict(id="0-date", jp="紀耀800年 4月9日 木曜日", rect=(940, 14, 1195, 50), glyph=20, kind="line",
                 en="Thursday, April 9, Shiyo 800", size=15, erase="paper"),
            dict(id="0-issue", jp="12561号", rect=(1210, 14, 1300, 50), glyph=20, kind="line",
                 en="No. 12561", size=15, erase="paper"),
            dict(id="0-headline", jp="元木町内で4名惨殺", rect=(40, 72, 1104, 218), glyph=95, kind="line",
                 en="4 Slaughtered in Motoki-cho", size=92, erase="black"),
            dict(id="0-nameplate", jp="元木日報 (vertical nameplate)", rect=(1150, 80, 1281, 510), glyph=80,
                 kind="stack", en=["THE", "MOTOKI", "DAILY"], sizes=[40, 48, 48], erase="diag", bold=True, spread=True, hatch=0.12),
            dict(id="0-publisher", jp="発行所 / 元木雑誌社 / 佐波県元木町城ケ丘1-1 / 郵便番号 909-0028 / ©元木雑誌社 紀耀800年 / 電話 128(991)XXXX",
                 rect=(1132, 520, 1298, 648), glyph=16, kind="stack",
                 en=["Publisher", "Motoki Magazine Co.", "1-1 Jogaoka, Motoki-cho,", "Sawa Pref.  Postal code 909-0028",
                     "© Motoki Magazine Co., Shiyo 800", "Tel. 128(991)XXXX"],
                 sizes=[12, 17, 12, 12, 12, 12], erase="paper", bold_lines=[1]),
            dict(id="0-ad", jp="プログラミング / 不要のゲーム / 開発ツール", rect=(1132, 658, 1298, 740), glyph=22,
                 kind="stack", en=["A game creation", "tool that needs", "no programming"], sizes=[19, 19, 19],
                 erase="paper", italic=True),
            dict(id="0-ad-logo", jp="LiveMaker / www.livemaker.net/", rect=(1132, 742, 1298, 800), glyph=22,
                 kind="texture", why="already Latin (tool logo + URL)"),
            dict(id="0-subhead-1", jp="女ケ沢市事件再来か", rect=(1028, 262, 1104, 834), glyph=58, kind="rot",
                 en="Megasawa City Murders Again?", size=52, erase="paper"),
            dict(id="0-subhead-2", jp="四月八日の惨劇は止められない?", rect=(982, 312, 1028, 756), glyph=30,
                 kind="rot", en="Is the April 8 Carnage Unstoppable?", size=28, erase="paper"),
            dict(id="0-article-1", jp="四月八日午前五時過ぎ、中央公園にて男性の惨殺された遺体が発見された。被害者は元木町内在住の古郡良治さん(42)で、第70回元木桜祭りの屋台準備をしていた男性によって発見された。",
                 rect=(700, 266, 976, 460), glyph=22, kind="para", en=[P0_TIER1], size=17, erase="paper"),
            dict(id="0-article-2", jp="事件前日古郡さんは、家族に出張に行くと言い、前日の夜から行方が分からなくなっていた。古郡さんの遺体は全身の皮が剥された状態で発見され、発見当時にはまだ息があったという。",
                 rect=(700, 458, 976, 648), glyph=22, kind="para", en=[P0_TIER2], size=17, erase="paper"),
            dict(id="0-caption", jp="最初の惨殺遺体が発見された中央公園(午前7時30撮影)", rect=(108, 614, 652, 648), glyph=20,
                 kind="line", en="Chuo Park, where the first slaughtered body was found (photographed at 7:30 a.m.)",
                 size=17, erase="paper"),
            dict(id="0-article-3", jp="また同日午後9時頃、城ケ丘保育園付近で、町内に住む五島絵梨奈さん(15)が何者かによって殺害されているのが発見された。死因は頭部強打による脳挫滅。そして午後11時頃、付近に住む古郡茜さん(42)、古郡なつみさん(16)も自宅で殺害されているのが発見された。／なお、早朝に発見された古郡良治さんと夜間に殺害された茜さん、なつみさんは家族であり、何者かが古郡さん一家を狙って犯行に及んだと見られている。同じく殺害された五島さんは、古郡さんとも親交があり、何らかのトラブルに巻き込まれたとの見解を警察は発表。／事件に関係していると思われる同じく町内在住の新村美冬さん(42)、新村春花さん(17)は行方不明となっており、警察では四月八日午前に発生した中央公園との関連性を調べている。",
                 rect=(40, 656, 968, 846), glyph=22, kind="para", en=P0_LOWER, size=17, erase="paper"),
            dict(id="0-photo", jp="(photo, no text)", rect=(95, 290, 660, 608), glyph=0, kind="texture",
                 why="photograph, no lettering"),
        ]),
    "1": dict(zoom="1-2x", blocks=[
        dict(id="1-page", jp="(whole page, ~60 lines of smeared handwriting-style text)", rect=(0, 0, 480, 1363), glyph=9,
             kind="texture", why="the lettering is smeared on purpose; at 1-2x only isolated characters survive, no line reads"),
    ]),
    "2": dict(zoom="1-2x", blocks=[
        dict(id="2-page", jp="(whole page, text in steep 3D perspective)", rect=(0, 0, 1899, 540), glyph=30, kind="texture",
             why="glyphs are smeared blots in perspective; no character can be read"),
    ]),
    "3": dict(zoom="1-3.5x", blocks=[
        dict(id="3-board", jp="(handwritten memo board, ~30 lines: 課題 / ①… / ②女ケ沢事件との関連 …)", rect=(0, 0, 1237, 864), glyph=18,
             kind="texture", why="faint embossed pencil on a dark vignette; even with contrast stretched only a few words "
                                   "can be made out, and none at game brightness"),
    ]),
    "4": dict(zoom="0.75-2x", blocks=[]),
    "5": dict(
        zoom="2.75-3x (cinema record 5.gal, measured on run-1 382.png)",
        paper_patch=(1000, 150, 1400, 380),
        blocks=[
            dict(id="5-masthead", jp="女　ケ　沢　新　聞", rect=(225, 26, 815, 100), glyph=50, kind="line",
                 en="THE  MEGASAWA  NEWSPAPER", size=48, erase="paper", bold=True),
            dict(id="5-date", jp="紀耀790年 4月9日", rect=(1088, 32, 1408, 92), glyph=32, kind="line",
                 en="April 9, Shiyo 790", size=34, erase="paper"),
            dict(id="5-weekday", jp="金曜日", rect=(1440, 32, 1570, 92), glyph=32, kind="line",
                 en="Friday", size=34, erase="paper"),
            dict(id="5-caption", jp="殺害された久慈浩二君(左)、畑中ここなちゃん(右)", rect=(170, 408, 992, 462), glyph=34,
                 kind="line", en="Murdered: Koji Kuji (left) and Kokona Hatanaka (right)", size=34, erase="paper"),
            dict(id="5-body-heads", jp="にたし捜魔た堂に 会畑通女連発が町過 (column heads cut by the bottom edge)",
                 rect=(95, 496, 960, 541), glyph=30, kind="texture",
                 why="only the first character of each vertical column is in the picture; no word can be translated"),
            dict(id="5-headline-cut", jp="小 / (two more cut glyphs, right)", rect=(1240, 385, 1612, 541), glyph=120,
                 kind="texture", why="fragments of a vertical headline cut by the picture edge"),
        ]),
    "6": dict(zoom="0.75-2.75x", blocks=[]),
}


def font(size, bold=False, italic=False):
    if bold:
        return ImageFont.truetype(FONT_B, size)
    if italic:
        return ImageFont.truetype("C:/Windows/Fonts/cambriai.ttf", size)
    return ImageFont.truetype(FONT, size, index=0)


def lum(a):
    return a[..., :3].mean(-1)


def paper_level(rgb, rect, pct=85, tile=24):
    x0, y0, x1, y1 = rect
    reg = rgb[y0:y1, x0:x1]
    h, w = reg.shape[:2]
    ny, nx = max(1, h // tile), max(1, w // tile)
    lv = np.zeros((ny, nx, 3))
    L = lum(reg)
    for j in range(ny):
        for i in range(nx):
            ys, ye = j * h // ny, (j + 1) * h // ny
            xs, xe = i * w // nx, (i + 1) * w // nx
            blk = reg[ys:ye, xs:xe].reshape(-1, 3)
            lb = L[ys:ye, xs:xe].reshape(-1)
            thr = np.percentile(lb, pct - 20)
            sel = blk[lb >= thr]
            lv[j, i] = np.median(sel, axis=0)
    img = Image.fromarray(np.clip(lv, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return np.asarray(img).astype(float)


def texture_hp(rgb, patch, shape):
    x0, y0, x1, y1 = patch
    p = rgb[y0:y1, x0:x1].astype(float)
    blur = np.asarray(Image.fromarray(p.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(float)
    hp = p - blur
    h, w = shape
    ph, pw = hp.shape[:2]
    out = np.zeros((h, w, 3))
    for y in range(0, h, ph):
        for x in range(0, w, pw):
            t = hp
            if (y // ph) % 2:
                t = t[::-1]
            if (x // pw) % 2:
                t = t[:, ::-1]
            out[y:y + ph, x:x + pw] = t[:h - y, :w - x]
    return out


def feather(shape, f=3):
    h, w = shape
    m = np.ones((h, w))
    for k in range(f):
        v = (k + 1) / (f + 1)
        m[k, :] = np.minimum(m[k, :], v); m[h - 1 - k, :] = np.minimum(m[h - 1 - k, :], v)
        m[:, k] = np.minimum(m[:, k], v); m[:, w - 1 - k] = np.minimum(m[:, w - 1 - k], v)
    return m[..., None]


def erase(rgb, blk, pic):
    x0, y0, x1, y1 = blk["rect"]
    h, w = y1 - y0, x1 - x0
    reg = rgb[y0:y1, x0:x1].astype(float)
    if blk["erase"] == "paper":
        fill = paper_level(rgb, blk["rect"]) + texture_hp(rgb, pic["paper_patch"], (h, w))
    elif blk["erase"] == "black":
        L = lum(reg)
        base = np.median(reg[L < 12].reshape(-1, 3), axis=0)
        noise = np.random.default_rng(1).normal(0, 0.7, (h, w, 1))
        fill = base[None, None, :] + noise
    elif blk["erase"] == "diag":
        # the nameplate hatch is invariant along the '/' direction (x+1, y-1): refill every glyph pixel from the
        # nearest clean pixel along that line, so the hatch continues through the erased strokes
        L = lum(reg)
        bg = np.median(L)
        m = L < bg - 18
        import cv2
        m = cv2.dilate(m.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        fill = reg.copy()
        for y in range(h):
            for x in range(w):
                if not m[y, x]:
                    continue
                for k in range(1, max(h, w)):
                    for sx, sy in ((x + k, y - k), (x - k, y + k)):
                        if 0 <= sx < w and 0 <= sy < h and not m[sy, sx]:
                            fill[y, x] = reg[sy, sx]
                            break
                    else:
                        continue
                    break
        # keep the refilled strokes at the plate's own mean brightness
        clean = reg[~m].mean(0)
        fill[m] = fill[m] - fill[m].mean(0) + clean
    elif blk["erase"] == "tile":
        strips = [rgb[b:d, a:c].astype(float) for (a, b, c, d) in blk["tile_src"]]
        fill = np.zeros((h, w, 3))
        rng = np.random.default_rng(7)
        x = 0
        k = 0
        while x < w:
            s = strips[k % len(strips)]
            sw = s.shape[1]
            off = int(rng.integers(0, 60))
            s = np.roll(s, off, axis=0)[:h]
            if s.shape[0] < h:
                s = np.concatenate([s, s[::-1]], 0)[:h]
            fill[:, x:x + sw] = s[:, :w - x]
            x += sw
            k += 1
    else:
        return
    m = feather((h, w), 3)
    rgb[y0:y1, x0:x1] = reg * (1 - m) + fill * m


def ink_colour(orig, blk):
    x0, y0, x1, y1 = blk["rect"]
    reg = orig[y0:y1, x0:x1].astype(float)
    L = lum(reg)
    if blk["erase"] == "black":
        sel = reg[L > np.percentile(L, 97)]
    else:
        sel = reg[L < np.percentile(L, 4)]
    return np.median(sel.reshape(-1, 3), axis=0)


SS = 4  # supersampling


def text_mask_line(txt, f, pad=4):
    tmp = Image.new("L", (1, 1))
    d = ImageDraw.Draw(tmp)
    l, t, r, b = d.textbbox((0, 0), txt, font=f)
    im = Image.new("L", (r - l + 2 * pad, b - t + 2 * pad), 0)
    ImageDraw.Draw(im).text((pad - l, pad - t), txt, font=f, fill=255)
    return im


def render_mask(blk, rect_wh):
    """Return an L mask (rect size) with the English set per the block kind."""
    W, H = rect_wh
    big = Image.new("L", (W * SS, H * SS), 0)
    d = ImageDraw.Draw(big)
    kind = blk["kind"]
    if kind == "line":
        s = blk["size"]
        while True:
            f = font(s * SS, blk.get("bold", False))
            l, t, r, b = d.textbbox((0, 0), blk["en"], font=f)
            if (r - l) <= (W - 4) * SS and (b - t) <= (H - 2) * SS or s <= 6:
                break
            s -= 0.5
            s = round(s * 2) / 2
        blk["_size"] = s
        a = f.getmetrics()
        cy = (H * SS) / 2
        # vertical centre on the cap/x band: use bbox of the whole string
        d.text(((W * SS - (r - l)) / 2 - l, cy - (t + b) / 2), blk["en"], font=f, fill=255)
    elif kind == "stack":
        lines = blk["en"]
        sizes = list(blk["sizes"])
        bl = set(blk.get("bold_lines", []))
        while True:
            fs = [font(int(sz * SS), blk.get("bold", False) or i in bl, blk.get("italic", False)) for i, sz in enumerate(sizes)]
            boxes = [d.textbbox((0, 0), ln, font=f) for ln, f in zip(lines, fs)]
            widths = [b[2] - b[0] for b in boxes]
            heights = [f.getmetrics()[0] + f.getmetrics()[1] for f in fs]
            total = sum(heights)
            if max(widths) <= (W - 6) * SS and total <= (H - 4) * SS:
                break
            sizes = [sz - 0.5 for sz in sizes]
        blk["_size"] = sizes
        gap = ((H - 4) * SS - total) / (len(lines) + 1)
        gap = gap if blk.get("spread") else min(gap, 0.35 * max(heights))
        y = (H * SS - total - gap * (len(lines) - 1)) / 2
        for ln, f, bx, hh in zip(lines, fs, boxes, heights):
            d.text(((W * SS - (bx[2] - bx[0])) / 2 - bx[0], y), ln, font=f, fill=255)
            y += hh + gap
    elif kind == "rot":
        s = blk["size"]
        while True:
            f = font(int(s * SS))
            l, t, r, b = d.textbbox((0, 0), blk["en"], font=f)
            if (r - l) <= (H - 6) * SS and (b - t) <= (W - 2) * SS:
                break
            s -= 0.5
        blk["_size"] = s
        line = Image.new("L", (H * SS, W * SS), 0)
        ImageDraw.Draw(line).text(((H * SS - (r - l)) / 2 - l, (W * SS - (b - t)) / 2 - t), blk["en"], font=f, fill=255)
        big = line.rotate(-90, expand=True)  # reads top to bottom
    elif kind == "para":
        s = blk["size"]
        while True:
            f = font(int(s * SS))
            lh = s * SS * 1.18
            space = d.textlength(" ", font=f)
            indent = s * SS
            laid = []  # (words, justify, first)
            for para in blk["en"]:
                words = para.split()
                cur, curw, first = [], 0, True
                avail = lambda first: W * SS - (indent if first else 0)
                for wd in words:
                    ww = d.textlength(wd, font=f)
                    need = ww if not cur else curw + space + ww
                    if need > avail(first) and cur:
                        laid.append((cur, True, first))
                        cur, curw, first = [wd], ww, False
                    else:
                        cur.append(wd)
                        curw = need
                laid.append((cur, False, first))
            if len(laid) * lh <= H * SS - 2 * SS or s <= 8:
                break
            s -= 0.5
        blk["_size"] = s
        top = (H * SS - len(laid) * lh) / 2
        asc = f.getmetrics()[0]
        for k, (words, just, first) in enumerate(laid):
            x = indent if first else 0
            y = top + k * lh + (lh - s * SS * 1.18) / 2
            ws = [d.textlength(wd, font=f) for wd in words]
            gap = space
            if just and len(words) > 1:
                g = (W * SS - x - sum(ws)) / (len(words) - 1)
                gap = g if g <= 2.2 * space else space  # ragged right rather than rivers in a narrow column
            for wd, ww in zip(words, ws):
                d.text((x, y), wd, font=f, fill=255)
                x += ww + gap
    return big.resize((W, H), Image.LANCZOS)


def hatch(w, h, x0, y0, period=7.0, amt=0.35):
    yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w]
    return 1 - amt * (0.5 + 0.5 * np.cos(2 * math.pi * (xx + yy) / period))


def process(n):
    pic = PICS[n]
    im = Image.open(SRC % n).convert("RGBA")
    arr = np.asarray(im).astype(float)
    orig = arr[..., :3].copy()
    rgb = arr[..., :3].copy()
    alpha = arr[..., 3:].copy()
    rows = []
    for blk in pic["blocks"]:
        row = dict(id=blk["id"], jp=blk["jp"], rect=list(blk["rect"]), glyph=blk["glyph"], kind=blk["kind"])
        if blk["kind"] == "texture":
            row.update(en="", why=blk.get("why", ""), legible=False)
            rows.append(row)
            continue
        ink = ink_colour(orig, blk)
        erase(rgb, blk, pic)
        x0, y0, x1, y1 = blk["rect"]
        m = np.asarray(render_mask(blk, (x1 - x0, y1 - y0))).astype(float) / 255.0
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.45))).astype(float) / 255
        a = (m * hatch(x1 - x0, y1 - y0, x0, y0, amt=blk.get("hatch", 0.22)))[..., None]
        reg = rgb[y0:y1, x0:x1]
        rgb[y0:y1, x0:x1] = reg * (1 - a) + ink[None, None, :] * a
        en = blk["en"] if isinstance(blk["en"], str) else " / ".join(blk["en"])
        row.update(en=en, legible=True, size=blk.get("_size"), ink=[int(v) for v in ink])
        rows.append(row)
    rng = np.random.default_rng(3)
    for (rx0, rx1, ry, col) in pic.get("rules", []):
        rgb[ry, rx0:rx1] = np.array(col, float)[None, :] + rng.normal(0, 3, (rx1 - rx0, 1))
    out = np.concatenate([np.clip(rgb, 0, 255), alpha], -1).astype(np.uint8)
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(out, "RGBA").save(OUT + "%s.png" % n)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="0,5")
    a = ap.parse_args()
    table_path = OUT + "blocks.json"
    table = json.load(open(table_path, encoding="utf-8")) if os.path.exists(table_path) else {}
    for n in PICS:
        if n in a.only.split(","):
            table[n] = dict(zoom=PICS[n]["zoom"], size=list(Image.open(SRC % n).size), rows=process(n),
                            changed=any(b["kind"] != "texture" for b in PICS[n]["blocks"]))
            print("picture", n, "blocks", len(table[n]["rows"]), "translated",
                  sum(1 for r in table[n]["rows"] if r["legible"]))
        elif n not in table:
            table[n] = dict(zoom=PICS[n]["zoom"], size=list(Image.open(SRC % n).size), changed=False,
                            rows=[dict(id=b["id"], jp=b["jp"], rect=list(b["rect"]), glyph=b["glyph"], kind="texture",
                                       en="", why=b.get("why", ""), legible=False) for b in PICS[n]["blocks"]])
    json.dump(table, open(table_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
