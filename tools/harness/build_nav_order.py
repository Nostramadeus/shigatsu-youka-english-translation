"""Derive the scenario-navigator order and unlock conditions from lmlsb dumps only.

Writes notes/_db/_navigator-order.tsv. The game is never launched.
"""
import csv, io, json, re
from pathlib import Path

D = Path("tools/harness/work/dumps")
OUT = Path("notes/_db/_navigator-order.tsv")

def load(name):
    """[(LineNo, indent, text)] in file order."""
    out = []
    for raw in io.open(D / name, encoding="utf-8"):
        m = re.match(r"^(\s*)(\d+):(.*)$", raw.rstrip("\n"))
        if m:
            body = m.group(3).rstrip()
            # indentation is AFTER the "<LineNo>:" prefix, not before it
            out.append((int(m.group(2)), len(body) - len(body.lstrip()), body))
    return out

DC, F2 = load("000015DC.txt"), load("000000F2.txt")

# ---- unlock graph: inside `選択シナリオ == N`, which st<M> are set, under which guards ----
unlocks = {}          # M -> [(N, value, verbatim guards, LineNo)]
cur, stack = None, []
for ln, ind, t in DC:
    s = t.strip()
    m = re.match(r"^(?:If|Elseif) 選択シナリオ == (\d+)$", s)
    if m:
        cur, stack = int(m.group(1)), [(ind, s)]
        continue
    if cur is not None:
        if ind <= stack[0][0] and not s.startswith(("If ", "Elseif ", "Else", "Calc ", "Break")):
            cur, stack = None, []
            continue
        while len(stack) > 1 and stack[-1][0] >= ind:
            stack.pop()
        if s.startswith(("If ", "Elseif ")):
            stack.append((ind, s))
        m2 = re.match(r"^Calc st(\d+) = (\d+)$", s)
        if m2:
            tgt, val = int(m2.group(1)), int(m2.group(2))
            if tgt != cur and val in (1, 3):
                guards = " / ".join(g for _, g in stack)
                unlocks.setdefault(tgt, []).append((cur, val, guards, ln))

# ---- fresh-save initialiser: 000000F2.lsb Label 0000199E ----
initial = {}
for ln, _, t in F2:
    if 305 <= ln <= 315:
        m = re.match(r"^\s*Calc st(\d+) = (\d+)$", t)
        if m:
            initial[int(m.group(1))] = (int(m.group(2)), ln)

# ---- data-driven unlock table パス.tsv ----
pas = {}
for r in csv.DictReader(io.open("orig/データベース/パス.tsv", encoding="cp932"), delimiter="\t"):
    for i in (1, 2, 3):
        v = (r.get("変更%d" % i) or "").strip()
        m = re.match(r"^st(\d+)$", v)
        if m:
            conds = []
            for j in (1, 2, 3):
                c, val = (r.get("条件%d" % j) or "").strip(), (r.get("値%d" % j) or "").strip()
                if c:
                    conds.append("%s == %s" % (c, val))
            pas.setdefault(int(m.group(1)), []).append(
                (r.get("ID"), " & ".join(conds), (r.get("変更値%d" % i) or "").strip()))

CHAIN = json.load(io.open("tools/harness/work/nav_chain.json", encoding="utf-8"))

rows = list(csv.DictReader(io.open("orig/データベース/シナリオデータベース.tsv",
                                   encoding="cp932"), delimiter="\t"))

