#!/bin/sh
# SUPERSEDED 2026-09-25 by tools/db/pack.py (packet) and `tools/db/query.py character <name>`.
# See tools/db/README.md.
# Write CAST.md blocks to notes/_tmp/cast-sel.txt (each block once, file order).
# Default: a block matches if its "## " heading STARTS with "## <name>" (anchored; derived blocks such as
# "## the X voice — Y impersonating ..." are NOT pulled in). Prefix a name with ~ for loose substring match.
# Usage: sh tools/cast_select.sh 名前1 ~部分一致 ...
awk -v pats="$(printf '%s\n' "$@")" '
BEGIN{ n=split(pats, p, "\n") }
/^## /{ inblk=0
  for(i=1;i<=n;i++){ if(p[i]=="") continue
    if(substr(p[i],1,1)=="~"){ if(index($0,substr(p[i],2))>0){inblk=1;break} }
    else if(index($0,"## " p[i])==1){inblk=1;break} } }
inblk { print }
' notes/CAST.md > notes/_tmp/cast-sel.txt
echo "cast-sel.txt lines: $(wc -l < notes/_tmp/cast-sel.txt), blocks: $(grep -c '^## ' notes/_tmp/cast-sel.txt)"
