"""Convert a UTF-8 translated data table tsv-en/<name>.tsv into the CP932 file the game loads,
work/データベース/<name>.tsv, after checking it against orig/データベース/<name>.tsv.
    uv run tools/build_tsv.py 注意.tsv [more.tsv ...]
    uv run tools/build_tsv.py --check <names>     (all checks, writes nothing)
Checks (all hard): same row count, same column count per row, header row identical (a column may gain " cha N", FIX2), every cell CP932-encodable,
no cell longer than its column width in CP932 BYTES (" cha N" / " chr N"; no declaration = 80), a cell that was empty/"0" in the source stays so.
The translated file keeps the literal backslash-n sequences the source uses for line breaks.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = 'データベース'
EXTRA_COLS = ('表示名', 'ポイント倍率100')   # R1 2026-09-26: allowed trailing display columns (see the header check); 2026-11-13: ポイント倍率100 = whole-number point multiplier of 編.tsv (points must not depend on the Windows decimal symbol)
CHECK_ONLY = False   # 2026-11-03: --check


def load(p, enc):
    t = p.read_bytes().decode(enc).lstrip('﻿')
    nl = '\r\n' if '\r\n' in t else '\n'
    return t.split(nl), nl


UNTYPED_CAP = 80   # FIX2 2026-09-26: the engine cuts a column with no width declaration at 80 bytes


def compatible_header(source, translated):
    """A header cell may stay as it is, gain " cha N", or raise the N of its own " cha N" / " chr N" (2026-11-03:
    chr too; 実況 tables declare " chr 200"). The type word and the column name never change."""
    if source == translated:
        return True
    source_width = re.fullmatch(r'(.*) (cha|chr) (\d+)', source)
    base = source_width.group(1) if source_width else source
    kind = source_width.group(2) if source_width else 'cha'
    target_width = re.fullmatch(re.escape(base) + ' ' + kind + r' (\d+)', translated)
    return target_width is not None and (source_width is None or int(target_width.group(1)) >= int(source_width.group(3)))


def cell_cap(header):
    """Byte width of a column: N of " cha N" / " chr N" (any case), else the untyped 80-byte cut."""
    m = re.search(r' (cha|chr) (\d+)$', header, re.IGNORECASE)
    return int(m.group(2)) if m else UNTYPED_CAP


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
                not compatible_header(a, b) for a, b in zip(hdr, e_hdr)):
            errs.append('header row changed')
        # 2026-11-03 (friend report: encyclopedia "...Megasawa Cit"): the width is in CP932 BYTES, not characters.
        # The old check counted characters, so a 1591-character cell with two 2-byte quotes (1594 bytes) passed
        # a 1592 cap and the game cut the last 2 bytes. A column with no declaration is cut at UNTYPED_CAP bytes;
        # that only fails a cell whose own Japanese source fitted (some author cells already exceed it).
        caps = [cell_cap(h) for h in (e_hdr or hdr)]
        s_caps = [cell_cap(h) for h in hdr]
        for r, (sr, er) in enumerate(zip(s_rows, e_rows)):
            sc, ec = sr.split('\t'), er.split('\t')
            if extra and len(ec) == len(sc) + extra:
                for c, b in enumerate(ec[len(sc):], len(sc)):
                    try:
                        if r and len(b.encode('cp932')) > caps[c]:
                            errs.append(f'row {r} col {c}: {len(b.encode("cp932"))} bytes > cap {caps[c]}')
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
                if r and c < len(caps):
                    try:
                        nb, na = len(b.encode('cp932')), len(a.encode('cp932'))
                    except UnicodeEncodeError:
                        continue  # reported above
                    if nb > caps[c] and not (na > s_caps[c] and nb <= na):
                        errs.append(f'row {r} col {c}: {nb} bytes > cap {caps[c]}')
        if errs:
            bad += 1
            print(f'{name}: {len(errs)} errors')
            for e in errs[:40]:
                print('  ', e)
            continue
        if CHECK_ONLY:
            print(f'{name}: ok (check only, nothing written)')
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(s_nl.join(e_rows).encode('cp932'))
        changed = sum(1 for a, b in zip(s_rows, e_rows) if a != b)
        print(f'{name}: ok, {len(e_rows)} rows, {changed} rows changed -> {out}')
    return 1 if bad else 0


if __name__ == '__main__':
    CHECK_ONLY = '--check' in sys.argv   # 2026-11-03: run every check, write nothing
    sys.exit(main([a for a in sys.argv[1:] if a != '--check']))
