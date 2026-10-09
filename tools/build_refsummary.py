"""Build work/ノベルシステム/リファレンス概要.txt — the navigator's reference-card hover caption data.

    uv run --no-project --python 3.12 python tools/build_refsummary.py [--survey] [--check]

WHAT READS IT (0000001C only, verified 2026-09-26)
Index **674** (LineNo 767) `LoadTextFile(リファレンス全体, "ノベルシステム\\リファレンス概要.txt")`, split on
`","` at index 678 into `二元配列`. The array has exactly **one** consumer in the whole game — the
Caption at index **737** (LineNo 831):

    "No." ++ rNum ++ " " ++ 二元配列[rNum][0]        <- タイトル
        ++ "\\r\\n閲覧者 ：" ++ 二元配列[rNum][6]      <- 入手人物
        ++ "\\r\\n閲覧日時：" ++ 二元配列[rNum][7]     <- 入手年月日
        ++ "\\r\\n形式　　：" ++ 二元配列[rNum][9]     <- 形式

**Four of the eleven columns are read, all four are display, and not one column is compared against a
literal, used as an object name, used as a DB key or concatenated into a path.** (`rNum` is a reference
ID, and the only path near here is `…\\リファレンス概要\\rr" ++ rNum ++ ".gal"`, a number.) So no
key-agreement problem of the blocker-1 / arc-chain kind exists in this file, in either language.

WHY THIS IS NOT A PROJECTION OF リファレンスデータベース.tsv (the brief's premise, which does not hold)
The file is a **stale export of an older, smaller reference set, sorted by in-world chronology**:

    txt data rows                                            100   (tsv has 360)
    txt titles that still exist in the tsv タイトル column      39 of 100
    txt row k whose title matches the tsv row with ID = k     13 of 100
    txt row 1 = この地、新田と言ふ ; tsv 登場順 1 / ID 1 = something else entirely

`rNum` indexes the array directly and is a `rk<ID>` flag number (ID column — `0000001E` builds
`AssignTemp("rk" ++ DBGetStr("ID"))`), so **the Japanese game already prints the wrong record here**:
"No.19" shows the 19th-oldest document of an obsolete list, not reference ID 19. That is a pre-existing
authoring bug in the original, not something the translation caused, and it is not repaired here.

Because there is no row correspondence, this tool cannot project the tsv the way
`tools/build_navidata.py` does. It translates the file **in place, by VALUE**, exactly the way
`tools/lsb_strings.py apply` translates a script: a whole-cell exact match against maps built from the
two `リファレンスデータベース.tsv` copies (per column) plus the project's shared value maps
(`hen-jp-en`, `jinbutsu-jp-en`, `keishiki-jp-en`, `titles-jp-en`). Row order and row count never change.

COLUMNS TRANSLATED — and why the prose columns are not
The `.txt` has **no quoting**; `StringToArray(…, ",")` would shift every following column of a row if a
cell gained a comma. English prose reliably contains commas — measured with `--survey`, the `概要`
column alone would introduce 2 (data rows 23 and 70, the only hazards in the whole file) — so
`概要` / `解禁条件` / `備考` are excluded by design, and they are safe to exclude because the script
never reads them: a later tables edit can then never fail this build for a column nothing shows.
The two DATE columns (`解禁日時`, `入手年月日`) cannot be reached by a value map at all — this file's
dates are its own stale cells, not the tsv's — so they go through `tools/calendar_en.py` instead
(`DATE_COLUMNS`), in the compact `Shiyo 800-05-05 23:59` form, which is the one date form with no comma.
`入手年月日` is one of the four columns the Caption prints.
`--survey` prints, per column, what a map would change and every separator hazard it would introduce,
without writing anything; run it after a tables edit before widening `TRANSLATE`.

GATES (exit 1)
1. with empty maps the transform must reproduce `orig/ノベルシステム/リファレンス概要.txt` byte for byte,
2. no output cell may contain a comma, a quote, a tab, CR or LF — the offending cells are listed,
3. same row count and same per-row column count as the original.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calendar_en  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / 'orig' / 'ノベルシステム' / 'リファレンス概要.txt'
JP = ROOT / 'orig' / 'データベース' / 'リファレンスデータベース.tsv'
EN = ROOT / 'tsv-en' / 'リファレンスデータベース.tsv'
OUT = ROOT / 'work' / 'ノベルシステム' / 'リファレンス概要.txt'
PATCH = ROOT / 'patch'

# .txt column -> (tsv column that holds the same domain, extra shared map file or None)
COLUMNS = {
    0:  ('タイトル',   'titles-jp-en.tsv'),
    1:  ('解禁編',     'hen-jp-en.tsv'),
    2:  ('解禁シナリオ', 'titles-jp-en.tsv'),
    3:  (None,        None),               # 解禁日時  - placeholder / date
    4:  ('解禁人物',   'jinbutsu-jp-en.tsv'),
    5:  ('解禁条件',   None),
    6:  ('閲覧人物',   'jinbutsu-jp-en.tsv'),  # the .txt calls it 入手人物
    7:  ('閲覧年月日', None),               # date, stays Japanese (Q2364 precedent)
    8:  ('概要',       None),
    9:  ('形式',       'keishiki-jp-en.tsv'),
    10: ('備考',       None),
}
# Columns actually written. 0/6/9 are three of the four the Caption prints; 1/2/4 are free and keep the
# file coherent. 5/8/10 are prose (commas), 3/7 are dates: see the docstring.
TRANSLATE = (0, 1, 2, 4, 6, 9)
# Columns converted by tools/calendar_en.py (compact form) instead of a value map: they hold dates, and
# this file's dates are its OWN stale cells, not the tsv's, so no map could reach them. Column 7 is one
# of the four the Caption prints. Safe only because the compact form has no comma (see calendar_en).
DATE_COLUMNS = (3, 7)
HAZARDS = ((',', 'COMMA'), ('"', 'QUOTE'), ('\t', 'TAB'), ('\r', 'CR'), ('\n', 'LF'))


def rd(p, sep, enc):
    return list(csv.reader(p.read_text(encoding=enc).splitlines(), delimiter=sep))


def shared(name):
    m = {}
    if not name:
        return m
    for line in (PATCH / name).read_text(encoding='utf-8').splitlines():
        if line.startswith('#') or '\t' not in line:
            continue
        a, b = line.split('\t')[:2]
        m[a] = b
    return m


def maps():
    """One JP->EN value map per .txt column."""
    jp, en = rd(JP, '\t', 'cp932'), rd(EN, '\t', 'utf-8')
    hdr = jp[0]
    out = {}
    for c, (col, extra) in COLUMNS.items():
        m = dict(shared(extra))
        if col and col in hdr:
            i = hdr.index(col)
            for rj, re_ in zip(jp[1:], en[1:]):
                a = rj[i] if i < len(rj) else ''
                b = re_[i] if i < len(re_) else ''
                if a and a != b and a.strip() not in ('0',):
                    m.setdefault(a, b)
        out[c] = m
    return out


def transform(table, m, cols, datecols=()):
    out = [list(table[0])]
    for r in table[1:]:
        r = list(r)
        for c in cols:
            if c < len(r):
                r[c] = m[c].get(r[c], r[c])
        for c in datecols:
            if c < len(r):
                r[c] = calendar_en.normalize(calendar_en.convert(r[c], compact=True))
        out.append(r)
    return out


def encode(table):
    return ('\r\n'.join(','.join(r) for r in table) + '\r\n').encode('cp932')


def hazards(table):
    bad = []
    for n, r in enumerate(table):
        for c, v in enumerate(r):
            for ch, nm in HAZARDS:
                if ch in v:
                    bad.append('%s row %d col %d: %r' % (nm, n, c, v[:60]))
        try:
            ','.join(r).encode('cp932')
        except UnicodeEncodeError as ex:
            bad.append('not CP932 row %d: %r' % (n, ex.object[ex.start:ex.end]))
    return bad


def main(argv):
    table = rd(ORIG, ',', 'cp932')
    m = maps()

    # gate 1: identity transform round-trips
    if encode(transform(table, m, ())) != ORIG.read_bytes():
        print('gate 1 FAILED: the identity transform does not reproduce %s' % ORIG.name)
        return 1

    if '--survey' in argv:
        print('%-4s %-14s %-6s %-7s %s' % ('col', 'header', 'mapped', 'cells', 'hazards a map would add'))
        for c, (col, extra) in sorted(COLUMNS.items()):
            t2 = transform(table, m, (c,))
            n = sum(1 for a, b in zip(table[1:], t2[1:]) if a != b)
            haz = [h for h in hazards(t2) if (' col %d:' % c) in h]
            print('%-4d %-14s %-6d %-7d %s' % (c, table[0][c], len(m[c]), n, len(haz)))
            for h in haz[:3]:
                print('        %s' % h)
        return 0

    out = transform(table, m, TRANSLATE, DATE_COLUMNS)

    bad = hazards(out)
    if bad:
        print('gate 2 FAILED: %d separator/encoding hazards (the .txt has no quoting)' % len(bad))
        for b in bad[:40]:
            print('  ', b)
        return 1
    if len(out) != len(table) or any(len(a) != len(b) for a, b in zip(out, table)):
        print('gate 3 FAILED: row/column shape changed')
        return 1

    data = encode(out)
    changed = sum(1 for a, b in zip(table[1:], out[1:]) if a != b)
    if '--check' in argv:
        cur = OUT.read_bytes() if OUT.exists() else b''
        print('build_refsummary: %s' % ('up to date' if cur == data else 'STALE, rerun without --check'))
        return 0 if cur == data else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print('build_refsummary: ok, %d rows, %d rows changed, columns %s -> %s (%d bytes)'
          % (len(out) - 1, changed, list(TRANSLATE), OUT, len(data)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
