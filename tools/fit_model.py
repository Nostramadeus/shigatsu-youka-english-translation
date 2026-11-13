"""FIT MODEL 2 reference implementation (measurement side; the checker spec in notes/FIT-MODEL-2.md mirrors it).

advance(ch) = max(GetCharWidth32W(ch), GGO_GRAY8 origin.x + blackBoxX) at lfHeight = FONTHEIGHT, face = PR_FONTNAME, weight 400
              + K,  K = 1 + SHADOW + 2 * BORDER        (MesNew only; Caption K = 0)
pitch       = FONTHEIGHT + LINESPACE + SHADOW + 2 * BORDER
wrap(text, W, reserve): greedy; tokens split at ASCII space; a token is placed when x + width(token) <= W - reserve;
              the space before a token that starts a new line is dropped; a token wider than the line is cut per glyph.
"""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from fit_gdi import Font, GGO_GRAY8_BITMAP

_fonts = {}


def font(face, h, bold=False):
    key = (face, h, bold)
    if key not in _fonts:
        _fonts[key] = Font(face, h, weight=700 if bold else 400)
    return _fonts[key]


def K(shadow=0, border=0):
    return 1 + shadow + 2 * border


def pitch(h, linespace, shadow=0, border=0):
    return h + linespace + shadow + 2 * border


_cells = {}


def cell(c, f):
    """Glyph cell = max(GetCharWidth32W, glyph origin x + black box width from GetGlyphOutlineW GGO_GRAY8_BITMAP).
    Verified glyph by glyph on tools/harness/shots/fitaudit/004.png ('f' in MS PMincho 30: advance 8, cell 11)."""
    key = (id(f), c)
    if key not in _cells:
        a = f.adv(c)
        g = f.ggo(c, GGO_GRAY8_BITMAP)
        _cells[key] = max(a, g[2] + g[0]) if g else a
    return _cells[key]


def width(s, f, k):
    return sum(cell(c, f) + k for c in s)


def is_wide(c):
    return ord(c) >= 0x2E80 or c in '\u3000'


def tokens(par):
    """Break opportunities: after an ASCII space run; between two CJK glyphs; between CJK and Latin."""
    out = []
    cur = ''
    for c in par:
        if c == ' ':
            cur += c
            continue
        if cur and (cur.endswith(' ') or is_wide(c) or is_wide(cur.rstrip(' ')[-1:] or 'a')):
            out.append(cur)
            cur = ''
        cur += c
    if cur:
        out.append(cur)
    return out


def wrap(text, f, k, W, reserve=0, limit=None, rule='space'):
    """Returns the list of screen lines.
    rule 'space' (the engine, verified on fitaudit4/010.png P3 vs Q3): a token is placed only when the word AND the
    ASCII space(s) after it fit: x + width(word + spaces) <= W.
    rule 'word' (the first guess, kept for the scans): x + width(word) <= limit, limit = W - reserve."""
    lim = (W - reserve) if limit is None else limit
    lines = []
    for par in text.replace('\r\n', '\n').split('\n'):
        cur = ''
        x = 0
        for tok in tokens(par):
            body = tok.rstrip(' ')
            wb = width(tok if rule == 'space' else body, f, k)
            if cur and x + wb > lim:
                lines.append(cur.rstrip(' '))
                cur, x = '', 0
            while not cur and width(body, f, k) > lim and len(body) > 1:   # one token wider than the line
                n = len(body)
                while n > 1 and width(body[:n], f, k) > lim:
                    n -= 1
                lines.append(body[:n])
                tok = tok[n:]
                body = tok.rstrip(' ')
            cur += tok
            x += width(tok, f, k)
        lines.append(cur.rstrip(' '))
    return lines
