"""Convert a UTF-8 translated data table tsv-en/<name>.tsv into the CP932 file the game loads,
work/データベース/<name>.tsv, after checking it against orig/データベース/<name>.tsv.
    uv run tools/build_tsv.py 注意.tsv [more.tsv ...]
Checks (all hard): same row count, same column count per row, header row identical (a column may gain " cha N", FIX2), every cell CP932-encodable,
no cell longer than the header's "cha N" cap for that column, a cell that was empty/"0" in the source stays so.
The translated file keeps the literal backslash-n sequences the source uses for line breaks.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = 'データベース'
EXTRA_COLS = ('表示名',)   # R1 2026-09-26: allowed trailing display columns (see the header check)


def load(p, enc):
    t = p.read_bytes().decode(enc).lstrip('﻿')
    nl = '\r\n' if '\r\n' in t else '\n'
    return t.split(nl), nl


def main(names):
    bad = 0
    for name in names:
        src = ROOT / 'orig' / DB / name
        en = ROOT / 'tsv-en' / name
        out = ROOT / 'work' / DB / name
        s_rows, s_nl = load(src, 'cp932')
        e_rows, _ = load(en, 'utf-8')
        errs = []
        if len(s_rows) != len(e_rows):
            errs.append(f'row count {len(s_rows)} vs {len(e_rows)}')
        hdr = s_rows[0].split('\t')
        # FIX2 2026-09-26: a header cell may gain a width declaration " cha N". The engine cuts an untyped string
        # column at 80 bytes (reference 概要 showed "...Prefectural Hi"). Nothing else in the header may change.
        e_hdr = e_rows[0].split('\t') if e_rows else []
        # R1 2026-09-26 (Q2054): a table may gain TRAILING display columns named in EXTRA_COLS (the encyclopedia
        # name columns are keys; the print sites read 表示名 instead, see patch/dispcol.py). Rows then carry the
        # extra cells too; the original columns are checked exactly as before.
        extra = 0
        while len(e_hdr) - extra > len(hdr) and e_hdr[len(e_hdr) - 1 - extra] in EXTRA_COLS:
            extra += 1
        if len(e_hdr) - extra != len(hdr) or any(
                a != b and not re.fullmatch(re.escape(a) + r' cha \d+', b) for a, b in zip(hdr, e_hdr)):
            errs.append('header row changed')
        caps = []
        for h in (e_hdr or hdr):
            m = re.search(r' cha (\d+)$', h)
            caps.append(int(m.group(1)) if m else None)
        for r, (sr, er) in enumerate(zip(s_rows, e_rows)):
            sc, ec = sr.split('\t'), er.split('\t')
            if extra and len(ec) == len(sc) + extra:
                for c, b in enumerate(ec[len(sc):], len(sc)):
                    try:
                        b.encode('cp932')
                    except UnicodeEncodeError as ex:
                        errs.append(f'row {r} col {c}: not CP932: {ex.object[ex.start:ex.end]!r}')
                ec = ec[:len(sc)]
            if len(sc) != len(ec):
                errs.append(f'row {r}: column count {len(sc)} vs {len(ec)}')
                continue
            for c, (a, b) in enumerate(zip(sc, ec)):
                if a.strip() in ('', '0') and b != a:
                    errs.append(f'row {r} col {c}: source empty/0 but EN {b[:30]!r}')
                try:
                    b.encode('cp932')
                except UnicodeEncodeError as ex:
                    errs.append(f'row {r} col {c}: not CP932: {ex.object[ex.start:ex.end]!r}')
                if c < len(caps) and caps[c] and len(b) > caps[c]:
                    errs.append(f'row {r} col {c}: {len(b)} chars > cap {caps[c]}')
        if errs:
            bad += 1
            print(f'{name}: {len(errs)} errors')
            for e in errs[:40]:
                print('  ', e)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(s_nl.join(e_rows).encode('cp932'))
        changed = sum(1 for a, b in zip(s_rows, e_rows) if a != b)
        print(f'{name}: ok, {len(e_rows)} rows, {changed} rows changed -> {out}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
