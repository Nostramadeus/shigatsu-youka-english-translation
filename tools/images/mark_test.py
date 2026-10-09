"""Draw an obvious colored bar on a PNG (format-test marker).

Usage: mark_test.py IN.png OUT.png COLOR [y0 y1]
"""
import sys

from PIL import Image, ImageDraw

src, dst, color = sys.argv[1], sys.argv[2], sys.argv[3]
y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 4
y1 = int(sys.argv[5]) if len(sys.argv) > 5 else 18
im = Image.open(src).convert("RGBA")
d = ImageDraw.Draw(im)
d.rectangle((0, y0, im.size[0], y1), fill=color)
im.save(dst)
print(dst, im.size)
