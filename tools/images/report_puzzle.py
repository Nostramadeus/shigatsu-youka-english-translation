"""report_puzzle.py - the report puzzles' UNSOLVED state: base sheet (土台.gal) + pieces (N.gal) + unsnapped overlays (Na.gal).

Script 0000001E draws rrr<ID>/土台.gal under the pieces until the puzzle is solved (rk == 5), then swaps in 全体.gal. The
pieces snap by POSITION (notes/_db/リファレンスレポート.tsv: NX / NY per piece, base-relative), so an English set must keep every
file's size, position and alpha. This tool makes that mechanical:

    compose ID [ID...]   JP full sheet = 土台 over (pieces composited into the holes) ->
                         work/images/png/<D>/rrr<ID>/_full.png and a gal template work/images/gal/<D>/rrr<ID>/_full.gal
                         (= a copy of 土台.gal) so a batch.py job can target the path "<D>/rrr<ID>/_full.gal".
    cut ID [ID...]       from the ENGLISH full sheet work/images/out/<D>/rrr<ID>/_full.png (the lane's render) write
                         out/<D>/rrr<ID>/土台.png, N.png, Na.png:
                           土台 = full_en RGB + 土台_jp alpha
                           N    = crop(full_en, NX, NY) * (N_jp / crop(full_jp))   (per pixel, per channel; = the lane's English
                                  where the piece is a plain fragment, the blood / ink tint where the piece is a stain), N_jp alpha
                           Na   = N_en * (Na_jp / N_jp), Na_jp alpha   (the dark "not snapped yet" look)
                         then GaleX files via gal_write (original as template) into work/グラフィック/<D>/rrr<ID>/, re-read and
                         compared, and the rel paths printed for tools/ship-list.txt.
    selftest ID [ID...]  cut with the JP full sheet as the source into work/images/_c/puzzle-selftest/rrr<ID>/ and report the
                         mean abs difference against the JP originals (must be ~0 for every file).

Run: cd /f/Projects/shigatsu-youka-en && PYTHONUTF8=1 uv run --no-project --with pylivemaker --with numpy python tools/images/report_puzzle.py cut 277
"""
import csv
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gal_write as GW  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
D = "グラフィック/リファレンス/リファレンス詳細/"
PNG = "work/images/png/" + D
GAL = "work/images/gal/" + D
OUT = "work/images/out/" + D
SHIP = "work/" + D          # D already starts with グラフィック/
TABLE = "notes/_db/リファレンスレポート.tsv"
EPS = 6  # a JP channel below this is "black": the ratio is undefined, the JP pixel is kept


def positions(rid):
    rows = list(csv.reader(open(TABLE, encoding="utf-8"), delimiter="\t"))
    h = rows[0]
    d = next(dict(zip(h, r)) for r in rows[1:] if r[0] == str(rid))
    n = int(d["パーツ数"])
    return [(int(float(d["%dX" % i])), int(float(d["%dY" % i]))) for i in range(n)]


def rgba(path):
    return np.array(Image.open(path).convert("RGBA")).astype(np.float32)


def save(arr, path, jp=None):
    """write RGBA; where the JP alpha is 0 the JP colour is kept (invisible in the game, keeps the encoder's bytes close)."""
    if jp is not None:
        arr = arr.copy()
        clear = jp[..., 3] == 0
        arr[clear, :3] = jp[clear, :3]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA").save(path)


def compose(rid):
    src = PNG + "rrr%d/" % rid
    base = Image.open(src + "土台.png").convert("RGBA")
    holes = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for i, (x, y) in enumerate(positions(rid)):
        p = Image.open(src + "%d.png" % i).convert("RGBA")
        holes.alpha_composite(p, (x, y))
    full = holes.copy()
    full.alpha_composite(base)          # the base wins wherever it is opaque; pieces only fill its holes
    full.save(src + "_full.png")
    shutil.copyfile(GAL + "rrr%d/土台.gal" % rid, GAL + "rrr%d/_full.gal" % rid)
    print("rrr%d: _full.png %dx%d, %d pieces" % (rid, full.width, full.height, len(positions(rid))))


def _blur(a, k=9):
    """box blur by separable cumulative sums (no scipy / cv2 needed)."""
    pad = k // 2
    for axis in (0, 1):
        ap = np.pad(a, [(pad, pad) if ax == axis else (0, 0) for ax in (0, 1)], mode="edge")
        c = np.cumsum(ap, axis=axis)
        c = np.concatenate([np.zeros_like(np.take(c, [0], axis=axis)), c], axis=axis)
        a = (np.take(c, range(k, c.shape[axis]), axis=axis) - np.take(c, range(0, c.shape[axis] - k), axis=axis)) / k
    return a


