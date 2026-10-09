#!/bin/sh
# Build work/<rel> from orig/<rel> for a script that has NO .lns text: copy it, then apply a label map
# and, if it exists, patch/extra-maps-<basename>.txt (same convention as tools/compile_en.sh).
#   sh tools/apply_labels.sh 00001923.lsb patch/labels-00001923.tsv
#   sh tools/apply_labels.sh "ノベルシステム/メッセージボックス/文字列入力.lsb" patch/labels-文字列入力.tsv
# <rel> is relative to orig/ and to work/, and is what goes into tools/ship-list.txt.
# Never touches orig/. For a script that DOES carry .lns text use tools/compile_en.sh instead.
set -e
cd "$(dirname "$0")/.."
rel="$1"; map="$2"
[ -z "$rel" ] && { echo "usage: sh tools/apply_labels.sh <path relative to orig/> [MAP.tsv]"; exit 1; }
[ -f "orig/$rel" ] || { echo "orig/$rel missing"; exit 1; }
# GUARD (R1 2026-09-26): this copies orig/ and so DROPS any translated .lns text. If the 5.5 tree has text for this
# script, refuse unless ALLOW_LABELS_ONLY=1; build it with SRC_DIR=lns-en-55 sh tools/compile_en.sh <id> <map> instead.
_b=$(basename "$rel" .lsb)
if [ -f "lns-en-55/$_b.lsbref" ] && [ "${ALLOW_LABELS_ONLY:-0}" != "1" ]; then
  echo "apply_labels: lns-en-55/$_b.lsbref exists - use: SRC_DIR=lns-en-55 sh tools/compile_en.sh $_b ${2:-} (work/$rel left as it was)"
  exit 1
fi
mkdir -p "$(dirname "work/$rel")"
cp -f "orig/$rel" "work/$rel"
if [ -n "$map" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_strings.py apply "work/$rel" "work/$rel" "$map"
fi
base=$(basename "$rel" .lsb)
if [ -f "patch/extra-maps-$base.txt" ]; then
  while read -r extra; do
    extra=$(printf '%s' "$extra" | tr -d '\r')
    [ -z "$extra" ] && continue; case "$extra" in \#*) continue;; esac
    PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_strings.py apply "work/$rel" "work/$rel" "$extra" --allow-missing
  done < "patch/extra-maps-$base.txt"
fi
# PROPERTY PATCHES: patch/props-<id>.tsv sets NON-STRING command properties (index/PROPERTY/old/new).
# The label maps reach string literals only; some render defects are a flag. PR_FONTBORDER=1 on a
# MesNew makes LiveMaker lay that box out on a full-width advance per glyph, so English comes out
# letter-spaced (UI lane, 2026-09-26).
if [ -f "patch/props-$base.tsv" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_prop.py apply "work/$rel" "work/$rel" "patch/props-$base.tsv"
fi
# STRUCTURAL FIXES (same step as tools/compile_en.sh; R1 2026-09-26): patch/fix-<id>.py IN OUT, e.g. the encyclopedia
# display-name repoint (patch/dispcol.py). Each script checks its sites and is idempotent.
if [ -f "patch/fix-$base.py" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python "patch/fix-$base.py" "work/$rel" "work/$rel"
fi
ls -la "work/$rel"
