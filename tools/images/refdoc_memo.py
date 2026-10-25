"""Readable full-page memo layout; overflow is an error, never a font reduction."""
from PIL import Image, ImageDraw, ImageFont

import typeset_ui


def flow(blocks, height):
    font = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 18)
    draw = ImageDraw.Draw(Image.new("RGB", (800, height)))
    line_height = sum(font.getmetrics())
    position = 4
    result = []
    for text in blocks:
        rows = typeset_ui.wrap(draw, text, font, 780, 0)
        bottom = position + len(rows) * line_height
        if bottom > height - 6:
            raise ValueError("Complete memo overflows at 18px; expand layout, never shorten meaning")
        result.append((text, [10, position, 790, bottom], {"max_size": 18, "erase": []}))
        position = bottom + 6
    result[0][2]["erase"] = [[1, 0, 799, height]]
    return result
