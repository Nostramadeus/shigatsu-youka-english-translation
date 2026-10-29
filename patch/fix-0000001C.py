"""Structural fix for work/0000001C.lsb, run by tools/compile_en.sh after the label and property maps
(FIX1, 2026-09-26, mouse run finding F7).

    uv run --no-project --with pylivemaker python patch/fix-0000001C.py IN.lsb OUT.lsb

F7: the navigator node's hover card (テキストウィンドウ) is sized at idx 140-144 as
    w = 120 + width(title);  if width(title) < width(date): w = 120 + width(date)
    if width(date) < width(person block): w = 120 + width(person block)
The last test forgets the title, so a title wider than the person block is cut at the card edge
("Meicho Arc  Dream Racin"). Japanese titles were never the widest line, English ones are. Fix: idx 143
becomes  width(date) < width(person) & width(title) < width(person)  so the card takes the widest of the
three lines. Nothing else changes. The script checks the original expression first and refuses to write if it
does not match (a re-extracted or already-fixed file), except that an already-fixed file is accepted as is.
"""
import copy
import sys
from livemaker.lsb import LMScript

IDX = 143
src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
cmd = s.commands[IDX]
ents = cmd['Calc'].entries


def sig(e):
    return (int(e.type), e.name, [getattr(o, 'value', None) for o in e.operands])


orig = [(1, '____0', ['シナリオ日時']), (1, '____1', ['シナリオ人物']), (11, '____2', ['____1', 5]),
        (11, '____3', ['____0', 5]), (14, '____4', ['____3', '____2']), (1, '____arg', ['____4'])]
now = [sig(e) for e in ents]
if len(now) == 10 and now[5][2] == ['シナリオ名前']:
    print('fix-0000001C: idx %d already fixed' % IDX)
elif now != orig:
    sys.exit('fix-0000001C: idx %d is not the expected expression: %r' % (IDX, now))
else:
    to_name, getp, less, arg = ents[0], ents[2], ents[4], ents[5]
    e5 = copy.deepcopy(to_name); e5.name = '____5'; e5.operands[0].value = 'シナリオ名前'
    e6 = copy.deepcopy(getp); e6.name = '____6'; e6.operands[0].value = '____5'
    e7 = copy.deepcopy(less); e7.name = '____7'
    e7.operands[0].value = '____6'; e7.operands[1].value = '____2'
    # the And op: copy the one idx 145 uses (type 8), rename and repoint it
    and_op = next(e for e in s.commands[145]['Calc'].entries if int(e.type) == 8)
    e8 = copy.deepcopy(and_op); e8.name = '____8'
    e8.operands[0].value = '____4'; e8.operands[1].value = '____7'
    new_arg = copy.deepcopy(arg); new_arg.operands[0].value = '____8'
    cmd['Calc'].entries = ents[:5] + [e5, e6, e7, e8, new_arg]
    print('fix-0000001C: idx %d now %s' % (IDX, cmd))
open(dst, 'wb').write(s.to_lsb())


# ---- F9 / F7 part 2 (FIX1, same day): the length-bar scales, now that 文字数1/2 are English totals ----
# Bars were scaled to 10,000 characters (x * 100 / 1000000) and their alpha to 12,000; English totals run
# 3,200-18,000, so most bars would clamp. Scale x2.5: 1000000 -> 2500000, 12000 -> 30000 (ticks every 125 px
# now mean 6,250 characters). And the card's minimum width 360 (idx 145, which the author applied to one arc
# only) now applies to every card, so the 240 px tick ruler at x = 105 always fits inside it.
from livemaker.lsb.core import LiveParser  # noqa: E402

s2 = LMScript.from_file(dst)


def swap_int(cmd_idx, old, new):
    c = s2.commands[cmd_idx]
    hits = []
    for k in c.keys():
        v = c[k]
        if isinstance(v, LiveParser):
            for e in v.entries:
                for o in e.operands:
                    if getattr(o, 'value', None) in (old, new) and type(getattr(o, 'value', None)) is int:
                        hits.append(o)
    if len(hits) != 1:
        sys.exit('fix-0000001C: idx %d has %d candidates for %d' % (cmd_idx, len(hits), old))
    hits[0].value = new


for i in (129, 131, 133, 136, 307, 309, 310, 312, 313, 315, 316):  # 1327 etc.: guarded block below
    swap_int(i, 1000000, 2500000)
for i in (138, 318):
    swap_int(i, 12000, 30000)

