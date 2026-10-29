"""Write English per-scene character totals (文字数1 / 文字数2 / コア文字数) and rescale the 実況 trigger positions.

    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_write.py          # dry run
    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_write.py --write  # write
    ... tools/charcount_write.py --only 0000107B,00002444   # limit to these lsb ids (scenario and hidden)

FIX1, 2026-09-26 (mouse run F9, owner item f; analysis notes/CHARCOUNT-FIX.md). The in-scene plate divides the
ENGLISH running count by the JAPANESE stored total ("3604/1476 chars (244.17%)"). Decision (brief: EN totals
preferred): the stored totals become English, counted from what SHIPS, not from a source tree.
Counter repair, 2026-10-29 (Lane A, work/feedback-repair-20261029/COUNTERS-PLAN.md): the recipes moved to
tools/charcount_recipes.py (34 old + 163 new scenario rows, 18 hidden rows) and this script also writes
tsv-en/裏ルート.tsv.

1. For every recipe (R: scenario rows, H: hidden rows) whose work/<id>.lsb exists (= a compiled English build), the
   .lsb is re-extracted with tools/extract_lsb.py into work/_charcount/<id>/ and the recipe's blocks are counted
   with tools/count_chars.py (the engine's own rule).
2. Gates, all must pass or the row is skipped and reported (it then stays Japanese):
   a. the stored JP value (work/_charcount/jp-totals.tsv / jp-hidden-totals.tsv, else the table cell) equals the
      orig/データベース table (CP932) - so an EN value is never mistaken for JP;
   b. the same recipe on lns/ (Japanese) reproduces the stored JP 文字数1 / 文字数2 / コア文字数 of the row, or
      differs by exactly the residual recorded in STALE_OK;
   c. every recipe block exists in lns/ and in the extracted English script (a renamed or missing block would
      otherwise count 0 silently);
   d. no recipe block contains a <VAR> tag in JP or EN (runtime substitution, length unknown: UNRESOLVED-VAR).
   The 8 first-arc rows (FIRST_ARC_OWNED) belong to tools/repair_first_arc_totals.py and are skipped here.
3. tsv-en/シナリオデータベース.tsv and tsv-en/裏ルート.tsv: only those three columns of those rows change (checked
   cell by cell before writing). Old JP values are kept in work/_charcount/jp-totals.tsv (scenario) and
   work/_charcount/jp-hidden-totals.tsv (hidden) so a re-run gates against JP, not against its own output.
4. データベース/実況/<連番>.tsv (and <連番>分岐.tsv for the 文字数2 route): column 文字数 scaled by EN/JP of the
   matching scenario total, round half up, where JP is the recipe's reproduced JP (the same blocks the EN total
   counts; it differs from the stored author value only for STALE_OK rows - 2026-10-29: row 169's stored 3117
   leaves out its red-box block while the author's trigger positions run to 3580, so EN/3117 would push the last
   commentary past the end of the scene; EN/3429 keeps the author's proportions), written CP932 to work/データベース/実況/ (loose-file override). C7/C8 in
   CHARCOUNT-FIX: the trigger positions must move with the totals or a branch-point resume deletes every
   commentary row. Hidden rows never rescale 実況: the tables are keyed by 連番 and are loaded for the scenario
   route (0000001C idx 1165-1172), so they follow the scenario row's ratio.
   TEXT SOURCE (lane C1, 2026-09-26): when tsv-en/実況/<name>.tsv exists (UTF-8, same rows and columns as orig;
   a header cell may gain " cha N"), the テキスト column(s) come from it; ID, 顔 (speaker KEY, stays Japanese),
   特殊, コマンド and 文字数 always come from orig, and 文字数 is then rescaled as above. Without a tsv-en file the
   text column stays Japanese. Each table prints "text: tsv-en" or "text: orig". A shape mismatch stops the run.
   Do NOT run tools/build_tsv.py on 実況 tables: it writes the orig (un-rescaled) 文字数 into work/. This script
   is the only builder of work/データベース/実況/.
Then run build_tsv.py シナリオデータベース.tsv 裏ルート.tsv, build_navidata.py, build_en_folder.py. Re-run after any
recompile of a scene (the totals follow the shipped text).
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from count_chars import body, count_text  # noqa: E402
from charcount_recipes import FIRST_ARC_OWNED, H, R, STALE_OK, UNRESOLVED  # noqa: E402

COLS = ('文字数1', '文字数2', 'コア文字数')
VAR = re.compile(r'<VAR\b', re.IGNORECASE)


class Paths:
    """Every file this script reads or writes, relative to one project root (tests use a temporary root)."""

    def __init__(self, root=ROOT):
        root = Path(root)
        self.root = root
        self.tmp = root / 'work' / '_charcount'
        self.tsv = root / 'tsv-en' / 'シナリオデータベース.tsv'
        self.hid = root / 'tsv-en' / '裏ルート.tsv'
        self.orig_tsv = root / 'orig' / 'データベース' / 'シナリオデータベース.tsv'
        self.orig_hid = root / 'orig' / 'データベース' / '裏ルート.tsv'
        self.jk_src = root / 'orig' / 'データベース' / '実況'
        self.jk_out = root / 'work' / 'データベース' / '実況'
        self.jk_en = root / 'tsv-en' / '実況'
        self.lns = root / 'lns'
        self.work = root / 'work'
        self.jpfile = self.tmp / 'jp-totals.tsv'
        self.jphfile = self.tmp / 'jp-hidden-totals.tsv'


class Table:
    """A tsv-en table kept as raw lines so that only the edited cells change (newline style, empty cells kept)."""

    def __init__(self, path, enc='utf-8'):
        self.path = path
        self.raw = path.read_bytes().decode(enc)
        self.nl = '\r\n' if '\r\n' in self.raw else '\n'
        self.lines = self.raw.split(self.nl)
        self.head = self.lines[0].split('\t')
        self.rowidx = {ln.split('\t')[0]: k for k, ln in enumerate(self.lines) if k and ln}

    def col(self, name):
        return self.head.index(name)

    def cells(self, key):
        return self.lines[self.rowidx[key]].split('\t')

    def set(self, key, values):
        c = self.cells(key)
        for name, v in zip(COLS, values):
            c[self.col(name)] = str(v)
        self.lines[self.rowidx[key]] = '\t'.join(c)

    def text(self):
        return self.nl.join(self.lines)


def check_only_totals(old, new, label):
    """Refuse a write that changes anything but the three total columns."""
    a, b = old.split(old_nl(old)), new.split(old_nl(old))
    if len(a) != len(b):
        sys.exit('%s: line count changed' % label)
    head = a[0].split('\t')
    allowed = {head.index(c) for c in COLS}
    for k, (x, y) in enumerate(zip(a, b)):
        if x == y:
            continue
        cx, cy = x.split('\t'), y.split('\t')
        if len(cx) != len(cy) or any(i not in allowed for i, (p, q) in enumerate(zip(cx, cy)) if p != q):
            sys.exit('%s line %d: a cell outside %s would change' % (label, k, '/'.join(COLS)))


def old_nl(text):
    return '\r\n' if '\r\n' in text else '\n'


def block_map(folder, sid):
    """{block name: (chars, has_var)} for every <sid>-<name>.lns in folder (zero-length blocks included)."""
    out = {}
    for f in sorted(Path(folder).glob(sid + '-*.lns')):
        t = body(f)
        out[f.name.split('-', 1)[1][:-4]] = (count_text(t), bool(VAR.search(t)))
    return out


def recipe_totals(bm, b1, b2, res):
    """((文字数1, 文字数2, コア文字数), [missing block names], [blocks with <VAR>])."""
    names = list(b1) + list(b2 or []) + list(res or [])
    missing = sorted({n for n in names if n not in bm})
    var = sorted({n for n in names if n in bm and bm[n][1]})
    s = lambda ns: sum(bm[n][0] for n in ns if n in bm)  # noqa: E731
    c1 = s(b1)
    return (c1, s(b2) if b2 else 0, c1 - s(res) if res else 0), missing, var


def extract(paths, sid, done=None):
    """Re-extract the shipped work/<sid>.lsb with tools/extract_lsb.py into work/_charcount/<sid>/ (emptied first).
    `done` (a set) skips a script already extracted in this run (hidden rows 14-17 share one script)."""
    from extract_lsb import extract as lsb_extract  # needs pylivemaker (uv run --with pylivemaker)
    out = paths.tmp / sid
    if done is not None:
        if sid in done:
            return out
        done.add(sid)
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*'):
        f.unlink()
    lsb_extract(paths.work / (sid + '.lsb'), out)
    return out


def read_store(path):
    store = {}
    if path.exists():
        for r in csv.reader(path.read_text(encoding='utf-8').splitlines(), delimiter='\t'):
            store[r[0]] = tuple(int(x) for x in r[1:4])
    return store


def orig_totals(path, keycol=0):
    raw = path.read_bytes().decode('cp932')
    lines = raw.split(old_nl(raw))
    head = lines[0].split('\t')
    idx = [head.index(c) for c in COLS]
    out = {}
    for ln in lines[1:]:
        c = ln.split('\t')
        if ln and len(c) > max(idx):
            out[c[keycol]] = tuple(int(c[i]) if c[i].strip().lstrip('-').isdigit() else 0 for i in idx)
    return out


def merge_text(paths, rows, name):
    """Return (rows, 'tsv-en'|'orig'): orig rows with the テキスト column(s) replaced from tsv-en/実況/<name>."""
    en = paths.jk_en / name
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


def gate_row(label, no, recipe, stored, orig, paths, sid):
    """JP gates for one row; returns (None, reproduced JP) when they pass, else (reason, None)."""
    b1, b2, res = recipe
    if orig is None:
        return 'no orig row', None
    if stored != orig:
        return 'stored JP %s differs from orig table %s' % (stored, orig), None
    jp, missing, var = recipe_totals(block_map(paths.lns, sid), b1, b2, res)
    if missing:
        return 'JP blocks missing in lns/: %s' % missing, None
    if var:
        return 'UNRESOLVED-VAR (JP): %s' % var, None
    bad = []
    for name, a, b in zip(COLS, jp, stored):
        want = STALE_OK.get((no, name), (0, ''))[0] if label == 'scenario' else 0
        if b - a != want:
            bad.append('%s computed %d stored %d (allowed residual %+d)' % (name, a, b, want))
    if bad:
        return 'GATE FAIL: recipe does not reproduce JP: ' + '; '.join(bad), None
    return None, jp


def run(paths=None, write=False, only=None, log=print):
    """Compute (and with write=True store) the English totals. Returns a summary dict."""
    paths = paths or Paths()
    paths.tmp.mkdir(parents=True, exist_ok=True)
    summary = {'scenario': {}, 'hidden': {}, 'skipped': {}, 'jk': []}
    extracted = set()
    # ---------------------------------------------------------------- scenario rows
    tab = Table(paths.tsv)
    orig = orig_totals(paths.orig_tsv)
    jpstore = read_store(paths.jpfile)
    ratios = {}
    for no in FIRST_ARC_OWNED:
        log('%-4s skip: first-arc row, owned by tools/repair_first_arc_totals.py' % no)
    for no, why in UNRESOLVED.items():
        log('%-4s skip: UNRESOLVED (%s)' % (no, why))
    for sid, (no, b1, b2, res) in sorted(R.items(), key=lambda kv: int(kv[1][0])):
        if only and sid not in only:
            continue
        if no in FIRST_ARC_OWNED:
            sys.exit('%s: first-arc row %s must not have a recipe here' % (sid, no))
        if not (paths.work / (sid + '.lsb')).exists():
            log('%-4s %s  skip: not compiled' % (no, sid))
            summary['skipped'][no] = 'not compiled'
            continue
        if no not in tab.rowidx:
            sys.exit('%s: 連番 %s not in %s' % (sid, no, paths.tsv.name))
        cols = tab.cells(no)
        cur = tuple(int(cols[tab.col(c)] or 0) for c in COLS)
        stored = jpstore.get(no) or cur
        why, jp = gate_row('scenario', no, (b1, b2, res), stored, orig.get(no), paths, sid)
        if why is None:
            en, missing, var = recipe_totals(block_map(extract(paths, sid, extracted), sid), b1, b2, res)
            if missing:
                why = 'EN blocks missing in the compiled script: %s' % missing
            elif var:
                why = 'UNRESOLVED-VAR (EN): %s' % var
        if why:
            log('%-4s %s  %s' % (no, sid, why))
            summary['skipped'][no] = why
            continue
        jpstore[no] = stored
        ratios[no] = (jp, en)     # 実況 ratio: EN over the JP of the SAME blocks (= stored unless STALE_OK)
        summary['scenario'][no] = (stored, en)
        log('%-4s %s  JP %s -> EN %s' % (no, sid, stored, en))
        tab.set(no, en)
    # ---------------------------------------------------------------- hidden rows (tsv-en/裏ルート.tsv)
    htab = Table(paths.hid)
    horig = orig_totals(paths.orig_hid)
    hstore = read_store(paths.jphfile)
    for hid, (no, sid, b1, b2, res) in sorted(H.items(), key=lambda kv: int(kv[0])):
        if only and sid not in only:
            continue
        if hid not in htab.rowidx or htab.cells(hid)[htab.col('連番')] != no:
            sys.exit('hidden %s: row missing or 連番 is not %s' % (hid, no))
        if not (paths.work / (sid + '.lsb')).exists():
            log('h%-3s %s  skip: not compiled' % (hid, sid))
            summary['skipped']['h' + hid] = 'not compiled'
            continue
        cols = htab.cells(hid)
        cur = tuple(int(cols[htab.col(c)] or 0) for c in COLS)
        stored = hstore.get(hid) or cur
        why, jp = gate_row('hidden', no, (b1, b2, res), stored, horig.get(hid), paths, sid)
        if why is None:
            en, missing, var = recipe_totals(block_map(extract(paths, sid, extracted), sid), b1, b2, res)
            if missing:
                why = 'EN blocks missing in the compiled script: %s' % missing
            elif var:
                why = 'UNRESOLVED-VAR (EN): %s' % var
        if why:
            log('h%-3s %s  %s' % (hid, sid, why))
            summary['skipped']['h' + hid] = why
            continue
        hstore[hid] = stored
        summary['hidden'][hid] = (stored, en)
        log('h%-3s %s  (連番 %s) JP %s -> EN %s; 実況: not rescaled (keyed by 連番, follows the scenario row)'
            % (hid, sid, no, stored, en))
        htab.set(hid, en)
    # ---------------------------------------------------------------- 実況 tables
    for no, (jp, en) in ratios.items():
        for suffix, k in (('', 0), ('分岐', 1)):
            src = paths.jk_src / (no + suffix + '.tsv')
            if not src.exists():
                continue
            if jp[k] == 0:
                log('  実況 %s%s: JP total %d is 0, left as is' % (no, suffix, jp[k]))
                continue
            t = src.read_bytes().decode('cp932')
            tnl = old_nl(t)
            rows, how = merge_text(paths, t.split(tnl), src.name)
            log('  実況 %s: text: %s' % (src.name, how))
            ci = rows[0].split('\t').index('文字数')
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
            summary['jk'].append((no + suffix, changed))
            if write:
                paths.jk_out.mkdir(parents=True, exist_ok=True)
                (paths.jk_out / src.name).write_bytes(tnl.join(rows).encode('cp932'))
    no_jk = [no for no in ratios if not any((paths.jk_src / (no + s + '.tsv')).exists() for s in ('', '分岐'))]
    log('実況 tables rescaled: %d %s' % (len(summary['jk']), summary['jk']))
    log('rows with a new total and no 実況 table: %d' % len(no_jk))
    log('scenario rows: %d EN; hidden rows: %d EN; skipped: %d %s' % (
        len(summary['scenario']), len(summary['hidden']), len(summary['skipped']), sorted(summary['skipped'])))
    new_s, new_h = tab.text(), htab.text()
    check_only_totals(tab.raw, new_s, paths.tsv.name)
    check_only_totals(htab.raw, new_h, paths.hid.name)
    summary['changed'] = (new_s != tab.raw, new_h != htab.raw)
    if write:
        if new_s != tab.raw:
            paths.tsv.write_bytes(new_s.encode('utf-8'))
        if new_h != htab.raw:
            paths.hid.write_bytes(new_h.encode('utf-8'))
        paths.jpfile.write_text(''.join('%s\t%d\t%d\t%d\n' % ((no,) + v) for no, v in
                                        sorted(jpstore.items(), key=lambda x: int(x[0]))), encoding='utf-8')
        paths.jphfile.write_text(''.join('%s\t%d\t%d\t%d\n' % ((h,) + v) for h, v in
                                         sorted(hstore.items(), key=lambda x: int(x[0]))), encoding='utf-8')
        log('wrote %s, %s, %s' % (paths.tsv, paths.hid, paths.jk_out))
    else:
        log('dry run: nothing written (tables would change: scenario %s, hidden %s)' % summary['changed'])
    return summary


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    only = None
    if '--only' in argv:
        only = set(argv[argv.index('--only') + 1].split(','))
    run(write='--write' in argv, only=only)


if __name__ == '__main__':
    main()
