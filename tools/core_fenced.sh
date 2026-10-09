#!/bin/sh
# SUPERSEDED 2026-09-25 by tools/db/fenced_core.py (same output, same fence). See tools/db/README.md.
# Fence notes/CORE.md for a drafter: notes/_tmp/core-<lastid>.md
#   sh tools/core_fenced.sh 000001E1     # <lastid> = the LAST file id you are translating
# Every line whose EARLIEST 8-hex file id is later than <lastid> is dropped, so CORE's later-fact rows
# (C4 resolutions, the D1 "LATER" clauses, rulings made from files you have not reached) never reach the
# drafter. Heading lines and lines with no file id stay. Same fence() awk as tools/tl_pack.sh, same reason:
# lsb ids are assigned in creation order = reading order, so a string compare works.
# Added 2026-09-25 for rules audit #4 (METHOD "never read ahead" vs the brief's "read CORE whole").
set -e
cd "$(dirname "$0")/.."
id="$1"; [ -z "$id" ] && { echo "usage: sh tools/core_fenced.sh <lsbid of the last file you translate>"; exit 1; }
mkdir -p notes/_tmp
out="notes/_tmp/core-$id.md"

# The id fence (same awk as tools/tl_pack.sh) plus the two removals rules audit #4 names by section:
#   - section C4 (resolved rows that change an earlier file): heading kept, rows dropped. Most of those rows
#     cite no file id at all, or cite the early file they change, so the id fence alone leaves them in.
#   - a "LATER ..." clause inside a D1 cast heading: the heading is kept, the clause is not.
fence() {
  awk -v cur="$id" '
    /^## C4\./ { print; print "(rows omitted by the fence: resolved rows that change an earlier file are reviewer and orchestrator material.)"; skip=1; next }
    /^#/ { skip=0
           if (match($0, /LATER[^)]*/)) { $0 = substr($0,1,RSTART-1) "later fact fenced" substr($0,RSTART+RLENGTH) }
           print; next }
    skip { next }
    { min=""; s=$0
      while (match(s, /[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]/)) {
        t=substr(s,RSTART,RLENGTH); if (min=="" || t<min) min=t; s=substr(s,RSTART+RLENGTH) }
      if (min=="" || min<=cur) print }' "$@"
}

{
  echo "<!-- CORE.md FENCED at $id (sh tools/core_fenced.sh $id). Lines whose earliest file id is later than"
  echo "     $id are omitted: that is the knowledge fence, TRANSLATOR-BRIEF-v2 §0. Do not read notes/CORE.md whole."
  echo "     A gap is GRAMMAR when two first-time Japanese readers fill it the same way without noticing: fill it,"
  echo "     no flag. A gap is WITHHELD when they could fill it two ways, or the text later turns on it: keep it"
  echo "     open, or take the pack-supported reading and flag needs-tlc. -->"
  fence notes/CORE.md
} > "$out"
echo "wrote $out ($(wc -l < "$out") lines, $(wc -c < "$out") bytes; CORE.md is $(wc -l < notes/CORE.md) lines, $(wc -c < notes/CORE.md) bytes)"
