# REMAINING-JP-AUDIT.md — every Japanese string that can still reach the screen

Written 2026-09-26, 15:30. Read-only audit: nothing shipped was edited.
Snapshot point: the compile lane finished a full rebuild at **15:05:08** (`work/compile-pause.log`,
"ALL DONE 15:05:08"). Everything below was measured from the files as they stood after that, NOT
from `work/keyaudit/dump-ship.tsv.gz` / `params-ship.tsv.gz` (those are 14:32 and are stale for
`0000001C` (15:02), `0000001E` (15:05) and all 20 section-3 scene scripts).

---

## DONE / NEXT

**DONE**

| pass | what it covered | output |
|---|---|---|
| fresh snapshot of the shipped build | all 74 `.lsb` in `tools/ship-list.txt`, read from `work/<rel>`: every `Str` param with its command + arg key, every flattened command, every message row | `work/jpaudit/snap-params.tsv` (41,664), `snap-cmds.tsv` (33,359), `snap-msg.tsv` (33,821) |
| message text of EVERY reachable script | 514 `.lsb` = the call-graph closure from `000000F2` (`work/gap-audit/reach.txt`) ∪ ship-list ∪ every `.lsb` named as a target in `work/gap-audit/callgraph.tsv`; each read AS SHIPPED (`work/` if built, else `orig/`) | `work/jpaudit/allmsg-counts.tsv`, `allmsg-jp.tsv` (66,951 JP rows), `untranslated-scripts.tsv` |
| display-position literals | Caption text, `SetProp <obj> 50/151` (property 50 = an object's text), MesNew / Menu / Button / TileNew label slots, with DB-lookup key literals split out | `work/jpaudit/findings-literals.tsv` |
| tables | all 23 shipped `work/データベース/**/*.tsv` (CP932), JP cells per column, column marked displayed when its name appears in a display expression in the fresh snapshot | `work/jpaudit/table-jp.tsv`, `table-cells-jp.tsv` |
| reachability of the milestone events | mapped every `Calc 全体進行 = N` in `000015DC` to its enclosing `選択シナリオ == M` and intersected with the parts 1-3 fence | `work/jpaudit/zentai.py` output (in this file, §4) |
| curated findings | the verified rows, each with class, reach, cause and the exact map file it belongs in | `work/jpaudit/findings.tsv` |

**NEXT (not done)**

1. `work/jpaudit/findings-literals.tsv` is RAW: 380 rows, and roughly two thirds are object names
   read back with `GetProp("<obj>", 50)`, not printed text. The curated `findings.tsv` is the
   trustworthy list. A second filter (drop any literal that is also a `Name` param of a Caption
   anywhere in the same file) would clean it; not written.
2. Row-level fence filtering of the tables. `table-jp.tsv` gives JP cells per column for the whole
   table; it does NOT yet split "rows a parts 1-3 player can open" from parts 4+ rows. The keys
   exist (`リファレンスデータベース.解禁シナリオID`, `雑談リスト.連番`, `あらすじ.シナリオ番号`,
   `シナリオデータベース.連番`) and are all 連番, so the fence set in
   `work/reachability/reachable-after-306.tsv` can be joined straight onto them.
3. Reference-document number → script id. 150 document-body scripts are jumped from `0000001E`,
   but the dispatch runs through an `.lsc` click handler keyed on the object name
   `DBGetStr("登場順")`, so which reference row opens which script was not resolved. Until it is,
   the count of documents a parts 1-3 player can open is unknown (the table has the unlock
   scenario per row, so the join is possible from the other side).
4. `0000156A.lsb` (3,219 JP message rows) — its role is not settled. `tools/ship-list.txt` calls it
   "end-of-synopsis notice", but it carries 20 full text scenarios. Reachability not determined.
5. Menu / choice arrays built with `AddArray` in `Calc` were not swept separately (only
   `Menu`/`Button`/`PrevMenuNew` component slots). `work/gap-audit/menus-shipped.tsv` exists and
   was not cross-checked.
6. `.lsc` files were not opened. Captions created inside an `.lsc` click handler are invisible to
   this audit (see §6).

---

## 1. Counts by class

From `work/jpaudit/findings.tsv` (curated) and the generated tables.

| class | what it is | count |
|---|---|---|
| `MSG_TEXT` | Japanese message text (TextIns / LiveNovel) in a script with no `lns-en` counterpart | **381 scripts**, 66,951 JP rows |
| `CAPTION_LIT` | JP string literal in a Caption's text argument | 28 verified sites |
| `SETPROP_LIT` | JP string literal written into property 50 (an object's text) | 13 verified sites |
| `DBCOL_DISPLAY` | a displayed value that comes from a DB column that is still Japanese | 24 displayed columns |
| `DBKEY_NOT_SHOWN` | JP literal that is a DB table / key column / key value (correct as is) | 213 sites |
| `IMAGE` | a Japanese word baked into a picture, no string anywhere | 1 (`固定中`) |
| `UNSURE` | printed, but may be an engine keyword | 3 columns (`特殊1/2/3` of リファレンスデータベース) |

Message-text scripts by kind (`work/jpaudit/untranslated-scripts.tsv`):

| kind | in fence | files |
|---|---|---|
| `SCENE` (a navigator entry's script) | no | 170 |
| `SCENE` | **yes** | 1 (`000005C1`, entry 138 — already the known frontier file) |
| `SCENE-alt` (裏 hidden-route variant of an in-fence entry) | **yes** | 5 |
| `SYSTEM` (navigator / side screens / milestone events / toasts) | n/a | 14 |
| `OTHER` (mostly reference-document bodies) | n/a | 191 |

## 2. Counts by reach

| reach | findings |
|---|---|
| scene HUD (every scene) | 2 — the `固定中` picture, and `閲覧年月日` printed in the in-scene top bar |
| navigator | 4 — the guide greeting script `000015C2`, the save/load panel `0000227A` (10 labels + 2 sentences), `現在の文字数` in the memo screen |
| right-click menu | 3 — `0000189A` (50 JP message rows, not shipped at all), `000018BF` 残ポイント + 3 substituted words |
| side screens | reference: `0000001E` 移動 / 祀耀 / 年, **150 document-body scripts (6,876 JP rows)**; encyclopedia: `00001878` 67 JP message rows + 場所名 / 出来事名 / 詳細チャプター / 簡易説明 columns |
| scene-end screen (after every scene) | 1 — `000019DD`, 5 JP message rows (人物：, 文字数：, ルート) |
| reachable in parts 1-3, milestone event | 1 — `00001984` (`予告`), reached at 全体進行 = 19 |
| later-part-only | `00001867`, `00001AFE`, `00001C4D`, `00001EC0`, `00001CA0`, `00001E29`, `000021E2` |
| in-fence scene scripts still Japanese | 6 — `000005C1` (entry 138, known) plus 5 裏 variants: `00002450`, `00002427`, `00002420`, `0000240C`, `0000241B` |
| unsure | `0000156A` (3,219 rows), `00002444` (1,895 rows), `000015E3` idx 1624 |

## 3. Top list, ordered by what a player meets first

1. **`000015C2.lsb` — 63 JP message rows out of 153. PRIORITY 1.**
   Reached by `0000001C.lsb` idx 3073 → `000015B3.lsb` idx 98 (`Jump … 全体進行 == 1`) → idx 8 →
   `000015C2.lsb`. `全体進行 = 1` is written at `000015DC.lsb` idx 879 under
   `If 選択シナリオ == 195 / If 全体進行 < 1`, and entry **195 is the only entry open on a fresh
   save** (`000000F2.lsb` idx 310 `Calc st195 = 3`). So this plays the moment the first scene ends.
   It is IN `tools/ship-list.txt`, but only in the "title-lookup files" group — its titles were
   mapped, its dialogue was never extracted. No `lns-en/000015C2-*.lns` exists.
   Message rows carry `<PG>` (the NEXT PAGE mark) and `{MESON "500"}`, matching what the owner saw.
2. **`0000189A.lsb` — 50 JP message rows. PRIORITY 2 (chatter list).**
   Reached by `0000001C.lsb` idx 3512. **Not in `tools/ship-list.txt` at all**, so the original
   Japanese file is what ships. Its companion `000018BF.lsb` IS shipped and has 0 JP message rows,
   but 8 JP literals written into property 50 (残ポイント, and 死月妖花 / ネクロ / 『何者か』
   substituted into choice labels by `StringReplace` at idx 302/304/306).
3. `000019DD.lsb` — 5 JP message rows on the screen shown after **every** scene.
4. `0000227A.lsb` — the save/load panel, reachable from the navigator (idx 3514, 5608) and from
   boot (`000000F2` idx 584): 8 `セーブデータ1..4` captions and 2 long JP instruction sentences.
   It is in the ship list only under "Item B (Q2361)", i.e. it was classified as an untranslated
   scene script; it is not a scene.
5. `閲覧年月日` in the in-scene top bar — the known one, already being worked.
6. `固定中` — the right end of that bar. **Not a string**: `0000001C.lsb` idx 2994 / 4497 create a
   `Cinema` object from `グラフィック\システム\固定中.lcm`. No labels map can ever reach it; it needs
   the image lane.
7. `00001878.lsb` — 67 JP message rows the guide speaks on the first visit to the encyclopedia,
   plus 場所名 / 出来事名 printed as the caption text of every card.
8. The **reference document bodies**: 150 scripts jumped from `0000001E`, 6,876 JP message rows,
   none of them in the ship list and none with an `lns-en` file. The reference TABLE
   (titles, summaries, dates) is English; opening a document shows Japanese.
9. `00001984.lsb` — `予告`, 200pt, at 全体進行 = 19 (inside the fence).

## 4. Milestone events (`全体進行`) and the fence

`000015B3.lsb` dispatches one event per `全体進行` value. Intersecting every
`Calc 全体進行 = N` in `000015DC.lsb` with the fence in
`work/reachability/reachable-after-306.tsv` gives the values a parts 1-3 player can reach:

**1, 3, 5, 7, 9, 11, 13, 19.**

- 1 → `000015C2` (63 JP message rows) — **the priority-1 finding**
- 3, 5, 7, 9, 11, 13 → `00001792`, `0000176E`, `000017A5`, `000017B6`, `000017EC`, `0000180D` —
  checked: **0 text commands each** (picture + sound only), so nothing to translate
- 19 → `0000198D` (0 text commands) → `00001984` (`予告` caption, 13 JP message rows)

Everything else (15, 17, 21…160) is set by an out-of-fence entry, so `00001867`, `00001973`,
`00001AFE`, `00001C4D`, `00001EC0`, `00001CA0`, `00001E29`, `000021E2`, `00001A13` are
later-part-only.

## 5. Never-mapped items, and the map each belongs in

| file | count | map file to add the row to |
|---|---|---|
| `0000227A.lsb` | 10 | new `patch/labels-0000227A.tsv` |
| `0000001E.lsb` | 5 | `patch/labels-0000001E.tsv` |
| `000018BF.lsb` | 8 | new `patch/labels-000018BF.tsv` |
| `00001C4D.lsb` | 4 | new `patch/labels-00001C4D.tsv` |
| `00001E29.lsb` | 3 | new `patch/labels-00001E29.tsv` |
| `00001CA0.lsb` | 2 | new `patch/labels-00001CA0.tsv` |
| `0000001C.lsb` | 1 | `patch/labels-0000001C.tsv` |
| `00001867.lsb` | 1 | new `patch/labels-00001867.tsv` |
| `00001984.lsb` | 1 | new `patch/labels-00001984.tsv` |
| `00001AFE.lsb` | 1 | new `patch/labels-00001AFE.tsv` |
| `00001EC0.lsb` | 1 | new `patch/labels-00001EC0.tsv` |
| `000015E3.lsb` | 1 | `patch/extra-maps-000015E3.txt` |
| `グラフィック/システム/固定中.lcm` | 1 | image lane, not a map |
| `tsv-en/事典出来事.tsv` col 年月日 | 10 rows | table lane |
| `tsv-en/事典場所.tsv` col 場所名 | 84 rows | table lane — **conflicts with Q2054**, see §7 |
| `tsv-en/事典出来事.tsv` col 出来事名 | 57 rows | table lane — same Q2054 conflict |
| `tsv-en/シナリオデータベース.tsv` col 閲覧年月日 | 171 rows | already in flight |

## 6. What this method cannot see

1. **`.lsc` files.** Click handlers, mouse-in handlers and menu scripts live in `.lsc` (e.g.
   `"0000001C.lsc:000016BC"`, `"00001878.lsc:楽曲オンマウス"`). Any Caption created inside one is
   invisible here. Every hover caption and every button click reaction goes through one.
2. **Computed strings.** A caption text like `DBGetStr("キャプション" ++ 番号 + 2)` names its column
   at run time; the column can only be guessed. Same for any label chosen by `@Sender`.
3. **One hop only.** A JP literal assigned to a variable that is assigned to a second variable that
   is then printed was not followed past the first hop.
4. **Baked pictures.** Japanese inside `.gal` / `.lcm` art is out of scope except where a string
   search found the file name (`固定中`). The image lane's own inventory is
   `notes/_db/_image-text-inventory.tsv`.
5. **`シーン回想.lsb`** could not be read (`text_scenarios()` raises `KeyError`); its message text
   was not scanned. It is not in `work/gap-audit/reach.txt`.
6. **Row-level table fencing** is not applied (see NEXT item 2), so the table JP counts mix
   parts 1-3 rows with parts 4+ rows that are untranslated by design.
7. **A moving target.** The compile lane rebuilt 24 `.lsb` files between 14:57 and 15:05 while this
   audit was running; an earlier pass of mine read the pre-rebuild `000004E3.lsb` and reported 273
   JP message rows that the post-rebuild file does not have. Anything measured here needs re-running
   after the next rebuild. `work/jpaudit/snapshot.py` and `allmsg.py` do exactly that.

## 7. Two rulings that need re-reading

1. **Q2054 / ship-list "場所名 stays JP", "出来事名 stays JP".** Those columns are not only keys:
   `00001878.lsb` idx 750/751/758/759/1009 create the place card with
   `Caption DBGetStr("場所名") … 1 DBGetStr("場所名")` — the object NAME and the printed TEXT are the
   same column. Same at idx 1340-1342/1405 for 出来事名. Keeping them JP keeps the encyclopedia
   card labels Japanese. The fix is a second column (an English display value) or a labels map, not
   a translation of the key.
2. **`notes/STYLE.md` "NEVER-TRANSLATE COLUMNS … 閲覧年月日 (object names)".** In
   `シナリオデータベース.tsv` that column is printed at `0000001C.lsb` idx 6023 and in the
   reference toast at `000016C3.lsb` idx 27/46/65/176/194/212. The "object names" justification
   holds for a different column use; the STYLE line as written forbids translating a string the
   player reads.

## 8. Generated files

    work/jpaudit/snapshot.py         fresh dump of the shipped build (params / cmds / msg)
    work/jpaudit/allmsg.py           message text of every reachable .lsb, as shipped
    work/jpaudit/classify.py         SCENE vs SYSTEM vs OTHER, fence tagging
    work/jpaudit/findings.py         JP literals in display positions
    work/jpaudit/tables.py           JP cells per shipped table column, displayed flag
    work/jpaudit/zentai.py           全体進行 milestone -> scenario -> fence
    work/jpaudit/grepship.py         grep the flattened shipped command dump
    work/jpaudit/findings.tsv        CURATED findings (the trustworthy list)
    work/jpaudit/untranslated-scripts.tsv   lsb, msg rows, jp rows, kind, fence, reached_from
    work/jpaudit/allmsg-jp.tsv       every JP message row, with the raw markup
    work/jpaudit/table-jp.tsv        per column: displayed?, rows, JP rows
    work/jpaudit/findings-literals.tsv      RAW literal sweep (needs the §NEXT-1 filter)
