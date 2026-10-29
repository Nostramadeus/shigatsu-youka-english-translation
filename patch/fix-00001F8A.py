"""Structural fix for work/00001F8A.lsb, run by tools/apply_labels.sh after the label maps
(game follow-up r2, 2026-10-30, consumer audit R6).

    uv run --no-project --with pylivemaker python patch/fix-00001F8A.py IN.lsb OUT.lsb

R6 staff roll. Scene 313 (and only it: idx 121 Calls label 00002229 when 選択シナリオ == 313) shows the credits from
the table スタッフロール2 one step per 100 running characters (idx 538-561, LineNo 596-618):
    step = 文字数誤差 / 100                      credit rows with 順番 == step are captioned "テキスト<step>"
    文字数誤差 % 100 <= 60  -> show the step's caption (once; the previous step's caption is deleted)
    文字数誤差 % 100 >  60  -> fade it out
25 steps = 2,500 characters: 65 % of the Japanese scene (3,869 characters), but only 29 % of the English one (8,500).
Fix: the step is 220 characters (8,500 / 3,869 = 2.2), so the roll again ends at 65 % of the scene; the show/fade
point inside a step moves with it, 60 -> 132 (60 % of the step, as in the original). Every `文字数誤差 / 100` and
`文字数誤差 % 100` in the block becomes 220 (24 + 2 sites) and the two `% ... 60` tests become 132; nothing outside
idx 538-561 changes (the percent displays at idx 348-365 also read 文字数誤差 and stay as they are).

Each (command, property) must hold exactly its original expression, or the fixed one (idempotent); anything else and
the script refuses to write. Checks: patch/exprfix.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript  # noqa: E402
import exprfix as xf  # noqa: E402
from exprfix import I, S, V  # noqa: E402

D = '文字数誤差'
STEP_OLD, STEP_NEW = 100, 220
SHOW_OLD, SHOW_NEW = 60, 132


def name(prefix):                       # "<prefix>" ++ 文字数誤差 / 100
    return [(1, '____0', None, [S(prefix)]), (5, '____1', None, [V(D), I(100)]),
            (19, '____2', None, [V('____0'), V('____1')]), (1, '____arg', None, [V('____2')])]


def name_prev(prefix):                  # "<prefix>" ++ 文字数誤差 / 100 - 1
    return [(1, '____0', None, [S(prefix)]), (5, '____1', None, [V(D), I(100)]),
            (3, '____2', None, [V('____1'), I(1)]), (19, '____3', None, [V('____0'), V('____2')]),
            (1, '____arg', None, [V('____3')])]


CENTER = [  # 0 - 960 - GetProp("テキスト" ++ 文字数誤差 / 100, 3) - GetProp("テキスト" ++ 文字数誤差 / 100, 5) / 2
    (1, '____0', None, [S('テキスト')]), (1, '____1', None, [S('テキスト')]),
    (5, '____4', None, [V(D), I(100)]), (19, '____5', None, [V('____1'), V('____4')]),
    (11, '____2', 'GetProp', [V('____5'), I(5)]),
    (5, '____8', None, [V(D), I(100)]), (19, '____9', None, [V('____0'), V('____8')]),
    (11, '____6', 'GetProp', [V('____9'), I(3)]),
    (3, '____11', None, [I(960), V('____6')]), (3, '____12', None, [V('____11'), V('____2')]),
    (5, '____13', None, [V('____12'), I(2)]), (3, '____14', None, [I(0), V('____13')]),
    (1, '____arg', None, [V('____14')])]

SITES = [  # (idx, command, property, original expression)
    (538, 'If', 'Calc', [  # If 文字数誤差 / 100 > 0
        (5, '____0', None, [V(D), I(100)]), (13, '____1', None, [V('____0'), I(0)]),
        (1, '____arg', None, [V('____1')])]),
    (539, 'If', 'Calc', [  # If (Exists("テキスト" ++ 文字数誤差 / 100) == 0 & 文字数誤差 % 100 <= 60)
        (1, '____0', None, [S('テキスト')]), (5, '____3', None, [V(D), I(100)]),
        (19, '____4', None, [V('____0'), V('____3')]), (11, '____1', 'Exists', [V('____4')]),
        (6, '____5', None, [V(D), I(100)]), (12, '____6', None, [V('____1'), (3, 0)]),
        (16, '____7', None, [V('____5'), I(60)]), (8, '____8', None, [V('____6'), V('____7')]),
        (1, '____arg', None, [V('____8')])]),
    (540, 'ObjDel', 'Name', name_prev('テキスト')),
    (541, 'ObjDel', 'Name', name_prev('テキスト黒')),
    (546, 'Break', 'Calc', [  # Break DBGetInt("順番") > 文字数誤差 / 100
        (1, '____0', None, [S('順番')]), (11, '____1', 'DBGetInt', [V('____0')]),
        (5, '____2', None, [V(D), I(100)]), (13, '____3', None, [V('____1'), V('____2')]),
        (1, '____arg', None, [V('____3')])]),
    (547, 'If', 'Calc', [  # If DBGetInt("順番") == 文字数誤差 / 100
        (1, '____0', None, [S('順番')]), (11, '____1', 'DBGetInt', [V('____0')]),
        (5, '____2', None, [V(D), I(100)]), (12, '____3', None, [V('____1'), V('____2')]),
        (1, '____arg', None, [V('____3')])]),
    (553, 'Caption', 'Name', name('テキスト')),
    (554, 'Caption', 'Name', name('テキスト黒')),
    (555, 'SetProp', 'ObjName', name('テキスト')),
    (555, 'SetProp', 'Value', CENTER),
    (556, 'SetProp', 'ObjName', name('テキスト黒')),
    (556, 'SetProp', 'Value', CENTER),
    (557, 'PropMotion', 'Name', name('テキスト出現')),
    (557, 'PropMotion', 'ObjName', name('テキスト')),
    (558, 'PropMotion', 'Name', name('テキスト出現黒')),
    (558, 'PropMotion', 'ObjName', name('テキスト黒')),
    (559, 'If', 'Calc', [  # If ((文字数誤差 % 100 > 60 & Exists("テキスト" ++ step) == 1) & Exists("テキスト消去" ++ step) == 0)
        (1, '____0', None, [S('テキスト')]), (1, '____1', None, [S('テキスト消去')]),
        (5, '____4', None, [V(D), I(100)]), (19, '____5', None, [V('____1'), V('____4')]),
        (11, '____2', 'Exists', [V('____5')]),
        (5, '____8', None, [V(D), I(100)]), (19, '____9', None, [V('____0'), V('____8')]),
        (11, '____6', 'Exists', [V('____9')]),
        (6, '____10', None, [V(D), I(100)]), (13, '____11', None, [V('____10'), I(60)]),
        (12, '____12', None, [V('____6'), (3, 1)]), (12, '____13', None, [V('____2'), (3, 0)]),
        (8, '____14', None, [V('____11'), V('____12')]), (8, '____15', None, [V('____14'), V('____13')]),
        (1, '____arg', None, [V('____15')])]),
    (560, 'PropMotion', 'Name', name('テキスト消去')),
    (560, 'PropMotion', 'ObjName', name('テキスト')),
    (561, 'PropMotion', 'Name', name('テキスト消去黒')),
    (561, 'PropMotion', 'ObjName', name('テキスト黒')),
]


def fixed(shape):
    """文字数誤差 / 100 and 文字数誤差 % 100 -> 220; a > or <= test of such a % result against 60 -> 132."""
    mods = {s[1] for s in shape if s[0] == 6 and s[3] == [V(D), I(STEP_OLD)]}
    swaps = {}
    for s in shape:
        if s[0] in (5, 6) and s[3] == [V(D), I(STEP_OLD)]:
            swaps[(s[1], 1)] = (STEP_OLD, STEP_NEW)
        if s[0] in (13, 16) and s[3][0][1] in mods and s[3][1] == I(SHOW_OLD):
            swaps[(s[1], 1)] = (SHOW_OLD, SHOW_NEW)
    return xf.const_fixed(shape, swaps)


count = {}
for _, _, _, shape in SITES:
    for s in shape:
        if s[3] == [V(D), I(STEP_OLD)] or (s[0] in (13, 16) and s[3][1] == I(SHOW_OLD)):
            count[s[0]] = count.get(s[0], 0) + 1
assert count == {5: 24, 6: 2, 16: 1, 13: 1}, count   # 24 steps, 2 remainders, the <= 60 show and > 60 fade tests

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
if len(s.commands) != 854:
    sys.exit('fix-00001F8A: %d commands, expected 854 (not 00001F8A, or its structure changed)' % len(s.commands))
done, already = xf.apply_sites(s, [(i, kind, key, shape, fixed(shape), None) for i, kind, key, shape in SITES],
                               'fix-00001F8A')
print('fix-00001F8A: r2 staff roll step %d -> %d characters, show/fade point %d -> %d, %d expressions '
      '(%d rewritten, %d already fixed)' % (STEP_OLD, STEP_NEW, SHOW_OLD, SHOW_NEW, len(SITES), done, already))
open(dst, 'wb').write(s.to_lsb())
