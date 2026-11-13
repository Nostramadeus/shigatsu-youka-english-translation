"""Build step for メッセージボックス作成.lsb (run by tools/apply_labels.sh after copying orig/; IN.lsb OUT.lsb; idempotent).
Stage 1 (the file's recipe since 2026-09-25, tools/harness/set_msgbox_prop.py ... PR_FONTNAME "ＭＳ Ｐ明朝"):
    every MesNew gets the face ＭＳ Ｐ明朝 (proportional Latin).
Stage 2 (lane W 2026-11-14, work/layout/W-FACTS.md P3): the イベント用 box (idx 113, BoxNew メッセージボックス土台) is
    800 x 141 at y 389 while the chatter screen is open (its background object 雑談背景 exists), else 630 x 100 at y 430:
    PR_WIDTH 630 + 170 * E, PR_HEIGHT 100 + 41 * E, PR_TOP 430 - 41 * E, E = Exists("雑談背景").
    The text (idx 114) follows by its own expressions (box width - 40, box height - 20): 760 x 121 = 5 lines."""
import sys
from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeData, OpeDataType as T, Param, ParamType as P, OpeFuncType as F

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
n = 0
for cmd in s.commands:
    if cmd.type.name != 'MesNew':
        continue
    op = cmd['PR_FONTNAME'].entries[0].operands[-1]
    op.value = 'ＭＳ Ｐ明朝'
    n += 1
print('fix-メッセージボックス作成: PR_FONTNAME ＭＳ Ｐ明朝 on %d MesNew' % n)

c = s.commands[113]
assert c.type.name == 'BoxNew' and str(c['Name']).strip('"') == 'メッセージボックス土台', 'idx 113 shape'
assert 'イベント用' in str(s.commands[108]['Calc']), 'idx 108 branch'


def expr(base, k, op):
    e = [OpeData(type=T.To, name='____1', operands=[Param('雑談背景', P.Str)]),
         OpeData(type=T.Func, name='____2', operands=[Param('____1', P.Var)], func=F.Exists),
         OpeData(type=T.Mul, name='____3', operands=[Param(k, P.Int), Param('____2', P.Var)]),
         OpeData(type=op, name='____4', operands=[Param(base, P.Int), Param('____3', P.Var)]),
         OpeData(type=T.To, name='____arg', operands=[Param('____4', P.Var)])]
    return e


done = []
for key, base, k, op in (('PR_WIDTH', 630, 170, T.Plus), ('PR_HEIGHT', 100, 41, T.Plus), ('PR_TOP', 430, 41, T.Minus)):
    lp = c[key]
    e = lp.entries
    if len(e) == 1 and e[0].operands[0].type == P.Int and e[0].operands[0].value == base:
        lp.entries = expr(base, k, op)
        done.append('%s %d -> expr' % (key, base))
    else:
        assert 'Exists' in str(lp), '%s unexpected: %s' % (key, lp)
        done.append('%s already' % key)
open(dst, 'wb').write(s.to_lsb())
print('fix-メッセージボックス作成 W: ' + '; '.join(done))
