"""Tests for tools/charcount_recipes.py + tools/charcount_write.py (counter repair Lane A, 2026-10-29).

    uv run --no-project --python 3.12 --with pylivemaker python tools/test_charcount_recipes.py

1. Recipes: shape, ownership (no first-arc or unresolved row), and JP reproduction of EVERY scenario and hidden
   recipe from lns/ against orig/データベース (exact, or exactly the STALE_OK residual). Read-only.
2. Writer, on a temporary copy of the project data (C: temp, never the project tables): a dry run writes nothing,
   --write changes only 文字数1/文字数2/コア文字数 of the sample rows (scenario + hidden) and only the 文字数 column
   of the sample's 実況 tables (169: scaled by EN over the reproduced JP 3429, not the stale 3117), and a second
   --write changes nothing (idempotent).
3. True-Jusatsu: every TJ section route reproduces its orig field of 真呪殺編文字数.txt (or exactly TJ_STALE) and
   the sections concatenate to the row's 文字数1 recipe; tools/build_tj_counts.py on a one-line temporary file:
   dry run writes nothing, --write changes only the opening/section fields (EN, adding up to the tsv-en 文字数1),
   rerun is idempotent, a JP field that no longer reproduces is refused with nothing written.
"""
import hashlib
import shutil
import sys
import tempfile
import unittest
import warnings
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import build_tj_counts as tjb  # noqa: E402
import charcount_write as cw  # noqa: E402
from charcount_recipes import FIRST_ARC_OWNED, H, R, STALE_OK, TJ, TJ_STALE, UNRESOLVED  # noqa: E402

ROOT = TOOLS.parent
# single block / 3 columns / old row with 実況 / stale row with 実況 (red-box block, ratio over the route JP)
SAMPLE = {'0000107B': '1', '0000088B': '29', '000001DB': '85', '00000488': '169'}
HIDDEN_SAMPLE = '00002444'                                       # hidden IDs 14-17 (連番 218, 裏分岐 0/2/3/4)
TJ_SAMPLE = '246'                                                # smallest True-Jusatsu script (00000EAF)


def jp_of(sid, b1, b2, res):
    return cw.recipe_totals(cw.block_map(ROOT / 'lns', sid), b1, b2, res)


