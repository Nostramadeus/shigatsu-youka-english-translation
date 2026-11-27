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


ROOM = 600   # header B / B2 start at x 350 (履歴座標), screen edge 960 -> 610 px; 10 px margin


def split_entries(existing, obj, room=ROOM):
    """2026-11-27 (friend report: chatter question 318 cut off at the right edge; 39 of 476 questions are wider than
    610 px at ＭＳ Ｐ明朝 20 bold). Entries that, when the Caption `obj` is wider than `room`, replace the first space
    after the middle of its text with CR LF (two lines); otherwise they set the same text back. No loop, no text change
    in the tables, works for any text (player nickname included). Prepended to an expression that runs right after the
    Caption is created; the expression's own GetProp(obj, 6) then reads the new height.
        t = GetProp(obj, 50); h = Int(JLength(t) / 2); p = JPos(" ", JCopy(t, h + 1, 9999)); bp = h + p
        n = Min(1, Max(0, GetProp(obj, 5) - room)) * Min(1, p)
        q = bp * n + (JLength(t) + 1) * (1 - n)        (n = 0: q is past the end, so the text comes back whole)
        SetProp(obj, 50, JCopy(t, 1, q - 1) ++ JCopy(CR LF, 3 - 2 * n, 2) ++ JCopy(t, q + n, 9999))
    Engine fact (test 2026-11-27, work/bugs-2026-11-27/chatter-header): JCopy with count 0 returns the WHOLE rest,
    not "", so no JCopy here may get count 0 for a non-empty string; start positions past the end give ""."""
    b = _B(existing)
    o = b.s(obj)
    w = b.f(F.GetProp, V(o), I(5))
    t = b.f(F.GetProp, V(o), I(50))
    L = b.f(F.JLength, V(t))
    h = b.f(F.Int, V(b.add(T.Div, [V(L), I(2)])))
    p = b.f(F.JPos, V(b.s(' ')), V(b.f(F.JCopy, V(t), V(b.plus(V(h), I(1))), I(9999))))
    bp = b.plus(V(h), V(p))
    over = b.f(F.Min, I(1), V(b.f(F.Max, I(0), V(b.add(T.Minus, [V(w), I(room)])))))
    n = b.mul(V(over), V(b.f(F.Min, I(1), V(p))))
    keep = b.add(T.Minus, [I(1), V(n)])
    q = b.plus(V(b.mul(V(bp), V(n))), V(b.mul(V(b.plus(V(L), I(1))), V(keep))))
    head = b.f(F.JCopy, V(t), I(1), V(b.add(T.Minus, [V(q), I(1)])))
    brk = b.f(F.JCopy, V(_crlf(b)), V(b.plus(I(1), V(b.mul(I(2), V(keep))))), I(2))
    tail = b.f(F.JCopy, V(t), V(b.plus(V(q), V(n))), I(9999))
    b.f(F.SetProp, V(o), I(50), V(b.cat(b.cat(head, brk), tail)))
    return b.e


def join_squeeze_entries(existing, obj, room=ROOM, line=None, line_base=None):
    """2026-11-27: keep the header stack inside the title bar (gauge 雑談ゲージ starts at y 57 = title height, 0000189A
    316) once header B2 is shown. Entries: CR LF in the text of `obj` -> one space (one line again), then width =
    Min(width, room) (the engine squeezes a Caption into a set width, W-FACTS A1). With `line`: that underline's TOP =
    line_base + GetProp(obj, 6).
        SetProp(obj, 50, StringReplace(GetProp(obj, 50), CR LF, " ")); SetProp(obj, 5, Min(GetProp(obj, 5), room))"""
    b = _B(existing)
    o = b.s(obj)
    b.f(F.SetProp, V(o), I(50), V(b.f(F.StringReplace, V(b.f(F.GetProp, V(o), I(50))), V(_crlf(b)), V(b.s(' ')))))
    b.f(F.SetProp, V(o), I(5), V(b.f(F.Min, V(b.f(F.GetProp, V(o), I(5))), I(room))))
    if line:
        b.f(F.SetProp, V(b.s(line)), I(4), V(b.plus(V(b.f(F.GetProp, V(o), I(6))), I(line_base))))
    return b.e


def _has_split(lp):
    return any(e.func == F.SetProp for e in lp.entries)


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
    # 2026-11-27 (work/bugs-2026-11-27/chatter-header): header B alone = two lines when too wide (280, right after
    # B is made). When B2 is made (248) B goes back to one line squeezed to ROOM and its underline 項目線 back up;
    # B2 itself is one line squeezed to ROOM (249). The stack then ends at y ~50 like the Japanese, above the gauge.
    for idx, obj, make in ((280, '選択項目', lambda e: split_entries(e, '選択項目')),
                           (248, '選択項目2', lambda e: join_squeeze_entries(e, '選択項目', line='項目線', line_base=7)),
                           (249, '選択項目2', lambda e: join_squeeze_entries(e, '選択項目2'))):
        lp = C[idx]['PR_TOP']
        if _has_split(lp):
            done.append('%d header fit already' % idx)
        else:
            lp.entries = make(lp.entries) + lp.entries
            done.append('%d header fit' % idx)
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
