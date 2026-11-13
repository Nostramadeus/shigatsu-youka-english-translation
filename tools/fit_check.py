"""Text-fit checker for the English build of Shigatsu Youka (implements notes/FIT-MODEL-2.md section 3).

    PYTHONUTF8=1 uv run --no-project --python 3.12 --with pylivemaker --with pillow python tools/fit_check.py

Windows only (GDI through ctypes; no window is opened). Order of a run:
  1. self-check: the 81 observed screen lines of the calibration (spec 3.1). Exit 1 if not 81 of 81.
  2. read the surface registry tools/fit_surfaces.tsv (spec 3.2, 3.6).
  3. check every cell of every registry surface (spec 3.3 to 3.5); Japanese is run through the same surface for every English CLIP.
  4. write work/fitcheck/findings.tsv (every row that is not OK), SUMMARY.md, run.log; compare with the reference results of spec 3.7.

The model code is tools/fit_model.py + tools/fit_gdi.py (copies of work/feedback-20261113/fit/model.py and gdi.py; only the
import lines changed). Registry columns are the ones of spec 3.2 plus jp_face, jp_size, jp_bold, jp_column. `table` and `column`
hold ';' separated lists that line up by position (one column entry is used for all tables); a column is a regular expression
over the header names (text before the first space). Tables: tsv-en/<table>.tsv, Japanese: notes/_db/<table>.tsv, same row key.
"""
import math
import re
import sys
import time
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(r'F:\Projects\shigatsu-youka-en')
TOOLS = ROOT / 'tools'
sys.path.insert(0, str(TOOLS))
sys.stdout.reconfigure(encoding='utf-8')

import fit_model as M  # noqa: E402

OUT = ROOT / 'work' / 'fitcheck'
OUT.mkdir(parents=True, exist_ok=True)
TSV_EN = ROOT / 'tsv-en'
TSV_JP = ROOT / 'notes' / '_db'
DUMP = ROOT / 'work' / 'feedback-20261113' / 'fit' / 'dump'
IMG = ROOT / 'reader' / 'img' / 'グラフィック' / 'リファレンス' / 'リファレンス詳細'
UI_IDS = {'0000001C', '0000001E', '000000F2', '00001878', '0000189A', '000018BF', '000019DD', '00001F8A', '00001FBE'}

_LOG = open(OUT / 'run.log', 'w', encoding='utf-8')


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    _LOG.write(s + '\n')
    _LOG.flush()


# ------------------------------------------------------------------ 1. self-check (spec 3.1)
def self_check():
    import fit_calib_sets as C
    total = bad = 0
    for s in C.SETS:
        f = M.font(s['face'], s['h'])
        k = M.K(s['shadow'], s['border'])
        got = M.wrap(s['text'], f, k, s['W'], limit=s['W'], rule='space')
        obs = s.get('tail') or s.get('head')
        seg = got[-len(obs):] if 'tail' in s else got[:len(obs)]
        n_bad = sum(a != b for a, b in zip(seg, obs)) + abs(len(seg) - len(obs))
        total += len(obs)
        bad += n_bad
        log('  self-check set %-70s %s' % (s['name'][:70], 'ALL %d LINES MATCH' % len(obs) if not n_bad else 'MISMATCH %d' % n_bad))
    line = 'TOTAL observed lines %d, reproduced %d, different %d' % (total, total - bad, bad)
    log(line)
    return total == 81 and bad == 0


# ------------------------------------------------------------------ registry (spec 3.2)
def lst(v):
    return [] if v in ('-', '') else v.split(';')


def num(v, default=None):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


class Surface:
    pass