# ---- Counter repair 2026-10-29 (lane A, work/feedback-repair-20261029/COUNTERS-PLAN.md D7): the remaining bars on
# the old 10,000 / 12,000 scales. Every scenario 文字数1 and every hidden-route 文字数1 (tsv-en/裏ルート.tsv) is an
# English total now, so the same x2.5 applies to: the unlock-notice bars idx 1327 (active table 裏ルート), 1384 and
# 1489 (ナビデータ), width = 500 * 100 / (K / Int(DBGetStr("文字数1"))); and the second copy of the selection bar,
# idx 6040-6049 (same expressions as idx 307-316) and its alpha idx 6051 (= idx 318). Each site must match its
# original expression exactly, with the constant either the original or the fixed value, or the script refuses.
K = 'K'
BAR_DB = [(1, '____0', ['文字数1']), (11, '____1', ['____0']), (11, '____2', ['____1']), (5, '____4', [K, '____2']),
          (4, '____6', [500, 100]), (5, '____7', ['____6', '____4']), (1, '____arg', ['____7'])]
BAR2 = [(11, '____0', ['ナビ文字数2', 2]), (3, '____4', ['ナビ文字数', '____0']), (5, '____6', [K, '____4']),
        (4, '____8', [500, 100]), (5, '____9', ['____8', '____6']), (11, '____1', ['____9']),
        (1, '選択文字数バー2定数', ['____1'])]
BASE = [(5, '____1', [K, 'ナビ文字数']), (4, '____3', [500, 100]), (5, '____4', ['____3', '____1'])]
BASE2 = [(11, '____0', ['ナビ文字数2', 2]), (5, '____2', [K, '____0']), (4, '____4', [500, 100]),
         (5, '____5', ['____4', '____2'])]
ALPHA = [(4, '____0', [255, 'ナビ文字数']), (5, '____1', ['____0', K]), (1, '____arg', ['____1'])]
BAR_OBJ, ALPHA_OBJ = ('"選択文字数バー"', '5'), ('"選択文字数バーアルファ"', '11')
GUARDED = [  # (idx, command, property, expression with K for the constant, (ObjName, ObjProp) or None, old, new)
    (1327, 'PropMotion', 'Value', BAR_DB, BAR_OBJ, 1000000, 2500000),
    (1384, 'PropMotion', 'Value', BAR_DB, BAR_OBJ, 1000000, 2500000),
    (1489, 'PropMotion', 'Value', BAR_DB, BAR_OBJ, 1000000, 2500000),
    (6040, 'Calc', 'Calc', BAR2, None, 1000000, 2500000),
    (6042, 'Calc', 'Calc', BASE + [(1, '選択文字数バー基本長さ', ['____4'])], None, 1000000, 2500000),
    (6043, 'PropMotion', 'Value', BASE + [(1, '____arg', ['____4'])], BAR_OBJ, 1000000, 2500000),
    (6045, 'Calc', 'Calc', BASE2 + [(1, '選択文字数バー基本長さ', ['____5'])], None, 1000000, 2500000),
    (6046, 'PropMotion', 'Value', BASE2 + [(1, '____arg', ['____5'])], BAR_OBJ, 1000000, 2500000),
    (6048, 'Calc', 'Calc', BASE + [(1, '選択文字数バー基本長さ', ['____4'])], None, 1000000, 2500000),
    (6049, 'PropMotion', 'Value', BASE + [(1, '____arg', ['____4'])], BAR_OBJ, 1000000, 2500000),
    (6051, 'PropMotion', 'Value', ALPHA, ALPHA_OBJ, 12000, 30000),
]


def swap_guarded(idx, kind, key, shape, obj, old, new):
    c = s2.commands[idx]
    if c.type.name != kind:
        sys.exit('fix-0000001C: idx %d is %s, expected %s' % (idx, c.type.name, kind))
    if obj and (str(c['ObjName']), str(c['ObjProp'])) != obj:
        sys.exit('fix-0000001C: idx %d animates %s/%s, expected %s/%s'
                 % ((idx, str(c['ObjName']), str(c['ObjProp'])) + obj))
    ents = c[key].entries
    norm = [(s[0], s[1], [K if type(v) is int and v in (old, new) else v for v in s[2]]) for s in map(sig, ents)]
    consts = [o for e in ents for o in e.operands if type(getattr(o, 'value', None)) is int and o.value in (old, new)]
    if norm != shape or len(consts) != 1:
        sys.exit('fix-0000001C: idx %d is neither the original nor the fixed expression: %r' % (idx, norm))
    consts[0].value = new


for site in GUARDED:
    swap_guarded(*site)
e145 = s2.commands[145]['Calc'].entries
eq = [e for e in e145 if int(e.type) == 12]
if len(eq) != 1 or [o.value for o in eq[0].operands] not in (['現行編名', '____0'], ['____0', '____0']):
    sys.exit('fix-0000001C: idx 145 is not the expected expression')
eq[0].operands[0].value = '____0'          # "True Jusatsu Arc" == "True Jusatsu Arc": always true
print('fix-0000001C: bar scales x2.5 (incl. %d guarded sites), idx 145 min width for every card: %s'
      % (len(GUARDED), s2.commands[145]))
open(dst, 'wb').write(s2.to_lsb())
