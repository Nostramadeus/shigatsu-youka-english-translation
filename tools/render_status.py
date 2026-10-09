"""Render status.svg: one square per game script, green = shipped in the English patch, grey = not yet.

Inputs: line-counts.tsv (every script id with its Japanese character count) and tools/ship-list.txt
(the files that go into the patch). No titles, no arc names, no section labels: the picture must not
spoil the game's structure. Run: python tools/render_status.py  (stdlib only)
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [l.split("\t") for l in (ROOT / "line-counts.tsv").read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
scripts = [(r[0][:-4], int(r[2])) for r in rows]          # (id, jp_chars), file order
shipped = set(re.findall(r"\b([0-9A-F]{8})\.lsb\b", (ROOT / "tools/ship-list.txt").read_text(encoding="utf-8")))

total = sum(c for _, c in scripts)
done = sum(c for i, c in scripts if i in shipped)
n_done = sum(1 for i, _ in scripts if i in shipped)
pct = round(100 * done / total)

COLS, CELL, GAP, PAD = 30, 14, 3, 16
rows_n = -(-len(scripts) // COLS)
W = PAD * 2 + COLS * (CELL + GAP) - GAP
BAR_Y = PAD
GRID_Y = BAR_Y + 54
H = GRID_Y + rows_n * (CELL + GAP) - GAP + PAD + 28
GREEN, GREY, INK = "#2ea043", "#d0d7de", "#57606a"

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
       f'<rect width="{W}" height="{H}" rx="8" fill="#ffffff"/>',
       f'<text x="{PAD}" y="{BAR_Y + 14}" font-size="15" font-weight="600" fill="#1f2328">Translation status: {pct}% of the game\'s text is in English</text>',
       f'<rect x="{PAD}" y="{BAR_Y + 24}" width="{W - 2*PAD}" height="12" rx="6" fill="{GREY}"/>',
       f'<rect x="{PAD}" y="{BAR_Y + 24}" width="{(W - 2*PAD) * done / total:.1f}" height="12" rx="6" fill="{GREEN}"/>']
for k, (sid, _) in enumerate(scripts):
    x = PAD + (k % COLS) * (CELL + GAP)
    y = GRID_Y + (k // COLS) * (CELL + GAP)
    out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{GREEN if sid in shipped else GREY}"/>')
out.append(f'<text x="{PAD}" y="{H - PAD + 4}" font-size="12" fill="{INK}">One square per script file, in file order. '
           f'<tspan fill="{GREEN}" font-weight="600">■</tspan> {n_done} translated and shipped  '
           f'<tspan fill="#8c959f" font-weight="600">■</tspan> {len(scripts) - n_done} not yet.  Percent is by Japanese character count.</text>')
out.append("</svg>")
(ROOT / "status.svg").write_text("\n".join(out), encoding="utf-8")
print(f"status.svg: {n_done}/{len(scripts)} scripts, {pct}% of text ({done}/{total} chars)")
