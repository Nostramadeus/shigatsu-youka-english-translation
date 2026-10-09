"""Shared JP -> EN converter for the date columns (STYLE CALENDAR rule).

    from calendar_en import convert, normalize, LEAVE
    convert('祀耀800年　五月　五日 23:59', compact=True)  -> 'Shiyo 800-05-05 23:59'   <- THE SHIPPED FORM
    convert('1560年四月三十日 23:05', compact=True)       -> '1560-04-30 23:05'
    convert('Now', compact=True)                         -> 'Now'   (unchanged, see LEAVE)

THE SHIPPED FORM IS COMPACT, and that is forced, not a taste call (measured 2026-09-26,
notes/_tmp/datecheck.py):
- the long form `Shiyo 800, May 5, 23:59` puts a COMMA into **732** cells. `閲覧年月日` and
  `入手年月日` are projected into `ノベルシステム\ナビデータ.txt`, which the engine splits on `","`
  with no quoting - one comma would shift every following column of that row and break the navigator
  map exactly the way the blocker in §1-4 did;
- the long form is also WIDER than the Japanese original at every caption size in both faces
  (worst `祀耀735年二月一日` -> `Shiyo 735, February 1`: +21 px at the size-25 confirm panel,
  +100 px at 000015E3's size-50 caption). The compact form is never wider at any size in either face
  (max EN 176 px vs max JP 192 px at size 15 proportional).
Injectivity checked on all five columns: **0 collisions**, so the adjacent-row comparisons
(`0000001C` 4897 / 6221 `[4] != [4]`, `000015E3` `== 前の時間`) keep their Japanese behaviour.

Columns it is used on: シナリオデータベース 閲覧年月日 + 入手年月日, リファレンスデータベース 閲覧年月日,
事典出来事 年月日, 裏ルート 閲覧年月日 (508 distinct values, 755 cells as of 2026-09-26).

RULES
- era `祀耀` -> `Shiyo `; no era -> no prefix (those years are Gregorian). Years stay digits, no
  calendar conversion. Month name spelled out, day in digits, time kept as written.
- Kanji numerals: if the run contains 十 it is read traditionally (十=10, 二十=20, 十二=12, 二十四=24);
  otherwise it is read positionally, the way this game's tables write it (一二=12, 三〇=30, 五=5).
  Both spellings occur in the tables (`三〇日` and `三十日`), hence the two rules.
- Full-width padding spaces around the month/day are dropped (they existed to make 1-9 align with
  一〇; English month names are not equal width, so the device cannot survive - same ruling as the
  0000001C month literals, tl-log-UI DECISION "0000001C:month literals").

CONSERVATIVE BY DESIGN
`convert` returns the input UNCHANGED unless it matches the strict grammar. Everything in `LEAVE`,
every value that is only full-width spaces, and every irregular form (ranges `～`, `頃`, `元年`,
`前1年`, `#VALUE!`, the mojibake cell) is left byte-identical: an untranslated cell is Japanese text
on screen, which is the status quo, whereas a wrong guess is a data error. `unconverted()` lists what
was skipped so the count is visible in the build log.

MUST NOT BE TRANSLATED (verified 2026-09-26, notes/NAVIGATOR-BUG-AUDIT.md §8)
- `Now` and `Unknown Date`: compared as literals - `0000001C` indices 1285, 1344, 1410
  `If DBGetStr("閲覧年月日") == "Now"`. They are already English in the Japanese tables.
- a cell of one, two or three full-width spaces: the grid-row blank sentinels compared at
  `0000001C` 4901 / 6225 `二元配列[n][4] == "　" | "　　" | "　　　"`.
Both are in `LEAVE` / handled before the grammar runs.
"""
import re

LEAVE = {'', '0', 'Now', 'Unknown Date', '#VALUE!'}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']
DIGIT = {'〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
         '六': 6, '七': 7, '八': 8, '九': 9}

# <era?><year>年 <pad?><month>月 <pad?><day>日 <pad?><time?>
GRAMMAR = re.compile(
    r'^(祀耀)?(\d+)年[　 ]*([〇一二三四五六七八九十]+)月[　 ]*([〇一二三四五六七八九十]+)日'
    r'(?:[　 ]+(\d{1,2}[:：]\d{2}))?$')

_skipped = []


def kanji_int(s):
    """Kanji numeral -> int, or None if unreadable. 十-form is traditional, otherwise positional."""
    if '十' in s:
        n, cur, seen = 0, None, False
        for ch in s:
            if ch == '十':
                n += (cur if cur is not None else 1) * 10
                cur, seen = None, True
            elif ch in DIGIT:
                cur, seen = DIGIT[ch], True
            else:
                return None
        return (n + (cur or 0)) if seen else None
    v = 0
    for ch in s:
        if ch not in DIGIT:
            return None
        v = v * 10 + DIGIT[ch]
    return v


def convert(cell, compact=False):
    """JP date cell -> English. Returns `cell` unchanged when it is not a plain single date."""
    if cell in LEAVE or not cell.strip('　 '):
        return cell
    m = GRAMMAR.match(cell)
    if not m:
        _skipped.append(cell)
        return cell
    era, year, mo, day, time = m.groups()
    mi, di = kanji_int(mo), kanji_int(day)
    if not mi or not di or mi > 12 or di > 31:
        _skipped.append(cell)
        return cell
    head = ('Shiyo ' if era else '') + year
    time = (time or '').replace('：', ':')
    if compact:
        out = '%s-%02d-%02d' % (head, mi, di)
        return (out + ' ' + time) if time else out
    out = '%s, %s %d' % (head, MONTHS[mi - 1], di)
    return (out + ', ' + time) if time else out





LONG_EN = re.compile(r'^(Shiyo )?(\d+), ([A-Z][a-z]+) (\d{1,2})(?: (\d{1,2}:\d{2}))?$')


def normalize(cell):
    """Fold an already-English LONG date ("Shiyo 800, May 6 13:00") into the compact form.

    The tables lane had already translated part of リファレンスデータベース 閲覧年月日 (58 cells) and
    事典出来事 年月日 (10) in that form before the column-wide pass. Those cells contain a COMMA, which
    is illegal in the two comma-separated files (`ナビデータ.txt`, `リファレンス概要.txt`) and makes one
    column carry two formats. Range / circa forms ("Shiyo 790～797, April 8") are left alone: they are
    not a single date and the compact form cannot express them.
    """
    m = LONG_EN.match(cell)
    if not m:
        return cell
    era, year, month, day, time = m.groups()
    if month not in MONTHS:
        return cell
    out = '%s%s-%02d-%02d' % (era or '', year, MONTHS.index(month) + 1, int(day))
    return (out + ' ' + time) if time else out


def unconverted():
    """Distinct cells `convert` refused, in first-seen order."""
    out, seen = [], set()
    for c in _skipped:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def reset():
    del _skipped[:]
