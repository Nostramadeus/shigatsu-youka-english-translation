"""Replace the first narration/dialogue text line of 00000024-line16.lns with a test string.

LiveMaker stores every glyph as a 16-bit CP932 code (livemaker/lsb/novel.py TWdChar), so
the test string must be CP932-encodable. U+2014 EM DASH is not; U+2015 HORIZONTAL BAR is,
and is the agreed dash for this project. Macrons and accented Latin are impossible.

Run from tools/harness:
    PYTHONUTF8=1 uv run --no-project python patch_test_line.py
then compile with:
    cd ../../orig && uvx --from pylivemaker lmlsb batchinsert --no-backup \
        ../tools/harness/work/00000024.lsb ../tools/harness/test-lns/
"""

import re
import sys

P = "test-lns/00000024-line16.lns"
SEP = b"\r\r\n"

TEST = (
    "TEST 01 abc ABC 0123 -- dash ― "
    "curly “quoted” ‘single’ ellipsis… "
    "straight \"quoted\" 'single' end. "
    "The quick brown fox jumps over the lazy dog, 0123456789."
)

data = open(P, "rb").read()
lines = data.split(SEP)
started = False
for i, raw in enumerate(lines):
    s = raw.decode("utf-8")
    if "BEGIN DECOMPILED SCRIPT" in s:
        started = True
        continue
    if not started:
        continue
    t = s.strip()
    if not t or t.startswith(";") or t.startswith("{") or re.fullmatch(r"(<[^>]*>)+", t):
        continue
    m = re.match(r"^((?:<[^>]*>)*)(.*?)((?:<[^>]*>)*)$", s, re.DOTALL)
    pre, mid, post = m.group(1), m.group(2), m.group(3)
    if not mid.strip():
        continue
    print("INDEX:", i)
    print("ORIGINAL:", s)
    new = pre + TEST + post
    print("NEW:", new)
    for ch in new:
        ch.encode("cp932")   # fail loudly rather than at compile time
    lines[i] = new.encode("utf-8")
    break
else:
    sys.exit("no text line found")

open(P, "wb").write(SEP.join(lines))
print("written", P)
