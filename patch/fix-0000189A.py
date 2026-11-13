"""Lane 1 2026-11-03 (keyaudit2 W1, Q2060): the chatter menu looks every per-topic flag up with
    DBDirectGet*("雑談リスト", "キャプション1", JCopy(選択肢[n], 5, 30), 0, 0, "<column>", <default>)
where 選択肢[n] = 連番 (3 digits) ++ " " ++ キャプション1, so the key is the caption cut to 30 characters. The
author's Japanese captions are 29 characters at most; the English ones run to 79 (雑談リスト.tsv; 77 in 雑談リスト2,
22 in 雑談リスト3), and five groups of English captions share their first 30 characters. Every JCopy(選択肢[...], 5, 30)
becomes JCopy(選択肢[...], 5, 100): whole captions (the キャプション1 column is untyped, i.e. at most 80 bytes), all
distinct (checked over the three tables; only one is loaded at a time, 0000189A idx 306-311).
47 sites (idx 226-268 and 1206-1257, 1513-1563). Each JCopy must have a first operand that is an element of
選択肢 and the operands 5 and 30 (or 100 when already fixed); the count must be exactly 47. Idempotent.
Run by tools/compile_en.sh (IN.lsb OUT.lsb)."""
import sys
from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeFuncType, ParamType

OLD, NEW, WANT = 30, 100, 47
src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
done = already = 0
for i, cmd in enumerate(s.commands):
    for k in list(cmd.keys()):
        try:
            p = cmd[k]
        except Exception:
            continue
        ents = getattr(p, 'entries', None)
        if not ents:
            continue
        dims = {e.name for e in ents if e.type.name == 'DimTo' and e.operands
                and e.operands[0].type == ParamType.Var and e.operands[0].value == '選択肢'}
        # the compiler copies the element into a temp first (____4 = ____d_5), so follow one To alias
        dims |= {e.name for e in ents if e.type.name == 'To' and len(e.operands) == 1
                 and e.operands[0].type == ParamType.Var and e.operands[0].value in dims}
        for e in ents:
            if e.func != OpeFuncType.JCopy or len(e.operands) != 3:
                continue
            a, b, c = e.operands
            if a.type != ParamType.Var or a.value not in dims:
                continue
            if b.type != ParamType.Int or b.value != 5 or c.type != ParamType.Int or c.value not in (OLD, NEW):
                sys.exit(f'fix-0000189A: idx {i} {k}: unexpected JCopy operands {b.value}, {c.value}')
            if c.value == NEW:
                already += 1
            else:
                c.value = NEW
                done += 1
if done + already != WANT:
    sys.exit(f'fix-0000189A: found {done + already} JCopy(選択肢[...], 5, n) sites, expected {WANT}; nothing written')

# keyaudit2 C9 (orchestrator decision: option a, one line like the Japanese; the full answer stays in the
# conversation). The answer excerpt is cut at JLength > N / JDelete(Aテキスト, N), N = 35 in the chatter info panel
# (idx 954/955, 963/964; one-line Caption "情報", ＭＳ ゴシック 18 px = 9 px per Latin letter, 810 px box, line
# "　　Haruka Niimura: " + excerpt + "…… ") and N = 38 in the choice info panel (idx 1433/1434, 1450/1451; ＭＳ 明朝 20 px
# = 10 px per letter, 962 px box, "Haruka Niimura: " prefix). The Japanese fills each line (801 / 910 px); x2.5
# would run 216 / 213 px past the edge. N becomes the most that fits: 62 and 73 (802 / 955 px incl. margins).
CUTS = {954: (35, 62), 955: (35, 62), 963: (35, 62), 964: (35, 62),
        1433: (38, 73), 1434: (38, 73), 1450: (38, 73), 1451: (38, 73)}
cut_done = cut_already = 0
for idx, (old, new) in CUTS.items():
    p = s.commands[idx]['Calc']
    if 'Aテキスト' not in str(p):
        sys.exit(f'fix-0000189A: idx {idx} is not an Aテキスト cut: {p}')
    ints = [o for e in p.entries for o in e.operands if o.type == ParamType.Int and o.value in (old, new)]
    if len(ints) != 1:
        sys.exit(f'fix-0000189A: idx {idx}: {len(ints)} operands {old}/{new} in {p}')
    if ints[0].value == new:
        cut_already += 1
    else:
        ints[0].value = new
        cut_done += 1
# Lane W 2026-11-14: two-line reply captions and their echo lines (patch/layoutw.py)
import os  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layoutw  # noqa: E402
layoutw.fix_189a(s)
open(dst, 'wb').write(s.to_lsb())
print(f'fix-0000189A: chatter key length {OLD} -> {NEW} at {done} sites ({already} already fixed)')
print(f'fix-0000189A: answer excerpt cuts 35/38 -> 62/73 at {cut_done} sites ({cut_already} already fixed)')