def load_registry():
    lines = (TOOLS / 'fit_surfaces.tsv').read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')
    cols = lines[0].split('\t')
    out = []
    for ln in lines[1:]:
        if not ln.strip() or ln.startswith('#'):
            continue
        d = dict(zip(cols, ln.split('\t')))
        s = Surface()
        s.__dict__.update(d)
        s.size_n = num(d['size'])
        s.bold_n = num(d['bold'], 0)
        s.shadow_n = num(d['shadow'], 0)
        s.border_n = num(d['border'], 0)
        s.ls_n = num(d['linespace'], 0)
        s.width_n = num(d['width'])
        room = lst(d['room'])
        s.room_n = num(room[0]) if room else None
        s.room_opts = dict(x.split('=', 1) for x in room[1:])
        s.jp_shadow_n = num(d['jp_shadow'], 0)
        s.jp_border_n = num(d['jp_border'], 0)
        s.jp_size_n = num(d['jp_size'], s.size_n)
        s.jp_bold_n = num(d['jp_bold'], 0)
        s.start_n = num(d['start_x'])
        lim = lst(d['limit_x'])
        s.limit_base = num(lim[0]) if lim else None
        s.limit_rules = []
        for x in lim[1:]:
            cond, v = x.split(':')
            c, val = cond.split('=')
            s.limit_rules.append((c, val, int(v)))
        out.append(s)
    return out


def unesc(s):
    return s.replace('\\n', '\n').replace('\\u3000', '\u3000')


# ------------------------------------------------------------------ tables
class Tab:
    def __init__(self, path, keyname=None):
        text = path.read_text(encoding='utf-8').lstrip('\ufeff').replace('\r\n', '\n')
        lines = text.split('\n')
        self.hdr = [c.split(' ')[0] for c in lines[0].split('\t')]
        self.rows = []
        for ln in lines[1:]:
            if not ln.strip():
                continue
            c = ln.split('\t')
            c += [''] * (len(self.hdr) - len(c))
            self.rows.append(c)
        kn = keyname if keyname in self.hdr else ('ID' if 'ID' in self.hdr else self.hdr[0])
        self.kcol = self.hdr.index(kn)
        self.by_key = defaultdict(list)
        self.occ = []
        for r in self.rows:
            k = r[self.kcol]
            self.occ.append(len(self.by_key[k]))
            self.by_key[k].append(r)

    def get(self, row, name):
        if row is None or name not in self.hdr:
            return ''
        return row[self.hdr.index(name)]

    def match(self, regex):
        return [i for i, h in enumerate(self.hdr) if re.fullmatch(regex, h)]


_tabs = {}


def load(base, rel):
    key = (str(base), rel)
    if key not in _tabs:
        p = base / (rel + '.tsv')
        if base == TSV_JP and '/' in rel:
            p = base / (rel.replace('/', '__') + '.tsv')
        _tabs[key] = Tab(p, '表示順') if rel.startswith('人物/') else (Tab(p) if p.exists() else None)
    return _tabs[key]


def expand(name):
    if name.endswith('/*'):
        d = name[:-2]
        return [d + '/' + p.stem for p in sorted((TSV_EN / d).glob('*.tsv'))]
    return [name]


# ------------------------------------------------------------------ text preparation (spec 3.3)
MARK = re.compile(r'/[^/\s]*[^\x00-\x7f][^/\s]*/')


def prep(s, side='en'):
    """Returns text, or None when the cell holds a variable marker other than /立木/ (NOT_MODELLED)."""
    s = s.replace('\\r\\n', '\n').replace('\\n', '\n')
    if side == 'en':
        s = s.replace('/立木/', 'you')
        if MARK.search(s):
            return None
    return s


def template(script, idx, side):
    """Text template of a TextIns from the script dump: <BR> = new line, <VAR NAME="x"> = {x}, other tags dropped."""
    path = DUMP / ('%s-%s.txt' % (side, script))
    for ln in path.read_text(encoding='utf-8').split('\n'):
        f = ln.split('\t', 4)
        if len(f) == 5 and f[0] == str(idx) and f[3] == 'TextIns':
            body = f[4].split('BEGIN DECOMPILED SCRIPT', 1)[1]
            body = body.split('END DECOMPILED SCRIPT', 1)[0]
            body = body.split('<SCENARIO VER="105">', 1)[1]
            body = re.sub(r'\\r\\n;-*', '', body)
            body = body.replace('\\r\\n', '')
            body = body.replace('<BR>', '\n')
            body = re.sub(r'<VAR NAME="([^"]+)"[^>]*>', r'{\1}', body)
            return re.sub(r'<(?!BR)[^>]*>', '', body).rstrip(' ')
    raise SystemExit('template idx %s not found in %s' % (idx, path))


