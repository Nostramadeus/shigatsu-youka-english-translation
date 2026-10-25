import unittest

from build_tsv import compatible_header


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


if __name__ == "__main__":
    unittest.main()
