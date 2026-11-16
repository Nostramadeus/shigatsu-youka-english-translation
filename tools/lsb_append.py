"""Checked renames, ONE command block appended at the END of an LSB, and Jumps retargeted into it.

    uv run --no-project --with pylivemaker python tools/lsb_append.py IN.lsb OUT.lsb SPEC.tsv

Run by tools/compile_en.sh as its LAST step when patch/append-<id>.tsv exists (EN trees only).
Why append: Jump/Call targets are COMMAND INDEXES (other pages, saves), so an inserted command would shift every
later index. Appending keeps every existing index: one existing Jump is retargeted to the block and the block ends
with the Jump it replaced (same technique as tools/harness/state/inject.py). First use: patch/append-0000001C.tsv
(rk119 fix, 2026-11-16).

SPEC (UTF-8, TAB-separated, # comments, no header):
    rename    IDX  CMDTYPE  ARG  OLD  NEW     a plain string argument (VarNew Name); OLD must match
    retarget  IDX  PAGE:LABEL                 the Jump at IDX must point at PAGE:LABEL now; afterwards at the block
    cmd       INDENT  CMDTYPE  [EXPR]  [PAGE:LABEL]
              one appended command, in order; INDENT is added to the Indent of the first retargeted command.
              If / Elseif: EXPR = condition.  Else: nothing.  Calc: `NAME = EXPR`.  Jump: condition + PAGE:LABEL.
EXPR: integers, "strings", Flag(n) (a Flag-typed literal: the compiler types `== 1` against a Flag variable or
VarExists() that way), names (@Temp too), NAME[i][j] array reads, Func(args) (any OpeFuncType name), operators
| & == != > < >= <= + - ++ and parentheses. Precedence: | lowest, then &, then comparisons, then + - ++.
Compiled to the engine's temporary form: `____n` per step, `____d_n` for an array read (DimTo), each string
literal in its own `To ____n`, `To ____arg` last (the shapes of 0000001C idx 5892 / 0000001E idx 1239, 1613).
Any mismatch (index, type, old value, current target) -> exit 1, nothing written. A file the spec was already
applied to fails the same way (its retarget no longer points at the old target).
Self-check before writing: the input is a byte prefix of the output except the command count, the renamed
bytes and the retargeted labels (<= 32 bytes differ); the output re-parses with input count + block length,
renamed / retargeted values as set, every appended command as built.
"""
import copy
import re
import sys
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.core import LiveParser, OpeData, OpeDataType, OpeFuncType, Param, ParamType

OPS = {'|': OpeDataType.Or, '&': OpeDataType.And, '==': OpeDataType.Equal, '!=': OpeDataType.NEqual,
       '>': OpeDataType.Big, '<': OpeDataType.Small, '>=': OpeDataType.EBig, '<=': OpeDataType.ESmall,
       '+': OpeDataType.Plus, '-': OpeDataType.Minus, '++': OpeDataType.ComboStr}
TOK = re.compile(r'\s*(?:(?P<num>\d+)(?![^\s|&><+\-()\[\],="!])|(?P<str>"[^"]*")'
                 r'|(?P<op>\+\+|==|!=|>=|<=|[|&><+\-()\[\],=])|(?P<name>[^\s|&><+\-()\[\],="!]+))')


def tokens(text):
    out, pos = [], 0
    text = text.strip()
    while pos < len(text):
        m = TOK.match(text, pos)
        if not m or m.end() == pos:
            raise ValueError('cannot read %r at %d' % (text, pos))
        pos = m.end()
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
    return out


