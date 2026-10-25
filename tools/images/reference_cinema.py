"""Repair reference-cinema captions while preserving fonts, colors and timing."""
import argparse
from pathlib import Path
import struct


JOBS = (
    ("右クリックテキスト", "右クリックでさらに追加情報", "Right-click for further information", 500),
    ("左クリックテキスト", "左クリックで追加情報", "Left-click for additional information", 500),
    ("初クリック", "クリック", "Click", None),
)


def patch_caption(data, source, target, width=None):
    if not data.startswith(b"LiveCinema113"):
        raise ValueError("Unsupported cinema version")
    original = source.encode("cp932")
    encoded = target.encode("cp932")
    field = struct.pack("<I", len(original)) + original
    if data.count(field) != 1:
        raise ValueError("Expected exactly one caption field")
    if width is None:
        if len(encoded) > len(original):
            raise ValueError("Longer caption requires an explicit canvas width")
        encoded = encoded.ljust(len(original), b" ")
    offset = data.index(field)
    result = bytearray(data[:offset] + struct.pack("<I", len(encoded)) + encoded + data[offset + len(field):])
    if width is not None:
        original_width = struct.unpack_from("<I", data, 13)[0]
        if width < original_width:
            raise ValueError("Canvas must not shrink")
        marker = struct.pack("<I", original_width)
        offsets = [position for position in range(len(result)) if result.startswith(marker, position)]
        if len(offsets) != 3 or offsets[0] != 13:
            raise ValueError("Expected canvas and two rectangle-width fields")
        for position in offsets:
            struct.pack_into("<I", result, position, width)
    return bytes(result)


def main():
    from livemaker.archive import LMArchive

    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with LMArchive(args.game) as archive:
        for name, japanese, english, width in JOBS:
            relative = "グラフィック/リファレンス/" + name + ".lcm"
            source = archive.read(relative.replace("/", "\\"))
            destination = args.output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(patch_caption(source, japanese, english, width))
    print("Repaired three complete captions; fonts, colors and timing retained")


if __name__ == "__main__":
    main()
