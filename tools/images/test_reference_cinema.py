import struct
import unittest

from reference_cinema import patch_caption


class CaptionTests(unittest.TestCase):
    def source(self, caption, widths=3):
        encoded = caption.encode("cp932")
        return (b"LiveCinema113" + struct.pack("<I", 214) + b"\x00" * 20 +
                struct.pack("<I", len(encoded)) + encoded + b"FONT_AND_TIMING" +
                (struct.pack("<I", 214) + b"\x00" * 8) * (widths - 1))

    def test_long_caption_and_background_widths(self):
        source = self.source("左クリックで追加情報")
        target = "Left-click for additional information"
        output = patch_caption(source, "左クリックで追加情報", target, 500)
        restored = output.replace(struct.pack("<I", 500), struct.pack("<I", 214))
        restored = restored.replace(struct.pack("<I", len(target)) + target.encode(),
                                    struct.pack("<I", 20) + "左クリックで追加情報".encode("cp932"))
        self.assertEqual(restored, source)
        self.assertEqual(output.count(struct.pack("<I", 500)), 3)

    def test_short_caption_padding(self):
        source = self.source("クリック")
        output = patch_caption(source, "クリック", "Click")
        self.assertEqual(len(output), len(source))
        self.assertIn(struct.pack("<I", 8) + b"Click   ", output)

    def test_unexpected_layout_is_refused(self):
        for source in (self.source("クリック", widths=2), b"invalid"):
            with self.assertRaises(ValueError):
                patch_caption(source, "クリック", "Click", 500)
        with self.assertRaises(ValueError):
            patch_caption(self.source("クリック"), "クリック", "Caption too long")


if __name__ == "__main__":
    unittest.main()
