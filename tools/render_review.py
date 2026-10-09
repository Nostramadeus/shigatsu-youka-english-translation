"""Side-by-side review page: `uv run tools/render_review.py <lsbid> [--lines N] [--shots DIR]`.
Reads lns/<id>-*.lns (JP) and $SY_EN_DIR/<id>-*.lns (EN, default lns-en-55) in .lsbref order, pairs text lines by position, and writes
review/<id>.html: line number, JP left, EN right, name colour kept (STYLE ID=1), dialogue colour (ID=2), one
screenshot column when --shots DIR holds 001.png, 002.png ... (one shot per click; click k = text line k).
Stdlib only.
"""
import re, sys, html, base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r'(<[^>]*>|\{[^}]*\})')

def parse_ref(lsbid, d):
    ref = (d / f'{lsbid}.lsbref').read_text(encoding='utf-8').split('\n')
    items = []
    for line in ref:
        if ':' in line and line.endswith(tuple('0123456789')):
            name, idx = line.rsplit(':', 1)
            items.append((int(idx), name.strip()))
    return [n for _, n in sorted(items)]

def text_lines(path):
    """Yield (lineno, raw) for lines that carry text (not pure command/comment lines)."""
    out = []
    for i, raw in enumerate(path.read_bytes().decode('utf-8').replace('\r', '').split('\n'), 1):
        if raw.startswith(';'):
            continue
        if TAG.sub('', raw).strip() == '':
            continue
        out.append((i, raw))
    return out

def render_cell(raw):
    parts, buf, style = [], [], None
    for tok in TAG.split(raw):
        if not tok:
            continue
        m = re.match(r'<STYLE ID="(\d+)">', tok)
        if m:
            style = m.group(1); continue
        if tok == '</STYLE>':
            style = None; continue
        if tok in ('<BR>',):
            parts.append('<br>'); continue
        if tok == '<PG>':
            parts.append('<span class="pg">▼</span>'); continue
        if TAG.fullmatch(tok):
            continue  # other tags/commands hidden
        cls = f' class="s{style}"' if style else ''
        parts.append(f'<span{cls}>{html.escape(tok)}</span>')
    return ''.join(parts)

def main(argv):
    lsbid = argv[0]
    limit = int(argv[argv.index('--lines') + 1]) if '--lines' in argv else 0
    shots = Path(argv[argv.index('--shots') + 1]) if '--shots' in argv else None
    # SY_EN_DIR picks the English tree (default lns-en-55 = the shipped Opus 5.5 tree since 2026-09-27; Fable 2026-10-01)
    import os
    jp_dir = ROOT / 'lns'
    en_dir = Path(os.environ['SY_EN_DIR']) if os.environ.get('SY_EN_DIR') else ROOT / 'lns-en-55'
    if not en_dir.is_absolute():
        en_dir = ROOT / en_dir
    order = parse_ref(lsbid, jp_dir)
    rows, n = [], 0
    for name in order:
        jp = text_lines(jp_dir / name)
        en_path = en_dir / name
        en = text_lines(en_path) if en_path.exists() else []
        en_map = dict(en)
        for lineno, raw in jp:
            n += 1
            if limit and n > limit:
                break
            e = en_map.get(lineno, '')
            shot = ''
            if shots:
                p = shots / f'{n:03d}.png'
                if p.exists():
                    b = base64.b64encode(p.read_bytes()).decode()
                    shot = f'<img src="data:image/png;base64,{b}" loading="lazy">'
            rows.append(f'<tr id="l{n}"><td class="n">{n}<small>{html.escape(name.split("-",1)[1][:-4])}:{lineno}</small></td>'
                        f'<td class="jp">{render_cell(raw)}</td><td class="en">{render_cell(e)}</td>'
                        + (f'<td class="shot">{shot}</td>' if shots else '') + '</tr>')
        if limit and n > limit:
            break
    out = ROOT / 'review' / f'{lsbid}.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(PAGE.format(id=lsbid, rows='\n'.join(rows), count=len(rows), shotcol='<th>screen</th>' if shots else ''), encoding='utf-8')
    print(f'wrote {out} ({len(rows)} lines)')

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Review {id}</title>
<style>
body{{font-family:"Segoe UI",system-ui,sans-serif;background:#14151a;color:#e8e6e1;margin:0;padding:1.5em}}
h1{{font-size:1.2em;font-weight:600;margin:0 0 .6em}} p.meta{{color:#9a9890;margin:0 0 1.2em}}
table{{border-collapse:collapse;width:100%}} th{{text-align:left;color:#9a9890;font-weight:500;padding:.3em .6em;border-bottom:1px solid #2c2e36;position:sticky;top:0;background:#14151a}}
td{{vertical-align:top;padding:.55em .6em;border-bottom:1px solid #22242b;line-height:1.55}}
td.n{{color:#6f6e68;width:3.5em;font-variant-numeric:tabular-nums}} td.n small{{display:block;font-size:.65em;color:#4d4c48}}
td.jp{{width:34%;font-family:"Yu Gothic","Meiryo","Noto Sans JP",sans-serif;font-size:1.02em}} td.en{{width:34%}}
td.shot{{width:26%}} td.shot img{{width:100%;border:1px solid #2c2e36;border-radius:4px}}
.s1{{color:#aaccff;font-weight:600}} .s2{{color:#ffd9aa}} .pg{{color:#4d4c48;font-size:.7em;margin-left:.3em}}
tr:hover td{{background:#1b1d24}}
</style></head><body>
<h1>{id} · JP / EN review</h1><p class="meta">Unofficial fan translation (非公式・二次創作). Not affiliated with New++. Private review page: never publish (shows the Japanese script).</p><p class="meta">{count} text lines. Blue = character name colour, orange = spoken text, ▼ = page break (click). Screenshot k = the screen after click k; small drift is possible.</p>
<table><thead><tr><th>#</th><th>Japanese</th><th>English</th>{shotcol}</tr></thead><tbody>
{rows}
</tbody></table></body></html>'''

if __name__ == '__main__':
    main(sys.argv[1:])
