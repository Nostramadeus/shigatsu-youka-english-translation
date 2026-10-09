"""Write English per-scene character totals (文字数1 / 文字数2 / コア文字数) and rescale the 実況 trigger positions.

    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_write.py          # dry run
    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_write.py --write  # write

FIX1, 2026-09-26 (mouse run F9, owner item f; analysis notes/CHARCOUNT-FIX.md). The in-scene plate divides the
ENGLISH running count by the JAPANESE stored total ("3604/1476 chars (244.17%)"). Decision (brief: EN totals
preferred): the stored totals become English, counted from what SHIPS, not from a source tree:

1. For every scene in work/charcount/recipes.py whose work/<id>.lsb exists (= a compiled English build), the
   .lsb is re-extracted with tools/extract_lsb.py into work/_charcount/<id>/ and the recipe's blocks are counted
   with tools/count_chars.py (the engine's own rule, proven on 33/34 rows).
2. Gate: the same recipe on lns/ (Japanese) must reproduce the stored JP 文字数1 / 文字数2 / コア文字数 of the row
   (the one known stale author value, 連番 119 文字数1, is allowed). A failing row is skipped and reported.
3. tsv-en/シナリオデータベース.tsv: only those three columns of those rows change. Old values are kept in
   work/_charcount/jp-totals.tsv (the JP numbers, needed for step 4 on a re-run).
4. データベース/実況/<連番>.tsv (and <連番>分岐.tsv for the 文字数2 route): column 文字数 scaled by EN/JP of the
   matching total, round half up, written CP932 to work/データベース/実況/ (loose-file override). C7/C8 in
   CHARCOUNT-FIX: the trigger positions must move with the totals or a branch-point resume deletes every
   commentary row.
   TEXT SOURCE (lane C1, 2026-09-26): when tsv-en/実況/<name>.tsv exists (UTF-8, same rows and columns as orig;
   a header cell may gain " cha N"), the テキスト column(s) come from it; ID, 顔 (speaker KEY, stays Japanese),
   特殊, コマンド and 文字数 always come from orig, and 文字数 is then rescaled as above. Without a tsv-en file the
   text column stays Japanese. Each table prints "text: tsv-en" or "text: orig". A shape mismatch stops the run.
   Do NOT run tools/build_tsv.py on 実況 tables: it writes the orig (un-rescaled) 文字数 into work/. This script
   is the only builder of work/データベース/実況/.
Then run build_tsv.py シナリオデータベース.tsv, build_navidata.py, build_en_folder.py. Re-run after any recompile
of a scene (the totals follow the shipped text).
"""
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'work' / 'charcount'))
from count_chars import blocks  # noqa: E402
from recipes import R  # noqa: E402

TMP = ROOT / 'work' / '_charcount'
TSV = ROOT / 'tsv-en' / 'シナリオデータベース.tsv'
JK_SRC = ROOT / 'orig' / 'データベース' / '実況'
JK_OUT = ROOT / 'work' / 'データベース' / '実況'
JK_EN = ROOT / 'tsv-en' / '実況'
STALE_OK = {('119', '文字数1')}


def merge_text(rows, name):
    """Return (rows, 'tsv-en'|'orig'): orig rows with the テキスト column(s) replaced from tsv-en/実況/<name>."""
    en = JK_EN / name
    if not en.exists():
        return rows, 'orig'
    et = en.read_bytes().decode('utf-8').lstrip('﻿')
    erows = et.split('\r\n' if '\r\n' in et else '\n')
    if len(erows) != len(rows):
        sys.exit('%s: tsv-en has %d rows, orig %d' % (name, len(erows), len(rows)))
    h, eh = rows[0].split('\t'), erows[0].split('\t')
    if len(h) != len(eh) or any(a != b and not re.fullmatch(re.escape(a) + r' cha \d+', b) for a, b in zip(h, eh)):
        sys.exit('%s: tsv-en header differs from orig' % name)
    tcols = [i for i, x in enumerate(h) if x.split(' ')[0] == 'テキスト']
    out = [rows[0]]
    for j in range(1, len(rows)):
        c, ec = rows[j].split('\t'), erows[j].split('\t')
        if len(c) != len(ec):
            sys.exit('%s row %d: tsv-en has %d columns, orig %d' % (name, j, len(ec), len(c)))
        for i in tcols:
            if i < len(c):
                if c[i].strip() == '' and ec[i] != c[i]:
                    sys.exit('%s row %d: orig text empty but tsv-en %r' % (name, j, ec[i][:30]))
                try:
                    ec[i].encode('cp932')
                except UnicodeEncodeError as ex:
                    sys.exit('%s row %d: not CP932: %r' % (name, j, ex.object[ex.start:ex.end]))
                c[i] = ec[i]
        out.append('\t'.join(c))
    return out, 'tsv-en'


