# Agents-only tool. Writes read/speakers/chunkNN.tsv next to every read/chunkNN.txt: one row per text line of
# the chunk, in the chunk's own order (### FILE order, then line order),
# `id<TAB>block:cell<TAB>speaker<TAB>narrator_switch<TAB>unreachable`.
#   speaker = the JP name when the cell is a quote and its text colour names the speaker,
#             `?` when the cell is a quote and the colour names nobody (uncoloured, emphasis, unmapped),
#             empty for narration and blank cells.
#   narrator_switch = the narrator from this cell on (to_jp of notes/v2/NARRATOR-SWITCHES.tsv) on the cell a
#             viewpoint-switch sprite lands on, else empty. A `<block>:end` switch has no cell and no mark here.
#   unreachable = 1 when the cell's block is in notes/v2/UNREACHABLE.tsv (no play shows it), else empty.
# Same convention as the `[speaker]` / `[unreachable]` tags of tools/db/pack.py. Sources: tools/style_colors.py
# cell_speakers (lns/ + notes/v2/SPEAKER-COLORS.tsv; notes/v2/SPEAKER-COLORS.md) and the two TSVs written by
# tools/build_scene_facts.py (notes/v2/CLUES.md hypotheses 2 and 7; missing file = one WARN line, column empty).
# Reads read/chunkNN.txt only for the cell ids; never writes it. Rerun after SPEAKER-COLORS.tsv grows or
# build_scene_facts.py is rerun.
#
# usage: uv run --no-project --python 3.12 python tools/build_speaker_chunks.py
import glob, io, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_colors import ROOT, cell_speakers, load_speaker_table, report_unknown  # noqa: E402

READ = os.path.join(ROOT, 'read')
OUT = os.path.join(READ, 'speakers')
V2 = os.path.join(ROOT, 'notes', 'v2')
FILE_RE = re.compile(r'^### FILE ([0-9A-F]{8})')


def tag(r):
    if r is None or r['kind'] != 'quote':
        return ''
    return r['speaker'] or '?'


def fact_rows(name):
    p = os.path.join(V2, name)
    if not os.path.exists(p):
        print(f'WARN missing source: notes/v2/{name} (its column stays empty)')
        return []
    return [l.rstrip('\r\n').split('\t') for l in io.open(p, encoding='utf-8').read().splitlines()[1:] if l.strip()]


def main():
    os.makedirs(OUT, exist_ok=True)
    table, unknown = load_speaker_table(), Counter()
    switch = {(r[0], r[1]): r[3] for r in fact_rows('NARRATOR-SWITCHES.tsv') if len(r) > 3}
    dead = {(r[0], r[1]) for r in fact_rows('UNREACHABLE.tsv') if len(r) > 1}
    tot = Counter()
    for path in sorted(glob.glob(os.path.join(READ, 'chunk*.txt'))):
        name = os.path.basename(path)[:-4]
        rows, fid, sp = [], None, {}
        for line in io.open(path, encoding='utf-8').read().splitlines():
            m = FILE_RE.match(line)
            if m:
                fid = m.group(1)
                sp = {r['cell']: r for r in cell_speakers(fid, table, unknown)}
                continue
            if fid is None or not line.strip():
                continue
            cell = line.split('\t', 1)[0]
            t = tag(sp.get(cell))
            sw = switch.get((fid, cell), '')
            un = '1' if (fid, cell.split(':')[0]) in dead else ''
            rows.append(f'{fid}\t{cell}\t{t}\t{sw}\t{un}')
            tot['cells'] += 1
            tot['missing'] += cell not in sp
            tot['switch'] += bool(sw)
            tot['unreachable'] += bool(un)
            if t:
                tot['quote'] += 1
                tot['named'] += t != '?'
        with io.open(os.path.join(OUT, name + '.tsv'), 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(rows) + '\n')
        tot['chunks'] += 1
    report_unknown(unknown)
    print(f"wrote {tot['chunks']} files to read/speakers/: {tot['cells']} cells, {tot['quote']} quote cells, "
          f"{tot['named']} with a speaker by colour, {tot['missing']} cells with no lns cell (UI), "
          f"{tot['switch']} narrator-switch cells, {tot['unreachable']} unreachable cells")


if __name__ == '__main__':
    main()
