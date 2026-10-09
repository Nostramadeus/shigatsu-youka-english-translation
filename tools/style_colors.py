# Agents-only tool. Prints the text colour of every text cell in lns/<id>-*.lns.
# Colour comes from the "; Font styles:" header (TDecorate unk2). Style ids are per FILE, so the colour,
# not the id, is what carries across files. Method, colour -> speaker table: notes/v2/SPEAKER-COLORS.md.
#
# usage: style_colors.py [ids...]            -> id | file | cell | style ids used | colour | first 20 chars
#        style_colors.py --table [ids...]    -> per file: cells per (style id, colour) of the cell's outer run
#        style_colors.py --names [ids...]    -> runs inside non-quote cells whose colour differs from the
#                                               cell's colour (the coloured name tags) with their colour
#        style_colors.py --check [ids...]    -> compare cell segmentation with csv/<id>.csv
#        style_colors.py --speakers [ids...] -> id<TAB>block:cell<TAB>colour (hex, empty = uncoloured)<TAB>
#                                               speaker<TAB>kind (quote|narration|other); speaker = the JP name
#                                               notes/v2/SPEAKER-COLORS.tsv gives the colour in that file
#                                               (as_of_from/as_of_to file range), "" when the colour names
#                                               nobody there; colours missing from the TSV -> stderr
# no ids = every id in lns/.
# cell = block:line, the same key read/chunkNN.txt and the notes use (file:block:line).
# colour: unk2 is a Delphi TColor (0x00BBGGRR), printed as #RRGGBB. 4294967295 (-1) = "default".
# Text outside any <STYLE> tag is style 0 (pylm does not print ID 0); style 0's colour differs per file.
# Outer colour of a cell = colour of its opening 「/『 (or of its closing 」/』 for a continuation cell);
# other cells: the colour covering most characters (tie: the last character's).
# Cells end at every {command}, <PG>, <EVENT>, <VAR> (checked against csv/ for all ids: identical).
# Import use: from style_colors import cell_colours; cell_colours('00000024') -> {'16:0': '#AAAAFF', ...}
#             from style_colors import cell_speakers; cell_speakers('00000024') -> [{'cell','colour','speaker',
#             'kind'}, ...] (used by tools/db/build.py and tools/build_speaker_chunks.py)
import sys, os, re, io, csv, glob
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LNS = os.path.join(ROOT, 'lns')
CSV = os.path.join(ROOT, 'csv')
DEFAULT = 'default'

def colour(v):
    v = int(v)
    if v == 4294967295 or v < 0:
        return DEFAULT
    r, g, b = v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF
    return '#%02X%02X%02X' % (r, g, b)

def parse_header(lines):
    """style id -> (colour, unk4). unk4 looks like a font size (0 = normal)."""
    styles = {}
    for ln in lines:
        m = re.match(r';\s+(\d+): TDecorate\(count=\d+, unk2=(\d+), unk3=\d+, unk4=(\d+)', ln)
        if m:
            styles[int(m.group(1))] = (colour(m.group(2)), int(m.group(3)))
        if ln.startswith('; BEGIN'):
            break
    return styles

TOK = re.compile(r'(\{[^}]*\}|<[^>]*>)')

