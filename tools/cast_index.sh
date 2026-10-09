#!/bin/sh
# One compact line per CAST block: heading | pronoun(s) (cut) | speech level (cut) | as-of
awk '
/^## /{ if (h!="") print h" || "p" || "s" || "a; h=$0; p="";s="";a="" }
/^- pronoun\(s\):/{ p=substr($0,1,110) }
/^- speech level baseline:/{ s=substr($0,1,110) }
/^- as-of:/{ a=$0 }
END{ if (h!="") print h" || "p" || "s" || "a }
' notes/CAST.md
