# CLUES.md — machine-readable signals besides text colour (TRICKS, 2026-09-26)

Scope: the 39 part-1..3 ids (orders 1-39 of notes/_db/_file-order.tsv, 0000001E … 000005AC), 6,020 text cells.
Some checks were run game-wide; they say so. Sources: lns/, orig/*.lsb (dumped with pylivemaker), notes/_db tables,
notes/v2/SUMMARY.md (pass-2 narrator and time lines only). No lns-en/, no pass-1 notes. Nothing in tools/ or in
any note master was changed.

Scripts and raw output: `notes/v2/_tmp/tricks/` (run with `uv run --no-project --python 3.12 python`, add
`--with pylivemaker` for lsbdump.py).

| script | writes | what |
|---|---|---|
| lsbdump.py OUTDIR ids/paths | dump/, dumpall/ (455 root .lsb), dumpsys/ (87 ノベルシステム .lsb) | one line per LSB command: index, LineNo, indent, type, params |
| cellstate.py ids | cells39.tsv, cells-all.tsv (74,253 cells) | per text cell: kind, colour, speaker, sprites on screen, background, BGM, commands since the previous cell, style ids with size/unk5/ruby, text. Cell split = style_colors rule; cell counts equal `style_colors.cells()` for every id (0 mismatches) |
| h2.py, h2b.py, h2c.py | h2-out.txt, h2b-out.txt, h2c-out.txt | sprites vs speaker, per-block sprites, narrator-never-drawn and addressee checks |
| swap.py cells.tsv | swap-all.tsv | every CG whose file name contains an arrow (viewpoint switch) |
| h4.py | h4-out.txt | BGM starts/stops per scene in run order, QUAKE counts |
| h5.py | h5-out.txt | font size, unk5, ruby, text-speed tags per cell class |
| ruby.py ids | ruby39.tsv | ruby base -> reading pairs, first cell |
| scdb.py | scdb-39.tsv | シナリオデータベース rows for the 39 ids (via the navigator entry) |
| reach.py ids | reach-out.txt | reachable text blocks per scene, and the variables that guard them |
| enc.py | enc-out.txt | encyclopedia / profile rows unlocked by a scene (stNNN) |

Cell keys below are `id:block:cell`, the key of read/chunkNN.txt and every note.

Limits of cellstate.py: sprite and background state is tracked inside one block (.lns file) and starts empty at
each block; a sprite created by the .lsb outside the text block is not seen. BGM order across blocks is given by
h4.py in .lsbref (run) order.

---

## Summary

| # | hypothesis | verdict | key count |
|---|---|---|---|
| 1 | message box names the narrator or a mode | **partly**: mode yes, narrator no | 0 of 5 viewpoint switches change the box; 8 one-cell blocks use 大文字用, 2 reachable blocks use 赤 |
| 2 | sprites fix speaker / addressee | **partly**: sprites fix the NARRATOR (never drawn) and the ADDRESSEE, not the speaker; plus 5 explicit viewpoint-switch CGs | narrator drawn in 1 of 5,834 narration-cell states; 5 switch CGs in parts 1-3 (8 game-wide) |
| 3 | voice files name speakers | **no** | 0 voice-acting files; the VOICE channel plays sound effects (3,345 cues game-wide) |
| 4 | BGM/SE as mood / event markers | **partly** | 156 BGM starts, 116 stops, 37 QUAKE in 39 ids; two BGM tracks are character themes (五島 ×6, 伊勢 ×3) |
| 5 | text style beyond colour | **partly** | 59 big-font cells, 27 slow-text cells, 3 emphasis-dot (圏点) cells; 0 cells open with （ (thoughts are not styled) |
| 6 | data tables as fence-safe per-scene facts | **holds** | 解禁人物 = narrator: 31 of 33 entries agree with SUMMARY, 1 more agrees with the switch CG, 0 contradict; 閲覧年月日 gives a start time for 33 of 39 ids, 0 contradictions |
| 7 | variables pick narrator / variants | **partly**: no narrator variable; variants are picked by `分岐ルートへ` / `途中から`, and 818 cells are unreachable | 0000034C blocks 11 and 23 are never shown |
| 8 | anything else | ruby = canonical readings (26 of 26 agree with GLOSSARY, 70 more not in GLOSSARY); name-entry variable only in system text; 実況 顔 column labels 2,803 of 2,944 rows | — |

---

## 1. Message box identity — partly (mode yes, narrator no)

Facts about the engine:
- `メッセージボックス作成.lsb` has 13 `MesNew` commands, but they are 7 named variants (the second half, from
  command 194, repeats six of them). A scene selects a variant with
  `Call メッセージボックス作成.lsb:0 Params="<name>"`. Every story `TextIns` targets the same object
  `"メッセージボックス"`; the name of the variant is the only switch.
- The variant stays until the next call. A scene with no call inherits the box of whatever ran before
  (in practice `(標準)`).

| variant | box | font | used game-wide (calls) | used in the 39 ids |
|---|---|---|---|---|
| (標準) | 600x500 at x=310-w/2, y=20, black | ＭＳ 明朝 30, white | 96 | reset after every special box |
| (編集用) | 490x104, bottom, transparent | ＭＳ ゴシック 16 | 0 | 0 |
| 大文字用 | full screen 960x540, transparent | ＭＳ 明朝 60 | 73 | 8 blocks |
| 電話 | same geometry and font as (標準) | ＭＳ 明朝 30 | 2 | 0 |
| イベント用 | 630x100 at the bottom, dark-blue fill | ＭＳ Ｐ明朝 20 | 75 | system/guide text only (0000001E, 000000F2) |
| リファレンス | 600x200 at y=345, black | ＭＳ 明朝 20 | 0 | 0 |
| 赤 | 600x500, dark-red fill | ＭＳ 明朝 30, RED text | 4 | 2 reachable blocks |

Every non-(標準) box in the 39 ids:

| box | blocks (cells) | what is in them |
|---|---|---|
| 大文字用 | 000001E3:12, :20; 000001E7:15; 000002FA:15, :23; 000004BB:12; 000004E3:15, :23 (1 cell each) | one giant line flashed on screen, no quote marks except 000004BB:12:0 |
| 赤 | 00000024:51 (48 cells, reachable only when `分岐ルートへ` = 1, see 7); 00000488:48 (13 cells, the voice flood) | the red box. 00000024:57 and :63 are also set to 赤 but are unreachable |
| イベント用 | 0000001E, 000000F2 system blocks | the guide addressing the player |

Scene -> box -> narrator (SUMMARY):

| id | box calls in the file | SUMMARY narrator |
|---|---|---|
| 0000001E | (標準), イベント用 | none (system) |
| 00000024 | (標準), 赤 (block 51) | なつみ (16, 67); 春花 (47, 51) |
| 000000F2 | イベント用 | none (system) |
| 000001DB | (標準) | なつみ |
| 000001DD, 000001DF, 000001E1, 000001E5 | none (inherit (標準)) | なつみ |
| 000001E3 | (標準), 大文字用 (12, 20) | なつみ |
| 000001E7 | (標準), 大文字用 (15) | なつみ |
| 0000020B, 000002F6, 000002F8, 0000033D, 0000034C, 00000366, 0000037D, 00000460, 00000473, 000004A7, 00000522 | none | 五島 |
| 0000020D | (標準) | 五島 |
| 000002FA | (標準), 大文字用 (15, 23) | 五島 |
| 00000488 | (標準), 赤 (48) | 五島 |
| 000003A8, 000003AE, 000003B4, 000003BC | none | none (transcripts) |
| 000004BB | (標準), 大文字用 (12) | 五島; なつみ in 16:0-36 |
| 000004CF | none | なつみ; 五島 12:60-96, 19, 25 |
| 000004E3 | (標準), 大文字用 (15, 23) | なつみ |
| 000004F9, 0000050E, 00000538, 00000550, 00000564, 0000057B, 00000595, 000005AC | none | なつみ (000004F9: 五島 from 11:128, see 2) |

Counts: the narrator changes 5 times inside a block (section 2) and at 4 block/file boundaries in these ids; the
box changes at none of them. The 電話 box is never used in parts 1-3; phone calls are shown with phone sprites
(section 2) in the (標準) box.

**How to use it in the pipeline.** Add the box name per block to the per-cell data (the `Call ... Params` that
precedes each `TextIns` in the .lsb; reach.py already walks that order). The packet (tools/db/pack.py) and the
read-through chunks would mark 大文字用 cells as "full-screen flash line" and 赤 cells as "red box": both tell the
note-taker and the drafter that the line is not ordinary narration and is usually unattributed. The EN patch must
keep these blocks short enough for one screen at size 60 (大文字用); tools/qa_check.py could flag an EN
大文字用 cell longer than the JP.

---

## 2. Sprites / faces — partly (fixes the narrator and the addressee; not the speaker)

Evidence (39 ids):
- 118 distinct image paths are on screen while text shows; 75 are standing sprites under `立ち絵\人物`. 64 of 75
  file names contain the character's name (なつみ, 春花, 五島, 桃子, 伊勢, 茜, 美冬, 良治, 栄一郎, and なつみ母 /
  春花母). The other 11 are unnamed figures (死神 ×7 variants, 串刺し, 赤人, 赤い人立ち, 立木三日).
- The suffix is a POSE or shot size, rarely an emotion: バストアップ 7, plain 7, 横顔 4, 考える 6, 腕組み 4,
  うつむき 2, 合掌 2 … Emotion words appear in 3 names only: 怒り, 驚き, 眠い. So "character" yes, "emotion" mostly no.
- Items encode phone state: `スマフォ黄入` 249 cells, `スマフォ赤入` 75, `スマフォ黄切` 42, `スマフォ赤切` 24,
  `スマフォ青切` 10, `スマフォ青入` 1, `ガラケ―赤入` 8 (入 = call on, 切 = call ended; the colour is the phone).
  This is the "phone mode" marker; the 電話 box is not used for it.

**The narrator is never drawn.** With the narrator per cell from SUMMARY (corrected by the switch CGs below):

| check | count |
|---|---|
| cells in first-person narration (39 ids) | 5,834 |
| of those, the narrator's own standing sprite on screen | **1** (000004A7:11:1, 五島万歳, the opening pose) |

**Viewpoint-switch CGs.** The engine plays a short animation file named `立ち絵\人物\lcm\X→Y.lcm` at the moment
the first-person narrator changes inside a block. Game-wide there are 8; 5 are in parts 1-3:

| cell (first cell after the CG) | CG | SUMMARY says | agreement |
|---|---|---|---|
| 000004BB:16:0 | 五島→なつみ | 16 narrated by なつみ from 16:2 | agrees |
| 000004BB:16:37 | なつみ→五島 | 五島 "from 16:41 (no marker)" | **differs by 4 cells: the switch is at 16:37** (the background also changes there) |
| 000004CF:12:60 | なつみ→五島 | 五島 12:60-96 | agrees exactly |
| 000004CF:12:97 | 五島→なつみ | なつみ from 12:97 | agrees exactly |
| 000004F9:11:128 | なつみ→五島 | なつみ only | **SUMMARY misses this switch**; シナリオデータベース 解禁人物 = なつみ/五島 supports the CG |

Outside parts 1-3: 00000617:8:43 (なつみ→五島), 00000F0D:56:0 (夏菜→伊勢), 00000F0D:62:0 (伊勢→夏菜).

**Sprite vs speaker.** Of 2,537 quote cells with a colour speaker: 1,326 have the speaker among the standing
sprites, 1,038 have sprites but not the speaker (typically the narrator speaking to the drawn person), 173 have no
sprite. Of 134 uncoloured quote cells, 55 show exactly one named sprite; read one by one, that sprite is the
listener (the officers in 000003B4 and 000003BC talking to 伊勢, the waitress in 000004BB:8 serving 伊勢), not the
speaker. So the sprite does not fix open speakers. Two candidates worth a human look, not attributed here:
000004E3:27:14-20 (uncoloured, 春花覗き込み on screen) and 00000538:11:85-87 (『…』 uncoloured, 五島怒りバストアップ).

**Addressee.** 61 narrator quotes open with a vocative (「春花、」「五島！」…). 46 of them have a named sprite on
screen; in 38 the addressee is on screen (28: the only sprite). 7 of the 8 misses are phone calls or shouts to
someone off screen; 1 is a regex false positive (000004CF:12:87).

**How to use it in the pipeline.** (a) Turn swap-all.tsv into a small table `viewpoint_switch(file_id, block,
cell, from, to)` in tools/db and print it in the packet next to the narrator line; the read-through brief can then
say "a switch CG at X is a fact; do not guess switch points". (b) Add a `drawn` column (characters on screen per
cell, from cellstate.py) to read/speakers/chunkNN.tsv: a narrator guess that is drawn on screen is wrong, and the
drawn person is the default addressee for the narrator's lines (useful for pronouns and address forms in
RELATIONS). (c) Phone-item cells mark phone calls for the drafter (tone, "on the phone" tags).

---

## 3. Voice — no

- The archive has no voice folder. The only speech-like sound files: `サウンド\リファレンス専用\超炭酸ボイス\*.ogg`
  (6, an English ad jingle in the reference section), `事典音声` (4 music pieces), and named effects outside parts
  1-3 (五島泣き声, 夏菜泣き声, 夏菜の声エフェクト1-3, 春花拘束).
- The channel called `VOICE` carries sound effects: 3,345 PLAYSND cues game-wide, e.g. SE\携帯押す 162,
  SE\sceneswitch2 131, SE\down1 104. `VOICE2` 109.
- In the 39 ids, voice-like cues: 4 moans (SE\うめき声, うめき声2) and 5 TV-voice ambience cues. None names a speaker.

**How to use it in the pipeline.** Nothing to carry. One practical note for the harness: sound effects on the
`VOICE` channel are muted by the same session mute; no extra audio path exists.

---

## 4. Sound / BGM cues — partly

39 ids: 156 BGM starts, 116 BGM stops, 37 QUAKE (screen shake), 29 distinct BGM tracks. Full per-scene list in
h4-out.txt (`cell track > cell [stop] > …`, run order). Most used: 日没廃校 24, togisuma 16, death_sound1 14,
残滓念 13, Lucky_You 10, 日常 10, ネジの壊れたロボット 10, 見えない光_2 9.

Findings useful as markers:
- **Character themes.** Track `五島` starts 6 times (000001E3:8:16, 8:77; 000001E5:23:88, 41:14;
  000004A7:11:2; 00000564:11:13) and track `伊勢` 3 times (000003B4:8:26, 000004A7:11:31, 000004BB:8:17), each time
  when that character enters or takes over the scene.
- **Silence before a sting.** Of 14 `death_sound1` starts, 10 follow a BGM `[stop]` within 0-4 cells of the same
  block (8 in live blocks, e.g. 000001E1:33:52, 0000034C:17:110, 00000366:11:67, 000004E3:27:114). death_sound1 is a
  short shock cue.
- **Scene cuts.** At the viewpoint switches of section 2 the background changes on the switch cell
  (000004BB:16:37, 000004CF:12:60 and 12:97); the BGM changes there too at 000004CF:12:97 and 4-6 cells later at
  000004BB:16:41-43.

Sample (4 of 39 rows):

| id | BGM in run order |
|---|---|
| 000001DD | 11:10 日常 > 11:73 [stop] > 11:75 日曜日の朝 > 11:141 [stop] > 11:154 日曜日の朝 |
| 0000020D | 11:12 日没廃校 > 11:46 [stop] > 11:47 忍び寄る影 > 11:54 [stop] > 11:55 明かされた真実 > 11:58 [stop] > 11:95 togisuma |
| 000004A7 | 11:2 五島 > 11:21 [stop] > 11:31 伊勢 > 11:109 [stop] |
| 00000522 | 11:0 avemaria > 11:170 [stop] |

**How to use it in the pipeline.** Put a `stage` table (file_id, block, cell, bg, bgm, events) from cellstate.py
into tools/db and let `query.py file <id>` print the BGM/background change cells. Note-takers can use background
changes as scene boundaries in their event lists (a fact, not a reading), and the drafter gets "sting here" /
"shake here" hints for sound words and exclamations. Not a speaker or narrator signal.

---

## 5. Text style beyond colour — partly

The `TDecorate` fields besides colour (unk2): `unk4` = font size (0 = box default), `unk5` = a style flag
(1 in story text), `ruby` = reading. Counts over the 6,020 cells:

| signal | cells | where / what |
|---|---|---|
| big font (unk4 16-80) | 59 (25 narration-type, 34 「」) | shouts (「ダメ！」 48), headlines, giant flash lines 60-80, and 000002F6:11:71-76 where the size steps DOWN 24 > 20 > 16 > 16 (a voice trailing off) |
| unk5 = 3 | 4 | a news headline (000001DF:11:115) and board-post headers (000001E1:33:120-122): likely bold |
| unk5 = 0 | 46 | system/guide text only (0000001E, 000000F2) |
| slow text `<TXSPS>` | 27 | drawn-out, weak or menacing speech (000002FA:11:35-63 run of 14; 000001DB:15:127-136) |
| `<TXSPD>` (set delay) | 11 | garbled or stuttering lines, the voice flood 00000488:48 |
| `<TXSPF>` fast | 1 | system label |
| QUAKE before the cell | 37 | shock cells |
| ruby | 192 cells, 98 pairs | readings; 3 pairs are 圏点 emphasis dots: 安全のため (000001DF:11:39), あの人 (00000522:11:31), ある (00000538:11:189) |
| cells opening with （ | **0** | thoughts are not bracketed and not styled |
| cells opening with 『 | 7 | quoted voices/phrases; 1 uses unk5=0 |
| cells opening with " | 28 | text messages / search strings |

Thoughts vs narration: no difference in style id, size, flag or speed. Style ids are per file (SPEAKER-COLORS.md),
so "style id" counts across files mean nothing; the fields above are the comparable part.

**How to use it in the pipeline.** Add two flags to the per-cell data: `big` (unk4 > 0, with the size) and
`speed` (S/D). The drafter brief: a big cell is shouted or a headline (caps or "!" per STYLE.md), a descending
size run is fading speech (ellipses), TXSPS is drawn out, 圏点 is emphasis (italics). qa_check.py can check that
an EN cell keeps its STYLE wrapper when the JP one has size or ruby=・・・ (else the emphasis silently disappears).

---

## 6. Data tables as fence-safe facts — holds

### 6.1 シナリオデータベース.tsv (joined through _navigator-order.tsv; 33 of 39 ids have an entry)

| column | what it says | agreement over the 39 ids |
|---|---|---|
| 連番 | navigator entry id (= 実況__NNN, stNNN in the encyclopedia) | key |
| 閲覧年月日 | in-story date and START time, e.g. `祀耀800年　四月　八日 19:00` | 33 filled; 20 agree with a SUMMARY clock/day line, 12 add a time SUMMARY does not have, 1 needs a look (0000020D: 19:10 vs board timestamps 23:50-0:35 inside the file), 0 contradict |
| タイトル | chapter title shown in the navigator | 33 |
| 解禁編 | arc: 呪殺編 (32), 明徴編 (00000024) | — |
| 列番号 | navigator column 1-6 | layout only; not a narrator |
| 解禁人物 | the viewpoint character(s): 古郡なつみ, 五島絵梨奈, or 古郡なつみ/五島絵梨奈 | **31 of 33 = SUMMARY narrator exactly**; 000004F9 lists both and the switch CG at 11:128 confirms it (SUMMARY missed it); 00000024 lists なつみ only = the narrator of the default route (blocks 16; the 春花 blocks 47/51 play only on the new route, section 7). 0 contradictions |
| 入手年月日 | same date in the real calendar (祀耀800年 = 2020年); `0` in 15 of 33 rows | duplicate of 閲覧年月日 |
| 概要, 形式, 備考 | 0 / empty for all 33 | no facts |
| 文字数1 | character count of the scene | — |

The 6 ids without an entry (0000001E, 000000F2, 000003A8, 000003AE, 000003B4, 000003BC) are system text or the
four transcript files launched from 0000001E.

Start times in reading order (the reading order is NOT chronological; e.g. 00000460 at 09:50 is read after
0000037D on the 9th):

| id | start | id | start | id | start |
|---|---|---|---|---|---|
| 00000024 | 5/5 23:59 | 0000033D | 4/8 20:20 | 000004E3 | 4/8 16:40 |
| 000001DB | 4/7 16:00 | 0000034C | 4/8 20:40 | 000004F9 | 4/8 19:00 |
| 000001DD | 4/8 06:30 | 00000366 | 4/8 21:00 | 0000050E | 4/8 19:10 |
| 000001DF | 4/8 08:20 | 0000037D | 4/9 10:00 | 00000522 | 4/8 23:55 |
| 000001E1 | 4/8 12:00 | 00000460 | 4/8 09:50 | 00000538 | 4/8 16:40 |
| 000001E3 | 4/8 12:20 | 00000473 | 4/8 20:00 | 00000550 | 4/8 18:00 |
| 000001E5 | 4/8 13:10 | 00000488 | 4/8 20:20 | 00000564 | 4/8 18:30 |
| 000001E7 | 4/8 14:00 | 000004A7 | 4/8 14:00 | 0000057B | 4/8 23:55 |
| 0000020B | 4/8 19:00 | 000004BB | 4/8 16:00 | 00000595 | 4/8 13:15 |
| 0000020D | 4/8 19:10 | 000004CF | 4/8 16:20 | 000005AC | 4/8 13:40 |
| 000002F6 | 4/8 19:10 | | | | |
| 000002F8 | 4/8 19:40 | | | | |
| 000002FA | 4/8 20:00 | | | | |

(Year 祀耀800 for all but 00000024; its row says 祀耀800年 五月 五日.)

### 6.2 Encyclopedia and profile tables (unlock-gated)

Every row of 事典人物 / 事典出来事 / 事典場所 / 事典物 and of the 24 `人物__<name>.tsv` tables carries an unlock
scene `stNNN` (navigator entry). Mapped to the lsb through _navigator-order.tsv, 0 rows fail to map. Rows unlocked
inside parts 1-3: 事典人物 6, 事典出来事 9 (with in-story date column 年月日), 事典場所 13, 事典物 5, 人物__五島絵梨奈 11,
人物__古郡なつみ 11, 人物__新村春花 8, 人物__伊勢大二郎 7, 人物__古郡茜 5, 人物__新村美冬 4, 人物__五島桃子 3,
人物__古郡良治 3; 29 of the 39 ids unlock at least one row (enc-out.txt).
These are author-written facts that the player can read right after that scene, so they carry their own as-of id.

### 6.3 実況 (commentary) tables

33 tables for the 39 ids (one per navigator entry). Columns: ID, text, 顔 (face = speaker of the comment),
特殊, コマンド, 文字数 (position of the comment in the scene, ascending). 顔 is filled in 2,803 of 2,944 rows
(game-wide), values なつみ 564, 春花 710, 五島 750, 夏菜 142, 茅萱 112 … plus face variants (桃子2, 美冬2, なつみVR).
文字数 grows with the scene but runs 1.15-1.5 × the visible character count, so it cannot be mapped to a cell
without calibration. The commentary talks about the story from outside and is not fence-safe.
Side evidence: the 0000034C table's largest 文字数 is 6,885, the size of ONE of its three blocks (5,959 chars), not of
all three (18,182) — consistent with section 7.

**How to use it in the pipeline.** The `nav` table in tools/db already joins タイトル; add 閲覧年月日 and 解禁人物 and
print both on the packet's header line ("start 4/8 19:00; viewpoint 五島") as facts. The read-through brief can then
drop "infer the narrator" and "infer the time" for these 33 ids and only record switches inside a file. Load the
encyclopedia rows as a `lore(table, row, asof_id, text)` table with asof = the unlock scene, so pack.py can
include them fenced like CAST. The 顔 column is the speaker column for whoever translates the 実況 tables.

---

## 7. Variables — partly (no narrator variable; variants are chosen, some are dead)

- No variable names the narrator or the viewpoint (searched all 542 dumped .lsb for 主人公, 視点, and the
  global variable list in 変数初期化.lsb).
- The two variables that pick blocks inside a scene are set by the navigator (0000001C.lsb command 1155-1161):
  `途中から = 1` when the player picks a "直前から" (resume from just before the branch) button, else 0;
  `分岐ルートへ = 1` when the player picks the `新ルート` (new route) button.
- Jump targets are never computed: every Jump/Call/PCReset names a literal page and label (0 exceptions in 542
  files), and the 39 scene files are entered only at label 0 (from 0000001C, 000015E3 or 0000001E). So
  reachability below is exact.

Guarded blocks (reach-out.txt):

| id | block <- condition |
|---|---|
| 00000024 | 12, 16, 22 <- 分岐ルートへ = 0; 47, 51 <- 分岐ルートへ = 1 |
| 000001E1 | 33 <- 途中から = 0; 40 <- 途中から = 1; then 27 <- 分岐ルートへ = 0, 21 <- 分岐ルートへ = 1 |
| 000001E5 | 23 <- 途中から = 0; 41, 48 <- 途中から = 1; 29 <- 分岐ルートへ = 0, 35 <- 1 |
| 0000020B | 12, 18 <- 途中から = 0; 31 <- 途中から = 1; 38 <- 分岐ルートへ = 1, 25 otherwise |
| 000002F8 | 12 <- 途中から = 0; 30, 37 <- 途中から = 1; 24 <- 分岐ルートへ = 0, 18 <- 1 |
| 000004CF | 12 <- 途中から = 0; 31 <- 途中から = 1; 19 <- 分岐ルートへ = 0, 25 <- 1 |

So the paired blocks (e.g. 000001E1:21 / :27) are alternatives: one play shows one of them, never both in a row.

Unreachable blocks (no incoming reference anywhere):

| id | dead blocks | cells | note |
|---|---|---|---|
| 0000034C | **11, 23** | 336 + 263 | the "three near-identical routes": command 4 jumps unconditionally (Calc=1) to block 17. No variable selects them; only 17 (267 cells) is ever shown. Label ids: 11 = 00000353 (original), 17 = 0000242C, 23 = 000024C8 (created later) |
| 00000024 | 67 (and empty 41, 57, 63) | 67 | 67 is the near-duplicate of 16 |
| 000001DB | 21, 30 (and empty 26); 36, 41, 46, 51 | 73 + 75 + 4 | only 11 and 15 play; 36-51 are the 隠しテキスト (backlog-image) cells after an unreached label |

Total: 818 of 6,020 cells in the 39 ids are never shown in the game. SUMMARY cites 0000034C cells by block 11
(the dead one) and tells the drafter to translate all three variants; the live block is 17.

**How to use it in the pipeline.** Add `live` (0/1) and `guard` (the condition text) per block to the `files` /
`text_line` tables from reach.py. pack.py prints "block 11: never shown (dead variant)"; notes should cite the live
block (0000034C:17) and the read-through can skip dead blocks or read them only for comparison. Drafting dead text
costs budget with no player-visible effect; it can stay a low-priority copy of its live twin.

---

## 8. Anything else

| signal | finding | count |
|---|---|---|
| ruby = canonical readings | ruby pairs in the 39 ids: 98 (ruby39.tsv). Compared with GLOSSARY `reading`: 26 present, 26 agree, 0 differ; 70 not a GLOSSARY key, mostly common kanji, plus names/places 栄一郎 えいいちろう, 良治 りょうじ, 大二郎 だいじろう, 西佐波 にしさわ, 明徴 めいちょう, 熾天使 してんし | 26/26 agree |
| 人物名簿.tsv | 読み仮名 for every named character (e.g. 古郡なつみ こごおり なつみ, 五島絵梨奈 ごとう えりな) and a 色 column (Delphi $BBGGRR). Roster colour = text colour exactly for 5 people (五島 #FFFF00, 桃子 #00FF80, 美冬 #00FFFF, 良治 #00FF00, サクラ #FF0080), same hue for なつみ, 春花, 夏菜. #F55850 (SPEAKER-COLORS 6.4) is nearest to the roster colour of 幸太郎 (#E1524A, distance 22), which supports the note's doubt about the 伊勢 row | 5 exact, 3 close |
| name-entry variable `プレイヤー名` | 137 cells game-wide; in the 39 ids only in 0000001E and 000000F2 (8 cells), always the guide addressing the player (+様). Never a story character | 8 |
| F2 labels | 000000F2 is the guide/notice flow: all 9 blocks use イベント用; it is not story text and has no narrator | 9 blocks |
| hidden text | 000001DB:36-51 (隠しテキスト) are the 4 lns cells without csv rows noted in SPEAKER-COLORS.md; they sit after an unreached label | 4 |
| unlock chain | 実況___解禁テーブル.tsv lists entry -> next entry and the 分岐 rows; it restates the navigator order and marks where the new route branches (154, 160, 119, 140, 113) | — |

**How to use it in the pipeline.** A qa check (tools/qa_check.py or a new query.py command) that compares every
ruby pair with GLOSSARY and reports readings missing from GLOSSARY; 人物名簿 読み仮名 goes into CAST as the
canonical romanization source (fenced by the first scene that names the person). The name-entry slot needs no
story handling beyond the existing V001 rule.