def chars_line(script, idx, side):
    path = DUMP / ('%s-%s.txt' % (side, script))
    for ln in path.read_text(encoding='utf-8').split('\n'):
        f = ln.split('\t', 4)
        if len(f) == 5 and f[0] == str(idx):
            m = re.search(r'概要用ノード文字数 = "([^"]*)" \+\+ DBGetStr\("文字数"\) \+\+ "([^"]*)"', f[4])
            if m:
                return m.group(1), m.group(2)
    raise SystemExit('chars line idx %s not found in %s' % (idx, path))


# ------------------------------------------------------------------ evaluation (spec 3.4, 3.5)
def mes_metrics(S, text, side, width=None):
    if side == 'en':
        face, size, bold, sh, bo = S.face, S.size_n, S.bold_n, S.shadow_n, S.border_n
    else:
        face, size, bold, sh, bo = S.jp_face, S.jp_size_n, S.jp_bold_n, S.jp_shadow_n, S.jp_border_n
    f = M.font(face, size, bool(bold))
    k = M.K(sh, bo)
    pitch = M.pitch(size, S.ls_n, sh, bo)
    gh = size + sh + 2 * bo
    w = S.width_n if width is None else width
    lines = M.wrap(text, f, k, w)
    widest = max(M.width(ln, f, k) for ln in lines) if lines else 0
    return dict(f=f, k=k, pitch=pitch, gh=gh, lines=lines, n=len(lines), widest=widest)


def capacity(room, gh, pitch):
    if room is None:
        return None
    return (room - gh) // pitch + 1 if room >= gh else 0


def mes_verdict(S, text, side, room):
    """-> (verdict, n_lines, capacity, widest, extra)"""
    m = mes_metrics(S, text, side)
    cap = capacity(room, m['gh'], m['pitch'])
    n = m['n']
    kind = S.kind
    if kind == 'PAGE':
        if n <= cap:
            return 'OK', n, cap, m['widest'], ''
        return 'PAGES', n, cap, m['widest'], 'pages=%d' % math.ceil(n / cap) if cap else 'pages=?'
    if kind == 'CLIP':
        if n > cap:
            return 'CLIP', n, cap, m['widest'], ''
        n3 = len(M.wrap(text, m['f'], m['k'], S.width_n - 3))
        if n3 > cap:
            return 'TIGHT', n, cap, m['widest'], ''
        return 'OK', n, cap, m['widest'], ''
    return 'OK', n, cap, m['widest'], ''   # SCROLL


def caption_px(text, face, size, bold):
    f = M.font(face, size, bool(bold))
    lines = text.replace('\r\n', '\n').split('\n')
    return max(M.width(ln, f, 0) for ln in lines)


def caption_verdict(px, limit):
    if px > limit:
        return 'CLIP'
    if px > limit - 3:
        return 'TIGHT'
    return 'OK'


# ------------------------------------------------------------------ cells of a registry surface
def en_cells(S):
    """Yield one dict per non-empty English cell for table/column surfaces."""
    tabs = lst(S.table)
    cols = lst(S.column)
    for ti, tname in enumerate(tabs):
        colre = cols[ti] if len(cols) > 1 else cols[0]
        for name in expand(tname):
            tab = load(TSV_EN, name)
            for ri, row in enumerate(tab.rows):
                for ci in tab.match(colre):
                    if row[ci].strip() == '':
                        continue
                    yield dict(ti=ti, name=name, tab=tab, row=row, ri=ri, key=row[tab.kcol], col=tab.hdr[ci], ci=ci, cell=row[ci])


def jp_row(ctx):
    jt = load(TSV_JP, ctx['name'])
    if jt is None:
        return None, None
    rows = jt.by_key.get(ctx['key'], [])
    occ = ctx['tab'].occ[ctx['ri']]
    return jt, (rows[occ] if occ < len(rows) else None)


