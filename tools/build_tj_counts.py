"""Build the English ノベルシステム/真呪殺編文字数.txt (True-Jusatsu section character totals).

    uv run --no-project --python 3.12 --with pylivemaker python tools/build_tj_counts.py          # dry run
    uv run --no-project --python 3.12 --with pylivemaker python tools/build_tj_counts.py --write  # write

Counter repair 2026-10-29 (Lane A, work/feedback-repair-20261029/COUNTERS-PLAN.md D7 + orchestrator item 2).
Why: in the True-Jusatsu arc the in-scene plate divides the running count by パートテキスト数, which
00000E7B idx 108-151 reads from this file (field [section + 4]); 00000E7B idx 153-184 seeds the scene counter
文字数誤差 on a mid-arc start with the sum of the earlier sections' fields; 0000001C idx 2715-2718 / 2806-2809 show the
selected section's field on the section picker. The running count is English, so every number in the file must be
an English count of the same section route, counted with tools/count_chars.py like 文字数1 (tools/charcount_write.py).

Source: orig/ノベルシステム/真呪殺編文字数.txt (CP932). Line: 連番, title, N sections, opening (section -1),
section 0..N-1, zero padding (20 fields). Only the opening and section fields change; 連番, title, N and padding are
copied, as are the newlines. Routes: TJ / TJ_STALE in tools/charcount_recipes.py.
Gates (any failure refuses the whole file; nothing is written):
  - every line's 連番 has a TJ route and N equals the number of section routes; every TJ row has a line;
  - each JP field reproduces from lns/ with its route, or differs by exactly TJ_STALE;
  - every route block exists in lns/ and in the extraction of the shipped work/<id>.lsb, none carries <VAR>;
  - the English sections 0..N add up to the English 文字数1 of that row in tsv-en/シナリオデータベース.tsv
    (run tools/charcount_write.py first; a mismatch means one of the two is stale).
Output: work/ノベルシステム/真呪殺編文字数.txt (CP932), shipped by tools/ship-list.txt. Idempotent.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import charcount_write as cw  # noqa: E402
from charcount_recipes import TJ, TJ_STALE  # noqa: E402

REL = Path('ノベルシステム') / '真呪殺編文字数.txt'


def route_counts(bm, opening, sections):
    """[opening, section 0, ...] counts, plus missing / <VAR> block names."""
    groups = [opening] + list(sections)
    names = [n for g in groups for n in g]
    missing = sorted({n for n in names if n not in bm})
    var = sorted({n for n in names if n in bm and bm[n][1]})
    return [sum(bm[n][0] for n in g if n in bm) for g in groups], missing, var


def run(paths=None, write=False, log=print, require_all=True, extracted=None):
    """Returns {'rows': {連番: (jp fields, en fields)}, 'refused': [reasons], 'changed': bool}.
    require_all=False and a shared `extracted` set are test hooks (a one-line file; one extraction per script)."""
    paths = paths or cw.Paths()
    src = paths.root / 'orig' / REL
    out = paths.root / 'work' / REL
    raw = src.read_bytes().decode('cp932')
    nl = cw.old_nl(raw)
    lines = raw.split(nl)
    parsed, refused = [], []
    seen = set()
    for k, ln in enumerate(lines):
        if not ln.strip():
            continue
        f = ln.split(',')
        no = f[0]
        seen.add(no)
        if no not in TJ:
            refused.append('line %d: 連番 %s has no TJ route' % (k, no))
            continue
        sid, opening, sections = TJ[no]
        n = int(f[2])
        if n != len(sections) or len(f) < 4 + n:
            refused.append('%s: %d sections in the file, %d routes' % (no, n, len(sections)))
            continue
        stored = [int(x) for x in f[3:4 + n]]
        jp, missing, var = route_counts(cw.block_map(paths.lns, sid), opening, sections)
        if missing or var:
            refused.append('%s: JP blocks missing %s / with <VAR> %s' % (no, missing, var))
            continue
        bad = ['section %d: file %d, route %d' % (i - 1, s, j) for i, (s, j) in enumerate(zip(stored, jp))
               if s - j != TJ_STALE.get((no, i - 1), 0)]
        if bad:
            refused.append('%s: JP gate: ' % no + '; '.join(bad))
            continue
        parsed.append((k, f, no, sid, n, stored))
    missing_rows = sorted(set(TJ) - seen)
    if missing_rows and require_all:
        refused.append('TJ rows without a line in the file: %s' % missing_rows)
    result = {'rows': {}, 'refused': refused, 'changed': False}
    if refused:
        for r in refused:
            log('REFUSED ' + r)
        return result
    tab = cw.Table(paths.tsv)
    extracted = set() if extracted is None else extracted
    for k, f, no, sid, n, stored in parsed:
        _, opening, sections = TJ[no]
        en, missing, var = route_counts(cw.block_map(cw.extract(paths, sid, extracted), sid), opening, sections)
        total = int(tab.cells(no)[tab.col('文字数1')] or 0)
        if missing or var:
            refused.append('%s: EN blocks missing %s / with <VAR> %s' % (no, missing, var))
        elif sum(en[1:]) != total:
            refused.append('%s: EN sections add up to %d, tsv-en 文字数1 is %d (run tools/charcount_write.py)'
                           % (no, sum(en[1:]), total))
        result['rows'][no] = (stored, en)
        lines[k] = ','.join(f[:3] + [str(x) for x in en] + f[4 + n:])
        log('%s %s  opening %d -> %d; sections JP %d -> EN %d (= 文字数1)' % (no, sid, stored[0], en[0],
                                                                         sum(stored[1:]), sum(en[1:])))
    if refused:
        for r in refused:
            log('REFUSED ' + r)
        result['rows'] = {}
        return result
    text = nl.join(lines)
    old = out.read_bytes() if out.exists() else None
    result['changed'] = old != text.encode('cp932')
    if write:
        if result['changed']:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(text.encode('cp932'))
            log('wrote %s' % out)
        else:
            log('%s unchanged' % out)
    else:
        log('dry run: nothing written (%s would %s)' % (out, 'change' if result['changed'] else 'stay as is'))
    return result


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    r = run(write='--write' in argv)
    return 1 if r['refused'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
