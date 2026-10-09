"""batch.py - render, encode, preview and ship the picture jobs of tools/images/jobs_part1.py.

Run (project root, one process, ~2-4 min):
    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --with pylivemaker --with numpy --with opencv-python-headless \
        python tools/images/batch.py [--only ID,ID] [--styles gothic,serif] [--no-ship] [--dry]

Per item: source PNG (work/images/png/<path>.png, converted from the archive GAL) -> analysis (background colour,
lettering mask, erase box, text band, fill / outline colour sampled from the original) -> erase (flat fill, inpaint
of the lettering mask, or alpha clear) -> English set with the style's font (largest size that fits the band) ->
PNG (work/images/out/<path>.png) -> GaleX (work/グラフィック/<path>.gal, verified by re-read) -> copied to
F:/4gatsu_8ka_EN/グラフィック/<path>.gal (the loose-file shipping path) -> listed in tools/ship-list.txt under
"# pictures". A before | after preview per job goes to review/images/preview/<nn>-<id>.png and an index page to
review/images/preview/index.html. Translations marked new=True are appended to notes/_tmp/tl-log-IMAGES.md.
"""
import argparse
import html
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
import cv2  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
import typeset_ui as T  # noqa: E402
import gal_write as GW  # noqa: E402

# which job module to run: --jobs on the command line, or SY_JOBS in the environment (default = part 1)
_JOBS_MODULE = os.environ.get("SY_JOBS", "jobs_part1")
for _i, _a in enumerate(sys.argv):
    if _a == "--jobs" and _i + 1 < len(sys.argv):
        _JOBS_MODULE = sys.argv[_i + 1]
    elif _a.startswith("--jobs="):
        _JOBS_MODULE = _a.split("=", 1)[1]
JOBS = __import__(_JOBS_MODULE).JOBS

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
PNG_DIR = "work/images/png/"
GAL_DIR = "work/images/gal/"
OUT_PNG = "work/images/out/"
OUT_GAL = "work/"
EN_DIR = os.environ.get("SY_EN_DIR", "F:/4gatsu_8ka_EN") + "/"
PREVIEW = "review/images/preview/" if _JOBS_MODULE == "jobs_part1" else "review/images/preview-%s/" % _JOBS_MODULE.replace("jobs_", "")
SHIP_LIST = "tools/ship-list.txt"
TL_LOG = os.environ.get("SY_TL_LOG") or (
    "notes/_tmp/tl-log-IMAGES.md" if _JOBS_MODULE == "jobs_part1" else "notes/_tmp/tl-log-IMAGES2.md")
F = "C:/Windows/Fonts/"

# the owner's picks (2026-09-26): heavy gothic = C, serif = Cambria Regular, rounded = Century Gothic Bold,
# handwriting = Ink Free, brush = Chiller
FONTS = {
    "gothic": (F + "HGRSGU.TTC", 1),
    "serif": (F + "cambria.ttc", 0),
    "rounded": (F + "GOTHICB.TTF", 0),
    "handwriting": (F + "Inkfree.ttf", 0),
    "brush": (F + "CHILLER.TTF", 0),
}


def hexcol(c):
    return "#%02x%02x%02x" % (int(c[0]), int(c[1]), int(c[2]))


def mode_colour(px):
    """Most common colour (quantised to 8 levels), then the mean of the pixels near it."""
    if len(px) == 0:
        return np.array([0, 0, 0])
    q = (px // 32).astype(np.int32)
    keys = q[:, 0] * 64 + q[:, 1] * 8 + q[:, 2]
    k = np.bincount(keys).argmax()
    sel = keys == k
    return px[sel].mean(axis=0)


def dist(rgb, c):
    return np.abs(rgb.astype(int) - np.array(c).astype(int)).sum(axis=-1)


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]