def affix(S, base, tab, row, extra):
    pre = S.prefix if S.prefix not in ('-', '') and not S.prefix.startswith('@') else ''
    suf = S.suffix if S.suffix not in ('-', '') else ''

    def sub(m):
        t = m.group(0)[1:-1]
        if '?' in t:
            col, txt = t.split('?', 1)
            v = tab.get(row, col) if tab is not None else ''
            return (unesc(txt) + v) if v.strip() else ''
        return str(extra.get(t, ''))

    pre = re.sub(r'\{[^}]*\}', sub, unesc(pre)) if pre else ''
    suf = re.sub(r'\{[^}]*\}', sub, unesc(suf)) if suf else ''
    return pre + base + suf


_tpl = {}


def compose_ref(tab, row, side):
    if side not in _tpl:
        pre, post = chars_line('0000001E', 518, 'en' if side == 'en' else 'jp')
        _tpl[side] = (template('0000001E', 529, 'en' if side == 'en' else 'jp'), pre, post)
    tpl, pre, post = _tpl[side]
    g = lambda c: tab.get(row, c)
    vals = {'概要用解禁編': g('解禁編'), '概要用シナリオ': g('解禁シナリオ'), '概要用解禁人物': g('解禁人物'),
            '概要用解禁条件': g('解禁条件'), '概要用概要': g('概要'), '概要用ノード文字数': pre + g('文字数') + post}
    return re.sub(r'\{([^}]+)\}', lambda m: vals.get(m.group(1), ''), tpl)


def node_room(S, ctx):
    n = re.match(r'\d+', ctx['col']).group(0)
    sp = ctx['tab'].get(ctx['row'], n + '特殊処理')
    if '拡大' not in sp:
        return S.room_n, ''
    c = list((IMG / ('rrr' + ctx['key'])).glob('部分拡大%s.*' % n))
    if not c:
        return None, 'no zoom picture rrr%s/部分拡大%s' % (ctx['key'], n)
    from PIL import Image
    ih = Image.open(c[0]).size[1]
    return 475 - ih, 'picture_h=%d' % ih


# ------------------------------------------------------------------ results
class Result:
    def __init__(self):
        self.counts = defaultdict(Counter)       # surface -> verdict counts
        self.classes = defaultdict(Counter)      # surface -> class counts (CLIP rows)
        self.rows = []                           # findings rows
        self.only = []                           # ENGLISH_ONLY CLIP rows
        self.cells = Counter()
        self.info = defaultdict(list)

    def add(self, surface, table, key, col, px, cap, widest, verdict, jp_n, jp_cap, jp_v, cls, text, info=''):
        self.cells[surface] += 1
        self.counts[surface][verdict] += 1
        if cls and verdict == 'CLIP':
            self.classes[surface][cls] += 1
        if verdict != 'OK':
            row = [surface, table, key, col, 'en', px, cap if cap is not None else '', widest, verdict,
                   '' if jp_n is None else jp_n, '' if jp_cap is None else jp_cap, jp_v or '', cls or '',
                   text.replace('\n', ' / ').replace('\t', ' ')[:60], info]
            self.rows.append(row)
            if cls == 'ENGLISH_ONLY':
                self.only.append((surface, table, key, col, px, cap))


def jp_class_mes(S, jtext, room):
    """Japanese through the same surface. -> (verdict, lines, capacity, class)"""
    if jtext is None or jtext.strip() == '':
        return 'OK', 0, None, 'ENGLISH_ONLY'
    v, n, cap, w, _ = mes_verdict(S, jtext, 'jp', room)
    if n in (cap, cap + 1):
        cls = 'JP_UNSURE'
    elif v == 'CLIP':
        cls = 'AS_ORIGINAL'
    else:
        cls = 'ENGLISH_ONLY'
    return v, n, cap, cls


