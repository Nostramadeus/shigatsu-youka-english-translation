"""apply_patch.py - apply a reviewer's line patch file to the English tree in ONE process (Fable, 2026-10-01).

    PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/apply_patch.py <patchfile> [--dir lns-en-55]

Patch rows (tab-separated), one per changed line:
    <lns file name>\t<line number, 1-based, as in lns/<name>>\t<the complete new English line, tags included>
Blank rows and rows starting with # are skipped. The tag/command sequence of the new line is compared with the
JP line (lns/<name>); a mismatch is reported and NOT applied. Why this exists: a reviewer that fixes 100 lines
with 100 Edit calls re-sends its whole context 100 times. One patch file + one apply = one turn. Stdlib only.
"""
import argparse
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r'<[^>]*>|\{[^}]*\}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('patch')
    ap.add_argument('--dir', default='lns-en-55')
    a = ap.parse_args()
    rows = {}
    bad = 0
    for n, row in enumerate(Path(a.patch).read_text(encoding='utf-8').split('\n'), 1):
        if not row.strip() or row.startswith('#'):
            continue
        f = row.split('\t', 2)
        if len(f) != 3 or not f[1].strip().isdigit():
            print(f'row {n}: malformed (need name<TAB>lineno<TAB>text)'); bad += 1; continue
        rows.setdefault(f[0].strip(), []).append((int(f[1]), f[2], n))
    applied = 0
    for name, items in rows.items():
        jp_p, en_p = ROOT / 'lns' / name, ROOT / a.dir / name
        if not jp_p.exists() or not en_p.exists():
            print(f'{name}: missing in lns/ or {a.dir}/'); bad += len(items); continue
        jp = io.open(jp_p, encoding='utf-8', newline='').read().replace('\r', '').split('\n')
        raw = io.open(en_p, encoding='utf-8', newline='').read()
        eol = '\r\r\n' if '\r\r\n' in raw else ('\r\n' if '\r\n' in raw else '\n')  # keep the file's own line ending (QMILER-02, 2026-10-02)
        en = raw.replace('\r', '').split('\n')
        k = 0
        for lineno, text, n in items:
            i = lineno - 1
            if i < 0 or i >= len(jp):
                print(f'{name}:{lineno}: no such line (row {n})'); bad += 1; continue
            if TAG.findall(jp[i]) != TAG.findall(text):
                print(f'{name}:{lineno}: TAG MISMATCH, not applied (row {n})\n   JP {TAG.findall(jp[i])}\n   EN {TAG.findall(text)}')
                bad += 1; continue
            en[i] = text; k += 1
        io.open(en_p, 'w', encoding='utf-8', newline='').write(eol.join(en))
        print(f'{name}: applied {k} of {len(items)}')
        applied += k
    print(f'applied {applied}, rejected {bad}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
