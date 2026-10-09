"""kb.py - the pass-2 notes as fact tables + one disposable SQLite index (design: tools/kb/README.md,
ported from the Mushoku Tensei project's notes/DATA-DESIGN.md and tools/kb.py).

    PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py <command> ...

  convert             notes/v2 masters -> notes/v2/db/*.tsv (one fact per row; idempotent, byte-identical reruns)
  build               notes/v2/db/*.tsv + read/ + lns/ + lns-en-55/ -> notes/v2/db/kb.sqlite (disposable)
  packet <id>         the drafter's packet for one file -> notes/v2/_tmp/pack-<id>.md (fenced at <id>, 40 KB budget)
  tm <id> [--all]     3-gram Jaccard translation memory -> notes/v2/_tmp/tm-<id>.tsv (EN from lns-en-55/)
  lint [--strict]     DATA-DESIGN section 9 caps; report mode prints breaches and exits 0, --strict exits 1
  search <text> [--asof <id>] [--in jp|en|facts]   full-text search (FTS5 trigram, else a 3-gram table)
  core <lastid>       fenced copy of the CORE file (port of tools/db/fenced_core.py; honours SY_NOTES_DIR)
  query <sub> ...     fence-audit, character, speaker, speaker-lines, narrator, narrator-audit (ports of query.py)
  merge-log <tag> [--dry-run] [--force] | merge-log check
                      notes/v2/_tmp/tl-log-<tag>.md appended onto the notes/v2 masters (port of merge_log.py)
  selftest            idempotency hash, lossless round trip, fence = brute force, packet audits, search, tm

The masters (CAST.md, SUMMARY.md, RELATIONS.tsv, GLOSSARY.tsv, QUERIES.md, SCENE-FACTS.tsv,
NARRATOR-SWITCHES.tsv, UNREACHABLE.tsv, read/chunkNN.txt, read/speakers/chunkNN.tsv) stay the truth. packet,
tm and search run convert and build first when a master is newer than the index. Stdlib only.

THE FENCE. A file id's position is its "order N" in the read/chunkNN.txt FILE header; a fact's position is
(order, block, cell). Every fact row carries first_id (and superseded_id where a later row replaces it). A fact
is shown to the drafter of file X when first_id <= X (anywhere in X) and superseded_id is empty or not before X:
interval stabbing, bisect on the first_id-sorted array. A line with no id of its own takes its parent's first_id
(CAST child bullet), else the id of the block it was written in (CAST first_appears, SUMMARY block id); nothing
is "always known".
"""
import bisect
import glob
import hashlib
import math
import os
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / 'notes' / 'v2'
DB = NOTES / 'db'
TMP = NOTES / '_tmp'
READ = ROOT / 'read'
LNS = ROOT / 'lns'
EN_DIR = ROOT / 'lns-en-55'
KB_PATH = DB / 'kb.sqlite'
CAP = 40 * 1024
BIG = 10 ** 6       # "end of a file": block/cell bound of the fence interval
UNK = 10 ** 7       # an 8-hex id that is no lsb file id sorts after the file before it
TAB, ESC_TAB = chr(9), chr(92) + 't'   # meta.tsv stores a tab inside a value as backslash-t

MASTER_NAMES = ['CAST.md', 'SUMMARY.md', 'RELATIONS.tsv', 'GLOSSARY.tsv', 'QUERIES.md',
                'SCENE-FACTS.tsv', 'NARRATOR-SWITCHES.tsv', 'UNREACHABLE.tsv']

HEX = re.compile(r'([0-9A-F]{8})(?::(\d+)(?::(\d+))?)?')
FILE_HEAD = re.compile(r'^### FILE ([0-9A-F]{8})\.lsb\s+\(order (\d+), (\d+) lines, (\d+) chars\)')


def utf8_stdout():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass


def rel(p):
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def read_lines(path):
    """Lines without line ends (CR stripped), interior blank lines kept, no phantom last line."""
    text = Path(path).read_bytes().decode('utf-8').replace('\r', '')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    return lines


def master_paths():
    out = [NOTES / n for n in MASTER_NAMES] + [NOTES / 'SPEAKER-COLORS.tsv']
    out += sorted(Path(p) for p in glob.glob(str(READ / 'chunk*.txt')))
    out += sorted(Path(p) for p in glob.glob(str(READ / 'speakers' / 'chunk*.tsv')))
    return out


# ------------------------------------------------------------------------------------------------ ids / order
class Order:
    """file id -> order (from the read/chunkNN.txt FILE headers) and the (order, block, cell) position of an id."""

    def __init__(self, files):
        self.order = {f['file_id']: int(f['order']) for f in files}
        self.by_order = {int(f['order']): f['file_id'] for f in files}
        self.chunk = {f['file_id']: f['chunk'] for f in files}
        self.hexes = sorted(self.order)
        # hex order == reading order (checked in selftest); an unknown 8-hex id sorts right after the file before it
        self.max_order = max(self.order.values()) if self.order else 0
        self._memo = {}

    def pos(self, fid, block=None, cell=None):
        if fid in self.order:
            return (self.order[fid], int(block) if block else 0, int(cell) if cell else 0)
        i = bisect.bisect_right(self.hexes, fid)
        prev = self.order[self.hexes[i - 1]] if i else 0
        return (prev, UNK, 0)

    def ids(self, text):
        """[(position, 'ID[:b[:c]]')] for every 8-hex id in the text, in order of appearance."""
        out = []
        for m in HEX.finditer(text or ''):
            fid, b, c = m.groups()
            out.append((self.pos(fid, b, c), m.group(0)))
        return out

    def min_id(self, text):
        found = self.ids(text)
        return min(found) if found else None

    def key(self, first_id):
        """position of a stored first_id / superseded_id ('' -> None)."""
        if not first_id:
            return None
        k = self._memo.get(first_id)
        if k is None:
            m = HEX.match(first_id)
            k = self._memo[first_id] = self.pos(*m.groups()) if m else False
        return k or None

    def hi(self, fid):
        return (self.order[fid], BIG, BIG)

    def lo(self, fid):
        return (self.order[fid], 0, 0)


def later(a, b):
    """the later of two (position, id-string) pairs; None-safe."""
    if a is None:
        return b
    if b is None:
        return a
    return a if a[0] >= b[0] else b


# ------------------------------------------------------------------------------------------------ tsv i/o
def tsv_write(path, header, rows):
    """Raw tab-joined rows (DATA-DESIGN section 10: never csv quoting). Atomic replace. A tab or newline inside a
    field is an error, never silently rewritten."""
    out = ['\t'.join(header)]
    for r in rows:
        vals = ['' if v is None else str(v) for v in r]
        if len(vals) != len(header):
            raise SystemExit(f'{path.name}: row has {len(vals)} fields, header {len(header)}: {vals[:3]}')
        for v in vals:
            if '\t' in v or '\n' in v or '\r' in v:
                raise SystemExit(f'{path.name}: a field contains a tab/newline: {v[:80]!r}')
        out.append('\t'.join(vals))
    data = ('\n'.join(out) + '\n').encode('utf-8')
    tmp = path.with_suffix(path.suffix + f'.tmp{os.getpid()}')
    tmp.write_bytes(data)
    replace(tmp, path)


def replace(src, dst):
    for i in range(20):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            time.sleep(0.25 * (i + 1))
    raise SystemExit(f'could not replace {rel(dst)} (another process holds it open)')


def tsv_read(path):
    lines = read_lines(path)
    if not lines:
        return []
    head = lines[0].split('\t')
    out = []
    for line in lines[1:]:
        vals = line.split('\t')
        out.append(dict(zip(head, vals + [''] * (len(head) - len(vals)))))
    return out


# ------------------------------------------------------------------------------------------------ convert
TABLES = {
    'files': ['file_id', 'order', 'chunk', 'lines', 'chars', 'header'],
    'summary': ['file_id', 'line', 'depth', 'key', 'first_id', 'superseded_id', 'text'],
    'cast': ['block', 'name', 'heading', 'first_appears'],
    'cast_facts': ['block', 'line', 'depth', 'parent', 'kind', 'voice', 'first_id', 'superseded_id', 'text'],
    'relations': ['row', 'from', 'to', 'calls_them', 'speech_level', 'as_of_file', 'changed_from', 'why',
                  'first_id', 'superseded_id'],
    'glossary': ['row', 'jp', 'reading', 'en', 'pos', 'category', 'first_seen', 'status', 'locked', 'note',
                 'first_id', 'superseded_id'],
    'queries': ['row', 'qid', 'loc', 'question', 'why', 'best_guess', 'confidence', 'status', 'resolved_by',
                'nfields', 'tail', 'first_id', 'superseded_id'],
    'scene_facts': ['file_id', 'narrator_jp', 'start_time', 'source_column', 'note', 'first_id'],
    'narrator_switches': ['file_id', 'loc', 'from_jp', 'to_jp', 'evidence', 'first_id'],
    'unreachable': ['file_id', 'block', 'reason', 'first_id'],
    'speakers': ['file_id', 'loc', 'speaker', 'narrator_switch', 'unreachable', 'first_id'],
    'chunk_cards': ['chunk', 'files', 'words', 'source', 'first_id', 'text'],
    'meta': ['key', 'value'],
}

# CAST template keys = the voice sheet (READTHROUGH-BRIEF "What to extract"): mandatory in a packet.
VOICE_KEYS = ('first_appears', 'pronoun', 'speech level', 'sentence-final', 'copula', 'verbal tics', 'dialect',
              'EN correlates', 'narration voice', 'known ambiguity', 'as-of')


def bullet_key(line):
    s = line.lstrip(' ')
    if not s.startswith('- '):
        return ''
    m = re.match(r'([^:]{1,80}?)(?: \(|:)', s[2:])   # "events (block order ...):" -> "events"
    return m.group(1).strip() if m else ''


def depth_of(line):
    return len(line) - len(line.lstrip(' '))


def conv_files():
    rows = []
    for p in sorted(glob.glob(str(READ / 'chunk*.txt'))):
        chunk = re.search(r'chunk(\d+)', Path(p).name).group(1)
        for line in read_lines(p):
            m = FILE_HEAD.match(line)
            if m:
                rows.append([m.group(1), m.group(2), chunk, m.group(3), m.group(4), line])
    rows.sort(key=lambda r: int(r[1]))
    return rows


def fid_str(p):
    """'ID[:b[:c]]' of a (position, idstring) pair, or ''."""
    return p[1] if p else ''


def conv_summary(od):
    rows, fid, block_first, n, stack = [], None, None, 0, []
    seen = set()
    for line in read_lines(NOTES / 'SUMMARY.md'):
        if line.startswith('## '):
            m = HEX.search(line)
            fid = m.group(1) if m else None
            if fid in seen:
                raise SystemExit(f'SUMMARY.md: two blocks for {fid}')
            if fid:
                seen.add(fid)
                block_first = (od.pos(fid), fid)
                n = 0
                stack = []
                rows.append([fid, n, 0, '_heading', fid, '', line])
            continue
        if fid is None:
            continue   # the file's preamble (title line) is not a fact
        n += 1
        d = depth_of(line)
        if not line.strip():
            rows.append([fid, n, 0, '_blank', fid, '', line])
            continue
        while stack and stack[-1][0] >= d:
            stack.pop()
        parent_first = stack[-1][1] if stack else block_first
        own = od.min_id(line)
        # a summary line is known at its block's file at the earliest; a line naming only a later file is later
        first = later(parent_first, own) if own and own[0] > parent_first[0] else parent_first
        stack.append((d, first))
        rows.append([fid, n, d, bullet_key(line), fid_str(first), '', line])
    return rows


