"""TEST BUILD ONLY: build a 000000F2.lsb whose boot dispatcher jumps into an appended test block.

The block (commands cloned from the game's own scripts, Indent 0; GameSave built fresh):

    VarNew ZZ_STATETEST_MARK = <nonce>  Scope 3: proves which save.dat this run wrote
    VarNew ZZ_STATETEST_STEP = 0        Scope 3: progress; 99 = the routine returned
    Call <init page:label> ...          fresh-game init the navigator does on entry (DEFAULT_INIT)
    Calc <var> = <value> ...            one per --set (array cells use the engine's DimTo form)
    Call <page>:<label or index>        the routine under test
    Calc ZZ_STATETEST_STEP = 99
    Call 00001F85.lsb:00001FDC          the game's pre-save DBClearTable(); without it GameSave errors
    Wait 1 / GameSave No=150 "STATETEST" / Wait 1    the game's own save pattern
    Wait 1000 / Terminate

The three boot-dispatcher Jumps (初回起動チェック==0 / 全部了承==0 / else) are retargeted to the block.
They are found by structure. Addresses are 0-based COMMAND INDEXES (README "Addressing").

*** NEVER SHIP THE OUTPUT. It skips the author's notices and the title. ***
"""
import copy
import re
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.command import GameSave
from livemaker.lsb.core import LiveParser, OpeData, OpeDataType, OpeFuncType, Param, ParamType

ROOT = Path(__file__).resolve().parents[3]
ORIG = ROOT / "orig"
MARK = "ZZ_STATETEST_MARK"
STEP = "ZZ_STATETEST_STEP"
DONE = 99
PRESAVE = "00001F85.lsb:00001FDC"   # = idx 204: DBClearTable(), what the game calls before every GameSave
DEFAULT_INIT = ["0000001C.lsb:000024C7", "00001F85.lsb:00001F86"]
SLOT_NO = 150
CAPTION = "STATETEST"

_cache = {}


def load_page(page, game_dir):
    """A page as the engine would load it: loose file in the game folder first, else orig/."""
    loose = Path(game_dir) / page
    src = loose if loose.exists() else ORIG / page
    key = str(src)
    if key not in _cache:
        _cache[key] = LMScript.from_file(str(src))
    return _cache[key], src


def resolve(target, game_dir):
    """'page.lsb:LABELNAME' or 'page.lsb:INDEX' -> (page, index, description)."""
    if ":" not in target:
        raise SystemExit("target must be PAGE.lsb:LABEL_OR_INDEX, got %r" % target)
    page, tok = target.rsplit(":", 1)
    if not page.lower().endswith(".lsb"):
        page += ".lsb"
    lm, src = load_page(page, game_dir)
    cmds = lm.commands
    idx = None
    for i, c in enumerate(cmds):
        if c.type.name == "Label" and str(c.args.get("Name")) == tok:
            idx = i
            break
    if idx is None and tok.isdigit() and int(tok) < len(cmds):
        idx = int(tok)
    if idx is None:
        raise SystemExit("cannot resolve %s in %s (no Label named %r, not an index)" % (target, src, tok))
    c = cmds[idx]
    desc = "%s:%s -> index %d (LineNo %d) %s [%s]" % (page, tok, idx, c.LineNo, str(c)[:60], src)
    if c.type.name != "Label":
        desc += "  WARNING: target is not a Label command"
    return page, idx, desc


SET_RE = re.compile(r"^\s*([^\[\]=\s]+)\s*(?:\[\s*([0-9,\s]+)\s*\])?\s*=\s*(.+?)\s*$")


def value_param(text):
    t = text.strip()
    if len(t) >= 2 and t[0] == t[-1] == '"':
        return Param(value=t[1:-1], type=ParamType.Str)
    if re.fullmatch(r"-?\d+", t):
        return Param(value=int(t), type=ParamType.Int)
    raise SystemExit("--set value must be an integer or a \"quoted string\": %r" % text)


