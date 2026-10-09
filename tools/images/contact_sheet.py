"""Build labeled contact sheets from a folder of PNGs so one image Read can judge many files.

Usage: uv run --no-project --with pillow python tools/images/contact_sheet.py SRC_DIR OUT_PREFIX [--cols 4] [--rows 4] [--cell 300x200]
Writes OUT_PREFIX-NN.png and OUT_PREFIX.tsv (sheet, cell index, relative path, WxH). Each cell shows the image
fitted into the cell (checkerboard under transparency) with its index in the corner.
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out_prefix")
ap.add_argument("--cols", type=int, default=4)
ap.add_argument("--rows", type=int, default=4)
ap.add_argument("--cell", default="300x200")
ap.add_argument("--ext", default=".png")
args = ap.parse_args()

cw, ch = (int(v) for v in args.cell.split("x"))
label_h = 18
files = []
for root, _, names in os.walk(args.src):
    for n in sorted(names):
        if n.lower().endswith(args.ext):
            files.append(os.path.relpath(os.path.join(root, n), args.src))
files.sort()
per = args.cols * args.rows
try:
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 14)
except Exception:
    font = ImageFont.load_default()

os.makedirs(os.path.dirname(args.out_prefix) or ".", exist_ok=True)
tsv = open(args.out_prefix + ".tsv", "w", encoding="utf-8")
tsv.write("sheet\tcell\tfile\tsize\n")
for s in range(0, len(files), per):
    chunk = files[s:s + per]
    sheet = Image.new("RGB", (args.cols * cw, args.rows * (ch + label_h)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for k, rel in enumerate(chunk):
        idx = s + k
        im = Image.open(os.path.join(args.src, rel)).convert("RGBA")
        w, h = im.size
        scale = min((cw - 4) / w, (ch - 4) / h, 1.0)
        thumb = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
        # checkerboard so transparent/white text is visible
        bg = Image.new("RGBA", thumb.size, (200, 200, 200, 255))
        bd = ImageDraw.Draw(bg)
        for yy in range(0, thumb.size[1], 16):
            for xx in range(0, thumb.size[0], 16):
                if ((xx // 16) + (yy // 16)) % 2:
                    bd.rectangle((xx, yy, xx + 15, yy + 15), fill=(120, 120, 120, 255))
        bg.alpha_composite(thumb)
        cx = (k % args.cols) * cw + 2
        cy = (k // args.cols) * (ch + label_h) + 2
        sheet.paste(bg.convert("RGB"), (cx, cy))
        d.text((cx + 2, cy + ch - 2), "%d  %s  %dx%d" % (idx, rel[-34:], w, h), fill=(255, 255, 0), font=font)
        tsv.write("%d\t%d\t%s\t%dx%d\n" % (s // per, idx, rel, w, h))
    out = "%s-%02d.png" % (args.out_prefix, s // per)
    sheet.save(out)
    print(out, len(chunk))
tsv.close()
print("files:", len(files))
