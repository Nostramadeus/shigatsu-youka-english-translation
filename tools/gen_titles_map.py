"""Regenerate patch/titles-jp-en.tsv: the JP->EN scenario-title map applied as an extra map to the
five files that look map objects up by their Japanese title (0000001C, 00001CA0, 00001E29,
00001F8A, 000015C2).

    uv run --no-project --python 3.12 python tools/gen_titles_map.py [--check]

Rows are DERIVED, row by row, from orig/データベース/シナリオデータベース.tsv (JP title) paired with
tsv-en/シナリオデータベース.tsv (EN title): a row is in the map when the JP title contains kana or
kanji and the EN title does not. Run it after every title batch, then rebuild the five files.

patch/titles-extra.tsv is appended verbatim afterwards. It holds rows that are NOT a bare title but
are built from one, so a pure derivation would miss them: 000015C2 indices 53 and 92 look up
"四月病New", the NEW-tag object 0000001C creates as `<title> ++ "New"` (Q2360). Keep hand-written
rows there, never in titles-jp-en.tsv, or the next regeneration drops them.

--check exits 1 and prints a diff instead of writing, for use after someone edits the tables by hand.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JP = ROOT / 'orig' / 'データベース' / 'シナリオデータベース.tsv'
EN = ROOT / 'tsv-en' / 'シナリオデータベース.tsv'
OUT = ROOT / 'patch' / 'titles-jp-en.tsv'
EXTRA = ROOT / 'patch' / 'titles-extra.tsv'
CJK = re.compile(r'[぀-ヿ一-鿿]')
HEADER = '# JP scenario title -> EN (object-name lookups; regenerate after every title batch)'


def rows(p, enc):
    return list(csv.reader(p.read_text(encoding=enc).splitlines(), delimiter='\t'))


def build():
    jp, en = rows(JP, 'cp932'), rows(EN, 'utf-8')
    i = jp[0].index('タイトル')
    pairs, seen = [], set()
    for rj, re_ in zip(jp[1:], en[1:]):
        if len(rj) <= i or len(re_) <= i:
            continue
        a, b = rj[i], re_[i]
        if not a or not b or a in seen:
            continue
        if CJK.search(a) and not CJK.search(b):
            seen.add(a)
            pairs.append((a, b))
    lines = [HEADER] + ['%s\t%s' % p for p in pairs]
    if EXTRA.exists():
        lines += [l for l in EXTRA.read_text(encoding='utf-8').splitlines() if l.strip()]
    return '\r\n'.join(lines) + '\r\n', len(pairs)


def main(argv):
    text, n = build()
    if '--check' in argv:
        old = OUT.read_text(encoding='utf-8') if OUT.exists() else ''
        if old.replace('\r', '') == text.replace('\r', ''):
            print('titles-jp-en.tsv up to date (%d derived rows)' % n)
            return 0
        print('titles-jp-en.tsv is STALE; rerun without --check')
        return 1
    OUT.write_text(text, encoding='utf-8', newline='')
    print('wrote %s: %d derived rows + %d extra' % (
        OUT.name, n, len(text.splitlines()) - 1 - n))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