def totals(sid, folder):
    no, b1, b2, res = R[sid]
    d = dict(blocks(sid, folder))
    s = lambda names: sum(d.get(n, 0) for n in names)
    c1 = s(b1)
    c2 = s(b2) if b2 else 0
    core = c1 - s(res) if res else 0
    return c1, c2, core


def extract(sid):
    out = TMP / sid
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*'):
        f.unlink()
    subprocess.run(['uv', 'run', '--no-project', '--with', 'pylivemaker', 'python', str(ROOT / 'tools' / 'extract_lsb.py'),
                    str(ROOT / 'work' / (sid + '.lsb')), '-o', str(out)], check=True, capture_output=True)
    return out.relative_to(ROOT).as_posix()


def main():
    write = '--write' in sys.argv
    TMP.mkdir(parents=True, exist_ok=True)
    raw = TSV.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.split(nl)
    head = lines[0].split('\t')
    C1, C2, CORE = head.index('文字数1'), head.index('文字数2'), head.index('コア文字数')
    rowidx = {ln.split('\t')[0]: k for k, ln in enumerate(lines) if k and ln}
    jpfile = TMP / 'jp-totals.tsv'
    jpstore = {}
    if jpfile.exists():
        for r in csv.reader(jpfile.read_text(encoding='utf-8').splitlines(), delimiter='\t'):
            jpstore[r[0]] = tuple(int(x) for x in r[1:4])
    ratios = {}
    for sid, (no, *_rest) in sorted(R.items(), key=lambda kv: int(kv[1][0])):
        if not (ROOT / 'work' / (sid + '.lsb')).exists():
            print('%-4s %s  skip: not compiled' % (no, sid))
            continue
        cols = lines[rowidx[no]].split('\t')
        stored = jpstore.get(no) or (int(cols[C1]), int(cols[C2]), int(cols[CORE]))
        jp = totals(sid, 'lns')
        bad = [n for n, a, b in zip(('文字数1', '文字数2', 'コア文字数'), jp, stored) if a != b and (no, n) not in STALE_OK]
        if bad:
            print('%-4s %s  GATE FAIL (recipe does not reproduce JP %s: %s vs %s)' % (no, sid, bad, jp, stored))
            continue
        en = totals(sid, extract(sid))
        jpstore[no] = stored
        ratios[no] = (stored, en)
        print('%-4s %s  JP %s -> EN %s' % (no, sid, stored, en))
        cols[C1], cols[C2], cols[CORE] = str(en[0]), str(en[1]), str(en[2])
        lines[rowidx[no]] = '\t'.join(cols)
    # 実況 tables
    jk_rows = []
    for no, (jp, en) in ratios.items():
        for suffix, k in (('', 0), ('分岐', 1)):
            src = JK_SRC / (no + suffix + '.tsv')
            if not src.exists():
                continue
            if jp[k] == 0:
                print('  実況 %s%s: JP total %d is 0, left as is' % (no, suffix, jp[k]))
                continue
            t = src.read_bytes().decode('cp932')
            tnl = '\r\n' if '\r\n' in t else '\n'
            rows, how = merge_text(t.split(tnl), src.name)
            print('  実況 %s: text: %s' % (src.name, how))
            h = rows[0].split('\t')
            ci = h.index('文字数')
            changed = 0
            for j in range(1, len(rows)):
                c = rows[j].split('\t')
                if len(c) > ci and c[ci].strip().isdigit():
                    v = int(c[ci])
                    nv = (v * en[k] * 2 + jp[k]) // (2 * jp[k])
                    if nv != v:
                        c[ci] = str(nv)
                        changed += 1
                    rows[j] = '\t'.join(c)
            jk_rows.append((no + suffix, changed))
            if write:
                JK_OUT.mkdir(parents=True, exist_ok=True)
                (JK_OUT / src.name).write_bytes(tnl.join(rows).encode('cp932'))
    print('実況 tables rescaled:', len(jk_rows), jk_rows)
    if write:
        TSV.write_bytes(nl.join(lines).encode('utf-8'))
        jpfile.write_text(''.join('%s\t%d\t%d\t%d\n' % ((no,) + v) for no, v in sorted(jpstore.items(), key=lambda x: int(x[0]))),
                          encoding='utf-8')
        print('wrote', TSV, 'and', JK_OUT)


if __name__ == '__main__':
    main()
