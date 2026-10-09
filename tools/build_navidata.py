"""Build work/ノベルシステム/ナビデータ.txt — the file the scenario navigator's MAP is built from.

    uv run --no-project --python 3.12 python tools/build_navidata.py [--check]

WHY THIS FILE EXISTS (2026-09-26, notes/NAVIGATOR-BUG-AUDIT.md)
`0000001C.lsb` indices 4872 and 6196 (LineNo 5215 / 6673) do

    VarNew ナビデータ 4 "" 2
    Calc LoadTextFile(ナビデータ, "ノベルシステム\\ナビデータ.txt")
    Calc StringToArray(ナビデータ[i], 分割用, ",")   ->  AddArray(二元配列, 分割用)

so every entry card on the navigator map comes out of this comma-separated text file, NOT out of the
`ナビデータ` DATABASE TABLE (which `00001F85` builds from データベース\シナリオデータベース.tsv and which
only serves the hover/confirm panel fields). notes/NAVIDATA-AUDIT.md called the .txt dead on a scan that
missed these two commands; it is live. The script reads, by position:

    [0] 連番   [1] 分類   [4] 閲覧年月日   [5] タイトル   [6] 解禁編   [7] 列番号
    [8]-[12] 罫線1-5   [25] 特殊1

`[5]` becomes the map object's NAME (`BoxNew 二元配列[n][5]`), `[6]` is compared against the nine arc
names, and `[8]`-`[12]` are `Exists()` / `GetProp()` lookups of OTHER entries' object names (the
connector lines). So once the scripts and the tsv are English this file has to be English too, or no
card is created at all.

WHAT IS TRANSLATED HERE
The first 31 columns of tsv-en/シナリオデータベース.tsv, verbatim — that is where タイトル, 解禁編 and
解禁人物 are already translated — with one addition: the 罫線1-6 cells hold scenario TITLES, and they are
run through the JP->EN title map derived from the two tables (same pairing rule as tools/gen_titles_map.py)
so the connector-line lookups keep matching the object names. The 罫線 columns are NOT translated in
tsv-en itself because no script ever reads them from the database (0 `DBGetStr("罫線…")` game-wide, checked
2026-09-26); this file is their only consumer.

The 連番 10000 terminator row is dropped: the original .txt does not have it (218 data rows vs the tsv's 219).

HARD GATES (exit 1)
1. the same projection of orig/データベース/シナリオデータベース.tsv must reproduce
   orig/ノベルシステム/ナビデータ.txt byte for byte,
2. no output cell may contain a comma, a quote, a tab, CR or LF — the engine splits on "," with no
   quoting, so one comma would shift every following column of that row,
3. same row count as the original.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JP_TSV = ROOT / 'orig' / 'データベース' / 'シナリオデータベース.tsv'
EN_TSV = ROOT / 'tsv-en' / 'シナリオデータベース.tsv'
ORIG_TXT = ROOT / 'orig' / 'ノベルシステム' / 'ナビデータ.txt'
OUT = ROOT / 'work' / 'ノベルシステム' / 'ナビデータ.txt'
NCOL = 31                      # the .txt is the tsv's first 31 columns
KEISEN = range(8, 14)          # 罫線1-6: cells that hold another entry's title
TERMINATOR = '10000'           # 連番 of the tsv-only empty terminator row


def rows(p, enc):
    return list(csv.reader(p.read_text(encoding=enc).splitlines(), delimiter='\t'))


def title_map(jp, en):
    """JP title -> EN title, paired row by row on 連番. Only rows whose title actually changed."""
    h = jp[0]
    i_no, i_t = h.index('連番'), h.index('タイトル')
    enm = {r[i_no]: r for r in en[1:] if len(r) > i_t}
    m = {}
    for rj in jp[1:]:
        if len(rj) <= i_t:
            continue
        re_ = enm.get(rj[i_no])
        if re_ and rj[i_t] and re_[i_t] and rj[i_t] != re_[i_t]:
            m[rj[i_t]] = re_[i_t]
    return m


def project(table, tmap):
    """table (list of rows) -> the comma file's bytes."""
    out = []
    for n, r in enumerate(table):
        cells = (r + [''] * NCOL)[:NCOL]
        if n and cells[0] == TERMINATOR:
            continue
        if n:
            for c in KEISEN:
                cells[c] = tmap.get(cells[c], cells[c])
        out.append(cells)
    return out


def encode(table):
    return ('\r\n'.join(','.join(r) for r in table) + '\r\n').encode('cp932')


def main(argv):
    jp, en = rows(JP_TSV, 'cp932'), rows(EN_TSV, 'utf-8')
    errs = []

    # gate 1: the projection reproduces the original file exactly
    ref = encode(project(jp, {}))
    want = ORIG_TXT.read_bytes()
    if ref != want:
        errs.append('gate 1: projecting the JP tsv does NOT reproduce %s (%d vs %d bytes)'
                    % (ORIG_TXT.name, len(ref), len(want)))
        a, b = ref.split(b'\r\n'), want.split(b'\r\n')
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                errs.append('  first differing line %d:\n    got  %r\n    want %r' % (i, x[:160], y[:160]))
                break

    tmap = title_map(jp, en)
    table = project(en, tmap)

    # gate 2: separator hazards
    for n, r in enumerate(table):
        for c, v in enumerate(r):
            for ch, nm in ((',', 'COMMA'), ('"', 'QUOTE'), ('\t', 'TAB'), ('\r', 'CR'), ('\n', 'LF')):
                if ch in v:
                    errs.append('gate 2: %s in row %d col %d: %r' % (nm, n, c, v))
        try:
            ','.join(r).encode('cp932')
        except UnicodeEncodeError as ex:
            errs.append('gate 2: row %d not CP932: %r' % (n, ex.object[ex.start:ex.end]))

    # gate 3: row count
    if len(table) != len(want.rstrip(b'\r\n').split(b'\r\n')):
        errs.append('gate 3: %d rows, original has %d'
                    % (len(table), len(want.rstrip(b'\r\n').split(b'\r\n'))))

    if errs:
        print('build_navidata: %d error(s)' % len(errs))
        for e in errs[:40]:
            print('  ', e)
        return 1

    data = encode(table)
    changed = sum(1 for x, y in zip(data.split(b'\r\n'), want.split(b'\r\n')) if x != y)
    if '--check' in argv:
        cur = OUT.read_bytes() if OUT.exists() else b''
        print('build_navidata: %s' % ('up to date' if cur == data else 'STALE, rerun without --check'))
        return 0 if cur == data else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print('build_navidata: ok, %d rows, %d rows changed, %d 罫線 titles mapped -> %s (%d bytes)'
          % (len(table), changed, len(tmap), OUT, len(data)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
