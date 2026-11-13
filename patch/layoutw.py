"""Lane W 2026-11-14: layout of long English reply captions in the chatter screen (work/layout/W-FACTS.md, P1 + P2).
The 27 reply captions wider than the 530 px button room carry the two-character marker backslash-n in the table
(tsv-en/雑談リスト*.tsv). Engine proof (work/layout/shots/run1/012.png): a Caption breaks at Chr(13) ++ Chr(10),
never at the marker itself, and a Caption never wraps by width.
fix_18bf (called by patch/fix-000018BF.py):
  299 SetProp Value: StringReplace(<old>, "\\n", Chr(13) ++ Chr(10))            -> two-line button
  291 VarNew Y座標 InitVal: 22 -> SPACING (see below)                            -> button pitch
  298 Caption PR_TOP: 250 + 番号 * Y座標 -> 200 + 番号 * Y座標
  280 項目線 PR_TOP: 27 -> 7 + GetProp("選択項目", 6)                            -> header B may have 2 lines
  248 選択項目2 PR_TOP: 30 -> 10 + GetProp("選択項目", 6); PR_FONTHEIGHT 20 -> 18
  249 項目線2 PR_TOP: 52 -> GetProp("選択項目2", 4) + GetProp("選択項目2", 6) + 2
fix_189a (called by patch/fix-0000189A.py): idx 958/960 (info list) and 1437/1439 (choice info) wrap the
  DBGetStr("キャプション" ++ ...) of the "You:" line in StringReplace(.., "\\n", Chr(13) ++ Chr(10) ++ indent).
Every site is checked by structure; a second run reports "already fixed" and changes nothing."""
import re
from livemaker.lsb.core import OpeData, OpeDataType as T, Param, ParamType as P, OpeFuncType as F

MARK = '\\n'             # the two characters backslash + n, as stored in the table cells
# 'expr' = 22 + 20 * Min(1, JPos(MARK, cap2) + ... + JPos(MARK, cap5)) FAILED its harness proof (work/layout/shots/round2/
# run1/014.png: a row with four two-line captions still got pitch 22), so the coordinator's fallback ships the plain 42.
SPACING = 42


class _B:
    """Appends OpeData entries with fresh temp names (after the highest ____N already in the expression)."""
    def __init__(self, entries):
        nums = [int(m.group(1)) for e in entries for m in [re.match(r'^____(\d+)$', e.name or '')] if m]
        self.n = max(nums, default=0) + 100
        self.e = []

    def t(self):
        self.n += 1
        return '____%d' % self.n

    def add(self, typ, ops, func=None):
        name = self.t()
        self.e.append(OpeData(type=typ, name=name, operands=ops, func=func) if func is not None
                      else OpeData(type=typ, name=name, operands=ops))
        return name

    def s(self, v): return self.add(T.To, [Param(v, P.Str)])
    def f(self, fn, *ops): return self.add(T.Func, list(ops), fn)
    def cat(self, a, b): return self.add(T.ComboStr, [Param(a, P.Var), Param(b, P.Var)])
    def plus(self, a, b): return self.add(T.Plus, [a, b])
    def mul(self, a, b): return self.add(T.Mul, [a, b])


def V(x): return Param(x, P.Var)
def I(x): return Param(x, P.Int)


def _arg(entries):
    last = entries[-1]
    assert last.name == '____arg' and last.type == T.To and len(last.operands) == 1, 'no ____arg'
    return last


def _crlf(b, tail=''):
    x = b.cat(b.f(F.Chr, I(13)), b.f(F.Chr, I(10)))
    return b.cat(x, b.s(tail)) if tail else x


def _wrap_replace(entries, src, tail):
    """Insert StringReplace(src, MARK, CR LF ++ tail) right after the entry named src; later readers of src read it."""
    pos = next(i for i, e in enumerate(entries) if e.name == src)
    b = _B(entries)
    new = b.f(F.StringReplace, V(src), V(b.s(MARK)), V(_crlf(b, tail)))
    for e in entries[pos + 1:]:
        for o in e.operands:
            if o.type == P.Var and o.value == src:
                o.value = new
    entries[pos + 1:pos + 1] = b.e


def _has_mark(lp):
    return any(o.type == P.Str and o.value == MARK for e in lp.entries for o in e.operands)


def _name(c):
    return str(c['Name']).strip('"')


def _set(lp, entries):
    lp.entries = entries


def _expr_top(base, objs):
    """base + GetProp(obj, prop) + ... as a fresh entry list."""
    b = _B([])
    acc = None
    for obj, prop in objs:
        g = b.f(F.GetProp, V(b.s(obj)), I(prop))
        acc = g if acc is None else b.plus(V(acc), V(g))
    acc = b.plus(V(acc), I(base))
    return b.e + [OpeData(type=T.To, name='____arg', operands=[V(acc)])]


