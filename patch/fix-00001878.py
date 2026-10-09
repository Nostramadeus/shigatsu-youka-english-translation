"""R1 2026-09-26: encyclopedia names are printed from the display column 表示名, the key column stays Japanese.
See patch/dispcol.py. Run by tools/compile_en.sh (or directly: IN.lsb OUT.lsb; idempotent)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispcol import run
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
import copy
from livemaker.lsb import LMScript

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
