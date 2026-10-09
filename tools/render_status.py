"""Render status.svg: how much of the translation WORK is done, as one gradient bar.

"Work" = estimated token spend, not text volume: the remaining story scripts, the in-game pictures
(menus, letters, documents that need typesetting) and a final check all count. Update the numbers
below after each part or picture batch (BACKLOG actuals / estimates), rerun, commit the svg.
The picture shows ONE percent rounded to the nearest 5 and two rounded token figures. No script
counts, no titles, no section labels: it must not reveal the game's size or structure.
Run: python tools/render_status.py  (stdlib only)
"""
import pathlib

SPENT_M = 100            # million tokens spent so far (parts 1-23 + side work; parts before the board estimated)
REMAINING_M = {          # million tokens still to spend, by kind
    "story text": 11,    # the last story scripts at the recent all-in rate (~2.7M per 1,000 cells)
    "pictures": 7,       # picture batches parked on the board
    "checks": 2,         # handwriting re-read, report pictures, final sweep
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
left = sum(REMAINING_M.values())
pct = 5 * round(100 * SPENT_M / (SPENT_M + left) / 5)
pct = min(pct, 95) if left > 0 else 100
word = "complete" if pct == 100 else f"about {pct}%"
spent_r = 10 * round(SPENT_M / 10)
left_r = 5 * round(left / 5)

W, H, PAD = 680, 132, 20
BAR_Y, BAR_H = 46, 22
GREY, INK, HEAD = "#d0d7de", "#57606a", "#1f2328"
fill_w = (W - 2 * PAD) * pct / 100
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
       '<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#1a7f37"/><stop offset="1" stop-color="#56d364"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" rx="8" fill="#ffffff"/>',
       f'<text x="{PAD}" y="{PAD + 10}" font-size="16" font-weight="600" fill="{HEAD}">Translation progress: {word} of the work is done</text>',
       f'<rect x="{PAD}" y="{BAR_Y}" width="{W - 2*PAD}" height="{BAR_H}" rx="{BAR_H//2}" fill="{GREY}"/>',
       f'<rect x="{PAD}" y="{BAR_Y}" width="{fill_w:.1f}" height="{BAR_H}" rx="{BAR_H//2}" fill="url(#g)"/>',
       f'<text x="{PAD + fill_w - 10:.1f}" y="{BAR_Y + 16}" text-anchor="end" font-size="13" font-weight="700" fill="#ffffff">{pct}%</text>',
       f'<text x="{PAD}" y="{H - PAD - 14}" font-size="12" fill="{INK}">Work = AI token spend. Roughly {spent_r} million tokens spent, about {left_r} million to go.</text>',
       f'<text x="{PAD}" y="{H - PAD + 4}" font-size="12" fill="{INK}">Left: the last story scripts, the in-game pictures (menus, letters, documents), a final check.</text>',
       "</svg>"]
(ROOT / "status.svg").write_text("\n".join(out), encoding="utf-8")
print(f"status.svg: {word} ({SPENT_M}M spent, ~{left}M left)")
