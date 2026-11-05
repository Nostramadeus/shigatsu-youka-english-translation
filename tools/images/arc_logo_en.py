"""arc_logo_en.py - English lettering for the encyclopedia arc-selector logo of 呪殺編 (smoke test r2, 2026-11-05).

    PYTHONUTF8=1 uv run --no-project --with pillow --with numpy python tools/images/arc_logo_en.py [--style A|B|C] [--sheet OUT.png]

WHY: the encyclopedia's arc selector (00001878 idx 1875 = the selected arc, path built from the English arc name;
idx 1878 = the dropdown entry, JP file name) shows グラフィック\\メニュー\\右クリック\\呪殺編ロゴ.gal, a 146x50 picture of
the brush kanji 呪殺編 in blue with furigana and a red blood-mist glow. Until now the patch shipped it unchanged
(tools/build_arc_assets.py copies it under the English name). The owner asked (2026-11-05) for an English picture
with the arc's English name; no other arc logo is re-lettered (Q2445 still open for the rest).

WORDING: the shipped arc name, patch/hen-jp-en.tsv / notes/v2/GLOSSARY.tsv: "Jusatsu Arc [Killing by Curse]".
Both layers stay (the reading as the big word, the meaning in brackets on the second line); nothing is cut.

LOOK: same canvas (146x50, alpha), the original's colours (blue fill, light at the top and darker at the bottom; red
glow around the letters), the original's red mist blurred past legibility behind the new words so no kanji ghost
remains. No English arc logo existed in the patch to copy, so the face follows the English plates on the same
screen: both lines in the owner's gothic pick (HGP Soei Kaku Gothic UB, the face of the encyclopedia's English
tabs and buttons) = style B. Compared on a sheet (--sheet): A (Chiller caps, the title-menu brush pick) was hard to
read at 146x50; C (Cambria Bold) read well but matches no English plate on that screen.

OUTPUT: work/images/out/グラフィック/メニュー/右クリック/呪殺編ロゴ.png; then gal_write.py with the original as template.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'work/images/png/グラフィック/メニュー/右クリック/呪殺編ロゴ.png'
OUT = ROOT / 'work/images/out/グラフィック/メニュー/右クリック/呪殺編ロゴ.png'
F = 'C:/Windows/Fonts/'
BIG, SMALL = 'JUSATSU ARC', '[Killing by Curse]'
STYLES = {  # big font, index, small font, index
    'A': (F + 'CHILLER.TTF', 0, F + 'HGRSGU.TTC', 1),
    'B': (F + 'HGRSGU.TTC', 1, F + 'HGRSGU.TTC', 1),
    'C': (F + 'cambriab.ttf', 0, F + 'HGRSGU.TTC', 1),
}
W, H = 146, 50
MARGIN = 3
BIG_BOX = (MARGIN, 1, W - MARGIN, 33)       # big line lives here (x0, y0, x1, y1)
SMALL_BOX = (MARGIN, 34, W - MARGIN, 49)    # gloss line


def fit(text, path, idx, box, max_size):
    """Largest size <= max_size whose ink fits the box."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    for size in range(max_size, 6, -1):
        font = ImageFont.truetype(path, size, index=idx)
        l, t, r, b = font.getbbox(text)
        if r - l <= bw and b - t <= bh:
            return font, (l, t, r, b)
    raise SystemExit('does not fit: %r' % text)


def text_mask(text, font, bbox, box):
    m = Image.new('L', (W, H), 0)
    l, t, r, b = bbox
    x = box[0] + ((box[2] - box[0]) - (r - l)) / 2 - l
    y = box[1] + ((box[3] - box[1]) - (b - t)) / 2 - t
    ImageDraw.Draw(m).text((x, y), text, font=font, fill=255)
    return m


def build(style):
    big_path, big_idx, small_path, small_idx = STYLES[style]
    orig = np.asarray(Image.open(SRC).convert('RGBA')).astype(np.float64)
    bf, bb = fit(BIG, big_path, big_idx, BIG_BOX, 34)
    sf, sb = fit(SMALL, small_path, small_idx, SMALL_BOX, 14)
    mask = np.maximum(np.asarray(text_mask(BIG, bf, bb, BIG_BOX), np.float64),
                      np.asarray(text_mask(SMALL, sf, sb, SMALL_BOX), np.float64)) / 255.0

    # 1) the original's red mist with the blue kanji/furigana removed, blurred past legibility
    r, g, b, a = (orig[..., i] for i in range(4))
    redish = (r > b + 20)
    mist_a = np.where(redish, a, 0.0)
    mist = Image.fromarray(mist_a.astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(4))
    mist_a = np.asarray(mist, np.float64) / 255.0 * 0.75

    # 2) a tight red glow around the new words (the original's glyph halo)
    halo = Image.fromarray((mask * 255).astype(np.uint8), 'L').filter(ImageFilter.MaxFilter(5))
    halo = halo.filter(ImageFilter.GaussianBlur(1.6))
    halo_a = np.clip(np.asarray(halo, np.float64) / 255.0 * 1.15, 0, 1)

    red = np.array([190.0, 18.0, 18.0])
    under_a = 1 - (1 - mist_a) * (1 - halo_a)
    # 3) blue words, vertical gradient like the original fill
    ys = np.linspace(0, 1, H)[:, None]
    g0 = 40 - 30 * ys * np.ones((1, W))
    blue = np.stack([g0, g0, 255 - 55 * ys * np.ones((1, W))], axis=-1)
    out_a = mask + under_a * (1 - mask)
    with np.errstate(invalid='ignore', divide='ignore'):
        rgb = (blue * mask[..., None] + red * (under_a * (1 - mask))[..., None]) / out_a[..., None]
    rgb = np.nan_to_num(rgb)
    img = np.dstack([np.clip(rgb, 0, 255), np.clip(out_a * 255, 0, 255)]).astype(np.uint8)
    return Image.fromarray(img, 'RGBA'), (bf.size, sf.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--style', default='B')
    ap.add_argument('--sheet', help='write a comparison sheet of all styles (plate colour, 1x and 3x) here')
    args = ap.parse_args()
    if args.sheet:
        plate = (100, 0, 0, 255)                                   # 00001878 idx 1867 inner box as drawn (522.png)
        tiles = [Image.open(SRC).convert('RGBA')] + [build(s)[0] for s in STYLES]
        Z = 3
        sheet = Image.new('RGBA', (W * Z + W + 40, (H * Z + 12) * len(tiles) + 12), (30, 30, 30, 255))
        for i, t in enumerate(tiles):
            y = 12 + i * (H * Z + 12)
            bg1 = Image.new('RGBA', (W, H), plate); bg1.alpha_composite(t)
            bgz = Image.new('RGBA', (W * Z, H * Z), plate); bgz.alpha_composite(t.resize((W * Z, H * Z), Image.LANCZOS))
            sheet.alpha_composite(bg1, (12, y)); sheet.alpha_composite(bgz, (W + 28, y))
        sheet.convert('RGB').save(args.sheet)
        print('sheet', args.sheet, '(rows: original, ' + ', '.join(STYLES) + ')')
        return
    img, sizes = build(args.style)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print('wrote %s style %s, type sizes big/small = %s' % (OUT.relative_to(ROOT), args.style, sizes))


if __name__ == '__main__':
    main()
