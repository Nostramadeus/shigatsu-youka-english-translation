#!/bin/sh
# Print the full CAST.md block(s) whose "## " heading contains each given string. Usage: sh tools/cast_block.sh 名前1 名前2 ...
for n in "$@"; do
  awk -v pat="$n" '
  /^## /{ inblk = index($0, pat) > 0 }
  inblk { print }
  ' notes/CAST.md
done
