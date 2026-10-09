"""refdoc_marks.py - replace small repeated kanji marks (timetable destination marks 女 / 大 / 西) with Latin
letters (IMAGES3, 2026-10-01). Each candidate blob (ink component of the given size range) is classified by
normalised correlation against template patches taken from the picture itself; a blob that matches no template
above --thr is left alone and reported. Matched blobs are painted in the local background colour and the letter
is centred on the blob. Starts from the Japanese source PNG and writes work/images/out/<path>.png, so run it
BEFORE the chained batch.py lines job of the same picture.

  uv run --no-project --with pillow --with numpy --with opencv-python-headless python tools/images/refdoc_marks.py \
      REL_PNG "x,y,w,h=L" ["x,y,w,h=L" ...] [--size 6-16] [--thr 0.7] [--px 12] [--below Y]
REL_PNG is relative to work/images/png/. --below: only blobs with top >= Y.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
FONT = "C:/Windows/Fonts/cambria.ttc"


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    rel = sys.argv[1]
    temps = [a for a in sys.argv[2:] if "=" in a and not a.startswith("--")]
    lo, hi = map(int, opt("--size", "6-16").split("-"))
    thr, px, below = float(opt("--thr", "0.7")), int(opt("--px", "12")), int(opt("--below", "0"))
    im = Image.open(ROOT / "work/images/png" / rel).convert("RGBA")
    a = np.array(im)
    g = cv2.cvtColor(a[:, :, :3], cv2.COLOR_RGB2GRAY)
    ink = (g < 140).astype(np.uint8)
    T = []
    for t in temps:
        box, letter = t.split("=")
        x, y, w, h = map(int, box.split(","))
        T.append((letter, (1 - ink[y:y + h, x:x + w]).astype(np.float32)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(ink, np.ones((2, 2), np.uint8)))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, px)
    counts, skipped = {}, []
    for s in st[1:]:
        x, y, w, h = map(int, s[:4])
        if not (lo <= w <= hi and lo <= h <= hi) or y < below:
            continue
        best = None
        for letter, tp in T:
            th, tw = tp.shape
            pad = 3
            y0, x0 = max(0, y - pad), max(0, x - pad)
            region = (1 - ink[y0:y + h + pad, x0:x + w + pad]).astype(np.float32)
            if region.shape[0] < th or region.shape[1] < tw:
                continue
            r = cv2.matchTemplate(region, tp, cv2.TM_CCOEFF_NORMED).max()
            if best is None or r > best[0]:
                best = (r, letter)
        if best is None or best[0] < thr:
            skipped.append((x, y, w, h, round(float(best[0]), 2) if best else None))
            continue
        # local background: the mode colour of the ring around the blob
        ring = a[max(0, y - 3):y + h + 3, max(0, x - 3):x + w + 3, :3].reshape(-1, 3)
        light = ring[ring.sum(axis=1) > 600]
        bg = tuple(int(v) for v in (np.median(light, axis=0) if len(light) else (255, 255, 255)))
        d.rectangle((x - 1, y - 1, x + w, y + h), fill=bg + (255,))
        d.text((x + w / 2, y + h / 2), best[1], font=font, fill=(17, 17, 17, 255), anchor="mm")
        counts[best[1]] = counts.get(best[1], 0) + 1
    out = ROOT / "work/images/out" / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out)
    print("replaced", counts, "| not matched:", skipped)


if __name__ == "__main__":
    main()
