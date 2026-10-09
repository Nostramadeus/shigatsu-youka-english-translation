"""refdoc_scope.py - which reference-document pictures are in scope for the R+306 fence.

The tables have no 画像N column: the pictures are keyed by the reference ID and live at
  グラフィック\\リファレンス\\リファレンスサムネ\\rr<ID>.gal      thumbnail (list row)
  グラフィック\\リファレンス\\リファレンス概要\\rr<ID>.gal        the picture the reference screen shows
  グラフィック\\リファレンス\\リファレンス詳細\\rrr<ID>\\<n>.gal   the zoom / node close-ups
Fence: a row of リファレンスデータベース is reachable iff its 解禁シナリオ is one of the titles in
patch/titles-jp-en.tsv (the same test notes/_tmp/tbl.py uses, R + 306 = 34 scenarios).

Usage: refdoc_scope.py [--names OUT.txt]   prints the table and optionally writes the name list.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEP = chr(92)
OVER = "グラフィック" + SEP + "リファレンス" + SEP + "リファレンス概要" + SEP + "rr%s.gal"
THUMB = "グラフィック" + SEP + "リファレンス" + SEP + "リファレンスサムネ" + SEP + "rr%s.gal"
DETAIL = "グラフィック" + SEP + "リファレンス" + SEP + "リファレンス詳細" + SEP + "rrr%s" + SEP


def load(p, enc="cp932"):
    t = p.read_bytes().decode(enc).lstrip("﻿")
    nl = "\r\n" if "\r\n" in t else "\n"
    return [r.split("\t") for r in t.split(nl)]


def reachable():
    titles = {l.split("\t")[0] for l in
              (ROOT / "patch" / "titles-jp-en.tsv").read_text(encoding="utf-8").replace("\r", "").strip().split("\n")
              if l and not l.startswith("#")}
    rows = load(ROOT / "orig" / "データベース" / "リファレンスデータベース.tsv")
    h = rows[0]
    i_id, i_sc, i_t, i_f = h.index("ID"), h.index("解禁シナリオ"), h.index("タイトル"), h.index("形式")
    out = []
    for r in rows[1:]:
        if len(r) > i_sc and r[i_sc].strip() in titles:
            out.append((r[i_id].strip(), r[i_t].strip(), r[i_f].strip()))
    return sorted(out, key=lambda x: int(x[0]))


def archive():
    arc = (ROOT / "notes" / "_db" / "_archive-list.txt").read_bytes().decode("utf-8")
    ent = {}
    for line in arc.split("\r\n"):
        m = re.match(r"\s*(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+(.+)$", line)
        if m:
            ent[m.group(2)] = int(m.group(1))
    return ent


def main():
    ent = archive()
    reach = reachable()
    files, tot = [], 0
    print("%-5s %-10s %-3s %-3s %-6s %-8s %s" % ("ID", "format", "ov", "th", "detail", "KB", "title"))
    for rid, title, fmt in reach:
        ov, th = OVER % rid, THUMB % rid
        det = sorted(p for p in ent if p.startswith(DETAIL % rid))
        got = [p for p in (ov, th) if p in ent] + det
        kb = sum(ent[p] for p in got) / 1024.0
        tot += kb
        files += got
        print("%-5s %-10s %-3s %-3s %-6d %-8.0f %s" % (
            rid, fmt, "Y" if ov in ent else "-", "Y" if th in ent else "-", len(det), kb, title))
    print()
    print("reachable references: %d   picture files: %d   stored: %.1f MB" % (len(reach), len(files), tot / 1024.0))
    if "--names" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--names") + 1])
        out.write_text("\n".join(files) + "\n", encoding="cp932")
        print("wrote %s" % out)


if __name__ == "__main__":
    main()
