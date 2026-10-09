"""SUPERSEDED 2026-09-25 by tools/db/merge_log.py, which does the same markdown appends, loads the rows
into notes/db/project.sqlite, refuses to re-append a row that was edited in the master after an earlier
merge, and has a `check` command. See tools/db/README.md.

Merge one agent log (notes/_tmp/tl-log-<tag>.md, rows `KIND | ...`) into the master logs, append-only:
DECISION -> notes/DECISIONS.md, TN -> notes/NOTES-TL.md, QUERY -> notes/QUERIES.md (8 pipe fields, same shape as the
read-through rows), RESOLVED -> sets status=resolved on the existing QUERIES row, PROGRESS -> notes/PROGRESS.md
"## Translation" table. Idempotent: a row already present (exact text) is skipped. Usage:
    uv run tools/merge_log.py A
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def append_unique(path, rows):
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    have = set(text.split('\n'))
    new = [r for r in rows if r not in have]
    if new:
        if text and not text.endswith('\n'):
            text += '\n'
        path.write_text(text + '\n'.join(new) + '\n', encoding='utf-8')
    return len(new)


def main(tag):
    log = ROOT / 'notes' / '_tmp' / f'tl-log-{tag}.md'
    rows = [l.rstrip() for l in log.read_text(encoding='utf-8').splitlines() if l.strip()]
    dec, tn, q, res, prog = [], [], [], [], []
    for r in rows:
        kind, _, rest = r.partition(' | ')
        kind = kind.strip()
        if kind == 'DECISION':
            dec.append(rest.strip())
        elif kind == 'TN':
            tn.append(rest.strip())
        elif kind == 'QUERY':
            q.append(rest.strip())          # "Q1160 | id:file:line | question | why | shipped | severity | status"
        elif kind == 'RESOLVED':
            res.append(rest.strip())        # "Q0042 | id:file:line | how"
        elif kind == 'PROGRESS':
            prog.append('| ' + rest.strip().replace(' | ', ' | ') + ' |')
    n_dec = append_unique(ROOT / 'notes' / 'DECISIONS.md', dec)
    n_tn = append_unique(ROOT / 'notes' / 'NOTES-TL.md', tn)
    n_q = append_unique(ROOT / 'notes' / 'QUERIES.md', q)
    qpath = ROOT / 'notes' / 'QUERIES.md'
    qtext = qpath.read_text(encoding='utf-8')
    n_res = 0
    for r in res:
        qid, _, how = r.partition(' | ')
        qid = qid.strip()
        pat = re.compile(r'^(' + re.escape(qid) + r' \| .*?) \| (tl-open|owner|open|provisional) \|\s*$', re.M)
        qtext, k = pat.subn(lambda m: m.group(1) + ' | resolved | resolved_by=' + how.strip().replace('\n', ' ') + ' |', qtext, count=1)
        n_res += k
    qpath.write_text(qtext, encoding='utf-8')
    n_prog = append_unique(ROOT / 'notes' / 'PROGRESS.md', prog)
    print(f'{tag}: decisions +{n_dec}, TN +{n_tn}, queries +{n_q}, resolved {n_res}, progress rows +{n_prog}')


if __name__ == '__main__':
    main(sys.argv[1])
