"""Apply IMGCHECK3-*.tsv grades to review/images/UNCHECKED-IMAGES.md.

Each TSV line: <preview>\t<row key>\t<grade>\t<note>. Row key = path suffix such as rrr34/7.png or rr65.png.
ok / FIX rows are ticked `- [x]` and get ` | IMGCHECK3: ok` or ` | IMGCHECK3 FIX: <note>` appended.
'not viewed IMGCHECK3' rows stay `- [ ]` and get ` | not viewed IMGCHECK3` appended. Keys with `-` are skipped.
Usage: python tools/images/imgcheck3_apply.py [--dry] [--tag=IMGCHECK4] A B C D
"""
import sys, glob, io
ROOT = 'F:/Projects/shigatsu-youka-en/'
LEDGER = ROOT + 'review/images/UNCHECKED-IMAGES.md'
dry = '--dry' in sys.argv
TAG = next((a.split('=',1)[1] for a in sys.argv[1:] if a.startswith('--tag=')), 'IMGCHECK3')
letters = [a for a in sys.argv[1:] if not a.startswith('--')]
grades = {}
for L in letters:
    for line in io.open(ROOT + f'review/images/{TAG}-{L}.tsv', encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        parts = line.split('\t')
        while len(parts) < 4:
            parts.append('')
        preview, key, grade, note = parts[:4]
        key = key.strip()
        if key in ('-', '', '(no row)'):
            continue
        grade = grade.strip()
        # a FIX on any frame beats an ok for the same key (two previews can share one row)
        prev = grades.get(key)
        if prev and prev[0] == 'FIX' and grade != 'FIX':
            continue
        grades[key] = (grade, note.strip(), L)
lines = io.open(LEDGER, encoding='utf-8').read().split('\n')
hit = set()
out = []
for ln in lines:
    new = ln
    if ln.startswith('- [ ]') or ln.startswith('- [x]'):
        path = ln[6:].split(' | ')[0].strip()
        for key, (grade, note, L) in grades.items():
            if path.endswith('/' + key) or path.endswith(key):
                hit.add(key)
                if grade == 'ok':
                    new = '- [x]' + ln[5:] + f' | {TAG}: ok'
                elif grade == 'FIX':
                    new = '- [x]' + ln[5:] + f' | {TAG} FIX: ' + note
                else:
                    new = ln + f' | not viewed {TAG}'
                break
    out.append(new)
missing = [k for k in grades if k not in hit]
print('graded keys', len(grades), 'applied', len(hit), 'unmatched', missing)
counts = {}
for k in hit:
    g = grades[k][0]
    counts[g] = counts.get(g, 0) + 1
print(counts)
if not dry:
    io.open(LEDGER, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    print('ledger written')