# ------------------------------------------------------------------ surfaces
def run_table_mes(S, R):
    """PAGE / CLIP / SCROLL surfaces whose text comes from table cells."""
    scroll_max = 0
    for ctx in en_cells(S):
        tab, row = ctx['tab'], ctx['row']
        room, why = S.room_n, ''
        if S.id == 'node_comment':
            room, why = node_room(S, ctx)
            if room is None:
                R.add(S.id, ctx['name'], ctx['key'], ctx['col'], '', None, '', 'NOT_MODELLED', None, None, '', '', ctx['cell'], why)
                continue
        extra = {}
        if S.id == 'people_body':
            extra = {'n': ctx['ri'] + 1, 'citation': (tab.get(row, '解禁編') + ' ' + tab.get(row, 'シナリオ名')).strip()}
        if S.id == 'ref_summary':
            raw = compose_ref(tab, row, 'en')
        else:
            raw = affix(S, ctx['cell'], tab, row, extra)
        text = prep(raw, 'en')
        if text is None:
            R.add(S.id, ctx['name'], ctx['key'], ctx['col'], '', None, '', 'NOT_MODELLED', None, None, '', '', ctx['cell'], 'variable marker')
            continue
        v, n, cap, widest, extra_info = mes_verdict(S, text, 'en', room)
        info = extra_info
        if S.kind == 'SCROLL':
            scroll_max = max(scroll_max, n)
        if why:
            info = (info + ' ' + why).strip()
        if S.room_opts.get('under_buttons') and v in ('OK', 'TIGHT') and n > int(S.room_opts['under_buttons']):
            if v == 'OK':
                v = 'UNDER_BUTTONS'
            info = (info + ' UNDER_BUTTONS lines=%d >%s' % (n, S.room_opts['under_buttons'])).strip()
        jn = jcap = jv = cls = None
        if v == 'CLIP':
            jt, jr = jp_row(ctx)
            if jt is None or jr is None:
                jtext = None
            else:
                if S.id == 'ref_summary':
                    jraw = compose_ref(jt, jr, 'jp')
                else:
                    jraw = affix(S, jt.get(jr, ctx['col']), jt, jr, {})
                jtext = prep(jraw, 'jp')
            jv, jn, jcap, cls = jp_class_mes(S, jtext, room)
        R.add(S.id, ctx['name'], ctx['key'], ctx['col'], n, cap, widest, v, jn, jcap, jv, cls, ctx['cell'], info)
    if S.kind == 'SCROLL':
        R.info[S.id].append('SCROLL: widest entry has %d lines (information only)' % scroll_max)


def run_caption(S, R):
    for ctx in en_cells(S):
        text = prep(ctx['cell'], 'en')
        if text is None:
            R.add(S.id, ctx['name'], ctx['key'], ctx['col'], '', None, '', 'NOT_MODELLED', None, None, '', '', ctx['cell'], 'variable marker')
            continue
        px = caption_px(text, S.face, S.size_n, S.bold_n)
        limit_x = S.limit_base
        for c, val, lim in S.limit_rules:
            if ctx['tab'].get(ctx['row'], c) == val:
                limit_x = lim
        limit = limit_x - S.start_n
        v = caption_verdict(px, limit)
        jpx = jv = cls = None
        if v == 'CLIP':
            jt, jr = jp_row(ctx)
            jcols = lst(S.jp_column)
            jc = (jcols[ctx['ti']] if len(jcols) > 1 else jcols[0]) if jcols else ctx['col']
            jpx = 0
            if jt is not None and jr is not None:
                for part in jc.split('+'):
                    cname, _, sz = part.partition('@')
                    jtxt = prep(jt.get(jr, cname), 'jp')
                    if jtxt and jtxt.strip():
                        jpx = max(jpx, caption_px(jtxt, S.jp_face, int(sz) if sz else S.jp_size_n, S.jp_bold_n))
            jv = caption_verdict(jpx, limit)
            cls = 'AS_ORIGINAL' if jv == 'CLIP' else 'ENGLISH_ONLY'
        R.add(S.id, ctx['name'], ctx['key'], ctx['col'], px, limit, px, v, jpx, limit if jpx is not None else None, jv, cls, ctx['cell'],
              'limit_x=%d start_x=%d' % (limit_x, S.start_n) if v != 'OK' else '')


