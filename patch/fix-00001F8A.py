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

Reference popup (bug 2026-11-16). Since patch-2026-11-03 the "reference unlocked" popup rests at x 570, not 610
(patch/props-000016C3.tsv, PropMotion Value idx 374/397/420). idx 105, 110, 115 here still test
`GetProp("リファレンス解禁土台<n>", 3) == 610` before they start the retreat, so the popup never retreats by itself.
Fix: that one literal 610 -> 570 in those three expressions (the click test is patch/fix-000016C3.py idx 460). The other
610 literals in this script (PR_LEFT=610 at idx 553, 585, 827, ...) are not the popup and stay.

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


REF_X_OLD, REF_X_NEW = 610, 570


def ref_retreat(n):                     # If (Exists("リファレンス撤収<n>") == 0 & GetProp("リファレンス解禁土台<n>", 3) == 610)
    return [(1, '____0', None, [S('リファレンス撤収' + n)]), (1, '____1', None, [S('リファレンス解禁土台' + n)]),
            (11, '____2', 'GetProp', [V('____1'), I(3)]), (11, '____3', 'Exists', [V('____0')]),
            (12, '____4', None, [V('____3'), (3, 0)]), (12, '____5', None, [V('____2'), I(REF_X_OLD)]),
            (8, '____6', None, [V('____4'), V('____5')]), (1, '____arg', None, [V('____6')])]


REF_SITES = [(105, 'If', 'Calc', ref_retreat('')), (110, 'If', 'Calc', ref_retreat('2')),
             (115, 'If', 'Calc', ref_retreat('3'))]


# Issue 8 (bug 2026-11-18, ORIGINAL-GAME bug, same in JP). While a scenario is on screen, idx 302 (Label 00001F8D)
# re-derives 選択シナリオ from the title: DBDirectGetStr("ナビデータ", "タイトル", ナビタイトル名, 0, 0, "連番", 選択シナリオ).
# Inside a hidden route ナビタイトル名 = title ++ " (Hidden Route)" / " (Hidden Route 2)" / " 3)" / " 4)" (0000001C idx
# 6124-6130), which matches no row, so a stale 選択シナリオ survives a slot load and the route-end write (000015DC idx
# 2362) lands on the wrong 裏ルート変数 cell. Fix: the lookup key is ナビタイトル名 with those four suffixes removed
# (StringReplace(source, old, new), the argument order of 0000001C idx 104). A normal title holds none of them, so
# normal play computes the same value. Checks: work/bugs-2026-11-18/issue8-fix/PROGRESS.md.
HR = [' (Hidden Route)', ' (Hidden Route 2)', ' (Hidden Route 3)', ' (Hidden Route 4)']
SEL = '選択シナリオ'
ISSUE8_OLD = [(1, '____0', None, [S('ナビデータ')]), (1, '____1', None, [S('タイトル')]), (1, '____2', None, [S('連番')]),
              (11, '____3', 'DBDirectGetStr', [V('____0'), V('____1'), V('ナビタイトル名'), (3, 0), (3, 0), V('____2'),
                                               V(SEL)]),
              (1, SEL, None, [V('____3')])]


def issue8_fixed():
    out = ISSUE8_OLD[:3]
    key, n = 'ナビタイトル名', 3
    for suffix in HR:   # ____n = suffix, ____n+1 = "", ____n+2 = StringReplace(key, ____n, ____n+1)
        a, b, r = '____%d' % n, '____%d' % (n + 1), '____%d' % (n + 2)
        out += [(1, a, None, [S(suffix)]), (1, b, None, [S('')]), (11, r, 'StringReplace', [V(key), V(a), V(b)])]
        key, n = r, n + 3
    res = '____%d' % n
    out += [(11, res, 'DBDirectGetStr', [V('____0'), V('____1'), V(key), (3, 0), (3, 0), V('____2'), V(SEL)]),
            (1, SEL, None, [V(res)])]
    return out


ISSUE8_SITES = [(302, 'Calc', 'Calc', ISSUE8_OLD, issue8_fixed(), None)]


def ref_fixed(shape):
    """The popup's resting-x test == 610 -> == 570 (entry ____5, operand 1); nothing else."""
    return xf.const_fixed(shape, {('____5', 1): (REF_X_OLD, REF_X_NEW)})


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
done, already = xf.apply_sites(s, [(i, kind, key, shape, fixed(shape), None) for i, kind, key, shape in SITES]
                               + [(i, kind, key, shape, ref_fixed(shape), None) for i, kind, key, shape in REF_SITES]
                               + ISSUE8_SITES,
                               'fix-00001F8A')
print('fix-00001F8A: r2 staff roll step %d -> %d characters, show/fade point %d -> %d; reference popup resting x '
      '%d -> %d; issue8 hidden-route suffixes stripped from the idx 302 title lookup; %d expressions (%d rewritten, '
      '%d already fixed)'
      % (STEP_OLD, STEP_NEW, SHOW_OLD, SHOW_NEW, REF_X_OLD, REF_X_NEW, len(SITES) + len(REF_SITES) + len(ISSUE8_SITES),
         done, already))
open(dst, 'wb').write(s.to_lsb())
