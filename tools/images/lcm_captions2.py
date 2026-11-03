"""lcm_captions2.py - English text layers for the 19 LiveCinema files the game really loads (lane 2, 2026-11-03,
work/feedback-20261103/lcm-usage/USAGE.md). Data: lcm_captions2_data.py (JP -> EN + source of every caption).

LiveCinema text layer, as read from these files (LiveCinema112 and 113 alike):
    caption-127: i32 x_start, y_start, x_end, y_end   (the layer's position at its first and last key frame)
    caption:     u32 length + cp932 text, u8 flag, u32 length + font name, u32 size, ...
    offset 13:   u32 canvas width, u32 canvas height  (a Cinema object is as wide as its canvas)
Edits: the caption (length prefix with it), x of a layer whose English must keep its Japanese right edge (names
left of the arrow, the 終 card), and the canvas width of the small plates/badges when the English is wider.
English lines are measured with the real fonts (msmincho.ttc: 0 = ＭＳ 明朝, 1 = ＭＳ Ｐ明朝). "WRAP:" text is broken
greedily inside the Japanese block's widest line ("||" = blank line). Nothing is ever shortened.

    PYTHONUTF8=1 uv run --no-project --with pillow python tools/images/lcm_captions2.py [--check] [--json OUT]
"""
import json
import math
import struct
import sys
from pathlib import Path

from PIL import ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lcm_captions as C  # noqa: E402
from lcm_captions2_data import RECAP, NAMES, UI  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
G = "グラフィック/"
FILES = {
    "イラスト/永劫回帰/未来/ラストテキスト": RECAP, "シナリオナビ/真呪殺編解禁/感染": RECAP,
    "シナリオナビ/真呪殺編解禁/放棄": RECAP, "シナリオナビ/真呪殺編解禁/春花と魔女と死神": RECAP,
    "シナリオナビ/真呪殺編解禁/監視": RECAP, "シナリオナビ/真呪殺編解禁/私にできること": RECAP,
    "シナリオナビ/真呪殺編解禁/葛藤": RECAP,
    "立ち絵/人物/lcm/なつみ→五島": NAMES, "立ち絵/人物/lcm/五島→なつみ": NAMES,
    "立ち絵/人物/lcm/伊勢→夏菜": NAMES, "立ち絵/人物/lcm/夏菜→伊勢": NAMES,
    "背景/lcm/ルートエンド": UI, "システム/既読スキップ土台": UI, "システム/自動送り土台": UI,
    "システム/実況案内": UI, "ドキュメント/上限メッセージ": UI,
    "メニュー/右クリック/雑談/新": UI, "メニュー/右クリック/雑談/雑談新": UI, "メニュー/右クリック/雑談/雑談旧": UI,
}
SCALE = {"システム/実況案内": 0.8}          # the layer's 0.8 x/y scale (doubles in its record)
NAME_RIGHT = set(NAMES)                    # a name left of the arrow and the 終 card keep their Japanese right edge
# 監視 board post: 4 Japanese lines become 6 English lines; the layer moves up 40 px at every key frame so the last
# line stays on the 540 px screen (coordinator 2026-11-03)
Y_SHIFT = {k: -40 for k in RECAP if k.startswith("祀耀800年4月9日")}
_FONTS = {}


