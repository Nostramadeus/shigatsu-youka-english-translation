#!/bin/sh
# SUPERSEDED 2026-09-25 by tools/db/pack.py (packet) and `tools/db/query.py character <name>`.
# See tools/db/README.md.
# Print the RELATIONS.tsv header plus every row whose from OR to column contains any of the given substrings.
# Usage: sh tools/relations_select.sh 名前1 名前2 ...   (output goes to stdout; keep under ~8 names per call)
awk -F'\t' -v pats="$(printf '%s\n' "$@")" '
BEGIN{ n=split(pats, p, "\n") }
NR==1 { print; next }
{ for(i=1;i<=n;i++) if(p[i]!="" && (index($1,p[i])>0 || index($2,p[i])>0)){ print; break } }
' notes/RELATIONS.tsv
