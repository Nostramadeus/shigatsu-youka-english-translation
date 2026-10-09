"""Rewrap the English 内容 cells of tsv-en/注意.tsv (boot prompts, consent screens) to the width they are drawn at.

    uv run --no-project --python 3.12 --with pillow python tools/rewrap_notice.py            # dry run: prints lines
    uv run --no-project --python 3.12 --with pillow python tools/rewrap_notice.py --apply    # rewrites tsv-en/注意.tsv

WHY (FIX1, 2026-09-26, mouse run findings F1-F4): each cell is drawn by 000000F2 as a centred Caption in ＭＳ Ｐ明朝
25 px, one screen line per literal "\\n", with NO engine wrapping. The earlier rewrap (<= 80 characters) counted
characters, not pixels, and left one-word lines ("so", "The") and cells too tall for the consent band (9 lines
running into the buttons).

RULE: the cell's words are kept exactly (never shortened, O-11). Each sentence starts a new line (as the JP puts
one sentence per line); a sentence wider than MAX_W is split into the FEWEST lines, then balanced (the widths
evened out, so no one-word tail). A fixed-label line such as "E-mail address: ..." is one sentence. MAX_W = 825 px
= the author's widest JP line (row 11, 33 full-width characters at 25 px). Widths are measured with the real face
(C:/Windows/Fonts/msmincho.ttc, face index 1 = ＭＳ Ｐ明朝) at 25 px; calibration: shot 032's line "Every care has
been taken to leave no defects, but if you should find" is 800 logical px on screen.
Exit 1 if any consent cell (rows 4-14) would need more than MAX_LINES lines.
"""
import re
import sys
from pathlib import Path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
TSV = ROOT / 'tsv-en' / '注意.tsv'
FONT = ImageFont.truetype('C:/Windows/Fonts/msmincho.ttc', 25, index=1)
MAX_W = 825
MAX_LINES = 7          # consent band: 8 lines fit above the buttons (29 px pitch from y=192); keep one spare
CONSENT_ROWS = range(4, 15)
SENT = re.compile(r'(?<=[.!?)”])\s+(?=[A-Z(“‘0-9])')


SCALE = 800 / 723       # in-game Latin is 10.7% wider than PIL draws this face at 25 px (calibration line below)


def w(s):
    return FONT.getlength(s) * SCALE


def wrap(sentence):
    words = sentence.split(' ')
    # fewest lines: greedy
    lines, cur = [], ''
    for word in words:
        t = word if not cur else cur + ' ' + word
        if w(t) <= MAX_W or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    n = len(lines)
    if n == 1:
        return lines
    # balance: smallest maximum width over all splits into n lines (dynamic programming over word positions)
    import functools
    k = len(words)

    @functools.lru_cache(None)
    def best(i, m):
        # split words[i:] into m lines; return (max width, tuple of lines)
        if m == 1:
            s = ' '.join(words[i:])
            return (w(s), (s,))
        res = None
        for j in range(i + 1, k - m + 2):
            head = ' '.join(words[i:j])
            hw = w(head)
            if hw > MAX_W:
                break
            tw, tl = best(j, m - 1)
            cand = (max(hw, tw), (head,) + tl)
            if res is None or cand[0] < res[0]:
                res = cand
        return res if res else (1e9, ())
    return list(best(0, n)[1])


def rewrap(cell):
    text = cell.replace('\\n', ' ')
    text = re.sub(r' +', ' ', text).strip()
    text = re.sub(r' (?=(E-mail address:|X account:))', '\n', text)   # label lines stay their own line
    out = []
    for sent in [s for part in text.split('\n') for s in SENT.split(part)]:
        out.extend(wrap(sent))
    return out


def main():
    apply = '--apply' in sys.argv
    raw = TSV.read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    rows = raw.split(nl)
    bad = 0
    for r in range(1, len(rows)):
        cols = rows[r].split('\t')
        if len(cols) < 3 or not cols[2].strip():
            continue
        no = int(cols[0])
        lines = rewrap(cols[2])
        wid = max(w(x) for x in lines)
        flag = ''
        if no in CONSENT_ROWS and len(lines) > MAX_LINES:
            flag = '  <-- TOO MANY LINES'
            bad += 1
        print('row %d: %d lines, widest %.0f px%s' % (no, len(lines), wid, flag))
        for x in lines:
            print('    | %s' % x)
        cols[2] = '\\n'.join(lines)
        rows[r] = '\t'.join(cols)
    if apply and not bad:
        TSV.write_bytes(nl.join(rows).encode('utf-8'))
        print('wrote', TSV)
    return 1 if bad else 0


if __name__ == '__main__':
    print('calibration: shot-032 line = %.0f px (screen 800)' %
          FONT.getlength('Every care has been taken to leave no defects, but if you should find'))
    sys.exit(main())
