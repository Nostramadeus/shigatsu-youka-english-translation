import struct
import tempfile
import unittest
from pathlib import Path
import zlib

import numpy as np
from PIL import Image

import gal_frames
import gal_write


class GalFramesTests(unittest.TestCase):
    def test_previous_frame_copies_every_row(self):
        previous = bytes(range(16))
        packed = struct.pack("<ii", 0, 0)
        self.assertEqual(gal_frames.unpack_blocks(packed, 4, 4, 1, 4, 4, [previous]), previous)

    def test_same_layer_block(self):
        packed = struct.pack("<iiii", -1, 0, -2, 0) + bytes([10, 20, 30, 40])
        self.assertEqual(gal_frames.unpack_blocks(packed, 4, 2, 1, 2, 2, []),
                         bytes([10, 20, 10, 20, 30, 40, 30, 40]))

    def test_partial_blocks_preserve_padding(self):
        packed = struct.pack("<iiii", -1, 0, -1, 0) + bytes([1, 2, 4, 5, 3, 6])
        self.assertEqual(gal_frames.unpack_blocks(packed, 3, 2, 1, 2, 2, []), bytes([1, 2, 3, 0, 4, 5, 6, 0]))

    def test_bad_references_rejected(self):
        for reference in [(0, 0), (-3, 0), (-2, 0), (-1, 0)]:
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                gal_frames.unpack_blocks(struct.pack("<ii", *reference), 4, 4, 1, 4, 4, [])

    def test_unblocked_size_and_trailing_bytes_rejected(self):
        with self.assertRaises(ValueError):
            gal_frames.unpack_blocks(b"", 2, 2, 3, 0, 0, [])
        with self.assertRaises(ValueError):
            gal_frames.unpack_blocks(struct.pack("<ii", -1, 0) + bytes(17), 4, 4, 1, 4, 4, [])

    def test_jpeg_animation_lossless_rewrite(self):
        frames = [np.full((4, 4, 4), [50, 100, 150, 255], np.uint8),
                  np.full((4, 4, 4), [150, 100, 50, 128], np.uint8)]
        header = zlib.compress(gal_write.fresh_xml(4, 4, 2, 1, 2))
        data = bytearray(b"GaleX200" + gal_write.p32(len(header)) + header)
        for frame in frames:
            image = Image.fromarray(frame, "RGBA")
            pixels, alpha = gal_write.encode_layer(image, 2, 90), gal_write.encode_alpha(image)
            data += gal_write.p32(len(pixels)) + pixels + gal_write.p32(len(alpha)) + alpha
        with tempfile.TemporaryDirectory() as scratch:
            source, output = Path(scratch) / "source.gal", Path(scratch) / "output.gal"
            source.write_bytes(data)
            original_xml, _, decoded = gal_frames.decode(source)
            gal_frames.write_lossless(source, output, decoded)
            final_xml, _, final = gal_frames.decode(output)
            self.assertIn(b'CompType="2"', original_xml)
            self.assertIn(b'CompType="0"', final_xml)
            for expected, actual in zip(decoded, final):
                self.assertTrue(np.array_equal(expected, actual))


if __name__ == "__main__":
    unittest.main()
