import unittest

from build_tsv import compatible_header, cell_cap


class HeaderWidthTests(unittest.TestCase):
    def test_accepts_unchanged_or_wider_fields(self):
        self.assertTrue(compatible_header("Text", "Text"))
        self.assertTrue(compatible_header("Text", "Text cha 160"))
        self.assertTrue(compatible_header("Text cha 124", "Text cha 160"))
        self.assertTrue(compatible_header("Text cha 124", "Text cha 124"))

    def test_rejects_column_renames_and_smaller_fields(self):
        self.assertFalse(compatible_header("Text cha 124", "Other cha 160"))
        self.assertFalse(compatible_header("Text cha 124", "Text cha 80"))
        self.assertFalse(compatible_header("Text cha 124", "Text"))
        self.assertFalse(compatible_header("Text", "Other"))


class ChrAndByteCapTests(unittest.TestCase):
    # 2026-11-03: caps are CP932 bytes; " chr N" (実況 tables) may be raised like " cha N"; untyped = 80 bytes.
    def test_chr_widen(self):
        self.assertTrue(compatible_header("Text chr 200", "Text chr 220"))
        self.assertFalse(compatible_header("Text chr 200", "Text chr 180"))
        self.assertFalse(compatible_header("Text chr 200", "Text cha 220"))

    def test_cell_cap(self):
        self.assertEqual(cell_cap("Text cha 1592"), 1592)
        self.assertEqual(cell_cap("Text chr 200"), 200)
        self.assertEqual(cell_cap("Text CHA 2446"), 2446)
        self.assertEqual(cell_cap("Text"), 80)


if __name__ == "__main__":
    unittest.main()