OUT.parent.mkdir(parents=True, exist_ok=True)
w = io.open(OUT, "w", encoding="utf-8", newline="\n")
w.write("""# Scenario-navigator order and unlock conditions.
# Derived 2026-09-25 from `lmlsb dump` output only. The game was not launched for this.
#
# ORDER   0000001C.lsb activates the table as "ナビデータ" (DBSetActive, LineNo 1444 / 1551)
#         and walks it with DBFindFirst()/DBFindNext() (loop at LineNo 3946). So the record
#         order of orig/データベース/シナリオデータベース.tsv IS the map order. 219 records.
#         Column 列番号 is the map column; 罫線1-6 are the link lines drawn to other entries.
# STATE   one variable per entry, st<連番>. 0000001C.lsb LineNo 3953 reads it as
#         AssignTemp("st" ++ DBGetStr("連番")). 0 = locked, 1 and 3 = unlocked/unplayed,
#         5+ = played (LineNo 3954 counts 5,7,8,10,11,12 as finished; LineNo 4004 refuses the
#         synopsis while < 5).
# UNLOCK  000015DC.lsb, entered at the end of a scene (e.g. 00000024.lsb LineNo 38
#         `Jump 000015DC.lsb:0`). It holds `If/Elseif 選択シナリオ == N` blocks that mark
#         st<N> played and set st<M> = 3 for what N unlocks. Guards are quoted verbatim.
# INITIAL 000000F2.lsb `Label 0000199E`, LineNo 305-315, is the first-boot initialiser
#         (version, volumes, 完成版 = 1, load the 注意 table). It sets exactly one st.
# PATHS   orig/データベース/パス.tsv is a second, data-driven unlock table:
#         条件N/値N -> 変更N/変更値N. Rows that write an st<M> are folded in below.
#
# TARGET  0000001C.lsb index 3282 jumps to 000015E3.lsb. Both files hold
#         `If/Elseif 選択シナリオ == N` conditions whose NEXT command is a
#         `PCReset Page=<file> Label=<n>`.
#
#         THE ADDRESSING RULE: LabelReference.Label is a 0-BASED INDEX into the target
#         page's command list (LMScript.commands, file order). It is NOT a LineNo and NOT
#         a label id/name. Every such reference lands on cmds[n] == a `Label` command,
#         followed by `Call <self>:1` (変数削除) and `Jump <scene>.lsb:0` - the triplet the
#         engine uses for every scene entry.
#         LineNo does NOT work as an address: it is not unique (WhileInit/While/WhileLoop
#         share one), so index and LineNo coincide early in a file and drift apart later
#         (000015E3.lsb: 2182 commands, max LineNo 2408).
#         All LineNo references in these comments are pylivemaker dump line numbers, for
#         reading only; all addresses used for resolution are command indices.
#
#         205 entries carry a condition and all 205 resolve, onto 221 distinct scene files
#         with no file claimed by two entries. Where an entry has more than one condition
#         (an alternate route), the primary chain's target is used and the alternates are
#         listed in the notes.
#
# columns: position  entry_label_or_id  unlock_condition  target_lsb  notes
""")
w.write("position\tentry_label_or_id\tunlock_condition\ttarget_lsb\tnotes\n")

def targets(num):
    return [x for x in CHAIN.get(str(num), []) if x.get("lsb")]


def emit(pos, ren, cond, notes, num=None):
    tg = targets(num)
    lsb = tg[0]["lsb"] if tg else ""
    if len(tg) > 1:
        notes += "; alternate targets: " + ",".join(x["lsb"] for x in tg[1:])
    w.write("%d\t%s\t%s\t%s\t%s\n" % (pos, ren, cond, lsb, notes))

n_rows = 0
for pos, r in enumerate(rows, 1):
    ren = (r.get("連番") or "").strip()
    try:
        num = int(float(ren))
    except ValueError:
        num = None
    arc = (r.get("解禁編") or "").strip()
    col = (r.get("列番号") or "").strip()
    base = "arc=%s; 列番号=%s; 文字数1=%s" % (arc, col, (r.get("文字数1") or "").strip())
    wrote = False
    if num in initial:
        val, ln = initial[num]
        emit(pos, ren, "INITIAL on a fresh save: 000000F2.lsb LineNo %d `Calc st%d = %d`"
             % (ln, num, val), base + "; the ONLY entry unlocked at first boot", num)
        wrote = True
        n_rows += 1
    for src, val, guards, ln in unlocks.get(num, []):
        emit(pos, ren, "playing 選択シナリオ == %d -> 000015DC.lsb LineNo %d `Calc st%d = %d`; guards: %s"
             % (src, ln, num, val, guards), base + "; unlocked by entry %d" % src, num)
        wrote = True
        n_rows += 1
    for pid, conds, val in pas.get(num, []):
        emit(pos, ren, "パス.tsv ID %s: if %s then st%d = %s" % (pid, conds or "(none)", num, val),
             base + "; data-driven unlock", num)
        wrote = True
        n_rows += 1
    if not wrote:
        emit(pos, ren, "(no st write found in 000015DC.lsb / 000000F2.lsb / パス.tsv)", base, num)
        n_rows += 1
w.close()

print("records:", len(rows), "| rows written:", n_rows)
print("INITIAL:", initial)
print("unlocked by playing 195:", [(k, v) for k, vs in unlocks.items() for v in vs if v[0] == 195])
filled = sum(1 for r in rows if targets(int(float(r["連番"]))) ) if rows else 0
print("entries with a target_lsb:", filled, "of", len(rows))
print("wrote", OUT)
