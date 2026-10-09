"""agent_pack.py - ONE input file per drafter/reviewer agent (Fable, 2026-10-01, cost cut for part 4+).

    PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/agent_pack.py --tag P4A --last 0000066B 000005C1 ...

Reads (already built by kb.py): notes/STYLE.md, notes/_tmp/core-<last>.md, notes/v2/_tmp/pack-<id>.md per id.
Writes notes/v2/_tmp/agentpack-<tag>.md = STYLE + CORE (D1/D3 cast entries filtered to the speakers present in
these files) + each packet WITHOUT its "Text-line view" section (the agent reads lns/ anyway).
Why: a drafter used to read STYLE + 84 KB core + 50-85 KB per packet in separate Read calls, and every later
turn re-sent all of it. One file, read once, ~40% smaller. Stdlib only.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CJK = re.compile(r'[぀-ヿ一-鿿]')


def speakers_of(pack_text):
    toks = set()
    for line in pack_text.split('\n'):
        if line.startswith('- speakers present:'):
            body = line.split(':', 1)[1]
            for t in re.split(r'[,、;=()（）/ ]+', body):
                t = t.strip()
                if len(t) >= 2 and CJK.search(t):
                    toks.add(t)
    return toks


def filter_core(core, toks):
    def keep(head):
        return any(t in head for t in toks)
    out = []
    for sec in re.split(r'(?m)^(?=## )', core):
        if sec.startswith('## D1.'):
            parts = re.split(r'(?m)^(?=### )', sec)
            kept = [parts[0]] + [p for p in parts[1:] if keep(p.split('\n', 1)[0])]
            out.append(''.join(kept))
        elif sec.startswith('## D3.'):
            parts = re.split(r'(?m)^(?=- \*\*)', sec)
            kept = [parts[0]] + [p for p in parts[1:] if keep(p.split('\n', 1)[0])]
            out.append(''.join(kept))
        else:
            out.append(sec)
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True)
    ap.add_argument('--last', required=True, help='last id of the files (the core digest fence)')
    ap.add_argument('--no-core', action='store_true',
                    help='omit PART 2 (the CORE digest): reviewer packs, cost lever decided 2026-10-01')
    ap.add_argument('ids', nargs='+')
    a = ap.parse_args()
    style = (ROOT / 'notes/STYLE.md').read_text(encoding='utf-8')
    core = (ROOT / f'notes/_tmp/core-{a.last}.md').read_text(encoding='utf-8')
    packs = {}
    for fid in a.ids:
        p = ROOT / f'notes/v2/_tmp/pack-{fid}.md'
        if not p.exists():
            sys.exit(f'missing {p}: run kb.py packet {fid} first')
        packs[fid] = p.read_text(encoding='utf-8')
    toks = set()
    for t in packs.values():
        toks |= speakers_of(t)
    core_f = filter_core(core, toks)
    parts = [f'# AGENT PACK {a.tag} - files in reading order: {" ".join(a.ids)}\n'
             f'# Built by tools/agent_pack.py. Read this file once, top to bottom. It replaces STYLE.md, the core digest '
             f'and the per-file packets. Do not Read those separately.\n\n',
             '# ===== PART 1: notes/STYLE.md (binding) =====\n\n', style, '\n\n']
    if a.no_core:
        parts.append('# ===== PART 2: (CORE digest omitted for this pack; the packets below carry the glossary rows, '
                     'cast sheets and relations for these files) =====\n\n')
    else:
        parts += [f'# ===== PART 2: CORE digest, fenced at {a.last}; cast entries limited to the speakers present =====\n\n',
                  core_f, '\n\n']
    seen = set()  # cross-packet dedupe of glossary / cast / relations lines (the same sheets repeat per file)
    DEDUPE = ('## GLOSSARY rows', '## CAST.md blocks', '## RELATIONS.tsv rows')
    for fid, text in packs.items():
        body = text.split('\n## Text-line view')[0]
        out_lines, dd = [], False
        for line in body.split('\n'):
            if line.startswith('## '):
                dd = line.startswith(DEDUPE)
            if dd and not line.startswith('## ') and line.strip():
                if line in seen:
                    continue
                seen.add(line)
            out_lines.append(line)
        body = '\n'.join(out_lines)
        parts.append(f'# ===== PART 3: PACKET {fid} (text-line view removed: read lns/{fid}-*.lns instead) =====\n\n')
        parts.append(body + '\n\n')
    out = ROOT / f'notes/v2/_tmp/agentpack-{a.tag}.md'
    data = ''.join(parts)
    out.write_text(data, encoding='utf-8')
    raw = len(style) + len(core) + sum(len(t) for t in packs.values())
    print(f'wrote {out.relative_to(ROOT)}: {len(data):,} bytes, {data.count(chr(10)):,} lines '
          f'(inputs were {raw:,} bytes; core {len(core):,} -> {len(core_f):,}; speakers: {", ".join(sorted(toks))})')


if __name__ == '__main__':
    main()
