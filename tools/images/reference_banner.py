"""Translate the all-node completion banner, retaining its original underline."""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from gal_write import write_gal


TEXT = "All-node check complete"


def render(original):
    if original.size != (476, 60):
        raise ValueError("Unexpected completion-banner dimensions")
    output = original.convert("RGBA").copy()
    output.paste((0, 0, 0, 0), (0, 0, 476, 54))
    scale = 4
    overlay = Image.new("RGBA", (476 * scale, 54 * scale))
    draw = ImageDraw.Draw(overlay)
    font = ImageFont.truetype("C:/Windows/Fonts/cambriaz.ttf", 42 * scale)
    bounds = draw.textbbox((0, 0), TEXT, font=font, stroke_width=3 * scale)
    width, height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    if width > 466 * scale or height > 48 * scale:
        raise ValueError("Complete caption does not fit; do not shorten it")
    position = ((476 * scale - width) / 2 - bounds[0], 3 * scale - bounds[1])
    draw.text(position, TEXT, font=font, fill="#08113d", stroke_width=3 * scale, stroke_fill="#f5f137")
    output.alpha_composite(overlay.resize((476, 54), Image.Resampling.LANCZOS))
    if output.crop((0, 54, 476, 60)).tobytes() != original.convert("RGBA").crop((0, 54, 476, 60)).tobytes():
        raise ValueError("Original underline changed")
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    picture = render(Image.open(args.source).convert("RGBA"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    png = args.output.with_suffix(".png")
    picture.save(png)
    write_gal(args.source, png, args.output, comp_mode="zip")
    if Image.open(args.output).convert("RGBA").tobytes() != picture.tobytes():
        raise ValueError("Completion banner failed its lossless round trip")
    print("Full caption fits; original underline exact; GAL round trip exact")


if __name__ == "__main__":
    main()
