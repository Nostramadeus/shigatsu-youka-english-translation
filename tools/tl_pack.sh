#!/bin/sh
# Build the ONE per-file packet a translation agent reads. Since 2026-09-26 this is a thin wrapper around
# tools/kb/kb.py packet (pass-2 notes in notes/v2, fenced, 40 KB budget; see tools/kb/README.md).
#   sh tools/tl_pack.sh 000001DD      -> notes/v2/_tmp/pack-000001DD.md
# The pass-1 shell version (hard-coded to notes/) is kept at tools/_retired/tl_pack.sh.pre-kb; tools/db/ moved to
# tools/_retired/db/.
set -e
cd "$(dirname "$0")/.."
[ -z "$1" ] && { echo "usage: sh tools/tl_pack.sh <lsbid> [<lsbid> ...]"; exit 1; }
PYTHONUTF8=1 exec uv run --no-project --python 3.12 python tools/kb/kb.py packet "$@"
