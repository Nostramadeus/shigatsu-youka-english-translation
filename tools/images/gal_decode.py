import io
import struct
import zlib

from PIL import Image
import livemaker.GalImagePlugin


livemaker.GalImagePlugin._GAL_MODE[1] = ("P", "P;1")


def one_bit_source(data):
    if data[:8] != b"GaleX200":
        return False
    size = struct.unpack_from("<I", data, 8)[0]
    return b' Bpp="1"' in zlib.decompress(data[12:12 + size])


def open_gal(data):
    picture = Image.open(io.BytesIO(data))
    if one_bit_source(data):
        tile = picture.tile[0]
        info = tile[3][0]
        if info["compression"] != 0 or info["block_width"] or len(info["frames"]) != 1:
            raise ValueError("Unsupported one-bit GAL layout")
        frame = info["frames"][0]
        if len(frame["layers"]) != 1 or frame["layers"][0]["alpha_on"]:
            raise ValueError("Unsupported one-bit GAL layers")
        size = struct.unpack_from("<I", data, tile[2])[0]
        raw = zlib.decompress(data[tile[2] + 4:tile[2] + 4 + size])
        stride = ((frame["width"] + 31) // 32) * 4
        if len(raw) != stride * frame["height"]:
            raise ValueError("Unexpected one-bit GAL row padding")
        frame["stride"] = stride
    return picture
