# tools/kb — the pass-2 notes as fact tables, a fence, and a budgeted packet

Built 2026-09-26. Replaces `tools/db/` (moved to `tools/_retired/db/`, nothing deleted). Design ported from the
Mushoku Tensei project (`<projects>/mushoku-tensei-en/notes/DATA-DESIGN.md`, `tools/kb.py`) and adapted here.
Port record: `notes/KB-PORT-REPORT.md` (parity gate), `notes/KB-PORT-PROGRESS.md` (done/next board).

**The pass-2 masters stay the human-editable sources of truth.** `kb.py convert` turns them into one-fact-per-row
TSVs under `notes/v2/db/`; `kb.py build` turns those into `notes/v2/db/kb.sqlite`, which is disposable. Nobody edits
the TSVs or the sqlite by hand: edit the master, the next `packet` / `tm` / `search` refreshes both.

Stdlib only, SQLite only, one process at a time. Every command below is prefixed with
`cd /f/Projects/shigatsu-youka-en &&` and run through `PYTHONUTF8=1 uv run --no-project --python 3.12 python`
(there is no `python` on PATH). No env vars: the tool reads `notes/v2` and `lns-en-55/` only (except `core`).

## Commands

```sh
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py convert          # masters -> notes/v2/db/*.tsv (<1 s)
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py build            # TSVs + read/ + lns/ -> kb.sqlite (~10 s)
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py packet 000001DD  # -> notes/v2/_tmp/pack-000001DD.md
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py tm 000001DD      # -> notes/v2/_tmp/tm-000001DD.tsv (--all: later files too)
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py lint             # report mode; --strict exits 1 on a breach
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py search 四月病 --asof 000001DD --in facts
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py core 000001DD    # -> notes/_tmp/core-000001DD.md
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query fence-audit 000001DD   # or `all`, `--fresh`
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query character 古郡なつみ --asof 000001DD
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query speaker 000001DD
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query speaker-lines なつみ --asof 000001DD
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query narrator 000004BB
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py query narrator-audit
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py merge-log E --dry-run   # then without --dry-run
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py merge-log check
PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py selftest
sh tools/tl_pack.sh 000001DD                                                            # = kb.py packet
```

