"""Tests for tools/charcount_refs.py (reference 文字数 totals, counter repair 2026-10-29, Lane B).

    uv run --no-project --python 3.12 --with pylivemaker python tools/test_charcount_refs.py

Read-only on the project: every write goes to a temporary copy of the table outside the project. The copy gets
the original Japanese values back in the sampled rows first, so the tests mean the same before and after the
real table has been written.
"""
import contextlib
import io
import shutil
import sys
import tempfile
import unittest
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import charcount_refs as cr  # noqa: E402
from count_chars import blocks  # noqa: E402

# single block (the three counters-audit.json fixtures), stale residual with a JP-empty block on the route,
# three blocks across a message-box restyle, the player-name VAR row, and one not-consumed report row.
SAMPLE = {'1', '37', '38', '46', '223', '295', '41'}
FIXTURE_EN = {'1': 3322, '37': 1331, '38': 2464}   # counters-audit.json "reference_reproductions"


def orig_counts():
    raw = (ROOT / 'orig' / 'データベース' / 'リファレンスデータベース.tsv').read_bytes().decode('cp932')
    lines = raw.replace('\r\n', '\n').split('\n')
    col = lines[0].split('\t').index('文字数')
    out = {}
    for ln in lines[1:]:
        c = ln.split('\t')
        if ln and len(c) > col and c[col].strip().isdigit() and int(c[col]) > 0:
            out[c[0]] = int(c[col])
    return out


ORIG = orig_counts()


def quiet(**kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return cr.run(**kw)


class CharcountRefs(unittest.TestCase):
    def setUp(self):
        # tools/extract_lsb.py parses with LMScript.from_file(path), which leaves the handle to the GC
        warnings.simplefilter('ignore', ResourceWarning)
        self.tmp = Path(tempfile.mkdtemp(prefix='charcount_refs_'))
        raw = cr.TABLE.read_bytes().decode('utf-8')
        self.nl = '\r\n' if '\r\n' in raw else '\n'
        lines = raw.split(self.nl)
        self.col = lines[0].split('\t').index('文字数')
        for k, ln in enumerate(lines):
            c = ln.split('\t')
            if k and c[0] in SAMPLE:
                c[self.col] = str(ORIG[c[0]])
                lines[k] = '\t'.join(c)
        self.table = self.tmp / 'table.tsv'
        self.table.write_bytes(self.nl.join(lines).encode('utf-8'))
        self.store = self.tmp / 'jp-ref-totals.tsv'
        self.kw = dict(table=self.table, jp_store=self.store, extract_root=self.tmp / 'x', ids=SAMPLE)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_coverage_is_every_positive_row(self):
        self.assertEqual(len(ORIG), 184)
        self.assertFalse(set(cr.REFS) & set(cr.NOT_CONSUMED))
        self.assertEqual(set(cr.REFS) | set(cr.NOT_CONSUMED), set(ORIG))
        self.assertEqual((len(cr.REFS), len(cr.NOT_CONSUMED)), (152, 32))

    def test_jp_reproduction_every_recipe(self):
        for rid, (_disp, sid, route) in cr.REFS.items():
            d = dict(blocks(sid, 'lns'))
            jp = sum(d.get(b, 0) for b in route)
            self.assertEqual(ORIG[rid] - jp, cr.STALE_OK.get(rid, 0), rid)

    def test_dry_run_writes_nothing(self):
        before = self.table.read_bytes()
        results, failures = quiet(write=False, **self.kw)
        self.assertEqual(failures, [])
        self.assertEqual(self.table.read_bytes(), before)
        self.assertFalse(self.store.exists())
        self.assertEqual(sum(r[7].startswith('DRY') for r in results), 6)

    def test_write_changes_only_allowed_cells_and_is_idempotent(self):
        before = self.table.read_bytes()
        results, failures = quiet(write=True, **self.kw)
        self.assertEqual(failures, [])
        after = self.table.read_bytes()
        old, new = before.decode('utf-8').split(self.nl), after.decode('utf-8').split(self.nl)
        self.assertEqual(len(old), len(new))
        self.assertEqual(before.count(b'\r\n'), after.count(b'\r\n'))
        self.assertEqual(before.endswith(b'\n'), after.endswith(b'\n'))
        changed = set()
        for a, b in zip(old, new):
            ca, cb = a.split('\t'), b.split('\t')
            self.assertEqual(len(ca), len(cb))
            diff = [i for i, (x, y) in enumerate(zip(ca, cb)) if x != y]
            if diff:
                self.assertEqual(diff, [self.col])
                self.assertIn(ca[0], cr.REFS)
                self.assertEqual(int(ca[self.col]), ORIG[ca[0]])
                changed.add(ca[0])
                if ca[0] in FIXTURE_EN:
                    self.assertEqual(int(cb[self.col]), FIXTURE_EN[ca[0]])
        self.assertEqual(changed, SAMPLE - {'41'})
        store = self.store.read_text(encoding='utf-8')
        self.assertIn('1\t4\t1383\n', store)
        self.assertIn('295\t244\t2490\n', store)
        # second run: nothing changes, byte for byte
        results2, failures2 = quiet(write=True, **self.kw)
        self.assertEqual(failures2, [])
        self.assertEqual(self.table.read_bytes(), after)
        self.assertEqual(self.store.read_text(encoding='utf-8'), store)
        self.assertTrue(all(r[7] == 'DONE (unchanged)' for r in results2 if r[2] != '-'))

    def test_gate_refuses_a_changed_japanese_total(self):
        raw = self.table.read_bytes().decode('utf-8').split(self.nl)
        for k, ln in enumerate(raw):
            c = ln.split('\t')
            if k and c[0] == '1':
                c[self.col] = '1384'
                raw[k] = '\t'.join(c)
        self.table.write_bytes(self.nl.join(raw).encode('utf-8'))
        before = self.table.read_bytes()
        results, failures = quiet(write=True, **dict(self.kw, ids={'1'}))
        self.assertEqual(len(failures), 1)
        self.assertIn('GATE FAIL', failures[0])
        self.assertEqual(self.table.read_bytes(), before)
        self.assertNotIn('1\t', self.store.read_text(encoding='utf-8'))

    def test_var_detection(self):
        p = self.tmp / 'AAAAAAAA-b.lns'
        p.write_text(';h\r\n<VAR NAME="プレイヤー名" unk3="50">x<VAR NAME="他">y<var>\r\n', encoding='utf-8')
        self.assertEqual(cr.var_counts(self.tmp, 'AAAAAAAA', ['b']), {'プレイヤー名': 1, '他': 1, '<var>': 1})

    def test_walk_refuses_a_branch(self):
        lsb = cr.script(ROOT / 'orig' / '0000001E.lsb')
        self.assertEqual(lsb.commands[1829].type.name, 'If')
        with self.assertRaises(cr.Refused):
            cr.walk(lsb, '0000001E', 1829)


if __name__ == '__main__':
    unittest.main(verbosity=2)