class Parser:
    def __init__(self, text):
        self.t, self.i = tokens(text), 0

    def peek(self, *ops):
        return self.i < len(self.t) and self.t[self.i][0] == 'op' and self.t[self.i][1] in ops

    def take(self, op):
        if not self.peek(op):
            raise ValueError('expected %r at token %d of %r' % (op, self.i, self.t))
        self.i += 1

    def done(self):
        if self.i != len(self.t):
            raise ValueError('trailing tokens %r' % self.t[self.i:])

    def binary(self, ops, sub, once=False):
        node = sub()
        while self.peek(*ops):
            op = self.t[self.i][1]
            self.i += 1
            node = ('bin', op, node, sub())
            if once:
                break
        return node

    def expr(self):
        return self.binary(('|',), lambda: self.binary(('&',), self.cmp))

    def cmp(self):
        return self.binary(('==', '!=', '>=', '<=', '>', '<'), self.add, once=True)

    def add(self):
        return self.binary(('+', '-', '++'), self.prim)

    def prim(self):
        if self.peek('('):
            self.take('(')
            node = self.expr()
            self.take(')')
            return node
        kind, val = self.t[self.i]
        self.i += 1
        if kind == 'num':
            return ('int', int(val))
        if kind == 'str':
            return ('str', val[1:-1])
        if kind != 'name':
            raise ValueError('unexpected %r' % val)
        if self.peek('('):
            self.take('(')
            args = []
            while not self.peek(')'):
                args.append(self.expr())
                if self.peek(','):
                    self.take(',')
            self.take(')')
            if val == 'Flag':
                if len(args) != 1 or args[0][0] != 'int':
                    raise ValueError('Flag() takes one integer')
                return ('flag', args[0][1])
            if val not in OpeFuncType.__members__:
                raise ValueError('unknown function %s' % val)
            return ('func', val, args)
        idx = []
        while self.peek('['):
            self.take('[')
            idx.append(self.expr())
            self.take(']')
        return ('dim', val, idx) if idx else ('var', val)


class Emit:
    def __init__(self):
        self.ents, self.k = [], 0

    def tmp(self, prefix='____'):
        self.k += 1
        return '%s%d' % (prefix, self.k - 1)

    def add(self, typ, name, ops, func=None):
        kw = dict(type=typ, name=name, operands=ops)
        if func is not None:
            kw['func'] = func
        self.ents.append(OpeData(**kw))
        return Param(value=name, type=ParamType.Var)

    def val(self, n):
        kind = n[0]
        if kind == 'int':
            return Param(value=n[1], type=ParamType.Int)
        if kind == 'flag':
            return Param(value=n[1], type=ParamType.Flag)
        if kind == 'var':
            return Param(value=n[1], type=ParamType.Var)
        if kind == 'str':
            return self.add(OpeDataType.To, self.tmp(), [Param(value=n[1], type=ParamType.Str)])
        if kind == 'dim':
            ops = [Param(value=n[1], type=ParamType.Var)] + [self.val(x) for x in n[2]]
            return self.add(OpeDataType.DimTo, self.tmp('____d_'), ops)
        if kind == 'func':
            args = [self.val(x) for x in n[2]]
            return self.add(OpeDataType.Func, self.tmp(), args, func=OpeFuncType[n[1]])
        left, right = self.val(n[2]), self.val(n[3])
        return self.add(OPS[n[1]], self.tmp(), [left, right])


def condition(text):
    p = Parser(text)
    root = p.expr()
    p.done()
    e = Emit()
    v = e.val(root)
    e.ents.append(OpeData(type=OpeDataType.To, name='____arg', operands=[v]))
    return LiveParser(entries=e.ents)


def assignment(text):
    p = Parser(text)
    kind, name = p.t[0]
    if kind != 'name' or not (len(p.t) > 2 and p.t[1] == ('op', '=')):
        raise ValueError('Calc wants NAME = EXPR, got %r' % text)
    p.i = 2
    root = p.expr()
    p.done()
    e = Emit()
    v = e.val(root)
    e.ents.append(OpeData(type=OpeDataType.To, name=name, operands=[v]))
    return LiveParser(entries=e.ents)


def target(text):
    page, label = text.rsplit(':', 1)
    return page, int(label)


