"""Convert .gal files to .png with pylivemaker's PIL plugin (read-only direction).

Run: uv run --no-project --with pylivemaker python tools/images/gal_to_png.py SRC_DIR_OR_FILE DST_DIR
Mirrors the folder structure under DST_DIR; skips files that already have a PNG; prints size/mode per file.
"""
import os
import sys

from PIL import Image
import livemaker.GalImagePlugin  # noqa: F401  (registers the GAL opener)

src, dst = sys.argv[1], sys.argv[2]
files = []
if os.path.isfile(src):
    files = [(os.path.dirname(src), os.path.basename(src))]
else:
    for root, _, names in os.walk(src):
        for n in names:
            if n.lower().endswith(".gal"):
                files.append((root, n))
ok = fail = 0
for root, n in sorted(files):
    rel = os.path.relpath(os.path.join(root, n), src if os.path.isdir(src) else os.path.dirname(src))
    out = os.path.join(dst, os.path.splitext(rel)[0] + ".png")
    if os.path.exists(out):
        ok += 1
        continue
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        im = Image.open(os.path.join(root, n))
        im.load()
        im.save(out)
        print(f"{rel}\t{im.size[0]}x{im.size[1]}\t{im.mode}\tframes={getattr(im, 'n_frames', 1)}")
        ok += 1
    except Exception as e:
        print(f"{rel}\tFAIL\t{e}")
        fail += 1
print(f"done ok={ok} fail={fail}", file=sys.stderr)
