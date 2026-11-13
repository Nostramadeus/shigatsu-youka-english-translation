"""R1 2026-09-26: encyclopedia names are printed from the display column 表示名, the key column stays Japanese.
See patch/dispcol.py. Run by tools/compile_en.sh (or directly: IN.lsb OUT.lsb; idempotent)."""
import copy
import os, sys
from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispcol import run

PLACE_IDX = 834
PLACE_HEIGHT = 'GetProp("テキスト矩形", 6) - 5'
source = LMScript.from_file(sys.argv[1])
if len(source.commands) <= PLACE_IDX:
    sys.exit(f'fix-00001878: missing PLACE command {PLACE_IDX}')
place = source.commands[PLACE_IDX]
if place.type.name != 'MesNew' or str(place['Name']) != '"場所詳細"':
    sys.exit(f'fix-00001878: unexpected PLACE target at idx {PLACE_IDX}')
if str(place['PR_HEIGHT']) not in (PLACE_HEIGHT, '20000'):
    sys.exit(f'fix-00001878: unexpected PLACE height {place["PR_HEIGHT"]}')

SITES = [
    (750, 'PR_TEXT', '場所名', '表示名'),
    (751, 'PR_TEXT', '場所名', '表示名'),
    (758, 'PR_TEXT', '場所名', '表示名'),
    (759, 'PR_TEXT', '場所名', '表示名'),
    (1009, 'PR_TEXT', '場所名', '表示名'),
    (1340, 'PR_TEXT', '出来事名', '表示名'),
    (1341, 'PR_TEXT', '出来事名', '表示名'),
    (1342, 'PR_TEXT', '出来事名', '表示名'),
    (1405, 'PR_TEXT', '出来事名', '表示名'),
]
run(SITES, 'fix-00001878')

# GAPS4 2026-10-01: 事典物 has a 表示名 column too. The one place an item NAME is printed is idx 1669
# (Caption "物キャプション", PR_TEXT = @Sender, the clicked object whose name is the 物名 key). The cursor is not on
# the clicked row there (the loop at 1653-1658 walks the whole table after the DBLocate at 1650), so the text
# becomes the script's own cursor-free lookup, the form idx 1630 uses:
#     DBDirectGetStr("物リスト", "物名", @Sender, 0, 0, "表示名", "NG")
# Only PR_TEXT of idx 1669 changes; the object name, every DBLocate / Exists / ImgNew path still use 物名 / @Sender.
TEXT_IDX, TEMPLATE_IDX = 1669, 1630
WANT = 'DBDirectGetStr("物リスト", "物名", @Sender, 0, 0, "表示名", "NG")'
dst = sys.argv[2]
s = LMScript.from_file(dst)
cap, tpl = s.commands[TEXT_IDX], s.commands[TEMPLATE_IDX]
cur = str(cap['PR_TEXT'])
if cur == WANT:
    print('fix-00001878: item caption already fixed')
else:
    if cur != '@Sender' or not str(tpl['Calc']).startswith('物テキスト値 = DBDirectGetStr("物リスト", "物名", @Sender, 0, 0, '):
        sys.exit(f'fix-00001878: unexpected idx {TEXT_IDX} {cur!r} / idx {TEMPLATE_IDX} {tpl["Calc"]}')
    ents = copy.deepcopy(tpl['Calc'].entries)  # ____0..____3 literals, ____4 the DBDirectGetStr call, then 物テキスト値 =
    for e, val in zip(ents[:4], ('物リスト', '物名', '表示名', 'NG')):
        e.operands[0].value = val
    last = copy.deepcopy(cap['PR_TEXT'].entries[-1])  # '____arg' <- @Sender
    last.operands[0].value = ents[4].name
    cap['PR_TEXT'].entries = ents[:5] + [last]
    if str(cap['PR_TEXT']) != WANT:
        sys.exit(f'fix-00001878: rebuilt idx {TEXT_IDX} reads {cap["PR_TEXT"]}')
    open(dst, 'wb').write(s.to_lsb())
    print('fix-00001878: item caption reads 表示名')

