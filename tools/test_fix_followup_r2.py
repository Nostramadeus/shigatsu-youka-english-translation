"""Tests for the game follow-up r2 script fixes (2026-10-30, consumer audit of the English character totals):

  R1  0000001C + 00001CA0  "Overall completion" E * 1000 / (T / 100) rewritten without the 32-bit overflow, exact
  R4  0000001C             Int() on both sides of the three `ナビ文字数 <= JCopy(ナビ文字数2, 2)` string compares
  R6  00001F8A             staff roll (scene 313) step 100 -> 220 characters, show/fade point 60 -> 132
  REF 0000001E             reference viewer length bar 200000 -> 500000, alpha 2000 -> 5000

Each patch/fix-<id>.py runs on a COPY of orig/<id>.lsb and of work/<id>.lsb in a C: scratch folder (work/ and game/ are
never written). Checked: the expression after the fix (independently of the fix code: an evaluator over the entry list
and pylivemaker's own rendering), a second run is byte-identical, and a changed expression is refused with nothing written.

    cd F:/Projects/shigatsu-youka-en
    PYTHONUTF8=1 uv run --no-project --python 3.12 --with pylivemaker python tools/test_fix_followup_r2.py
"""
import random
import re
import runpy
import shutil
import tempfile
import sys
import unittest
from pathlib import Path

from livemaker.lsb import LMScript

ROOT = Path(__file__).resolve().parents[1]
SCRATCH = Path(tempfile.gettempdir()) / 'shigatsu-r2-testcopies'
sys.path.insert(0, str(ROOT / 'patch'))
from exprfix import EXPR_KEY, sig  # noqa: E402

R1_1C = [3732, 3734, 3736, 3737, 3739, 3741, 3742, 3746, 3748, 3750, 3752, 3753]
R1_CA0 = [1109, 1112, 1139, 1141, 1143, 1144, 1146, 1148, 1149, 1153, 1155, 1157, 1159, 1160]
R4_1C = [130, 308, 6041]
R4_KEEP = [128, 306, 6039]          # the `!=` compares stay string compares (see patch/fix-0000001C.py)
REF_1E = {372: ('50000 / 200000 / リファレンス文字数', '50000 / 500000 / リファレンス文字数'),
          373: ('255 * リファレンス文字数 / 2000', '255 * リファレンス文字数 / 5000')}
INT_MAX = 2 ** 31 - 1


def expr(cmd):
    return cmd[EXPR_KEY[cmd.type.name]]


def text(cmd):
    try:
        return re.sub(r"0x[0-9A-Fa-f]+", "0x", str(cmd))   # TextIns bodies print object addresses
    except Exception as e:   # a few commands hold a float pylivemaker cannot print
        return "<%s %s>" % (cmd.type.name, type(e).__name__)


def evaluate(entries, env):
    """Run an entry list the way LiveMaker does (in order, every entry, no short-circuit); ints truncate on / (all
    values here are >= 0). Returns (variables after, largest absolute int produced by an entry)."""
    env, peak = dict(env), 0
    for e in entries:
        v = [env[o.value] if int(o.type) == 0 else o.value for o in e.operands]
        t = int(e.type)
        if t == 1:
            r = v[0]
        elif t == 2:
            r = v[0] + v[1]
        elif t == 3:
            r = v[0] - v[1]
        elif t == 4:
            r = v[0] * v[1]
        elif t == 5:
            r = v[0] // v[1]
        elif t == 6:
            r = v[0] % v[1]
        elif t == 8:
            r = int(bool(v[0]) and bool(v[1]))
        elif t == 11 and e.func.name == 'Int':
            r = int(v[0])
        elif t == 11 and e.func.name == 'JCopy':
            r = v[0][v[1] - 1:]
        elif t == 19:
            r = str(v[0]) + str(v[1])
        else:
            r = {12: lambda a, b: a == b, 13: lambda a, b: a > b, 14: lambda a, b: a < b,
                 15: lambda a, b: a >= b, 16: lambda a, b: a <= b, 20: lambda a, b: a != b}[t](*v)
            r = int(r)
        if type(r) is int:
            peak = max(peak, abs(r))
        env[e.name] = r
    return env, peak


def run_fix(fid, src, dst):
    argv = sys.argv
    sys.argv = [str(ROOT / 'patch' / ('fix-%s.py' % fid)), str(src), str(dst)]
    try:
        runpy.run_path(sys.argv[0], run_name='__main__')
    finally:
        sys.argv = argv


