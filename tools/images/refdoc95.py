"""Typeset reference 95 (the change-of-address form, グラフィック\\リファレンス\\リファレンス詳細\\rrr95\\0.gal) in English.
FIX1, 2026-09-26 (mouse run F28, owner items b/e). Wording: notes/_tmp/tl-log-IMAGES2.md "Drafted, NOT yet
rendered - 95" (IMAGES2), place names as shipped elsewhere (Motoki-cho, Sawa Prefecture). Printed text =
Cambria, handwritten field values = Ink Free (the owner's picks for serif / handwriting), black on the white
page. Every Japanese glyph box (found with work/_fix1/ink_boxes.py, table rules excluded) is filled white;
the table rules and the seal boxes are untouched; the circled 印 by the name is "(seal)" (FIX2).

    uv run --no-project --with pillow python tools/images/refdoc95.py
writes work/images/out/グラフィック/リファレンス/リファレンス詳細/rrr95/0.png (RGBA, same size, alpha untouched).
Then: refdoc_overview.py build 95 (the 300x170 preview is a scaled top crop of this page), gal_write.py.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'work/images/png/グラフィック/リファレンス/リファレンス詳細/rrr95/0.png'
OUT = ROOT / 'work/images/out/グラフィック/リファレンス/リファレンス詳細/rrr95/0.png'
SERIF = 'C:/Windows/Fonts/cambria.ttc'
HAND = 'C:/Windows/Fonts/Inkfree.ttf'
INK = (0, 0, 0, 255)

im = Image.open(SRC).convert('RGBA')
alpha = im.getchannel('A')
d = ImageDraw.Draw(im)


def erase(x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=(255, 255, 255, 255))


def font(path, size):
    return ImageFont.truetype(path, size)


def put(x, y, text, path, size, anchor='lm', max_w=None):
    f = font(path, size)
    while max_w and d.textlength(text, font=f) > max_w and size > 8:
        size -= 1
        f = font(path, size)
    d.text((x, y), text, font=f, fill=INK, anchor=anchor)
    return x + d.textlength(text, font=f)


# erase every Japanese glyph run (boxes from ink_boxes.py, padded 3 px; none touches a rule)
for x0, x1, y0, y1 in [(535, 756, 46, 67), (262, 537, 94, 138), (425, 660, 189, 218), (440, 715, 228, 255),
                       (433, 735, 265, 292), (170, 620, 328, 356), (96, 184, 424, 447), (228, 492, 421, 452),
                       (96, 184, 481, 504), (228, 708, 479, 508), (96, 184, 539, 561), (228, 708, 536, 565),
                       (236, 414, 618, 653), (103, 174, 624, 647), (76, 116, 695, 711), (497, 566, 862, 878),
                       (575, 645, 862, 878), (660, 716, 862, 878)]:
    erase(x0, y0, x1, y1)

P, H = SERIF, HAND
# top line: 祀耀[ ]年度 第[ ]号
put(540, 57, 'Shiyo', P, 15)
put(600, 57, 'School Year', P, 15)
put(690, 57, 'No.', P, 15)
# title
put(400, 116, 'CHANGE OF ADDRESS', P, 34, anchor='mm')
# name, class, birth date
put(425, 203, 'Name', P, 15)
put(480, 203, 'Natsumi Kogori', H, 23)
put(442, 242, 'Year', P, 15)
put(480, 242, '2', H, 23)
put(510, 242, 'Class', P, 15)
put(555, 242, '2', H, 23)
put(590, 242, 'No.', P, 15)
put(622, 242, '20', H, 23)
x = put(437, 280, 'Born  Shiyo', P, 15)
put(x + 8, 280, '783, July 29', H, 23)
# statement
put(397, 342, 'I have moved to the address below and hereby submit this notification.', P, 20, anchor='mm',
    max_w=640)
# table
put(139, 436, 'Date of move', P, 15, anchor='mm')
put(240, 437, 'Shiyo 800, May 5', H, 25)
put(139, 493, 'Address before', P, 15, anchor='mm')
put(232, 484, '120-10 Nagaminedai, Motoki-cho, Sawa Prefecture', H, 19, max_w=480)
put(232, 506, 'Repo Heights Room 305', H, 19)
put(139, 550, 'Address after', P, 15, anchor='mm')
put(232, 541, '120-10 Nagaminedai, Motoki-cho, Sawa Prefecture', H, 19, max_w=480)
put(232, 563, 'Repo Heights Room 306', H, 19)
put(139, 636, 'Reason for move', P, 15, anchor='mm', max_w=122)
put(240, 636, 'Due to family circumstances', H, 25)
put(78, 702, 'Remarks', P, 14)
# FIX2 2026-09-26 (mouse run 2 N3): the circled 印 next to the name (ink box x 678-691, y 201-214) -> "(seal)"
erase(676, 199, 693, 216)
put(685, 208, '(seal)', P, 11, anchor='mm')
# seal box headers
put(531, 871, 'Principal', P, 13, anchor='mm', max_w=64)
put(610, 871, 'Year Head', P, 13, anchor='mm', max_w=64)
put(688, 871, 'Homeroom', P, 13, anchor='mm', max_w=54)

im.putalpha(alpha)
OUT.parent.mkdir(parents=True, exist_ok=True)
im.save(OUT)
print('wrote', OUT)