def run_not_modelled(S, R):
    for ctx in en_cells(S):
        R.add(S.id, ctx['name'], ctx['key'], ctx['col'], '', None, '', 'NOT_MODELLED', None, None, '', '', ctx['cell'], 'registry kind NOT_MODELLED')


def scene_files():
    ship = set()
    for ln in (TOOLS / 'ship-list.txt').read_text(encoding='utf-8').splitlines():
        ln = ln.split('#')[0].strip()
        if ln.endswith('.lsb'):
            ship.add(ln[:-4])
    ids55 = {p.name.split('-')[0] for p in (ROOT / 'lns-en-55').glob('*-*.lns')}
    ids_en = {p.name.split('-')[0] for p in (ROOT / 'lns-en').glob('*-*.lns')}
    use = OrderedDict()
    for i in sorted(ids55):
        use[i] = 'lns-en-55'
    for i in sorted(ids_en - ids55):
        use[i] = 'lns-en'
    unshipped = sorted(i for i in use if i not in ship)
    log('scene sources: lns-en-55 ids %d; ids only in lns-en %s; ids not in tools/ship-list.txt (skipped): %d' % (
        len(ids55), sorted(ids_en - ids55), len(unshipped)))
    files = []
    for i, d in use.items():
        if i in ship:
            files += sorted((ROOT / d).glob('%s-*.lns' % i))
    return files, unshipped


def run_scene(S, R):
    import fit_audit as fa
    files, unshipped = scene_files()
    R.info[S.id].append('scene files %d, skipped ids not in ship-list: %s' % (len(files), ','.join(unshipped) or 'none'))
    for p in files:
        sid = p.name.split('-')[0]
        for ln, text in fa.cells(p):
            if sid in UI_IDS:
                R.add(S.id, p.name, ln, '-', '', None, '', 'NOT_MODELLED', None, None, '', '', text, 'UI script id: text goes to a box other than the scene box')
                continue
            t = prep(text, 'en')
            if t is None:
                R.add(S.id, p.name, ln, '-', '', None, '', 'NOT_MODELLED', None, None, '', '', text, 'variable marker')
                continue
            v, n, cap, widest, info = mes_verdict(S, t, 'en', S.room_n)
            R.add(S.id, p.name, ln, '-', n, cap, widest, v, None, None, '', '', text, info)


def unregistered(reg):
    """Text objects of work/feedback-20261113/fit/inventory.tsv that are fed from tables or variables and are not a registry (script, idx)."""
    import csv
    rows = list(csv.DictReader(open(ROOT / 'work' / 'feedback-20261113' / 'fit' / 'inventory.tsv', encoding='utf-8'), delimiter='	', quoting=csv.QUOTE_NONE))
    pairs = set()
    for S in reg:
        for sc in S.script.split(';'):
            for i in S.idx.split(';'):
                pairs.add((sc, i))
    cap = [r for r in rows if r['type'] == 'Caption' and r['text_source'] in ('DB', 'expression')]
    mes = [r for r in rows if r['type'] == 'MesNew' and any('var ' in t and 'var -' not in t for t in r['textins'].split(' ; '))]
    uc = [r for r in cap if (r['script'], r['idx']) not in pairs]
    um = [r for r in mes if (r['script'], r['idx']) not in pairs]
    return ['- registry rows: %d (added by this run beyond spec 3.6: 0), kind NOT_MODELLED in the registry: %d (jikkyo)' % (
                len(reg), sum(S.kind == 'NOT_MODELLED' for S in reg)),
            '- inventory.tsv Captions fed by DB or expression: %d, not in the registry (NOT_MODELLED by omission): %d' % (len(cap), len(uc)),
            '- inventory.tsv MesNew fed by a variable: %d, not in the registry: %d' % (len(mes), len(um))]