| command | writes | replaces |
|---|---|---|
| `convert` | notes/v2/db/*.tsv | build.py (the parsing half) |
| `build` | notes/v2/db/kb.sqlite | build.py (the index half) |
| `packet <id> [<id> ...]` | notes/v2/_tmp/pack-\<id\>.md | pack.py, tl_pack.sh (+ tl_slice/cast_select/relations_select) |
| `tm <id> [--all]` | notes/v2/_tmp/tm-\<id\>.tsv | — (new) |
| `lint [--strict]` | stdout | — (new) |
| `search <text> [--asof <id>] [--in jp\|en\|facts]` | stdout | query.py `term` for plain lookups |
| `core <lastid>` | notes/_tmp/core-\<id\>.md (`SY_NOTES_DIR=notes/v2`: notes/v2/_tmp/, CORE-RULES.md) | fenced_core.py |
| `query <sub> ...` | stdout | query.py fence-audit, character, speaker, speaker-lines, narrator, narrator-audit |
| `merge-log <tag> [--dry-run] [--force]`, `merge-log check` | the notes/v2 masters (append), then the TSVs + sqlite | merge_log.py |
| `selftest` | stdout | selftest.py |

`packet`, `tm` and `search` run `convert` when a master is newer than the TSVs and `build` when a TSV is newer than
the sqlite (one line each on stdout), so a drafter never reads a stale packet. Writes are atomic (temp + replace).

Retired without a replacement (no brief or RESUME.md calls them; kept in `tools/_retired/db/`): `graph.py` (the
edge table and its neighbors/path/components/fence commands) and the query.py subcommands term, collisions,
open-queries, file, refrains (`kb.py search` covers plain term lookups). They do NOT run from
`tools/_retired/db/` (common.py finds the project root by folder depth); to use one, copy the folder back to
`tools/db/` first.

## Sources

| master (notes/v2 unless said) | TSV | rows (2026-09-26) |
|---|---|---|
| read/chunkNN.txt `### FILE` headers | files.tsv `file_id order chunk lines chars header` | 422 |
| SUMMARY.md | summary.tsv `file_id line depth key first_id superseded_id text` (one row per LINE) | 6,366 |
| CAST.md | cast.tsv `block name heading first_appears`; cast_facts.tsv `block line depth parent kind voice first_id superseded_id text` (one row per LINE) | 155 / 2,875 |
| RELATIONS.tsv | relations.tsv (the 7 columns + `first_id superseded_id`) | 1,073 |
| GLOSSARY.tsv | glossary.tsv (the 9 columns + `first_id superseded_id`) | 2,961 |
| QUERIES.md | queries.tsv `qid loc question why best_guess confidence status resolved_by nfields tail first_id superseded_id` | 667 |
| SCENE-FACTS.tsv, NARRATOR-SWITCHES.tsv, UNREACHABLE.tsv | scene_facts / narrator_switches / unreachable.tsv (+ `first_id`) | 205 / 9 / 13 |
| read/speakers/chunkNN.tsv | speakers.tsv (rows with a speaker, a switch or unreachable=1; + `first_id`) | 37,634 |
| SUMMARY.md (derived) | chunk_cards.tsv `chunk files words source first_id text`, source = `auto` | 30 |
| headers | meta.tsv (a tab inside a value is stored as backslash-t) | 5 |

TSV rule (DATA-DESIGN §10): raw tab-joined lines, LF, UTF-8, header row, never csv quoting. A tab or line break
inside a field stops `convert` with a message (none today). `convert` output depends only on the masters, so two
runs give byte-identical files (selftest proves it by sha256). The TSVs reprint the masters line for line
(selftest round trip), so nothing is lost in the conversion.

`kb.sqlite` holds every TSV as a table (all TEXT, indexes on id columns) plus: `text` (74,180 chunk lines),
`mention` (glossary jp x file, n), `speaker_color` (74,253 lns cells: colour, speaker, kind; from
tools/style_colors.py + notes/v2/SPEAKER-COLORS.tsv), `tm` (7,486 JP/EN lns line pairs from lns-en-55/), `doc` (the search index:
FTS5 with the trigram tokenizer when this sqlite has it; else a plain table + `gram(g, doc)` 3-gram table, and
`build` says so), `kbmeta` (which search mode was built).

## THE FENCE

- **Order.** A file id's position = the `order N` of its `### FILE` header in read/chunkNN.txt. A fact's position =
  (order, block, cell) from an id written as `ID`, `ID:block` or `ID:block:cell`. An 8-hex id that is no lsb file
  id (an .lns part id) sorts right after the file before it in hex order (hex order == reading order; selftest).
- **first_id per row.**
  - CAST line: top-level bullet = its earliest id; with no id of its own = the block's `first_appears` id. A child
    bullet = the later of its own earliest id and its parent's first_id (so a child is never known before its parent,
    the FR-02 rule, now in the data). Heading = first_appears. No CAST line is "always known" (selftest).
  - SUMMARY line: the later of the block's file id and the line's own earliest id (a child: of its parent's).
  - RELATIONS row: its `as_of_file` id (the old fence used the earliest id anywhere on the row).
  - GLOSSARY row: its `first_seen` id. QUERIES row: the first id of its `file:line` cell.
  - chunk card: the later of the chunk's last file and every line it quotes.
- **superseded_id.** A RELATIONS row with `changed_from` replaces the latest earlier row of the same from/to whose
  calls_them or speech_level equals changed_from exactly; that row's superseded_id = the new row's first_id
  (16 rows today). A GLOSSARY row with status `superseded` is never shown.
- **Stabbing.** A row is shown to the drafter of file X when first_id <= (X, end of file) and superseded_id is empty
  or not before (X, start of file): the old row stays visible in the file where the change happens. `Fence` sorts
  rows by first_id once and bisects; selftest proves it equals a brute-force scan for every file id.
- **Later-id rule (packet).** first_id uses a line's EARLIEST id, so a known line can still QUOTE a later file
  (e.g. `- as-of: <later> (was <earlier>)`). The packet therefore also drops every fact line (SUMMARY, card,
  GLOSSARY, QUERIES, CAST, RELATIONS, speakers/narrator line) that quotes any 8-hex id later than the packet's id,
  together with the deeper-indented lines under it; a CAST line with ancestors quoting a later id is dropped too.
  Exception: a MANDATORY cast line (block heading, voice-sheet bullet or its child) keeps its key, loses every
  `; `-separated clause that holds a later id, and ends in ` [trimmed]`. The budget line counts both. Result on
  the test ids: 0 later ids shown (before: 8 / 0 / 4); 6 lines dropped, 7 trimmed. `query fence-audit` checks the
  whole notes part of a packet for later ids (the old audit checked only the CAST/RELATIONS sections).

## The packet

Same order and headings as the old pack.py where the section exists; the text-line view is unchanged (a quote cell
gets `[name] ` / `[?] ` from read/speakers, a cell of an unreachable block `[unreachable] `).

| section | items | in the 40 KB cap |
|---|---|---|
| header: speakers detected, speaker/unreachable note, owner-rulings pointer, GRAMMAR paragraph, SLICE line, scenario narrator + start, NARRATOR SWITCH lines | fixed | counted |
| SUMMARY block of the previous file, of THIS file (leaves, fenced per line) | mandatory | counted |
| Earlier files of this chunk (leaf SUMMARY blocks) | optional, tier 0 | counted |
| Earlier chunks (auto cards) | optional, tier 1 | counted |
| GLOSSARY rows whose jp occurs in the file (substring, as before), fenced | mandatory | counted |
| QUERIES rows filed against this file | mandatory | counted |
| Speakers present, Narrator line | mandatory | counted |
| CAST blocks whose heading starts with a speaker name (as before): voice-sheet bullets (first_appears, pronoun, speech level, sentence-final, copula, verbal tics, dialect, EN correlates, narration voice, known ambiguity, as-of) with their children | mandatory | counted |
| CAST: every other line (chunk additions, facts, lines, calls ...), one item per line; a chosen line brings its ancestors | optional, tier 0 | counted |
| RELATIONS rows between two speakers present (substring, as before) | mandatory | counted |
| RELATIONS rows one hop out (one party present; tier 3 when neither party is present) | optional, tier 2/3 | counted |
| Text-line view | fixed | NOT counted (it is the source) |
| Budget line + dropped list (grouped by section and label, with counts and bytes) | fixed | foot |

**Budget (DATA-DESIGN §5).** Cap 40,960 bytes for everything above the text-line view. Mandatory items always go
in; if they alone pass the cap the budget line says so. Optional items: by tier, then by score / size, where score
= sum over the glossary terms of THIS file that the item contains of (occurrences in this file x
log(files / files containing the term)), x2 when the item's first_id is in this file or the two before it, x0.25
for tier-3 relations. After the greedy pass the notes part is rendered and measured; while it is over the cap the
lowest-ranked optional item is dropped (ancestor lines are only counted there).

**Summary tree (DATA-DESIGN §4).** Leaf = the per-file SUMMARY block. Parent = per-chunk card, AUTO: each file's
`events` bullet and its children, cut to an equal share of 400 words (`400 // files - 3` words per file, the id,
"..." and separator counted), joined; `source = auto` in chunk_cards.tsv. Root: none yet.

## tm

For each JP line of `lns/<id>-*.lns` with Japanese in it (tags and `{commands}` stripped): the up to 3 JP lines of
OTHER files with English in `lns-en-55/` (same .lns file name and line number; EN differs from JP) whose character
3-gram Jaccard is >= 0.6 (spaces and 「」『』（）()、。…！？!?―─・～~ removed first). `must` = `MUST-MATCH` when the stripped
texts are equal. Only files BEFORE `<id>` are used unless `--all`. Output columns
`row match jaccard must jp match_jp match_en`.

## lint (DATA-DESIGN §9, report mode)

Checks: notes/v2/*.md over 20 KB (briefs exempt); SUMMARY leaf over 150 words; chunk card over 400 words; CAST line
over 30 words; non-voice CAST lines per block over 40 (120 for the block with the most); CSV-quoted fields in any
TSV; GLOSSARY jp twice. Prints counts and the first 8 of each; also the number of CAST lines with no id of their
own (information). Exit 0; `--strict` exits 1 on any breach. It never edits a master. 2026-09-26: 1,031 breaches in
4 checks (the pass-2 notes predate the caps).

## query (ports of tools/db/query.py)

| sub | does | difference from the old one |
|---|---|---|
| `fence-audit <id\|all> [--fresh]` | every line above the text view quoting a file later than `<id>`; reads `notes/v2/_tmp/pack-<id>.md` when present, else builds; `all` = sections 1-3 of tools/ship-list.txt | checks the whole notes part, not only CAST/RELATIONS; a packet on disk written by the old pack.py is labelled OLD TOOL; `--fresh` ignores disk. 2026-09-26: `all --fresh` 0 leaks over 85 ids; the 28 old-tool packets still on disk hold 269 |
| `character <JP name> [--asof <id>]` | CAST blocks (fenced), RELATIONS rows (fenced + superseded), files whose SUMMARY speakers line names it | fence = kb first_id rule |
| `speaker <id>` | per text cell: block:cell, colour, speaker, kind, text | same (table speaker_color, built from tools/style_colors.py) |
| `speaker-lines <JP name> [--asof <id>]` | every quote cell in that colour, reading order | same |
| `narrator <id>` / `narrator-audit` | scenario-table narrator + start, switch sprites, unreachable blocks, SUMMARY narrator line, verdict | same rule (name_forms / narrator_compare) |

## merge-log (port of tools/db/merge_log.py)

`notes/v2/_tmp/tl-log-<tag>.md` -> the notes/v2 masters, same row kinds and append rules as before: DECISION ->
`notes/v2/DECISIONS.md`, TN -> `notes/v2/NOTES-TL.md` (both created by the first append; pass 2 had neither),
QUERY -> `QUERIES.md`, RESOLVED -> the QUERIES row's status becomes `resolved | resolved_by=<how>` when it was
tl-open/owner/open/provisional, PROGRESS -> a `| ... |` row appended to `PROGRESS.md`. A row already present
(exact text) is skipped; a row whose key (first field, or first two) is present with different text is skipped
and reported (`--force` appends it). `--dry-run` prints what would change. After a real merge: convert + build and
`merge-log check` (master row counts == TSV == sqlite for queries, glossary, relations, cast, summary;
DECISIONS/NOTES-TL are counted, not indexed: no packet section reads them). The old tool refused pass 2; this one
works only on notes/v2. Selftest runs it on a scratch copy (notes/v2/_tmp/kbport/mergetest/), never on the masters.

## selftest

1. convert twice, sha256 over all TSVs equal (retried if a master changes during the test);
2. SUMMARY, CAST, RELATIONS, GLOSSARY, QUERIES reprinted from the TSVs equal the masters;
3. build: row counts of every table equal the TSVs; hex order == reading order;
4. fence: bisect == brute force for every file id over cast_facts, relations, glossary; every CAST line has a
   first_id; id-free top-level bullets carry first_appears; no child before its parent;
5. packets 000001DD, 00000460, 000016AE: no kept item after the id, every rendered CAST/RELATIONS/GLOSSARY line is a
   row visible at the id, notes part within the cap;
   0 lines above the text view quoting a later file;
6. search finds a glossary key; 3-gram Jaccard sanity; every MUST-MATCH of a real tm run is an exact match;
7. `query fence-audit 000016AE --fresh` is 0; merge-log on a scratch copy appends one row of each kind and resolves
   one query, a rerun appends nothing, an edited master row is skipped.

## Deviations from the Mushoku design (and why)

1. **Leaves are long.** A SUMMARY block here is several hundred words, not 150, so only the previous file's leaf is
   mandatory; other leaves of the chunk are ranked optional items (the §5 "this volume's earlier summaries
   mandatory" would fill the cap on its own).
2. **Tiers before score / size.** Pure score / size let many small one-hop RELATIONS rows push out the present
   speakers' CAST lines; the seeds' lines rank first (§3: expand one hop, the hop only ranks).
3. **CAST items are single lines**, not whole cards, so the cap cuts facts, not characters.
4. **The text-line view is outside the cap**: it is the file itself, not notes.
5. **`core` is an extra subcommand**, a port of fenced_core.py, because the briefs still call it.
6. **Glossary is fenced** on first_seen (the old packet was not); the parity report lists what that removed.
7. **kb.py is one file of ~2,000 lines** (convert, build, fence, packet, tm, search, lint, core, query, merge-log,
   selftest). A split into modules is possible; not done without the owner's word.
