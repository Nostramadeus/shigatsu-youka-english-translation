"""Typeset the two tutorial example pictures the mouse run met (F16 コンフィグ.gal, F17 テキストログ.gal).
FIX1, 2026-09-26. Both are the full 960x540 screen scaled to 280 px wide (x 0.2917), so every English label is
placed where the English build draws it (positions read off mouse-run shot 158 and the 00001923 code, with the
FIX1 moves applied: volume labels 100 px left, Break Off Scenario 50 px left) and set in the build's own face,
ＭＳ Ｐ明朝, at the scaled size (25 px -> 7, 30 px -> 9). The Japanese lettering is found by brightness inside a
box per label, dilated 1 px and inpainted (cv2 Telea) so the blurred art behind it survives.
The text-log picture shows scene 000001DB (route line30, lines 250-256 + 258): its English is read from
lns-en-55/000001DB-line30.lns AT RUN TIME, so re-run this after that file's review changes.

    uv run --no-project --with pillow --with numpy --with opencv-python-headless python tools/images/tutorial_pics.py
writes work/images/out/グラフィック/システム/チュートリアル/{コンフィグ,テキストログ}.png
"""
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'work/images/png/グラフィック/システム/チュートリアル'
OUT = ROOT / 'work/images/out/グラフィック/システム/チュートリアル'
FACE = 'C:/Windows/Fonts/msmincho.ttc'   # index 1 = ＭＳ Ｐ明朝


def f(size):
    return ImageFont.truetype(FACE, size, index=1)


def erase(img, boxes, thr=110):
    """inpaint the bright lettering inside each box (x0, y0, x1, y1)."""
    a = np.array(img.convert('RGB'))
    lum = a.mean(axis=2)
    mask = np.zeros(lum.shape, np.uint8)
    for x0, y0, x1, y1 in boxes:
        sub = (lum[y0:y1, x0:x1] > thr).astype(np.uint8) * 255
        mask[y0:y1, x0:x1] = np.maximum(mask[y0:y1, x0:x1], sub)
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
    out = cv2.inpaint(a, mask, 3, cv2.INPAINT_TELEA)
    res = Image.fromarray(out).convert('RGBA')
    res.putalpha(img.getchannel('A'))
    return res


def text(d, xy, s, size, fill=(255, 255, 255, 255), anchor='lm', underline=False, stroke=0, stroke_fill=None):
    ft = f(size)
    d.text(xy, s, font=ft, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)
    if underline:
        x0, y0, x1, y1 = d.textbbox(xy, s, font=ft, anchor=anchor)
        d.line((x0, y1 + 1, x1, y1 + 1), fill=fill, width=1)


def config():
    img = Image.open(SRC / 'コンフィグ.png').convert('RGBA')
    boxes = [(13, 16, 70, 30), (13, 28, 69, 40), (13, 39, 88, 51), (13, 51, 80, 63), (13, 62, 97, 75),
             (114, 15, 165, 27), (114, 27, 196, 39), (166, 49, 184, 61), (166, 63, 194, 75), (166, 74, 193, 86),
             (196, 49, 208, 86), (256, 49, 268, 86), (109, 85, 206, 97), (29, 99, 90, 111), (110, 99, 147, 111),
             (216, 99, 244, 111), (131, 109, 196, 125), (203, 109, 260, 125), (0, 146, 40, 158)]
    img = erase(img, boxes, thr=70)
    d = ImageDraw.Draw(img)
    for y, s in ((22.5, 'Text Log'), (34, 'Skip Read Text'), (46, 'Auto Text Advance'), (57.5, 'Full Screen'),
                 (69, 'Display Mode')):
        text(d, (14.6, y), s, 9, underline=True)
    text(d, (117, 21), 'Text Speed', 7)
    text(d, (117, 33), 'Auto Advance Speed', 7)
    for y, s in ((56.4, 'BGM'), (68, 'Ambient Sound'), (80, 'Sound Effects')):
        text(d, (140, y), s, 7)
        text(d, (198, y), 'Low', 7)
        text(d, (258, y), 'High', 7)
    text(d, (111, 91), 'Text Window Opacity', 7)
    text(d, (29, 104.5), 'Quick Menu', 7)
    text(d, (111, 104.5), 'Character Bar', 7)
    text(d, (219, 104.5), 'Notifications', 7)
    text(d, (132, 116), 'Tutorial', 9, underline=True)
    text(d, (190, 116), 'Break Off Scenario', 9, underline=True)
    text(d, (1.5, 152), 'Left: 8299', 6)
    return img


def log_lines():
    raw = (ROOT / 'lns-en-55/000001DB-line30.lns').read_bytes().decode('utf-8').split('\r\r\n')
    out = []
    for ln in raw[249:258]:          # lines 250-258: the four sentences the picture shows, then the next one
        if ln.startswith(('{', ';')) or ln in ('<BR>', '<PG>', ''):
            continue
        out.append(re.sub(r'<(PG|BR|TXSPN)>', '', ln))
    return out


def textlog():
    img = Image.open(SRC / 'テキストログ.png').convert('RGBA')
    img = erase(img, [(0, 3, 170, 153)], thr=90)
    # the overlay (yellow lettering over the blue figure): repaint the whole plate from its neighbours
    a = np.array(img.convert('RGB'))
    mask = np.zeros(a.shape[:2], np.uint8)
    yel = (a[..., 0].astype(int) > 90) & (a[..., 1].astype(int) > 90) & (a[..., 2].astype(int) < 150)
    mask[58:92, 180:280] = (yel[58:92, 180:280] * 255).astype(np.uint8)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    a = cv2.inpaint(a, mask, 4, cv2.INPAINT_TELEA)
    img2 = Image.fromarray(a).convert('RGBA')
    img2.putalpha(img.getchannel('A'))
    img = img2
    d = ImageDraw.Draw(img)
    # log text: STYLE ID 1 = white body, bare words between styles = the name colour (0xFFAAAA BGR = 170,170,255)
    ft = f(8)
    x0, y, maxw, pitch = 4, 8, 162, 11.5
    for ln in log_lines():
        runs = []
        for m in re.finditer(r'<STYLE ID="1">(.*?)</STYLE>|([^<]+)', ln):
            if m.group(1) is not None:
                runs.append((m.group(1), (235, 235, 235, 255)))
            elif m.group(2):
                runs.append((m.group(2), (170, 170, 255, 255)))
        x = x0
        for s, col in runs:
            for word in re.split(r'(\s+)', s):
                if not word:
                    continue
                wlen = d.textlength(word, font=ft)
                if word.strip() and x + wlen > x0 + maxw:
                    x, y = x0, y + pitch
                if not word.strip() and x == x0:
                    continue
                d.text((x, y), word, font=ft, fill=col, anchor='lm')
                x += wlen
        y += pitch
        if y > 150:
            break
    text(d, (228, 70), 'Viewing log', 11, fill=(230, 230, 60, 255), anchor='mm', stroke=1,
         stroke_fill=(40, 90, 40, 255))
    text(d, (228, 83), 'Right-click to close', 7, fill=(230, 230, 60, 255), anchor='mm', stroke=1,
         stroke_fill=(40, 90, 40, 255))
    return img


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    config().save(OUT / 'コンフィグ.png')
    textlog().save(OUT / 'テキストログ.png')
    print('wrote', OUT)