ASSIGN_RE = re.compile(r'^\s*AssignTemp\(\s*"([^"]*)"\s*\)\s*$')
TEMP_RE = re.compile(r"^\s*([^\[\]=\s]+)\s*=\s*@Temp\s*(?:\+\s*(\d+))?\s*$")


def set_parser(assign):
    """'st173=5' or '裏ルート変数[173]=0' -> LiveParser in the engine's own shape.
    Also (2026-11-16, for @Temp probes), same shapes as the game's own commands:
      'AssignTemp("rk118")'   = 0000001E idx 1603 with a literal instead of "rk" ++ ID保存
      'NAME=@Temp'            = 0000001C idx 2713 (`初期ナンバー = @Temp`)
      'NAME=@Temp+100'        = idx 1614 shape (Plus into ____0, then To NAME)
      '@Temp=3'               = plain name form (0000001E idx 1619), already worked."""
    m = ASSIGN_RE.match(assign)
    if m:
        return LiveParser(entries=[
            OpeData(type=OpeDataType.To, name="____0", operands=[Param(value=m.group(1), type=ParamType.Str)]),
            OpeData(type=OpeDataType.Func, name="____1", func=OpeFuncType.AssignTemp,
                    operands=[Param(value="____0", type=ParamType.Var)]),
            OpeData(type=OpeDataType.To, name="____arg", operands=[Param(value="____1", type=ParamType.Var)])])
    m = TEMP_RE.match(assign)
    if m:
        name, add = m.groups()
        if add is None:
            return LiveParser(entries=[OpeData(type=OpeDataType.To, name=name,
                                               operands=[Param(value="@Temp", type=ParamType.Var)])])
        return LiveParser(entries=[
            OpeData(type=OpeDataType.Plus, name="____0",
                    operands=[Param(value="@Temp", type=ParamType.Var), Param(value=int(add), type=ParamType.Int)]),
            OpeData(type=OpeDataType.To, name=name, operands=[Param(value="____0", type=ParamType.Var)])])
    m = SET_RE.match(assign)
    if not m:
        raise SystemExit("bad --set %r (want NAME=VALUE or NAME[i]=VALUE)" % assign)
    name, idx, val = m.groups()
    vp = value_param(val)
    if idx is None:
        # same shape as 000000F2 idx 571 `全部了承 = 1`
        return LiveParser(entries=[OpeData(type=OpeDataType.To, name=name, operands=[vp])])
    ops = [Param(value=name, type=ParamType.Var)]
    ops += [Param(value=int(x), type=ParamType.Int) for x in idx.split(",")]
    # same shape as 0000001C idx 1174 `実況変数[0] = 0`
    return LiveParser(entries=[
        OpeData(type=OpeDataType.DimTo, name="____d_0", operands=ops),
        OpeData(type=OpeDataType.To, name="____d_0", operands=[vp]),
    ])


def first(cmds, typ, pred=lambda c: True):
    for c in cmds:
        if c.type.name == typ and pred(c):
            return c
    raise SystemExit("no %s template found" % typ)


def find_dispatcher(cmds):
    for i in range(len(cmds) - 2):
        a, b, c = cmds[i:i + 3]
        if all(x.type.name == "Jump" for x in (a, b, c)) \
                and "初回起動チェック" in str(a.args.get("Calc")) \
                and "全部了承" in str(b.args.get("Calc")):
            return i
    raise SystemExit("boot dispatcher (3 Jumps: 初回起動チェック / 全部了承 / else) not found in 000000F2.lsb")


