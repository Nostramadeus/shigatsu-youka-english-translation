# KEY-COLLISION-AUDIT.md — every translated string that the engine also uses as a key

Run 2026-09-26 by the key-collision agent. READ-ONLY audit: no shipped file was changed.
Evidence and every intermediate table live in `work/keyaudit/`.

The bug class: a string we translated is ALSO used by the engine as a database lookup key, a
comparison operand, an object name, a variable name, or a file-path component. Five instances had
been found one at a time before this run (scenario titles = PART1-GAP-AUDIT blocker 1; the chatter
caption 30-character key = Q2060; 形式 as a comparison literal and a `.gal` path component =
Q2050 / Q2370; 解禁編 / 解禁人物 = Q2361; the `<title>New` object name = Q2360; 閲覧年月日 object
names = Q2364). This run looked for the rest systematically.

## 1. Method

### Set T — every translated string that reaches the game (`work/keyaudit/translated-strings.tsv`, 6,130 rows)

| kind | rows | how it was built |
|---|---|---|
| `db` | 2,952 | every cell that differs between `orig/データベース/**/*.tsv` and `work/データベース/**/*.tsv`, both CP932, with table, row key, column name, JP, EN |
| `map` | 438 | every JP→EN row of `patch/labels-*.tsv`, `patch/*-jp-en.tsv`, `patch/titles-extra.tsv` |
| `extra` | 32 | the map files each `patch/extra-maps-*.txt` applies |
| `lsb` | 2,282 | **ground truth**: every Str param that differs between `orig/<rel>.lsb` and the built `work/<rel>.lsb`, keyed by command index and arg name. This is what the shipped builds really changed, including ctx-scoped rows, so it supersedes the map files |
| `lns` | 476 | line pairs of `lns/` vs `lns-en/` for the three menu scripts `0000001C` `0000001E` `000000F2` |

The 36 built `.lsb` carry 2,282 changed literals; the 40 story scripts carry **0** — their text is a
`TextIns` payload, which is not a `Param` and cannot be read back as a key by any command.

### Set U — every "use as key" site in all 542 `orig/**/*.lsb` (`work/keyaudit/use-sites.tsv`, 21,361 rows)

Two new whole-game dumps were made (one process each, ~3 min):

| file | what |
|---|---|
| `work/keyaudit/dump-all.tsv(.gz)` | every NON-`TextIns` command of all 542 scripts flattened with `str(cmd)` — 50,358 rows, 13 unfoldable fallbacks, 0 load failures |
| `work/keyaudit/params.tsv.gz` | every Str param of every command with its command type, **arg key** (`Name`, `ObjName`, `PR_PARENT`, `PR_TEXT`, …) and param path — 50,745 rows |
| `work/keyaudit/dump-ship.tsv.gz` + `params-ship.tsv.gz` | the same two dumps over the AS-SHIPPED game (`work/<rel>` when built, else `orig/<rel>`) |

Roles recognised: `dbtable`, `dbkeycol`, `dbkeyval`, `dbretcol`, `objref`, `objdef`, `varname`,
`window` (a `JCopy`/`JLength`/`JPos` over the expression), `cmp`, `path`.

### The joins

1. **Site-precise expression diff** (`sitediff.py` → `site-changes.tsv`): the same use-site
   in the original and in the shipped build. 143 key-role expressions changed (117 `objref`,
   26 `varname`); **0 path expressions changed** anywhere.
2. **Object-name graph** (`objgraph2.py` → `obj-broken.tsv`): creations (`Name` on a creating
   command) vs references (`ObjName`, `PR_PARENT`, `ObjDel.Name`, `Exists()`, `GetProp()`,
   `SetProp()`), computed twice and compared site by site. 1 dangling reference, 5 orphaned
   creations, 491 concatenated names parked in `obj-concat.tsv`.
3. **Column-versus-literal with the active table resolved** (`colcmp3.py` → `col-vs-literal.tsv`):
   every `DBGet*("col") == "literal"`, with the active table taken from the nearest preceding
   `DBSetActive` and the table→tsv map read out of `00001F85`'s `DBCreateTable`+`DBLoadTsvFile`
   pairs. 121 MAPPED, 57 SAFE, **42 BROKEN**, 4 more of the same shape whose value does not
   currently occur, 1 DYNAMIC.
