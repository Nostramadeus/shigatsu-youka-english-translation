"""refnode_boxes.py - object-reference check points (リファレンスターゲット LEFT/TOP/WIDTH/HEIGHT) vs the English
picture text (lane 2, 2026-11-03, friend's report item 7).

The viewer (0000001E.lsb idx 189) makes one clickable highlight box per check point on rrr<ID>/0.gal with
    left = nLEFT, top = nTOP, width = nWIDTH - nLEFT, height = nHEIGHT - nTOP
so the four columns are really x1, y1, x2, y2 in picture pixels; a point whose 特殊処理 contains 裏 gets no box.
The Japanese values mark Japanese text. Our English pictures re-set the text, sometimes elsewhere (reflowed memos,
longer or shorter lines, a phrase at another x), so a box can sit next to its text.

For every point this tool takes the JAPANESE rectangle (orig/データベース, never the edited table), finds the
English text that translates the Japanese inside it, and lays that text out with the renderer's own code
(batch.set_text: same fonts, boxes, fit, wrap; draw_runs is recorded to get each wrapped line's position), so the
English box is the box of the pixels the shipped picture really has. It prints per reference and point: the
Japanese rectangle, the current table rectangle, the English text box, the status and the rectangle to write.

    SY_JOBS=jobs_refdocs PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --with pylivemaker --with numpy \
        --with opencv-python-headless python tools/images/refnode_boxes.py [--tsv FILE] [--write] [IDS...]

Which English text: MAP[(ref, point)] when present (read off the Japanese picture: the Japanese inside the
rectangle = these English lines / this English phrase), else every job line whose box lies at least MIN_OVER inside
the Japanese rectangle (lines-mode boxes are the Japanese line positions). MAP values:
    [(job id, line index, phrase or None), ...]  phrase = the English words to mark inside that line (None = line)
    "keep"   the rectangle marks no re-set text (picture area, untouched Japanese-free art): keep the Japanese one
Status: OK = the Japanese rectangle already holds the English box (TOL px); FIX = table still needs the English box
+ PAD (--write); FIXED = table holds it; KEEP = no
re-set text under the point; HIDDEN = 裏 point, no box in game; NOPIC = no English picture.
--write puts every FIX rectangle into tsv-en/リファレンスターゲット.tsv (then run tools/build_tsv.py on it).
"""
import csv
import os
import sys

import numpy as np

os.environ.setdefault("SY_JOBS", "jobs_refdocs")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import batch as B  # noqa: E402  (chdir to the project root)
import typeset_ui as T  # noqa: E402
from PIL import Image  # noqa: E402

TABLE = "tsv-en/リファレンスターゲット.tsv"
ORIG = "orig/データベース/リファレンスターゲット.tsv"
D = "グラフィック/リファレンス/リファレンス詳細/"
MODULES = ["jobs_refdocs"]
MIN_OVER = 0.5
TOL = 3
PAD = 3

from refnode_map import MAP  # noqa: E402  (the per-point content mapping, kept in its own file)


def read_rows(path, enc):
    return list(csv.reader(open(path, encoding=enc, newline=""), delimiter="\t"))


def points(row):
    out = []
    for k in range(10):
        b = 6 + k * 11
        seg = row[b:b + 11]
        if len(seg) < 11:
            continue
        v = [int(x) if x.strip() else 0 for x in seg[4:8]]
        if sum(v) > 0:
            out.append((k + 1, v, seg[10]))
    return out


def job_lines(rid):
    """[(job id, index, text, box, opts, job)] for every lines-mode job on rrr<rid>/0.gal, in job order."""
    path = D + "rrr%s/0.gal" % rid
    res = []
    for m in MODULES:
        for job in __import__(m).JOBS:
            if job.get("mode") != "lines" or not any(it[0] == path for it in job.get("items", [])):
                continue
            for i, e in enumerate(job["lines"]):
                res.append((job["id"], i, e[0], list(e[1]), (e[2] if len(e) > 2 else {}), job))
    return res


_REC = []
_draw_runs = T.draw_runs


def _recording_draw_runs(d, xy, text, font, **kw):
    _REC.append((xy, text, font))
    return _draw_runs(d, xy, text, font, **kw)


T.draw_runs = _recording_draw_runs


def alpha_box(layer):
    bb = layer.getchannel("A").point(lambda a: 255 if a > 40 else 0).getbbox()
    return list(bb) if bb else None


