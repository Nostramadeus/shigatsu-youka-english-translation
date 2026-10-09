#!/bin/sh
# Apply CAST.md block updates from a staging file. Usage: sh tools/cast_apply.sh notes/_tmp/cNN-castupd.txt
# Staging format: sections start with "@@@## <heading prefix>" (must match the start of an existing "## " line
# in CAST.md). The section body = new bullet lines to insert BEFORE the block's "- as-of:" line, and MUST end
# with the new "- as-of: <id>" line, which replaces the old one. Prints NOHIT: <key> for unmatched keys.
staging="$1"
[ -f "$staging" ] || { echo "no staging file: $staging" >&2; exit 1; }
cp notes/CAST.md notes/_tmp/CAST.pre-apply.bak
awk -v sf="$staging" '
BEGIN{
  key=""
  while ((getline line < sf) > 0) {
    if (substr(line,1,5)=="@@@##") { key=substr(line,4); keys[++n]=key; body[key]="" }
    else if (key!="") body[key]=body[key] line "\n"
  }
  close(sf)
}
/^## /{ cur=""; for (i=1;i<=n;i++) if (index($0, keys[i])==1) { cur=keys[i]; hit[cur]=1 } }
/^- as-of:/ && cur!="" { printf "%s", body[cur]; cur=""; next }
{ print }
END{ for (i=1;i<=n;i++) if (!hit[keys[i]]) print "NOHIT: " keys[i] > "/dev/stderr" }
' notes/CAST.md > notes/_tmp/CAST.new && mv notes/_tmp/CAST.new notes/CAST.md
h=$(grep -c "^## " notes/CAST.md); a=$(grep -c "^- as-of:" notes/CAST.md)
echo "blocks=$h as-of=$a"
[ "$h" = "$a" ] || echo "MISMATCH: restore from notes/_tmp/CAST.pre-apply.bak" >&2
