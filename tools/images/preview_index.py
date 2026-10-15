"""preview_index.py - rebuild review/images/preview-<module>/index.html from the preview files actually present.
batch.py's write_index() only finds previews named <job index>-<id>.png; the picture lanes rename theirs into a reserved
number range (e.g. 200-rep178-whole.png), so its page goes stale. This lists every preview png in number order with the
job id parsed from the name and that job's ledger rows (review/images/UNCHECKED-IMAGES.md, matched on the job-id field).
stdlib only. usage: python tools/images/preview_index.py [refdocs]   (run it again after every batch.py run)
"""
import html, os, re, sys
mod = sys.argv[1] if len(sys.argv) > 1 else "refdocs"
P = "review/images/preview-%s/" % mod
ledger = {}
for row in open("review/images/UNCHECKED-IMAGES.md", encoding="utf-8").read().splitlines():
    f = [c.strip() for c in row.split("|")]
    if row.startswith("- [") and len(f) >= 4:
        for jid in f[3].split("+"):   # a row may name several jobs: ref93-head+ref93-big
            ledger.setdefault(jid.strip(), []).append(row)
files = [f for f in os.listdir(P) if f.endswith(".png") and re.match(r"\d+-", f)]
files.sort(key=lambda f: (int(f.split("-")[0]), f))
out = ['<!DOCTYPE html><html><head><meta charset="utf-8"><title>Picture previews</title><style>body{background:#222;color:#ddd;'
       'font-family:Segoe UI,sans-serif;padding:16px}code{color:#9cf}img{display:block;margin:6px 0 24px;max-width:100%}'
       'li{font-size:13px}</style></head><body>', '<h1>Picture previews (%d files, number order)</h1>' % len(files)]
for f in files:
    jid = f[:-4].split("-", 1)[1]
    rows = ledger.get(jid) or ledger.get(re.sub(r"-\d+$", "", jid)) or []
    out.append("<h3>%s</h3><ul>%s</ul><img src=\"%s\" loading=\"lazy\">" % (html.escape(f), "".join(
        "<li><code>%s</code></li>" % html.escape(r) for r in rows) or "<li>no ledger row with job id %s</li>" % html.escape(jid),
        html.escape(f)))
out.append("</body></html>")
open(P + "index.html", "w", encoding="utf-8").write("".join(out))
print("index.html: %d previews, %d with ledger rows" % (len(files), sum(1 for f in files if ledger.get(f[:-4].split("-", 1)[1])
      or ledger.get(re.sub(r"-\d+$", "", f[:-4].split("-", 1)[1])))))