def segments(path):
    """-> styles, [(text, runs, style_ids_in_order)] per text cell. runs = [(style_id, text)]."""
    raw = io.open(path, encoding='utf-8').read()
    lines = re.split(r'\r\n|\r|\n', raw)
    styles = parse_header(lines)
    body, on = [], False
    for ln in lines:
        if ln.startswith('; BEGIN'):
            on = True; continue
        if ln.startswith('; END'):
            break
        if on and not ln.startswith(';'):
            body.append(ln)
    stack, runs, out = [], [], []

    def flush():
        txt = ''.join(t for _, t in runs)
        if txt.strip('\n'):
            ids = []
            for s, t in runs:
                if t.strip() and s not in ids:
                    ids.append(s)
            out.append((txt.strip('\n'), list(runs), ids))
        runs.clear()

    for tok in TOK.split(''.join(body)):
        if not tok:
            continue
        if tok.startswith('{'):
            flush()  # every command ends a cell (PAUSE, WAIT, ...), as in the csv
            continue
        if tok.startswith('<'):
            t = tok.upper()
            m = re.match(r'<STYLE ID="(\d+)"', tok)
            if m:
                stack.append(int(m.group(1)))
            elif t.startswith('</STYLE'):
                if stack:
                    stack.pop()
            elif t == '<PG>' or t.startswith('<EVENT') or t.startswith('<VAR'):
                flush()
            elif t == '<BR>' and runs:
                runs.append((stack[-1] if stack else 0, '\n'))
            continue
        runs.append((stack[-1] if stack else 0, tok))  # untagged text = style 0
    flush()
    return styles, out

def col(styles, s):
    return styles.get(s, (DEFAULT, 0))[0]

def outer_style(runs):
    chars = [(ch, s) for s, t in runs for ch in t if ch not in '\n 　']
    if not chars:
        return 0
    if chars[0][0] in '「『':
        return chars[0][1]
    if chars[-1][0] in '」』':
        return chars[-1][1]
    return None

def outer(styles, runs):
    s = outer_style(runs)
    if s is not None:
        return col(styles, s)
    cnt, last = Counter(), None
    for sid, t in runs:
        for ch in t:
            if ch not in '\n 　':
                last = col(styles, sid)
                cnt[last] += 1
    top = cnt.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return last
    return top[0][0]

def label_blocks(fid):
    """-> csv Label -> block number, and block -> [csv texts]."""
    p = os.path.join(CSV, fid + '.csv')
    lab, rows = {}, {}
    if not os.path.exists(p):
        return lab, rows
    rd = csv.reader(io.open(p, encoding='utf-8-sig')); next(rd)
    for r in rd:
        blk = r[0].split(':')[-2]
        if r[1]:
            lab[r[1]] = blk
        rows.setdefault(blk, []).append(r[3].replace('\r', ''))
    return lab, rows

def files_for(fid):
    lab, rows = label_blocks(fid)
    res = []
    for p in sorted(glob.glob(os.path.join(LNS, fid + '-*.lns'))):
        name = os.path.basename(p)[len(fid) + 1:-4]
        if name.startswith('line') and name[4:].isdigit():
            blk = name[4:]
        else:
            blk = lab.get(name, '?' + name)
        res.append((p, name, blk))
    return res, rows

def all_ids():
    return sorted({os.path.basename(p).split('-')[0] for p in glob.glob(os.path.join(LNS, '*.lns'))})

def cells(fid):
    fl, _ = files_for(fid)
    for p, name, blk in fl:
        styles, segs = segments(p)
        for i, (txt, runs, ids) in enumerate(segs):
            yield dict(id=fid, file=name, blk=blk, n=i, cell=f'{blk}:{i}', text=txt, runs=runs,
                       ids=ids, styles=styles, colour=outer(styles, runs))

def cell_colours(fid):
    return {c['cell']: c['colour'] for c in cells(fid)}


# ---------------------------------------------------------------- speaker by colour
# The colour -> speaker table is ONE data file, notes/v2/SPEAKER-COLORS.tsv (color, speaker, as_of_from,
# as_of_to, note); the method and the caveats are in notes/v2/SPEAKER-COLORS.md. A row with an empty speaker is a
# KNOWN colour that names nobody (default = uncoloured, #FF0000 / #FFFFFF = emphasis). A colour that is not in the
# table at all gets speaker "" and is reported once on stderr so the table can grow.
# File ranges (COLOR4): a colour may have several rows when it changes owner. A cell's speaker = the row of its
# colour whose [file of as_of_from, file of as_of_to] contains the cell's file id (as_of_to empty = open-ended).
# The colour's EARLIEST row is also open towards the start of the game: as_of_from is the first naming tag, and
# cells of that colour before it (e.g. 00000024:51:42 in #D0DA61, 00000697 in #68B4FF) keep their speaker, as before
# this column existed. A cell in a gap between two rows of one colour gets speaker "".
# File ids are 8 hex digits and the game order equals the hex order (notes/_db/_file-order.tsv), so a string
# compare is the order compare.
SPEAKER_TSV = os.path.join(ROOT, 'notes', 'v2', 'SPEAKER-COLORS.tsv')
# Blocks whose colours are decorative (colour changes mid-word): never a speaker by colour there.
DECORATIVE = {('00000488', '48')}   # the voice flood, SPEAKER-COLORS.md section 2
QUOTE_OPEN, QUOTE_CLOSE = '「『', '」』'
FID_RE = re.compile(r'^[0-9A-Fa-f]{8}')