4. **Variable dataflow** (`vars.py` → `var-chains.tsv`, `var-mixed.tsv`): for every variable ever
   compared against a string literal, every assignment site and every comparison site, in both
   languages. A variable whose same Japanese literal comes out as two different strings is a mixed
   chain. **0 mixed pairs** — `背景名`, `ナビ編名`, `現行編名`, `ナビ人物`, `ナビ背景名`, `事典編`
   and the rest are internally consistent after the maps.
5. **All changed comparison literals** (`cmpall.py` → `cmp-changed.tsv`): 435 comparison literals
   moved, in 83 distinct (file, left-hand-side) shapes; each shape was traced to the source of its
   left-hand side.
6. **Cross-file literal consistency** (`analyze.py` → `stale-literals.tsv`): 314 (literal, file)
   pairs where a literal renamed in one build is still Japanese in another script that mentions it.
7. **Substring parents** (`substring-parents.tsv`): 566 literals that contain a mapped value as a
   substring. `tools/lsb_strings.py` replaces whole literals only, so none of them moved — the list
   exists so nobody ever switches that tool to substring replacement, and so the derived forms are
   known: the `編` variants ending in `2`, the `真`/`極`/`最` prefixed forms, `…背景`, `…背景2`,
   `…タイトル`, `…透過`, `…進行`, the `編ロゴ` and `ナビ背景` `.gal` paths, and the arc names that
   are COLUMN HEADERS in `事典出来事.tsv`.
8. **Data files** (`data-files.tsv`): every `DBLoadTsvFile` and `LoadTextFile` site, resolved,
   with shipped/translated/reachable flags and the key columns of each table.

## 2. Counts

| class | n |
|---|---|
| BROKEN — a key that resolved in Japanese and does not resolve after the builds | **6 findings.** F1 (already fixed) = 18 DB key lookups + 50 column comparisons + 41 renamed literal object references. The 5 still open = **56 sites**: F2 39, F3 6, F5 8, F4 2 (+4 dependent branches), F6 1 |
| UNSURE — cannot be decided from the scripts | 5 findings |
| GAP — a live untranslated data source (not a collision) | 1 finding, 40 files |
| SAFE — checked and consistent | 6 previously-open classes closed |

Per-detector totals: 143 changed key-role expressions; 42 + 4 broken column comparisons;
6 object-graph defects (4 of them one root cause each); 0 mixed variable chains; 0 changed paths;
0 chatter captions over the 30-character key limit.

## 3. BROKEN, ordered by what a parts 1-3 player meets first

Full rows, with evidence and the proposed fix, are in `work/keyaudit/findings.tsv`.

| id | first met | file(s) | sites | one line |
|---|---|---|---|---|
| **F1** | first navigator visit | `0000001C` + `00001CA0` `00001E29` `00001F8A` `000015C2` | 3 loads, 678 column reads, 18 DB key lookups, 41 renamed literals | the navigator's objects are named from the plain-text file `ノベルシステム\ナビデータ.txt` (column 5 = タイトル), not from the database; that file is untranslated and unshipped, so both `titles-jp-en` and the translated `タイトル` column now address objects that do not exist |
| **F3** | boot | `000000F2` | 653 675 686 696 703 715 | six per-table loops compare a column against an English arc name while that column is still Japanese (`リファレンスデータ`, `人物\*`, `事典場所`, `事典出来事`, `事典物`, `雑談リスト`). Only index 640 (`ナビデータ`) matches |
| **F5** | navigator, right-click on a played entry | `0000001C` | 2701 vs 4214-4217 4255-4258 | a ctx-scoped row moved a Caption's `Name` as well as its text, so two `Exists()` and six `SetProp` still address the Japanese object name |
| **F6** | end of the first scene | `0000001C` + `00001F8A` | created 6777 / 739, deleted 3248 | the two creations were renamed, the `ObjDel` was not, so the object is never removed |
| **F2** | first visit to the reference viewer | `0000001E` | 39 | `DBGetStr("解禁編") == "<English arc>"` against `リファレンスデータベース.tsv`, whose `解禁編` column was never translated |
| **F4** | encyclopedia, one location entry | `00001878` | 1005 1022 (+4 dependent branches) | one label-map row with no ctx also replaced two literals that are compared against untranslated `事典場所` columns |

