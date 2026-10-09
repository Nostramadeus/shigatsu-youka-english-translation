#!/bin/sh
# Compile <src>/<id>-*.lns into work/<id>.lsb (a copy of orig/<id>.lsb). Run from the project root.
#   sh tools/compile_en.sh 00000024 [MAP.tsv]          (src = lns-en; SRC_DIR=lns-en-55 for the 5.5 tree; SRC_DIR=lns for a JP round-trip test)
# Steps: copy the .lsbref verbatim (CR LF; batchinsert reads it in text mode, CR CR LF breaks it), normalize
# the .lns line endings to CR CR LF (what lmlsb extract produced) into work/lns-<id>/, copy orig/<id>.lsb ->
# work/<id>.lsb, lmlsb batchinsert, then (optional) tools/lsb_strings.py apply MAP.tsv for menu labels /
# captions that live outside the .lns text. Never touches orig/.
# FURIGANA (Fable ruling 2026-09-25, Q1321 + owner): ruby strings live in the lsb style table. EN builds: a
# `<STYLE ID="n" RUBY="jp">` word KEEPS its own STYLE id with the RUBY attribute dropped (2026-09-27: re-pointing to the
# enclosing style lost the ruby style's own colour, e.g. a yellow name) UNLESS patch/ruby-<id>.tsv
# has a row `jp<TAB>en`; then the tag is rewritten to RUBY="en" (the LNS compiler writes it into the table) and
# tools/lsb_ruby.py afterwards clears every ruby that is not in the map. lns-en keeps the original tags.
# UNREVIEWED MARKER (owner 2026-09-25): ids listed in work/UNREVIEWED.txt get "[Unreviewed draft] " prefixed to
# the first text line of their first .lns (temp copy only; tools/mark_unreviewed.pl). Remove the id from the list
# and recompile once the section has passed the reviewer.
set -e
cd "$(dirname "$0")/.."
id="$1"; map="$2"
src="${SRC_DIR:-lns-en}"
[ -z "$id" ] && { echo "usage: sh tools/compile_en.sh <id> [MAP.tsv]"; exit 1; }
[ -f "$src/$id.lsbref" ] || { echo "$src/$id.lsbref missing"; exit 1; }
tmp="work/lns-$id"
rm -rf "$tmp"; mkdir -p "$tmp"
cp -f "$src/$id.lsbref" "$tmp/"
rubymap="patch/ruby-$id.tsv"
[ -f "$rubymap" ] || rubymap=""
for f in $src/$id-*.lns; do
  if [ "$src" != "lns" ]; then  # any EN tree (lns-en, lns-en-55)
    RUBYMAP="$rubymap" perl -CSD -Mutf8 -MEncode -pe '
      BEGIN {
        %map = ();
        if ($ENV{RUBYMAP}) {
          open(my $fh, "<:encoding(UTF-8)", $ENV{RUBYMAP}) or die;
          while (<$fh>) { chomp; next if /^#/ || !/\t/; my ($j, $e) = split /\t/; $map{$j} = $e }
          close $fh;
        }
      }
      s/\r?\r?\n/\r\r\n/;
      my $guard = 0; my $from = 0;
      while ($guard++ < 50 && substr($_, $from) =~ /<STYLE ID="(\d+)" RUBY="([^"]*)">/) {
        my ($sid, $ruby) = ($1, $2);
        my $abs = $from + $-[0]; my $len = $+[0] - $-[0];
        if (exists $map{$ruby}) {
          my $new = "<STYLE ID=\"$sid\" RUBY=\"$map{$ruby}\">";
          substr($_, $abs, $len) = $new; $from = $abs + length($new); next;
        }
        my $pre = substr($_, 0, $abs);
        my ($m) = $pre =~ /.*<STYLE ID="(\d+)">/;
        if (!defined $m) { my $post = substr($_, $abs + $len); ($m) = $post =~ /<STYLE ID="(\d+)">/ }
        $m = $sid unless defined $m;
        substr($_, $abs, $len) = "<STYLE ID=\"$sid\">"; $from = $abs + 1;   # keep the ruby style id: its colour stays (yellow names); lsb_ruby.py blanks the kana
      }' "$f" > "$tmp/$(basename "$f")"
  else
    perl -pe 's/\r?\r?\n/\r\r\n/' "$f" > "$tmp/$(basename "$f")"
  fi
done
if [ "$src" != "lns" ] && grep -qx "$id" work/UNREVIEWED.txt 2>/dev/null; then
  first=$(head -1 "$tmp/$id.lsbref" | tr -d '\r' | sed 's/:[0-9]*$//')
  [ -f "$tmp/$first" ] && perl tools/mark_unreviewed.pl "$tmp/$first"
fi
cp -f "orig/$id.lsb" "work/$id.lsb"
( cd orig && uvx --from pylivemaker lmlsb batchinsert --no-backup "../work/$id.lsb" "../$tmp/" )
if [ "$src" != "lns" ]; then  # any EN tree (lns-en, lns-en-55)
  # clear every ruby not in the map (mapped ones were rewritten to their English by the compiler; keep those)
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_ruby.py apply "work/$id.lsb" "work/$id.lsb" ${rubymap:+"$rubymap"} --keep-en
fi
if [ -n "$map" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_strings.py apply "work/$id.lsb" "work/$id.lsb" "$map"
fi
# EXTRA MAPS: patch/extra-maps-<id>.txt lists more label maps to apply after the main one (e.g. the scenario-title
# lookup map patch/titles-jp-en.tsv); keys missing from this particular file are allowed there.
if [ "$src" != "lns" ] && [ -f "patch/extra-maps-$id.txt" ]; then
  while read -r extra; do
    extra=$(printf '%s' "$extra" | tr -d '\r')   # the map lists are CRLF; a trailing CR breaks the open()
    [ -z "$extra" ] && continue; case "$extra" in \#*) continue;; esac
    PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_strings.py apply "work/$id.lsb" "work/$id.lsb" "$extra" --allow-missing
  done < "patch/extra-maps-$id.txt"
fi
# PROPERTY PATCHES: patch/props-<id>.tsv sets NON-STRING command properties (index/PROPERTY/old/new).
# The label maps reach string literals only; some render defects are a flag. PR_FONTBORDER=1 on a
# MesNew makes LiveMaker lay that box out on a full-width advance per glyph, so English comes out
# letter-spaced (UI lane, 2026-09-26).
if [ -f "patch/props-$id.tsv" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python tools/lsb_prop.py apply "work/$id.lsb" "work/$id.lsb" "patch/props-$id.tsv"
fi
# STRUCTURAL FIXES (FIX1 2026-09-26): patch/fix-<id>.py IN OUT edits an expression the maps cannot reach
# (e.g. 0000001C idx 143, the hover-card width test). Each script checks the original form and is idempotent.
if [ "$src" != "lns" ] && [ -f "patch/fix-$id.py" ]; then
  PYTHONUTF8=1 uv run --no-project --with pylivemaker python "patch/fix-$id.py" "work/$id.lsb" "work/$id.lsb"
fi
ls -la "work/$id.lsb"
