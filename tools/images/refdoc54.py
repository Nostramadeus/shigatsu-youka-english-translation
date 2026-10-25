"""Expand the first class-report cell without changing page dimensions.

Run before batch.py --jobs jobs_refdocs --only ref54, using the normal source/output PNG paths.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
PAGE = "グラフィック/リファレンス/リファレンス詳細/rrr54/0.png"


def expand_first_cell(source):
    output = source.copy()
    first_rule = source.crop((68, 422, 719, 424))
    second_rule = source.crop((68, 456, 719, 458))
    paper = source.getpixel((400, 435))
    for box in [(69, 326, 718, 448), (69, 450, 718, 478), (69, 480, 718, 554),
                (69, 589, 718, 686), (69, 720, 718, 818), (69, 853, 718, 949)]:
        output.paste(paper, box)
    output.paste(paper, (69, 422, 718, 424))
    output.paste(paper, (69, 456, 718, 458))
    output.paste(paper, (67, 455, 70, 478))
    output.paste(paper, (717, 455, 720, 478))
    draw = ImageDraw.Draw(output)
    for column in (68, 718):
        draw.line((column, 423, column, 449), fill=source.getpixel((column, 400)))
    output.paste(first_rule, (68, 448))
    output.paste(second_rule, (68, 478))
    return output


def main():
    source = ROOT / "work/images/png" / PAGE
    target = ROOT / "work/images/out" / PAGE
    target.parent.mkdir(parents=True, exist_ok=True)
    expand_first_cell(Image.open(source).convert("RGBA")).save(target)
    print("Prepared reference 54 first-cell expansion; next run its batch job.")


if __name__ == "__main__":
    main()