**F1 is already fixed** by the navigator lane, checked this run: `work/ノベルシステム/ナビデータ.txt`
(14:14) and `work/ノベルシステム/リファレンス概要.txt` (14:46) exist, both are in
`tools/ship-list.txt` (lines 10 and 421), the generated file keeps 219 rows x 31 comma-separated
columns in CP932, column 6 (`解禁編`) is English so the 50 `二元配列[..][6]` comparisons match, and
column 1 (`分類`) is still Japanese so the 36 `二元配列[..][1] == "シナリオ"` comparisons keep
working. What is left is a play test and the same check on `リファレンス概要.txt`. It is listed here
because the defect explains the whole titles-jp-en question and because nothing else records it.

**Correction to `notes/NAVIDATA-AUDIT.md`.** That audit concluded "`ノベルシステム\ナビデータ.txt`
is dead. No script in the game references any `.txt` path." The evidence was a grep for `\.txt`
over `work/gap-audit/lits-ALL.tsv.gz`, which holds 1.59 M literals — but that file was written with
`lits_all.py`'s default filter, and `visible()` drops every literal containing a backslash, i.e.
every path. There are 9 `LoadTextFile` sites and one `DBLoadTsvFile` on a `.txt`; three of them are
in `0000001C` and two of those load `ナビデータ.txt`. The rest of that audit (the `ナビデータ` DB
table really is `シナリオデータベース.tsv`) still stands; the two mechanisms coexist — the DB table
serves the confirm panel and the `.txt` serves the timeline objects.

## 4. What this method cannot see

- **Runtime-built keys.** A key assembled from variables at run time (`DBSetActive(人物抽出[i])`,
  `AssignTemp(代数用)`, `"データベース\実況\" ++ 選択シナリオ ++ ".tsv"`) is resolved here only when
  a literal prefix or the nearest `DBSetActive` pins it down. One comparison (`000000F2:675`) is
  reported as DYNAMIC; 491 concatenated object names are parked in `obj-concat.tsv` unresolved.
- **Control flow.** The active table is taken from the nearest preceding `DBSetActive` in index
  order. A site reached by a `Jump` or `Call` from elsewhere can run with a different table. Each
  finding above was re-read by hand against its surrounding block, but the negative results
  (MAPPED / SAFE) carry that assumption.
- **`.lcm`, `.lsc` and LiveNovel links.** `00001878.lsc:00001F47` style handler references, `.lcm`
  animation files and `PR_ON*` script hooks are strings this audit treats as opaque. If an `.lsc`
  or `.lcm` contains its own object names or comparisons, nothing here would notice.
- **Save data.** Variables that persist into `save.dat` were renamed in some files (26 `varname`
  expressions in `0000001E`). An existing Japanese save would not find them. No save file was
  opened.
- **`プレイ中シナリオデータ`** is read by 18 sites and written by none of the 542 scripts; if the
  engine or the save system fills it, its values are invisible here (F8).
- **Display-only damage.** 261 of the 314 stale (literal, file) pairs are Japanese text still shown
  in a script no lane has mapped. Those are translation gaps, not key collisions, and were not
  chased.
- **The game was not launched.** Everything above is static. The five `UNSURE` findings and every
  layout consequence (F9, F10) need a mouse.

## 5. Files

Deliverables: `work/keyaudit/translated-strings.tsv` (T), `use-sites.tsv` (U), `findings.tsv`,
`data-files.tsv`, this file.
Supporting tables: `lsb-literal-diff.tsv`, `site-changes.tsv`, `obj-broken.tsv`, `obj-concat.tsv`,
`col-vs-literal.tsv`, `cmp-changed.tsv`, `var-chains.tsv`, `var-mixed.tsv`, `stale-literals.tsv`,
`samefile-roles.tsv`, `substring-parents.tsv`, `join-lit.tsv`.
Tools (all reusable, all one-process): `dumpall.py`, `ship_dump.py`, `argkeys.py`, `build_T.py`,
`build_U.py`, `build_lsbdiff.py`, `sitediff.py`, `objgraph2.py`, `colcmp3.py`, `vars.py`,
`cmpall.py`, `analyze.py`, `analyze2.py`, `active_table.py`, `join_lit.py`, `finish.py`.
Re-run order after any new build: `dumpall.py` → `ship_dump.py` → `argkeys.py` → `build_T.py` →
`build_U.py` → `build_lsbdiff.py` → `sitediff.py` → `objgraph2.py` → `colcmp3.py` → `vars.py` →
`cmpall.py` → `finish.py`.
