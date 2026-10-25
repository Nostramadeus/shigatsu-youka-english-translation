import os
from pathlib import Path
import tempfile
import unittest
import zipfile

from build_en_folder import zip_entry


class PatchArchiveTests(unittest.TestCase):
    def test_source_timestamps_do_not_enter_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.txt"
            source.write_bytes(b"English document\n")
            archives = []
            for number, timestamp in enumerate((1000000000, 1700000000)):
                os.utime(source, (timestamp, timestamp))
                destination = root / f"patch-{number}.zip"
                with zipfile.ZipFile(destination, "w") as archive:
                    zip_entry(archive, source, "documents/translation.txt")
                archives.append(destination.read_bytes())
            self.assertEqual(archives[0], archives[1])
            with zipfile.ZipFile(root / "patch-0.zip") as archive:
                entry = archive.infolist()[0]
                self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                self.assertEqual(entry.extra, b"")
                self.assertEqual(archive.read(entry), source.read_bytes())
                self.assertEqual(entry.external_attr >> 16, 0o100644)


if __name__ == "__main__":
    unittest.main()
