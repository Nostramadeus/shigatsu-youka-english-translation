import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile

from check_reference_release import check, PREFIX


def digest(data):
    return hashlib.sha256(data).hexdigest()


class ReferenceCoverageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.patch = Path(self.temp.name) / "candidate.zip"
        self.existing = PREFIX + "リファレンス詳細/rrr1/0.gal"
        self.repaired = PREFIX + "リファレンス詳細/rrr2/0.gal"
        self.art = PREFIX + "リファレンス詳細/rrr3/0.gal"
        self.inventory = dict(assets=[
            dict(original_path=self.existing, original_sha256=digest(b"JP1"),
                 shipped_overlay_present=True, shipped_overlay_sha256=digest(b"accepted EN")),
            dict(original_path=self.repaired, original_sha256=digest(b"JP2"), shipped_overlay_present=False),
            dict(original_path=self.art, original_sha256=digest(b"art"), shipped_overlay_present=False)])
        self.classification = dict(assets=[
            dict(original_path=self.existing, original_sha256=digest(b"JP1"), status="existing_overlay",
                 expected_overlay_sha256=digest(b"accepted EN"), evidence="accepted hash-bound review"),
            dict(original_path=self.repaired, original_sha256=digest(b"JP2"), status="repaired_overlay",
                 expected_overlay_sha256=digest(b"new EN"), evidence="source and rendered pixels reviewed"),
            dict(original_path=self.art, original_sha256=digest(b"art"), status="textless_art", evidence="original pixels reviewed")],
            extra_overlays=[], limitations=[])
        self.files = {self.existing: b"accepted EN", self.repaired: b"new EN"}

    def run_check(self):
        with zipfile.ZipFile(self.patch, "w") as archive:
            for path, data in self.files.items():
                archive.writestr(path, data)
        return check(self.inventory, self.classification, self.patch)

    def test_complete_required_hashes_pass(self):
        self.assertTrue(self.run_check()["passed"])

    def test_unknown_classification_blocks(self):
        self.classification["assets"][1]["status"] = "pending"
        self.assertFalse(self.run_check()["passed"])

    def test_missing_original_classification_blocks(self):
        self.classification["assets"].pop()
        self.assertFalse(self.run_check()["passed"])

    def test_duplicate_classification_blocks(self):
        self.classification["assets"].append(copy.deepcopy(self.classification["assets"][0]))
        self.assertFalse(self.run_check()["passed"])

    def test_original_hash_drift_blocks(self):
        self.classification["assets"][1]["original_sha256"] = digest(b"wrong source")
        self.assertFalse(self.run_check()["passed"])

    def test_actual_zip_missing_overlay_blocks(self):
        self.files.pop(self.repaired)
        self.assertFalse(self.run_check()["passed"])

    def test_actual_zip_wrong_english_bytes_blocks(self):
        self.files[self.repaired] = b"JP2"
        self.assertFalse(self.run_check()["passed"])

    def test_baseline_cannot_be_weakened_to_art(self):
        self.classification["assets"][0]["status"] = "textless_art"
        self.files.pop(self.existing)
        self.assertFalse(self.run_check()["passed"])

    def test_unregistered_new_reference_path_blocks(self):
        self.files[PREFIX + "new.gal"] = b"unreviewed"
        self.assertFalse(self.run_check()["passed"])

    def test_registered_alias_exact_hash_passes(self):
        path = PREFIX + "new.gal"
        self.files[path] = b"reviewed alias"
        self.classification["extra_overlays"].append(dict(path=path, sha256=digest(b"reviewed alias"), evidence="alias review"))
        self.assertTrue(self.run_check()["passed"])

    def test_japanese_puzzle_state_cannot_be_changed(self):
        self.classification["assets"][2]["status"] = "intentional_puzzle_japanese"
        self.files[self.art] = b"changed clue"
        self.assertFalse(self.run_check()["passed"])

    def test_missing_review_evidence_blocks(self):
        self.classification["assets"][1]["evidence"] = ""
        self.assertFalse(self.run_check()["passed"])


if __name__ == "__main__":
    unittest.main()