def _int_only(lp):
    e = lp.entries
    if len(e) == 1 and e[0].name == '____arg' and len(e[0].operands) == 1 and e[0].operands[0].type == P.Int:
        return e[0].operands[0].value
    return None


def fix_18bf(s, tag='fix-000018BF W'):
    C = s.commands
    done = []
    # 299: two-line buttons
    c = C[299]
    assert c.type.name == 'SetProp' and '選択肢' in str(c['ObjName']) and '/立木/' in str(c['Value']), '299 shape'
    if _has_mark(c['Value']):
        done.append('299 already')
    else:
        _wrap_replace(c['Value'].entries, _arg(c['Value'].entries).operands[0].value, '')
        done.append('299 StringReplace')
    # 291: pitch
    c = C[291]
    assert c.type.name == 'VarNew' and str(c['Name']).strip('"') == 'Y座標', '291 shape'
    lp = c['InitVal']
    v = _int_only(lp)
    if v == 22:
        if SPACING == 'expr':
            b = _B([])
            acc = None
            for k in (2, 3, 4, 5):
                j = b.f(F.JPos, V(b.s(MARK)), V(b.f(F.DBGetStr, V(b.s('キャプション%d' % k)))))
                acc = j if acc is None else b.plus(V(acc), V(j))
            m = b.f(F.Min, I(1), V(acc))
            r = b.plus(I(22), V(b.mul(I(20), V(m))))
            _set(lp, b.e + [OpeData(type=T.To, name='____arg', operands=[V(r)])])
        else:
            lp.entries[0].operands[0].value = int(SPACING)
        done.append('291 -> %s' % SPACING)
    else:
        assert v == SPACING or (v is None and _has_mark(lp)), '291 unexpected %r' % v
        done.append('291 already')
    # 298: base 250 -> 200
    c = C[298]
    assert c.type.name == 'Caption' and '選択肢' in str(c['Name']) and 'Y座標' in str(c['PR_TOP']), '298 shape'
    ints = [o for e in c['PR_TOP'].entries for o in e.operands if o.type == P.Int and o.value in (250, 200)]
    assert len(ints) == 1, '298 PR_TOP ints %d' % len(ints)
    done.append('298 already' if ints[0].value == 200 else '298 250->200')
    ints[0].value = 200
    # 280 / 248 / 249: header lines follow the height of header B
    for idx, typ, nm, old, objs, base in ((280, 'BoxNew', '項目線', 27, [('選択項目', 6)], 7),
                                          (248, 'Caption', '選択項目2', 30, [('選択項目', 6)], 10),
                                          (249, 'BoxNew', '項目線2', 52, [('選択項目2', 4), ('選択項目2', 6)], 2)):
        c = C[idx]
        assert c.type.name == typ and _name(c) == nm, '%d shape' % idx
        v = _int_only(c['PR_TOP'])
        if v == old:
            _set(c['PR_TOP'], _expr_top(base, objs))
            done.append('%d PR_TOP %d->expr' % (idx, old))
        else:
            assert v is None and 'GetProp' in str(c['PR_TOP']), '%d PR_TOP unexpected' % idx
            done.append('%d already' % idx)
    lp = C[248]['PR_FONTHEIGHT']
    v = _int_only(lp)
    assert v in (20, 18), '248 font %r' % v
    done.append('248 font already' if v == 18 else '248 font 20->18')
    lp.entries[0].operands[0].value = 18
    print('%s: %s' % (tag, '; '.join(done)))


def fix_189a(s, tag='fix-0000189A W'):
    C = s.commands
    done = []
    for idx, tail in ((958, '　　     '), (960, '　　     '), (1437, '     '), (1439, '     ')):
        lp = C[idx]['Calc']
        assert C[idx].type.name == 'Calc' and 'You: ' in str(lp), '%d shape' % idx
        if _has_mark(lp):
            done.append('%d already' % idx); continue
        E = lp.entries
        by = {e.name: e for e in E}
        hits = []
        for e in E:
            if e.func != F.DBGetStr or len(e.operands) != 1 or e.operands[0].type != P.Var:
                continue
            k = by.get(e.operands[0].value)
            if k is None or k.type != T.ComboStr:
                continue
            h = by.get(k.operands[0].value) if k.operands[0].type == P.Var else None
            if h is not None and h.type == T.To and h.operands[0].type == P.Str and h.operands[0].value == 'キャプション':
                hits.append(e.name)
        assert len(hits) == 1, '%d: %d caption reads' % (idx, len(hits))
        _wrap_replace(E, hits[0], tail)
        done.append('%d StringReplace' % idx)
    print('%s: %s' % (tag, '; '.join(done)))