class Base(unittest.TestCase):
    FID = None

    @classmethod
    def setUpClass(cls):
        if cls.FID is None:
            raise unittest.SkipTest("base class")
        cls.dir = SCRATCH / cls.FID
        if cls.dir.exists():
            shutil.rmtree(cls.dir)
        cls.dir.mkdir(parents=True)
        cls.orig, cls.out = {}, {}
        base = LMScript.from_file(str(ROOT / 'orig' / ('%s.lsb' % cls.FID)))
        for tree in ('orig', 'work'):
            src = cls.dir / ('%s-%s.lsb' % (tree, cls.FID))
            shutil.copyfile(ROOT / tree / ('%s.lsb' % cls.FID), src)
            once, twice = cls.dir / ('%s-once.lsb' % tree), cls.dir / ('%s-twice.lsb' % tree)
            run_fix(cls.FID, src, once)
            run_fix(cls.FID, once, twice)
            cls.orig[tree] = base   # orig/ and work/ hold identical expressions at every r2 site (checked)
            cls.out[tree] = (once, twice, LMScript.from_file(str(once)))

    def test_second_run_byte_identical(self):
        for tree in ('orig', 'work'):
            once, twice, _ = self.out[tree]
            self.assertEqual(once.read_bytes(), twice.read_bytes(), tree)

    def refused(self, mutate):
        """Copy orig/, break one site with `mutate(script)`, run the fix: it must exit and write nothing."""
        s = LMScript.from_file(str(ROOT / 'orig' / ('%s.lsb' % self.FID)))
        mutate(s)
        bad, dst = self.dir / 'bad-in.lsb', self.dir / 'bad-out.lsb'
        bad.write_bytes(s.to_lsb())
        if dst.exists():
            dst.unlink()
        with self.assertRaises(SystemExit) as cm:
            run_fix(self.FID, bad, dst)
        self.assertNotIn(cm.exception.code, (0, None))
        return dst, str(cm.exception.code)


def r1_check(test, idxs):
    """Evaluate every R1 site original vs fixed on many (E, T) pairs: same value, fixed never past 2^31 - 1."""
    rnd = random.Random(20261030)
    pairs = [(e, t) for t in (1458934, 3333322, 4000000) for e in (0, 1, 2147483, 2147484, t - 1, t)]
    pairs += [(rnd.randint(0, t), t) for t in (3333322, 2999999, 3500000) for _ in range(300)]
    for tree in ('orig', 'work'):
        fixed = test.out[tree][2]
        for idx in idxs:
            a, b = expr(test.orig[tree].commands[idx]).entries, expr(fixed.commands[idx]).entries
            test.assertFalse(any(int(e.type) == 4 and [o.value for o in e.operands] == ['終了テキスト数', 1000]
                                 for e in b), '%s idx %d still multiplies E by 1000' % (tree, idx))
            for unlock in (3, 6):
                for E, T in pairs:
                    env = {'終了テキスト数': E, '総テキスト数1': T, '総テキスト数2': T, '解禁編': unlock,
                           '進行率小数': '123'}
                    ra, _ = evaluate(a, env)
                    rb, peak = evaluate(b, env)
                    name = a[-1].name
                    test.assertEqual(ra[name], rb[name], '%s idx %d E=%d T=%d' % (tree, idx, E, T))
                    test.assertLessEqual(peak, INT_MAX, '%s idx %d E=%d T=%d' % (tree, idx, E, T))


class Fix0000001C(Base):
    FID = '0000001C'

    def test_r1_exact_and_no_overflow(self):
        r1_check(self, R1_1C)

    def test_r1_overflow_was_real(self):
        _, peak = evaluate(expr(self.orig['orig'].commands[3732]).entries,
                           {'終了テキスト数': 2147484, '総テキスト数1': 3333322, '総テキスト数2': 3333322})
        self.assertGreater(peak, INT_MAX)

    def test_r4_int_compare(self):
        for tree in ('orig', 'work'):
            s = self.out[tree][2]
            for idx in R4_1C:
                text = str(s.commands[idx])
                self.assertIn('Int(ナビ文字数) <= Int(JCopy(ナビ文字数2, 2))', text, '%s idx %d' % (tree, idx))
                ents = expr(s.commands[idx]).entries
                for a, b, want in (('11770', '/9494', 0), ('8598', '/10111', 1), ('9494', '/11770', 1),
                                   ('500', '/500', 1)):
                    env, _ = evaluate(ents, {'ナビ文字数': a, 'ナビ文字数2': b})
                    self.assertEqual(env['____arg'], want, '%s idx %d %s <= %s' % (tree, idx, a, b))
                env, _ = evaluate(expr(self.orig[tree].commands[idx]).entries, {'ナビ文字数': '11770', 'ナビ文字数2': '/9494'})
                self.assertEqual(env['____arg'], 1)   # the original string compare takes the wrong branch
            for idx in R4_KEEP:
                self.assertEqual([sig(e) for e in expr(s.commands[idx]).entries],
                                 [sig(e) for e in expr(self.orig[tree].commands[idx]).entries])

    def test_earlier_fixes_still_in_place(self):
        for tree in ('orig', 'work'):
            s = self.out[tree][2]
            self.assertIn('2500000', str(s.commands[131]))
            self.assertIn('30000', str(s.commands[138]))
            self.assertIn('2500000', str(s.commands[6043]))

    def test_refuses_changed_r1_site(self):
        def mutate(s):
            for e in expr(s.commands[3750]).entries:
                for o in e.operands:
                    if o.value == 1000 and int(e.type) == 4:
                        o.value = 999
        dst, msg = self.refused(mutate)
        self.assertIn('3750', msg)

    def test_refuses_changed_r4_site(self):
        def mutate(s):
            for e in expr(s.commands[308]).entries:
                if int(e.type) == 16:
                    e.operands.reverse()
        dst, msg = self.refused(mutate)
        self.assertIn('308', msg)