def font(name, size):
    idx = 1 if "Ｐ" in name else 0
    key = (idx, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype("C:/Windows/Fonts/msmincho.ttc", size, index=idx)
    return _FONTS[key]


def width(line, f):
    return f.getlength(line)


def wrap(text, f, limit):
    """greedy wrap inside `limit` px; "||" = blank line, CR LF = forced break (kept)."""
    out = []
    for para in text.replace("||", "\r\n\x00\r\n").split("\r\n"):
        if para == "\x00":
            out.append("")
            continue
        tokens, cur = [], ""
        for ch in para:          # keep separators (space / U+3000) attached to the preceding word
            cur += ch
            if ch in " \u3000":
                tokens.append(cur)
                cur = ""
        if cur:
            tokens.append(cur)
        line = ""
        for t in tokens:
            if line and width((line + t).rstrip(" "), f) > limit:
                out.append(line.rstrip(" "))
                line = t.lstrip(" ")
            else:
                line += t
        out.append(line.rstrip(" "))
    return "\r\n".join(out)


def caption_info(data, jp):
    res = []
    for o, size in C.caption_offsets(data, jp):
        p = o + 4 + len(jp.encode("cp932"))
        m = struct.unpack_from("<I", data, p + 1)[0]
        fname = data[p + 5:p + 5 + m].decode("cp932")
        pos = list(struct.unpack_from("<4i", data, o - 127))
        res.append(dict(off=o, size=size, font=fname, pos=pos))
    return res


def build(rel, table):
    src = (ROOT / "work/images/gal" / (G + rel + ".lcm")).read_bytes()
    cw, ch = struct.unpack_from("<II", src, 13)
    scale = SCALE.get(rel, 1.0)
    found = {}
    for jp in table:
        info = caption_info(src, jp)
        if info:
            found[jp] = info
    if not found:
        raise SystemExit("no caption of the table in " + rel)
    edits, report, need_w = [], [], cw
    for jp, infos in found.items():
        en_raw, source = table[jp] if isinstance(table[jp], tuple) else (table[jp], "glossary / shipped name")
        for inf in infos:
            f = font(inf["font"], inf["size"])
            jp_lines = jp.split("\r\n")
            jp_w = max(width(l, f) for l in jp_lines) * scale
            en = wrap(en_raw[5:], f, jp_w / scale) if en_raw.startswith("WRAP:") else en_raw
            en_lines = en.split("\r\n")
            en_w = max(width(l, f) for l in en_lines) * scale
            x0, y0, x1, y1 = inf["pos"]
            pos = None
            if jp == "終" or (jp in NAME_RIGHT and max(x0, x1) < 461):   # 461 = x of the arrow
                shift = int(math.floor(max(x0, x1) + jp_w - en_w)) - max(x0, x1)
                pos = [x0 + shift, y0, x1 + shift, y1]
            if jp in Y_SHIFT:
                dy = Y_SHIFT[jp]
                pos = [x0, y0 + dy, x1, y1 + dy]
            nx0, nx1 = (pos[0], pos[2]) if pos else (x0, x1)
            en_right = max(nx0, nx1) + en_w
            jp_right = max(x0, x1) + jp_w
            end_right = nx1 + en_w
            # same or smaller footprint than the Japanese, or the end key frame (the resting place) is on the canvas
            fits = en_w <= jp_w + 0.5 or end_right <= cw or cw < 300
            if cw < 300:          # plates and badges: grow the canvas to the English
                need_w = max(need_w, int(math.ceil(en_right)) + 2)
            report.append(dict(file=rel, off=inf["off"], jp=jp, en=en, source=source, font=inf["font"],
                               size=inf["size"], jp_lines=len(jp_lines), en_lines=len(en_lines),
                               jp_w=round(jp_w), en_w=round(en_w), pos=inf["pos"], new_pos=pos,
                               right=round(en_right), jp_right=round(jp_right), fits=fits))
            edits.append((inf["off"], jp, en, pos))
    out = bytearray(src)
    for off, jp, en, pos in sorted(edits, reverse=True):
        old = C.field(jp)
        assert out[off:off + len(old)] == old
        out[off:off + len(old)] = C.field(en)
        if pos:
            struct.pack_into("<4i", out, off - 127, *pos)
    if need_w != cw:
        struct.pack_into("<I", out, 13, need_w)
    for r in report:
        r["canvas"] = [cw, ch]
        r["new_canvas"] = [need_w, ch]
    return bytes(out), report, src


def verify(new, src, report):
    """re-read every English caption at its new offset; the bytes outside the edited fields equal the source."""
    back = bytearray(new)
    if struct.unpack_from("<I", back, 13)[0] != report[0]["canvas"][0]:
        struct.pack_into("<I", back, 13, report[0]["canvas"][0])
    # rebuild the source from the English file: undo captions (by search, they are unique fields) and positions
    for r in report:
        enf, jpf = C.field(r["en"]), C.field(r["jp"])
        i = back.find(enf)
        if i < 0:
            return "caption missing: %r" % r["en"][:30]
        if r["new_pos"]:
            struct.pack_into("<4i", back, i - 127, *r["pos"])
        back[i:i + len(enf)] = jpf
    return "ok" if bytes(back) == src else "round trip differs"


def main():
    check = "--check" in sys.argv
    allrep, bad = [], 0
    for rel, table in FILES.items():
        new, rep, src = build(rel, table)
        v = verify(new, src, rep)
        if v != "ok":
            bad += 1
        for r in rep:
            bad += 0 if r["fits"] else 1
            print("%-4s %-30s @%-5d %-11s %2d->%2d lines  w %4d->%4d  right %4d (JP %4d)%s  %r" % (
                "OK" if r["fits"] else "WIDE", rel.split("/")[-1], r["off"], r["font"], r["jp_lines"], r["en_lines"],
                r["jp_w"], r["en_w"], r["right"], r["jp_right"],
                ("  x %s->%s" % (r["pos"][0], r["new_pos"][0])) if r["new_pos"] else "", r["en"][:40]))
        if rep[0]["new_canvas"] != rep[0]["canvas"]:
            print("     canvas %s -> %s" % (rep[0]["canvas"], rep[0]["new_canvas"]))
        print("     round trip:", v)
        allrep += rep
        if not check:
            dst = ROOT / "work" / (G + rel + ".lcm")
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(new)
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(allrep, ensure_ascii=False, indent=1),
                                                                encoding="utf-8")
    print("files %d, captions %d, problems %d%s" % (len(FILES), len(allrep), bad, " (check only)" if check else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
