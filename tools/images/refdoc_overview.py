"""refdoc_overview.py - is a reference's 概要 picture just a scaled crop of its 詳細 page?

If it is, the English 概要 can be rebuilt from the English 詳細 instead of being typeset again at 300x170,
where the body text of a form is only a few pixels tall and nothing would be legible.

  probe  <ID> [<ID> ...]   search crop+scale, print the best mean abs difference
  build  <ID> [<ID> ...]   apply the recorded transform to our translated 詳細 and write the 概要 PNG

The transform is a top-anchored crop of the detail, width-fitted, then resized to the 概要 size.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PNG = ROOT / "work/images/png/グラフィック/リファレンス"
OUT = ROOT / "work/images/out/グラフィック/リファレンス"


def detail(rid, src=PNG):
    return Image.open(src / ("リファレンス詳細/rrr%s/0.png" % rid)).convert("RGB")


def overview(rid, src=PNG):
    return Image.open(src / ("リファレンス概要/rr%s.png" % rid)).convert("RGB")


def candidates(d, ow, oh):
    """yield (label, box) crops of the detail that could have produced an ow x oh overview."""
    W, H = d.size
    yield "whole page (squashed)", (0, 0, W, H)
    ar = ow / float(oh)
    ch = int(round(W / ar))
    if ch <= H:
        for name, top in (("top crop", 0), ("upper third", int(H * 0.08)), ("middle", (H - ch) // 2)):
            yield name, (0, top, W, top + ch)
    cw = int(round(H * ar))
    if cw <= W:
        yield "centre column", ((W - cw) // 2, 0, (W - cw) // 2 + cw, H)


def probe(rid):
    d, o = detail(rid), overview(rid)
    best = None
    for name, box in candidates(d, *o.size):
        c = d.crop(box).resize(o.size, Image.LANCZOS)
        diff = np.abs(np.array(c).astype(int) - np.array(o).astype(int)).mean()
        if best is None or diff < best[0]:
            best = (diff, name, box)
        print("   %-22s box=%-28s mean abs diff %.2f" % (name, box, diff))
    print("rr%-5s BEST %s %s -> %.2f%s" % (rid, best[1], best[2], best[0],
                                           "   (a rebuild reproduces it)" if best[0] < 12 else "   (NOT a crop: typeset it)"))
    return best


def build(rid):
    best = probe(rid)
    if best[0] >= 12:
        print("rr%s: not a crop of the detail, skipped" % rid)
        return False
    en = Image.open(OUT / ("リファレンス詳細/rrr%s/0.png" % rid)).convert("RGB")
    o = overview(rid)
    out = en.crop(best[2]).resize(o.size, Image.LANCZOS)
    # IMAGES3: keep the original 概要's alpha (rounded card corners); the RGB comes from the English page
    out = out.convert("RGBA")
    out.putalpha(Image.open(PNG / ("リファレンス概要/rr%s.png" % rid)).getchannel("A"))
    p = OUT / ("リファレンス概要/rr%s.png" % rid)
    p.parent.mkdir(parents=True, exist_ok=True)
    out.save(p)
    print("wrote %s" % p)
    return True


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    for i in ids:
        (probe if cmd == "probe" else build)(i)
