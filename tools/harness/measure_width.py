"""Measure text advance width in a message box screenshot.

The test TSV writes four lines into the first prompt:
  1  mixed ASCII + punctuation
  2  twenty 'i'
  3  twenty 'W'
  4  nineteen 'あ'
If line 2 and line 3 come out the same width the font is FIXED PITCH for Latin.
Line 4 gives the em, so Latin width / em says half-width vs full-width.
"""
import sys
from PIL import Image

BANDS = [("ascii mix", 100, 126, 55),
         ("20 x i   ", 130, 154, 20),
         ("20 x W   ", 158, 182, 20),
         ("19 x あ  ", 186, 216, 19)]

for path in sys.argv[1:]:
    print("==", path)
    em = None
    for label, y0, y1, n in BANDS:
        im = Image.open(path).convert("L").crop((0, y0, 960, y1))
        w, h = im.size
        px = im.load()
        cols = [x for x in range(w) if any(px[x, y] > 140 for y in range(h))]
        if not cols:
            print("  %s no ink" % label)
            continue
        width = max(cols) - min(cols) + 1
        per = width / n
        if label.startswith("19"):
            em = per
        print("  %s x=(%3d,%3d) width=%3d n=%2d  %6.2f px/char" % (label, min(cols), max(cols), width, n, per))
    if em:
        print("  em = %.2f px" % em)