def drop_edge_components(mask, region):
    """Remove connected components that touch the image edge or the edge of the opaque region (frames, side blocks)."""
    n, lab, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8)
    if n <= 1:
        return mask
    edge = np.zeros_like(mask)
    edge[0, :] = edge[-1, :] = edge[:, 0] = edge[:, -1] = True
    outside = ~region
    outside_d = cv2.dilate(outside.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    bad = edge | outside_d
    keep = np.zeros_like(mask)
    for i in range(1, n):
        comp = lab == i
        if not (comp & bad).any():
            keep |= comp
    return keep


def analyze(im, job):
    rgba = np.array(im)
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]
    h, w = alpha.shape
    opaque = alpha > job.get("alpha_thr", 128)
    info = {"w": w, "h": h}
    glyph_mode = False
    region = np.ones((h, w), bool)
    if opaque.mean() < 0.98:
        ob = bbox(opaque)
        fill_ratio = opaque[ob[1]:ob[3], ob[0]:ob[2]].mean() if ob else 0
        if fill_ratio < 0.85 or job.get("erase") == "alpha":
            glyph_mode = True
        else:
            region = opaque
    if job.get("mask_color"):
        t = job["mask_color"]
        mask = ((rgb[:, :, 0] >= t[0]) & (rgb[:, :, 0] <= t[1]) & (rgb[:, :, 1] >= t[2]) & (rgb[:, :, 1] <= t[3])
                & (rgb[:, :, 2] >= t[4]) & (rgb[:, :, 2] <= t[5]) & opaque)
        bg = mode_colour(rgb[opaque & ~mask])
        glyph_mode = False
    elif glyph_mode:
        mask = opaque
        bg = None
    else:
        bg = mode_colour(rgb[region])
        mask = region & (dist(rgb, bg) > job.get("thr", 70))
        if not job.get("keep_edges"):
            mask = drop_edge_components(mask, region)
    if job.get("box"):
        x0, y0, x1, y1 = job["box"]
        inner = np.zeros_like(mask)
        inner[y0:y1, x0:x1] = True
        mask = mask & inner
    eb = bbox(mask)
    if eb is None:
        raise RuntimeError("no lettering found")
    pad = job.get("pad", 3)
    eb = [max(0, eb[0] - pad), max(0, eb[1] - pad), min(w, eb[2] + pad), min(h, eb[3] + pad)]
    # fill / outline colours
    m8 = mask.astype(np.uint8)
    inner = cv2.erode(m8, np.ones((5, 5), np.uint8)).astype(bool)
    if inner.sum() < 20:
        inner = cv2.erode(m8, np.ones((3, 3), np.uint8)).astype(bool)
    if inner.sum() < 8:
        inner = mask
    fill = mode_colour(rgb[inner])
    border = mask & ~cv2.erode(m8, np.ones((3, 3), np.uint8)).astype(bool)
    outline = None
    if border.sum() >= 20:
        oc = mode_colour(rgb[border])
        if dist(oc[None, :], fill)[0] > 120:
            outline = oc
    # text band and horizontal room
    gh = eb[3] - eb[1]
    py = max(2, int(0.22 * gh))
    ty0, ty1 = max(0, eb[1] - py), min(h, eb[3] + py)
    if job.get("textbox"):
        tb = job["textbox"]
    elif glyph_mode:
        tb = [2, ty0, w - 2, ty1]
    else:
        band = slice(eb[1], eb[3])
        free = ((dist(rgb[band], bg) <= job.get("thr", 70)) | mask[band]) & region[band]
        colfree = free.all(axis=0)
        left = eb[0]
        while left > 0 and colfree[left - 1]:
            left -= 1
        right = eb[2]
        while right < w and colfree[right]:
            right += 1
        tb = [min(left + 4, eb[0]), ty0, max(right - 4, eb[2]), ty1]
    info.update(glyph=glyph_mode, bg=bg, mask=mask, erase_box=eb, textbox=tb, fill=fill, outline=outline,
                keep_alpha=job.get("keep_alpha", False))
    return info


def erase(im, info, method, grow=5):
    rgba = np.array(im)
    k = np.ones((grow, grow), np.uint8)
    x0, y0, x1, y1 = info["erase_box"]
    if method == "alpha" or (info["glyph"] and method not in ("inpaint", "inpainta", "maskalpha", "maskfill", "texfill")):
        rgba[y0:y1, x0:x1, :] = 0
    elif method == "flat":
        rgba[y0:y1, x0:x1, :3] = np.array(info["bg"]).astype(np.uint8)
        if not info["glyph"] and not info.get("keep_alpha"):
            rgba[y0:y1, x0:x1, 3] = 255
    elif method == "inpaint":
        m = cv2.dilate(info["mask"].astype(np.uint8) * 255, k)
        bgr = rgba[:, :, :3][:, :, ::-1].copy()
        out = cv2.inpaint(bgr, m, 4, cv2.INPAINT_TELEA)
        rgba[:, :, :3] = out[:, :, ::-1]
        if info["glyph"]:
            rgba[y0:y1, x0:x1, 3] = 0
    elif method == "inpainta":
        # lettering that sits ON artwork with its own alpha (icon buttons): inpaint colour AND the alpha plane,
        # so the glyph disappears instead of leaving a transparent hole in the icon.
        m = cv2.dilate(info["mask"].astype(np.uint8) * 255, k)
        bgr = rgba[:, :, :3][:, :, ::-1].copy()
        rgba[:, :, :3] = cv2.inpaint(bgr, m, 4, cv2.INPAINT_TELEA)[:, :, ::-1]
        a3 = cv2.cvtColor(rgba[:, :, 3].copy(), cv2.COLOR_GRAY2BGR)
        rgba[:, :, 3] = cv2.inpaint(a3, m, 4, cv2.INPAINT_TELEA)[:, :, 0]
    elif method == "maskfill":
        # paint the lettering out in the background colour, pixel by pixel, leaving the shape of the plate alone
        m = cv2.dilate(info["mask"].astype(np.uint8), k).astype(bool)
        rgba[m, :3] = np.array(info["bg"]).astype(np.uint8)
    elif method == "texfill":
        # IMAGES3C: textured / mottled paper. Each masked pixel takes the colour of the nearest unmasked ORIGINAL
        # pixel at a growing offset (up, down, left, right, diagonals; 4..61 px), so the paper keeps its grain
        # instead of the smooth lighter patch inpaint leaves; anything still unfilled gets TELEA inpaint.
        m = cv2.dilate(info["mask"].astype(np.uint8) * 255, k) > 0
        rgb = rgba[:, :, :3].copy()
        todo = m.copy()
        H, W = m.shape
        for d in range(4, 64, 3):
            if not todo.any():
                break
            for dx, dy in ((0, -d), (0, d), (-d, 0), (d, 0), (d, d), (-d, -d), (d, -d), (-d, d)):
                ys, xs = np.nonzero(todo)
                sy, sx = ys + dy, xs + dx
                ok = (sy >= 0) & (sy < H) & (sx >= 0) & (sx < W)
                ys, xs, sy, sx = ys[ok], xs[ok], sy[ok], sx[ok]
                good = ~m[sy, sx]
                rgb[ys[good], xs[good]] = rgba[sy[good], sx[good], :3]
                todo[ys[good], xs[good]] = False
        if todo.any():
            bgr = rgb[:, :, ::-1].copy()
            rgb = cv2.inpaint(bgr, todo.astype(np.uint8) * 255, 4, cv2.INPAINT_TELEA)[:, :, ::-1]
        rgba[:, :, :3] = rgb
    elif method == "maskalpha":
        m = cv2.dilate(info["mask"].astype(np.uint8), k).astype(bool)
        rgba[m, 3] = 0
    else:
        raise RuntimeError("erase method %s" % method)
    return Image.fromarray(rgba, "RGBA")