def _fid(ref):
    m = FID_RE.match(ref or '')
    return m.group(0).upper() if m else ''


def load_speaker_table(path=SPEAKER_TSV):
    """colour -> [row, ...] sorted by start file; row = dict(speaker, as_of_from, as_of_to, note, lo, hi, first).
    lo/hi = file ids of as_of_from / as_of_to ('' = open). first = earliest row of its colour (open towards the
    start of the game). 'default' is the uncoloured key, as cell_colours returns it. Columns are found by the
    header names, so the column order may change."""
    lines = io.open(path, encoding='utf-8').read().splitlines()
    head = lines[0].split('	')
    ix = {h.strip(): i for i, h in enumerate(head)}
    table = {}
    for line in lines[1:]:
        if not line.strip() or line.startswith('#') and '	' not in line:
            continue
        c = line.split('	') + [''] * len(head)
        get = lambda k: c[ix[k]].strip() if k in ix else ''
        row = dict(speaker=get('speaker'), as_of_from=get('as_of_from'), as_of_to=get('as_of_to'), note=get('note'))
        row['lo'], row['hi'] = _fid(row['as_of_from']), _fid(row['as_of_to'])
        table.setdefault(get('color'), []).append(row)
    for rows in table.values():
        rows.sort(key=lambda r: r['lo'])
        for n, r in enumerate(rows):
            r['first'] = n == 0
    return table


def speaker_for(table, colour, fid):
    """The speaker of a cell in <colour> in file <fid>: the row whose file range contains fid (see above);
    '' when no row contains it. None when the colour is not in the table."""
    rows = table.get(colour)
    if rows is None:
        return None
    for r in rows:
        if (r['first'] or not r['lo'] or r['lo'] <= fid) and (not r['hi'] or fid <= r['hi']):
            return r['speaker']
    return ''


def cell_speakers(fid, table=None, unknown=None):
    """One dict per text cell of <fid> in lns order (block file order, then cell):
    cell, colour ('' = uncoloured), speaker ('' = none by colour), kind (quote | narration | other).

    kind: quote = the cell opens with 「/『 or a straight " (text messages), ends with 」/』, or continues a 「/『
    opened by the cell before it in the same block and not yet closed (a line split by {PAUSE});
    other = no visible text; narration = the rest.
    speaker: the table's name for the cell's colour, for every kind (a coloured narration cell is bracketless
    speech, a text message, a letter, or a name shown on its own; consumers that want quotes only filter kind).
    <unknown>, when given, is a Counter that collects colours missing from the table."""
    table = load_speaker_table() if table is None else table
    out, blk, depth = [], None, 0
    for c in cells(fid):
        if c['blk'] != blk:
            blk, depth = c['blk'], 0
        t = c['text'].replace('\n', '').strip(' 　')
        if not t:
            kind = 'other'
        elif t[0] in QUOTE_OPEN + '"' or t[-1] in QUOTE_CLOSE or depth > 0:   # "..." = a text message
            kind = 'quote'
        else:
            kind = 'narration'
        if kind == 'quote':
            for ch in t:
                if ch in QUOTE_OPEN:
                    depth += 1
                elif ch in QUOTE_CLOSE and depth:
                    depth -= 1
        else:
            depth = 0
        col = c['colour']
        spk = speaker_for(table, col, fid)
        if spk is None:
            spk = ''
            if unknown is not None:
                unknown[col] += 1
        if (fid, c['blk']) in DECORATIVE or kind == 'other':
            spk = ''
        out.append(dict(cell=c['cell'], colour='' if col == DEFAULT else col, speaker=spk, kind=kind))
    return out


