"""Shared helper for the encyclopedia display-name fix (lane R1, 2026-09-26, UNTR1 row "c encyclopedia names", Q2054).

事典場所.tsv 場所名 and 事典出来事.tsv 出来事名 are KEYS (object names, DBLocate, .gal path components, a literal
compare) and are also printed as captions. The key columns stay Japanese; tsv-en/事典場所.tsv and 事典出来事.tsv gain a
trailing column 表示名 (English name for translated rows, a copy of the key for the others), and every PRINT site reads
DBGetStr("表示名") instead of the key. Only the string operand inside the named property of the named command changes;
nothing else in the file is touched.

    SITES = [(index, property, old column, new column), ...]
    run(SITES, 'fix-<id>')   # reads sys.argv[1] (IN.lsb), writes sys.argv[2] (OUT.lsb)

Each site must hold exactly one string operand equal to `old` (or, when already fixed, `new`); anything else is an
error and nothing is written. Idempotent.
"""
import sys
from livemaker.lsb import LMScript


def _operands(parser):
    for e in parser.entries:
        for o in e.operands:
            yield o


def run(sites, tag, extra=None):
    """extra(script), optional (game follow-up r2, 2026-10-30): more guarded edits on the same loaded script, called
    after every display site checked out and before the one write; it exits on a mismatch, so nothing is written."""
    src, dst = sys.argv[1], sys.argv[2]
    s = LMScript.from_file(src)
    errs, done, already = [], 0, 0
    for idx, prop, old, new in sites:
        cmd = s.commands[idx]
        try:
            parser = cmd[prop]
        except KeyError:
            errs.append(f'idx {idx}: no property {prop}')
            continue
        ops = [o for o in _operands(parser) if getattr(o, 'value', None) in (old, new)]
        if len(ops) != 1:
            errs.append(f'idx {idx} {prop}: expected one operand {old!r}, found {len(ops)} in {parser}')
            continue
        if ops[0].value == new:
            already += 1
            continue
        ops[0].value = new
        done += 1
    if errs:
        sys.exit(f'{tag}: ' + '; '.join(errs))
    if extra is not None:
        extra(s)
    open(dst, 'wb').write(s.to_lsb())
    print(f'{tag}: {done} display sites repointed, {already} already fixed')


# Lane 1, 2026-11-03 (friend report item 6: "Encyclopedia updated" listed 五島絵梨奈 / 古郡茜 / 古郡良治).
# The scene-end unlock list prints 終了時用事典解禁通知 in one Caption ("事典解禁テキスト" ++ n). For a person that
# variable holds 人物抽出[i] = 人物名簿.tsv 名前, a KEY (table name, "ロック" ++ name, the dedupe compare and the
# == "新村夏菜" test all read it), so it stays Japanese. Only the Caption's PR_TEXT changes, to
#     DBDirectGetStr("人物名簿", "名前", 終了時用事典解禁通知, 0, 0, "表示名", 終了時用事典解禁通知)
# i.e. the English 表示名 of tsv-en/人物名簿.tsv for a person and, when no row matches (a place heading, an event
# name, an item summary, "????"), the value itself. DBDirectGetStr is a cursor-free lookup (0000189A idx 996
# calls it on the table its own loop is walking and reads DBGetStr on the same record afterwards).
# The encyclopedia's own person hover caption (00001878 idx 518, PR_TEXT = @Sender = the 名前 key) gets the
# same lookup with @Sender.
PERSON_VAR = '終了時用事典解禁通知'


def _person_text(var):
    return f'DBDirectGetStr("人物名簿", "名前", {var}, 0, 0, "表示名", {var})'


def person_caption(idx, tag, var=PERSON_VAR, name_prefix='"事典解禁テキスト"'):
    """extra hook for run(): rewrite Caption idx PR_TEXT from the bare variable `var` to the 人物名簿 表示名 lookup."""
    want = _person_text(var)

    def hook(s):
        from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType
        cmd = s.commands[idx]
        if cmd.type.name != 'Caption' or not str(cmd['Name']).startswith(name_prefix):
            sys.exit(f'{tag}: idx {idx} is {cmd.type.name} {cmd["Name"]}, not the {name_prefix} caption')
        cur = str(cmd['PR_TEXT'])
        if cur == want:
            print(f'{tag}: person caption idx {idx} already fixed')
            return
        if cur != var:
            sys.exit(f'{tag}: idx {idx} PR_TEXT is {cur!r}, expected {var!r}')
        S, V = ParamType.Str, ParamType.Var
        lits = [OpeData(type=OpeDataType.To, name=f'____{i}', operands=[Param(value=v, type=S)])
                for i, v in enumerate(('人物名簿', '名前', '表示名'))]
        call = OpeData(type=OpeDataType.Func, name='____3', func=OpeFuncType.DBDirectGetStr, operands=[
            Param(value='____0', type=V), Param(value='____1', type=V), Param(value=var, type=V),
            Param(value=0, type=ParamType.Flag), Param(value=0, type=ParamType.Flag),
            Param(value='____2', type=V), Param(value=var, type=V)])
        arg = OpeData(type=OpeDataType.To, name='____arg', operands=[Param(value='____3', type=V)])
        cmd['PR_TEXT'].entries = lits + [call, arg]
        if str(cmd['PR_TEXT']) != want:
            sys.exit(f'{tag}: rebuilt idx {idx} reads {cmd["PR_TEXT"]}')
        print(f'{tag}: person caption idx {idx} reads 人物名簿 表示名')
    return hook


