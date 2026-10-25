"""Translate the photo-turn caption literally, retaining all eight original frames."""
import argparse
import hashlib
import json
from pathlib import Path
import zlib

import cv2
import numpy as np
from PIL import Image
import livemaker.GalImagePlugin

import gal_write
import refdoc_flip
import typeset_ui


def decode(path):
    data = Path(path).read_bytes()
    xml, root, blobs = gal_write.parse_galx(data)
    if int(root.get("Bpp")) != 24 or int(root.get("CompType")) != 0 or int(root.get("BlockWidth")):
        raise ValueError("Only the verified unblocked 24-bit ZIP animation layout is supported")
    frames = []
    for frame_index, layer, layers, pixels, alpha in blobs:
        width, height = int(layers.get("Width")), int(layers.get("Height"))
        stride = (width * 3 + 3) & ~3
        raw = zlib.decompress(pixels)
        if len(raw) != stride * height:
            raise ValueError("Unexpected animation row stride")
        rgb = np.frombuffer(raw, np.uint8).reshape(height, stride)[:, :width * 3].reshape(height, width, 3)[:, :, ::-1].copy()
        if alpha:
            raw_alpha = zlib.decompress(alpha)
            alpha_stride = (width + 3) & ~3
            if len(raw_alpha) != alpha_stride * height:
                raise ValueError("Unexpected animation alpha stride")
            opacity = np.frombuffer(raw_alpha, np.uint8).reshape(height, alpha_stride)[:, :width]
        else:
            if int(layer.get("AlphaOn", 0)):
                raise ValueError("Missing required alpha plane")
            opacity = np.full((height, width), 255, np.uint8)
            transparent = int(layer.get("TransColor", -1))
            if transparent >= 0:
                key = [transparent & 255, (transparent >> 8) & 255, (transparent >> 16) & 255]
                opacity[np.all(rgb == key, axis=2)] = 0
        if frame_index != len(frames):
            raise ValueError("Unexpected multi-layer animation")
        frames.append(np.dstack((rgb, opacity)))
    return xml, blobs, frames


def caption(frame):
    height, width = frame.shape[:2]
    corners, _ = refdoc_flip.quad(frame[:, :, 3])
    center = corners.mean(axis=0)
    corners = corners[np.argsort(np.arctan2(corners[:, 1] - center[1], corners[:, 0] - center[0]))]
    corners = np.roll(corners, -int(np.argmin(corners.sum(axis=1))), axis=0).astype(np.float32)
    matrix = cv2.getPerspectiveTransform(np.float32([[0, 0], [444, 0], [444, 300], [0, 300]]), corners)
    region = np.zeros((300, 444), np.uint8)
    region[246:299, 168:444] = 255
    allowed = cv2.warpPerspective(region, matrix, (width, height), flags=cv2.INTER_NEAREST) > 0
    dark = np.max(frame[:, :, :3], axis=2) < 180
    erase = cv2.dilate((allowed & dark).astype(np.uint8), np.ones((3, 3), np.uint8))
    erase[~allowed] = 0
    cleaned = cv2.inpaint(frame[:, :, :3][:, :, ::-1].copy(), erase * 255, 3, cv2.INPAINT_TELEA)[:, :, ::-1]
    layer = Image.new("RGBA", (444, 300), (0, 0, 0, 0))
    size, lines = typeset_ui.draw_text(layer, dict(string="Akane and Mifuyu-chan's entrance ceremony",
        font="C:/Windows/Fonts/Inkfree.ttf", box=[170, 247, 440, 298], max_size=16,
        color="#3c352c", align="left", line_spacing=1.05))
    if size < 16:
        raise ValueError("Caption does not fit at the accepted 16px size")
    warped = cv2.warpPerspective(np.array(layer), matrix, (width, height), flags=cv2.INTER_LINEAR)
    opacity = warped[:, :, 3:4].astype(float) / 255
    result = frame.copy()
    result[:, :, :3] = np.round(warped[:, :, :3] * opacity + cleaned * (1 - opacity)).astype(np.uint8)
    changed = np.any(result != frame, axis=2)
    if np.any(changed & ~cv2.dilate(allowed.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)):
        raise ValueError("Caption changed unrelated pixels")
    if not np.array_equal(result[:, :, 3], frame[:, :, 3]):
        raise ValueError("Animation opacity changed")
    return result, dict(corners=corners.tolist(), font_pixels=size, lines=lines,
                        changed_pixels=int(changed.sum()), unchanged_outside_caption=True)


def build(source, output, evidence):
    source, output, evidence = Path(source), Path(output), Path(evidence)
    xml, original_blobs, frames = decode(source)
    if len(frames) != 8:
        raise ValueError("Expected exactly eight photo-turn frames")
    first = np.array(Image.open(source).convert("RGBA"))
    if not np.array_equal(first[:, :, :3], frames[0][:, :, :3]):
        raise ValueError("Decoder does not match the standard plugin's first frame")
    if int(original_blobs[0][1].get("AlphaOn", 0)) and not np.array_equal(first, frames[0]):
        raise ValueError("Decoder does not match the standard plugin's first alpha plane")
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    output.write_bytes(source.read_bytes())
    selected = (4, 5, 6, 7) if source.stem == "0→1" else (0, 1, 2, 3)
    records = []
    for index in selected:
        english, record = caption(frames[index])
        png = evidence / ("frame-%d.png" % index)
        Image.fromarray(english, "RGBA").save(png)
        gal_write.write_gal(output, png, output, "keep", None, index)
        records.append(dict(frame=index, **record))
    final_xml, final_blobs, final_frames = decode(output)
    if final_xml != xml:
        raise ValueError("Animation timing or structural metadata changed")
    for index in range(8):
        if index not in selected:
            if final_blobs[index][3:] != original_blobs[index][3:]:
                raise ValueError("Untouched animation frame blob changed")
        else:
            expected = np.array(Image.open(evidence / ("frame-%d.png" % index)).convert("RGBA"))
            if not np.array_equal(final_frames[index], expected):
                raise ValueError("ZIP animation frame round-trip is not pixel-exact")
        Image.fromarray(final_frames[index], "RGBA").save(evidence / ("final-%d.png" % index))
    report = dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                  frame_count=8, metadata_identical=True, unchanged_frames_exact=True,
                  modified_frames_pixel_exact=True, caption="Akane and Mifuyu-chan's entrance ceremony",
                  source_date="/4/6 and pale patch unchanged", frames=records, pixel_review="pending")
    (evidence / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("evidence")
    args = parser.parse_args()
    report = build(args.source, args.output, args.evidence)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