def set_text(im, string, style, box, fill, outline, stroke, spacing=0, line_spacing=1.0, caps=False, max_size=0, align="center"):
    font, index = FONTS[style]
    if caps:
        string = string.upper()
    lines = string.split("\n")
    spec = {"string": " ".join(lines), "font": font, "font_index": index, "size": 0, "box": box, "max_size": max_size,
            "color": fill, "align": align, "valign": "middle", "spacing": spacing, "line_spacing": line_spacing}
    if outline is not None and stroke:
        spec["stroke"] = stroke
        spec["stroke_color"] = outline
    if len(lines) > 1:
        # explicit line breaks: fit each line separately at one common size
        return draw_multiline(im, lines, spec)
    return T.draw_text(im, spec)


def draw_multiline(im, lines, spec):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    box = spec["box"]
    bw, bh = box[2] - box[0], box[3] - box[1]
    best = None
    for s in range(6, int(spec.get("max_size") or 0) + 1 if spec.get("max_size") else 200):
        font = ImageFont.truetype(spec["font"], s, index=spec.get("font_index", 0))
        asc, desc = font.getmetrics()
        lh = (asc + desc) * spec.get("line_spacing", 1.0)
        widest = max(T.tlen(d, l, font) + spec.get("spacing", 0) * max(0, len(l) - 1) for l in lines)
        if widest > bw or lh * len(lines) > bh:
            break
        best = (font, lh)
    if best is None:
        raise RuntimeError("multiline text does not fit: %r" % lines)
    font, lh = best
    y = box[1] + (bh - lh * len(lines)) / 2
    for l in lines:
        wl = T.tlen(d, l, font)
        x = box[0] if spec.get("align") == "left" else (
            box[2] - wl if spec.get("align") == "right" else box[0] + (bw - wl) / 2)
        T.draw_runs(d, (x, y), l, font, fill=spec["color"], stroke_width=spec.get("stroke", 0),
                    stroke_fill=spec.get("stroke_color", "#000000"))
        y += lh
    im.alpha_composite(layer)
    return font.size, lines


def word_boxes(info, n_words, gap=10, explicit=None):
    if explicit:
        out = []
        for x0, y0, x1, y1 in explicit:
            sub = info["mask"][y0:y1, x0:x1]
            bb = bbox(sub)
            if bb is None:
                raise RuntimeError("no lettering inside word box %s" % [x0, y0, x1, y1])
            out.append([x0 + bb[0], y0 + bb[1], x0 + bb[2], y0 + bb[3]])
        return out
    m = info["mask"].astype(np.uint8)
    merged = cv2.dilate(m, np.ones((1, gap * 2 + 1), np.uint8))
    n, lab, stats, cent = cv2.connectedComponentsWithStats(merged, connectivity=8)
    boxes = []
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < 12:
            continue
        sub = info["mask"][y:y + h, x:x + w]
        bb = bbox(sub)
        boxes.append([x + bb[0], y + bb[1], x + bb[2], y + bb[3]])
    # reading order: rows by y centre, then x
    boxes.sort(key=lambda b: (b[1] + b[3]) / 2)
    rows = []
    for b in boxes:
        cy = (b[1] + b[3]) / 2
        if rows and abs(cy - rows[-1][0]) < (b[3] - b[1]) * 0.8:
            rows[-1][1].append(b)
        else:
            rows.append([cy, [b]])
    ordered = []
    for cy, bs in rows:
        ordered += sorted(bs, key=lambda b: b[0])
    if len(ordered) != n_words:
        raise RuntimeError("found %d word boxes, expected %d: %s" % (len(ordered), n_words, ordered))
    return ordered


def redness(rgb):
    r = rgb[:, :, 0].astype(int) - np.maximum(rgb[:, :, 1], rgb[:, :, 2]).astype(int)
    return np.clip(r, 0, 255).astype(np.uint8)