# ------------------------------------------------------------------ main
HEAD = ['surface', 'table', 'key', 'column', 'lang', 'lines_or_px', 'capacity_or_limit', 'widest_line_px', 'verdict',
        'jp_lines_or_px', 'jp_capacity_or_limit', 'jp_verdict', 'class', 'text_first_60', 'info']
COLS = ['cells', 'OK', 'TIGHT', 'CLIP', 'PAGES', 'UNDER_BUTTONS', 'NOT_MODELLED']


def write_progress(done, nxt, questions):
    txt = ['# fit_check PROGRESS', '', 'Lane C, checker run of the FIT MODEL 2 spec (notes/FIT-MODEL-2.md section 3).', '', '## Done']
    txt += ['- ' + d for d in done] + ['', '## Next'] + ['- ' + n for n in nxt] + ['', '## Questions'] + (['- ' + q for q in questions] or ['- none'])
    (OUT / 'PROGRESS.md').write_text('\n'.join(txt) + '\n', encoding='utf-8')


QUESTIONS = [
    'Scene cells: lns of the UI-script ids (0000001C 0000001E 000000F2 00001878 0000189A 000018BF 000019DD 00001F8A 00001FBE) are drawn in boxes other than the scene box; marked NOT_MODELLED. Other non-scene lns ids (guide / reference body scripts) are still measured against the scene box because the box a script uses was not resolved per script.',
    'Chatter and help cells with formatting markers (/小/ /大文字/ /揺れ/ ...) are NOT_MODELLED under the rule "any marker other than /立木/" (spec 3.3); they are markers for small / large / shaking text, not variables. Decision for Fable: model them or keep NOT_MODELLED.',
    'Synopsis: the New Route block is shown only in some states (@Temp 8, 10, 11); the worst case (block appended whenever 新ルート is not empty) is measured. The 6 header lines are counted as 6 lines (they are not wrapped).',
    'ref_summary: the Characters line (idx 518) is used for the last template line; the Nodes line (idx 520) is shorter or equal. Rows are the 297 with a non-empty 概要.',
    'people_body is SCROLL (always OK); n and citation in the composed text are best effort and only change the information line of the log.',
    'Captions: the JP face of the registry is ＭＳ 明朝 (spec 3.5) although the jp dump says ＭＳ Ｐ明朝 for the notice captions; full-width glyphs have the same width in both.',
    'Registry gained four columns (jp_face, jp_size, jp_bold, jp_column) so that the Japanese run is data-driven; jp_column of the notices uses 出来事名 / 名前 because the Japanese tables have no 表示名 (jp dump idx 2420, 2437).',
]


