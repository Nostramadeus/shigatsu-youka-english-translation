"""Does the English fit the box it is drawn in?

    # scene text: every English cell of every shipped scene .lns, against the (標準) box
    PYTHONUTF8=1 uv run --no-project --python 3.12 --with pillow python tools/fit_audit.py scenes

    # UI: geometry + literal text of every Caption / BoxNew / MesNew in the shipped .lsb files
    PYTHONUTF8=1 uv run --no-project --python 3.12 --with pillow --with pylivemaker \
        python tools/fit_audit.py ui [ID ...]

Both write rows to work/fitaudit/findings.tsv (scenes writes findings-scenes.tsv, ui writes
findings-ui.tsv; `merge` concatenates them). Columns:

    file  index  box  font  size  capacity  measured  source  en_text[:60]  class

class = OK | TIGHT (>90% of capacity) | OVERFLOW.

------------------------------------------------------------------------------------
THE WIDTH MODEL, and why it is not just PIL
------------------------------------------------------------------------------------
LiveMaker does NOT advance by the font's own metrics. Every glyph gets an extra, constant
advance on top of its proportional width. Calibrated 2026-09-26 against eight line breaks
photographed in the running game (tools/harness/shots/fitaudit*, notes/FIT-AUDIT.md):

    advance(ch) = PIL_advance(ch, FONTHEIGHT, MS PMincho) + EXTRA_EM * FONTHEIGHT
    EXTRA_EM    = 0.15          (= 4.5 px at FONTHEIGHT 30)

EXTRA_EM = 0.15 reproduces all 8 observed breaks; 0.14 and 0.16 do not. The extra advance
is what PR_FONTBORDER=1 costs (tools/lsb_prop.py): the box is drawn glyph by glyph with a
border, so nothing is kerned and every glyph is padded.

Line pitch, calibrated on the same shots (13 lines in a 480 px text area at FONTHEIGHT 30,
PR_LINESPACE 4):

    pitch = 1.09 * FONTHEIGHT + PR_LINESPACE

Wrapping: the engine breaks at ASCII spaces and at U+3000, word-wrap style, and swallows
the breaking space at the start of the new line. Verified on shots/fitaudit/004.png and
shots/fitaudit4/009.png.

OVERFLOW does NOT mean text leaves the screen. The engine AUTO-PAGES: when a cell fills the
last visible line it waits for a click, clears the box and continues. Proof:
tools/harness/shots/fitaudit/008.png -> 010.png -> 012.png (1000 Latin characters, four
pages, nothing clipped). So for a MesNew, OVERFLOW = "the reader gets an unplanned extra
click in the middle of the line", not "text is lost". For a Caption (no auto-page) it is a
real clip.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from pathlib import Path

from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "work" / "fitaudit"
FONT_FILE = "C:/Windows/Fonts/msmincho.ttc"
FACE = {"ＭＳ Ｐ明朝": 1, "ＭＳ 明朝": 0, "MS PMincho": 1, "MS Mincho": 0}
EXTRA_EM = 0.15          # extra advance per glyph, in ems (calibrated, see docstring)
PITCH_EM = 1.09          # line pitch = PITCH_EM * FONTHEIGHT + PR_LINESPACE
TIGHT = 0.90

_fonts: dict[tuple[int, int], ImageFont.FreeTypeFont] = {}


def font(size: int, face: int = 1):
    key = (size, face)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILE, size, index=face)
    return _fonts[key]


def advance(s: str, size: int, face: int = 1) -> float:
    f = font(size, face)
    return f.getlength(s) + EXTRA_EM * size * len(s)


def pitch(size: int, linespace: int) -> float:
    return PITCH_EM * size + linespace


def wrap(text: str, width: float, size: int, face: int = 1) -> list[str]:
    """Greedy word wrap the way the engine does it: break at ASCII space / U+3000,
    swallow the breaking space, hard-break a word that is wider than the box."""
    lines: list[str] = []
    for para in text.split("\n"):
        cur = ""
        for token in re.findall(r"[^ \u3000]+[ \u3000]?", para):
            word = token.rstrip(" \u3000")
            cand = cur + token
            if advance(cand.rstrip(" \u3000"), size, face) <= width or not cur:
                cur = cand
                continue
            lines.append(cur.rstrip(" \u3000"))
            cur = token
        while advance(cur.rstrip(" \u3000"), size, face) > width and len(cur) > 1:
            # a single token longer than the box: cut it where it stops fitting
            n = len(cur)
            while n > 1 and advance(cur[:n], size, face) > width:
                n -= 1
            lines.append(cur[:n])
            cur = cur[n:]
        lines.append(cur.rstrip(" \u3000"))
    return lines


# ----------------------------------------------------------------------------------
# the message boxes. Geometry read out of メッセージボックス作成.lsb 2026-09-26; the
# BoxNew width/height are literals there and the MesNew insets are literal too, so these
# numbers are the file, not a guess. 13 MesNew = 7 live definitions + 6 FormatHist copies
# of the same seven geometries.
# ----------------------------------------------------------------------------------
BOXES = {
    # name:        (box_w, box_h, inset_l, inset_t, inset_r, inset_b, size, linespace)
    "(標準)":      (600, 500, 10, 10, 10, 10, 30, 4),
    "(編集用)":    (490, 104, 10, 10, 10, 10, 16, 6),
    "大文字用":    (960, 540, 10, 10, 10, 10, 60, 4),
    "電話":        (600, 500, 10, 10, 10, 10, 30, 4),
    "イベント用":  (630, 100, 20, 15, 20,  5, 20, 4),
    "リファレンス": (600, 200, 10, 10, 10, 10, 20, 1),
    "赤":          (600, 500, 10, 10, 10, 10, 30, 4),
}
STORY_BOX = "(標準)"     # what a scene script uses unless it calls for another


def box_capacity(name: str):
    bw, bh, il, it, ir, ib, size, ls = BOXES[name]
    w = bw - il - ir
    h = bh - it - ib
    return w, int(h // pitch(size, ls)), size, ls


# ----------------------------------------------------------------------------------
# scene pass
# ----------------------------------------------------------------------------------
TAG = re.compile(r"<[^>]*>")
CMD = re.compile(r"^\{.*\}$")


def cells(path: Path):
    """Yield (first_line_no, plain_text) per cell. A cell = text up to <PG>; <BR> is a
    hard line break inside it. Tags and {COMMANDS} are stripped; the [TN] translator
    notes are kept, they are drawn like any other text."""
    started = False
    buf: list[str] = []
    start = 0
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        s = raw.rstrip("\r")
        if not started:
            if "BEGIN DECOMPILED SCRIPT" in s:
                started = True
            continue
        if s.startswith(";") or CMD.match(s.strip()):
            continue
        page = "<PG>" in s
        s = s.replace("<BR>", "\x01")
        s = TAG.sub("", s)
        if s.strip() or "\x01" in s:
            if not buf:
                start = n
            buf.append(s)
        if page:
            text = "".join(buf).replace("\x01", "\n").strip("\n")
            if text.strip():
                yield start, text
            buf = []
    if buf:
        text = "".join(buf).replace("\x01", "\n").strip("\n")
        if text.strip():
            yield start, text


def scenes(argv):
    ids = argv or sorted({p.name.split("-")[0] for p in (ROOT / "lns-en").glob("*-*.lns")})
    w, maxlines, size, ls = box_capacity(STORY_BOX)
    rows = []
    per_file: dict[str, list[int]] = {}
    for sid in ids:
        for p in sorted((ROOT / "lns-en").glob("%s-*.lns" % sid)):
            for lineno, text in cells(p):
                lines = wrap(text, w, size)
                used = len(lines)
                cls = "OVERFLOW" if used > maxlines else (
                    "TIGHT" if used >= math.ceil(maxlines * TIGHT) else "OK")
                counts = per_file.setdefault(p.name, [0, 0, 0])
                counts[{"OK": 0, "TIGHT": 1, "OVERFLOW": 2}[cls]] += 1
                if cls != "OK":
                    rows.append([p.name, lineno, STORY_BOX, "ＭＳ Ｐ明朝", size,
                                 "%d lines x %dpx" % (maxlines, w), "%d lines" % used,
                                 "lns cell", text.replace("\n", " / ")[:60], cls])
    rows.sort(key=lambda r: (-int(r[6].split()[0]), r[0]))
    write(OUT / "findings-scenes.tsv", rows)
    tot = [sum(c[i] for c in per_file.values()) for i in range(3)]
    print("scene cells: OK %d  TIGHT %d  OVERFLOW %d   (box %s: %d lines x %d px)"
          % (tot[0], tot[1], tot[2], STORY_BOX, maxlines, w))
    print("per file (only files with a finding):")
    for name in sorted(per_file):
        ok, tight, over = per_file[name]
        if tight or over:
            print("  %-34s OK %4d  TIGHT %3d  OVERFLOW %3d" % (name, ok, tight, over))
    print("worst 20:")
    for r in rows[:20]:
        print("  %-34s line %-5s %-9s %-8s %s" % (r[0], r[1], r[6], r[9], r[8][:44]))
    return 0


# ----------------------------------------------------------------------------------
# UI pass
# ----------------------------------------------------------------------------------
INTLIT = re.compile(r"^-?\d+$")


def num(v, default=None):
    s = "" if v is None else str(v).strip()
    return int(s) if INTLIT.match(s) else default


def strlit(v):
    """The string LITERAL behind a property, or None when it is an expression.
    pylivemaker prints an expression such as `"No." ++ DBGetStr("表示")` with the same
    outer quotes as a literal, so anything with a `++` or a call in it is refused."""
    s = "" if v is None else str(v)
    m = re.fullmatch(r'"(.*)"', s, re.DOTALL)
    if not m:
        return None
    inner = m.group(1)
    if "++" in inner or re.search(r'\w+\(', inner) or '""' in inner:
        return None
    return inner


def textlines(s: str) -> list[str]:
    """PR_TEXT holds real CR LF, which pylivemaker prints as the two-character escape."""
    return re.split(r"\\r\\n|\r\n|\n", s)


def ui(argv):
    from livemaker.lsb import LMScript
    ship = [l.split("#")[0].strip() for l in
            (ROOT / "tools" / "ship-list.txt").read_text(encoding="utf-8").splitlines()]
    files = [ROOT / "work" / f for f in ship if f.endswith(".lsb")]
    if argv:
        files = [f for f in files if f.stem in argv or f.name in argv]
    rows = []
    n_ok = n_tight = n_over = n_unmeasured = 0
    for path in files:
        if not path.exists():
            continue
        try:
            lsb = LMScript.from_file(str(path))
        except Exception as e:
            print("SKIP %s: %s" % (path.name, e), file=sys.stderr)
            continue
        boxes: dict[str, tuple] = {}     # object name -> (w, h) when both are literal
        for i, cmd in enumerate(lsb.commands):
            t = cmd.type.name
            if t not in ("BoxNew", "MesNew", "Caption", "TextIns"):
                continue
            name = strlit(cmd.args.get("Name")) if hasattr(cmd, "args") else None
            if t == "BoxNew":
                w, h = num(cmd.args.get("PR_WIDTH")), num(cmd.args.get("PR_HEIGHT"))
                if name and w and h:
                    boxes[name] = (w, h)
                continue
            if t not in ("Caption", "MesNew"):
                continue
            a = cmd.args
            face_name = strlit(a.get("PR_FONTNAME")) or ""
            face = FACE.get(face_name, 1)
            size = num(a.get("PR_FONTHEIGHT"), 0) or 0
            ls = num(a.get("PR_LINESPACE"), 0) or 0
            border = num(a.get("PR_FONTBORDER"), 0) or 0
            w = num(a.get("PR_WIDTH"))
            h = num(a.get("PR_HEIGHT"))
            wrapmode = "box"
            if w is None:
                parent = strlit(a.get("PR_PARENT"))
                pw = boxes.get(parent or "")
                il = num(a.get("PR_LEFT"), 0) or 0
                if pw:
                    w = pw[0] - 2 * il
                    h = pw[1] - 2 * (num(a.get("PR_TOP"), 0) or 0)
                elif t == "Caption":
                    # A Caption with no PR_WIDTH does not wrap: it draws from PR_LEFT
                    # rightwards until it runs out of screen. 960 = the render surface.
                    w = 960 - il
                    h = None
                    wrapmode = "nowrap-to-screen-edge"
            text = strlit(a.get("PR_TEXT")) if t == "Caption" else None
            src = "literal" if text is not None else (
                "expression / DB / label map" if t == "Caption" else "lns cell")
            if text is None or not size or not w:
                n_unmeasured += 1
                rows.append([path.name, i, t, face_name, size, w or "?", "?", src,
                             (text or str(a.get("PR_TEXT") or ""))[:60], "UNMEASURED"])
                continue
            extra = EXTRA_EM * size if border else 0.0
            lines = textlines(text) if text else []
            used = 0
            widest = 0.0
            for ln in lines:
                wpx = font(size, face).getlength(ln) + extra * len(ln)
                widest = max(widest, wpx)
                used += max(1, math.ceil(wpx / w)) if h else 1
            maxlines = int(h // pitch(size, ls)) if h else 1
            if maxlines <= 1:
                ratio = widest / w
                cls = "OVERFLOW" if ratio > 1 else ("TIGHT" if ratio > TIGHT else "OK")
                meas, cap = "%.0f px" % widest, "%d px %s" % (w, wrapmode)
            else:
                ratio = used / maxlines
                cls = "OVERFLOW" if used > maxlines else ("TIGHT" if ratio > TIGHT else "OK")
                meas, cap = "%d lines" % used, "%d lines x %d px" % (maxlines, w)
            n_ok += cls == "OK"
            n_tight += cls == "TIGHT"
            n_over += cls == "OVERFLOW"
            if cls != "OK":
                rows.append([path.name, i, t, face_name, size, cap, meas, src, text[:60], cls])
    write(OUT / "findings-ui.tsv", rows)
    print("UI sites: OK %d  TIGHT %d  OVERFLOW %d  UNMEASURED %d"
          % (n_ok, n_tight, n_over, n_unmeasured))
    return 0


def write(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["file", "index", "box", "font", "size", "capacity", "measured",
                    "source", "en_text", "class"])
        w.writerows(rows)
    print("wrote %s (%d rows)" % (path, len(rows)))


def merge(_argv):
    rows = []
    head = None
    for name in ("findings-scenes.tsv", "findings-ui.tsv"):
        p = OUT / name
        if not p.exists():
            continue
        lines = p.read_text(encoding="utf-8").splitlines()
        head = head or lines[0]
        rows += lines[1:]
    (OUT / "findings.tsv").write_text("\n".join([head or ""] + rows) + "\n", encoding="utf-8")
    print("wrote %s (%d rows)" % (OUT / "findings.tsv", len(rows)))
    return 0


def main(argv):
    if not argv or argv[0] not in ("scenes", "ui", "merge"):
        print(__doc__)
        return 2
    return {"scenes": scenes, "ui": ui, "merge": merge}[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
