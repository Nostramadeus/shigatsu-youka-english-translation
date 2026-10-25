import io
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

from PIL import Image

from gal_decode import open_gal


class OneBitGalTests(unittest.TestCase):
    def test_converter_rejects_failed_images(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid = root / "invalid.gal"
            invalid.write_bytes(b"not a GAL image")
            converter = Path(__file__).with_name("gal_to_png.py")
            result = subprocess.run([sys.executable, str(converter), str(invalid), str(root / "out")],
                                    capture_output=True, text=True, creationflags=0x08000000 if sys.platform == "win32" else 0)
            self.assertEqual(result.returncode, 1)
            self.assertIn("fail=1", result.stderr)

    def test_padded_scanlines(self):
        width, height, stride = 300, 8, 40
        header = (f'<Frames Version="200" Width="{width}" Height="{height}" Bpp="1" Count="1" '
                  'Randomized="0" CompType="0" BlockWidth="0" BlockHeight="0">'
                  f'<Frame Name="test"><Layers Width="{width}" Height="{height}" Bpp="1">'
                  '<RGB>000000FFFFFF</RGB><Layer AlphaOn="0"/></Layers></Frame></Frames>')
        compressed_header = zlib.compress(header.encode("ascii"))
        pixels = bytearray(stride * height)
        expected = Image.new("P", (width, height))
        for row in range(height):
            column = row * 7 % width
            pixels[row * stride + column // 8] |= 128 >> (column % 8)
            expected.putpixel((column, row), 1)
        compressed_pixels = zlib.compress(pixels)
        data = (b"GaleX200" + struct.pack("<I", len(compressed_header)) + compressed_header
                + struct.pack("<I", len(compressed_pixels)) + compressed_pixels)
        picture = open_gal(data)
        picture.load()
        self.assertEqual(picture.tobytes(), expected.tobytes())
        self.assertEqual(picture.convert("RGB").getpixel((0, 0)), (255, 255, 255))
        unaligned = Image.open(io.BytesIO(data))
        unaligned.load()
        self.assertNotEqual(unaligned.tobytes(), expected.tobytes())


if __name__ == "__main__":
    unittest.main()