def ratio_apply(en_rgb, jp_rgb, jp_rgb_ref):
    """en * (jp / jp_ref) per channel = the piece's own tint (blood, ink wash) put over the English.
    Where jp_ref is near black (a Japanese stroke) the ratio is undefined: it is filled from the surrounding tint, so the
    JP strokes do NOT survive into the English piece (2026-10-16: the first cut carried JP handwriting inside the blood blots)."""
    out = np.empty_like(en_rgb)
    lum = jp_rgb_ref.mean(axis=2)
    local_bg = _blur(lum, 31)
    stroke = (lum < 0.7 * local_bg) | (lum > 1.4 * local_bg + 8)   # a dark or bright mark on its surroundings = a stroke (ink or chalk): undefined
    for c in range(3):
        ref = jp_rgb_ref[..., c]
        ok = ((ref >= EPS) & ~stroke).astype(np.float32)
        r = np.where(ok > 0, jp_rgb[..., c] / np.maximum(ref, 1.0), 0.0).astype(np.float32)
        r = np.minimum(r, 4.0)
        num, den = _blur(r * ok), _blur(ok)
        fill = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 1.0)
        if (den <= 1e-3).any():
            num2, den2 = _blur(r * ok, 31), _blur(ok, 31)
            fill = np.where(den > 1e-3, fill, np.where(den2 > 1e-3, num2 / np.maximum(den2, 1e-3), 1.0))
        rr = np.where(ok > 0, r, fill)
        out[..., c] = en_rgb[..., c] * rr
    return np.clip(out, 0, 255)


def cut(rid, src_full, out_dir, write_gals):
    jp_dir = PNG + "rrr%d/" % rid
    full_en = rgba(src_full)
    full_jp = rgba(jp_dir + "_full.png")
    if full_en.shape != full_jp.shape:
        raise SystemExit("rrr%d: English full sheet %s is not the JP size %s" % (rid, full_en.shape, full_jp.shape))
    made = []
    base_jp = rgba(jp_dir + "土台.png")
    base = full_en.copy()
    base[..., 3] = base_jp[..., 3]
    save(base, out_dir + "土台.png", base_jp)
    made.append("土台")
    for i, (x, y) in enumerate(positions(rid)):
        p_jp = rgba(jp_dir + "%d.png" % i)
        h, w = p_jp.shape[:2]
        crop_en = full_en[y:y + h, x:x + w, :3]
        crop_jp = full_jp[y:y + h, x:x + w, :3]
        p = np.zeros_like(p_jp)
        p[..., :3] = ratio_apply(crop_en, p_jp[..., :3], crop_jp)
        p[..., 3] = p_jp[..., 3]
        save(p, out_dir + "%d.png" % i, p_jp)
        made.append(str(i))
        a_path = jp_dir + "%da.png" % i
        if os.path.exists(a_path):
            a_jp = rgba(a_path)
            a = np.zeros_like(a_jp)
            a[..., :3] = ratio_apply(p[..., :3], a_jp[..., :3], p_jp[..., :3])
            a[..., 3] = a_jp[..., 3]
            save(a, out_dir + "%da.png" % i, a_jp)
            made.append("%da" % i)
    rel = []
    if write_gals:
        for name in made:
            orig = GAL + "rrr%d/%s.gal" % (rid, name)
            out_gal = SHIP + "rrr%d/%s.gal" % (rid, name)
            os.makedirs(os.path.dirname(out_gal), exist_ok=True)
            GW.write_gal(orig, out_dir + name + ".png", out_gal, "keep", None, 0)
            back = np.array(Image.open(out_gal).convert("RGBA")).astype(np.float32)
            want = rgba(out_dir + name + ".png")
            vis = want[..., 3] > 0
            diff = float(np.abs(back[vis] - want[vis]).mean()) if vis.any() else 0.0   # JPEG loss on visible pixels only
            if diff > 6.0:
                raise SystemExit("rrr%d/%s.gal re-read differs from the png (mean %.2f)" % (rid, name, diff))
            rel.append(D + "rrr%d/%s.gal" % (rid, name))
    return made, rel


def selftest(rid):
    out_dir = "work/images/_c/puzzle-selftest/rrr%d/" % rid
    made, _ = cut(rid, PNG + "rrr%d/_full.png" % rid, out_dir, False)
    worst = 0.0
    for name in made:
        a = rgba(out_dir + name + ".png")
        b = rgba(PNG + "rrr%d/%s.png" % (rid, name))
        d = float(np.abs(a - b).mean())
        worst = max(worst, d)
        if d > 1.0:
            print("  rrr%d/%s: mean abs diff %.2f" % (rid, name, d))
    print("rrr%d selftest: %d files, worst mean abs diff %.3f" % (rid, len(made), worst))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd, ids = sys.argv[1], [int(a) for a in sys.argv[2:]]
    for rid in ids:
        if cmd == "compose":
            compose(rid)
        elif cmd == "selftest":
            if not os.path.exists(PNG + "rrr%d/_full.png" % rid):
                compose(rid)
            selftest(rid)
        elif cmd == "cut":
            src = OUT + "rrr%d/_full.png" % rid
            if not os.path.exists(src):
                raise SystemExit("missing the English full sheet %s" % src)
            made, rel = cut(rid, src, OUT + "rrr%d/" % rid, True)
            print("rrr%d: %d files written and verified" % (rid, len(made)))
            for r in rel:
                print(r)
        else:
            raise SystemExit("unknown command " + cmd)


if __name__ == "__main__":
    main()