def safe_str(c):
    try:
        return str(c)
    except Exception:
        return c.type.name + ' <unprintable>'


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, dst, spec = Path(argv[0]), Path(argv[1]), Path(argv[2])
    orig = src.read_bytes()
    lm = LMScript.from_lsb(orig)
    cmds = lm.commands
    n0 = len(cmds)
    renames, retargets, block, bad = [], [], [], []
    for ln, line in enumerate(spec.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        p = line.split('\t')
        try:
            if p[0] == 'rename':
                renames.append((int(p[1]), p[2], p[3], p[4], p[5]))
            elif p[0] == 'retarget':
                retargets.append((int(p[1]), target(p[2])))
            elif p[0] == 'cmd':
                indent, typ = int(p[1]), p[2]
                expr = p[3] if len(p) > 3 else ''
                to = target(p[4]) if len(p) > 4 and p[4].strip() else None
                if typ in ('If', 'Elseif', 'Jump'):
                    calc = condition(expr)
                elif typ == 'Calc':
                    calc = assignment(expr)
                elif typ == 'Else':
                    calc = None
                else:
                    raise ValueError('cmd type %s not supported' % typ)
                if (typ == 'Jump') != (to is not None):
                    raise ValueError('a Jump needs PAGE:LABEL, nothing else takes one')
                block.append((indent, typ, expr, calc, to))
            else:
                raise ValueError('unknown row kind %r' % p[0])
        except (ValueError, IndexError, KeyError) as ex:
            bad.append('spec line %d: %s' % (ln, ex))
    for idx, typ, arg, old, new in renames:
        c = cmds[idx] if idx < n0 else None
        if c is None or c.type.name != typ or str(c.args.get(arg)) != old or len(new.encode('cp932')) != len(old.encode('cp932')):
            bad.append('rename idx %d: want %s %s=%r (same byte length as %r), found %s'
                       % (idx, typ, arg, old, new, safe_str(c) if c is not None else 'no such index'))
    for idx, (page, label) in retargets:
        c = cmds[idx] if idx < n0 else None
        r = c.args.get('Page') if c is not None and c.type.name == 'Jump' else None
        if r is None or (r.Page, r.Label) != (page, label):
            bad.append('retarget idx %d: want Jump %s:%d, found %s (already applied?)'
                       % (idx, page, label, safe_str(c) if c is not None else 'no such index'))
    if not retargets or not block:
        bad.append('spec needs at least one retarget row and one cmd row')
    if bad:
        print('\n'.join(bad), file=sys.stderr)
        print('%d PROBLEMS, nothing written' % len(bad), file=sys.stderr)
        return 1

    base = cmds[retargets[0][0]].Indent
    lineno = max(c.LineNo for c in cmds) + 1
    tpl = {}
    new = []
    for indent, typ, expr, calc, to in block:
        if typ not in tpl:
            tpl[typ] = next((c for c in cmds if c.type.name == typ), None)
            if tpl[typ] is None:
                print('no %s command in %s to copy' % (typ, src), file=sys.stderr)
                return 1
        c = copy.deepcopy(tpl[typ])
        if calc is not None:
            c.args['Calc'] = calc
        if to is not None:
            c.args['Page'].Page, c.args['Page'].Label = to
        c.Indent, c.LineNo, c.Mute = base + indent, lineno, False
        lineno += 1
        new.append(c)
    for idx, typ, arg, old, nv in renames:
        cmds[idx].args[arg] = nv
        print('rename   idx %d %s %s %s -> %s' % (idx, typ, arg, old, nv))
    for idx, (page, label) in retargets:
        cmds[idx].args['Page'].Label = n0
        print('retarget idx %d Jump %s:%d -> %s:%d' % (idx, page, label, page, n0))
    cmds.extend(new)
    data = lm.to_lsb()

    ndiff = sum(1 for x, y in zip(orig, data) if x != y)
    assert len(data) > len(orig) and ndiff <= 32, 'byte check: %d bytes differ inside the original span' % ndiff
    chk = LMScript.from_lsb(data)
    assert len(chk.commands) == n0 + len(new), 'command count after re-parse'
    for idx, typ, arg, old, nv in renames:
        assert str(chk.commands[idx].args[arg]) == nv, 'rename idx %d after re-parse' % idx
    for idx, (page, label) in retargets:
        r = chk.commands[idx].args['Page']
        assert (r.Page, r.Label) == (page, n0), 'retarget idx %d after re-parse' % idx
    for k, c in enumerate(new):
        r = chk.commands[n0 + k]
        assert (safe_str(r), r.Indent, r.type.name) == (safe_str(c), c.Indent, c.type.name), 'appended %d' % k
        print('append   idx %d indent %d  %s' % (n0 + k, r.Indent, safe_str(r)))
    dst.write_bytes(data)
    print('wrote %s: %d commands kept, %d appended at idx %d-%d, %d bytes differ inside the original %d bytes'
          % (dst, n0, len(new), n0, n0 + len(new) - 1, ndiff, len(orig)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
