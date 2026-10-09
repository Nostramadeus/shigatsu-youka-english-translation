"""pause_space.py - add the English space at a {PAUSE} cell boundary.

Japanese needs no space after 。 so a text box split by {PAUSE ""} into two cells reads fine;
English concatenates the two cells with nothing between them ("huh.Yeah"). This sweep finds a text
line followed (after PAUSE lines only) by another text line, where the first ends with sentence
punctuation or a closing quote and the second begins with a letter, digit or opening quote, and adds
one ASCII space at the end of the first cell's text (inside its last </STYLE> when the line ends with one).

    uv run --no-project --python 3.12 python tools/pause_space.py            # dry run, prints candidates
    uv run --no-project --python 3.12 python tools/pause_space.py --apply    # edits <tree>/*.lns
    SY_EN_DIR=lns-en-55 ...                                                   # tree (default lns-en)
    ... --only 0000095B 00000972                                              # restrict to these ids

v2 (Fable, 2026-10-01, found by reviewer P7R2): v1 only saw cells wrapped in <STYLE ...> and only looked at lns-en/.
A BARE text line (no STYLE tag: default-colour narration) was never checked, in either tree, so uncoloured cells
could still join as "huh.Yeah". v2 treats every non-command line as a text line and reads SY_EN_DIR. A cell whose
visible text is only dots / ellipsis ("......") is left alone: those are the silence device, not a sentence end;
so is a name or word stammered over two cells ("Na... | tsu..."): both fragments of 3 letters or fewer, the second lowercase.
v1 kept at tools/_retired/pause_space.v1.py.
v3 (Fable, 2026-10-08, found in autopilot run 1): on a CR CR LF file the bare-text branch appended the space AFTER the
line's trailing \r, so the space landed on its own line (54 cells rejoined by hand in 00000F24, 7 in 00000FB7). Fixed.
"""
import glob
import io
import os
import re
import sys

APPLY = '--apply' in sys.argv
ONLY = set(sys.argv[sys.argv.index('--only') + 1:]) if '--only' in sys.argv else None
TREE = os.environ.get('SY_EN_DIR', 'lns-en')
PAUSE_RE = re.compile(r'^\{PAUSE [^}]*\}\s*$')
END_PUNCT = tuple('.!?,;:…"\'”’)')
START_OK_CH = re.compile(r'^[A-Za-z0-9"“(\[]')
DOTS_ONLY = re.compile(r'^[.…\s"“”]+$')
FRAG = re.compile(r'[^A-Za-z]')
TAG = re.compile(r'<[^>]+>')


def is_text(line):
    t = line.rstrip('\r\n')
    return bool(t) and not t.startswith(('{', ';')) and TAG.sub('', t).strip() != ''


def visible_tail(line):
    return TAG.sub('', line).rstrip('\r\n')


total = 0
files = 0
for path in sorted(glob.glob(f'{TREE}/*.lns')):
    if ONLY is not None and os.path.basename(path)[:8] not in ONLY:
        continue
    raw = io.open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.split(nl)
    changed = 0
    i = 0
    while i < len(lines):
        if is_text(lines[i]) and '<PG>' not in lines[i] and '<BR>' not in lines[i]:
            j = i + 1
            while j < len(lines) and PAUSE_RE.match(lines[j]):
                j += 1
            if j > i + 1 and j < len(lines) and is_text(lines[j]) and START_OK_CH.match(TAG.sub('', lines[j])):
                tail = visible_tail(lines[i])
                nxt = TAG.sub('', lines[j])
                split_word = len(FRAG.sub('', tail)) <= 3 and len(FRAG.sub('', nxt.split('.')[0].split(' ')[0])) <= 3 and nxt[:1].islower()
                if tail and tail.endswith(END_PUNCT) and not tail.endswith(' ') and not DOTS_ONLY.match(tail) and not split_word:
                    if lines[i].rstrip().endswith('</STYLE>'):
                        k = lines[i].rfind('</STYLE>')
                        lines[i] = lines[i][:k] + ' ' + lines[i][k:]
                    else:
                        body = lines[i].rstrip('\r')  # CR CR LF files keep a trailing \r per line: the space goes before it
                        lines[i] = body + ' ' + lines[i][len(body):]
                    if not APPLY:
                        print(path, i + 1, '|', tail[-30:], '||', TAG.sub('', lines[j])[:30])
                    changed += 1
        i += 1
    if changed:
        files += 1
        total += changed
        if APPLY:
            io.open(path, 'w', encoding='utf-8', newline='').write(nl.join(lines))
print(('APPLIED' if APPLY else 'DRY RUN'), 'tree:', TREE, 'cells:', total, 'files:', files)
