"""Derive bankbook turn states from accepted faces, preserving source shading/art."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

from refdoc_surface import carry


GEOMETRY = {
    "01": ("C", [[45, 0], [545, 0], [590, 319], [0, 319]], None),
    "02": ("C", [[101, 0], [600, 0], [700, 287], [0, 287]], [101, 2]),
    "03": ("C", [[156, 0], [654, 0], [810, 203], [0, 203]], [155, 0]),
    "04": ("C", [[194, 0], [696, 0], [890, 76], [0, 76]], [196, 1]),
    "05": ("T", [[0, 0], [877, 0], [685, 77], [184, 77]], [184, 77]),
    "06": ("T", [[1, 0], [811, 0], [657, 208], [151, 208]], [153, 205]),
    "07": ("T", [[0, 0], [700, 0], [602, 293], [98, 293]], [100, 291]),
    "08": ("T", [[0, 0], [585, 0], [541, 318], [43, 318]], [42, 318]),
    "09": ("T", [[0, 0], [545, 0], [521, 321], [24, 321]], [23, 321]),
    "10": ("T", [[0, 0], [645, 0], [573, 320], [73, 320]], [73, 311]),
    "11": ("T", [[0, 0], [751, 0], [625, 250], [125, 250]], [125, 250]),
    "12": ("T", [[1, 0], [869, 0], [686, 150], [182, 150]], [184, 148]),
    "14": ("C", [[198, 0], [702, 0], [900, 76], [0, 76]], [200, 0]),
    "15": ("C", [[182, 0], [686, 0], [866, 146], [0, 146]], [184, 4]),
    "16": ("C", [[129, 0], [632, 0], [760, 254], [0, 254]], [131, 3]),
    "17": ("C", [[74, 0], [586, 0], [660, 318], [0, 318]], None),
    "18": ("C", [[24, 0], [547, 0], [570, 335], [0, 335]], None),
}


def load(path):
    return np.array(Image.open(path).convert("RGBA"))


def build(source, english, output, evidence):
    source, english, output, evidence = map(Path, (source, english, output, evidence))
    output.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    original_page, english_page = load(source / "1.png"), load(english / "1.png")
    pieces = {"C": (load(source / "0.png"), load(english / "0.png")),
              "T": (original_page[:310], english_page[:310]), "B": (original_page[310:], english_page[310:])}
    records = []
    for name, (flap, corners, bottom) in GEOMETRY.items():
        frame = load(source / (name + ".png"))
        original, accepted = pieces[flap]
        transformed, selected, coverage, record = carry(original, accepted, frame, corners)
        result, union = frame.copy(), selected.copy()
        details = {flap: record}
        if bottom is not None:
            column, row = bottom
            original, accepted = pieces["B"]
            corners_bottom = [[column, row], [column + 500, row],
                              [column + 500, row + 310], [column, row + 310]]
            visible = coverage < 1
            transferred, bottom_selected, _, details["B"] = carry(original, accepted, frame, corners_bottom, visible)
            result[bottom_selected] = transferred[bottom_selected]
            union |= bottom_selected
        result[selected] = transformed[selected]
        if not np.array_equal(result[:, :, 3], frame[:, :, 3]) or not np.array_equal(result[~union], frame[~union]):
            raise ValueError("Original alpha or unrelated artwork changed")
        target = output / (name + ".png")
        Image.fromarray(result, "RGBA").save(target)
        pair = Image.new("RGBA", (frame.shape[1] * 2, frame.shape[0]), "white")
        pair.alpha_composite(Image.fromarray(frame, "RGBA"))
        pair.alpha_composite(Image.fromarray(result, "RGBA"), (frame.shape[1], 0))
        pair.convert("RGB").save(evidence / (name + "-pair.png"))
        records.append(dict(frame=name, pieces=details, dimensions=[frame.shape[1], frame.shape[0]],
            alpha_identical=True, unrelated_pixels_identical=True, output_png=str(target),
            png_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), pixel_review="pending"))
        print(name, {piece: round(value["fitted_residual"], 2) for piece, value in details.items()})
    (evidence / "report.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8", newline="\n")
    return records


def main():
    parser = argparse.ArgumentParser()
    for argument in ("source", "english", "output", "evidence"):
        parser.add_argument(argument)
    args = parser.parse_args()
    build(args.source, args.english, args.output, args.evidence)


if __name__ == "__main__":
    main()