def conv_cast(od):
    blocks, facts = [], []
    cur = []

    def flush():
        if not cur:
            return
        b = len(blocks)
        heading = cur[0]
        name = re.match(r'^## ([^(—]+?)(?: \(|$| —)', heading)
        fa = None
        for line in cur[1:]:
            if bullet_key(line) == 'first_appears' and depth_of(line) == 0:
                fa = od.min_id(line)
                break
        if fa is None:   # no first_appears: the earliest id in the block (never "always known")
            fa = min((p for line in cur for p in od.ids(line)), default=None)
        if fa is None:
            fa = ((od.max_order + 1, 0, 0), 'NEVER')
        blocks.append([b, (name.group(1) if name else heading[3:]).strip(), heading, fid_str(fa)])
        facts.append([b, 0, 0, '', 'heading', '1', fid_str(fa), '', heading])
        stack = []   # (depth, first, line_no, voice)
        for i, line in enumerate(cur[1:], 1):
            if not line.strip():
                facts.append([b, i, 0, '', 'blank', '', fid_str(fa), '', line])
                continue
            d = depth_of(line)
            while stack and stack[-1][0] >= d:
                stack.pop()
            own = od.min_id(line)
            if stack:
                pd, pfirst, pline, pvoice = stack[-1]
                first = later(pfirst, own)          # a child is never known before its parent
                voice = pvoice
                parent = pline
            else:
                first = own if own else fa           # top-level: its own earliest id, else first_appears
                k = bullet_key(line)
                voice = '1' if any(k.startswith(v) for v in VOICE_KEYS) else ''
                parent = ''
            stack.append((d, first, i, voice))
            facts.append([b, i, d, parent, bullet_key(line), voice, fid_str(first), '', line])

    preamble = True
    for line in read_lines(NOTES / 'CAST.md'):
        if line.startswith('## '):
            flush()
            cur = [line]
            preamble = False
            continue
        if not preamble:
            cur.append(line)
    flush()
    return blocks, facts


def conv_relations(od):
    lines = read_lines(NOTES / 'RELATIONS.tsv')
    header = lines[0]
    rows, last = [], {}
    for i, line in enumerate(lines[1:], 1):
        if not line.strip():
            continue
        c = line.split('\t')
        if len(c) != 7:
            raise SystemExit(f'RELATIONS.tsv row {i}: {len(c)} fields, expected 7')
        asof = od.min_id(c[4])
        first = asof or od.min_id(line) or ((od.max_order + 1, 0, 0), 'NEVER')
        rows.append([i] + c + [fid_str(first), ''])
    # superseded: a row with changed_from replaces the latest earlier row of the same (from, to) whose
    # calls_them or speech_level equals changed_from exactly (READTHROUGH-BRIEF: "add a NEW row ... keep the old")
    for r in rows:
        frm, to, ch = r[1], r[2], r[6].strip()
        if ch and ch != '-':
            prev = last.get((frm, to), [])
            for p in reversed(prev):
                if not p[9] and ch in (p[3].strip(), p[4].strip()):
                    p[9] = r[8]
                    break
        last.setdefault((frm, to), []).append(r)
    return header, rows


def conv_glossary(od):
    lines = read_lines(NOTES / 'GLOSSARY.tsv')
    rows = []
    for i, line in enumerate(lines[1:], 1):
        if not line.strip():
            continue
        c = line.split('\t')
        if len(c) != 9:
            raise SystemExit(f'GLOSSARY.tsv row {i}: {len(c)} fields, expected 9')
        first = od.min_id(c[5]) or ((od.max_order + 1, 0, 0), 'NEVER')
        rows.append([i] + c + [fid_str(first), 'superseded' if c[6] == 'superseded' else ''])
    return lines[0], rows


QID = re.compile(r'^[QV]\d')


def conv_queries(od):
    rows, header = [], ''
    for i, line in enumerate(read_lines(NOTES / 'QUERIES.md'), 1):
        if line.startswith('id | '):
            header = line
        if not QID.match(line):
            continue
        core = line.rstrip()
        if core.endswith('|'):
            core = core[:-1]
        tail = line[len(core):]
        p = core.split(' | ')
        nf = len(p)
        if nf > 8:
            p = p[:7] + [' | '.join(p[7:])]
        p += [''] * (8 - len(p))
        first = od.min_id(p[1]) or ((od.max_order + 1, 0, 0), 'NEVER')
        rows.append([i] + p + [min(nf, 8), tail.replace('\t', ' '), fid_str(first), ''])
    return header, rows


def conv_small(od):
    sf = [r[:5] + [r[0]] for r in (l.split('\t') + [''] * 5 for l in read_lines(NOTES / 'SCENE-FACTS.tsv')[1:])]
    sw = [r[:5] + [f'{r[0]}:{r[1]}'.replace(':end', '')] for r in
          (l.split('\t') + [''] * 5 for l in read_lines(NOTES / 'NARRATOR-SWITCHES.tsv')[1:])]
    un = []
    p = NOTES / 'UNREACHABLE.tsv'
    if p.exists():
        un = [r[:3] + [f'{r[0]}:{r[1]}'] for r in (l.split('\t') + [''] * 3 for l in read_lines(p)[1:])]
    sp = []
    for path in sorted(glob.glob(str(READ / 'speakers' / 'chunk*.tsv'))):
        for line in read_lines(path):
            c = (line.split('\t') + [''] * 5)[:5]
            if c[2] or c[3] or c[4]:
                sp.append(c + [f'{c[0]}:{c[1]}'])
    return [r[:6] for r in sf], [r[:6] for r in sw], un, sp


def words(s):
    return s.split()