def match_words(comp_rgba, matches):
    comp_red = redness(comp_rgba[:, :, :3])
    found = []
    for path, string in matches:
        s_rgba = np.array(Image.open(PNG_DIR + path).convert("RGBA"))
        sb = bbox(s_rgba[:, :, 3] > 128)
        s_rgba = s_rgba[sb[1]:sb[3], sb[0]:sb[2]]
        t_red = redness(s_rgba[:, :, :3]) * (s_rgba[:, :, 3] > 128)
        best = (-1, None, None)
        H, W = comp_red.shape
        for sc in (1.0, 0.9, 0.8, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3):
            tw, th = int(t_red.shape[1] * sc), int(t_red.shape[0] * sc)
            if tw < 8 or th < 8 or tw >= W or th >= H:
                continue
            t = cv2.resize(t_red.astype(np.uint8), (tw, th), interpolation=cv2.INTER_AREA)
            # unmasked normalised cross-correlation on the redness maps: background is 0 in both
            res = cv2.matchTemplate(comp_red, t, cv2.TM_CCOEFF_NORMED)
            _, mx, _, loc = cv2.minMaxLoc(res)
            if mx > best[0]:
                best = (mx, [loc[0], loc[1], loc[0] + tw, loc[1] + th], sc)
        found.append((string, best[1], best[0], best[2]))
    return found


def preview_pair(before, after, label, font):
    w = before.size[0] + after.size[0] + 24
    h = max(before.size[1], after.size[1]) + 22
    canvas = Image.new("RGB", (max(w, 320), h), (52, 52, 52))
    d = ImageDraw.Draw(canvas)
    d.text((4, 2), label, fill=(255, 255, 0), font=font)
    canvas.paste(before.convert("RGB"), (4, 20), before)
    canvas.paste(after.convert("RGB"), (before.size[0] + 20, 20), after)
    return canvas


PREVIEW_MAX_W = 1600   # previews wider than this are scaled down (IMAGES3C: the checker's image reader refused the big sheets)


def _fit_w(im):
    if im.size[0] <= PREVIEW_MAX_W:
        return im
    return im.resize((PREVIEW_MAX_W, max(1, round(im.size[1] * PREVIEW_MAX_W / im.size[0]))), Image.LANCZOS)


def write_previews(n, job, pairs, font_small):
    """<nn>-<id>.png = all before | after pairs stacked; for flip-animation jobs (id ends in -flip) the stacked
    sheet is replaced by a 4-column grid of the frames and every frame also gets its own <nn>-<id>-<kk>.png."""
    head = "%02d %s  [%s / %s]  screen: %s" % (n, job["id"], job["style"], FONTS[job["style"]][0].split("/")[-1], job["screen"])
    base = "%02d-%s" % (n, job["id"])
    if job["id"].endswith("-flip") and len(pairs) > 1:
        cols = 4
        cw = PREVIEW_MAX_W // cols
        thumbs = [p.resize((cw, max(1, round(p.size[1] * cw / p.size[0]))), Image.LANCZOS) for p in pairs]
        rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
        h = 24 + sum(max(t.size[1] for t in r) for r in rows)
        sheet = Image.new("RGB", (cw * cols, h), (30, 30, 30))
        ImageDraw.Draw(sheet).text((4, 4), head + "  (grid; one file per frame follows)", fill=(120, 220, 255), font=font_small)
        y = 24
        for r in rows:
            for i, t in enumerate(r):
                sheet.paste(t, (i * cw, y))
            y += max(t.size[1] for t in r)
        sheet.save(PREVIEW + base + ".png")
        for k, p in enumerate(pairs):
            fr = Image.new("RGB", (p.size[0], p.size[1] + 24), (30, 30, 30))
            ImageDraw.Draw(fr).text((4, 4), "%s  frame %d/%d" % (head, k + 1, len(pairs)), fill=(120, 220, 255), font=font_small)
            fr.paste(p, (0, 24))
            _fit_w(fr).save(PREVIEW + "%s-%02d.png" % (base, k + 1))
        return
    w = max(p.size[0] for p in pairs)
    h = sum(p.size[1] for p in pairs) + 24
    sheet = Image.new("RGB", (w, h), (30, 30, 30))
    ImageDraw.Draw(sheet).text((4, 4), head, fill=(120, 220, 255), font=font_small)
    y = 24
    for p in pairs:
        sheet.paste(p, (0, y))
        y += p.size[1]
    _fit_w(sheet).save(PREVIEW + base + ".png")


def write_index():
    """index.html over every preview file present for this job module (not only the jobs of this run)."""
    files = set(os.listdir(PREVIEW))
    with open(PREVIEW + "index.html", "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>picture batch previews</title>'
                '<style>body{background:#222;color:#ddd;font-family:Segoe UI,sans-serif;padding:16px}img{display:block;margin:6px 0 24px;max-width:100%}</style></head><body>')
        f.write("<h1>Picture batch: before | after per job</h1>")
        for n, job in enumerate(JOBS):
            base = "%02d-%s" % (n, job["id"])
            names = sorted(x for x in files if x == base + ".png" or (x.startswith(base + "-") and x[len(base) + 1:-4].isdigit()))
            if not names:
                continue
            f.write("<h3>%s</h3><p>%s</p>" % (html.escape(job["id"]), html.escape(job.get("note", ""))))
            for name in names:
                f.write("<img src=\"%s\" loading=\"lazy\">" % name)
        f.write("</body></html>")


