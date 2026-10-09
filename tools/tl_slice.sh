#!/bin/sh
# SUPERSEDED 2026-09-25 by tools/db/pack.py, which builds the slice sections straight from
# notes/db/project.sqlite. See tools/db/README.md.
# Build the per-file translation slice for ONE lsb id and write it to notes/_tmp/slice-<id>.md.
# Usage (from the project root): sh tools/tl_slice.sh 00000024
# Contents, in order:
#   1. the file's own SUMMARY block and the block of the file just before it in reading order
#   2. GLOSSARY rows whose jp key occurs in the file's text (read/chunk text, csv fallback)
#   3. open QUERIES rows filed against this file (any status except resolved/typo), plus typo rows for it
#   4. the list of speaker names found in the SUMMARY block, for the agent's cast_select / relations_select calls
id="$1"; [ -z "$id" ] && { echo "usage: sh tools/tl_slice.sh <lsbid>"; exit 1; }
out="notes/_tmp/slice-$id.md"
order=$(awk -F'\t' -v id="$id" '($2 "")==id{print $1}' notes/_db/_file-order.tsv)
prev=$(awk -F'\t' -v o="$order" '$1==o-1{print $2}' notes/_db/_file-order.tsv)
chunk=$(awk -F'\t' -v id="$id" '($2 "")==id{print $5}' notes/_db/_file-order.tsv)
{
echo "# SLICE for $id (order $order, chunk $chunk). Previous file in reading order: ${prev:-none}"
echo
echo "## SUMMARY block of the previous file ($prev)"
[ -n "$prev" ] && awk -v id="$prev" '/^## /{p=(index($0,"## " id)==1)} p' notes/SUMMARY.md
echo
echo "## SUMMARY block of THIS file ($id)"
awk -v id="$id" '/^## /{p=(index($0,"## " id)==1)} p' notes/SUMMARY.md
echo
echo "## GLOSSARY rows for terms that occur in this file (jp, reading, en, pos, category, first_seen, status, locked, note)"
# file text: the chunk section for this file
txt="notes/_tmp/slice-$id.txt"
awk -v id="$id" '/^### FILE /{p=(index($0,"### FILE " id)>0)} p' read/chunk$chunk.txt > "$txt"
awk -F'\t' -v txtfile="$txt" '
  BEGIN{ while((getline l < txtfile)>0) text=text l "\n" }
  NR==1{print; next}
  index(text,$1)>0 {print}
' notes/GLOSSARY.tsv
echo
echo "## QUERIES rows filed against this file"
grep "^Q[0-9]* | $id" notes/QUERIES.md
echo
echo "## Speakers present (from the SUMMARY block; use these names with tools/cast_select.sh and tools/relations_select.sh)"
awk -v id="$id" '/^## /{p=(index($0,"## " id)==1)} p && /^- speakers present:/' notes/SUMMARY.md
echo
echo "## Narrator line"
awk -v id="$id" '/^## /{p=(index($0,"## " id)==1)} p && /^- narrator:/' notes/SUMMARY.md
} > "$out"
echo "wrote $out ($(wc -l < "$out") lines); chunk text copy at $txt ($(wc -l < "$txt") lines)"
{
echo
echo "## GLOBAL-RESOLVES entries that mention this file (an earlier line of yours is load-bearing later, or your file resolves an earlier line)"
grep -n "$id" notes/GLOBAL-RESOLVES.md | cut -c1-420
} >> "$out"
echo "appended resolves entries: $(grep -c "$id" notes/GLOBAL-RESOLVES.md)"
