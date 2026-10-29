"""Structural fix for work/00001CA0.lsb, run by tools/compile_en.sh after the label maps
(counter repair 2026-10-29, lane A; work/feedback-repair-20261029/COUNTERS-PLAN.md D7).

    uv run --no-project --with pylivemaker python patch/fix-00001CA0.py IN.lsb OUT.lsb

The True-Jusatsu unlock animation draws the 500 px selection bar for 連番 245/246/247/248/305/250 at idx
491/700/782/821/903/979: PropMotion "選択文字数バー伸びる" on "選択文字数バー" property 5 (width), Value
    500 * 100 / (1000000 / DBDirectGetStr("ナビデータ", "連番", "<連番>", 0, 0, "文字数1", ""))
- the same 10,000-character scale as 0000001C idx 1327/1384/1489. 文字数1 is an English total now, so the scale
gets the same x2.5 as patch/fix-0000001C.py: 1000000 -> 2500000. (These six rows are whole-arc totals: 53k-87k JP,
125k-206k EN, so the bar ran past 500 px in the original too; the swap keeps the original proportion.)
Each site must match its original expression exactly, with the constant either 1000000 or 2500000, or the script
refuses to write; an already-fixed file is accepted as is (idempotent).
Second stage, game follow-up r2 2026-10-30: the completion percent at idx 1109-1160 without 32-bit overflow (end of file).
"""
import sys
from livemaker.lsb import LMScript

K = 'K'
SITES = {491: '245', 700: '246', 782: '247', 821: '248', 903: '305', 979: '250'}
OLD, NEW = 1000000, 2500000


def sig(e):
    return (int(e.type), e.name, [getattr(o, 'value', None) for o in e.operands])


def shape(no):
    return [(1, '____0', ['ナビデータ']), (1, '____1', ['連番']), (1, '____2', [no]), (1, '____3', ['文字数1']),
            (1, '____4', ['']), (11, '____5', ['____0', '____1', '____2', 0, 0, '____3', '____4']),
            (5, '____7', [K, '____5']), (4, '____9', [500, 100]), (5, '____10', ['____9', '____7']),
            (1, '____arg', ['____10'])]


src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
if len(s.commands) != 1224:
    sys.exit('fix-00001CA0: %d commands, expected 1224 (not 00001CA0, or its structure changed)' % len(s.commands))
for idx, no in SITES.items():
    c = s.commands[idx]
    if c.type.name != 'PropMotion' or (str(c['ObjName']), str(c['ObjProp'])) != ('"選択文字数バー"', '5'):
        sys.exit('fix-00001CA0: idx %d is not the 選択文字数バー width motion' % idx)
    ents = c['Value'].entries
    norm = [(x[0], x[1], [K if type(v) is int and v in (OLD, NEW) else v for v in x[2]]) for x in map(sig, ents)]
    consts = [o for e in ents for o in e.operands if type(getattr(o, 'value', None)) is int and o.value in (OLD, NEW)]
    if norm != shape(no) or len(consts) != 1:
        sys.exit('fix-00001CA0: idx %d is neither the original nor the fixed expression: %r' % (idx, norm))
    consts[0].value = NEW
print('fix-00001CA0: unlock bar scale x2.5 at idx %s' % sorted(SITES))

# ---- Game follow-up r2 (2026-10-30): R1 "Overall completion" without a 32-bit overflow -----------------------------
# The True-Jusatsu unlock animation (label 00001CE9, idx 1109-1160) counts the completion from 進行率1 down to 進行率2 and
# rebuilds 全体進行率 from the globals 終了テキスト数 / 総テキスト数1 / 総テキスト数2 that 0000001C idx 3707-3722 summed
# (this script only reads them). Same X = 終了テキスト数 * 1000 / (総テキスト数n / 100) and the same exact overflow-free
# rewrite as patch/fix-0000001C.py (see patch/exprfix.py permille_fixed).
import os  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exprfix as xf  # noqa: E402

R1 = [  # (idx, command, original expression)
    (1109, 'Calc', xf.r1_rate(xf.T1, '進行率1')),
    (1112, 'Calc', xf.r1_rate(xf.T2, '進行率2')),
    (1139, 'If', xf.r1_mod_lt(xf.T1, 100)),
    (1141, 'Calc', xf.r1_frac_pad(xf.T2, '0', 10)),
    (1143, 'Calc', xf.r1_frac_pad(xf.T1, '0', 10)),
    (1144, 'Elseif', xf.r1_mod_lt(xf.T1, 10)),
    (1146, 'Calc', xf.r1_frac_pad(xf.T2, '00', 100)),
    (1148, 'Calc', xf.r1_frac_pad(xf.T1, '00', 100)),
    (1149, 'If', xf.r1_over(xf.T1, 14)),
    (1153, 'Calc', xf.r1_frac(xf.T2)),
    (1155, 'Calc', xf.r1_frac(xf.T1)),
    (1157, 'Calc', xf.r1_whole_pct(xf.T2)),
    (1159, 'Calc', xf.r1_whole_pct(xf.T1)),
    (1160, 'If', xf.r1_over(xf.T2, 15)),
]
done, already = xf.apply_sites(s, [(i, kind, None, shape, xf.permille_fixed(shape), None) for i, kind, shape in R1],
                               'fix-00001CA0')
print('fix-00001CA0: r2 completion percent without overflow at %d sites (%d rewritten, %d already fixed)'
      % (len(R1), done, already))
open(dst, 'wb').write(s.to_lsb())