def main():
    t0 = time.time()
    log('== self-check (spec 3.1)')
    if not self_check():
        log('SELF-CHECK FAILED: stop (constants not adjusted)')
        write_progress(['self-check ran'], ['report to coordinator: self-check failed'], [])
        return 1
    done = ['self-check: 81 of 81 observed lines reproduced']
    write_progress(done, ['run all registry surfaces'], QUESTIONS)
    reg = load_registry()
    R = Result()
    for S in reg:
        t = time.time()
        if S.kind == 'NOT_MODELLED':
            run_not_modelled(S, R)
        elif S.id == 'scene':
            run_scene(S, R)
        elif S.kind == 'CAPTION':
            run_caption(S, R)
        else:
            run_table_mes(S, R)
        c = R.counts[S.id]
        log('%s: cells %d, OK %d, TIGHT %d, CLIP %d, PAGES %d, NOT_MODELLED %d' % (
            S.id, R.cells[S.id], c['OK'], c['TIGHT'], c['CLIP'], c['PAGES'], c['NOT_MODELLED']) +
            ('' if not c['UNDER_BUTTONS'] else ' (UNDER_BUTTONS %d, counted apart)' % c['UNDER_BUTTONS']) +
            '   [%.1fs]' % (time.time() - t))
        for i in R.info[S.id]:
            log('    ' + i)
        done.append('%s: %d cells' % (S.id, R.cells[S.id]))
        write_progress(done, ['remaining surfaces', 'write findings.tsv and SUMMARY.md'], QUESTIONS)

    # findings
    with open(OUT / 'findings.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(HEAD) + '\n')
        for r in R.rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    log('findings.tsv rows: %d' % len(R.rows))

    # reference results (spec 3.7)
    log('== reference results (spec 3.7)')
    ok = True
    n_cells, c = R.cells['node_comment'], R.counts['node_comment']
    ref92 = [r for r in R.rows if r[0] == 'node_comment' and r[2] == '92' and r[3] == '3概要']
    r1 = n_cells == 315 and c['CLIP'] == 1 and len(ref92) == 1 and ref92[0][12] == 'AS_ORIGINAL'
    log('node_comment: cells %d (want 315), CLIP %d (want 1), ID 92 3概要: %s -> %s' % (
        n_cells, c['CLIP'], [(r[5], r[6], r[9], r[10], r[12]) for r in ref92], 'PASS' if r1 else 'FAIL'))
    c = R.counts['name_plate']
    r2 = R.cells['name_plate'] == 24 and c['CLIP'] == 12
    log('name_plate: names %d (want 24), CLIP %d (want 12) -> %s' % (R.cells['name_plate'], c['CLIP'], 'PASS' if r2 else 'FAIL'))
    ok = r1 and r2

    # summary
    L = ['# fit_check SUMMARY', '', 'Run of tools/fit_check.py over the English build (model: notes/FIT-MODEL-2.md). Self-check: 81 of 81 lines.', '',
         '| surface | kind | ' + ' | '.join(COLS) + ' | CLIP AS_ORIGINAL | CLIP ENGLISH_ONLY | CLIP JP_UNSURE |',
         '|' + '---|' * (len(COLS) + 5)]
    tot = Counter()
    for S in reg:
        c = R.counts[S.id]
        cl = R.classes[S.id]
        vals = [R.cells[S.id]] + [c[k] for k in COLS[1:]]
        row = vals + [cl['AS_ORIGINAL'], cl['ENGLISH_ONLY'], cl['JP_UNSURE']]
        for k, v in zip(COLS + ['AS_ORIGINAL', 'ENGLISH_ONLY', 'JP_UNSURE'], row):
            tot[k] += v
        L.append('| %s | %s | %s |' % (S.id, S.kind, ' | '.join(str(v) for v in row)))
    L.append('| TOTAL | | %s |' % ' | '.join(str(tot[k]) for k in COLS + ['AS_ORIGINAL', 'ENGLISH_ONLY', 'JP_UNSURE']))
    L += ['', 'UNDER_BUTTONS is the synopsis rule of spec 3.6 (lines > 17, not CLIP and not TIGHT); those rows are counted in their own column, not in OK.',
          'Of the CLIP rows, AS_ORIGINAL + ENGLISH_ONLY + JP_UNSURE = CLIP for every surface.', '',
          '## ENGLISH_ONLY CLIP rows (%d)' % len(R.only), '',
          '| surface | table | key | column | measured | limit |', '|---|---|---|---|---|---|']
    for s_, t_, k_, c_, p_, l_ in R.only:
        L.append('| %s | %s | %s | %s | %s | %s |' % (s_, t_, k_, c_, p_, l_))
    L += ['', 'measured / limit are in px for CAPTION surfaces and in lines for the others (limit = capacity in lines).']
    L += ['', '## Surfaces outside the registry', ''] + unregistered(reg)
    for x in unregistered(reg):
        log(x.lstrip('- '))
    (OUT / 'SUMMARY.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    log('SUMMARY.md written; ENGLISH_ONLY rows %d; per surface: %s' % (len(R.only), dict(Counter(x[0] for x in R.only))))
    log('total time %.1fs' % (time.time() - t0))
    write_progress(done + ['findings.tsv, SUMMARY.md, run.log written', 'reference results: %s' % ('both reproduced' if ok else 'MISMATCH, see run.log')],
                   ['coordinator reads SUMMARY.md'], QUESTIONS)
    return 0 if ok else 2


if __name__ == '__main__':
    sys.exit(main())
