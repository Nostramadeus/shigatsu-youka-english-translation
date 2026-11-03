"""Lane 1 2026-11-03 (keyaudit2), break-off save/load panel. Run by tools/apply_labels.sh (IN.lsb OUT.lsb); idempotent.

U4: idx 192 (after a save) and idx 266 (slot list) do セーブ内容[スロット-1][0] = StringReplace(<it>, " ", "", 1, 1)
    before printing the slot date. The Japanese date only loses a cosmetic half-width space; the English one becomes
    "Shiyo800-04-0819:10" and a True-arc slot "Section3/7". The replacement "" becomes " ", so the call leaves the
    text as it is (the save itself already stores ナビ日時 unchanged apart from full-width spaces, idx 151/152).
C2: idx 203 / 275 DBLocate("名前", セーブ内容[スロット-1][6]) with the English person name of the slot -> mapped back to
    the 人物名簿 key first (dispcol.key_at_dblocate), so DBGetStr("色") at 204 / 276 reads the located person's colour
    as in Japanese. Names that are no 表示名 ("Natsumi Kogori/Erina Goto", "the Prince", ...) fail as before."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript
from dispcol import key_at_dblocate

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
for idx in (192, 266):
    p = s.commands[idx]['Calc']
    cur = str(p)
    if 'StringReplace(セーブ内容[スロット - 1][0], " ", " ", 1, 1)' in cur:
        print(f'fix-0000227A: idx {idx} date space strip already off')
        continue
    if 'StringReplace(セーブ内容[スロット - 1][0], " ", "", 1, 1)' not in cur:
        sys.exit(f'fix-0000227A: idx {idx} unexpected {cur}')
    empties = [o for e in p.entries for o in e.operands if o.type.name == 'Str' and o.value == '']
    if len(empties) != 1:
        sys.exit(f'fix-0000227A: idx {idx}: {len(empties)} empty literals')
    empties[0].value = ' '
    print(f'fix-0000227A: idx {idx} date keeps its spaces: {p}')
key_at_dblocate([(203, 'Calc'), (275, 'Calc')], 'fix-0000227A')(s)
open(dst, 'wb').write(s.to_lsb())
