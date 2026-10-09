# SPEAKER-COLORS.md — the text colour names the speaker (COLOR, 2026-09-26)

BYTE ORDER: CONFIRMED (COLOR2, 2026-09-26). Delphi order 00BBGGRR is right; the hex column stands. Checked on
scene-1 screenshots work/mouse-shots/run1/100.png, 130.png, 140.png (00000024, EN build): 春花's quote and name tags
draw lavender blue (#AAAAFF); なつみ's quote and name tag draw pink (#FFAAFF). Swapped order would give 春花 #FFAAAA
(salmon); no salmon text appears. (Pink #FFAAFF reads the same both ways, so the 春花 cells decide it.)

Scope: parts 1-2, 27 ids: 0000001E 00000024 000000F2 000001DB 000001DD 000001DF 000001E1 000001E3 000001E5 000001E7
0000020B 0000020D 000002F6 000002F8 000002FA 0000033D 0000034C 00000366 0000037D 000003A8 000003AE 000003B4 000003BC
00000460 00000473 00000488 000004A7. Source: lns/ only (no lns-en/, no pass-1 notes).

Short answer: yes. In the game every named character's speech is drawn in that character's own colour, and every
mention of that character (name, kin word, pronoun) is drawn in the same colour, in narration and inside other
people's speech. Narration is uncoloured. Minor and unnamed speakers are uncoloured. The read chunks strip the tags,
so no note-taking agent has seen this until now.

## 1. Method

Tool: `tools/style_colors.py` (stdlib; run `uv run --no-project --python 3.12 python tools/style_colors.py [ids]`).

- `[ids]` lists `id | file | cell | style ids used | colour | first 20 chars` for every text cell.
  `cell` = block:line, the same key read/chunkNN.txt and all notes use.
- `--table` counts cells per (style id, colour) per lns file. `--names` lists the coloured runs inside non-quote
  cells (the name tags). `--check` compares the cell split with csv/<id>.csv.
- `from style_colors import cell_colours` returns `{'16:0': '#AAAAFF', ...}` for one id.

Facts about the format the tool relies on:
1. Colour = `unk2` of the `TDecorate` entry in the `; Font styles:` header. It is a Delphi TColor (bytes 00BBGGRR),
   printed as #RRGGBB. 4294967295 = no colour ("default"). Only unk2 matters here; unk4 is 0 or 16-80 and looks like
   a font size (big shouted lines).
2. Style ids are per lns file (ID 1 is pink in one file and blue in the next). Only the colour carries across files.
3. Text outside any `<STYLE>` tag is style 0: pylm never prints `<STYLE ID="0">`. Style 0 has a colour in 41 of 153
   files (in 000001E3-000002A0 it is 春花's colour and narration is wrapped in an uncoloured style 1). Reading
   untagged text as "no colour" is wrong.
4. A cell ends at every `{command}` (PAUSE, WAIT, ...), `<PG>`, `<EVENT>` and `<VAR>`. With this rule the cell
   list equals csv/<id>.csv (same count, same text) for every lns block that has csv rows, whole game. lns blocks
   with text but no csv row (so not in the chunks): 000001DB lines 36/41/46/51 (one cell each) and 3 navigator/help
   blocks. csv cells with no lns file: 5 (navigator/help).
5. The colour of a cell = the colour of its opening 「/『 (or its closing 」/』 for a continuation cell). A coloured
   name inside the quote (someone being addressed or mentioned) does not count. Cells without brackets: the colour
   that covers most characters.

Test: (a) name tags: for every colour, list every coloured word in narration and in speech, per file; one colour
must point at one person. (b) speakers: every quote cell directly followed by narration that starts with a coloured
name + は/が/も and a speech or reaction verb (59 cells), and every quote cell followed by narration starting with
私は/私が/私も (30 cells; the narrator); compare the quote's colour with the name's colour / the narrator.
Scratch: notes/v2/_tmp/color-analyze.py, color-evid.txt (the 89 rows), color-ids.txt.

## 2. Colour -> speaker

"as of" = the first cell where a name tag in that colour fixes who it is. Words = what the tags in that colour say.

| colour | looks | speaker | tag words seen | as of | cells opening a quote (27 ids) |
|---|---|---|---|---|---|
| #FFAAFF | pink | なつみ | なつみ, 古郡なつみ, 古郡先輩, 先輩 (in 五島's narration), お前/あなた (addressed) | 00000024:47:2 | 270 |
| #AAAAFF | lavender blue | 春花 | 春花, 新村春花, 新村先輩, 先輩 (in 五島's narration), 親友 | 00000024:47:1 | 419 |
| #FFFF00 | yellow | 五島 | 五島, 絵梨奈, 五島絵梨奈, お前/あんた/君 (addressed) | 000001DB:21:36 (speaks from 000001E3:8:12) | 378 |
| #FFD5AA | peach | なつみ's mother | お母さん (なつみ narrating), 古郡先輩のお母さん, 茜 (0000034C) | 000001DB:15:80 | 40 |
| #00FFFF | cyan | 春花's mother | お母さん (春花 narrating), おばさん, 春花のお母さん, 新村先輩のお母さん | 00000024:47:11 | 18 |
| #00FF00 | green | なつみ's father | お父さん (なつみ narrating), なつみのお父さん, 先輩のお父さん, 良治 (0000034C) | 000001DB:15:91 | 0 (bracketless text only) |
| #B6ED72 | light green | 春花's father | お父さん (春花 narrating, 00000024 block 47 only) | 00000024:47:17 | 0 |
| #00FF80 | spring green | 桃子 | お姉ちゃん (五島 narrating), 桃子 | 000002F8:12:2 | 23 |
| #FF2D2D | red | 伊勢 | 伊勢さん, 伊勢警部補, 警部補, 警部補殿 | 000003B4:8:14 | 35 |
| #F55850 | red (older value) | 伊勢 | 伊勢さん, once, 00000024:51:11 only; later files use #FF2D2D (section 7: from 0000095B this colour is 幸太郎) | 00000024:51:11 | 0 |
| default | uncoloured | narration, and every minor or unnamed speaker | — | — | 78 |

Not speaker colours:
- #FF0000 bright red: emphasis on shock cells (000001E3:12:0, 20:0; 000001E7:15:0; 0000020D:11:56; 000002FA:15:0,
  23:0) and the moans at 000001E1:33:9, 33:33. Treat as emphasis; attribute from the text.
- #FFFFFF white: emphasis on a quoted phrase inside narration (「一緒にいて」 in 000002F8, 「仕方ないなあ」 in
  0000020D). Not a person.
- #D0DA61: one quote cell, 00000024:51:42. No name tag in that colour in the 27 ids. Unmapped here; mapped in
  section 7 (春花の父, same person as #B6ED72).
- 00000488 block 48 (the voice flood): colour changes mid-word (48:2 「桜の警|告」, 「四|月」) across 10 colours
  incl. #0000FF and #C0C0C0. Decorative. Do not attribute fragments by colour there.
- default is shared: uncoloured speakers in one file can be several people (0000037D: 五島's mother and the old
  detective; 000003B4: the gossiping officers; 000003AE: examiner and patient). 五島's parents, TV voices,
  waitresses, police staff, the reporter, the phone recording are all uncoloured.

Outside the 27 ids the same palette recurs (no new speaker colour); the table above is only verified for parts 1-2.

## 3. Test results

| check | result |
|---|---|
| cells: lns split vs csv | identical, whole game: 6,253 of 6,258 csv cells get a colour; the other 5 are navigator/help cells with no lns file |
| name tags: one colour -> one person, within a file | 0 exceptions in the 27 files |
| name tags: one colour -> one person, across files | yes for all 9 character colours; 伊勢 has two values (#F55850 in 00000024, #FF2D2D from 000003B4) |
| narration has its own colour? | no. 2,372 of 2,423 non-quote cells are uncoloured; the 51 coloured ones are bracketless speech, text messages, letters, the two doll names at 0000037D:11:57-58, and the red/white emphasis above |
| narrator's own quoted speech | in the narrator's character colour (なつみ pink, 五島 yellow), so the colour of "my" lines shows a narrator switch |
| quote cells (incl. continuation cells) | 1,628 |
| quote cells in a character colour (speaker fixed by colour) | 1,539 of 1,628 (94.5%) |
| quote cells uncoloured / #FF0000 / unmapped | 86 / 2 / 1 |
| speaker check, name after the line (59 cells) | 51 same colour; 8 differ, and in all 8 the named person is reacting (nods, grins, is described), not speaking; the colour matches the line's real speaker |
| speaker check, 私 after the line (30 cells) | 27 in the narrator's colour; 3 where the narration says the narrator listened or waited (000001E3:8:71, 000002FA:11:5, 000004A7:11:30); colour gives the other speaker |
| contradictions | 0 of 89 |

## 4. NOTES-DIFF-c01-03.md rows about who says a line, in these 27 ids

31 table rows checked. Colour settles 20 (names the speaker of the cited cell). 11 not settled: the cited lines
are uncoloured (minor speakers) or the voice flood. No colour result contradicts a verdict in the diff; five
open items become attributed.

| diff row(s) | cell(s) | colour says | settled |
|---|---|---|---|
| SUMMARY 00000024:51:9 (P1), Q033 | 00000024:51:9-13 | 51:9 なつみ, 51:10 春花, 51:11 なつみ, 51:12 春花, 51:13 なつみ | yes (2 rows) |
| SUMMARY 000001E3:8:154 (P2), V022 | 000001E3:8:154-155 「…………？／あれ……？」 | #FFAAFF なつみ | yes (2 rows); no longer "unattributed" |
| SUMMARY 000001E5:41:0 (P1) | 000001E5:41:0 「ダメ！」 | #FFAAFF なつみ from the first cell (41:2 also なつみ) | yes |
| SUMMARY 000003B4:8:0 (P1) | 000003B4:8:0-13 briefing | #FF2D2D 伊勢 from 8:0, not only from 8:14 | yes |
| SUMMARY 000003BC:8:6 (P1) | 000003BC:8:4-7 | all #FF2D2D: one speaker, 伊勢; the other officer's lines (8:0, 3, 8, 11-12, 15-16, 19) are uncoloured | yes |
| V032 (collision table), V032 (P2-only list), C3 | 000002F6:11:78 「五島様……すみませんでした。」 | #AAAAFF 春花 | yes (3 rows) |
| R24 (and C3's first cell) | 0000034C:11:30 「あの……すみません、お邪魔します」 | #AAAAFF 春花 | yes |
| C8 | 00000024:16:13 「んん……」 | #AAAAFF 春花 (16:11 is なつみ) | yes |
| C9 | 000001DD:11:73 「あ痛！」 | #00FFFF 春花's mother (same colour as おばさん / 春花のお母さん tags in that file) | yes |
| R10, R19 | 0000037D:11:5 「おかあさーん！…」 | #00FF80 桃子 | yes (2 rows) |
| R8 | 000003B4:8:26 「君は年上好きなのか？」 | #FF2D2D 伊勢 | yes |
| R3, Q059 | 000004A7:11:64, 68, 94, 96-97 | #FF2D2D 伊勢 (11:65, 67, 95 are 五島) | yes (2 rows) |
| C4, R1 | 000002FA:27:8, 27:11 (text messages) | #FFFF00 五島 (27:7, 27:9 are 春花) | yes (2 rows) |
| R20 | 0000037D:11:74 「桃子……もうやめなさいよ」 | uncoloured (五島's mother has no colour) | no |
| C6, R6 | 0000037D:11:41-67 old detective | uncoloured, shared with 五島's mother in the same file | no (2 rows) |
| C7, C12, R9, R21 | 000003AE block 8 (examiner / patient) | every cell uncoloured | no (4 rows) |
| SUMMARY 000003A8:8:5 (P1), R13 | 000003A8 block 8 (reporter / students) | every cell uncoloured | no (2 rows) |
| SUMMARY 000003B4:8:15 (P1) | 000003B4:8:15-25 gossip | uncoloured | no |
| Q050 | 00000488:48 voice flood | colours change mid-word; decorative | no (supports leaving it unattributed) |

Colour evidence on a naming row (not a speaker row, not counted above): C11 / V042 / SUMMARY 0000037D:11:58. The
doll names are coloured: 0000037D:11:57 新村春花 in #AAAAFF (春花), 11:58 新村美冬 in #00FFFF, the colour of 春花's
mother's tags since 00000024:47:11. The player sees that link at 11:58. Whether that counts as "identified in this
file" is a translation decision for Fable; the colour fact is not in either pass.

Rows outside the 27 ids (R4, R7, C13, C17, V066, V072: files 000004BB, 00000522, 00000538, 00000550) were not
checked. Command: `uv run --no-project --python 3.12 python tools/style_colors.py 00000538 00000550 | grep -E "11:(16|25|130) "`.

## 5. For the read-through brief (and the drafter)

Paragraph for READTHROUGH-BRIEF (pass 3 or later):

> Each chunk line is `cell<TAB>colour<TAB>text`. The colour is the text colour the player sees. The game draws
> every named character's speech in that character's colour and draws every mention of the character (name, kin
> word, お前/あんた) in the same colour; narration and minor speakers are uncoloured (empty column). Learn the
> colours as you read: the first name tag in a colour tells you whose it is. Use it to attribute untagged lines
> and record the attribution as fact, citing the colour (e.g. "000001E3:8:154, colour of なつみ"). A line with an
> empty colour column is narration or a minor speaker; attribute those from the text as before. Ignore colour for
> #FF0000 (shock emphasis), #FFFFFF (emphasis on a phrase), and inside 00000488 block 48 (decorative). Within a
> quote, a coloured name belongs to the person named, not the speaker; the column already shows the speaker's
> colour. Do not open notes/v2/SPEAKER-COLORS.md before your chunk's files: its table names colours as of later
> files.

Exact change to `tools/build_chunks.py` (built the chunks: `grep -rl "chunk" tools/*.py tools/*.sh` finds it and
tools/tl_slice.sh). Not applied, and the chunk files are not rebuilt. Rerunning it rewrites read/chunkNN.txt and
notes/_db/_file-order.tsv (same file order and chunk split; only the new column differs).

```diff
 import io,csv,os
+import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
+from style_colors import cell_colours
 TARGET=45000  # JP chars per chunk
@@
         out.append(f'### FILE {f}.lsb  (order {n}, {l} lines, {c} chars)')
+        cc=cell_colours(f)
         rd=csv.reader(io.open(f'csv/{f}.csv',encoding='utf-8-sig')); next(rd)
         for r in rd:
             idx=r[0].split(':')[-2]+':'+r[0].split(':')[-1]
             t=r[3].replace('\r','').replace('\n','⏎')
-            out.append(f'{idx}\t{t}')
+            k=cc.get(idx,'default')
+            out.append(f'{idx}\t{"" if k=="default" else k}\t{t}')
```

Colour and speaker for later work:
- The EN patch shows the same colours only if each quote keeps its speaker's STYLE wrapper and each name tag's
  STYLE run moves onto the English name. A lost or misplaced wrapper silently changes who seems to speak.
- `style_colors.py <id>` gives the colour of any cell a note cites; use it before calling a line "unattributed".

## 6. Seven more colours, whole game (COLOR3, 2026-09-26)

Scope: every lns id. Source: lns/ only. Same evidence rules as section 1: (a) name tags in the colour (a coloured
name / kin word / pronoun in narration or in someone else's speech), (b) the narration cell right after a quote
names the speaker, (c) self-identification inside the quote. Cell = `id:block:cell`. Scratch scripts in
notes/v2/_tmp/: color3-analyze.py (tag words per colour, output color3-evid.txt), color3-ctx.py (`id block from to`,
prints cells with coloured runs marked), color3-check.py (the check in 6.2), color3-differ.py.

### 6.1 Result

| colour | speaker | cells | first cell (game order) | as of (first fixing tag) | evidence lines below | contradictions |
|---|---|---|---|---|---|---|
| #FCFEAB | 夏菜 | 2,345 | 00000656:11:172 | 00000697:8:77 | 8 | 0 |
| #68B4FF | 茅萱 | 1,860 | 00000697:8:61 (tag お姉ちゃん already at 00000656:11:172) | 00000944:8:21 | 9 | 0 |
| #FF0080 | サクラ | 1,073 | 00000A7C:11:4 (tag お母さん at 00000697:8:81) | 00000A62:11:70 | 9 | 0 |
| #AE74CD | エリカ | 1,020 | 00000779:8:31 (tag ばあちゃん at 00000697:8:72) | 00000697:8:72 | 12 | 0 |
| #B074CD | エリカ (variant value) | 9 | 00000A7C:11:72 | 000008D0:46:84 | all 9 cells | 0 |
| #B33EAF | エリカ (stray bracket colour) | 1 | 00000779:8:39 | 00000779:8:39 | the 1 cell | 0 |
| #808080 | 女神様 | 46 (00002444 block 32 only) | 00002444:32:74 | 00002444:26:502 | 8 | 0 |

Names: 夏菜, 茅萱, サクラ, エリカ are written in the text in that colour (see tags). 女神様 is how the text refers to
the gray voice; the voice says it does not know its own name (00002444:32:168-173).

### 6.2 Check (b), whole game

Every quote cell in one of the seven colours that is followed by narration opening with a coloured name + は/が/も:

| colour | name in the same colour | name in another colour | of those, the named person is speaking |
|---|---|---|---|
| #FCFEAB | 106 | 21 | 0 |
| #68B4FF | 58 | 20 | 0 |
| #FF0080 | 20 | 4 | 0 |
| #AE74CD | 48 | 10 | 0 |
| #808080 | 1 | 0 | - |
| #B074CD / #B33EAF | 0 | 0 | - |

All 55 "another colour" rows were read (color3-differ.py): the named person reacts, is described, or is thought
about (e.g. 0000095B:35:104 「…五島ちゃんは私のものって決まってるの！」 -> 五島はそのままずるずると…連行されていった).
One of them supports the table: 00000AAC:11:37 (#AE74CD quote) -> エリカちゃんはそう言って、居間を出た (name in #B074CD).

### 6.3 Evidence lines

**#FCFEAB = 夏菜**
1. 00000697:8:77 茅萱's quote 「ん……夏菜が残念がってたからね…」, 夏菜 in #FCFEAB; 8:78 春花 「あーあいつか」, あいつ in #FCFEAB.
2. 0000095B:35:39 self-identification 「なつみちゃん初めまして！　新村幸太郎の次女、新村夏菜でーす！」 (#FCFEAB); 35:40 -> 夏菜という子は馴れ馴れしく挨拶をしてきた。 (夏菜 in #FCFEAB).
3. 0000095B:35:44 -> 夏菜ちゃんは歳不相応な質問でまくし立ててくる。
4. 00000972:11:132 -> 夏菜ちゃんがなぜか偉そうに胸を張っている。
5. 00000989:11:43 -> 夏菜ちゃんも五島のモノマネにチャレンジしているようだ。
6. 00000989:11:113 -> 夏菜ちゃんは観客に徹するようだ。
7. 00000A7C:11:66-71 narration and 春花's quotes tag 夏菜 in #FCFEAB; 11:70 「んまま？」 is #FCFEAB.
8. 00000F0D:8:130-133 「私は……古村秋菜っていいます」 (#FCFEAB), then narration 新村夏菜だから古村秋菜ってちょっと安易だったかな: the narrator's own alias; the 秋菜 tags in this file are the same person.

Not tags (collector artifacts): 大翔 at 00001325:8:160 and ほ、 at 8:182-184 are words inside 夏菜's own continuation
cells (she reads a text aloud). 00000656:11:172 is the first cell; the name is not said in that file; the speaker
addresses お姉ちゃん, which is #68B4FF there.

**#68B4FF = 茅萱**
1. 00000944:8:21 春花 「あれ？　チガ姉？」 (チガ姉 #68B4FF); 8:22 春花がその女性に話しかけた (その女性 #68B4FF); 8:23 reply is #68B4FF.
2. 00000944:8:24 -> 8:25 チガ姉と呼ばれた女性は儚げな笑顔を向けた。
3. 00000944:8:36 -> 8:37 チガ姉と呼ばれた女性は袋に入れられた山菜を広げる。
4. 00000944:8:41 self-identification 「ん……初めまして。春花の従姉の新村茅萱と申します。」
5. 00000944:8:48 -> 茅萱さんはそう言うと、五島の寝顔に顔を近づけた。
6. 00000944:8:56 -> 茅萱さんは五島に近づき、あごをなでる。
7. 00000944:8:68 -> 茅萱さんが五島の手を握る。
8. 0000095B:11:8 -> チガ姉が声をかけると、五島は…
9. 0000095B:11:124 -> チガ姉の声が聞こえると、五島は素早く身を隠す。

00000697:8:61-81 (the first quotes) is a phone call to 春花 in the same colour with the same 「ん……」 opener.

**#FF0080 = サクラ**
1. 00000A62:11:69-70 春花 「幸太郎さんの奥さん――サクラさんって言うんだけどさ。」 (サクラさん #FF0080).
2. 00000A7C:11:16 -> サクラさん、体調でも崩していたのかな……。
3. 00000A7C:11:52 -> サクラさんも居間にやってきて、夏菜をは優しい目で見つめている。
4. 00000A7C:11:56 -> サクラさんにこうやって褒められるだけで…
5. 00000A7C:11:104 -> サクラさんの顔は蒼白、…
6. 00000E7B:28:154 -> サクラさんはゆっくりと身体を起こした。
7. 00000E7B:28:165 -> サクラさんは眉間にしわを残しつつもニコリとほほ笑む。
8. 00000E7B:54:111 -> サクラさんはちょっと得意げに話してみせる。
9. 00001EFF:8:22-23 「茅萱、ごめんね。お母さん、…」 (#FF0080) -> 茅萱 「お母さん……！」 (お母さん #FF0080).

Other tags in the colour, same person: ママ / お母さん (夏菜, 茅萱), 夏菜ちゃんのお母さん (00000AF7:11:96), 新村サクラ,
わが母 and ブルーシャ (00000F24:106:104-109; narration there: このミイラはサクラさんだ), 大魔女様 (00000E7B:88:120).

**#AE74CD = エリカ**
1. 00000697:8:72-73 春花 「なあ……ばあちゃん、怒ってないか？」, 茅萱 「…おばあちゃんはちゃんと分かってくれてるみたいよ」 (both tags #AE74CD).
2. 00000779:8:43 美冬 「お久しぶりです。大魔女様」 (大魔女 #AE74CD), to the voice of 8:31 and 8:39.
3. 00000779:8:77 -> 大魔女が叫び、メイスでテーブルを殴ると、…
4. 00000779:8:80 -> 大魔女は五島絵梨奈の頭をそっと撫でる。 (8:73 in the same voice: 「…そして孫の春花。」)
5. 0000095B:11:84-85 self-identification 「…春花の祖母の、新村エリカ！　こちらこそ、よろしくな！」
6. 00000989:11:39 -> おばあさんが五島に向かってニカッと笑った。 (五島エリカ in 11:38-45 is her own play-acting)
7. 00000989:11:119 -> おばあさんがテーブルに何かを叩きつけた。
8. 000009A0:11:96 -> おばあさんは引いた紙人形をテーブルの真ん中に置いた。
9. 000009B7:19:114 -> おばあさんはたいそう気に入ったようだ。
10. 00001295:8:174 -> おばあさんはポンと私の肩に手を置いた。
11. 00002026:8:0-1 「失礼致します」 (#AE74CD) -> 「ああ、エリカさん。…」 (エリカさん #AE74CD).
12. 00000AAC:11:37 -> エリカちゃんはそう言って、居間を出た。

Same lines, same colour: 000009A0:11:163-164 and 000021CF:8:356-359 (「財布……落としちゃって……帰れなくて……電車代を……」).

**#B074CD = エリカ** (all 9 cells)
1. 00000A7C:11:72 「ただいま」 -> 11:73 春花 「おかえりおばあちゃん！」 (おばあちゃん #B074CD).
2. 00000A7C:11:74 「お、春花、夏菜の子守なんて偉いね」.
3. 00000A7C:11:77-78 「お母さんが？　そうかい」; 11:81 美冬 「…おばあちゃんを迎えようって思ってね」 (おばあちゃん #B074CD).
4. 00000A7C:11:82 「美冬さん、私に話があるって？」 (answering 11:81).
5. 00000D59:11:65, 67, 68 continue the #AE74CD speech of 11:60-63 with no change of speaker (11:66 opens in #B074CD too).
6. 00000E49:11:80 answers 春花's 11:77 「ばあちゃん、…」 (ばあちゃん #AE74CD); 11:75 narration ばあちゃん in #B074CD; 11:78 is one quote cell mixing #AE74CD and #B074CD runs.

Tags: 000008D0:46:84 美冬 「…お義母さんから聞いたことがある」 (お義母さん #B074CD); 00000A62:19:90 エリカちゃん; 00000AAC:11:38.
Like 伊勢's #F55850/#FF2D2D: a second value for one person.

**#B33EAF = エリカ** (the 1 cell)
00000779:8:39 = `[#B33EAF 「][#00FFFF 美冬さん][#AE74CD ……ずいぶん待ったわ……」]`: only the opening bracket has this colour; the body
and closing bracket are #AE74CD, the voice of 8:31 「待ってましたよ、美冬さん……」 (#AE74CD), addressed at 8:43 as 大魔女様 (#AE74CD).

**#808080 = 女神様** (46 cells, 00002444 block 32)
1. 00002444:32:72, 75, 77, 83 春花 「お前が……」「お前、人だろ……？」「お前……誰なんだ……？」 (お前 #808080), each answered by a #808080 cell (32:74, 76, 84).
2. 32:108 「あの子の……代わり……」; 32:115 私はその子の前にしゃがんだ。 (その子 #808080).
3. 32:127 「ママに会いたいよお……」 -> 32:128 この子は思っていた以上に幼いようだ。 (この子 #808080).
4. 32:168-170 春花 「お前の……君の名前は……？」 -> 「分からない……」; 32:173 「教えてくれないの」 (no given name).
5. 32:202 その子の身体がピクリと動く。 -> 32:204 「本当にママを探してくれるの？」.
6. 32:238 そいつは…亀裂をすっと指さす。 -> 32:239 「その穴から外に出られる」.
7. 32:241 そいつはさらりとうなずく。; 32:292 私はその時、初めてそいつの顔を見たのだ。
8. Name: 26:502-503 女神様 in #808080 (inside a #D0DA61 quote); 32:248 and 32:255 女神様 in #808080 in the same block (「…女神様はお疲れなんだ。なつみちゃんを連れて出ていってくれ」); 00002473:11:304, 306 新しい女神様 in #808080.

Why a person and not an emphasis or "voice" style: in the whole game the colour covers one voice's quotes and every
word that refers to that voice (お前, この子, その子, そいつ, 女神様), and nothing else. That is the person-colour pattern of
section 1.

### 6.4 Seen while doing this, NOT changed (for Fable)

- #F55850 (row: 伊勢, "older value") has 1,097 quote cells in the whole game, from 0000095B on. Outside parts 1-2
  its tags name 幸太郎: 00000A62:11:69 「幸太郎さんの奥さん――」 (幸太郎さん #F55850); 00000E7B:88:122 「…よくも幸太郎を……！」
  (#F55850); 00000B87:19:5 -> 幸太郎さんがそんな指導を。 (#F55850); 茅萱's お父さん (00000BED:11:154) in #F55850.
  So `--speakers` prints 伊勢 for those cells. The row needs a file range or a second look; not checked by the
  full evidence rules here. Done in section 7 (file range: 伊勢 00000024, 幸太郎 from 0000095B).
- #D0DA61 (row: unmapped) has 619 quote cells in the whole game. Tags seen in it: 栄一郎 (00002444:26:496), 叔父さん
  (00001385:8:8), お父さん (春花 narrating, 00002444:32:65). Not checked by the full evidence rules. Done in section 7
  (春花の父).

## 7. #F55850 file range and #D0DA61 (COLOR4, 2026-09-26)

Scope: every lns id. Source: lns/ only. Same evidence rules as sections 1 and 6 ((a) name tags, (b) the narration
cell after a quote names the speaker, (c) self-identification). Scratch in notes/v2/_tmp/: color4-analyze.py
(per colour: quote cells per file, every tag run, check (b); output color4-evid.txt), color4-ise.py (colour of every
伊勢/警部補 run), color4-kin.py (kin-word tags by the colour of the cell that says them), color4-before.tsv /
color4-after.tsv (`--speakers` output before and after this change).

### 7.1 Result

| colour | speaker | files | quote cells | as_of_from | as_of_to | evidence lines | contradictions |
|---|---|---|---|---|---|---|---|
| #F55850 | 伊勢 | 00000024 only | 0 | 00000024:51:11 | 00000024 | 1 (below the rule of 5; the only run of this colour before 0000095B) | 0 |
| #F55850 | 幸太郎 | 0000095B .. 00002478 (120 files) | 1,097 | 0000095B:35:14 | open | 10 below | 0 |
| #D0DA61 | 春花の父 | 00000024 .. 00002473 | 619 | 00000682:11:9 | open | 10 below | 0 |

No #F55850 run exists in any file from 00000025 to 0000095A, so no cell falls between the two rows. The 伊勢 row
labels 0 cells: the one run is a tag inside なつみ's quote (00000024:51:11, outer colour #FFAAFF). It stays so the
table records what the tag says.

Why two owners and not a mistake: 伊勢 is drawn in #FF2D2D in 40 files (000003B4 .. 00002450), including files
where #F55850 is in use (00000F0D: 280 伊勢 runs in #FF2D2D, 2 uncoloured, next to パパ tags in #F55850). No 伊勢 or
警部補 run after 00000024 is #F55850.

Why #D0DA61 is 春花の父 (the #B6ED72 person) and not a new label: 00000682:11:9-12, 春花 narrating (her quotes 11:0,
11:7 are #AAAAFF; 私となつみ), tags the same father 私のお父さん in #D0DA61 (11:9, 11:10) and お父さん in #B6ED72 (11:11,
11:12) in consecutive sentences. #B6ED72 is also used in 000007D3, 000007EA, 00000801, 00000818, 0000082F, 000010DD
next to #D0DA61. Label kept descriptive, as for #B6ED72; the tags give the given name 栄一郎 from 00000779:8:57.

### 7.2 Evidence lines

**#F55850 = 伊勢 (00000024)**
1. 00000024:51:11 なつみ 「だったら家宅捜索のときに伊勢さんが持っていってるはずだよね？」 (伊勢さん #F55850).

**#F55850 = 幸太郎 (from 0000095B)**
1. 0000095B:35:14 春花 「幸太郎伯父さん、何してんだ？」 (幸太郎, 伯父さん #F55850); the reply 35:15-16 is #F55850.
2. 0000095B:35:21 self-identification 「俺は新村幸太郎って言って、栄一郎の双子の兄だ。」 (#F55850; 栄一郎 #D0DA61).
3. 0000095B:35:29 なつみ 「…幸太郎さんが……？」 -> 35:30 「え？　女の子……？」 (#F55850) -> 35:31 急に幸太郎さんの顔から笑顔が消えた。
4. 0000095B:35:35 「おい、夏菜……。いるんだろ？」 (#F55850) -> 35:37 夏菜 「さっすがパパ！…」 (パパ #F55850) -> 35:38
   小さな人影が幸太郎さんのことをパパと呼び (幸太郎さん #F55850).
5. 00000A7C:11:101 「おいサクラ、どうした！？…」 -> 幸太郎さんはサクラさんの背中をさすった。
6. 00000AC4:11:3 -> 幸太郎さんはあきれ顔でバリバリと頭をかく。
7. 00000AC4:11:7 -> 幸太郎さんは五島のメモを奪い取った。
8. 00000AC4:19:7 -> 幸太郎さんは特に動揺した様子も見せない。
9. 00000E01:11:163 「幸太郎！　早くお前も地下に行くんだ！」 (幸太郎, お前 #F55850).
10. 00000E7B:88:122 「…よくも幸太郎を……！」 (幸太郎 #F55850).

Check (b): 72 #F55850 quotes followed by narration opening with a coloured name + は/が/も: 45 name 幸太郎 (#F55850),
27 name someone else. All 27 read: the named person reacts, is described or addressed, or the next cell continues
the same quote without a bracket (e.g. 00000E7B:34:18). None has the other person speaking the line.
Tags (1,593 runs from 0000095B): 幸太郎さん 553, お父さん 239, パパ 220, 幸太郎 196, 兄貴 61, 幸太郎君 35. Who says the
kin words (color4-kin.py): パパ 149 in 夏菜's cells (#FCFEAB); お父さん 89 in 茅萱's (#68B4FF), 7 in サクラ's; 兄貴 41
in #D0DA61 cells and 1 in #B6ED72 (the younger twin). Contradictions: 0.

**#D0DA61 = 春花の父**
1. 00000682:11:9-12 私のお父さん (#D0DA61) and お父さん (#B6ED72), same person, 春花 narrating (see 7.1).
2. 00000779:8:57 「20年ほど前、美冬さんと栄一郎の婚姻式に…」 (栄一郎 #D0DA61; 美冬さん #00FFFF, 春花の母).
3. 000007A5:8:124 「栄一郎さん、とても優しい人だった。春花はいいところがお父さんに似たのね」 (栄一郎さん, お父さん #D0DA61).
4. 000008E8:8:292 春花のお父さん (#D0DA61); same tag 00000916:31:16, 0000095B:35:24, 00000C38:11:4.
5. 0000095B:35:21 幸太郎 「…栄一郎の双子の兄だ。」 -> 35:24 つまり、春花のお父さんのお兄さん…… (春花のお父さん #D0DA61).
6. 00000BB7:11:215 新村先輩のお父さん――新村栄一郎さん (both #D0DA61).
7. 000007D3:11:55 「あ痛！」 -> 栄一郎さんは何もない空間に足を引っ掛け転んでしまった。
8. 0000082F:11:27, 37, 83, 125 -> 栄一郎は… (four cells, e.g. 11:125 栄一郎はそう言って、ヒョコヒョコと御神木の方へ歩き出した。).
9. 0000142B:8:166, 204 -> 新村栄一郎がそこまで言うと… / 新村栄一郎は私をなだめ…
10. 00000024:51:42 「やあ春花、久しぶりだね」 (#D0DA61) -> 51:43-46 春花 「お|と|う|さ…」 (#AAAAFF).

Check (b): 29 quotes followed by a coloured name + は/が/も: 16 name this person (栄一郎(さん), 新村栄一郎, お父さん,
おじさん, 叔父さん in #D0DA61), 13 name someone else; all 13 read: mentions or quote continuations, none has the
other person speaking. Tags (844 runs): 栄一郎 185, 栄一郎さん 128, お父さん 95 (44 in 春花's cells, 5 in 春花の母's),
おじさん 78 (なつみ), 叔父さん 30 (15 in 茅萱's cells), 新村栄一郎 28, 春花のお父さん 24, 新村先輩のお父さん 15.
Contradictions: 0.

Seen, not changed: 0000095B:35:11 has a tag おじさん in #DAE17D (なつみ's quote). Not an outer colour anywhere, so it
never decides a speaker.

### 7.3 Tool change

`as_of_to` column added (empty = open-ended); `style_colors.load_speaker_table` reads columns by header name and
returns every row per colour; `style_colors.speaker_for(table, colour, fid)` picks the row whose file range
contains fid. The colour's earliest row is open towards the start of the game (the brief's strict
[as_of_from, as_of_to] would untag 28 quote cells that sit before their colour's first naming tag: 夏菜 15, 茅萱 12,
春花の父 1). `tools/db/build.py` resolves the range through `cell_speakers` and warns when two rows of one colour
overlap. README "Speaker by color" has the rule.

Coverage (quote cells with a speaker by colour, whole lns/): before 31,636 of 37,146 (1,097 of them read 伊勢,
wrongly); after 32,255 (+619 #D0DA61; the 1,097 #F55850 cells now read 幸太郎). Chunks: 31,636 -> 32,255 of 37,144.
No `--speakers` cell changed other than those 1,111 #F55850 cells (1,097 quote, 14 narration) and 624 #D0DA61
cells (619 quote, 5 narration).