# Lane 1, 2026-11-03 (GitHub issue #5: encyclopedia People / Events / Things empty after applying the patch).
# 事典編 (scope 3 = shared by every slot, kept in save.dat) holds the encyclopedia's selected arc. The English build
# compares it with English arc names everywhere (00001878: event/thing filters DBGetStr("解禁編") == 事典編, the
# 事典解禁編 chains that drive the people page, the logo path). A save.dat written by the Japanese game holds
# "呪殺編" etc., matches nothing, and the lists stay empty until the player re-picks an arc in the selector
# (idx 2031 事典編 = @Sender) - which the empty screen does not suggest. Fix: the Calc at encyclopedia entry
# (00001878 idx 49, `事典2035 = 0`, run on every entry: all callers jump to 00001878:0 -> 44) also rewrites
# 事典編 through nested StringReplace JP -> EN (longest names first, so 真・呪殺編 is not hit by 呪殺編). An English
# value has no Japanese and passes unchanged. The ops run in order (the engine's parser is a linear list of
# named ops, see 000019DD idx 39's DimTo + To); the original assignment stays the last op.
HEN_JP_EN = [  # same pairs as patch/hen-jp-en.tsv, longest Japanese first
    ('真・呪殺編', 'True Jusatsu Arc [Killing by Curse]'), ('真・明徴編', 'True Meicho Arc [Clear Sign]'),
    ('エデンの桜編', "Eden no Sakura Arc [Eden's Cherry]"), ('最後の声編', 'Saigo no Koe Arc [Last Voice]'),
    ('永劫回帰編', 'Eigo Kaiki Arc [Eternal Recurrence]'), ('呪殺編', 'Jusatsu Arc [Killing by Curse]'),
    ('明徴編', 'Meicho Arc [Clear Sign]'), ('詫言編', 'Wabigoto Arc [Apology]'), ('死月編', 'Shigatsu Arc [Death Month]'),
]
HEN_VAR = '事典編'


def hen_normalise(idx, tag, expect='事典2035 = 0'):
    def hook(s):
        from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType
        cmd = s.commands[idx]
        ents = cmd['Calc'].entries
        if any(e.name == HEN_VAR for e in ents):
            print(f'{tag}: 事典編 normalisation at idx {idx} already present')
            return
        if cmd.type.name != 'Calc' or str(cmd['Calc']) != expect:
            sys.exit(f'{tag}: idx {idx} is {cmd.type.name} {cmd["Calc"]}, expected Calc {expect!r}')
        S, V = ParamType.Str, ParamType.Var
        ops, prev, n = [], HEN_VAR, 0
        for jp, en in HEN_JP_EN:
            a, b, r = f'____{n}', f'____{n + 1}', f'____{n + 2}'
            n += 3
            ops += [OpeData(type=OpeDataType.To, name=a, operands=[Param(value=jp, type=S)]),
                    OpeData(type=OpeDataType.To, name=b, operands=[Param(value=en, type=S)]),
                    OpeData(type=OpeDataType.Func, name=r, func=OpeFuncType.StringReplace, operands=[
                        Param(value=prev, type=V), Param(value=a, type=V), Param(value=b, type=V)])]
            prev = r
        ops.append(OpeData(type=OpeDataType.To, name=HEN_VAR, operands=[Param(value=prev, type=V)]))
        cmd['Calc'].entries = ops + list(ents)
        print(f'{tag}: idx {idx} now also normalises 事典編 ({len(HEN_JP_EN)} StringReplace)')
    return hook


