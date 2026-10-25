"""Read one-layer GaleX200 animation frames, including previous-frame blocks."""
import io
from pathlib import Path
import re
import struct
import zlib

import numpy as np
from PIL import Image

import gal_write


def unpack_blocks(packed, width, height, channels, block_width, block_height, previous):
    stride = (width * channels + 3) & ~3
    if not block_width and not block_height:
        if len(packed) != stride * height:
            raise ValueError("Unexpected unblocked plane size")
        return packed
    if block_width <= 0 or block_height <= 0:
        raise ValueError("Invalid block dimensions")
    columns = (width + block_width - 1) // block_width
    rows = (height + block_height - 1) // block_height
    header_size = columns * rows * 8
    if len(packed) < header_size:
        raise ValueError("Truncated block reference table")
    references = list(struct.iter_unpack("<ii", packed[:header_size]))
    position = header_size
    output = bytearray(stride * height)
    for index, (frame_reference, layer_reference) in enumerate(references):
        column, row = index % columns * block_width, index // columns * block_height
        run_width, run_height = min(block_width, width - column), min(block_height, height - row)
        destination = row * stride + column * channels
        chunk_size = run_width * channels
        if frame_reference == -1:
            for offset in range(run_height):
                chunk = packed[position:position + chunk_size]
                if len(chunk) != chunk_size:
                    raise ValueError("Truncated raw block")
                target = destination + offset * stride
                output[target:target + chunk_size] = chunk
                position += chunk_size
        else:
            if frame_reference == -2:
                if not 0 <= layer_reference < index:
                    raise ValueError("Invalid same-layer block reference")
                source = (layer_reference // columns * block_height * stride +
                          layer_reference % columns * block_width * channels)
                reference = output
            else:
                if not 0 <= frame_reference < len(previous) or layer_reference != 0:
                    raise ValueError("Invalid previous-frame layer reference")
                reference, source = previous[frame_reference], destination
                if len(reference) != len(output):
                    raise ValueError("Previous-frame dimensions differ")
            for offset in range(run_height):
                chunk = reference[source + offset * stride:source + offset * stride + chunk_size]
                if len(chunk) != chunk_size:
                    raise ValueError("Block reference exceeds plane")
                target = destination + offset * stride
                output[target:target + chunk_size] = chunk
    if position != len(packed):
        raise ValueError("Unexpected trailing block data")
    return bytes(output)


def decode(path):
    xml, root, blobs = gal_write.parse_galx(Path(path).read_bytes())
    compression = int(root.get("CompType"))
    if int(root.get("Bpp")) != 24 or compression not in (0, 2) or int(root.get("Randomized", 0)):
        raise ValueError("Unsupported animation pixel format")
    block_width, block_height = int(root.get("BlockWidth", 0)), int(root.get("BlockHeight", 0))
    frames, raw_frames, alpha_frames = [], [], []
    for frame_index, layer, layers, pixels, alpha in blobs:
        if frame_index != len(frames) or int(layer.get("Left", 0)) or int(layer.get("Top", 0)):
            raise ValueError("Expected one origin-aligned layer per frame")
        width, height = int(layers.get("Width")), int(layers.get("Height"))
        stride, alpha_stride = (width * 3 + 3) & ~3, (width + 3) & ~3
        if compression == 2:
            if block_width or block_height:
                raise ValueError("Blocked JPEG is unsupported")
            image = Image.open(io.BytesIO(pixels)).convert("RGB")
            if image.size != (width, height):
                raise ValueError("JPEG dimensions differ")
            rgb = np.array(image)
            raw = b"".join(rgb[:, :, ::-1][row].tobytes() + bytes(stride - width * 3)
                           for row in range(height))
        else:
            raw = unpack_blocks(zlib.decompress(pixels), width, height, 3, block_width, block_height, raw_frames)
            rgb = np.frombuffer(raw, np.uint8).reshape(height, stride)[:, :width * 3].reshape(height, width, 3)[:, :, ::-1].copy()
        raw_frames.append(raw)
        if int(layer.get("AlphaOn", 0)):
            if not alpha:
                raise ValueError("Missing required alpha plane")
            raw_alpha = unpack_blocks(zlib.decompress(alpha), width, height, 1,
                                      block_width, block_height, alpha_frames)
            opacity = np.frombuffer(raw_alpha, np.uint8).reshape(height, alpha_stride)[:, :width]
        else:
            raw_alpha = bytes(alpha_stride * height)
            opacity = np.full((height, width), 255, np.uint8)
            transparent = int(layer.get("TransColor", -1))
            if transparent >= 0:
                key = [transparent & 255, (transparent >> 8) & 255, (transparent >> 16) & 255]
                opacity[np.all(rgb == key, axis=2)] = 0
        alpha_frames.append(raw_alpha)
        frames.append(np.dstack((rgb, opacity)))
    return xml, blobs, frames


def write_lossless(source, output, frames):
    xml, blobs, original_frames = decode(source)
    if len(frames) != len(original_frames):
        raise ValueError("Frame count changed")
    updated_xml = re.sub(rb'BlockWidth="\d+"', b'BlockWidth="0"', xml, count=1)
    updated_xml = re.sub(rb'BlockHeight="\d+"', b'BlockHeight="0"', updated_xml, count=1)
    updated_xml = re.sub(rb'CompType="\d+"', b'CompType="0"', updated_xml, count=1)
    header = zlib.compress(updated_xml, 9)
    result = bytearray(b"GaleX200" + gal_write.p32(len(header)) + header)
    for frame, original, (_, layer, _, _, alpha) in zip(frames, original_frames, blobs):
        if frame.shape != original.shape:
            raise ValueError("Frame dimensions changed")
        image = Image.fromarray(frame, "RGBA")
        pixels = gal_write.encode_layer(image, 0, 0)
        if int(layer.get("AlphaOn", 0)):
            alpha = gal_write.encode_alpha(image)
        elif alpha:
            raise ValueError("Ignored nonempty alpha plane requires explicit handling")
        result += gal_write.p32(len(pixels)) + pixels + gal_write.p32(len(alpha or b"")) + (alpha or b"")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)
    checked_xml, _, checked_frames = decode(output)
    if checked_xml != updated_xml or not all(np.array_equal(expected, actual)
                                            for expected, actual in zip(frames, checked_frames)):
        raise ValueError("Lossless animation round-trip changed pixels or metadata")