def ink_box(size, text, box, o, job, phrase=None):
    """English ink box of one job line (or of `phrase` inside it), drawn by the renderer's own code."""
    if not text:
        return None
    if o.get("rot"):
        return list(box)
    st = o.get("style", job.get("style"))
    kw = dict(line_spacing=o.get("line_spacing", job.get("line_spacing", 1.0)), caps=job.get("caps", False),
              max_size=o.get("max_size", job.get("max_size", 0)), align=o.get("align", job.get("align", "left")))
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    del _REC[:]
    B.set_text(layer, text, st, list(box), "#000000", None, 0, **kw)
    if phrase is None:
        return alpha_box(layer)
    rec = list(_REC)
    norm = text.replace("\n", " ")
    if job.get("caps"):
        norm, phrase = norm.upper(), phrase.upper()
    joined = " ".join(r[1] for r in rec)
    if joined != norm:
        raise SystemExit("cannot map phrase (wrapped text differs): %r" % text)
    start = norm.find(phrase)
    if start < 0 or norm.find(phrase, start + 1) >= 0:
        raise SystemExit("phrase %r not found exactly once in %r" % (phrase, text))
    end = start + len(phrase)
    from PIL import ImageDraw
    part_layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(part_layer)
    pos = 0
    for (x, y), line, font in rec:
        s, e = max(start, pos), min(end, pos + len(line))
        if s < e:
            px = x + T.tlen(d, line[:s - pos], font)
            _draw_runs(d, (px, y), line[s - pos:e - pos], font, fill="#000000")
        pos += len(line) + 1
    return alpha_box(part_layer)


def overlap(box, rect):
    x0, y0 = max(box[0], rect[0]), max(box[1], rect[1])
    x1, y1 = min(box[2], rect[2]), min(box[3], rect[3])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    return (x1 - x0) * (y1 - y0) / max(1, (box[2] - box[0]) * (box[3] - box[1]))


def union(boxes):
    boxes = [b for b in boxes if b]
    if not boxes:
        return None
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def inside(inner, outer, tol=TOL):
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol and inner[2] <= outer[2] + tol
            and inner[3] <= outer[3] + tol)


_EN = {}


def english_picture(rid):
    """the English picture as shipped: work/images/out PNG, else the shipped GAL decoded (35/50/59 have no out PNG)."""
    if rid not in _EN:
        out = "work/images/out/" + D + "rrr%s/0.png" % rid
        if os.path.exists(out):
            _EN[rid] = Image.open(out).convert("RGB")
        else:
            from pathlib import Path
            from gal_decode import open_gal
            im = open_gal(Path("work/" + D + "rrr%s/0.gal" % rid).read_bytes())
            im.load()
            _EN[rid] = im.convert("RGB")
    return _EN[rid]


def changed(rid, rect):
    """share of pixels inside rect that differ between the Japanese and the English picture."""
    jp = "work/images/png/" + D + "rrr%s/0.png" % rid
    if not os.path.exists(jp):
        return None
    a = np.asarray(Image.open(jp).convert("RGB"))[rect[1]:rect[3], rect[0]:rect[2]].astype(int)
    b = np.asarray(english_picture(rid))[rect[1]:rect[3], rect[0]:rect[2]].astype(int)
    return float((np.abs(a - b).max(2) > 40).mean()) if a.size else 0.0