def report_unknown(unknown, stream=None):
    """One stderr line per colour that is not in SPEAKER-COLORS.tsv (so the table can grow)."""
    stream = stream or sys.stderr
    for col, n in sorted(unknown.items(), key=lambda x: -x[1]):
        stream.write(f'unknown colour {col}: {n} cell(s), speaker left empty; add a row to '
                     f'notes/v2/SPEAKER-COLORS.tsv\n')

def main():
    args = sys.argv[1:]
    mode = 'list'
    if args and args[0] in ('--table', '--names', '--check', '--speakers'):
        mode = args.pop(0)[2:]
    ids = args or all_ids()
    out = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', newline='\n')
    if mode == 'speakers':
        table, unknown = load_speaker_table(), Counter()
        for fid in ids:
            for r in cell_speakers(fid, table, unknown):
                out.write(f"{fid}\t{r['cell']}\t{r['colour']}\t{r['speaker']}\t{r['kind']}\n")
        out.flush()
        err = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', newline='\n')
        report_unknown(unknown, err)
        err.flush()
        return
    for fid in ids:
        if mode == 'list':
            for c in cells(fid):
                ids_s = ','.join(map(str, c['ids'])) or '-'
                t = c['text'].replace('\n', '⏎')[:20]
                out.write(f"{fid} | {c['file']} | {c['cell']} | {ids_s} | {c['colour']} | {t}\n")
        elif mode == 'table':
            fl, _ = files_for(fid)
            for p, name, blk in fl:
                styles, segs = segments(p)
                if not segs:
                    continue
                cnt = Counter()
                for txt, runs, ids in segs:
                    sid = outer_style(runs)
                    if sid is None:
                        best = Counter()
                        for s, t in runs:
                            best[s] += len(t.strip())
                        sid = best.most_common(1)[0][0]
                    cnt[(sid, col(styles, sid))] += 1
                out.write(f'{fid} | {name} | block {blk} | {len(segs)} cells\n')
                for (sid, c), k in sorted(cnt.items(), key=lambda x: -x[1]):
                    size = styles.get(sid, (0, 0))[1]
                    out.write(f"    style {sid:>2} {c:8} size {size:>2}: {k}\n")
        elif mode == 'names':
            for c in cells(fid):
                if outer_style(c['runs']) is not None and c['text'].lstrip('　 ')[:1] in '「『':
                    continue
                for s, t in c['runs']:
                    k = col(c['styles'], s)
                    if t.strip() and k != c['colour']:
                        out.write(f"{fid} | {c['file']} | {c['cell']} | {k} | {t.strip()}\n")
        elif mode == 'check':
            fl, rows = files_for(fid)
            bad = tot = 0
            for p, name, blk in fl:
                _, segs = segments(p)
                want = rows.get(blk, [])
                got = [re.sub(r'<[^>]*>', '', t) for t, _, _ in segs]
                tot += len(want)
                if len(got) != len(want):
                    bad += 1
                    out.write(f'{fid} {name} block {blk}: lns {len(got)} cells, csv {len(want)}\n')
                    continue
                for i, (a, b) in enumerate(zip(got, want)):
                    if a.replace('\n', '') != b.replace('\n', ''):
                        bad += 1
                        out.write(f'{fid} {name} {blk}:{i}: lns {a[:30]!r} csv {b[:30]!r}\n')
                        break
            out.write(f'{fid}: csv cells {tot}, mismatching blocks {bad}\n')
    out.flush()

if __name__ == '__main__':
    main()