def process_item(job, path, string, font_small, overrides=None):
    if overrides:
        job = dict(job, **overrides)
    src_png = PNG_DIR + path.replace(".gal", ".png")
    if job.get("chain"):
        # a second job on the same picture: start from the previous job's output, not the Japanese original
        chained = OUT_PNG + path.replace(".gal", ".png")
        if os.path.exists(chained):
            src_png = chained
    orig_gal = GAL_DIR + path
    if not os.path.exists(src_png):
        raise RuntimeError("missing source PNG %s" % src_png)
    im = Image.open(src_png).convert("RGBA")
    before = im.copy()
    style = job["style"]
    method = job.get("erase", "flat")
    notes = []
    if job.get("mode") == "words":
        info = analyze(im, job)
        boxes = word_boxes(info, len(job["words"]), job.get("word_gap", 10), job.get("word_boxes"))
        out = im
        for i, (b, wstr) in enumerate(zip(boxes, job["words"])):
            sub = dict(info)
            pad = job.get("pad", 3)
            sub["erase_box"] = [max(0, b[0] - pad), max(0, b[1] - pad), min(info["w"], b[2] + pad), min(info["h"], b[3] + pad)]
            sub_mask = np.zeros_like(info["mask"])
            sub_mask[b[1]:b[3], b[0]:b[2]] = info["mask"][b[1]:b[3], b[0]:b[2]]
            sub["mask"] = sub_mask
            out = erase(out, sub, method, job.get("mask_grow", 5))
            # room: half the gap to the neighbours on the same row
            left = max(0, b[0] - 14)
            right = min(info["w"], b[2] + 14)
            for ob in boxes:
                if ob is b:
                    continue
                if abs((ob[1] + ob[3]) / 2 - (b[1] + b[3]) / 2) < (b[3] - b[1]):
                    if ob[2] <= b[0]:
                        left = max(left, (ob[2] + b[0]) // 2 + 1)
                    elif ob[0] >= b[2]:
                        right = min(right, (ob[0] + b[2]) // 2 - 1)
            gh = b[3] - b[1]
            py = max(2, int(0.22 * gh))
            tb = [left, max(0, b[1] - py), right, min(info["h"], b[3] + py)]
            size, _ = set_text(out, wstr, style, tb, job.get("color") or hexcol(info["fill"]),
                               job.get("stroke_color") or (hexcol(info["outline"]) if info["outline"] is not None else None),
                               job.get("stroke", 1 if info["outline"] is not None else 0), caps=job.get("caps", False), max_size=job.get("max_size", 0))
            notes.append("%s@%dpx" % (wstr, size))
        im = out
    elif job.get("mode") == "boxes":
        # pass 1: one mask for every word (box grown by `grow`, red pixels above `red_thr`, dilated), one inpaint
        arr = np.array(im)
        rgb_i = arr[:, :, :3].astype(int)
        red = redness(arr[:, :, :3]) > job.get("red_thr", 25)
        pink = (rgb_i[:, :, 0] > 150) & (rgb_i[:, :, 2] > 120) & (rgb_i[:, :, 1] < 200) & (rgb_i[:, :, 0] > rgb_i[:, :, 1] + 30)
        red = red | pink
        H, W = red.shape
        grow = job.get("grow", 12)
        m = np.zeros(red.shape, np.uint8)
        for entry in job["boxes"]:
            b = entry[1]
            x0, y0, x1, y1 = max(0, b[0] - grow), max(0, b[1] - grow), min(W, b[2] + grow), min(H, b[3] + grow)
            m[y0:y1, x0:x1] |= red[y0:y1, x0:x1].astype(np.uint8) * 255
        m = cv2.dilate(m, np.ones((9, 9), np.uint8))
        for x0, y0, x1, y1 in job.get("protect", []):  # art that must survive (the pink heart)
            m[y0:y1, x0:x1] = 0
        bgr = arr[:, :, :3][:, :, ::-1].copy()
        arr[:, :, :3] = cv2.inpaint(bgr, m, 6, cv2.INPAINT_TELEA)[:, :, ::-1]
        out = Image.fromarray(arr, "RGBA")
        # pass 2: set every word
        for entry in job["boxes"]:
            # a box may carry its own colour: (text, box) or (text, box, "#rrggbb")
            wstr, b = entry[0], entry[1]
            col = entry[2] if len(entry) > 2 else job.get("color", "#fb0201")
            size, _ = set_text(out, wstr, style, b, col, job.get("stroke_color", "#ffffff"),
                               job.get("stroke", 1), caps=job.get("caps", False), max_size=job.get("max_size", 0))
            notes.append("%s@%dpx" % (wstr, size))
        im = out
    elif job.get("mode") == "match":
        found = match_words(np.array(im), job["match"])
        rgba = np.array(im)
        red = redness(rgba[:, :, :3]) > 60
        out = im
        for wstr, b, score, sc in found:
            if b is None or score < 0.45:
                notes.append("%s: NO MATCH (%.2f)" % (wstr, score))
                continue
            m = np.zeros(red.shape, np.uint8)
            m[b[1]:b[3], b[0]:b[2]] = red[b[1]:b[3], b[0]:b[2]].astype(np.uint8) * 255
            m = cv2.dilate(m, np.ones((7, 7), np.uint8))
            arr = np.array(out)
            bgr = arr[:, :, :3][:, :, ::-1].copy()
            arr[:, :, :3] = cv2.inpaint(bgr, m, 5, cv2.INPAINT_TELEA)[:, :, ::-1]
            out = Image.fromarray(arr, "RGBA")
            gh = b[3] - b[1]
            grow = int(0.35 * (b[2] - b[0]))
            tb = [max(0, b[0] - grow), max(0, b[1] - 2), min(rgba.shape[1], b[2] + grow), min(rgba.shape[0], b[3] + 2)]
            size, _ = set_text(out, wstr, style, tb, job.get("color", "#d40000"), job.get("stroke_color", "#5a0000"),
                               job.get("stroke", 1), caps=job.get("caps", False), max_size=job.get("max_size", 0))
            notes.append("%s@%dpx(%.2f,x%.2f)" % (wstr, size, score, sc))
        im = out
    elif job.get("mode") == "lines":
        # a rebuilt text panel: erase inside each named box only, then set one English string per box, left aligned
        info = analyze(im, job)
        out = im
        fill = job.get("color") or hexcol(info["fill"])
        outline = job.get("stroke_color")
        src_arr = np.array(im)
        rules = None
        if job.get("text_only"):
            # forms: drop the table rules from the lettering mask (long straight runs), so a box may span a cell
            # and only glyphs are erased; the rule pixels are restored from the source after erasing
            m8 = info["mask"].astype(np.uint8)
            rl = job.get("rule_len", (60, 40))
            hr = cv2.morphologyEx(m8, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (rl[0], 1)))
            vr = cv2.morphologyEx(m8, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, rl[1])))
            rules = (hr | vr).astype(bool)
            info["mask"] = info["mask"] & ~rules
        # IMAGES3 2026-10-01: a line is (text, box) or (text, box, opts). opts: erase = list of boxes to erase
        # instead of [box] ([] = erase nothing); bg = flat fill colour for this line; method = erase method for
        # this line; mask_color = [rmin,rmax,gmin,gmax,bmin,bmax] glyph mask for inpaint / maskfill in this line;
        # style / color / max_size / align / line_spacing per line; rot = degrees (90 = reads bottom-up,
        # -90 = reads top-down; the box is the on-page box); ellipse = [x0,y0,x1,y1] drawn after the text (a
        # hand-drawn choice circle). Job key erase_first = erase every line before setting any text.
        # Job key protect = boxes copied back from the job's source picture at the end (a sticker over the text).

        def line_parts(entry):
            return entry[0], entry[1], (entry[2] if len(entry) > 2 else {})

        def erase_line(img, bx, o):
            for eb in o.get("erase", [bx]):
                sub = dict(info)
                sub["erase_box"] = list(eb)
                if o.get("mask_color"):
                    t = o["mask_color"]
                    rgb = np.array(img)[:, :, :3]
                    m = ((rgb[:, :, 0] >= t[0]) & (rgb[:, :, 0] <= t[1]) & (rgb[:, :, 1] >= t[2]) & (rgb[:, :, 1] <= t[3])
                         & (rgb[:, :, 2] >= t[4]) & (rgb[:, :, 2] <= t[5]))
                else:
                    m = info["mask"]
                sm = np.zeros_like(info["mask"])
                sm[eb[1]:eb[3], eb[0]:eb[2]] = m[eb[1]:eb[3], eb[0]:eb[2]]
                sub["mask"] = sm
                if o.get("bg"):
                    c = o["bg"]
                    sub["bg"] = np.array([int(c[i:i + 2], 16) for i in (1, 3, 5)] if isinstance(c, str) else c)
                img = erase(img, sub, o.get("method", method), o.get("mask_grow", job.get("mask_grow", 5)))
            return img

        def set_line(img, text, bx, o):
            st = o.get("style", style)
            kw = dict(line_spacing=o.get("line_spacing", job.get("line_spacing", 1.0)), caps=job.get("caps", False),
                      max_size=o.get("max_size", job.get("max_size", 0)), align=o.get("align", job.get("align", "left")))
            col = o.get("color", fill)
            if o.get("rot") and abs(o["rot"]) != 90:
                # any other angle: the text runs along the box diagonal band, rot_h px tall, centred in the box
                w, h = bx[2] - bx[0], bx[3] - bx[1]
                tw, th = int((w * w + h * h) ** 0.5), int(o.get("rot_h", h * 0.4))
                layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
                size, _ = set_text(layer, text, st, [0, 0, tw, th], col, outline, job.get("stroke", 0), **dict(kw, align="center"))
                layer = layer.rotate(o["rot"], expand=True, resample=Image.BICUBIC)
                img.alpha_composite(layer, (int((bx[0] + bx[2] - layer.size[0]) / 2), int((bx[1] + bx[3] - layer.size[1]) / 2)))
            elif o.get("rot"):
                w, h = bx[2] - bx[0], bx[3] - bx[1]
                layer = Image.new("RGBA", (h, w), (0, 0, 0, 0))
                size, _ = set_text(layer, text, st, [0, 0, h, w], col, outline, job.get("stroke", 0), **kw)
                layer = layer.rotate(o["rot"], expand=True)
                img.alpha_composite(layer, (bx[0], bx[1]))
            else:
                size, _ = set_text(img, text, st, list(bx), col, outline, job.get("stroke", 0), **kw)
            if o.get("ellipse"):
                ImageDraw.Draw(img).ellipse(o["ellipse"], outline=col, width=o.get("ellipse_w", 2))
            notes.append("%s@%dpx" % (text[:14], size))
            return img

        if job.get("erase_first"):
            for entry in job["lines"]:
                text, bx, o = line_parts(entry)
                out = erase_line(out, bx, o)
            if rules is not None:
                # IMAGES3C: a line with no_rules=True keeps its erase boxes out of the rule restore (big
                # headline / masthead glyph strokes are long straight runs and were being put back as "rules")
                rules = rules.copy()
                for entry in job["lines"]:
                    _t, _bx, _o = line_parts(entry)
                    if _o.get("no_rules"):
                        for eb in _o.get("erase", [_bx]):
                            rules[eb[1]:eb[3], eb[0]:eb[2]] = False
                arr = np.array(out)
                arr[rules] = src_arr[rules]
                out = Image.fromarray(arr, "RGBA")
            for entry in job["lines"]:
                text, bx, o = line_parts(entry)
                if text:
                    out = set_line(out, text, bx, o)
        else:
            for entry in job["lines"]:
                text, bx, o = line_parts(entry)
                out = erase_line(out, bx, o)
                if text:
                    out = set_line(out, text, bx, o)
        if job.get("protect"):
            arr = np.array(out)
            for x0, y0, x1, y1 in job["protect"]:
                arr[y0:y1, x0:x1] = src_arr[y0:y1, x0:x1]
            out = Image.fromarray(arr, "RGBA")
        im = out
    elif job.get("mode") == "asis":
        # IMAGES3: the picture was built by a helper (refdoc_flip.py / refdoc_overview.py build) into the out
        # PNG; chain=True picks it up and this mode only encodes, verifies and ships it.
        if not job.get("chain") or src_png == PNG_DIR + path.replace(".gal", ".png"):
            raise RuntimeError("asis needs chain=True and a built out PNG")
        before = Image.open(PNG_DIR + path.replace(".gal", ".png")).convert("RGBA")
        notes.append("as built")
    elif job.get("mode") == "blank":
        # erase the lettering and set nothing (shatter frames: the shards keep their shape, the Japanese goes)
        info = analyze(im, job)
        im = erase(im, info, method, job.get("mask_grow", 5))
        notes.append("blanked %s" % (info["erase_box"],))
    elif job.get("mode") == "rotated":
        # lettering set at an angle (corner ribbons): render horizontally on a scratch layer, rotate, paste
        info = analyze(im, job)
        im = erase(im, info, method, job.get("mask_grow", 5))
        # one rotated string (rot_box / rot_center) or several (rot_lines = [(text, [w,h], [cx,cy], max_size), ...])
        rot_lines = job.get("rot_lines") or [(string, job["rot_box"], job["rot_center"], job.get("max_size", 0))]
        for text, (sw, sh), (cx, cy), msz in rot_lines:
            layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
            size, _ = set_text(layer, text, style, [0, 0, sw, sh], job.get("color") or hexcol(info["fill"]),
                               job.get("stroke_color") or (hexcol(info["outline"]) if info["outline"] is not None else None),
                               job.get("stroke", 0), caps=job.get("caps", False), max_size=msz or job.get("max_size", 0))
            layer = layer.rotate(job.get("rotate", 45), resample=Image.BICUBIC, expand=True)
            im.alpha_composite(layer, (int(cx - layer.size[0] / 2), int(cy - layer.size[1] / 2)))
            notes.append("%s@%dpx rot%d" % (text[:12], size, job.get("rotate", 45)))
    else:
        info = analyze(im, job)
        im = erase(im, info, method, job.get("mask_grow", 5))
        fill = job.get("color") or hexcol(info["fill"])
        outline = job.get("stroke_color") or (hexcol(info["outline"]) if info["outline"] is not None else None)
        stroke = job.get("stroke", 1 if (info["outline"] is not None or info["glyph"]) else 0)
        if outline is None and stroke:
            outline = "#000000" if sum(info["fill"]) > 380 else "#ffffff"
        size, lines = set_text(im, string, style, job.get("textbox") or info["textbox"], fill, outline, stroke,
                               spacing=job.get("spacing", 0), line_spacing=job.get("line_spacing", 1.0),
                               caps=job.get("caps", False), max_size=job.get("max_size", 0))
        notes.append("%dpx box=%s fill=%s%s" % (size, info["textbox"], fill, (" outline=" + outline) if stroke else ""))
    out_png = OUT_PNG + path.replace(".gal", ".png")
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    im.save(out_png)
    out_gal = OUT_GAL + path
    os.makedirs(os.path.dirname(out_gal), exist_ok=True)
    # small pictures go zip (pixel exact); big photo-like ones keep the original JPEG mode. Both load in-game.
    comp = "zip" if im.size[0] * im.size[1] <= 200000 else "keep"
    GW.write_gal(orig_gal, out_png, out_gal, comp, None, 0)
    back = Image.open(out_gal)
    back.load()
    ref = im.convert(back.mode)
    diff = np.abs(np.array(back).astype(int) - np.array(ref).astype(int))
    verify = "verify mean %.2f max %d" % (diff.mean(), diff.max())
    if diff.mean() > 6.0:
        raise RuntimeError("verify failed for %s: %s" % (path, verify))
    prev = preview_pair(before, im, path.split("/")[-1] + "   " + "; ".join(notes) + "   " + verify, font_small)
    return out_gal, prev, "; ".join(notes) + "; " + verify


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default=_JOBS_MODULE, help="job module under tools/images (jobs_part1, jobs_tierb, ...)")
    ap.add_argument("--only", default="", help="comma list of job ids")
    ap.add_argument("--styles", default="", help="comma list of styles to process")
    ap.add_argument("--no-ship", action="store_true", help="render + encode + preview only; no copy to the EN folder, no ship list")
    ap.add_argument("--dry", action="store_true", help="analysis + preview only; no encode")
    ap.add_argument("--previews-only", action="store_true",
                    help="no rendering: rebuild the before | after previews from the source PNG and the existing out PNG")
    args = ap.parse_args()
    only = set(s for s in args.only.split(",") if s)
    styles = set(s for s in args.styles.split(",") if s)
    os.makedirs(PREVIEW, exist_ok=True)
    try:
        font_small = ImageFont.truetype(F + "segoeui.ttf", 12)
    except Exception:
        font_small = ImageFont.load_default()
    shipped, previews, failures, log_rows = [], [], [], []
    for n, job in enumerate(JOBS):
        if only and job["id"] not in only:
            continue
        if styles and job["style"] not in styles:
            continue
        pairs = []
        if args.previews_only:
            for item in job["items"]:
                src = PNG_DIR + item[0].replace(".gal", ".png")
                out = OUT_PNG + item[0].replace(".gal", ".png")
                if os.path.exists(src) and os.path.exists(out):
                    pairs.append(preview_pair(Image.open(src).convert("RGBA"), Image.open(out).convert("RGBA"),
                                              item[0].split("/")[-1], font_small))
            if pairs:
                write_previews(n, job, pairs, font_small)
            print("PREVIEW %-24s %d pictures" % (job["id"], len(pairs)))
            continue
        for item in job["items"]:
            path, string = item[0], item[1]
            overrides = item[2] if len(item) > 2 else None
            try:
                out_gal, prev, note = process_item(job, path, string, font_small, overrides)
                pairs.append(prev)
                if not args.no_ship:
                    dst = EN_DIR + path
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copyfile(out_gal, dst)
                    shipped.append(path)
                print("OK  %-28s %-48s %s" % (job["id"], path.split("/")[-1], note))
            except Exception as e:
                failures.append((job["id"], path, str(e)))
                print("FAIL %-27s %-48s %s" % (job["id"], path.split("/")[-1], e))
        if pairs:
            write_previews(n, job, pairs, font_small)
        if job.get("new"):
            for item in job["items"]:
                if item[1]:
                    log_rows.append((job["id"], item[0], item[1]))
            for path, string in job.get("match", []):
                log_rows.append((job["id"], path, string))
            for rl in job.get("rot_lines", []):
                log_rows.append((job["id"], job["items"][0][0], rl[0]))
            if job.get("mode") == "lines":   # jobs_part1 uses `lines` as an int line-count hint; only the
                for _entry in job["lines"]:  # mode="lines" jobs carry (text, box[, opts]) tuples
                    lstr = _entry[0]
                    if lstr:
                        log_rows.append((job["id"], job["items"][0][0], lstr))
            for wstr in job.get("words", []):
                log_rows.append((job["id"], job["items"][0][0], wstr))
    write_index()
    if shipped and not args.no_ship:
        current = open(SHIP_LIST, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in current else "\n"  # keep the file's line endings (CRLF since 2026-10-01; IMAGES7 found v1 stripped them)
        lines = current.splitlines()
        if "# pictures" not in current:
            lines.append("# pictures (image lane, 2026-09-26; work/グラフィック/... = translated GaleX pictures; loose-file override)")
        existing = set(l.split("#")[0].strip() for l in lines)
        for p in shipped:
            if p not in existing:
                lines.append(p)
                existing.add(p)
        open(SHIP_LIST, "w", encoding="utf-8", newline="").write(nl.join(lines) + nl)
    if log_rows:
        os.makedirs(os.path.dirname(TL_LOG), exist_ok=True)
        new_file = not os.path.exists(TL_LOG)
        with open(TL_LOG, "a", encoding="utf-8") as f:
            if new_file:
                f.write("# tl-log-IMAGES.md - first translations of picture text (image lane, 2026-09-26)\n\n"
                        "Wording that already existed in patch/labels-*.tsv, tsv-en/ or GLOSSARY was reused verbatim and is not listed.\n\n"
                        "| job | picture | English | note |\n|---|---|---|---|\n")
            seen = set()
            already = "" if new_file else open(TL_LOG, encoding="utf-8").read()
            for jid, path, string in log_rows:
                key = (jid, string)
                if key in seen:
                    continue
                seen.add(key)
                job = next(j for j in JOBS if j["id"] == jid)
                row = "| %s | %s | %s | %s |" % (jid, path.split("/")[-1], string.replace("\n", " / "), job.get("note", ""))
                if row in already:
                    continue
                f.write(row + "\n")
    print("\nshipped %d files, %d failures, previews in %s" % (len(shipped), len(failures), PREVIEW))
    for fjob, fpath, msg in failures:
        print("  FAIL", fjob, fpath, msg)


if __name__ == "__main__":
    main()
