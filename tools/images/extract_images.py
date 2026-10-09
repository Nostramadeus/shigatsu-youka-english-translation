"""Extract ONLY the named image entries (or folder prefixes) from the LiveMaker exe archive.

Never extracts the whole archive (the exe is 1 GB; F: has < 1 GB free). Output keeps the
archive-relative path under --out (default work/images/gal), so a file can later be dropped
next to the exe in the same relative path.

Run (from the project root):
    uv run --no-project --with pylivemaker python tools/images/extract_images.py --prefix "グラフィック\\タイトル\\"
    uv run --no-project --with pylivemaker python tools/images/extract_images.py --name "グラフィック\\システム\\foo.gal"
    uv run --no-project --with pylivemaker python tools/images/extract_images.py --names-file work/images/part1-images.txt
    ... --list-only prints the matching entries and their stored sizes without extracting.
"""
import argparse
import os
import sys

from livemaker.archive import LMArchive

EXE = r"F:\4gatsu_8ka_Ver2.0.0.4\死月妖花～四月八日～.exe"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUT = os.path.join(ROOT, "work", "images", "gal")

ap = argparse.ArgumentParser()
ap.add_argument("--prefix", action="append", default=[], help="archive path prefix (backslashes), repeatable")
ap.add_argument("--name", action="append", default=[], help="exact archive path, repeatable")
ap.add_argument("--names-file", default=None, help="UTF-8 file, one archive path per line")
ap.add_argument("--ext", default=".gal,.png,.jpg,.bmp,.lcm", help="comma list of extensions to keep")
ap.add_argument("--out", default=DEFAULT_OUT)
ap.add_argument("--list-only", action="store_true")
ap.add_argument("--max-mb", type=float, default=60.0, help="refuse to extract more than this many stored MB")
args = ap.parse_args()

exts = tuple(e.strip().lower() for e in args.ext.split(",") if e.strip())
names = set(n.lower() for n in args.name)
if args.names_file:
    with open(args.names_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                names.add(line.lower())
picked = []
seen = set()
with LMArchive(EXE) as lm:
    for info in lm.infolist():
        n = info.name
        if not n.lower().endswith(exts):
            continue
        if n.lower() in names or any(n.startswith(p) for p in args.prefix):
            picked.append(info)
            seen.add(n.lower())
    total = sum(i.compressed_size for i in picked)
    print("matched %d entries, stored %.1f MB" % (len(picked), total / 1048576), file=sys.stderr)
    for n in sorted(names - seen):
        print("not in archive: %s" % n, file=sys.stderr)
    if args.list_only:
        for i in picked:
            print("%d\t%s" % (i.compressed_size, i.name))
        sys.exit(0)
    if total / 1048576 > args.max_mb:
        print("refusing: %.1f MB > --max-mb %s" % (total / 1048576, args.max_mb), file=sys.stderr)
        sys.exit(2)
    os.makedirs(args.out, exist_ok=True)
    skipped = 0
    for i in picked:
        dst = os.path.join(args.out, i.name.replace("\\", os.sep))
        if os.path.exists(dst):
            skipped += 1
            continue
        lm.extract(i, path=args.out)
        print(i.name)
print("extracted %d files to %s (%d already present)" % (len(picked) - skipped, args.out, skipped), file=sys.stderr)
