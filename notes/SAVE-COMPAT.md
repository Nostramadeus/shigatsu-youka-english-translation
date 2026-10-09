# Save compatibility across patch versions (Fable, 2026-09-27)

Agents only. Do not quote arc names to the owner (spoiler rule in README).

## How a LiveMaker save works (help: file.html, varlist.html, mirrored at pylivemaker.readthedocs.io/_static/LiveNovel/)
- GameSave stores: script file + the command AFTER the GameSave (command index), variables, screen state, caption (表題).
- Variable 動作タイプ (変数初期化.lsb VarNew last byte): `0` = 通常 (per game save, reset on title return);
  `3` = ステータス (initialised once after install, restored at boot, saved at exit, NOT touched by game
  save/load = shared by every slot). 340 vars are 0, 302 are 3. One file holds all of it: `save.dat`.

## What our pipeline does to saves
- batchinsert / lsb_strings apply / props / labels edit commands IN PLACE. Command count orig vs work:
  100 scripts checked 2026-09-27, 0 mismatches. => resume position of any save stays valid. More scene
  translations later change nothing here.
- Backlog text and save-slot captions written under an older build keep that build's language. Cosmetic.

## Known save-affecting change: `レポート` -> `report` in 0000001E (UI lane 2026-09-26, patch/keishiki-jp-en.tsv row 9)
- `lsb_strings apply` replaced all 111 literal sites, of which 26 are VARIABLE-NAME prefixes
  (`AssignTemp("レポート" ++ ID保存)`, `"レポート" ++ ID保存 ++ "解禁"`, `VarExists("レポート" ++ レポートチェック)`)
  and 85 are screen-object names (`ImgNew "レポート" ++ 真パーツ`). The EN build is internally consistent
  (all 111 renamed, no other script builds these names). Object names are rebuilt whenever the references
  screen opens: harmless. The variables hold the per-report parts layout/unlock arrays and live in save.dat
  under the OLD name for anyone who played the JP game or the 2026-09-25 zip (that zip's 0000001E has
  0 `report` hits, 728 `レポート`). Effect after upgrading: report-parts progress in the references
  screen appears reset; going back to JP hides progress made on EN. No crash. The `rk` ++ ID unlock flags
  (scope 3) are ASCII and were NOT renamed, so actual unlocks survive.
- FIXED 2026-09-27: keishiki row is now `レポート	report	形式` (ctx = expression must contain 形式; all 36 display/DB sites do, none of the 111 name-prefix sites do); 0000001E recompiled. Old plan: idx-target the keishiki row so only the DB-value comparisons / display sites get
  `report`, and leave the 111 `"レポート" ++ ...` sites Japanese. Reversible: recompile 0000001E from
  orig with the narrowed map.

## Arc-name status variables (現行編名, 背景名, 事典編 = scope 3, persist across slots)
- Values are the 解禁編 literals (hen-jp-en.tsv). A save.dat from JP / 09-25 holds Japanese values; the
  09-26 build compares against English literals. Self-heals: 0000001C:67-68 reassigns 現行編名 on every
  navigator card click, 0000001C:4410 reassigns 背景名 when a scenario starts; scene files assign both.
  Window = first screen after boot may take the default branch once. Cosmetic, one-time.

## Rule for future UI-lane work
Before mapping a JP literal, grep the dump for `"<literal>" ++` and `VarExists("<literal>"`: a hit means
the literal is a variable/object-name prefix and must be excluded (idx-target), or every player's
save.dat changes meaning on upgrade. Tell players: copy save.dat before applying a new patch zip.