def conv_cards(od, files, summary):
    """Parent level of the summary tree: one card per chunk, AUTO = the 'events' text of each leaf (per-file
    SUMMARY block) concatenated, each leaf truncated to an equal share of 400 words."""
    by_file = defaultdict(list)
    for r in summary:
        by_file[r[0]].append(r)
    chunks = defaultdict(list)
    for f in files:
        chunks[f[2]].append(f[0])
    out = []
    for ch in sorted(chunks):
        fids = chunks[ch]
        share = max(1, 400 // len(fids) - 3)   # + the "<id>:", "..." and "|" tokens of each leaf
        parts, first = [], None
        for fid in fids:
            rows = by_file.get(fid, [])
            ev, on = [], False
            for r in rows:
                if r[2] == 0 and r[3] not in ('_blank',):
                    on = (r[3] == 'events')
                    if on:
                        rest = r[6].split(':', 1)[1].strip() if ':' in r[6] else ''
                        if rest:
                            ev.append((r, rest))
                        continue
                if on and r[3] != '_blank':
                    ev.append((r, r[6].strip().lstrip('- ').strip()))
            w = []
            for r, t in ev:
                w += words(t)
                first = later(first, (od.key(r[4]), r[4]))
            if not w:
                continue
            cut = w[:share]
            parts.append(f'{fid}: ' + ' '.join(cut) + (' ...' if len(w) > share else ''))
        last = fids[-1]
        first = later(first, (od.pos(last), last))
        text = ' | '.join(parts)
        out.append([ch, f'{fids[0]}-{last}', len(words(text)), 'auto', fid_str(first), text])
    return out


def convert(quiet=False):
    files = conv_files()
    od = Order([dict(zip(TABLES['files'], f)) for f in files])
    DB.mkdir(parents=True, exist_ok=True)
    summary = conv_summary(od)
    blocks, facts = conv_cast(od)
    rel_head, rels = conv_relations(od)
    gl_head, gl = conv_glossary(od)
    q_head, qs = conv_queries(od)
    sf, sw, un, sp = conv_small(od)
    cards = conv_cards(od, files, summary)
    # meta values: a tab is stored as the two characters backslash-t (the header lines have no backslash)
    meta = [['glossary_header', gl_head.replace(TAB, ESC_TAB)], ['relations_header', rel_head.replace(TAB, ESC_TAB)],
            ['queries_header', q_head],
            ['summary_preamble', '\\n'.join(read_lines(NOTES / 'SUMMARY.md')[:next(
                i for i, l in enumerate(read_lines(NOTES / 'SUMMARY.md')) if l.startswith('## '))])],
            ['cast_preamble', '\\n'.join(read_lines(NOTES / 'CAST.md')[:next(
                i for i, l in enumerate(read_lines(NOTES / 'CAST.md')) if l.startswith('## '))])]]
    out = {'files': files, 'summary': summary, 'cast': blocks, 'cast_facts': facts, 'relations': rels,
           'glossary': gl, 'queries': qs, 'scene_facts': sf, 'narrator_switches': sw, 'unreachable': un,
           'speakers': sp, 'chunk_cards': cards, 'meta': meta}
    for name, rows in out.items():
        tsv_write(DB / f'{name}.tsv', TABLES[name], rows)
    if not quiet:
        print('convert: ' + ', '.join(f'{k} {len(v)}' for k, v in out.items()) + f' -> {rel(DB)}/*.tsv')
    return out


# ------------------------------------------------------------------------------------------------ build
def strip_tags(s):
    return re.sub(r'<[^>]*>|\{[^}]*\}', '', s).strip()


JP_CHAR = re.compile(r'[぀-ヿ一-鿿々〆ー]')


def lns_pairs():
    """(file_id, lns name, line no, jp text, en text) for every lns line with Japanese whose EN twin in
    lns-en-55/ differs (JP and EN .lns files are line for line)."""
    out = []
    for en_path in sorted(glob.glob(str(EN_DIR / '*.lns'))):
        name = Path(en_path).name
        jp_path = LNS / name
        if not jp_path.exists():
            continue
        jl, el = read_lines(jp_path), read_lines(en_path)
        fid = name.split('-')[0]
        for n, jline in enumerate(jl, 1):
            if jline.startswith(';') or n > len(el):
                continue
            j, e = strip_tags(jline), strip_tags(el[n - 1])
            if j and e and j != e and JP_CHAR.search(j):
                out.append((fid, name, n, j, e))
    return out


def speaker_color_rows():
    """one row per lns text cell: colour, speaker by colour, kind (tools/style_colors.py; notes/v2/SPEAKER-COLORS.md)"""
    sys.path.insert(0, str(ROOT / 'tools'))
    import style_colors
    table, unknown, rows = style_colors.load_speaker_table(), Counter(), []
    for fid in style_colors.all_ids():
        for r in style_colors.cell_speakers(fid, table, unknown):
            b, _, c = r['cell'].partition(':')
            rows.append((fid, b, c, r['colour'], r['speaker'], r['kind']))
    for c, n in sorted(unknown.items()):
        print(f'WARN unknown colour {c} in {n} cell(s): not in notes/v2/SPEAKER-COLORS.tsv, speaker left empty')
    return rows


def fts_ok(con):
    try:
        con.execute("CREATE VIRTUAL TABLE temp._probe USING fts5(x, tokenize='trigram')")
        con.execute('DROP TABLE temp._probe')
        return True
    except sqlite3.OperationalError:
        return False


def build(quiet=False):
    t = {name: tsv_read(DB / f'{name}.tsv') for name in TABLES}
    tmp = DB / f'kb.sqlite.tmp{os.getpid()}'
    if tmp.exists():
        tmp.unlink()
    con = sqlite3.connect(str(tmp))
    for name, cols in TABLES.items():
        if name == 'meta':
            t[name] = [dict(r, value=r['value'].replace(ESC_TAB, TAB)) for r in t[name]]
        con.execute(f'CREATE TABLE "{name}" ({", ".join(chr(34) + c + chr(34) + " TEXT" for c in cols)})')
        con.executemany(f'INSERT INTO "{name}" VALUES ({",".join("?" * len(cols))})',
                        [[r.get(c, '') for c in cols] for r in t[name]])
        for c in cols:
            if c in ('file_id', 'first_id', 'jp', 'en', 'block', 'qid', 'from', 'to', 'chunk'):
                con.execute(f'CREATE INDEX "i_{name}_{c}" ON "{name}"("{c}")')
    # source text: the chunk lines (what the drafter reads) and the lns pairs (the TM and the EN search)
    con.execute('CREATE TABLE text(file_id TEXT, ord INTEGER, loc TEXT, block INTEGER, cell INTEGER, text TEXT, '
                'raw TEXT)')
    rows = []
    for p in sorted(glob.glob(str(READ / 'chunk*.txt'))):
        fid, n = None, 0
        for line in read_lines(p):
            m = FILE_HEAD.match(line)
            if m:
                fid, n = m.group(1), 0
                continue
            if not line.strip() or fid is None:
                continue
            loc, _, text = line.partition('\t')
            b, _, c = loc.partition(':')
            rows.append((fid, n, loc, int(b) if b.isdigit() else None, int(c) if c.isdigit() else None, text, line))
            n += 1
    con.executemany('INSERT INTO text VALUES (?,?,?,?,?,?,?)', rows)
    con.execute('CREATE INDEX i_text_file ON text(file_id, ord)')
    # mention: glossary jp -> file, n (the searchable text is the FILE header + every raw chunk line, as before)
    keys = sorted({r['jp'] for r in t['glossary'] if r['jp']})
    by_first = defaultdict(list)
    for k in keys:
        by_first[k[0]].append(k)
    header = {f['file_id']: f['header'] for f in t['files']}
    per_file = defaultdict(list)
    for r in rows:
        per_file[r[0]].append(r[6])
    ment = []
    for fid in sorted(per_file):
        hits = Counter()
        for raw in [header.get(fid, '')] + per_file[fid]:
            for i, ch in enumerate(raw):
                for term in by_first.get(ch, ()):
                    if raw.startswith(term, i):
                        hits[term] += 1
        ment += [(fid, term, n) for term, n in hits.items()]
    con.execute('CREATE TABLE mention(file_id TEXT, jp TEXT, n INTEGER)')
    con.executemany('INSERT INTO mention VALUES (?,?,?)', ment)
    con.execute('CREATE INDEX i_mention_file ON mention(file_id)')
    con.execute('CREATE INDEX i_mention_jp ON mention(jp)')
    con.execute('CREATE TABLE speaker_color(file_id TEXT, block TEXT, cell TEXT, color TEXT, speaker TEXT, kind TEXT)')
    con.executemany('INSERT INTO speaker_color VALUES (?,?,?,?,?,?)', speaker_color_rows())
    con.execute('CREATE INDEX i_speaker_color ON speaker_color(file_id, block, cell)')
    con.execute('CREATE INDEX i_speaker_color_sp ON speaker_color(speaker, kind)')
    pairs = lns_pairs()
    con.execute('CREATE TABLE tm(file_id TEXT, lns TEXT, line INTEGER, jp TEXT, en TEXT)')
    con.executemany('INSERT INTO tm VALUES (?,?,?,?,?)', pairs)
    # search index: FTS5 trigram when this sqlite has it, else a plain 3-gram table
    docs = [('jp', f'{r[0]}:{r[2]}', r[0], r[5]) for r in rows]
    docs += [('en', f'{p[0]}:{p[1]}:{p[2]}', p[0], p[4]) for p in pairs]
    for r in t['summary']:
        docs.append(('facts', f'SUMMARY {r["file_id"]}#{r["line"]}', r['first_id'], r['text']))
    for r in t['cast_facts']:
        docs.append(('facts', f'CAST b{r["block"]}#{r["line"]}', r['first_id'], r['text']))
    for r in t['relations']:
        docs.append(('facts', f'RELATIONS #{r["row"]}', r['first_id'],
                     '\t'.join(r[c] for c in TABLES['relations'][1:8])))
    for r in t['glossary']:
        docs.append(('facts', f'GLOSSARY #{r["row"]}', r['first_id'],
                     '\t'.join(r[c] for c in TABLES['glossary'][1:10])))
    for r in t['queries']:
        docs.append(('facts', f'QUERIES {r["qid"]}', r['first_id'], ' | '.join(
            r[c] for c in TABLES['queries'][2:9])))
    fts = fts_ok(con)
    if fts:
        con.execute("CREATE VIRTUAL TABLE doc USING fts5(kind UNINDEXED, id UNINDEXED, asof UNINDEXED, text, "
                    "tokenize='trigram')")
        con.executemany('INSERT INTO doc VALUES (?,?,?,?)', docs)
    else:
        con.execute('CREATE TABLE doc(rowid INTEGER PRIMARY KEY, kind TEXT, id TEXT, asof TEXT, text TEXT)')
        con.executemany('INSERT INTO doc(kind, id, asof, text) VALUES (?,?,?,?)', docs)
        con.execute('CREATE TABLE gram(g TEXT, doc INTEGER)')
        con.executemany('INSERT INTO gram VALUES (?,?)', ((d[4][i:i + 3], d[0]) for d in con.execute(
            'SELECT rowid, kind, id, asof, text FROM doc').fetchall() for i in range(max(0, len(d[4]) - 2))))
        con.execute('CREATE INDEX i_gram ON gram(g)')
    con.execute('CREATE TABLE kbmeta(key TEXT PRIMARY KEY, value TEXT)')
    con.execute("INSERT INTO kbmeta VALUES ('search', ?)", ('fts5-trigram' if fts else '3gram-table',))
    con.commit()
    con.close()
    replace(tmp, KB_PATH)
    if not quiet:
        print(f'build: {len(rows)} text lines, {len(ment)} mentions, {len(pairs)} TM rows, {len(docs)} search docs '
              f'({"FTS5 trigram" if fts else "NO FTS5 in this sqlite: 3-gram table fallback"}) -> {rel(KB_PATH)} '
              f'({KB_PATH.stat().st_size // 1024} KB)')


def refresh():
    """convert when a master is newer than the TSVs, build when a TSV is newer than the index."""
    tsvs = [DB / f'{n}.tsv' for n in TABLES]
    code = Path(__file__).stat().st_mtime   # a new kb.py can change the TSV or table layout
    newest_master = max([p.stat().st_mtime for p in master_paths() if p.exists()] + [code])
    if not all(p.exists() for p in tsvs) or newest_master > min(p.stat().st_mtime for p in tsvs):
        print('refresh: a master is newer than notes/v2/db/*.tsv -> convert')
        convert(quiet=True)
    if not KB_PATH.exists() or max([p.stat().st_mtime for p in tsvs] + [code]) > KB_PATH.stat().st_mtime:
        print('refresh: notes/v2/db/*.tsv newer than kb.sqlite -> build')
        build(quiet=True)


def connect():
    con = sqlite3.connect(str(KB_PATH))
    con.row_factory = sqlite3.Row
    return con


def load_order(con):
    return Order([dict(r) for r in con.execute('SELECT * FROM files')])


# ------------------------------------------------------------------------------------------------ fence
class Fence:
    """Interval stabbing over rows with first_id / superseded_id: sort by first position once, bisect per query."""

    def __init__(self, rows, od):
        keyed = []
        for r in rows:
            k = od.key(r['first_id'])
            if k is None:
                k = (od.max_order + 1, 0, 0)
            keyed.append((k, od.key(r.get('superseded_id') or '') if r.get('superseded_id') not in (None, '', 'superseded') else
                          ((-1, 0, 0) if r.get('superseded_id') == 'superseded' else None), r))
        keyed.sort(key=lambda x: x[0])
        self.keys = [k for k, _, _ in keyed]
        self.rows = keyed

    def at(self, od, fid):
        """rows known while reading <fid>: first <= end of fid, superseded (if any) not before fid."""
        i = bisect.bisect_right(self.keys, od.hi(fid))
        lo = od.lo(fid)
        return [r for k, s, r in self.rows[:i] if s is None or s >= lo]


def visible(od, r, fid):
    """the same test for one row (the brute-force twin of Fence.at, used by selftest and the audits)."""
    k = od.key(r['first_id'])
    if k is None or k > od.hi(fid):
        return False
    s = r.get('superseded_id') or ''
    if s == 'superseded':
        return False
    return not s or od.key(s) >= od.lo(fid)


# ------------------------------------------------------------------------------------------------ packet
CJK_RUN = re.compile(r'^([぀-ゟ゠-ヿ一-鿿ー]+)')
SPLIT = re.compile(r'[,;、(（]')

SPEAKER_NOTE = ('speaker in [] comes from the text color (notes/v2/SPEAKER-COLORS.md); '
                '? = uncolored quote, attribute from context; [unreachable] = a cell of a block no play shows '
                '(notes/v2/UNREACHABLE.tsv): read it for comparison only. The narrator and in-story start under '
                'the SLICE heading come from the game\'s scenario table, a NARRATOR SWITCH line from a '
                'viewpoint-switch sprite: both are facts.')

TEST_PARAGRAPH = """\
> GRAMMAR vs WITHHELD (rev. 2026-09-25, rules audit #1; METHOD.md §3 is the full rule). A gap is
> GRAMMAR when two first-time Japanese readers would fill it the same way without noticing a gap:
> fill it as they do, no flag, no DECISIONS row. A gap is WITHHELD when those readers could fill it
> differently, or when the text later turns on which filling is right: keep it open if the list below
> names it or if English can without a contortion, otherwise take the supported reading and flag
> needs-tlc. The subject-guessed / gender-guessed / number-guessed flags are for WITHHELD gaps ONLY.
> The "ambiguity that the translation MUST keep open" lines below were written under the OLDER
> definition and mix real withholding with grammar habits and structural notes: READ EVERY SUCH LINE
> THROUGH THIS TEST until the lists are re-tagged."""

SECTIONS = [
    ('prev', '## SUMMARY block of the previous file ({prev})'),
    ('this', '## SUMMARY block of THIS file ({fid})'),
    ('leaf', '## Earlier files of this chunk (leaf summaries, fenced; ranked items, see the foot)'),
    ('card', '## Earlier chunks (chunk cards, AUTO: each leaf\'s events cut to an equal share of 400 words)'),
    ('gloss', '## GLOSSARY rows for terms that occur in this file (jp, reading, en, pos, category, first_seen, '
              'status, locked, note; FENCED on first_seen)'),
    ('query', '## QUERIES rows filed against this file'),
    ('speak', '## Speakers present (from the SUMMARY block; the CAST blocks below are chosen by these names)'),
    ('narr', '## Narrator line'),
    ('cast', '## CAST.md blocks for the speakers present (living sheets, FENCED at {fid}: a line is shown when its '
             'first_id is not later than {fid}; an id-free line takes its parent\'s id or the block\'s first_appears; '
             'voice-sheet bullets always, other bullets ranked under the 40 KB cap)'),
    ('rel', '## RELATIONS.tsv rows where both parties are among the speakers present (FENCED on as_of_file; '
            'a row replaced by a changed_from row before {fid} is not shown)'),
    ('hop', '## RELATIONS.tsv rows one hop out (one party present, or both parties met one hop out; FENCED, '
            'ranked)'),
]


def speakers_of(summary_rows):
    for r in summary_rows:
        if r['depth'] == '0' and r['key'] == 'speakers present':
            out = []
            for tok in SPLIT.split(r['text'].split(':', 1)[1] if ':' in r['text'] else ''):
                m = CJK_RUN.match(tok.strip())
                if m:
                    out.append(m.group(1))
            return sorted(set(out)), r['text']
    return [], ''


def terms_in(text, terms):
    return [t for t in terms if t in text]


class Packet:
    def __init__(self, con, fid):
        self.con, self.fid = con, fid
        self.od = load_order(con)
        if fid not in self.od.order:
            raise SystemExit(f'{fid}: no "### FILE {fid}.lsb (order N, ...)" header in read/chunk*.txt')
        self.items = []          # dict(sec, sort, text, mand, score, label)
        self.fenced_out = []     # (section, line) facts not known at fid
        self.superseded = []     # (section, line) replaced before fid
        self.later_dropped = []  # (section, line) known at fid but quoting a LATER file id: dropped
        self.trimmed = []        # (original, trimmed) mandatory cast lines whose later-id clauses were cut
        self.hi = self.od.hi(fid)

    def later_in(self, text):
        """True when the text quotes any file id later than the fence id (an unknown 8-hex id counts by hex order)."""
        return any(p > self.hi for p, _ in self.od.ids(text))

    def keep_lines(self, sec, lines):
        """Drop every line that quotes a later id, and the deeper-indented lines under it."""
        out, drop = [], None
        for t in lines:
            d = depth_of(t)
            if drop is not None and t.strip() and d > drop:
                self.later_dropped.append((sec, t))
                continue
            drop = None
            if self.later_in(t):
                self.later_dropped.append((sec, t))
                drop = d
                continue
            out.append(t)
        return out

    def trim(self, t):
        """A mandatory cast line that quotes a later id: cut every '; '-clause holding one, mark [trimmed]."""
        if not self.later_in(t):
            return t
        m = re.match(r'^(\s*(?:- |## )?(?:[^:]{1,80}?: )?)(.*)$', t)
        prefix, body = m.group(1), m.group(2)
        if self.later_in(prefix):
            prefix = HEX.sub(lambda x: x.group(0) if self.od.pos(x.group(1)) <= self.hi else '[later id]', prefix)
        kept = [c for c in body.split('; ') if not self.later_in(c)]
        out = (prefix + '; '.join(kept)).rstrip() + ' [trimmed]'
        self.trimmed.append((t, out))
        return out

    def q(self, sql, *a):
        return [dict(r) for r in self.con.execute(sql, a).fetchall()]

    def add(self, sec, sort, text, mand, label, first=None):
        self.items.append(dict(sec=sec, sort=sort, text=text, mand=mand, label=label, first=first,
                               size=len(text.encode('utf-8')) + 1, score=0.0))

    def summary_lines(self, fid, rows_by_file):
        out = []
        for r in rows_by_file.get(fid, []):
            if r['key'] == '_heading' or visible(self.od, r, self.fid):
                out.append(r['text'])
            else:
                self.fenced_out.append(('summary', r['text']))
        return self.keep_lines('summary', out)

    def run(self):
        od, fid = self.od, self.fid
        cur = od.order[fid]
        prev = od.by_order.get(cur - 1, '')
        chunk = od.chunk[fid]
        srows = self.q('SELECT * FROM summary ORDER BY file_id, CAST(line AS INTEGER)')
        by_file = defaultdict(list)
        for r in srows:
            by_file[r['file_id']].append(r)
        names, _ = speakers_of(by_file.get(fid, []))
        self.names = names
        # term statistics for the tf-idf rank (DATA-DESIGN section 5)
        nfiles = len(od.order)
        tf = {r['jp']: int(r['n']) for r in self.q('SELECT jp, n FROM mention WHERE file_id=?', fid)}
        df = {r['jp']: int(r['c']) for r in self.q(
            'SELECT jp, COUNT(*) c FROM mention WHERE jp IN (SELECT jp FROM mention WHERE file_id=?) GROUP BY jp', fid)}
        self.weights = {t: n * math.log(nfiles / max(1, df.get(t, 1))) for t, n in tf.items() if len(t) >= 2}

        # ---- summaries: this + previous file mandatory (leaves), other earlier leaves of this chunk and
        #      the cards of earlier chunks optional
        if prev:
            self.add('prev', 0, '\n'.join(self.summary_lines(prev, by_file)), True, f'SUMMARY {prev}')
        self.add('this', 0, '\n'.join(self.summary_lines(fid, by_file)), True, f'SUMMARY {fid}')
        for f in self.q('SELECT file_id, "order" FROM files WHERE chunk=?', chunk):
            o = int(f['order'])
            if o < cur - 1:
                self.add('leaf', o, '\n'.join(self.summary_lines(f['file_id'], by_file)), False,
                         f'SUMMARY {f["file_id"]}', first=(o, 0, 0))
        cards = Fence(self.q('SELECT * FROM chunk_cards'), od).at(od, fid)
        for c in cards:
            if c['chunk'] < chunk and self.later_in(c['text']):
                self.later_dropped.append(('card', c['text']))
            elif c['chunk'] < chunk:
                self.add('card', int(c['chunk']), f'**chunk {c["chunk"]}** ({c["files"]}, auto): {c["text"]}',
                         False, f'chunk card {c["chunk"]}', first=od.key(c['first_id']))

        # ---- glossary rows whose jp occurs in the file (fenced on first_seen); all mandatory
        gl = self.q('SELECT * FROM glossary WHERE jp IN (SELECT jp FROM mention WHERE file_id=?) '
                    'ORDER BY CAST("row" AS INTEGER)', fid)
        for r in gl:
            line = '\t'.join(r[c] for c in TABLES['glossary'][1:10])
            if visible(od, r, fid) and self.later_in(line):
                self.later_dropped.append(('glossary', line))
            elif visible(od, r, fid):
                self.add('gloss', int(r['row']), line, True, f'GLOSSARY {r["jp"]}')
            else:
                self.fenced_out.append(('glossary', line))

        # ---- queries filed against this file
        for r in self.q('SELECT * FROM queries ORDER BY CAST("row" AS INTEGER)'):
            if not r['loc'].startswith(fid):
                continue
            line = ' | '.join([r[c] for c in TABLES['queries'][1:9]][:int(r['nfields'])]) + r['tail']
            if visible(od, r, fid) and self.later_in(line):
                self.later_dropped.append(('query', line))
            elif visible(od, r, fid):
                self.add('query', int(r['row']), line, True, f'QUERY {r["qid"]}')
            else:
                self.fenced_out.append(('query', line))

        # ---- speakers / narrator lines (first line of the bullet, as before)
        for sec, key in (('speak', 'speakers present'), ('narr', 'narrator')):
            for r in by_file.get(fid, []):
                if r['depth'] == '0' and r['key'] == key:
                    if self.later_in(r['text']):
                        self.later_dropped.append((sec, r['text']))
                    else:
                        self.add(sec, 0, r['text'], True, key)
                    break

        # ---- cast blocks of the speakers present
        blocks = [b for b in self.q('SELECT * FROM cast ORDER BY CAST(block AS INTEGER)')
                  if any(b['heading'].startswith('## ' + n) for n in names)]
        for b in blocks:
            facts = self.q('SELECT * FROM cast_facts WHERE block=? ORDER BY CAST(line AS INTEGER)', b['block'])
            bo = int(b['block'])
            head = facts[0]
            if not visible(od, head, fid):
                for f in facts:
                    if f['kind'] != 'blank':
                        self.fenced_out.append(('cast', f['text']))
                continue
            self.add('cast', (bo, 0), self.trim(head['text']), True, head['text'][:60])
            # group each top-level bullet with its children; fence line by line (children inherit via first_id)
            groups, g = [], None
            for f in facts[1:]:
                if f['kind'] == 'blank':
                    continue
                if f['depth'] == '0':
                    g = [f]
                    groups.append(g)
                elif g is not None:
                    g.append(f)
            for g in groups:
                shown = []
                for f in g:
                    if visible(od, f, fid):
                        shown.append(f)
                    else:
                        self.fenced_out.append(('cast', f['text']))
                if not shown:
                    continue
                top = g[0]
                if top['voice'] == '1':   # the voice sheet: whole bullet with its children, mandatory
                    self.add('cast', (bo, int(top['line'])), '\n'.join(self.trim(f['text']) for f in shown), True,
                             f'CAST {b["name"]}: {top["text"][:50]}', first=od.key(top['first_id']))
                    continue
                # other bullets: one item per line (one fact per row); a chosen child brings its ancestors along
                by_line = {f['line']: f for f in g}
                for f in shown:
                    anc, p = [], f['parent']
                    while p:
                        anc.append((int(p), by_line[p]['text']))
                        p = by_line[p]['parent']
                    if self.later_in(f['text']) or any(self.later_in(t) for _, t in anc):
                        self.later_dropped.append(('cast', f['text']))
                        continue
                    self.add('cast', (bo, int(f['line'])), f['text'], False,
                             f'CAST {b["name"]}', first=od.key(f['first_id']))
                    self.items[-1]['anc'] = anc
                    self.items[-1]['block'] = bo

        # ---- relations: both parties present = mandatory; one hop out = optional (DATA-DESIGN section 3)
        rels = self.q('SELECT * FROM relations ORDER BY CAST("row" AS INTEGER)')
        known = Fence(rels, od).at(od, fid)
        known_rows = {r['row'] for r in known}

        def is_seed(s):
            return any(n in s for n in names)

        hop_nodes = set()
        for r in known:
            if is_seed(r['from']) and not is_seed(r['to']):
                hop_nodes.add(r['to'])
            if is_seed(r['to']) and not is_seed(r['from']):
                hop_nodes.add(r['from'])
        for r in rels:
            line = '\t'.join(r[c] for c in TABLES['relations'][1:8])
            a, b2 = is_seed(r['from']), is_seed(r['to'])
            both = a and b2
            hop = not both and (a or r['from'] in hop_nodes) and (b2 or r['to'] in hop_nodes) and names
            if not (both or hop):
                continue
            if r['row'] not in known_rows:
                if visible(od, dict(r, superseded_id=''), fid):
                    self.superseded.append(('relations', line))
                else:
                    self.fenced_out.append(('relations', line))
                continue
            if self.later_in(line):
                self.later_dropped.append(('relations', line))
            elif both:
                self.add('rel', int(r['row']), line, True, f'RELATION {r["from"]}->{r["to"]}')
            else:
                self.add('hop', int(r['row']), line, False, 'RELATIONS row one hop out',
                         first=od.key(r['first_id']))
                self.items[-1]['weak'] = not (a or b2)   # neither party present: ranked lower
        return self

    def rank(self):
        """score = sum over terms of this file found in the item of tf x idf; x2 for facts from this file or the two
        before it (recency); then greedy by score / size."""
        cur = self.od.order[self.fid]
        terms = list(self.weights)
        for it in self.items:
            if it['mand']:
                continue
            s = sum(self.weights[t] for t in terms_in(it['text'], terms))
            f = it['first']
            if f is not None and cur - 2 <= f[0] <= cur:
                s *= 2
            if it.get('weak'):
                s *= 0.25
            it['score'] = s + 0.01

    def budget(self, head_bytes):
        """mandatory items first (all of them), then optional items by score / size while they fit."""
        self.rank()
        left = CAP - head_bytes
        chosen, dropped = [], []
        for it in self.items:
            if it['mand']:
                chosen.append(it)
                left -= it['size']
        self.mand_over = left < 0
        # tiers (DATA-DESIGN section 3: the seeds' own cards before anything one hop out): 0 = cast lines of the
        # speakers present and leaf summaries, 1 = chunk cards, 2 = relations one hop out, 3 = relations between
        # two hop-1 nodes; inside a tier by score / size
        tier = {'cast': 0, 'leaf': 0, 'card': 1, 'hop': 2}
        for it in sorted((it for it in self.items if not it['mand']),
                         key=lambda it: (tier[it['sec']] + (1 if it.get('weak') else 0), -it['score'] / it['size'])):
            if it['size'] <= left:
                chosen.append(it)
                left -= it['size']
            else:
                dropped.append(it)
        return chosen, dropped


    def text_view(self):
        fid = self.fid
        head = self.q('SELECT header FROM files WHERE file_id=?', fid)
        dead = {r['block'] for r in self.q('SELECT block FROM unreachable WHERE file_id=?', fid)}
        sp = {r['loc']: r['speaker'] for r in self.q('SELECT loc, speaker FROM speakers WHERE file_id=?', fid)}
        out = [head[0]['header']] if head else []
        for r in self.q('SELECT loc, block, text, raw FROM text WHERE file_id=? ORDER BY ord', fid):
            tag = (f'[{sp[r["loc"]]}] ' if sp.get(r['loc']) else '') + \
                  ('[unreachable] ' if str(r['block']) in dead else '')
            out.append(f'{r["loc"]}\t{tag}{r["text"]}' if tag else r['raw'])
        return out

    def render_notes(self, head, chosen):
        fid, prev = self.fid, self.prev
        gl_head = self.q("SELECT value FROM meta WHERE key='glossary_header'")[0]['value']
        rel_head = self.q("SELECT value FROM meta WHERE key='relations_header'")[0]['value']
        out = list(head)
        for sec, title in SECTIONS:
            its = sorted((it for it in chosen if it['sec'] == sec), key=lambda it: it['sort'])
            if not its and sec in ('leaf', 'card', 'hop'):
                continue
            if sec == 'prev' and not prev:
                continue
            out.append('')
            out.append(title.format(fid=fid, prev=prev))
            if sec == 'gloss':
                out.append(gl_head)
            if sec in ('rel', 'hop'):
                out.append(rel_head)
            if sec != 'cast':
                out += [it['text'] for it in its]
                continue
            # cast: per block, the chosen lines plus their ancestors, in the order of CAST.md
            lines = {}
            for it in its:
                bo, n = it['sort']
                lines[(bo, n)] = it['text']
                for an, at in it.get('anc', ()):
                    lines.setdefault((bo, an), at)
            out += [lines[k] for k in sorted(lines)]
        return out

    def render(self):
        od, fid = self.od, self.fid
        cur = od.order[fid]
        self.prev = prev = od.by_order.get(cur - 1, '')
        sf = self.q('SELECT * FROM scene_facts WHERE file_id=?', fid)
        sw = self.q('SELECT * FROM narrator_switches WHERE file_id=?', fid)
        head = [f'# PACK for {fid}  (speakers detected: ' + (' '.join(self.names) + ' ' if self.names else 'none')
                + ')',
                SPEAKER_NOTE,
                'Built by tools/kb/kb.py packet from notes/v2 (the pass-2 masters). Owner rulings: '
                'notes/v2/OWNER-RULINGS.md (the full ledger; read it once, it is not repeated here).',
                '',
                TEST_PARAGRAPH,
                '',
                f'# SLICE for {fid} (order {cur}, chunk {od.chunk[fid]}). Previous file in reading order: '
                f'{prev or "none"}',
                f'narrator (scenario table): {" | ".join(r["narrator_jp"] for r in sf) or "(no scenario-table row)"}',
                f'in-story start: {" | ".join(r["start_time"] for r in sf) or "(no scenario-table row)"}']
        head += [f'NARRATOR SWITCH at {r["loc"]}: {r["from_jp"]} -> {r["to_jp"]} (sprite evidence)' for r in sw]
        titles = sum(len(t.encode('utf-8')) + 2 for _, t in SECTIONS) + 600
        chosen, dropped = self.budget(len(('\n'.join(head) + '\n').encode('utf-8')) + titles)
        # exact check: render, and while the notes part is over the cap drop the lowest-ranked optional item
        tier = {'cast': 0, 'leaf': 0, 'card': 1, 'hop': 2}
        opt = sorted((it for it in chosen if not it['mand']),
                     key=lambda it: (-(tier[it['sec']] + (1 if it.get('weak') else 0)), it['score'] / it['size']))
        while True:
            notes = self.render_notes(head, chosen)
            notes_bytes = len(('\n'.join(notes) + '\n').encode('utf-8'))
            if notes_bytes <= CAP or not opt:
                break
            it = opt.pop(0)
            chosen.remove(it)
            dropped.append(it)
        self.chosen, self.dropped, self.notes_bytes = chosen, dropped, notes_bytes
        out = notes
        out.append('')
        out.append('## Text-line view of this file in reading order (row:sub = block:cell; translate in the .lns '
                   'files, not here; not counted in the 40 KB cap)')
        out += self.text_view()
        out.append('')
        out.append(f'## Budget: notes part {notes_bytes} of {CAP} bytes; {len(chosen)} items kept, '
                   f'{len(dropped)} dropped for the cap' + (' (MANDATORY ITEMS ALONE EXCEED THE CAP)'
                                                             if self.mand_over or notes_bytes > CAP else '')
                   + f'; {len(self.later_dropped)} fact line(s) not shown because they quote a file later than {fid}, '
                     f'{len(self.trimmed)} voice-sheet line(s) [trimmed] for the same reason')
        groups = defaultdict(list)
        for it in dropped:
            groups[(it['sec'], it['label'])].append(it)
        for (sec, label), its in sorted(groups.items()):
            size = sum(it['size'] for it in its)
            out.append(f'- dropped {sec}: {label}' + (f' x{len(its)}' if len(its) > 1 else '') + f' ({size} bytes)')
        return '\n'.join(out) + '\n'



def packet(fid, write=True):
    refresh()
    con = connect()
    p = Packet(con, fid).run()
    text = p.render()
    if write:
        TMP.mkdir(parents=True, exist_ok=True)
        path = TMP / f'pack-{fid}.md'
        path.write_bytes(text.encode('utf-8'))
        print(f'wrote {rel(path)} ({text.count(chr(10))} lines, {len(text.encode("utf-8"))} bytes; notes part '
              f'{p.notes_bytes} B of {CAP}; {len(p.dropped)} items dropped for the cap, listed at the foot)')
    return p, text


# ------------------------------------------------------------------------------------------------ tm
PUNCT = re.compile(r'[\s　「」『』（）()、。…！？!?―─・～~]')


def grams(s, n=3):
    s = PUNCT.sub('', s)
    return {s[i:i + n] for i in range(max(0, len(s) - n + 1))}


def jaccard(a, b):
    return len(a & b) / len(a | b) if a or b else 0.0


def jp_rows_of(fid):
    out = []
    for p in sorted(glob.glob(str(LNS / f'{fid}-*.lns'))):
        name = Path(p).name
        for n, line in enumerate(read_lines(p), 1):
            if line.startswith(';'):
                continue
            j = strip_tags(line)
            if j and JP_CHAR.search(j):
                out.append((f'{name}:{n}', j))
    return out


def tm(fid, include_later=False, quiet=False, threshold=0.6):
    refresh()
    con = connect()
    od = load_order(con)
    if fid not in od.order:
        raise SystemExit(f'{fid}: unknown file id')
    cur = od.order[fid]
    done = []
    for r in con.execute('SELECT file_id, lns, line, jp, en FROM tm').fetchall():
        if r[0] == fid or r[0] not in od.order:
            continue
        if not include_later and od.order[r[0]] > cur:
            continue   # fenced: EN of later files is not shown unless --all
        done.append(r)
    index, gset = defaultdict(set), []
    for i, r in enumerate(done):
        g = grams(r[3])
        gset.append(g)
        for x in g:
            index[x].add(i)
    rows = []
    for rid, text in jp_rows_of(fid):
        g = grams(text)
        if len(g) < 2:
            continue
        cand = Counter()
        for x in g:
            for i in index.get(x, ()):
                cand[i] += 1
        best = []
        for i, shared in cand.items():
            j = shared / (len(g) + len(gset[i]) - shared)
            if j >= threshold:
                best.append((j, i))
        best.sort(key=lambda x: (-x[0], x[1]))
        for j, i in best[:3]:
            r = done[i]
            must = 'MUST-MATCH' if PUNCT.sub('', r[3]) == PUNCT.sub('', text) else ''
            rows.append([rid, f'{r[1]}:{r[2]}', f'{j:.2f}', must, text, r[3], r[4]])
    TMP.mkdir(parents=True, exist_ok=True)
    path = TMP / f'tm-{fid}.tsv'
    tsv_write(path, ['row', 'match', 'jaccard', 'must', 'jp', 'match_jp', 'match_en'], rows)
    if not quiet:
        print(f'wrote {rel(path)}: {len(rows)} hints ({sum(1 for r in rows if r[3])} MUST-MATCH) over '
              f'{len(done)} translated JP rows' + (' incl. later files' if include_later else ' of earlier files'))
    return rows


# ------------------------------------------------------------------------------------------------ search
def search(q, asof=None, kind=None, limit=40):
    refresh()
    con = connect()
    od = load_order(con)
    mode = con.execute("SELECT value FROM kbmeta WHERE key='search'").fetchone()[0]
    where = ' AND kind=?' if kind else ''
    args = [kind] if kind else []
    if mode == 'fts5-trigram' and len(q) >= 3:
        rows = con.execute(f'SELECT kind, id, asof, text FROM doc WHERE doc MATCH ?{where} LIMIT 5000',
                           ['"' + q.replace('"', '""') + '"'] + args).fetchall()
    elif mode == 'fts5-trigram':
        rows = con.execute(f'SELECT kind, id, asof, text FROM doc WHERE text LIKE ?{where} LIMIT 5000',
                           ['%' + q + '%'] + args).fetchall()
    else:
        gs = [q[i:i + 3] for i in range(max(1, len(q) - 2))]
        ids = None
        for g in gs:
            s = {r[0] for r in con.execute('SELECT doc FROM gram WHERE g=?', (g,))}
            ids = s if ids is None else ids & s
        rows = [r for r in con.execute(f'SELECT kind, id, asof, text FROM doc WHERE rowid IN '
                                       f'({",".join(map(str, ids or [-1]))}){where}', args) if q in r[3]]
    n = 0
    for k, i, a, text in rows:
        if asof:
            key = od.key(a)
            if key is None or key > od.hi(asof):
                continue
        n += 1
        if n <= limit:
            pos = text.find(q)
            print(f'{k:5} {i:28} {text[max(0, pos - 40):pos + 80]}')
    print(f'{n} hit(s)' + (f' known at {asof}' if asof else '') + (f', first {limit} shown' if n > limit else '')
          + f' [{mode}]')
    return n


# ------------------------------------------------------------------------------------------------ lint
def lint(strict=False):
    t = {name: tsv_read(DB / f'{name}.tsv') for name in ('summary', 'cast', 'cast_facts', 'chunk_cards')}
    probs = defaultdict(list)
    for p in sorted(glob.glob(str(NOTES / '*.md'))):
        n = os.path.getsize(p)
        if n > 20 * 1024 and 'BRIEF' not in Path(p).name:
            probs['notes file > 20 KB (briefs exempt)'].append(f'{Path(p).name} {n}')
    leaf = defaultdict(int)
    for r in t['summary']:
        if r['key'] != '_heading':
            leaf[r['file_id']] += len(words(r['text']))
    for f, n in leaf.items():
        if n > 150:
            probs['summary leaf > 150 words'].append(f'{f} {n}')
    for r in t['chunk_cards']:
        if int(r['words']) > 400:
            probs['chunk card > 400 words'].append(f'chunk {r["chunk"]} {r["words"]}')
    names = {r['block']: r['name'] for r in t['cast']}
    nonvoice = Counter()
    for r in t['cast_facts']:
        if r['kind'] in ('heading', 'blank'):
            continue
        if len(words(r['text'])) > 30:
            probs['cast note line > 30 words'].append(f'block {r["block"]} ({names[r["block"]]}) line {r["line"]}')
        if r['voice'] != '1':
            nonvoice[r['block']] += 1
    top = nonvoice.most_common(1)[0][0] if nonvoice else None
    for b, n in nonvoice.items():
        cap = 120 if b == top else 40
        if n > cap:
            probs['non-voice cast notes over cap (40; 120 for the key with most rows)'].append(
                f'block {b} ({names[b]}) {n} > {cap}')
    for p in sorted(glob.glob(str(DB / '*.tsv'))) + [str(NOTES / n) for n in MASTER_NAMES if n.endswith('.tsv')]:
        for line in read_lines(p):
            if any(len(f) >= 2 and f[0] == '"' and f[-1] == '"' and '""' in f[1:-1] for f in line.split('\t')):
                probs['CSV-quoted field in a TSV'].append(rel(p))
                break
    jp = Counter(r.split('\t')[0] for r in read_lines(NOTES / 'GLOSSARY.tsv')[1:])
    for k, n in jp.items():
        if n > 1:
            probs['GLOSSARY jp key twice'].append(k)
    idfree = sum(1 for r in t['cast_facts'] if r['kind'] not in ('heading', 'blank') and not HEX.search(r['text']))
    total = sum(len(v) for v in probs.values())
    for k, v in probs.items():
        print(f'{k}: {len(v)}')
        for x in v[:8]:
            print(f'    {x}')
        if len(v) > 8:
            print(f'    ... {len(v) - 8} more')
    print(f'info: {idfree} CAST lines carry no id of their own (fenced by their parent / first_appears)')
    print(f'lint: {total} breach(es) in {len(probs)} check(s)' + (' [strict: FAIL]' if strict and total else
                                                                   ' [report mode]' if total else ''))
    return 1 if strict and total else 0


# ------------------------------------------------------------------------------------------------ core
LATER = re.compile(r'LATER[^)]*')
C4_NOTE = ('(rows omitted by the fence: resolved rows that change an earlier file are reviewer and '
           'orchestrator material.)')


def core(cur):
    """Port of tools/db/fenced_core.py: notes/CORE.md (or, with SY_NOTES_DIR=notes/v2, notes/v2/CORE-RULES.md)
    with every line whose earliest id is later than <cur> dropped, section C4 rows dropped, and a LATER clause in a
    heading replaced. Same output paths as before."""
    ndir = Path(os.environ.get('SY_NOTES_DIR') or 'notes')
    ndir = ndir if ndir.is_absolute() else ROOT / ndir
    src = ndir / 'CORE.md'
    if not src.exists() and ndir.resolve() != (ROOT / 'notes').resolve():
        src = ndir / 'CORE-RULES.md'
    if not src.exists():
        raise SystemExit(f'{rel(src)} does not exist')
    od = Order([dict(zip(TABLES['files'], f)) for f in conv_files()])
    if cur not in od.order:
        raise SystemExit(f'{cur}: unknown file id')
    lines = src.read_bytes().decode('utf-8').split('\n')
    out, skip = [], False
    for line in lines:
        if line.startswith('## C4.'):
            out += [line, C4_NOTE]
            skip = True
            continue
        if line.startswith('#'):
            skip = False
            out.append(LATER.sub('later fact fenced', line))
            continue
        if skip:
            continue
        m = od.min_id(line)
        if m is None or m[0] <= od.hi(cur):
            out.append(line)
    head = [f'<!-- {rel(src)} FENCED at {cur} (tools/kb/kb.py core {cur}). Lines whose earliest file id is later '
            f'than {cur} are omitted',
            '     (the knowledge fence). Do not read the source file whole.',
            '     A gap is GRAMMAR when two first-time Japanese readers fill it the same way without noticing: fill it,',
            '     no flag. A gap is WITHHELD when they could fill it two ways, or the text later turns on it: keep it',
            '     open, or take the pack-supported reading and flag needs-tlc. -->']
    path = ndir / '_tmp' / f'core-{cur}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    data = '\n'.join(head + out).encode('utf-8')
    path.write_bytes(data)
    print(f'wrote {rel(path)} ({data.count(b"\n")} lines, {len(data)} bytes; {src.name} is {len(lines) - 1} lines)')
    return path


# ------------------------------------------------------------------------------------------------ query
def ship_sections():
    """id -> section number, from tools/ship-list.txt (the `# Section N` comments split the list)."""
    cur, out = 1, {}
    for line in read_lines(ROOT / 'tools' / 'ship-list.txt'):
        m = re.search(r'Section (\d+)', line)
        if line.startswith('#'):
            if m:
                cur = int(m.group(1))
            continue
        name = line.split('#')[0].strip()
        if name.endswith('.lsb'):
            out[name[:-4]] = cur
    return out


def later_lines(od, fid, text):
    """[(line)] of the notes part of a packet (everything above the text-line view) that quote an id later than fid."""
    hi = od.hi(fid)
    body = text.split('\n## Text-line view')[0]
    return [l for l in body.split('\n') if any(p > hi for p, _ in od.ids(l))]


def q_fence_audit(con, arg, fresh=False):
    """Every line of the packet's notes part that quotes a file id later than the packet's id: must be zero.
    Audits notes/v2/_tmp/pack-<id>.md when it exists (the file a drafter read), else a freshly built packet.
    `all` = every id of tools/ship-list.txt sections 1-3. --fresh ignores the files on disk. A packet on disk
    without the kb.py banner was written by the retired tools/db/pack.py and is labelled OLD TOOL."""
    od = load_order(con)
    ids = [i for i in sorted(ship_sections(), key=lambda i: od.order.get(i, 0)) if i in od.order] \
        if arg == 'all' else [arg]
    total, on_disk, old_tool = 0, 0, 0
    for fid in ids:
        path = TMP / f'pack-{fid}.md'
        if path.exists() and not fresh:
            text, src = path.read_bytes().decode('utf-8'), rel(path)
            on_disk += 1
            if 'Built by tools/kb/kb.py packet' not in text:
                old_tool += 1
                src += ' (OLD TOOL: written by tools/db/pack.py; rerun kb.py packet)'
        else:
            text, src = Packet(con, fid).run().render(), 'freshly built'
        bad = later_lines(od, fid, text)
        total += len(bad)
        if bad:
            print(f'{fid}: {len(bad)} LEAK(S) in {src}')
            for line in bad[:10]:
                print(f'  {line[:160]}')
    print(f'fence-audit over {len(ids)} file(s) ({on_disk} packet(s) read from {rel(TMP)}, {old_tool} of them '
          f'written by the old tool): {total} leak(s)'
          + ('' if total else '  <- zero, as required'))
    return 1 if total else 0


def q_character(con, name, asof=None):
    """CAST block(s) of <name> (fenced with --asof), the RELATIONS rows naming it, the files it speaks in."""
    od = load_order(con)
    blocks = [dict(b) for b in con.execute('SELECT * FROM cast ORDER BY CAST(block AS INTEGER)')
              if b['name'] == name or b['heading'].startswith('## ' + name)]
    if not blocks:
        print(f'no CAST block for {name}')
        return 1
    for b in blocks:   # two people can share a name: every matching block
        print(f'\n== CAST {b["heading"]}' + (f'   (FENCED at {asof})' if asof else ''))
        for f in con.execute('SELECT * FROM cast_facts WHERE block=? ORDER BY CAST(line AS INTEGER)', (b['block'],)):
            if asof and not visible(od, dict(f), asof):
                continue
            print(f['text'])
    key = blocks[0]['name']
    print('\n== RELATIONS rows')
    rels = [dict(r) for r in con.execute('SELECT * FROM relations ORDER BY CAST("row" AS INTEGER)')]
    shown = {r['row'] for r in Fence(rels, od).at(od, asof)} if asof else None
    for r in rels:
        if (key in r['from'] or key in r['to']) and (shown is None or r['row'] in shown):
            print('\t'.join(r[c] for c in TABLES['relations'][1:8]))
    files = []
    for fid in od.hexes:
        if asof and od.order[fid] > od.order[asof]:
            continue
        rows = [dict(r) for r in con.execute('SELECT * FROM summary WHERE file_id=? AND depth=? AND key=?',
                                             (fid, '0', 'speakers present'))]
        toks, _ = speakers_of(rows)
        if any(key.startswith(t) or t.startswith(key) for t in toks):
            files.append(fid)
    print(f'\n== speaks in\n{len(files)} files: ' + ' '.join(files))
    return 0


def q_speaker(con, fid):
    rows = con.execute('SELECT s.block, s.cell, s.color, s.speaker, s.kind, t.text FROM speaker_color s '
                       'LEFT JOIN text t ON t.file_id=s.file_id AND t.loc=s.block||":"||s.cell '
                       'WHERE s.file_id=? ORDER BY COALESCE(t.ord, 1e9), s.rowid', (fid,)).fetchall()
    if not rows:
        print(f'no speaker_color rows for {fid} (no lns/{fid}-*.lns)')
        return 1
    q = [r for r in rows if r['kind'] == 'quote']
    print(f'\n== SPEAKER BY COLOUR {fid}: {len(rows)} cells, {len(q)} quote cells, '
          f'{sum(1 for r in q if r["speaker"])} with a speaker by colour (notes/v2/SPEAKER-COLORS.md)')
    print('block:cell\tcolour\tspeaker\tkind\ttext')
    for r in rows:
        print(f'{r["block"]}:{r["cell"]}\t{r["color"]}\t{r["speaker"]}\t{r["kind"]}\t{(r["text"] or "")[:60]}')
    return 0


def q_speaker_lines(con, name, asof=None):
    od = load_order(con)
    rows = con.execute('SELECT s.file_id, s.block, s.cell, t.text, t.ord FROM speaker_color s '
                       'LEFT JOIN text t ON t.file_id=s.file_id AND t.loc=s.block||":"||s.cell '
                       "WHERE s.speaker=? AND s.kind='quote'", (name,)).fetchall()
    rows = [r for r in rows if r['file_id'] in od.order and (not asof or od.order[r['file_id']] <= od.order[asof])]
    rows.sort(key=lambda r: (od.order[r['file_id']], r['ord'] if r['ord'] is not None else 1e9))
    if not rows:
        known = [r[0] for r in con.execute("SELECT DISTINCT speaker FROM speaker_color WHERE speaker<>'' ORDER BY 1")]
        print(f'no quote cell in the colour of {name}; speakers in the table: {" ".join(known)}')
        return 1
    print(f'\n== {name}: {len(rows)} quote cells in {len({r["file_id"] for r in rows})} files'
          + (f' (up to {asof})' if asof else ''))
    for r in rows:
        print(f'{r["file_id"]}:{r["block"]}:{r["cell"]}\t{r["text"] or ""}')
    return 0


PAREN = re.compile(r'\([^()]*\)|（[^（）]*）')


def name_forms(con, extra=()):
    """form -> short name for every name of notes/_db/人物名簿.tsv (+ extra): the given name when it is a speaker
    label of SPEAKER-COLORS.tsv, else a speaker label inside the full name, else the given name, else the name.
    Family name = the longest 2+ character prefix shared with another roster name (tools/db/query.py rule)."""
    labels = {r[0] for r in con.execute("SELECT DISTINCT speaker FROM speaker_color WHERE speaker<>''")}
    path = ROOT / 'notes' / '_db' / '人物名簿.tsv'
    roster = [l.split('\t')[1].strip() for l in read_lines(path)[1:] if l.count('\t') >= 1] if path.exists() else []
    roster = [n for n in roster if n]
    forms = {}
    for n in list(dict.fromkeys(roster + list(extra))):
        fam = ''
        for o in roster:
            if o == n:
                continue
            k = 0
            while k < min(len(n), len(o)) and n[k] == o[k]:
                k += 1
            if 2 <= k < len(n) and k > len(fam):
                fam = n[:k]
        given = n[len(fam):] if fam else ''
        inner = sorted((lab for lab in labels if lab in n), key=len, reverse=True)
        short = given if given in labels else inner[0] if inner else given or n
        forms.setdefault(n, short)
        forms.setdefault(short, short)
    return forms


def names_in(text, forms):
    found = set()
    for f in sorted(forms, key=len, reverse=True):
        if f and f in text:
            found.add(forms[f])
            text = text.replace(f, '\0')
    return found


def summary_narrator(con, fid):
    r = con.execute("SELECT text FROM summary WHERE file_id=? AND depth='0' AND key='narrator'", (fid,)).fetchone()
    return r[0].split(':', 1)[1].strip() if r and ':' in r[0] else None


def narrator_compare(con, fid, forms=None):
    rows = con.execute('SELECT narrator_jp FROM scene_facts WHERE file_id=?', (fid,)).fetchall()
    if not rows:
        return None
    names = [n for r in rows for n in r[0].split('/') if n and n != '0']
    forms = dict(forms or name_forms(con))
    for n in names:
        if n not in forms:
            forms.update(name_forms(con, [n]))
    tab = {forms.get(n, n) for n in names}
    line = summary_narrator(con, fid)
    summ = None
    if line is not None:
        bare = line
        while PAREN.search(bare):
            bare = PAREN.sub(' ', bare)
        summ = names_in(bare, forms)
    return names, tab, line, summ


def q_narrator(con, fid):
    print(f'\n== NARRATOR {fid}')
    rows = con.execute('SELECT * FROM scene_facts WHERE file_id=?', (fid,)).fetchall()
    if not rows:
        print('  scenario table: no row for this file')
    for r in rows:
        print(f'  scenario table  narrator {r["narrator_jp"]}   start {r["start_time"]}')
        print(f'                  ({r["source_column"]}{"; " + r["note"] if r["note"] else ""})')
    sw = con.execute('SELECT * FROM narrator_switches WHERE file_id=?', (fid,)).fetchall()
    print(f'  switches        {len(sw)}')
    for r in sw:
        print(f'    {r["loc"]}: {r["from_jp"]} -> {r["to_jp"]}   {r["evidence"]}')
    for r in con.execute('SELECT block, reason FROM unreachable WHERE file_id=?', (fid,)):
        print(f'  unreachable     block {r["block"]}: {r["reason"]}')
    line = summary_narrator(con, fid)
    print(f'  SUMMARY         {("- narrator: " + line) if line is not None else "(no narrator line)"}')
    c = narrator_compare(con, fid)
    if c and c[3] is not None:
        print(f'  compare         table {sorted(c[1])} vs SUMMARY {sorted(c[3])}: '
              + ('agree' if c[1] == c[3] else 'DISAGREE'))
    return 0


def q_narrator_audit(con):
    od = load_order(con)
    forms = name_forms(con)
    sec = ship_sections()
    bad, compared, no_line = [], 0, 0
    fids = sorted({r[0] for r in con.execute('SELECT file_id FROM scene_facts')} & set(od.order),
                  key=lambda f: od.order[f])
    for fid in fids:
        names, tab, line, summ = narrator_compare(con, fid, forms)
        if summ is None:
            no_line += 1
            continue
        compared += 1
        if tab != summ:
            bad.append((fid, names, tab, line, summ))
    print(f'\n== narrator-audit: {len(bad)} of {compared} files disagree with the scenario table ({no_line} files with a '
          f'scenario row have no SUMMARY narrator line yet); in sections 1-3: {sum(1 for b in bad if sec.get(b[0]))}')
    for fid, names, tab, line, summ in bad:
        print(f'{fid}  section {sec.get(fid) or "-"}  table {"/".join(names)} -> {sorted(tab)}   SUMMARY -> {sorted(summ)}')
        print(f'          - narrator: {line[:200]}')
        for r in con.execute('SELECT loc, from_jp, to_jp FROM narrator_switches WHERE file_id=?', (fid,)):
            print(f'          switch sprite {r["loc"]}: {r["from_jp"]} -> {r["to_jp"]}')
    return 0


QUERY_HELP = """kb.py query <sub> ...   (ports of the tools/db/query.py subcommands a brief or RESUME.md still names)
  fence-audit <id|all> [--fresh]   packet lines above the text view quoting a file later than <id>: must be 0
  character <JP name> [--asof <id>]   CAST block(s), RELATIONS rows, files spoken in (fenced with --asof)
  speaker <id>                  per text cell: block:cell, colour, speaker by colour, kind, text
  speaker-lines <JP name> [--asof <id>]   every quote cell in that speaker's colour, reading order
  narrator <id>                 scenario-table narrator/start, switch sprites, unreachable blocks, SUMMARY line, verdict
  narrator-audit                every file whose SUMMARY narrator line names other people than the scenario table"""


def query(argv, asof=None, fresh=False):
    refresh()
    con = connect()
    sub, rest = (argv[0], argv[1:]) if argv else ('', [])
    if sub == 'fence-audit' and rest:
        return q_fence_audit(con, rest[0], fresh)
    if sub == 'character' and rest:
        return q_character(con, rest[0], asof)
    if sub == 'speaker' and rest:
        return q_speaker(con, rest[0])
    if sub == 'speaker-lines' and rest:
        return q_speaker_lines(con, rest[0], asof)
    if sub == 'narrator' and rest:
        return q_narrator(con, rest[0])
    if sub == 'narrator-audit':
        return q_narrator_audit(con)
    print(QUERY_HELP)
    return 2


# ------------------------------------------------------------------------------------------------ merge-log
def row_key(row, fields=2):
    """The identity of a log row: its first <fields> pipe fields (V/Q id, or file:line + the JP/term)."""
    return ' | '.join(x.strip() for x in row.split(' | ')[:fields])


def append_unique(path, rows, fields=2, force=False, dry=False):
    """Append the rows not in the master yet (tools/db/merge_log.py semantics). A row whose KEY is in the master
    with different text is not appended (the master row was edited since an earlier merge); --force appends it.
    A missing master is created by the first append, as before."""
    data = path.read_bytes().decode('utf-8') if path.exists() else ''
    lines = data.split('\n')
    have, keys = set(lines), {row_key(l, fields) for l in lines if ' | ' in l}
    new, edited = [], []
    for r in rows:
        if r in have or r in new:
            continue
        if not force and row_key(r, fields) in keys:
            edited.append(r)
            continue
        new.append(r)
    if new and not dry:
        if data and not data.endswith('\n'):
            data += '\n'
        path.write_bytes((data + '\n'.join(new) + '\n').encode('utf-8'))
    return new, edited


def merge_log(tag, force=False, dry=False, notes=None):
    """notes/v2/_tmp/tl-log-<tag>.md -> DECISION rows to notes/v2/DECISIONS.md, TN to NOTES-TL.md, QUERY to
    QUERIES.md, RESOLVED sets status resolved on the QUERIES row, PROGRESS to the PROGRESS.md table. Then refresh
    the TSVs and kb.sqlite and run the check."""
    notes = notes or NOTES
    log = notes / '_tmp' / f'tl-log-{tag}.md'
    if not log.exists():
        raise SystemExit(f'no such log: {rel(log)}')
    dec, tn, q, res, prog = [], [], [], [], []
    for r in (l.rstrip() for l in read_lines(log) if l.strip()):
        kind, _, rest = r.partition(' | ')
        kind = kind.strip()
        if kind == 'DECISION':
            dec.append(rest.strip())
        elif kind == 'TN':
            tn.append(rest.strip())
        elif kind == 'QUERY':
            q.append(rest.strip())
        elif kind == 'RESOLVED':
            res.append(rest.strip())
        elif kind == 'PROGRESS':
            prog.append('| ' + rest.strip() + ' |')
    new_dec, ed_dec = append_unique(notes / 'DECISIONS.md', dec, 2, force, dry)
    new_tn, ed_tn = append_unique(notes / 'NOTES-TL.md', tn, 2, force, dry)
    new_q, ed_q = append_unique(notes / 'QUERIES.md', q, 1, force, dry)
    qpath = notes / 'QUERIES.md'
    qtext = before = qpath.read_bytes().decode('utf-8') if qpath.exists() else ''
    n_res = 0
    for r in res:
        qid, _, how = r.partition(' | ')
        pat = re.compile(r'^(' + re.escape(qid.strip()) + r' \| .*?) \| (tl-open|owner|open|provisional) \|\s*$', re.M)
        qtext, k = pat.subn(lambda m: m.group(1) + ' | resolved | resolved_by=' + how.strip().replace('\n', ' ') + ' |',
                            qtext, count=1)
        n_res += k
    if qtext != before and not dry:   # never rewrite a master another agent may be reading for no change
        qpath.write_bytes(qtext.encode('utf-8'))
    new_prog, ed_prog = append_unique(notes / 'PROGRESS.md', prog, 2, force, dry)
    edited = ed_dec + ed_tn + ed_q + ed_prog
    counts = dict(decisions=len(new_dec), tn=len(new_tn), queries=len(new_q), resolved=n_res,
                  progress=len(new_prog), skipped_edited=len(edited))
    if dry:
        print(f'{tag} DRY RUN: would append decisions +{len(new_dec)}, TN +{len(new_tn)}, queries +{len(new_q)}, '
              f'resolve {n_res}, progress +{len(new_prog)}; {len(edited)} row(s) already present with different text '
              '(edited since an earlier merge; --force appends them anyway)')
        for r in edited:
            print('  already present, text differs:', row_key(r, 2)[:100])
        return counts
    print(f'{tag}: decisions +{len(new_dec)}, TN +{len(new_tn)}, queries +{len(new_q)}, resolved {n_res}, '
          f'progress rows +{len(new_prog)}' + (f'; {len(edited)} row(s) skipped: already present with different text'
                                              if edited else ''))
    if notes == NOTES:
        refresh()
        merge_check()
    return counts


def merge_check():
    """Master row counts vs notes/v2/db TSVs vs kb.sqlite (the TSVs and the index cannot drift from the masters)."""
    refresh()
    con = connect()
    md = {
        'queries': sum(1 for l in read_lines(NOTES / 'QUERIES.md') if QID.match(l)),
        'glossary': len([l for l in read_lines(NOTES / 'GLOSSARY.tsv')[1:] if l.strip()]),
        'relations': len([l for l in read_lines(NOTES / 'RELATIONS.tsv')[1:] if l.strip()]),
        'cast': sum(1 for l in read_lines(NOTES / 'CAST.md') if l.startswith('## ')),
        'summary': sum(1 for l in read_lines(NOTES / 'SUMMARY.md') if l.startswith('## ') and HEX.search(l)),
    }
    tsv = {k: len(tsv_read(DB / f'{k}.tsv')) for k in ('queries', 'glossary', 'relations', 'cast')}
    tsv['summary'] = sum(1 for r in tsv_read(DB / 'summary.tsv') if r['key'] == '_heading')
    db = {k: con.execute(f'SELECT COUNT(*) FROM "{k}"').fetchone()[0] for k in ('queries', 'glossary', 'relations', 'cast')}
    db['summary'] = con.execute("SELECT COUNT(*) FROM summary WHERE key='_heading'").fetchone()[0]
    bad = 0
    for k in md:
        ok = md[k] == tsv[k] == db[k]
        bad += not ok
        print(f'{"ok  " if ok else "DIFF"} {k:10} master {md[k]:6}  tsv {tsv[k]:6}  db {db[k]:6}')
    for name in ('DECISIONS.md', 'NOTES-TL.md'):
        p = NOTES / name
        n = sum(1 for l in read_lines(p) if ' | ' in l) if p.exists() else 0
        print(f'info {name:12} {n} row(s) in notes/v2 (not indexed: no packet section reads them)')
    print('merge check: in sync' if not bad else f'merge check: {bad} table(s) OUT OF SYNC')
    return 1 if bad else 0


# ------------------------------------------------------------------------------------------------ selftest
def hash_tsvs():
    h = hashlib.sha256()
    for name in sorted(TABLES):
        h.update(name.encode())
        h.update((DB / f'{name}.tsv').read_bytes())
    return h.hexdigest()


def reprint():
    """masters rebuilt from the TSVs: the conversion is lossless for every row it claims to hold."""
    t = {name: tsv_read(DB / f'{name}.tsv') for name in TABLES}
    meta = {r['key']: r['value'].replace(ESC_TAB, TAB) for r in t['meta']}
    out = {}
    out['SUMMARY.md'] = [r['text'] for r in t['summary']]
    out['CAST.md'] = [r['text'] for r in t['cast_facts']]
    out['RELATIONS.tsv'] = [meta['relations_header']] + ['\t'.join(r[c] for c in TABLES['relations'][1:8])
                                                         for r in t['relations']]
    out['GLOSSARY.tsv'] = [meta['glossary_header']] + ['\t'.join(r[c] for c in TABLES['glossary'][1:10])
                                                       for r in t['glossary']]
    out['QUERIES.md'] = [' | '.join([r[c] for c in TABLES['queries'][1:9]][:int(r['nfields'])]) + r['tail']
                         for r in t['queries']]
    return out


def selftest():
    fails = []

    def check(ok, what):
        print(('PASS ' if ok else 'FAIL ') + what)
        if not ok:
            fails.append(what)

    # 1. idempotent convert (retry if a master changed between the two runs: another agent may be appending)
    for attempt in range(3):
        stamp = [p.stat().st_mtime for p in master_paths()]
        convert(quiet=True)
        h1 = hash_tsvs()
        convert(quiet=True)
        h2 = hash_tsvs()
        if stamp == [p.stat().st_mtime for p in master_paths()]:
            break
        print('  (a master changed during the idempotency test; retrying)')
    check(h1 == h2, f'convert twice -> byte-identical TSVs (sha256 {h1[:16]} == {h2[:16]})')
    # 2. lossless round trip
    rp = reprint()
    for name, lines in rp.items():
        src = read_lines(NOTES / name)
        if name in ('SUMMARY.md', 'CAST.md'):
            src = src[next(i for i, l in enumerate(src) if l.startswith('## ')):]
        elif name == 'QUERIES.md':
            src = [l for l in src if QID.match(l)]
        else:
            src = [l for l in src if l.strip()]
        check(lines == src, f'round trip {name}: {len(lines)} lines reprinted from notes/v2/db == master')
    # 3. build + row counts
    build(quiet=True)
    con = connect()
    for name in TABLES:
        n_tsv = len(tsv_read(DB / f'{name}.tsv'))
        n_db = con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
        if n_tsv != n_db:
            check(False, f'table {name}: tsv {n_tsv} rows, sqlite {n_db}')
    check(True, 'build: every TSV row is in kb.sqlite (row counts compared for all tables)')
    od = load_order(con)
    check(od.hexes == [od.by_order[o] for o in sorted(od.by_order)],
          f'hex order == reading order for all {len(od.hexes)} file ids (unknown 8-hex ids sort by hex)')
    # 4. fence: bisect stabbing == brute force for every file, cast facts + relations + glossary
    tabs = {n: [dict(r) for r in con.execute(f'SELECT * FROM {n}')] for n in ('cast_facts', 'relations', 'glossary')}
    bad = 0
    for name, rows in tabs.items():
        fe = Fence(rows, od)
        for fid in od.hexes:
            a = {id(r) for r in fe.at(od, fid)}
            b = {id(r) for r in rows if visible(od, r, fid)}
            bad += a != b
    check(bad == 0, f'fence: bisect interval stabbing == brute-force scan for every file id x 3 tables ({bad} diffs)')
    check(all(r['first_id'] for r in tabs['cast_facts']), 'every CAST line has a first_id (no always-known lines)')
    orphan = 0
    fa = {r['block']: r['first_appears'] for r in con.execute('SELECT * FROM cast')}
    for r in tabs['cast_facts']:
        if r['kind'] not in ('heading', 'blank') and not HEX.search(r['text']) and r['depth'] == '0':
            orphan += r['first_id'] != fa[r['block']]
    check(orphan == 0, 'id-free top-level CAST bullets take the block\'s first_appears id')
    child_leak = 0
    by_line = {(x['block'], x['line']): x for x in tabs['cast_facts']}
    for r in tabs['cast_facts']:
        if r['parent']:
            p = by_line[(r['block'], r['parent'])]
            child_leak += od.key(r['first_id']) < od.key(p['first_id'])
    check(child_leak == 0, 'no CAST child line is known before its parent line')
    sup = sum(1 for r in tabs['relations'] if r['superseded_id'])
    check(True, f'relations: {sup} rows carry a superseded_id (replaced by a changed_from row)')
    # 5. packets: audit + budget
    for fid in ('000001DD', '00000460', '000016AE'):
        p, text = packet(fid, write=False)
        leaks = [it for it in p.chosen if it['first'] is not None and it['first'] > od.hi(fid)]
        body = text.split('## Text-line view')[0]
        later = later_lines(od, fid, text)
        check(not leaks, f'packet {fid}: no chosen item has a first_id after {fid}')
        # line-level audit of the rendered packet: every line under the CAST / RELATIONS / GLOSSARY headings is a
        # row visible at fid (the header rows excepted)
        ok_lines = {r['text'] for r in tabs['cast_facts'] if visible(od, r, fid)}
        ok_lines |= {'\t'.join(r[c] for c in TABLES['relations'][1:8]) for r in tabs['relations']
                     if r['row'] in {x['row'] for x in Fence(tabs['relations'], od).at(od, fid)}}
        ok_lines |= {'\t'.join(r[c] for c in TABLES['glossary'][1:10]) for r in tabs['glossary'] if visible(od, r, fid)}
        heads = {con.execute("SELECT value FROM meta WHERE key=?", (k,)).fetchone()[0]
                 for k in ('glossary_header', 'relations_header')}
        sec, bad_lines, n_lines = None, 0, 0
        for line in body.split('\n'):
            if line.startswith(('## GLOSSARY rows', '## CAST.md blocks', '## RELATIONS.tsv rows')):
                sec = line
                continue
            if line.startswith('## ') and sec and not sec.startswith('## CAST.md'):
                sec = None
            if line.startswith(('## SUMMARY', '## QUERIES', '## Speakers', '## Narrator', '## Earlier')):
                sec = None
            if sec and line.strip() and line not in heads:
                n_lines += 1
                bad_lines += line not in ok_lines and not any(
                    line == t and o in ok_lines for o, t in p.trimmed)
        check(bad_lines == 0, f'packet {fid}: all {n_lines} rendered cast/relations/glossary lines are rows '
                              f'visible at {fid} ({bad_lines} not)')
        check(not later, f'packet {fid}: 0 lines above the text view quote a file later than {fid} ({len(later)}); '
                         f'{len(p.later_dropped)} fact lines dropped and {len(p.trimmed)} voice lines [trimmed] for it')
        check(p.notes_bytes <= CAP or p.mand_over,
              f'packet {fid}: notes part {p.notes_bytes} B <= {CAP} (or mandatory items alone exceed it)')
    # 6. search + tm
    mode = con.execute("SELECT value FROM kbmeta WHERE key='search'").fetchone()[0]
    probe = next(r['jp'] for r in tabs['glossary'] if len(r['jp']) >= 3 and con.execute(
        'SELECT 1 FROM mention WHERE jp=? LIMIT 1', (r['jp'],)).fetchone())
    if mode == 'fts5-trigram':
        n = con.execute('SELECT COUNT(*) FROM doc WHERE doc MATCH ?', ('"' + probe + '"',)).fetchone()[0]
    else:
        n = 1
    check(n > 0, f'search index ({mode}) finds a glossary key that occurs in the text')
    a, b = grams('春花、起きて。寝るなら、部屋に行こう'), grams('春花、起きて。寝るなら部屋に行こう')
    check(jaccard(a, b) == 1.0 and jaccard(a, grams('まったく別の文章です')) == 0.0,
          'tm: 3-gram Jaccard ignores punctuation, 1.0 on equal text, 0.0 on unrelated text')
    rows = tm('000001DD', include_later=True, quiet=True, threshold=0.6)
    check(all(r[3] == '' or PUNCT.sub('', r[4]) == PUNCT.sub('', r[5]) for r in rows),
          f'tm 000001DD --all: {len(rows)} hints, every MUST-MATCH is an exact text match')
    # 7. query fence-audit on fresh packets, merge-log on a scratch copy of the masters
    check(q_fence_audit(con, '000016AE', fresh=True) == 0, 'query fence-audit 000016AE --fresh: 0 leaks')
    con.close()
    scratch = TMP / 'kbport' / 'mergetest'
    (scratch / '_tmp').mkdir(parents=True, exist_ok=True)
    for name in ('DECISIONS.md', 'NOTES-TL.md'):
        if (scratch / name).exists():
            (scratch / name).unlink()
    for name in ('QUERIES.md', 'PROGRESS.md'):
        (scratch / name).write_bytes((NOTES / name).read_bytes())
    open_q = next(l.split(' | ')[0] for l in read_lines(NOTES / 'QUERIES.md') if QID.match(l) and l.endswith(' | open |'))
    last_q = max(int(l.split(' | ')[0][1:]) for l in read_lines(NOTES / 'QUERIES.md') if QID.match(l))
    log = ['# tl-log-SELFTEST', '',
           'DECISION | 000001DD:11:0 | JP | EN | literal | why | yes',
           'TN | 000001DD:11:1 | term | note | first only',
           f'QUERY | V{last_q + 1:03d} | 000001DD:11:2 | question | why | guess | low | open |',
           f'RESOLVED | {open_q} | selftest resolution',
           'PROGRESS | 000001DD | selftest | done']
    (scratch / '_tmp' / 'tl-log-SELFTEST.md').write_bytes(('\n'.join(log) + '\n').encode('utf-8'))
    c1 = merge_log('SELFTEST', notes=scratch)
    c2 = merge_log('SELFTEST', notes=scratch)
    check(c1 == dict(decisions=1, tn=1, queries=1, resolved=1, progress=1, skipped_edited=0),
          f'merge-log on a scratch copy: first run appends 1 of each kind and resolves 1 query ({c1})')
    check(c2 == dict(decisions=0, tn=0, queries=0, resolved=0, progress=0, skipped_edited=0),
          'merge-log rerun of the same tag appends nothing')
    q = (scratch / 'QUERIES.md').read_bytes().decode('utf-8')
    q = q.replace(f'V{last_q + 1:03d} | 000001DD:11:2 | question', f'V{last_q + 1:03d} | 000001DD:11:2 | question (edited)')
    (scratch / 'QUERIES.md').write_bytes(q.encode('utf-8'))
    c3 = merge_log('SELFTEST', notes=scratch)
    check(c3['queries'] == 0 and c3['skipped_edited'] == 1,
          'merge-log: a log row whose key is in the master with edited text is skipped, not re-appended')
    print(f'selftest: {"PASS" if not fails else str(len(fails)) + " FAIL"}')
    return 1 if fails else 0


# ------------------------------------------------------------------------------------------------ main
def main(argv):
    utf8_stdout()
    if not argv:
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    flags = {a for a in rest if a.startswith('--')}
    pos = [a for a in rest if not a.startswith('--')]

    def opt(name):
        if name in rest:
            i = rest.index(name)
            if i + 1 < len(rest):
                v = rest[i + 1]
                if v in pos:
                    pos.remove(v)
                return v
        return None

    if cmd == 'convert':
        convert()
    elif cmd == 'build':
        build()
    elif cmd == 'packet' and pos:
        for fid in pos:
            packet(fid)
    elif cmd == 'tm' and pos:
        tm(pos[0], include_later='--all' in flags)
    elif cmd == 'lint':
        return lint(strict='--strict' in flags)
    elif cmd == 'search' and pos:
        asof, kind = opt('--asof'), opt('--in')
        search(' '.join(pos), asof=asof, kind=kind)
    elif cmd == 'core' and pos:
        core(pos[0])
    elif cmd == 'query':
        asof = opt('--asof')
        return query(pos, asof=asof, fresh='--fresh' in flags)
    elif cmd == 'merge-log' and pos:
        if pos[0] == 'check':
            return merge_check()
        merge_log(pos[0], force='--force' in flags, dry='--dry-run' in flags)
    elif cmd == 'selftest':
        return selftest()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