# Lane 1, 2026-11-03 follow-up (orchestrator: the encyclopedia's own person name must be English too, key stays JP).
# 00001878 idx 518 "人物テキスト" shows @Sender (the 名前 key) and its text is READ BACK as the key at idx 575, 584,
# 2057, 2066 (DBLocate("名前", GetProp("人物テキスト", 50))), 587 (== "アヴォレ・デュ・ム・モーメン") and 2101
# (VarNew フォーカス人物 InitVal). A separate display caption would need new commands, and inserting commands shifts
# every later index (jumps and handlers address commands by index), so instead: idx 518 prints the 表示名
# (person_caption) and every read-back site maps the caption text back to the key with the same table:
#     GetProp("人物テキスト", 50) -> DBDirectGetStr("人物名簿", "表示名", GetProp("人物テキスト", 50), 0, 0, "名前", <same>)
# 表示名 values are unique; a text that is not a 表示名 ("????" placeholder, the two avatars kept Japanese) comes back
# unchanged, exactly as before. idx 2222 (the "no data for <arc>/<name>" line) prints フォーカス人物 through 表示名.
def _temps_max(ents):
    n = -1
    for e in ents:
        if e.name.startswith('____') and e.name[4:].isdigit():
            n = max(n, int(e.name[4:]))
    return n


def _lookup(start, key_param, keycol, outcol):
    from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType
    S, V = ParamType.Str, ParamType.Var
    a, b, c, d = (f'____{start + i}' for i in range(4))
    ops = [OpeData(type=OpeDataType.To, name=a, operands=[Param(value='人物名簿', type=S)]),
           OpeData(type=OpeDataType.To, name=b, operands=[Param(value=keycol, type=S)]),
           OpeData(type=OpeDataType.To, name=c, operands=[Param(value=outcol, type=S)]),
           OpeData(type=OpeDataType.Func, name=d, func=OpeFuncType.DBDirectGetStr, operands=[
               Param(value=a, type=V), Param(value=b, type=V), Param(value=key_param, type=V),
               Param(value=0, type=ParamType.Flag), Param(value=0, type=ParamType.Flag),
               Param(value=c, type=V), Param(value=key_param, type=V)])]
    return ops, d


def _has_lookup(ents):
    return any(getattr(e.func, 'name', '') == 'DBDirectGetStr' and any(
        getattr(o, 'value', None) == '人物名簿' for x in ents if x.name == e.operands[0].value for o in x.operands)
        for e in ents)


def key_from_display(sites, tag):
    """sites: [(idx, property)]: wrap GetProp("人物テキスト", 50) in the 表示名 -> 名前 lookup."""
    def hook(s):
        from livemaker.lsb.core import OpeFuncType
        for idx, prop in sites:
            parser = s.commands[idx][prop]
            ents = list(parser.entries)
            if _has_lookup(ents):
                print(f'{tag}: key site idx {idx} already fixed')
                continue
            lit = {e.name: e.operands[0].value for e in ents if e.type.name == 'To' and e.operands
                   and getattr(e.operands[0], 'value', None) == '人物テキスト'}
            gp = [k for k, e in enumerate(ents) if e.func == OpeFuncType.GetProp and len(e.operands) == 2
                  and e.operands[0].value in lit and e.operands[1].value == 50]
            if len(gp) != 1:
                sys.exit(f'{tag}: idx {idx} {prop}: expected one GetProp("人物テキスト", 50), found {len(gp)}: {parser}')
            k = gp[0]
            gname = ents[k].name
            new, res = _lookup(_temps_max(ents) + 1, gname, '表示名', '名前')
            for e in ents[k + 1:]:
                for o in e.operands:
                    if getattr(o, 'value', None) == gname:
                        o.value = res
            parser.entries = ents[:k + 1] + new + ents[k + 1:]
            got = str(parser)
            if 'DBDirectGetStr("人物名簿", "表示名", GetProp("人物テキスト", 50), 0, 0, "名前", GetProp("人物テキスト", 50))' not in got:
                sys.exit(f'{tag}: idx {idx} rebuilt as {got}')
            print(f'{tag}: key site idx {idx} reads the key back from the display name')
    return hook


def display_var(sites, tag):
    """sites: [(idx, property, var)]: every operand `var` in that expression -> its 人物名簿 表示名."""
    def hook(s):
        from livemaker.lsb.core import ParamType
        for idx, prop, var in sites:
            parser = s.commands[idx][prop]
            ents = list(parser.entries)
            if _has_lookup(ents):
                print(f'{tag}: display site idx {idx} already fixed')
                continue
            uses = [o for e in ents for o in e.operands if o.type == ParamType.Var and o.value == var]
            if not uses:
                sys.exit(f'{tag}: idx {idx} {prop}: no operand {var}: {parser}')
            new, res = _lookup(_temps_max(ents) + 1, var, '名前', '表示名')
            for o in uses:
                o.value = res
            parser.entries = new + ents
            print(f'{tag}: display site idx {idx}: {parser}')
    return hook