def build(game_dir, boot_src, sets, call, nonce, init=None, trace=False, pause_ms=0, from_save=False):
    """Return (lsb bytes, listing lines). from_save (run_state_test --start-save, 2026-11-16): the start save
    already holds MARK and STEP from its own run, and a VarNew may keep an existing value, so both are also SET
    by a Calc right after their VarNew. pause_ms > 0 (debug): a Wait before every block command,
    so the time an engine error dialog appears names the command that raised it."""
    init = DEFAULT_INIT if init is None else init
    boot = LMScript.from_file(str(boot_src))
    cmds = boot.commands
    n0 = len(cmds)
    save_tpl_page = LMScript.from_file(str(ORIG / "00002369.lsb"))

    t_call = first(cmds, "Call", lambda c: len(getattr(c.args.get("Params"), "parsers", [])) == 0)
    t_calc = first(cmds, "Calc")
    t_varnew = first(cmds, "VarNew")
    t_term = first(cmds, "Terminate")
    t_wait = first(cmds, "Wait")
    t_save = first(save_tpl_page.commands, "GameSave")

    lineno = max(c.LineNo for c in cmds) + 1
    new, listing = [], []

    def add(c, note):
        nonlocal lineno
        if pause_ms and c.type.name != "Wait":
            w = copy.deepcopy(t_wait)
            w.args["Calc"], w.args["Time"], w.args["StopEvent"] = lp(1, ParamType.Int), \
                lp(pause_ms, ParamType.Int), lp(0, ParamType.Int)
            add_raw(w, "pause %d ms (debug)" % pause_ms)
        add_raw(c, note)

    def add_raw(c, note):
        nonlocal lineno
        listing.append("000000F2.lsb idx %d  %-9s %s  [mute=%s]" % (n0 + len(new), c.type.name, note, c.Mute))
        c.Indent = 0
        c.LineNo = lineno
        lineno += 1
        new.append(c)

    assert "Int" in str(t_varnew.args["Type"]) or int(t_varnew.args["Type"]) == int(ParamType.Int), \
        "VarNew template is not Type=Int: %r" % t_varnew.args["Type"]

    def lp(value, ptype):
        return LiveParser(entries=[OpeData(type=OpeDataType.To, name="____arg",
                                           operands=[Param(value=value, type=ptype)])])

    def varnew(name, value):
        c = copy.deepcopy(t_varnew)
        c.args["Name"], c.args["Scope"], c.args["InitVal"] = name, 3, lp(value, ParamType.Int)
        add(c, "mark  " + str(c))

    def wait(ms):
        c = copy.deepcopy(t_wait)
        c.args["Calc"], c.args["Time"], c.args["StopEvent"] = lp(1, ParamType.Int), lp(ms, ParamType.Int), \
            lp(0, ParamType.Int)
        add(c, "wait  %d ms" % ms)

    def gamesave():
        # The game wraps every GameSave in `Wait Time=1` (0000001C idx 4330/4332, 0000227A 167/170).
        # Built fresh, not cloned: pylivemaker 1.2.1 GameSave.__init__ assigns the parsed Caption to
        # `No` (typo), so a parsed GameSave keeps a raw Container caption and cannot be re-serialized.
        # Same field shapes as the game's autosave, 00002369.lsb idx 9 (No=150, Page "", Label 0).
        # The game also runs `Call 00001F85.lsb:204` (Label 00001FDC, DBClearTable() on the active
        # table) before every save (00002369 idx 7, 0000001C idx 4329, 0000227A idx 164). Without it
        # the save raised an engine error dialog (run 20261116 T0pause: dialog in the GameSave slot).
        page, idx, desc = resolve(PRESAVE, game_dir)
        c = copy.deepcopy(t_call)
        c.args["Page"].Page, c.args["Page"].Label = page, idx
        add(c, "pre-save " + desc)
        wait(1)
        cap = LiveParser(entries=[      # same 2-entry shape as every caption in the game
            OpeData(type=OpeDataType.To, name="____0", operands=[Param(value=CAPTION, type=ParamType.Str)]),
            OpeData(type=OpeDataType.To, name="____arg", operands=[Param(value="____0", type=ParamType.Var)])])
        c = GameSave(No=lp(SLOT_NO, ParamType.Int), Page=str(t_save.args.get("Page") or ""), Label=0,
                     Caption=cap)
        add(c, "save  " + str(c))
        wait(1)

    def step(k):
        c = copy.deepcopy(t_calc)
        c.args["Calc"] = set_parser("%s=%d" % (STEP, k))
        add(c, "step  %s = %d" % (STEP, k))
        if trace:
            gamesave()

    varnew(MARK, nonce)          # first: every save.dat written from here on carries this run's nonce
    varnew(STEP, 0)
    if from_save:
        for name, value in ((MARK, nonce), (STEP, 0)):
            c = copy.deepcopy(t_calc)
            c.args["Calc"] = set_parser("%s=%d" % (name, value))
            add(c, "mark  %s = %d (Calc: the start save already has it)" % (name, value))
    if trace:
        gamesave()
    k = 0
    for tgt in init:
        page, idx, desc = resolve(tgt, game_dir)
        c = copy.deepcopy(t_call)
        c.args["Page"].Page, c.args["Page"].Label = page, idx
        add(c, "init  " + desc)
        k += 1
        step(k)
    for s in sets:
        c = copy.deepcopy(t_calc)
        c.args["Calc"] = set_parser(s)
        add(c, "set   %s   (engine form: %s)" % (s, safe_str(c)))
    if sets:
        k += 1
        step(k)
    page, idx, desc = resolve(call, game_dir)
    c = copy.deepcopy(t_call)
    c.args["Page"].Page, c.args["Page"].Label = page, idx
    add(c, "call  " + desc)
    c = copy.deepcopy(t_calc)
    c.args["Calc"] = set_parser("%s=%d" % (STEP, DONE))
    add(c, "step  %s = %d (done)" % (STEP, DONE))
    gamesave()
    wait(1000)
    add(copy.deepcopy(t_term), "quit")
    listing.append("steps: 0 = block reached, 1..%d = after each init Call%s, %d = routine returned"
                   % (len(init), ", %d = after the sets" % k if sets else "", DONE))

    d = find_dispatcher(cmds)
    for j in range(d, d + 3):
        r = cmds[j].args["Page"]
        listing.insert(j - d, "000000F2.lsb idx %d  Jump      %s:%s -> 000000F2.lsb:%d  (if %s)"
                       % (j, r.Page, r.Label, n0, cmds[j].args.get("Calc")))
        r.Page, r.Label = "000000F2.lsb", n0
    cmds.extend(new)
    data = boot.to_lsb()

    # self-check: re-parse, old commands unchanged except the 3 jumps, new block as built
    # bytes: the original file is a prefix of the output except the command-count u32 and the
    # three Jump label u32s (<= 16 bytes); everything after it is the appended block.
    orig = Path(boot_src).read_bytes()
    ndiff = sum(1 for x, y in zip(orig, data) if x != y)
    assert len(data) > len(orig) and ndiff <= 16, "byte check: %d bytes differ in the original span" % ndiff
    chk = LMScript.from_lsb(data)
    assert len(chk.commands) == n0 + len(new), "command count after re-parse"
    for j in range(d, d + 3):
        r = chk.commands[j].args["Page"]
        assert (r.Page, r.Label) == ("000000F2.lsb", n0), "jump %d after re-parse: %s" % (j, r)
    for k, c in enumerate(new):
        r = chk.commands[n0 + k]
        if c.type.name == "GameSave":   # re-parse leaves Caption a raw Container (same pylivemaker typo)
            cap = r.args["Caption"]
            cap = LiveParser.from_struct(cap) if not isinstance(cap, LiveParser) else cap
            got = (str(r.args["No"]), r.args["Page"], r.args["Label"], str(cap))
            want = (str(c.args["No"]), c.args["Page"], c.args["Label"], str(c.args["Caption"]))
            assert got == want, "GameSave after re-parse: %s != %s" % (got, want)
            continue
        assert safe_str(r) == safe_str(c), "appended cmd %d differs after re-parse" % k
    listing.append("self-check: %d original commands; %d bytes differ inside the original %d bytes "
                   "(count + 3 jump targets); re-parse OK; %d commands appended"
                   % (n0, ndiff, len(orig), len(new)))
    return data, listing


def safe_str(c):
    try:
        return str(c)
    except Exception:       # pylivemaker's numpy constant fold can raise inside __str__
        return c.type.name + " <unprintable>"
