import json
import tempfile
import unittest
from pathlib import Path
import zlib

import numpy as np
from PIL import Image, ImageDraw

import gal_frames
import gal_write
import refdoc118
from refdoc_surface import carry


class ReferenceAnimationTests(unittest.TestCase):
    def test_shaded_surface_preserves_alpha_and_unrelated_pixels(self):
        random = np.random.default_rng(20261025)
        original = np.dstack((random.integers(40, 220, (80, 100, 3), dtype=np.uint8),
                              np.full((80, 100), 255, np.uint8)))
        english = original.copy()
        english[30:45, 30:65, :3] = 30
        frame = original.copy()
        frame[:, :, :3] = np.round(original[:, :, :3].astype(float) * .6 + 20).astype(np.uint8)
        frame[:5, :, 3] = 0
        result, selected, _, report = carry(original, english, frame, [[0, 0], [100, 0], [100, 80], [0, 80]])
        self.assertTrue(np.array_equal(result[:, :, 3], frame[:, :, 3]))
        self.assertTrue(np.array_equal(result[~selected], frame[~selected]))
        self.assertLess(report["fitted_residual"], 1)
        self.assertLessEqual(np.abs(result[33:42, 35:60, :3].astype(int) - 38).max(), 1)

    def test_surface_visibility_does_not_paint_through_flap(self):
        random = np.random.default_rng(35)
        original = np.dstack((random.integers(30, 230, (80, 100, 3), dtype=np.uint8),
                              np.full((80, 100), 255, np.uint8)))
        english = original.copy()
        english[20:60, 20:80, :3] = 0
        visible = np.ones((80, 100), bool)
        visible[:40] = False
        result, _, _, _ = carry(original, english, original, [[0, 0], [100, 0], [100, 80], [0, 80]], visible)
        self.assertTrue(np.array_equal(result[:40], original[:40]))
        self.assertFalse(np.array_equal(result[45:55, 30:70], original[45:55, 30:70]))

    def test_photo_caption_date_and_unmodified_frames_survive(self):
        image = Image.new("RGBA", (444, 300), "#eee8dc")
        draw = ImageDraw.Draw(image)
        draw.text((20, 255), "/4/6", fill="black")
        draw.rectangle((180, 255, 330, 263), fill="black")
        header = zlib.compress(gal_write.fresh_xml(444, 300, 8, 1, 0))
        data = bytearray(b"GaleX200" + gal_write.p32(len(header)) + header)
        for index in range(8):
            pixels, alpha = gal_write.encode_layer(image, 0, 0), gal_write.encode_alpha(image)
            data += gal_write.p32(len(pixels)) + pixels + gal_write.p32(len(alpha)) + alpha
        with tempfile.TemporaryDirectory() as scratch:
            source, output = Path(scratch) / "0→1.gal", Path(scratch) / "english.gal"
            source.write_bytes(data)
            report = refdoc118.build(source, output, Path(scratch) / "evidence")
            original_xml, original_blobs, original = gal_frames.decode(source)
            final_xml, final_blobs, final = gal_frames.decode(output)
            self.assertEqual(original_xml, final_xml)
            self.assertTrue(report["modified_frames_pixel_exact"])
            for index in range(8):
                self.assertTrue(np.array_equal(original[index][:, :160], final[index][:, :160]))
                self.assertTrue(np.array_equal(original[index][:, :, 3], final[index][:, :, 3]))
                if index < 4:
                    self.assertEqual(original_blobs[index][3:], final_blobs[index][3:])
                else:
                    self.assertFalse(np.array_equal(original[index], final[index]))
            saved = json.loads((Path(scratch) / "evidence/report.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["caption"], "Akane and Mifuyu-chan's entrance ceremony")


if __name__ == "__main__":
    unittest.main()
