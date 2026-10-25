"""Carry the accepted police-ID lettering into both eight-frame wallet turns."""
import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

import gal_frames
from refdoc_surface import carry


def feature_corners(original, frame):
    sift = cv2.SIFT_create()
    first, descriptors = sift.detectAndCompute(cv2.cvtColor(original[:, :, :3], cv2.COLOR_RGB2GRAY), None)
    second, target = sift.detectAndCompute(cv2.cvtColor(frame[:, :, :3], cv2.COLOR_RGB2GRAY),
                                          (frame[:, :, 3] > 128).astype(np.uint8))
    good = [left for left, right in cv2.BFMatcher().knnMatch(descriptors, target, k=2)
            if left.distance < .75 * right.distance]
    matrix, inliers = cv2.findHomography(np.float32([first[match.queryIdx].pt for match in good]),
        np.float32([second[match.trainIdx].pt for match in good]), cv2.RANSAC, 2)
    if matrix is None or int(inliers.sum()) < 50:
        raise ValueError("Insufficient feature registration; measured geometry is required")
    height, width = original.shape[:2]
    return cv2.perspectiveTransform(np.float32([[[0, 0], [width, 0], [width, height], [0, height]]]), matrix)[0]


def build(source, original_png, english_png, output, evidence):
    source, output, evidence = Path(source), Path(output), Path(evidence)
    frames = gal_frames.decode(source)[2]
    if len(frames) != 8:
        raise ValueError("Expected eight wallet-turn frames")
    first = np.array(Image.open(source).convert("RGBA"))
    if not np.array_equal(first, frames[0]):
        raise ValueError("Source decoder differs from the standard first-frame decoder")
    original = np.array(Image.open(original_png).convert("RGBA"))
    english = np.array(Image.open(english_png).convert("RGBA"))
    pieces = {"T": (original[:420], english[:420]), "B": (original[420:], english[420:])}
    if not source.stem.endswith(("0→1", "1→0")):
        raise ValueError("Expected the named forward or reverse wallet turn")
    forward = source.stem.endswith("0→1")
    selected_frames = range(3, 8) if forward else range(5)
    evidence.mkdir(parents=True, exist_ok=True)
    results, records = [frame.copy() for frame in frames], []
    for index in selected_frames:
        frame = frames[index]
        union = np.zeros(frame.shape[:2], bool)
        details = {}
        for piece in ("B", "T"):
            if piece == "T" and ((forward and index == 3) or (not forward and index == 4)):
                continue
            original_piece, english_piece = pieces[piece]
            if piece == "T" and ((forward and index in (4, 5)) or (not forward and index in (2, 3))):
                depth = 94 if (forward and index == 4) or (not forward and index == 3) else 251
                corners = [[26, 0], [417, 0], [368, depth], [72, depth]]
            else:
                corners = feature_corners(original_piece, frame)
            transformed, selected, _, record = carry(original_piece, english_piece, frame, corners)
            results[index][selected] = transformed[selected]
            union |= selected
            details[piece] = record
        if not np.array_equal(results[index][:, :, 3], frame[:, :, 3]) or not np.array_equal(results[index][~union], frame[~union]):
            raise ValueError("Wallet alpha or unrelated art changed")
        records.append(dict(frame=index, pieces=details, unrelated_pixels_identical=True, alpha_identical=True))
        print(index, {piece: round(record["fitted_residual"], 2) for piece, record in details.items()})
    gal_frames.write_lossless(source, output, results)
    checked = gal_frames.decode(output)[2]
    for index, (original_frame, final_frame) in enumerate(zip(frames, checked)):
        Image.fromarray(final_frame, "RGBA").save(evidence / ("final-%d.png" % index))
        pair = Image.new("RGBA", (880, 832), "white")
        pair.alpha_composite(Image.fromarray(original_frame, "RGBA"))
        pair.alpha_composite(Image.fromarray(final_frame, "RGBA"), (440, 0))
        pair.convert("RGB").save(evidence / ("pair-%d.png" % index))
    report = dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(), frame_count=8,
        all_frames_pixel_exact=True, source_alpha_identical=True, unchanged_frames_pixel_exact=True,
        metadata_changes="compression only: unblocked ZIP; all timing, layer, transparency and frame settings retained",
        frames=records, pixel_review="pending")
    (evidence / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    for argument in ("source", "original_png", "english_png", "output", "evidence"):
        parser.add_argument(argument)
    args = parser.parse_args()
    build(args.source, args.original_png, args.english_png, args.output, args.evidence)


if __name__ == "__main__":
    main()