class RecipeTests(unittest.TestCase):
    def test_shapes_and_ownership(self):
        nos = [v[0] for v in R.values()]
        self.assertEqual(len(nos), len(set(nos)), 'one recipe per 連番')
        self.assertFalse(set(nos) & set(FIRST_ARC_OWNED), 'first-arc rows belong to repair_first_arc_totals.py')
        self.assertFalse(set(nos) & set(UNRESOLVED), 'unresolved rows must not have a recipe')
        for sid, (no, b1, b2, res) in R.items():
            self.assertRegex(sid, r'^[0-9A-F]{8}$')
            self.assertTrue(b1 and all(isinstance(n, str) for n in b1), sid)
            self.assertTrue(b2 is None or b2, sid)
            self.assertTrue(res is None or res, sid)
        for hid, (no, sid, b1, b2, res) in H.items():
            self.assertRegex(sid, r'^[0-9A-F]{8}$')
            self.assertTrue(b1 and b2 is None and res is None, hid)
        for (no, col), (n, why) in STALE_OK.items():
            self.assertIn(no, nos)
            self.assertIn(col, cw.COLS)
            self.assertTrue(n and why)

    def test_first_arc_list_matches_owner(self):
        try:
            import repair_first_arc_totals as rf
        except ImportError:
            self.skipTest('needs pylivemaker')
        self.assertEqual(set(FIRST_ARC_OWNED), set(rf.ROUTES))

    def test_jp_reproduction_every_scenario_recipe(self):
        orig = cw.orig_totals(ROOT / 'orig/データベース/シナリオデータベース.tsv')
        for sid, (no, b1, b2, res) in R.items():
            jp, missing, var = jp_of(sid, b1, b2, res)
            self.assertEqual(missing, [], (no, sid))
            self.assertEqual(var, [], (no, sid))
            for col, a, b in zip(cw.COLS, jp, orig[no]):
                self.assertEqual(b - a, STALE_OK.get((no, col), (0, ''))[0], (no, sid, col, a, b))

    def test_jp_reproduction_every_hidden_recipe(self):
        orig = cw.orig_totals(ROOT / 'orig/データベース/裏ルート.tsv')
        for hid, (no, sid, b1, b2, res) in H.items():
            jp, missing, var = jp_of(sid, b1, b2, res)
            self.assertEqual((missing, var), ([], []), hid)
            self.assertEqual(jp, orig[hid], (hid, sid))

    def test_known_rows(self):
        by_no = {v[0]: (k,) + v[1:] for k, v in R.items()}
        self.assertEqual(jp_of(*by_no['29'])[0], (2661, 2483, 1347))           # 3 columns, resume route
        self.assertEqual(jp_of(*by_no['31'])[0], (6312, 6452, 3712))           # 分岐案内 == 1 branch
        self.assertEqual(jp_of(*by_no['244'])[0][0], 3896)                     # text after the staff-roll loop
        self.assertIn('line15', by_no['227'][1])                               # red-box block counts (D2e)
        self.assertEqual(jp_of(*by_no['227'])[0][0], 6412)
        self.assertEqual(jp_of(*by_no['247'])[0][0], 60477)                    # True-Jusatsu sections 0..12
        self.assertEqual(STALE_OK[('247', '文字数1')][0], 4)
        self.assertNotIn('314', {v[0] for v in R.values()})                    # placeholder + VAR: stays JP
        self.assertEqual([H[h][2] for h in ('14', '15', '16', '17')],
                         [['00002447'], ['00002449'], ['0000244D'], ['0000244E']])
        # 169: the live red-box block line48 counts (orchestrator 2026-10-29); author total 3117 is 312 short
        self.assertIn('line48', by_no['169'][1])
        self.assertEqual(jp_of(*by_no['169'])[0][0], 3429)
        self.assertEqual(STALE_OK[('169', '文字数1')][0], -312)

    def test_tj_sections(self):
        raw = (ROOT / 'orig/ノベルシステム/真呪殺編文字数.txt').read_bytes().decode('cp932')
        lines = {ln.split(',')[0]: ln.split(',') for ln in raw.splitlines() if ln.strip()}
        self.assertEqual(set(lines), set(TJ))
        for no, (sid, opening, sections) in TJ.items():
            self.assertEqual(R[sid][0], no)
            self.assertEqual(R[sid][1], [b for s in sections for b in s], no)   # sections 0..N = 文字数1 recipe
            f = lines[no]
            self.assertEqual(int(f[2]), len(sections), no)
            jp, missing, var = tjb.route_counts(cw.block_map(ROOT / 'lns', sid), opening, sections)
            self.assertEqual((missing, var), ([], []), no)
            for i, (stored, got) in enumerate(zip((int(x) for x in f[3:]), jp)):
                self.assertEqual(stored - got, TJ_STALE.get((no, i - 1), 0), (no, i - 1))
            self.assertEqual(sum(v for (n, k), v in TJ_STALE.items() if n == no and k >= 0),
                             STALE_OK.get((no, '文字数1'), (0, ''))[0], no)


def tree_hash(root, skip):
    out = {}
    for p in sorted(Path(root).rglob('*')):
        if p.is_file() and not any(s in p.parents for s in skip):
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


class WriterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import livemaker  # noqa: F401
        except ImportError:
            raise unittest.SkipTest('needs pylivemaker (uv run --with pylivemaker)')
        # pylivemaker's LMScript.from_file(<path str>) (inside tools/extract_lsb.py) leaves the .lsb handle open
        warnings.filterwarnings('ignore', message=r'unclosed file .*\.lsb', category=ResourceWarning)
        sids = set(SAMPLE) | {HIDDEN_SAMPLE}
        if not all((ROOT / 'work' / (s + '.lsb')).is_file() for s in sids):
            raise unittest.SkipTest('needs the compiled English scripts in work/')
        cls.tmp = Path(tempfile.mkdtemp(prefix='charcount-test-'))
        t = cls.tmp
        for rel in ('tsv-en/シナリオデータベース.tsv', 'tsv-en/裏ルート.tsv',
                    'orig/データベース/シナリオデータベース.tsv', 'orig/データベース/裏ルート.tsv',
                    'orig/データベース/実況/85.tsv', 'tsv-en/実況/85.tsv',
                    'orig/データベース/実況/169.tsv', 'tsv-en/実況/169.tsv'):
            if (ROOT / rel).exists():
                (t / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, t / rel)
        (t / 'lns').mkdir()
        (t / 'work').mkdir()
        for s in sids:
            for f in (ROOT / 'lns').glob(s + '-*.lns'):
                shutil.copy2(f, t / 'lns' / f.name)
            shutil.copy2(ROOT / 'work' / (s + '.lsb'), t / 'work' / (s + '.lsb'))
        # start the sample rows from their Japanese values, whatever the project tables hold today
        orig = cw.orig_totals(t / 'orig/データベース/シナリオデータベース.tsv')
        horig = cw.orig_totals(t / 'orig/データベース/裏ルート.tsv')
        tab = cw.Table(t / 'tsv-en/シナリオデータベース.tsv')
        for no in SAMPLE.values():
            tab.set(no, orig[no])
        (t / 'tsv-en/シナリオデータベース.tsv').write_bytes(tab.text().encode('utf-8'))
        htab = cw.Table(t / 'tsv-en/裏ルート.tsv')
        cls.hids = [h for h, v in H.items() if v[1] == HIDDEN_SAMPLE]
        for h in cls.hids:
            htab.set(h, horig[h])
        (t / 'tsv-en/裏ルート.tsv').write_bytes(htab.text().encode('utf-8'))
        cls.paths = cw.Paths(t)
        cls.only = set(SAMPLE) | {HIDDEN_SAMPLE}
        cls.skip = [cls.paths.tmp / s for s in cls.only]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_writer(self, write):
        return cw.run(self.paths, write=write, only=self.only, log=lambda *a: None)

    def test_1_dry_run_writes_nothing(self):
        before = tree_hash(self.tmp, self.skip)
        s = self.run_writer(False)
        self.assertEqual(tree_hash(self.tmp, self.skip), before)
        self.assertEqual(s['skipped'], {})
        self.assertEqual(set(s['scenario']), set(SAMPLE.values()))
        self.assertEqual(set(s['hidden']), set(self.hids))

    def test_2_write_changes_only_allowed_cells(self):
        p = self.paths
        old_s, old_h = p.tsv.read_bytes(), p.hid.read_bytes()
        s = self.run_writer(True)
        for path, old, keys, values in ((p.tsv, old_s, set(SAMPLE.values()), s['scenario']),
                                        (p.hid, old_h, set(self.hids), s['hidden'])):
            a = old.decode('utf-8').split('\n')
            b = path.read_bytes().decode('utf-8').split('\n')
            self.assertEqual(len(a), len(b))
            head = a[0].rstrip('\r').split('\t')
            allowed = {head.index(c) for c in cw.COLS}
            changed = set()
            for x, y in zip(a, b):
                if x == y:
                    continue
                cx, cy = x.split('\t'), y.split('\t')
                self.assertEqual(len(cx), len(cy))
                diff = {i for i, (u, v) in enumerate(zip(cx, cy)) if u != v}
                self.assertTrue(diff <= allowed, (path.name, cx[0], diff))
                changed.add(cx[0])
                en = values[cx[0]][1]
                self.assertEqual(tuple(int(cy[head.index(c)]) for c in cw.COLS), en)
            self.assertEqual(changed, keys, path.name)
        self.assertEqual(p.tsv.read_bytes().count(b'\r\n'), old_s.count(b'\r\n'))   # newline style kept
        # 138 (first-arc, owned elsewhere) untouched
        self.assertEqual(cw.Table(p.tsv).cells('138'), [c for c in old_s.decode('utf-8').split('\n')
                                                       if c.startswith('138\t')][0].split('\t'))
        # 実況 85: only the 文字数 column differs from the orig rows (text merged from tsv-en as before)
        jk_t = (p.jk_out / '85.tsv').read_bytes().decode('cp932')
        src_t = (p.jk_src / '85.tsv').read_bytes().decode('cp932')
        self.assertEqual(cw.old_nl(jk_t), cw.old_nl(src_t))
        jk, src = jk_t.split(cw.old_nl(jk_t)), src_t.split(cw.old_nl(src_t))
        self.assertEqual(len(jk), len(src))
        ci = src[0].split('\t').index('文字数')
        tcols = {i for i, x in enumerate(src[0].split('\t')) if x.split(' ')[0] == 'テキスト'}
        for x, y in zip(src, jk):
            for i, (u, v) in enumerate(zip(x.split('\t'), y.split('\t'))):
                if u != v:
                    self.assertIn(i, tcols | {ci})
        self.assertTrue(p.jpfile.exists() and p.jphfile.exists())
        # 実況 169: triggers scaled by EN / reproduced JP (3429), not by the stale author total 3117
        en169 = s['scenario']['169'][1][0]
        t = (p.jk_out / '169.tsv').read_bytes().decode('cp932')
        o = (p.jk_src / '169.tsv').read_bytes().decode('cp932')
        rows_t, rows_o = t.split(cw.old_nl(t)), o.split(cw.old_nl(o))
        ci = rows_o[0].split('\t').index('文字数')
        for x, y in zip(rows_o[1:], rows_t[1:]):
            v = x.split('\t')[ci] if len(x.split('\t')) > ci else ''
            if v.strip().isdigit():
                self.assertEqual(int(y.split('\t')[ci]), (int(v) * en169 * 2 + 3429) // (2 * 3429))

    def test_3_rerun_is_idempotent(self):
        p = self.paths
        files = [p.tsv, p.hid, p.jpfile, p.jphfile, p.jk_out / '85.tsv']
        before = [f.read_bytes() for f in files]
        s = self.run_writer(True)
        self.assertEqual([f.read_bytes() for f in files], before)
        self.assertEqual(s['skipped'], {})


class TJBuilderTests(unittest.TestCase):
    """tools/build_tj_counts.py on a temporary root holding one line of 真呪殺編文字数.txt (row 246)."""

    @classmethod
    def setUpClass(cls):
        try:
            import livemaker  # noqa: F401
        except ImportError:
            raise unittest.SkipTest('needs pylivemaker (uv run --with pylivemaker)')
        warnings.filterwarnings('ignore', message=r'unclosed file .*\.lsb', category=ResourceWarning)
        sid = TJ[TJ_SAMPLE][0]
        if not (ROOT / 'work' / (sid + '.lsb')).is_file():
            raise unittest.SkipTest('needs the compiled English script in work/')
        cls.tmp = t = Path(tempfile.mkdtemp(prefix='tjcounts-test-'))
        raw = (ROOT / 'orig' / tjb.REL).read_bytes().decode('cp932')
        nl = cw.old_nl(raw)
        line = [ln for ln in raw.split(nl) if ln.startswith(TJ_SAMPLE + ',')][0]
        cls.src_text = line + nl
        (t / 'orig' / tjb.REL).parent.mkdir(parents=True)
        (t / 'orig' / tjb.REL).write_bytes(cls.src_text.encode('cp932'))
        (t / 'tsv-en').mkdir()
        shutil.copy2(ROOT / 'tsv-en/シナリオデータベース.tsv', t / 'tsv-en/シナリオデータベース.tsv')  # EN 文字数1
        (t / 'lns').mkdir()
        (t / 'work').mkdir()
        for f in (ROOT / 'lns').glob(sid + '-*.lns'):
            shutil.copy2(f, t / 'lns' / f.name)
        shutil.copy2(ROOT / 'work' / (sid + '.lsb'), t / 'work' / (sid + '.lsb'))
        cls.paths = cw.Paths(t)
        cls.out = t / 'work' / tjb.REL
        cls.extracted = set()
        cls.skip = [cls.paths.tmp / sid]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def build(self, write):
        return tjb.run(self.paths, write=write, log=lambda *a: None, require_all=False, extracted=self.extracted)

    def test_1_dry_run_writes_nothing(self):
        before = tree_hash(self.tmp, self.skip)
        r = self.build(False)
        self.assertEqual(r['refused'], [])
        self.assertTrue(r['changed'])
        self.assertEqual(tree_hash(self.tmp, self.skip), before)

    def test_2_write(self):
        r = self.build(True)
        self.assertEqual(r['refused'], [])
        jp, en = r['rows'][TJ_SAMPLE]
        a = self.src_text.rstrip('\r\n').split(',')
        b = self.out.read_bytes().decode('cp932')
        self.assertEqual(cw.old_nl(b), cw.old_nl(self.src_text))
        b = b.rstrip('\r\n').split(',')
        n = int(a[2])
        self.assertEqual(len(a), len(b))
        self.assertEqual(a[:3] + a[4 + n:], b[:3] + b[4 + n:])                # 連番, title, N, padding kept
        self.assertEqual([int(x) for x in b[3:4 + n]], en)                    # opening + sections in English
        self.assertEqual([int(x) for x in a[3:4 + n]], jp)
        tab = cw.Table(self.paths.tsv)
        self.assertEqual(sum(en[1:]), int(tab.cells(TJ_SAMPLE)[tab.col('文字数1')]))
        self.assertTrue(all(e > j for e, j in zip(en, jp)))

    def test_3_rerun_is_idempotent(self):
        before = self.out.read_bytes()
        r = self.build(True)
        self.assertEqual((r['refused'], r['changed']), ([], False))
        self.assertEqual(self.out.read_bytes(), before)

    def test_4_changed_jp_field_is_refused(self):
        src = self.tmp / 'orig' / tjb.REL
        f = self.src_text.rstrip('\r\n').split(',')
        f[5] = str(int(f[5]) + 1)                                           # section 1 no longer reproduces
        src.write_bytes((','.join(f) + cw.old_nl(self.src_text)).encode('cp932'))
        before = self.out.read_bytes() if self.out.exists() else None
        try:
            r = self.build(True)
        finally:
            src.write_bytes(self.src_text.encode('cp932'))
        self.assertTrue(r['refused'] and 'JP gate' in r['refused'][0])
        self.assertEqual(self.out.read_bytes() if self.out.exists() else None, before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