place = s.commands[PLACE_IDX]
if str(place['PR_HEIGHT']) == '20000':
    print('fix-00001878: PLACE scroll buffer already fixed')
else:
    place['PR_HEIGHT'].entries = [OpeData(
        type=OpeDataType.To, name='____arg',
        operands=[Param(value=20000, type=ParamType.Int)])]
    open(dst, 'wb').write(s.to_lsb())
    print('fix-00001878: PLACE scroll buffer height 20000')

# Lane 1 2026-11-03 (GitHub issue #5 + friend report item 6), see patch/dispcol.py:
#  - idx 49 (`事典2035 = 0`, run on every encyclopedia entry) also rewrites a Japanese 事典編 from an old save.dat to
#    its English name, so the People / Events / Things filters match again (dispcol.hen_normalise).
#  - idx 1343..1357 (odd): the per-event arc badge tests read the 事典出来事 COLUMNS 呪殺編 ... エデンの桜編, whose
#    headers stay Japanese; patch/hen-jp-en.tsv had renamed the column argument to the English arc name, so
#    DBGetStr returned "" and no badge was ever drawn. The column name goes back to Japanese (only that operand).
#  - idx 518, the person hover caption (PR_TEXT = @Sender = the 名前 key), prints the 人物名簿 表示名; the six sites
#    that read that caption back as a KEY (575/584/2057/2066 DBLocate, 587 compare, 2101 フォーカス人物) map it back
#    to 名前 through the same table (dispcol.key_from_display); idx 2222 ("no data for <arc>/<name>") prints the
#    表示名 of フォーカス人物 (dispcol.display_var). Follow-up 2026-11-03.
from dispcol import HEN_JP_EN, hen_normalise, person_caption, key_from_display, display_var
BADGES = [(1343 + 2 * k, jp) for k, jp in enumerate(
    ('呪殺編', '明徴編', '詫言編', '死月編', '最後の声編', '真・呪殺編', '真・明徴編', 'エデンの桜編'))]
EN_OF = dict(HEN_JP_EN)
s = LMScript.from_file(dst)
for idx, jp in BADGES:
    cmd = s.commands[idx]
    ops = [o for e in cmd['Calc'].entries for o in e.operands if getattr(o, 'value', None) in (jp, EN_OF[jp])]
    if cmd.type.name != 'If' or len(ops) != 1:
        sys.exit(f'fix-00001878: badge idx {idx}: {cmd.type.name} {cmd["Calc"]} ({len(ops)} matching operands)')
    if not str(cmd['Calc']).startswith(('DBGetStr(', '(DBGetStr(')):
        sys.exit(f'fix-00001878: badge idx {idx} unexpected {cmd["Calc"]}')
    ops[0].value = jp
hen_normalise(49, 'fix-00001878')(s)
person_caption(518, 'fix-00001878', var='@Sender', name_prefix='"人物テキスト"')(s)
key_from_display([(575, 'Calc'), (584, 'Calc'), (587, 'Calc'), (2057, 'Calc'), (2066, 'Calc'), (2101, 'InitVal')],
                 'fix-00001878')(s)
display_var([(2222, 'Calc', 'フォーカス人物')], 'fix-00001878')(s)
# idx 519 (person hover kana reading, DBDirectGetStr(... "読み仮名" ...)): blanked like the map captions' readings
# (patch/labels-00001878.tsv maps each map reading literal to ""), coordinator decision 2026-11-03.
READING_WANT = 'DBDirectGetStr("人物名簿", "名前", @Sender, 0, 0, "読み仮名", "NG")'
rd = s.commands[519]
if rd.type.name != 'Caption' or str(rd['Name']) != '"人物読み仮名"':
    sys.exit(f'fix-00001878: idx 519 is {rd.type.name} {rd["Name"]}')
if str(rd['PR_TEXT']) == '""':
    print('fix-00001878: reading caption idx 519 already blank')
