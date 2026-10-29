"""Guarded expression rewrites shared by patch/fix-0000001C.py, fix-00001CA0.py, fix-00001F8A.py and fix-0000001E.py
(game follow-up r2, 2026-10-30; consumer audit of the English character totals).

Every site names a command index, its command type, the property that holds the expression and the exact ORIGINAL
entry list (as `sig` tuples). The fixed list is computed from that original list, so the script knows both forms:
an original site is rewritten, an already-fixed site is left alone (idempotent), anything else stops the script before
it writes (a re-extracted script, a shifted index, a label map that touched the expression).

sig(entry) = (operator type, result name, function name or None, [(param type, value), ...])
  operator types (pylivemaker OpeDataType): 1 To, 2 Plus, 3 Minus, 4 Mul, 5 Div, 6 Mod, 8 And, 11 Func, 12 Equal,
  13 Big (>), 14 Small (<), 15 EBig (>=), 16 ESmall (<=), 19 ComboStr (++), 20 NEqual (!=);
  param types: 0 Var (a variable or an earlier entry's result), 1 Int, 3 Flag, 4 Str.
Entries run in list order, every one of them (no short-circuit); a later entry reads an earlier one by its name.
"""
import sys

from livemaker.lsb.core import LiveParser, OpeData, OpeDataType, OpeFuncType, Param, ParamType

VAR, INT, STR = int(ParamType.Var), int(ParamType.Int), int(ParamType.Str)
EXPR_KEY = {'If': 'Calc', 'Elseif': 'Calc', 'Calc': 'Calc', 'PropMotion': 'Value'}


def sig(e):
    func = e.func.name if int(e.type) == int(OpeDataType.Func) and e.func is not None else None
    return (int(e.type), e.name, func, [(int(o.type), o.value) for o in e.operands])


def sigs(entries):
    return [sig(e) for e in entries]


def make(s):
    """A new OpeData from a sig tuple."""
    t, name, func, ops = s
    return OpeData(type=t, name=name, func=None if func is None else OpeFuncType[func],
                   operands=[Param(value=v, type=pt) for pt, v in ops])


def V(x):
    return (VAR, x)


def I(x):
    return (INT, x)


def S(x):
    return (STR, x)


def _max_temp(shape):
    out = [int(s[1][4:]) for s in shape if s[1].startswith('____') and s[1][4:].isdigit()]
    return max(out) if out else -1


# ---- R1 "Overall completion": original shapes ---------------------------------------------------------------------
# X = 終了テキスト数 * 1000 / (総テキスト数n / 100), the completion in 0.001 % units (100.000 % = 100000).
# The LiveMaker compiler numbers its temporaries with gaps; the names below are what orig/ holds.
E_DONE, T1, T2 = '終了テキスト数', '総テキスト数1', '総テキスト数2'


def _x(T, nd, nm, nr):
    return [(5, nd, None, [V(T), I(100)]), (4, nm, None, [V(E_DONE), I(1000)]), (5, nr, None, [V(nm), V(nd)])]


def r1_mod_lt(T, k):            # If / Elseif  X % 1000 < k
    return _x(T, '____1', '____3', '____4') + [
        (6, '____5', None, [V('____4'), I(1000)]), (14, '____6', None, [V('____5'), I(k)]),
        (1, '____arg', None, [V('____6')])]


def r1_frac_pad(T, pad, d):     # Calc 進行率小数 = "0" ++ X % 1000 / 10   (pad "00", d 100: the other branch)
    return [(1, '____0', None, [S(pad)])] + _x(T, '____2', '____4', '____5') + [
        (6, '____6', None, [V('____5'), I(1000)]), (5, '____7', None, [V('____6'), I(d)]),
        (19, '____8', None, [V('____0'), V('____7')]), (1, '進行率小数', None, [V('____8')])]


def r1_over(T, cmp):            # If (X > 100000 & 解禁編 < 6)   (cmp 14 <, 15 >=)
    return _x(T, '____1', '____3', '____4') + [
        (13, '____5', None, [V('____4'), I(100000)]), (cmp, '____6', None, [V('解禁編'), I(6)]),
        (8, '____7', None, [V('____5'), V('____6')]), (1, '____arg', None, [V('____7')])]


