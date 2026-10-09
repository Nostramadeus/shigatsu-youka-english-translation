"""Write the three machine-readable per-scene fact files of notes/v2/CLUES.md (hypotheses 2, 6, 7):

    uv run --no-project --python 3.12 python tools/build_scene_facts.py

  notes/v2/SCENE-FACTS.tsv       file_id  narrator_jp  start_time  source_column  note
      One row per file of notes/_db/_file-order.tsv that has a シナリオデータベース row. The join is the one of
      notes/v2/_tmp/tricks/scdb.py: _file-order id -> _navigator-order.tsv target_lsb -> entry id (連番) ->
      notes/_db/シナリオデータベース.tsv row. (notes/_db/_scenario-to-lsb.tsv is header-only, so it is not
      used.) narrator_jp = column 解禁人物 as written (one name, or two joined by `/`); start_time = column
      閲覧年月日 (in-story date and start time) with runs of spaces cut to one. CLUES 6: 31 of 33 part-1..3
      rows equal the pass-2 SUMMARY narrator, 0 contradict.
  notes/v2/NARRATOR-SWITCHES.tsv file_id  block:cell  from_jp  to_jp  evidence
      Every `立ち絵\\人物\\lcm\\X→Y.lcm` CG created (CREATECG/CHANGECG) inside a text block of lns/: the
      engine plays it where the first-person narrator changes from X to Y (CLUES 2). block:cell = the first
      text cell after the command, counted with the cell rule of tools/style_colors.py segments(); `<block>:end`
      when the CG follows the last text cell of its block (000004CF:12:end; swap.py missed it). Scanned
      from lns/ directly (stdlib), then compared with notes/v2/_tmp/tricks/swap-all.tsv when that file exists.
  notes/v2/UNREACHABLE.tsv       file_id  block  reason
      Text blocks no play can show (CLUES 7), from notes/v2/_tmp/tricks/reach-out.txt (reach.py over the
      pylivemaker dumps of the part-1..3 ids). 0000001E and 000000F2 are left out as CLUES 7 does: they are
      system/guide flows whose entry points reach.py does not model, so its `dead=` list there is not a fact.

Stdlib only. Reads lns/, notes/_db/, notes/v2/_tmp/tricks/; writes only the three TSVs. Rerun after lns/ or
the scenario table changes, then rebuild both dbs (tools/db/build.py) and tools/build_speaker_chunks.py.
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'notes', '_db')
V2 = os.path.join(ROOT, 'notes', 'v2')
TRICKS = os.path.join(V2, '_tmp', 'tricks')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import style_colors as sc  # noqa: E402

# CLUES 7, "Unreachable blocks": ids whose reach.py `dead=` list is not used (system/guide flows).
UNREACH_SKIP = {'0000001E', '000000F2'}
UNREACH_BASE = 'no path from label 0 or any incoming Jump/Call/PCReset (reach.py)'
# CLUES 7 table, the "note" column, per file (and per block where it differs).
UNREACH_NOTE = {
    ('0000034C', None): 'dead variant: command 4 jumps unconditionally (Calc=1) to block 17, the live twin; '
                        'no variable selects it',
    ('00000024', '67'): 'near-duplicate of block 16',
    ('00000024', None): 'empty block',
    ('000001DB', '21'): 'variant of block 15; only blocks 11 and 15 play',
    ('000001DB', '26'): 'empty block; only blocks 11 and 15 play',
    ('000001DB', '30'): 'variant of block 15; only blocks 11 and 15 play',
    ('000001DB', None): '隠しテキスト (backlog-image) cells after an unreached label',
}


def tsv(path):
    return [l.rstrip('\r\n').split('\t') for l in io.open(path, encoding='utf-8')]


def write(path, header, rows):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(header) + '\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    print(f'wrote {os.path.relpath(path, ROOT)}: {len(rows)} rows')


def scene_facts():
    order = [r[1] for r in tsv(os.path.join(DB, '_file-order.tsv'))[1:] if r and r[0].isdigit()]
    entry_of = {}
    for r in tsv(os.path.join(DB, '_navigator-order.tsv')):
        if not r or r[0].startswith('#') or r[0] == 'position' or len(r) < 4 or not r[3]:
            continue
        entry_of.setdefault(r[3], [])
        if r[1] not in entry_of[r[3]]:
            entry_of[r[3]].append(r[1])
    rows = tsv(os.path.join(DB, 'シナリオデータベース.tsv'))
    head = [h.strip() for h in rows[0]]
    ni, ti = head.index('解禁人物'), head.index('閲覧年月日')
    by = {r[0].strip(): r for r in rows[1:] if r and r[0].strip()}
    out = []
    for fid in order:
        entries = [e for e in entry_of.get(fid, []) if e in by]
        for e in sorted(entries, key=lambda x: int(x) if x.isdigit() else 0):
            r = by[e]
            narr = r[ni].strip() if len(r) > ni else ''
            start = re.sub(r'\s+', ' ', r[ti].strip()) if len(r) > ti else ''
            note = []
            if narr in ('', '0'):
                note.append('解禁人物 empty')
            if start in ('', '0'):
                note.append('閲覧年月日 empty')
            if len(entries) > 1:
                note.append(f'{len(entries)} navigator entries for this file')
            out.append([fid, narr, start, f'シナリオデータベース 連番 {e}: 解禁人物, 閲覧年月日', '; '.join(note)])
    return out


SWITCH_RE = re.compile(r'([^\\"]+)→([^\\".]+)\.lcm')
ARG = re.compile(r'"([^"]*)"')


def switches_in(path, blk):
    """[(cell, from, to, cg path)] for one .lns: the cell rule of style_colors.segments() (every {command},
    <PG>, <EVENT>, <VAR> ends a cell; a cell counts only if its text is not blank)."""
    raw = io.open(path, encoding='utf-8').read()
    body, on = [], False
    for ln in re.split(r'\r\n|\r|\n', raw):
        if ln.startswith('; BEGIN'):
            on = True
            continue
        if ln.startswith('; END'):
            break
        if on and not ln.startswith(';'):
            body.append(ln)
    idx, runs, pending, out = 0, [], [], []

    def flush():
        nonlocal idx
        if ''.join(runs).strip('\n'):
            for f, t, cg in pending:
                out.append((f'{blk}:{idx}', f, t, cg))
            pending.clear()
            idx += 1
        runs.clear()

    for tok in sc.TOK.split(''.join(body)):
        if not tok:
            continue
        if tok.startswith('{'):
            flush()
            cmd = tok[1:].split(' ')[0].rstrip('}')
            if cmd in ('CREATECG', 'CHANGECG'):
                for a in ARG.findall(tok):
                    m = SWITCH_RE.search(a)
                    if m and '→' in a:
                        pending.append((m.group(1), m.group(2), a))
            continue
        if tok.startswith('<'):
            t = tok.upper()
            if t == '<PG>' or t.startswith('<EVENT') or t.startswith('<VAR'):
                flush()
            elif t == '<BR>' and runs:
                runs.append('\n')
            continue
        runs.append(tok)
    flush()
    for f, t, cg in pending:   # a switch CG after the last text cell of the block: no cell to attach it to
        out.append((f'{blk}:end', f, t, cg))
    return out


def narrator_switches():
    out = []
    for fid in sc.all_ids():
        fl, _ = sc.files_for(fid)
        for p, _name, blk in fl:
            for cell, f, t, cg in switches_in(p, blk):
                where = ('after the last text cell of the block; applies from the next block played'
                         if cell.endswith(':end') else 'created before this cell')
                out.append([fid, cell, f, t, f'viewpoint-switch CG {cg} {where} (sprite evidence)'])
    ref = os.path.join(TRICKS, 'swap-all.tsv')
    if os.path.exists(ref):
        want = {(r[1], r[2]) for r in tsv(ref) if len(r) > 2}
        got = {(r[0], r[1]) for r in out}
        print(f'check vs {os.path.relpath(ref, ROOT)}: {len(want)} there, {len(got)} here, '
              f'only-there {sorted(want - got)}, only-here {sorted(got - want)}')
    return out


def unreachable():
    src = os.path.join(TRICKS, 'reach-out.txt')
    if not os.path.exists(src):
        sys.exit(f'{os.path.relpath(src, ROOT)} missing: rerun notes/v2/_tmp/tricks/reach.py (CLUES 7)')
    out = []
    for line in io.open(src, encoding='utf-8'):
        m = re.match(r'^([0-9A-F]{8})\tblocks=\S*\tdead=(\S+)', line)
        if not m or m.group(2) == '-' or m.group(1) in UNREACH_SKIP:
            continue
        fid = m.group(1)
        for b in m.group(2).split(','):
            note = UNREACH_NOTE.get((fid, b)) or UNREACH_NOTE.get((fid, None))
            out.append([fid, b, UNREACH_BASE + ('; ' + note if note else '')])
    return out


def main():
    write(os.path.join(V2, 'SCENE-FACTS.tsv'), ['file_id', 'narrator_jp', 'start_time', 'source_column', 'note'],
          scene_facts())
    write(os.path.join(V2, 'NARRATOR-SWITCHES.tsv'), ['file_id', 'block:cell', 'from_jp', 'to_jp', 'evidence'],
          narrator_switches())
    write(os.path.join(V2, 'UNREACHABLE.tsv'), ['file_id', 'block', 'reason'], unreachable())


if __name__ == '__main__':
    main()