elif str(rd['PR_TEXT']) != READING_WANT:
    sys.exit(f'fix-00001878: idx 519 PR_TEXT {rd["PR_TEXT"]}')
else:
    rd['PR_TEXT'].entries = [OpeData(type=OpeDataType.To, name='____0', operands=[Param(value='', type=ParamType.Str)]),
                             OpeData(type=OpeDataType.To, name='____arg', operands=[Param(value='____0', type=ParamType.Var)])]
    print('fix-00001878: reading caption idx 519 blank')
open(dst, 'wb').write(s.to_lsb())
print('fix-00001878: badge columns Japanese again, 事典編 normalised at entry, person names via 表示名')

# Lane X1 2026-11-13 (notes/FIT-MODEL-2.md 4.2; friend report: name plate "Mifuyu Niimur"). On a People-page click the
# plate 人物テキスト土台 slides to x 490 (idx 554 PropMotion, ObjProp 3 = PR_LEFT). The arc selector 編選択 (idx 1866, x 680,
# PRIORITY 4000) is drawn over everything from x 680, so a long English name lost its end. With the name Caption at 26 px
# (patch/props-00001878.tsv, idx 516/518) the plate now keeps x 490 when it fits and moves left only as far as needed,
# never past x 410 (the scroll-up icon at idx 602 covers x 301..409):
#     Max(410, Min(490, 676 - GetProp("人物テキスト土台", 5)))      676 = 680 minus a 4 px gap
# GetProp index 5 = PR_WIDTH (idx 527 tests left 3 + width 5 against @ScrWidth; pylivemaker PropertyType PR_NONE 0 .. PR_WIDTH 6).
# Min / Max are engine functions the game runs already (ノベルシステム/■オプション_テキスト速度.lsb idx 14, 18).
# The plate width was set at idx 521/523 (caption width + 4) before the click, so the value is read at the slide.
SLIDE_IDX = 554
SLIDE_WANT = 'Max(410, Min(490, 676 - GetProp("人物テキスト土台", 5)))'
s = LMScript.from_file(dst)
sl = s.commands[SLIDE_IDX]
if sl.type.name != 'PropMotion' or str(sl['ObjName']) != '"人物テキスト土台"' or str(sl['ObjProp']) != '3':
    sys.exit(f'fix-00001878: idx {SLIDE_IDX} is {sl.type.name} {sl.get("ObjName")} {sl.get("ObjProp")}, not the plate slide')
cur = str(sl['Value'])
if cur == SLIDE_WANT:
    print('fix-00001878: name plate slide idx 554 already fixed')
elif cur != '490':
    sys.exit(f'fix-00001878: idx {SLIDE_IDX} Value {cur!r}, expected 490')
else:
    S, V, I = ParamType.Str, ParamType.Var, ParamType.Int
    sl['Value'].entries = [
        OpeData(type=OpeDataType.To, name='____0', operands=[Param(value='人物テキスト土台', type=S)]),
        OpeData(type=OpeDataType.Func, name='____1', func=OpeFuncType.GetProp,
                operands=[Param(value='____0', type=V), Param(value=5, type=I)]),
        OpeData(type=OpeDataType.Minus, name='____2', operands=[Param(value=676, type=I), Param(value='____1', type=V)]),
        OpeData(type=OpeDataType.Func, name='____3', func=OpeFuncType.Min,
                operands=[Param(value=490, type=I), Param(value='____2', type=V)]),
        OpeData(type=OpeDataType.Func, name='____4', func=OpeFuncType.Max,
                operands=[Param(value=410, type=I), Param(value='____3', type=V)]),
        OpeData(type=OpeDataType.To, name='____arg', operands=[Param(value='____4', type=V)])]
    if str(sl['Value']) != SLIDE_WANT:
        sys.exit(f'fix-00001878: rebuilt idx {SLIDE_IDX} reads {sl["Value"]}')
    open(dst, 'wb').write(s.to_lsb())
    print('fix-00001878: name plate slide idx 554 = ' + SLIDE_WANT)