def r1_frac(T):                 # Calc 進行率小数 = X % 1000
    return _x(T, '____1', '____3', '____4') + [
        (6, '____5', None, [V('____4'), I(1000)]), (1, '進行率小数', None, [V('____5')])]


def r1_whole(T):                # Calc 全体進行率 = X / 1000 ++ "." ++ 進行率小数              (0000001C)
    return [(1, '____0', None, [S('.')])] + _x(T, '____2', '____4', '____6') + [
        (5, '____7', None, [V('____6'), I(1000)]), (19, '____8', None, [V('____7'), V('____0')]),
        (19, '____9', None, [V('____8'), V('進行率小数')]), (1, '全体進行率', None, [V('____9')])]


def r1_whole_pct(T):            # Calc 全体進行率 = X / 1000 ++ "." ++ 進行率小数 ++ "%"       (00001CA0)
    return [(1, '____0', None, [S('.')]), (1, '____1', None, [S('%')])] + _x(T, '____3', '____5', '____7') + [
        (5, '____8', None, [V('____7'), I(1000)]), (19, '____9', None, [V('____8'), V('____0')]),
        (19, '____10', None, [V('____9'), V('進行率小数')]), (19, '____11', None, [V('____10'), V('____1')]),
        (1, '全体進行率', None, [V('____11')])]


def r1_rate(T, var):            # Calc 進行率1 = X                                            (00001CA0)
    return _x(T, '____1', '____3', '____4') + [(1, var, None, [V('____4')])]


# ---- R1 rewrite: the same X without a 32-bit overflow, exact ------------------------------------------------------
# floor(1000 E / D) == (E / D) * 1000 + (E % D) * 1000 / D for E >= 0, D > 0 (E = qD + r, 0 <= r < D). With D = T / 100
# the largest intermediate is (E % D) * 1000 < 1000 D <= 10 T, about 33.4 million for the English T2 (3,333,322),
# while E * 1000 passes 2^31 once E > 2,147,483. Every displayed digit stays exactly what the original computes.
def permille_fixed(shape):
    """Rewrite the one `a = E * 1000; c = a / b` pair (b = T / 100) in `shape`. Returns the new list."""
    mul = [i for i, s in enumerate(shape) if s[0] == 4 and s[3] == [V(E_DONE), I(1000)]]
    if len(mul) != 1:
        raise ValueError('expected one %s * 1000, found %d' % (E_DONE, len(mul)))
    a = shape[mul[0]][1]
    div = [i for i, s in enumerate(shape) if s[0] == 5 and len(s[3]) == 2 and s[3][0] == V(a)]
    if len(div) != 1:
        raise ValueError('expected one (%s) / D' % a)
    c, (bt, b) = shape[div[0]][1], shape[div[0]][3][1]
    dent = [s for s in shape if s[1] == b]
    if bt != VAR or len(dent) != 1 or dent[0][0] != 5 or dent[0][3] not in ([V(T1), I(100)], [V(T2), I(100)]):
        raise ValueError('denominator %s is not T / 100' % b)
    if sum(1 for s in shape for o in s[3] if o == V(a)) != 1:
        raise ValueError('%s is read more than once' % a)
    n = _max_temp(shape) + 1
    q, m1, r, m2, d = ('____%d' % (n + k) for k in range(5))
    new = [(5, q, None, [V(E_DONE), V(b)]),    # q  = E / D
           (4, m1, None, [V(q), I(1000)]),     # m1 = q * 1000
           (6, r, None, [V(E_DONE), V(b)]),    # r  = E % D
           (4, m2, None, [V(r), I(1000)]),     # m2 = r * 1000
           (5, d, None, [V(m2), V(b)]),        # d  = m2 / D
           (2, c, None, [V(m1), V(d)])]        # c  = m1 + d  (same result name: the later entries are unchanged)
    out = []
    for i, s in enumerate(shape):
        if i != mul[0]:
            out.extend(new if i == div[0] else [s])
    return out


