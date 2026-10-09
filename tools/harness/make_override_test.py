"""Build the loose-file override test files.

The opening scene (00000024.lsb) turned out to be unreachable with PostMessage - the
title/notice screen is gated behind image buttons that only answer to a real mouse.
So the test uses two files whose text is on the FIRST screen the game shows instead:

  000000F2.lsb          (archive root)      - holds the menu labels of the boot prompts
                                              as plain CP932 PascalStrings
  データベース\注意.tsv  (archive subfolder)  - holds the boot prompt body text, plain CP932

Both get a test string, are written to tools/harness/work/loose/, and are meant to be
copied next to the exe. If the game shows the test strings, loose files override the
archive; if it shows the Japanese, they do not.

The .lsb patch is a SAME-LENGTH byte replacement of the PascalString payload, so the
file stays structurally valid without recompiling anything.
"""

from pathlib import Path

ORIG = Path("../../orig")
OUT = Path("work/loose")

# CP932 is the only character set LiveMaker can store (see PROGRESS.md), so the em dash
# is U+2015 HORIZONTAL BAR and the macrons are gone.
TSV_TEST = (
    "TEST 01 abc ABC 0123 -- em―dash curly “q” ‘s’ ellipsis…\\n"
    "iiiiiiiiiiiiiiiiiiii\\n"
    "WWWWWWWWWWWWWWWWWWWW\\n"
    "あああああああああああああああああああ"
)
LSB_LABEL_OLD = "チェックしない"  # the 2nd menu row of screen 1
LSB_LABEL_NEW = "LSB TEST abcAB"  # must be the same number of CP932 BYTES


def patch_tsv():
    src = ORIG / "データベース" / "注意.tsv"
    rows = src.read_bytes().decode("cp932").split("\r\n")
    # row 1 is No=0, the very first prompt the game shows
    cols = rows[1].split("\t")
    print("TSV old:", cols[2][:60])
    cols[2] = TSV_TEST
    rows[1] = "\t".join(cols)
    dst = OUT / "データベース" / "注意.tsv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes("\r\n".join(rows).encode("cp932"))
    print("TSV new:", TSV_TEST[:60])
    print("wrote", dst, dst.stat().st_size, "bytes")


def patch_lsb():
    src = ORIG / "000000F2.lsb"
    data = bytearray(src.read_bytes())
    old = LSB_LABEL_OLD.encode("cp932")
    new = LSB_LABEL_NEW.encode("cp932")
    assert len(new) == len(old), "replacement must be %d CP932 bytes, got %d" % (
        len(old), len(new))
    n = 0
    i = data.find(old)
    while i != -1:
        # sanity: a Delphi/LiveMaker PascalString is Int32 length + payload
        length = int.from_bytes(data[i - 4:i], "little")
        print("  hit at 0x%x, preceding int32 = %d (payload %d)" % (i, length, len(old)))
        data[i:i + len(old)] = new
        n += 1
        i = data.find(old, i + len(new))
    print("patched %d occurrence(s)" % n)
    dst = OUT / "000000F2.lsb"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(bytes(data))
    print("wrote", dst, dst.stat().st_size, "bytes (orig %d)" % src.stat().st_size)


if __name__ == "__main__":
    patch_tsv()
    patch_lsb()