def check(rid, jp_pts, cur_pts):
    jp_png = "work/images/png/" + D + "rrr%s/0.png" % rid
    shipped = os.path.exists("work/" + D + "rrr%s/0.gal" % rid)
    lines = job_lines(rid)
    size = Image.open(jp_png).size if os.path.exists(jp_png) else None
    by_key = {(jid, i): (text, box, o, job) for jid, i, text, box, o, job in lines}
    cur = {k: rect for k, rect, _ in cur_pts}
    out = []
    for k, rect, special in jp_pts:
        table = cur.get(k, rect)
        res = dict(point=k, jp=rect, table=table, special=special, members=[], en=None, how="")
        if "裏" in special:
            res.update(status="HIDDEN", new=table)
        elif not shipped or not lines or size is None:
            res.update(status="NOPIC" if not shipped else "NOJOB", new=table)
        else:
            m = MAP.get((rid, k))
            if m == "keep":
                res.update(status="KEEP", new=rect, how="map")
            else:
                if m is not None:
                    members = list(m)
                    res["how"] = "map"
                else:
                    members = [(jid, i, None) for jid, i, text, box, o, job in lines
                               if text and overlap(box, rect) >= MIN_OVER]
                    res["how"] = "overlap"
                boxes, phrase, with_jp = [], False, False
                for member in members:
                    if member == ("jp",):
                        with_jp = True
                        res["members"].append(("jp", 0, "(the Japanese rectangle: art / numerals kept)", rect))
                        continue
                    jid, i, ph = member
                    text, box, o, job = by_key[(jid, i)]
                    boxes.append(ink_box(size, text, box, o, job, ph))
                    phrase = phrase or ph is not None
                    res["members"].append((jid, i, text if ph is None else ph, boxes[-1]))
                en = union(boxes)
                res["en"] = en
                if en is None:
                    res.update(status="KEEP", new=rect)
                else:
                    new = [max(0, en[0] - PAD), max(0, en[1] - PAD), min(size[0], en[2] + PAD),
                           min(size[1], en[3] + PAD)]
                    if with_jp:
                        new = union([new, rect])
                    # a Japanese edge at 0 (picture edge) stays 0: the box still holds the English, and
                    # tools/build_tsv.py refuses a cell that was empty/0 in the source
                    new = [0 if rect[n] == 0 and n < 2 else new[n] for n in range(4)]
                    # whole English lines already inside the Japanese rectangle: keep it; a phrase is always marked
                    # tightly (the Japanese rectangle may span words the point does not mean)
                    good = inside(en, rect) and not phrase
                    res.update(status="OK" if good else "FIX", new=rect if good else new)
            res["partial"] = [(jid, i) for jid, i, text, box, o, job in lines
                              if text and 0.1 <= overlap(box, rect) < MIN_OVER] if res["how"] == "overlap" else []
            res["changed"] = changed(rid, rect)
        out.append(res)
    return out


def main():
    argv = sys.argv[1:]
    tsv_out = None
    if "--tsv" in argv:
        i = argv.index("--tsv")
        tsv_out = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    ids = [a for a in argv if not a.startswith("--")]
    cur_rows = {r[0]: r for r in read_rows(TABLE, "utf-8")[1:]}
    out_rows, writes, counts = [], {}, {}
    for jrow in read_rows(ORIG, "cp932")[1:]:
        rid = jrow[0]
        jp_pts = points(jrow)
        if not jp_pts or (ids and rid not in ids):
            continue
        crow = cur_rows[rid]
        print("== ref %s (display No.%s)" % (rid, jrow[1]))
        for r in check(rid, jp_pts, points(crow)):
            if r["status"] == "FIX" and r["new"] == r["table"]:
                r["status"] = "FIXED"   # the table already holds the English rectangle
            counts[r["status"]] = counts.get(r["status"], 0) + 1
            flag = ""
            if r.get("partial"):
                flag += " PARTIAL %s" % r["partial"]
            if r["status"] == "KEEP" and r["how"] == "overlap" and (r.get("changed") or 0) > 0.01:
                flag += " CHANGED-UNDER-KEEP %.2f" % r["changed"]
            print("  point %-2d %-6s JP %-22s table %-22s EN %-22s -> %s [%s]%s%s" % (
                r["point"], r["status"], r["jp"], r["table"], r["en"], r["new"], r["how"], flag,
                ("  (" + r["special"] + ")") if r["special"] else ""))
            for jid, i, text, bb in r["members"]:
                print("        %s#%d %r %s" % (jid, i, text[:70], bb))
            out_rows.append([rid, jrow[1], r["point"], r["status"], ",".join(map(str, r["jp"])),
                             ",".join(map(str, r["table"])), ",".join(map(str, r["en"])) if r["en"] else "",
                             ",".join(map(str, r["new"])), r["how"],
                             " / ".join(t[:60] for _, _, t, _ in r["members"])])
            if r["new"] != r["table"]:
                writes[(rid, r["point"])] = r["new"]
    if tsv_out:
        with open(tsv_out, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["ref", "display", "point", "status", "jp_rect", "table_rect", "en_box", "rect_to_write",
                        "how", "english_marked"])
            w.writerows(out_rows)
    print("SUMMARY", counts, "| table rectangles that differ from the computed one:", len(writes))
    if "--write" in sys.argv and writes:
        raw = open(TABLE, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(nl)
        for li in range(1, len(lines)):
            cells = lines[li].split("\t")
            for (rid, k), new in writes.items():
                if cells[0] == rid:
                    b = 6 + (k - 1) * 11 + 4
                    cells[b:b + 4] = [str(v) for v in new]
            lines[li] = "\t".join(cells)
        open(TABLE, "w", encoding="utf-8", newline="").write(nl.join(lines))
        print("wrote %d rectangles into %s" % (len(writes), TABLE))


if __name__ == "__main__":
    main()