# ---- R4: Int() on both sides of a string compare -----------------------------------------------------------------
def int_compare_fixed(shape, op):
    """Wrap both operands of the one compare entry of type `op` in Int(); the two Int entries go right before it."""
    hit = [i for i, s in enumerate(shape) if s[0] == op]
    if len(hit) != 1:
        raise ValueError('expected one compare of type %d, found %d' % (op, len(hit)))
    t, name, func, ops = shape[hit[0]]
    if len(ops) != 2 or ops[0][0] != VAR or ops[1][0] != VAR:
        raise ValueError('compare operands are not names')
    n = _max_temp(shape) + 1
    li, ri = '____%d' % n, '____%d' % (n + 1)
    return (shape[:hit[0]]
            + [(11, li, 'Int', [ops[0]]), (11, ri, 'Int', [ops[1]]), (t, name, func, [V(li), V(ri)])]
            + shape[hit[0] + 1:])


# ---- constant swaps (R6 staff roll, reference bar) ---------------------------------------------------------------
def const_fixed(shape, swaps):
    """swaps = {(entry result name, operand position): (old int, new int)}. Returns the new sig list."""
    out, used = [], set()
    for s in shape:
        ops = list(s[3])
        for pos in range(len(ops)):
            key = (s[1], pos)
            if key in swaps:
                old, new = swaps[key]
                if ops[pos] != I(old):
                    raise ValueError('%s operand %d is %r, expected int %d' % (s[1], pos, ops[pos], old))
                ops[pos] = I(new)
                used.add(key)
        out.append((s[0], s[1], s[2], ops))
    if used != set(swaps):
        raise ValueError('swap targets not found: %r' % sorted(set(swaps) - used))
    return out


# ---- apply -------------------------------------------------------------------------------------------------------
def _rebuild(parser, fixed):
    """Turn parser.entries into `fixed`: an entry that keeps its name, operator, function and operand types only has
    its operand values set in place; everything else is a new OpeData."""
    have = {e.name: e for e in parser.entries}
    new = []
    for s in fixed:
        e = have.get(s[1])
        if e is not None and sig(e)[0] == s[0] and sig(e)[2] == s[2] \
                and [o[0] for o in sig(e)[3]] == [o[0] for o in s[3]]:
            for o, (_, v) in zip(e.operands, s[3]):
                o.value = v
            new.append(e)
        else:
            new.append(make(s))
    parser.entries = new


def apply_sites(script, sites, tag):
    """sites = [(idx, command type, property or None, original sig list, fixed sig list, extra check or None)];
    property None = the usual expression property (If/Elseif/Calc 'Calc', PropMotion 'Value').
    Checks EVERY site first and exits on any mismatch (nothing changed, nothing written); then rewrites the original
    sites and leaves the already-fixed ones alone. Returns (rewritten, already fixed)."""
    plan = []
    for idx, kind, key, orig, fixed, extra in sites:
        if idx >= len(script.commands):
            sys.exit('%s: idx %d out of range (%d commands)' % (tag, idx, len(script.commands)))
        cmd = script.commands[idx]
        if cmd.type.name != kind:
            sys.exit('%s: idx %d is %s, expected %s' % (tag, idx, cmd.type.name, kind))
        if extra is not None:
            msg = extra(cmd)
            if msg:
                sys.exit('%s: idx %d: %s' % (tag, idx, msg))
        k = key or EXPR_KEY.get(kind)
        p = cmd[k] if k in cmd.keys() else None
        if not isinstance(p, LiveParser):
            sys.exit('%s: idx %d has no expression property %s' % (tag, idx, k))
        now = sigs(p.entries)
        if now == fixed:
            plan.append((idx, k, p, None))
        elif now == orig:
            plan.append((idx, k, p, fixed))
        else:
            sys.exit('%s: idx %d %s is neither the original nor the fixed expression: %r' % (tag, idx, k, now))
    done = 0
    for idx, k, p, fixed in plan:
        if fixed is None:
            continue
        _rebuild(p, fixed)
        if sigs(p.entries) != fixed:
            sys.exit('%s: idx %d %s rewrite check failed' % (tag, idx, k))
        done += 1
    return done, len(sites) - done


def obj_is(name, prop):
    """Extra check for a PropMotion: it animates object `name` (with quotes, as str() prints it), property `prop`."""
    def check(cmd):
        got = (str(cmd['ObjName']), str(cmd['ObjProp']))
        return None if got == (name, prop) else 'animates %s/%s, expected %s/%s' % (got + (name, prop))
    return check