class Fix00001CA0(Base):
    FID = '00001CA0'

    def test_r1_exact_and_no_overflow(self):
        r1_check(self, R1_CA0)

    def test_unlock_bar_scale_still_in_place(self):
        for tree in ('orig', 'work'):
            self.assertIn('2500000', str(self.out[tree][2].commands[491]))

    def test_refuses_changed_r1_site(self):
        def mutate(s):
            for e in expr(s.commands[1109]).entries:
                for o in e.operands:
                    if o.value == 100 and int(e.type) == 5:
                        o.value = 10
        dst, msg = self.refused(mutate)
        self.assertFalse(dst.exists())
        self.assertIn('1109', msg)


R6_RANGE = range(538, 562)
R6_CHANGED = [538, 539, 540, 541, 546, 547, 553, 554, 555, 556, 557, 558, 559, 560, 561]


def r6_text(text):
    """The original rendering with the r2 staff-roll constants, by plain text replacement (independent of the fix)."""
    return (text.replace('文字数誤差 / 100', '文字数誤差 / 220').replace('文字数誤差 % 100', '文字数誤差 % 220')
            .replace('% 220 <= 60', '% 220 <= 132').replace('% 220 > 60', '% 220 > 132'))


class Fix00001F8A(Base):
    FID = '00001F8A'

    def test_r6_step_and_threshold(self):
        for tree in ('orig', 'work'):
            s, o = self.out[tree][2], self.orig[tree]
            changed = []
            for idx in range(len(s.commands)):
                before, after = text(o.commands[idx]), text(s.commands[idx])
                if tree == 'orig' or idx in R6_RANGE:
                    want = r6_text(before) if idx in R6_RANGE else before
                    self.assertEqual(after, want, '%s idx %d' % (tree, idx))
                if before != after:
                    changed.append(idx)
            if tree == 'orig':
                self.assertEqual(changed, R6_CHANGED)
            self.assertIn('% 220 <= 132', str(s.commands[539]))
            self.assertIn('% 220 > 132', str(s.commands[559]))

    def test_r6_timeline(self):
        """Scene 313: no credit before 220 characters; step n is shown from 220 n until 220 n + 132, then fades;
        step 25 (the last 順番) starts at 5,500 of the 8,500 English characters (65 %, as 2,500 / 3,869 in Japanese)."""
        s = self.out['orig'][2]
        go = expr(s.commands[538]).entries               # If 文字数誤差 / 220 > 0
        show = [e for e in expr(s.commands[539]).entries if int(e.type) in (6, 16)]   # % 220 <= 132
        fade = [e for e in expr(s.commands[559]).entries if int(e.type) in (6, 13)]   # % 220 > 132
        step = [e for e in expr(s.commands[547]).entries if int(e.type) == 5]          # 順番 == 文字数誤差 / 220
        for chars, n, on, shown, faded in ((219, 0, 0, 0, 1), (220, 1, 1, 1, 0), (352, 1, 1, 1, 0),
                                           (353, 1, 1, 0, 1), (5500, 25, 1, 1, 0), (5720, 26, 1, 1, 0)):
            env = {'文字数誤差': chars}
            self.assertEqual(evaluate(go, env)[0]['____arg'], on, chars)
            self.assertEqual(evaluate(step, env)[0][step[0].name], n, chars)
            self.assertEqual(evaluate(show, env)[0][show[-1].name], shown, chars)
            self.assertEqual(evaluate(fade, env)[0][fade[-1].name], faded, chars)
        self.assertEqual(round(5500 / 8500 * 100), round(2500 / 3869 * 100))

    def test_refuses_other_script(self):
        dst = self.dir / 'wrong-out.lsb'
        with self.assertRaises(SystemExit):
            run_fix(self.FID, ROOT / 'orig' / '0000001E.lsb', dst)
        self.assertFalse(dst.exists())

    def test_refuses_changed_site(self):
        def mutate(s):
            for e in expr(s.commands[547]).entries:
                for o in e.operands:
                    if o.value == 100:
                        o.value = 101
        dst, msg = self.refused(mutate)
        self.assertFalse(dst.exists())
        self.assertIn('547', msg)


class Fix0000001E(Base):
    FID = '0000001E'

    def test_reference_bar_scale(self):
        for tree in ('orig', 'work'):
            s, o = self.out[tree][2], self.orig[tree]
            for idx, (before, after) in REF_1E.items():
                self.assertIn(before, str(o.commands[idx]))
                self.assertIn(after, str(s.commands[idx]))
            self.assertIn('表示名', str(s.commands[2420]))   # the display-name repoint still runs

    def test_refuses_changed_site(self):
        def mutate(s):
            for e in expr(s.commands[373]).entries:
                for o in e.operands:
                    if o.value == 2000:
                        o.value = 3000
        dst, msg = self.refused(mutate)
        self.assertFalse(dst.exists())
        self.assertIn('373', msg)


if __name__ == '__main__':
    unittest.main(verbosity=2)
