"""Render status.svg: how much of the game's text is in English, as a bar and a 10x10 grid.

Inputs: line-counts.tsv (every script id with its Japanese character count) and tools/ship-list.txt
(the files that go into the patch). The picture shows ONE number, rounded to the nearest 5 percent.
No script counts, no titles, no section labels: it must not reveal the game's size or structure.
Run: python tools/render_status.py  (stdlib only)
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
rows = [l.split("\t") for l in (ROOT / "line-counts.tsv").read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
scripts = [(r[0][:-4], int(r[2])) for r in rows]
shipped = set(re.findall(r"\b([0-9A-F]{8})\.lsb\b", (ROOT / "tools/ship-list.txt").read_text(encoding="utf-8")))

total = sum(c for _, c in scripts)
done = sum(c for i, c in scripts if i in shipped)
pct = 5 * round(100 * done / total / 5)          # nearest 5 percent
pct = min(pct, 100 if done == total else 95)      # 100 only when every script ships

PAD, CELL, GAP, COLS = 20, 22, 5, 10
GRID_W = COLS * (CELL + GAP) - GAP
W = PAD * 2 + 420
GRID_X = (W - GRID_W) // 2
BAR_Y = PAD + 30
GRID_Y = BAR_Y + 44
H = GRID_Y + GRID_W + PAD + 24
GREEN, GREEN2, GREY, INK = "#2ea043", "#56d364", "#d0d7de", "#57606a"
word = "complete" if pct == 100 else f"about {pct}%"

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">',
       f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN2}"/></linearGradient></defs>',
       f'<rect width="{W}" height="{H}" rx="8" fill="#ffffff"/>',
       f'<text x="{W//2}" y="{PAD + 12}" text-anchor="middle" font-size="16" font-weight="600" fill="#1f2328">Translation status: {word} of the game\'s text is in English</text>',
       f'<rect x="{PAD}" y="{BAR_Y}" width="{W - 2*PAD}" height="14" rx="7" fill="{GREY}"/>',
       f'<rect x="{PAD}" y="{BAR_Y}" width="{(W - 2*PAD) * pct / 100:.1f}" height="14" rx="7" fill="url(#g)"/>']
for k in range(100):
    x = GRID_X + (k % COLS) * (CELL + GAP)
    y = GRID_Y + (k // COLS) * (CELL + GAP)
    out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{GREEN if k < pct else GREY}"/>')
out.append(f'<text x="{W//2}" y="{H - PAD + 2}" text-anchor="middle" font-size="12" fill="{INK}">'
           f'Each square is one percent of the text. <tspan fill="{GREEN}" font-weight="600">■</tspan> in English  '
           f'<tspan fill="#8c959f" font-weight="600">■</tspan> still Japanese</text>')
out.append("</svg>")
(ROOT / "status.svg").write_text("\n".join(out), encoding="utf-8")
print(f"status.svg: {word} (exact {100*done/total:.1f}%)")
