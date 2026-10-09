"""Render a blind bake-off reading page: JP | A | B, one row per JP text line.

Usage (stdlib only):
  uv run --no-project --python 3.12 python tools/render_bakeoff.py <scene_id> <dirA> <dirB> [--dump]
Writes review/bakeoff-<scene_id>.html and review/bakeoff-<scene_id>-verdict.html
(the latter from notes/v2/BAKEOFF-VERDICT.md, if present). --dump prints a plain
text triplet view instead of writing HTML.
File reading order comes from lns/<scene_id>.lsbref.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r"<[^>]*>")
NL = chr(10)  # files use CR CR LF or LF; read bytes, drop CR, split on LF only


def order(scene):
    names = []
    for ln in (ROOT / "lns" / f"{scene}.lsbref").read_bytes().decode("utf-8").replace(chr(13), "").split(NL):
        ln = ln.strip()
        if ln:
            names.append(ln.split(":")[0])
    return names


def clean(line):
    """Tags stripped; <BR> -> line break, <PG> -> end of page. Returns plain text."""
    s = line.replace("<BR>", "\n").replace("<PG>", "")
    s = TAG.sub("", s)
    return s.strip("\n")


def text_lines(path):
    """(line_number, raw) for every line holding visible text."""
    out = []
    for i, raw in enumerate(path.read_bytes().decode("utf-8").replace(chr(13), "").split(NL), 1):
        if raw.startswith(";") or raw.startswith("{"):
            continue
        if clean(raw).strip():
            out.append((i, raw))
    return out


def rows(scene, dir_a, dir_b):
    res = []
    for name in order(scene):
        jp_path = ROOT / "lns" / name
        a_lines = (ROOT / dir_a / name).read_bytes().decode("utf-8").replace(chr(13), "").split(NL)
        b_lines = (ROOT / dir_b / name).read_bytes().decode("utf-8").replace(chr(13), "").split(NL)
        for i, raw in text_lines(jp_path):
            res.append((name, i, clean(raw), clean(a_lines[i - 1]), clean(b_lines[i - 1])))
    return res


def cell(s):
    return html.escape(s).replace("\n", "<br>")


CSS = """
body{font-family:Georgia,'Times New Roman',serif;font-size:1.1em;line-height:1.55;margin:0;background:#fbf8f2;color:#222}
header{position:sticky;top:0;background:#2b2b2b;color:#fff;padding:.7em 1.2em;display:flex;gap:1.5em;align-items:center;z-index:2}
header h1{font-size:1.05em;margin:0;font-weight:normal}
header label{font-size:.9em;cursor:pointer}
main{padding:1em 1.2em;max-width:110em;margin:auto}
table{border-collapse:collapse;width:100%}
th{text-align:left;background:#e9e2d4;padding:.4em .6em;position:sticky;top:2.6em}
td{vertical-align:top;padding:.45em .6em;border-bottom:1px solid #e2dccf}
td.n{color:#999;font-size:.75em;white-space:nowrap}
td.jp{font-family:'Yu Mincho','MS Mincho',serif;width:30%}
body.nojp .jp{display:none}
tr:hover td{background:#f3eee3}
"""


def page(scene, dir_a, dir_b):
    rs = rows(scene, dir_a, dir_b)
    out = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        f"<title>Bake-off {scene}</title><style>{CSS}</style></head><body>",
        "<header><h1>Scene 1: two blind versions. Key: notes/v2/BAKEOFF-KEY.md</h1>",
        "<label><input type='checkbox' id='jp' checked onchange=\"document.body.classList.toggle('nojp',!this.checked)\"> show Japanese</label>",
        f"<span style='font-size:.85em;opacity:.7'>{len(rs)} lines</span></header><main><table>",
        "<tr><th>#</th><th class='jp'>Japanese</th><th>A</th><th>B</th></tr>",
    ]
    for k, (_name, _i, jp, a, b) in enumerate(rs, 1):
        out.append(f"<tr><td class='n'>{k}</td><td class='jp'>{cell(jp)}</td><td>{cell(a)}</td><td>{cell(b)}</td></tr>")
    out.append("</table></main></body></html>")
    return "\n".join(out)


def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s


def md_to_html(md, title):
    out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title>",
           "<style>body{font-family:Georgia,serif;font-size:1.1em;line-height:1.6;max-width:52em;margin:2em auto;padding:0 1em;background:#fbf8f2;color:#222}"
           "table{border-collapse:collapse;margin:1em 0}td,th{border:1px solid #cfc7b6;padding:.35em .7em;text-align:left}th{background:#e9e2d4}"
           "code{background:#eee6d6;padding:0 .2em}li{margin:.3em 0}</style></head><body>"]
    lines = md.splitlines()
    i = 0
    in_list = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table>")
            for r, cells in enumerate(tbl):
                if r == 1 and all(set(c) <= set("-: ") for c in cells):
                    continue
                t = "th" if r == 0 else "td"
                out.append("<tr>" + "".join(f"<{t}>{inline(c)}</{t}>" for c in cells) + "</tr>")
            out.append("</table>")
            continue
        if ln.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(ln[2:])}</li>")
            i += 1
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        m = re.match(r"(#+) (.*)", ln)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif ln.strip():
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    if in_list:
        out.append("</ul>")
    out.append("</body></html>")
    return "\n".join(out)


def main():
    scene, dir_a, dir_b = sys.argv[1:4]
    if "--dump" in sys.argv:
        sys.stdout.reconfigure(encoding="utf-8")
        for k, (name, i, jp, a, b) in enumerate(rows(scene, dir_a, dir_b), 1):
            print(f"[{k}] {name.split('-')[1]}:{i}\nJ: {jp}\nA: {a}\nB: {b}\n")
        return
    rev = ROOT / "review"
    (rev / f"bakeoff-{scene}.html").write_text(page(scene, dir_a, dir_b), encoding="utf-8")
    verdict = ROOT / "notes" / "v2" / "BAKEOFF-VERDICT.md"
    if verdict.exists():
        (rev / f"bakeoff-{scene}-verdict.html").write_text(
            md_to_html(verdict.read_text(encoding="utf-8"), f"Bake-off verdict {scene}"), encoding="utf-8")


if __name__ == "__main__":
    main()
