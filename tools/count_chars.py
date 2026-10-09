"""count_chars.py - reproduce the per-scene character total the game stores in 文字数1 / 文字数2.

    uv run --no-project --python 3.12 python tools/count_chars.py jp          # JP reproduction table
    uv run --no-project --python 3.12 python tools/count_chars.py en          # EN totals (dry run)
    uv run --no-project --python 3.12 python tools/count_chars.py en --write  # write tsv-en columns
    uv run --no-project --python 3.12 python tools/count_chars.py blocks <id> [lns|lns-en]

THE COUNTING RULE (derived 2026-09-26, proven against 20 single-block scenes, see
notes/CHARCOUNT-FIX.md):

    total = for every displayed page:  len(page text)  with every line break counted as
            CR+LF = 2 characters, including the break that ends the page.
            An empty page contributes 0.

In .lns terms: strip ';' header comments and {COMMAND ...} lines, drop every <TAG> except
<BR> (a line break, 2) and <PG> (ends the page: 2 if the page had text), keep everything
else verbatim - leading spaces and ideographic spaces included. The physical newlines of the
.lns file are layout only and count for nothing.

WHY THIS IS THE ENGINE'S OWN NUMBER: 0000001C.lsb index 4557-4561 samples
JLength(GetProp("メッセージボックス", 50)) - the text currently in the message box - every
frame and banks the previous page when the box shrinks. So the running counter counts exactly
the characters the box holds, CRLFs included, and 文字数1 is that same total for the whole
scene.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRLF = 2                       # a line break in the message box is CR+LF
TAG = re.compile(r'<[^>\n]*>')
CMD = re.compile(r'\{[A-Z_]*[^{}]*\}')

SYSTEM_IDS = {'0000001C', '0000001E', '000000F2',
              '000003A8', '000003AE', '000003B4', '000003BC'}


def body(path: Path) -> str:
    """The .lns text with the pylivemaker ';' header/footer comments removed."""
    return '\n'.join(ln.rstrip('\r') for ln in path.read_text(encoding='utf-8').splitlines()
                     if not ln.startswith(';'))


def pages(text: str):
    """[page, ...] - the raw page strings the message box holds, <BR> still in place."""
    buf, out = [], []
    for raw in text.split('\n'):
        s = CMD.sub('', raw)
        if not s:
            continue
        while '<PG>' in s:
            head, s = s.split('<PG>', 1)
            buf.append(head)
            out.append(('\n'.join(buf), True))
            buf = []
        buf.append(s)
    out.append(('\n'.join(buf), False))
    return out


def plain(page: str) -> str:
    """The page with markup removed and <BR> turned into one break marker."""
    return TAG.sub('', page.replace('<BR>', '\x00').replace('\n', ''))


def count_text(text: str) -> int:
    n = 0
    for page, closed in pages(text):
        p = plain(page)
        if not p:
            continue                     # an empty page is never displayed
        n += len(p) + p.count('\x00') * (CRLF - 1)   # each <BR> is CRLF, not 1 char
        if closed:
            n += CRLF                    # the break that ends the page
    return n


def count_file(path: Path) -> int:
    return count_text(body(path))


def blocks(scene_id: str, folder: str = 'lns'):
    """[(block name, chars), ...] for one scene id, empty blocks dropped."""
    out = []
    for f in sorted((ROOT / folder).glob(scene_id + '-*.lns')):
        n = count_file(f)
        if n:
            out.append((f.name.split('-', 1)[1][:-4], n))
    return out


# --------------------------------------------------------------------------- tables
def nav_map():
    """lsb id -> 連番 (first occurrence wins; notes/_db/_navigator-order.tsv)."""
    out = {}
    for r in csv.reader((ROOT / 'notes/_db/_navigator-order.tsv')
                        .read_text(encoding='utf-8').splitlines(), delimiter='\t'):
        if not r or r[0].startswith('#') or r[0] == 'position':
            continue
        out.setdefault(r[3], r[1])
    return out


def scene_ids():
    return sorted({f.name.split('-')[0] for f in (ROOT / 'lns-en').glob('*.lns')} - SYSTEM_IDS)


def read_tsv(path: Path, enc: str):
    return list(csv.reader(path.read_text(encoding=enc).splitlines(), delimiter='\t'))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'blocks'
    if mode == 'blocks':
        for name, n in blocks(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'lns'):
            print('%-12s %6d' % (name, n))
        raise SystemExit(0)
    raise SystemExit('use work/charcount/*.py drivers for jp/en until this is wired up')
