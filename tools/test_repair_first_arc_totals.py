from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from livemaker.lsb import LMScript

from repair_first_arc_totals import (
    ROOT, ROUTES, TABLE_NAME, assert_no_commentary, block_count, compute_totals,
    repair_table, route_total, write_candidate,
)


class FirstArcTotalsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not all((ROOT / "work" / f"{route.script}.lsb").is_file() for route in ROUTES.values()):
            raise unittest.SkipTest("Requires the audited compiled English scripts in work/")
        cls.totals = compute_totals()
        rows = (ROOT / "tsv-en" / TABLE_NAME).read_text(encoding="utf-8").splitlines(keepends=True)
        column = rows[0].rstrip("\r\n").split("\t").index("文字数1")
        for index, row in enumerate(rows[1:], 1):
            cells = row.split("\t")
            if cells[0] in ROUTES:
                cells[column] = str(ROUTES[cells[0]].original_total)
                rows[index] = "\t".join(cells)
        cls.source = "".join(rows).encode("utf-8")

    def load_script(self, name):
        return LMScript.from_file(BytesIO((ROOT / "work" / name).read_bytes()), call_name=name)

    def test_known_compiled_route_totals(self):
        self.assertEqual(self.totals, {
            "138": 13282, "145": 8065, "147": 5219, "205": 6985,
            "162": 13290, "170": 12836, "206": 9325, "202": 10259,
        })

    def test_dead_legacy_block_excluded_and_all_live_blocks_included(self):
        script = self.load_script("000005C1.lsb")
        self.assertEqual(block_count(script, 11, "000005C7"), 15417)
        self.assertEqual(sum(block_count(script, *block) for block in ROUTES["138"].blocks),
                         self.totals["138"])
        script = self.load_script("0000062C.lsb")
        self.assertEqual([block_count(script, *block) for block in ROUTES["170"].blocks],
                         [7224, 44, 5568])

    def test_only_eight_count1_cells_change(self):
        repaired = repair_table(self.source, self.totals)
        old_rows = [line.split("\t") for line in self.source.decode("utf-8").splitlines()]
        new_rows = [line.split("\t") for line in repaired.decode("utf-8").splitlines()]
        self.assertEqual(len(old_rows), len(new_rows))
        column = old_rows[0].index("文字数1")
        changes = []
        for old_row, new_row in zip(old_rows, new_rows):
            self.assertEqual(len(old_row), len(new_row))
            for index, (before, after) in enumerate(zip(old_row, new_row)):
                if before != after:
                    changes.append((old_row[0], index))
        self.assertEqual(set(changes), {(number, column) for number in ROUTES})
        for row in new_rows:
            if row[0] in ROUTES:
                self.assertEqual(row[column], str(self.totals[row[0]]))
        self.assertEqual(len(changes), 8)
        self.assertEqual(repair_table(repaired, self.totals), repaired)

    def test_crlf_and_trailing_empty_cells_are_preserved(self):
        source = self.source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        repaired = repair_table(source, self.totals)
        self.assertEqual(source.count(b"\r\n"), repaired.count(b"\r\n"))
        self.assertNotIn(b"\n", repaired.replace(b"\r\n", b""))
        for before, after in zip(source.split(b"\r\n"), repaired.split(b"\r\n")):
            self.assertEqual(len(before.split(b"\t")), len(after.split(b"\t")))
            self.assertEqual(len(before) - len(before.rstrip(b"\t")),
                             len(after) - len(after.rstrip(b"\t")))
        self.assertEqual(repair_table(source.rstrip(b"\r\n"), self.totals),
                         repaired.rstrip(b"\r\n"))

    def test_unexpected_table_counts_and_missing_empty_cells_refused(self):
        rows = self.source.decode("utf-8").splitlines()
        column = rows[0].split("\t").index("文字数1")
        selected = next(index for index, row in enumerate(rows) if row.startswith("145\t"))
        cells = rows[selected].split("\t")
        cells[column] = "123456"
        rows[selected] = "\t".join(cells)
        with self.assertRaisesRegex(ValueError, "unexpected scenario counts"):
            repair_table("\n".join(rows).encode("utf-8"), self.totals)
        rows[selected] = rows[selected].rstrip("\t")
        with self.assertRaisesRegex(ValueError, "malformed scenario row"):
            repair_table("\n".join(rows).encode("utf-8"), self.totals)

    def test_changed_compiled_script_refused(self):
        route = ROUTES["145"]
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / f"{route.script}.lsb"
            candidate.write_bytes((ROOT / "work" / candidate.name).read_bytes() + b"changed")
            with self.assertRaisesRegex(ValueError, "changed compiled script"):
                route_total(candidate, route)

    def test_changed_target_label_and_dynamic_text_refused(self):
        script = self.load_script("000005D6.lsb")
        command = script.commands[11]
        target = command["Target"]
        command.args["Target"] = '"unexpected"'
        with self.assertRaisesRegex(ValueError, "identity/target"):
            block_count(script, 11, "000005E1")
        command.args["Target"] = target
        with self.assertRaisesRegex(ValueError, "block label"):
            block_count(script, 11, "unexpected")
        with patch("repair_first_arc_totals.LNSDecompiler.decompile", return_value='<VAR NAME="x">'):
            with self.assertRaisesRegex(ValueError, "dynamic VAR"):
                block_count(script, 11, "000005E1")

    def test_new_commentary_refused_and_project_output_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            commentary = root / "tsv-en/実況/145分岐.tsv"
            commentary.parent.mkdir(parents=True)
            commentary.write_bytes(b"new commentary\n")
            with self.assertRaisesRegex(ValueError, "commentary requires"):
                assert_no_commentary(root)
            with self.assertRaisesRegex(ValueError, "outside the project"):
                write_candidate(root / "candidate.tsv", b"candidate", root)
            candidate = root / "candidate.tsv"
            write_candidate(candidate, b"candidate")
            self.assertEqual(candidate.read_bytes(), b"candidate")


if __name__ == "__main__":
    unittest.main()
