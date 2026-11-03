"""lcm_captions.py - put English into the text layers of LiveCinema (.lcm) animations (lane 2, 2026-11-03, item 5).

A LiveCinema text layer stores its caption as  u32 length + cp932 bytes, then a flag byte, then the font name as
u32 length + cp932 bytes, then the font size (u32). The file is one sequential stream (no offset table: checked,
no u32 in these files equals a record start or the file length), so a caption may change length as long as its
length prefix changes with it. The same method was engine-proven for LiveCinema113 on 2026-10-25
(tools/images/reference_cinema.py, work/reference-repair-20261025/engine-probe). Fonts, sizes, colours, positions
and timing stay untouched. Never shorten to fit: a caption that needs more room gets another line (CR LF).

    PYTHONUTF8=1 uv run --no-project python tools/images/lcm_captions.py [--check]

Reads the Japanese originals from work/images/gal/<path>, writes work/<path> (= work/グラフィック/...), checks:
every listed caption replaced the expected number of times, nothing else changed (reverse substitution gives the
original bytes back), each English line fits the layer's own box where the layer has one (MS Gothic: Latin =
size/2 px, CJK = size px).
"""
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAKO = "グラフィック/立ち絵/アイテム/ロシアンたこ焼き/"

# Meicho Arc, "The Maidens' Holy War ~Prodigy~" (scenario 125, 000006F9.lsb idx 17 block 00000708): Natsumi's
# explanation of the Russian takoyaki game. Wording follows the shipped script (当たり = "hit", 芸のない =
# "unimaginative", ブラック・デス・デビル・ペッパー = Black Death Devil Pepper, so BDDP stays BDDP).
CAPTIONS = {
    "9個のうち、1つ当たり": "Out of 9, 1 is a hit",
    "　↑\r\nバ　カ": "　↑\r\nIdiot",
    "つまらん！": "Boring!",
    "黒以外にBDDPこそ\r\n芸がない！": "BDDP in a color\r\nother than black is\r\nwhat's unimaginative!",
}
# file -> number of caption fields expected per Japanese caption
FILES = {
    TAKO + "12つ.lcm": {"9個のうち、1つ当たり": 1},
    TAKO + "バカ.lcm": {"9個のうち、1つ当たり": 1, "　↑\r\nバ　カ": 1},
    TAKO + "五島当たる.lcm": {"9個のうち、1つ当たり": 1},
    TAKO + "春花当たる.lcm": {"9個のうち、1つ当たり": 1},
    TAKO + "蹴散らす.lcm": {"9個のうち、1つ当たり": 1, "　↑\r\nバ　カ": 1},
    TAKO + "つまらん.lcm": {"つまらん！": 1},
    TAKO + "芸がない.lcm": {"つまらん！": 1, "黒以外にBDDPこそ\r\n芸がない！": 1},
}


def field(text):
    raw = text.encode("cp932")
    return struct.pack("<I", len(raw)) + raw


def caption_offsets(data, text):
    """offsets of the caption field `text` that are followed by flag byte + font field + plausible size."""
    f = field(text)
    out, start = [], 0
    while True:
        o = data.find(f, start)
        if o < 0:
            return out
        p = o + len(f)
        flag = data[p]
        m = struct.unpack_from("<I", data, p + 1)[0]
        size = struct.unpack_from("<I", data, p + 5 + m)[0] if m <= 40 else 0
        if flag in (0, 1) and m <= 40 and 6 <= size <= 200:
            out.append((o, size))
        start = o + 1


def layer_box(data, offset):
    """the layer's own (w, h) box if it has one: the last pair before the caption (0 = auto size)."""
    seg = data[max(0, offset - 64):offset]
    for k in range(len(seg) - 8, -1, -1):
        w, h = struct.unpack_from("<II", seg, k)
        if 20 <= w <= 960 and 20 <= h <= 540 and seg[k - 8:k] == b"\x00" * 8:
            return w, h
    return None


def width(line, size):
    return sum(size if ord(c) > 0xFF else size / 2 for c in line)


def patch(data, mapping):
    out = data
    for jp, n in mapping.items():
        offs = caption_offsets(out, jp)
        if len(offs) != n:
            raise SystemExit("expected %d caption field(s) %r, found %d" % (n, jp, len(offs)))
        out = out.replace(field(jp), field(CAPTIONS[jp]))
    return out


def main():
    check_only = "--check" in sys.argv
    bad = 0
    for rel, mapping in FILES.items():
        src = (ROOT / "work/images/gal" / rel).read_bytes()
        if not src.startswith(b"LiveCinema11"):
            raise SystemExit("not a LiveCinema file: " + rel)
        new = patch(src, mapping)
        back = new
        for jp in mapping:
            back = back.replace(field(CAPTIONS[jp]), field(jp))
        if back != src:
            print("FAIL round trip", rel)
            bad += 1
        for jp in mapping:
            for o, size in caption_offsets(new, CAPTIONS[jp]):
                box = layer_box(new, o)
                widest = max(width(l, size) for l in CAPTIONS[jp].split("\r\n"))
                jp_w = max(width(l, size) for l in jp.split("\r\n"))
                ok = box is None or widest <= box[0]
                bad += 0 if ok else 1
                print("%-4s %-24s %-34r size %d  EN widest %4dpx (JP %4dpx)  box %s" % (
                    "OK" if ok else "WIDE", rel.split("/")[-1], CAPTIONS[jp], size, widest, jp_w, box or "auto"))
        if not check_only:
            dst = ROOT / "work" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(new)
    print("files %d, problems %d%s" % (len(FILES), bad, " (check only)" if check_only else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
