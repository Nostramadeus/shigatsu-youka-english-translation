# FIT MODEL 2: how the LiveMaker engine lays out text in this game

Written 2026-11-13 by lane F (model id claude-fable-5-2). Replaces the width model in the docstring of
`tools/fit_audit.py` (calibration of 2026-09-26). `notes/FIT-AUDIT.md`, which that docstring cites, does not exist and
was never committed; the docstring was the only record.

No game launch was made. Everything below rests on (a) script properties read with pylivemaker, (b) pixel measurements
by script on the four friend screenshots of 2026-11-13 and on the 1:1 captures of 2026-09-26 in
`tools/harness/shots/fitaudit*`, (c) Windows GDI font metrics read through ctypes. No image was viewed.

Scratch folder with every script and output: `work/feedback-20261113/fit/`.

## 0. Result in one table

| question | answer |
|---|---|
| Does the new model reproduce the observed line breaks? | Yes: 81 of 81 observed screen lines, at the box width written in the script, on 3 different font and flag sets (`fit/verify_all.out.txt`). |
| Does the old `EXTRA_EM = 0.15` model? | Only on the scene box: 1.png 8 of 8. 2.png 0 of 13. 3.png 1 of 15. 4.png 5 of 15 (`fit/old_model.out.txt`). |
| Failure 1, reference No.101 commentary cut at the bottom | The Japanese original is cut too: 18 lines of text, 12 fully visible. It is the only one of 315 commentary cells that overflows, in either language. Leave as the original. |
| Failure 2, name plate "Mifuyu Niimur" | Our defect. The plate is not too small. It is 205 px wide, starts at x 490, and the arc selector box at x 680 is drawn over its right end. 12 of 24 English names are cut at font 30. The Japanese never is (widest plate 183 px, room 190). |

## 1. The model

Terms: a "MesNew" is a LiveMaker message box object (wraps text, can page). A "Caption" is a one-string label object
(no wrapping). "GDI" is the Windows text API the engine draws with.

### 1.1 Glyph cell (both object types)

```
cell(ch) = max( GetCharWidth32W(ch),  origin.x + blackBoxX )
           both read on a memory DC with a LOGFONT of lfHeight = +FONTHEIGHT, lfFaceName = the face,
           lfCharSet = SHIFTJIS_CHARSET (128), lfWeight = 400 (700 when PR_FONTSTYLE has bit 1 = bold);
           origin.x and blackBoxX come from GetGlyphOutlineW(ch, GGO_GRAY8_BITMAP, identity matrix)
```

The second term matters for glyphs whose ink is wider than their advance. In ＭＳ Ｐ明朝 30 that is `f` (advance 8,
ink 11). In ＭＳ Ｐ明朝 24 it is `f` +3 and `R _ v w y` +1 each. Fixed-pitch ＭＳ 明朝 has none.

### 1.2 MesNew

```
K        = 1 + PR_FONTSHADOW + 2 * PR_FONTBORDER          (unset flag = 0)
advance  = cell(ch) + K                                    (every glyph, spaces included)
pitch    = FONTHEIGHT + PR_LINESPACE + PR_FONTSHADOW + 2 * PR_FONTBORDER      (unset linespace = 0)
glyph_h  = FONTHEIGHT + PR_FONTSHADOW + 2 * PR_FONTBORDER
font     = the TextIns style 0 face and size when its size is not 0, else PR_FONTNAME / PR_FONTHEIGHT of the MesNew
```

Wrap rule (greedy, left to right, x starts at 0 on every line):

1. A paragraph ends at CR LF (`\r\n`, `<BR>`).
2. Token = a run of characters that are neither ASCII space nor wide, plus every ASCII space that follows it.
   A wide character (code point >= U+2E80, which includes U+3000 the full-width space and U+FF0E "．") is a token by itself.
3. A token is placed on the current line only if `x + width(token) <= PR_WIDTH`, where width counts the token's
   trailing spaces too. In plain words: a word needs room for itself and for the space after it.
   The last word of a paragraph, or a word followed by a wide character, has no trailing space and only needs room for itself.
4. If it does not fit and the line is not empty: start a new line, then place it. The spaces that ended the previous
   line stay there, invisible. A full-width space is a normal glyph and is kept at the start of a line.
5. A token wider than PR_WIDTH on an empty line is cut glyph by glyph (assumed, no evidence).

Vertical capacity:

```
lines that fit fully in a height R  =  (R - glyph_h) // pitch + 1          (0 when R < glyph_h)
```

R is PR_HEIGHT for a paging box. For a box cut by its parent or by the screen, R is the visible room from the text top.

### 1.3 Caption

```
width = sum of cell(ch)          K = 0, no wrapping, the object sizes itself to its text
```

Bold is lfWeight 700 (GDI makes every glyph of ＭＳ Ｐ明朝 1 px wider). A Caption is cut only by what is around it:
the right edge of its parent box, the screen edge at x 960, or another object drawn over it.

### 1.4 Constants per verified surface

| surface | face, size | shadow / border | K | pitch | PR_WIDTH | W range that still reproduces every line |
|---|---|---|---|---|---|---|
| scene box (標準) | ＭＳ Ｐ明朝 30 | 1 / 1 | 4 | 37 | 580 | 578..581 |
| people body | ＭＳ Ｐ明朝 24 | 1 / 0 | 2 | 28 | 690 | 688..690 |
| node commentary | ＭＳ 明朝 25 | 0 / 0 | 1 | 27 | 750 | 742..754 |

### 1.5 Evidence and residuals

- Glyph positions at 1:1: `tools/harness/shots/fitaudit/004.png`, line "B04 dddd. B05 eeee. B06 ffff.": all 24 glyph
  starts within 2 px of the model with the max rule; with the plain advance the last glyph is 12 px off
  (`fit/glyphpos.py`). K = 4.000 measured on "mmmm. B14 nnnn. B15 oooo." (`fit/k_from_ink.py`).
- Line pitch at 1:1: `fitaudit/008.png` and `010.png`: 13 lines per page, tops exactly 37 px apart.
- The wrap rule: `fitaudit4/010.png`. "P3 ... fffff." (574 px) is followed by a full-width space and stays on one line.
  "Q3 ... fffff." (580 px + space 13 = 593) is followed by an ASCII space and wraps, although the word alone would fit 580.
  "Q2 ... ffff." (565 + 13 = 578) stays. Only a limit of 578..582 on word + space explains all three.
- People body, 27 lines of 3.png and 4.png: ink width residual sd 1.07 px with the max rule at scale 0.9442
  (the measured screenshot scale is 0.9443..0.9448). Plain advance: sd 1.94 px and needs an impossible scale 0.9492 (`fit/regress24.py`).
- Friend screenshots are scaled: the 960 x 540 game area is 907 x 511 px in all four (`fit/area.py`), factor about 0.944.
- Per-line table for all 81 lines (width, room left, where the next word would have reached): `fit/verify_all.out.txt`.
  Smallest margins: scene "the Niimura family had moved" + next word and space = 582 (W + 2);
  people body "stillborn. ... ever" = 679 (11 px room); commentary lines 5, 9, 12 = 756 with the next word (W + 6).

Answer to "which font and pitch is the commentary in 2.png": ＭＳ 明朝 25 px, set by the TextIns style of
0000001E idx 1562 (the MesNew at idx 1556 has no font of its own). Half-width glyph 13 + 1 = 14 px, full-width 26 + 1 = 27 px,
line pitch 25 + 2 = 27 px. Measured: character pitch 13.225 screenshot px = 14.00 game px; line pitch 25.5 = 27.0 game px.
All 13 visible lines reproduced. 52 characters fit a line (728 px + space 14 = 742), 53 do not (756).

## 2. Surfaces

Confidence words: VERIFIED = measured on a screenshot. DERIVED = from script properties plus the verified model.
ASSUMED = no evidence, stated rule.

### 2.1 Scene text box (標準) and its siblings

- Where: `メッセージボックス作成.lsb` idx 7 (base 600 x 500 at y 20) and idx 8 (MesNew, insets 10): 580 x 480.
- Font and flags: ＭＳ Ｐ明朝 30, linespace 4, border 1, shadow 1, FONTCHANGEABLED 0. K 4, pitch 37, glyph_h 33.
- Overflow: PAGE. The box waits for a click, clears and continues. 13 lines per page = (480 - 33) // 37 + 1.
- Evidence: 1:1 captures 004, 008, 010, 012 and fitaudit4/010; 1.png. VERIFIED.
- Siblings in the same file (same engine object, DERIVED): (編集用) idx 35: 470 x 84, size 16, linespace 6, shadow 1: K 2, pitch 23, 3 lines.
  大文字用 idx 60: 940 x 520, size 60, linespace 4, border 1, shadow 1: K 4, pitch 67, 7 lines. 電話 idx 87 and 赤 idx 168: as 標準.
  イベント用 idx 114: 590 x 80 (insets 20/15/20/5), size 20, linespace 4, shadow 1: K 2, pitch 25, 3 lines.
  リファレンス idx 141: 580 x 180, size 20, linespace 1, shadow 1: K 2, pitch 22, 8 lines. All PAGE.

### 2.2 Reference viewer, node commentary (failure 1)

- Where: 0000001E idx 1556 MesNew 部分コメント, text from idx 1559/1561 (`リファレンスターゲット` columns N概要 / N裏概要), TextIns idx 1562.
- Geometry: left = 100, width 750, PR_HEIGHT 540. Top = 200, or 60 + zoom picture height + 5 when the node's 特殊処理
  holds 拡大 (idx 1553-1565). The box runs past the screen bottom (y 540), so the room is 540 - top.
- Font and flags, English build: ＭＳ 明朝 25, linespace 2, border 0, shadow unset, FONTCHANGEABLED 0
  (`patch/props-0000001E.tsv` rows for idx 1556). K 1, pitch 27, glyph_h 25.
  Japanese original: border 1, FONTCHANGEABLED unset. K 3, pitch 29, glyph_h 27.
- Overflow: CLIP at the screen bottom. No page turn and no scroll: PR_IGNOREMOUSE 1, PR_HANDLEKEY 0, no event handler
  on the object, TextIns Wait 0; any click or key goes to the dim layer (idx 1547/1549) and closes the view (label 0000039D).
- Capacity, English: without picture room 340: 12 lines. Reference No.101 node 3 (picture 205 x 115, top 180, room 360): 13 lines,
  the 14th shows 9 of its 25 px. That is exactly 2.png.
- VERIFIED on 2.png (breaks, pitch, 13 lines + a cut 14th). Japanese constants DERIVED (border adds 2 to K by subtraction
  of the people body from the scene box).

### 2.3 Encyclopedia body texts

- Where: 00001878. People 人物解説テキスト idx 570 and 2052 (690 wide, ＭＳ Ｐ明朝 24, linespace 3, shadow 1: K 2, pitch 28).
  Place 場所詳細 idx 834 (870 wide, size 22, linespace 2, shadow 2: K 3 ASSUMED, pitch 26). Event 出来事テキスト idx 1406
  (size 22, linespace 3, shadow 1). Item 物テキスト idx 1670 (size 22, linespace 3, shadow 1).
- Composition of a people entry (idx 2174 / 2183 / 2191): `" " + U+3000 U+3000 + number + "．" + テキスト + CR LF + "(" + citation + ")" + CR LF CR LF`.
  The "[New!]" mark is a picture laid over the two full-width spaces, not text.
- Overflow: SCROLL. PR_HEIGHT is 20000 at creation; after the insert the height is set to caret Y + font height
  (idx 2216, 842, 1411, 1678); the parent テキストサブ矩形 (people 690 x 440) is the window; the idle handler at label 00001882
  (idx 25-33, attached at idx 612 / 2077 or by PR_ONIDLE) moves the text between top 5 and (window height - text height).
- Wrap VERIFIED on 3.png and 4.png (30 lines). Scroll DERIVED from the properties.
- One-line summaries 事件簡易説明 idx 1525 and 物簡易説明 idx 1629: MesNew 850 x 90, size 25, linespace 4, shadow 1: K 2, pitch 30, 3 lines. CLIP (no handler). DERIVED.

### 2.4 Encyclopedia People page name plate (failure 2)

- Where: 00001878 idx 512/514 BoxNew 人物テキスト土台 (height 60, border 1, no width), idx 516/518 Caption 人物テキスト
  (PR_LEFT 2, PR_TOP 22, ＭＳ Ｐ明朝 30, PR_FONTSTYLE 1 = bold, PR_HALIGN 1), idx 519 Caption 人物読み仮名 (size 15, empty in English).
  idx 520-523: box width = wider caption + 4. idx 554: the box slides to x 490; idx 555: y 2.
- What cuts it: idx 1866 BoxNew 編選択, the arc selector: x 680, y 2, 250 x 60, PRIORITY 4000, a top-level object drawn over the
  plate. On People page 3 it is hidden (idx 552-553) and the screen edge x 960 is the limit.
- Formula: text starts at 490 + 3 = 493. Visible if `493 + width <= 680` (pages 0-2), i.e. width <= 187 px; page 3: width <= 467 px.
- Evidence, VERIFIED: 4.png plate is 168 game px wide = 164 ("Ryoji Kogori" bold) + 4. 3.png: the selector's left border sits at
  game x 680.6 in both shots; "Mifuyu Niimura" is 204 px, its last letter cell is x 682..697; the letter before ends at the border.
- Overflow: CLIP (covered). No engine auto-fit flag exists for a Caption: it has no width property and no fit property.

### 2.5 Unlock notices

- Encyclopedia unlock: Caption 事典解禁テキスト, bold ＭＳ Ｐ明朝, PR_LEFT 110 in a 960 x 40 base: room 850 px, one line, CLIP at the screen edge.
  0000001E idx 2415 / 2515 (place, 詳細チャプター, size 30), 2420 / 2520 (event, 表示名, 30), 2425 / 2525 (item, 簡易説明, 22),
  2437 / 2531 (person, 表示名, 30); 000000F2 idx 1049, 000019DD idx 135, 00001FBE idx 123 (the end-of-scenario copies, size 22,
  text = the variable 終了時用事典解禁通知). DERIVED.
  Model run (`fit/notice_scan.py`): event, item and person cells all fit. 7 place titles are wider than 850 px at size 30:
  事典場所 keys 25 (1170 px), 65 (959), 82 (888), 38 (881), 22 (880), 10 (863), 32 (853). Not verified on a screenshot.
- Reference unlock: 00001FBE idx 240 / 241, bold size 20 in a 10000-wide base. The base position comes from an expression. NOT MODELLED.

### 2.6 Chatter

- Pages: 000018BF TextIns (`<VAR 表示テキスト><PG>`) into the イベント用 message box made at 0000189A idx 38 / 398 / 857 / 900:
  590 px, K 2, pitch 25, 3 lines per page. PAGE. DERIVED.
- List rows, headers, new-topic notice: Captions (0000189A idx 244, 246, 741, 1202; 000018BF idx 248, 279, 298), ＭＳ Ｐゴシック 20 or
  ＭＳ Ｐ明朝 20 bold or ＭＳ 明朝 20. One line each, CLIP. Width by rule 1.3. Their right limits are in lane B's
  `work/shorten-restore/laneB/allfit.tsv`, computed with the old widths; they must be recomputed. DERIVED.

### 2.7 Navigator synopsis and route summary

- Where: 0000001C idx 3779 (synopsis), 3773 / 3776 (route); 000019DD idx 362, 355 / 358. MesNew 876 x 500 at top 20 inside the
  500-high panel あらすじ土台: room 480. ＭＳ Ｐ明朝 22, linespace 2, no border, no shadow, FONTCHANGEABLED 0 (patch). K 1, pitch 24, glyph_h 22.
- Text: synopsis = 4 header lines + 2 empty lines + body (+ the New Route block); route = 1 header line + 2 empty lines + U+3000 + body
  (TextIns idx 3814 / 3815).
- Overflow: CLIP at the panel bottom. No handler, Wait 0. Capacity 20 full lines. The hidden-route buttons (idx 3788-3806, PR_TOP 447,
  shown only on some scenarios) cover line 18 and below: 17 lines are clear of them. DERIVED. Earlier notes said 18 lines; that used the old pitch 25.98.

### 2.8 Other MesNew fed from tables (all DERIVED)

| script idx | object | size | font, flags | K / pitch | capacity | overflow |
|---|---|---|---|---|---|---|
| 0000001E 528 | 概要ウィンドウ (reference summary) | 760 x 220 | ＭＳ Ｐ明朝 18, linespace unset | 1 / 18 | 12 lines | CLIP |
| 0000001E 4498 | ギミックテキスト | 428 x 90 | ＭＳ Ｐ明朝 20, linespace 2 | 1 / 22 | 4 lines | CLIP |
| 0000001E 3942, 4812 | reference help (イベント用 box) | 590 x 80 | see 2.1 | 2 / 25 | 3 per page | PAGE |
| 0000001C 1123 | チュートリアルウィンドウ | 600 x 250 | ＭＳ Ｐ明朝 22, linespace 2, border 0 | 1 / 24 | 10 lines | CLIP |
| 0000001C 3859 | チュートリアルテキスト | 660 x 20000 | ＭＳ Ｐ明朝 20, linespace 2, shadow 1 | 2 / 23 | none | SCROLL |

### 2.9 Scene-side commentary (実況): NOT MODELLED

00001F8A idx 626..686 step 4 and 689: 17 MesNew, 286 x 290, ＭＳ 明朝 20, linespace 2, PR_FONTCHANGEABLED UNSET.
Unset is the state that drew Latin text on a full-width advance on 0000001C idx 1123 before the fix of 2026-09-26
(`tools/lsb_prop.py` docstring). No screenshot of this panel exists. If the flag behaves like 0 here: K 1, 11 px per Latin letter,
pitch 22, 13 lines in 290 px. If it does not, every English line is about twice as wide. See Open questions.

## 3. CHECKER SPEC

Goal: one script that scans every table cell and literal label against its surface and prints what will page, clip or sit under another object.
The implementer writes no heuristic. Where this spec says NOT MODELLED, the checker prints that word and nothing else for the row.

### 3.1 Platform and reuse

- Windows only (GDI through ctypes, standard library; no window is opened). Run:
  `PYTHONUTF8=1 uv run --no-project --python 3.12 --with pylivemaker --with pillow python tools/fit_check.py`.
- Copy `work/feedback-20261113/fit/gdi.py` and `model.py` next to the checker and import them. They are the reference:
  `model.cell`, `model.width`, `model.K`, `model.pitch`, `model.tokens`, `model.wrap(text, font, k, W)` (default rule `space`).
- First step of every run: execute the logic of `fit/verify_all.py` and stop with exit 1 unless it prints
  `TOTAL observed lines 81, reproduced 81, different 0`. This catches a machine with a different ＭＳ 明朝 file.

### 3.2 Inputs

1. A surface registry file `tools/fit_surfaces.tsv`, one row per surface, columns:
   `id, kind, script, idx, face, size, bold, shadow, border, linespace, width, room, limit_x, start_x, table, column, key_filter, prefix, suffix, jp_shadow, jp_border, note`.
   `kind` is one of PAGE, CLIP, SCROLL, CAPTION, NOT_MODELLED. The starting rows are section 3.6. Every number in a row must be read from the script dump
   (`fit/inventory.py` prints them); a row whose width, room or limit is an expression the implementer cannot resolve to a number gets kind NOT_MODELLED.
2. English cells from `tsv-en/`, Japanese cells from `notes/_db/` (same row key, same column name before the first space).
3. Scene cells from `lns-en/` with the cell splitter of `tools/fit_audit.py` (`cells()`), surface = `scene`.

### 3.3 Text preparation

- A literal `\n` or `\r\n` in a cell is a paragraph end.
- `prefix` and `suffix` of the registry row are added around the cell before wrapping (example: people body prefix
  `" " + U+3000 + U+3000 + "<n>．"` with the highest entry number of that person, suffix = CR LF + the citation line).
- A cell that contains a `/.../` variable marker: replace `/立木/` by `you`; any other marker makes the row NOT MODELLED.
- Tags `<...>` and `{...}` lines are removed as `fit_audit.cells()` does.

### 3.4 Formulas

Exactly section 1. For a MesNew: `lines = len(model.wrap(text, font, K, width))`, `widest = max(model.width(line, font, K))`,
`capacity = (room - glyph_h) // pitch + 1`. For a CAPTION: `px = model.width(text, font, 0)` on the longest line of the text (split at CR LF),
`limit = limit_x - start_x`.

### 3.5 Verdicts and thresholds

| kind | verdict | rule |
|---|---|---|
| PAGE | OK | lines <= capacity |
| PAGE | PAGES | lines > capacity; print pages = ceil(lines / capacity). Not a loss of text: one extra click per page. |
| CLIP | CLIP | lines > capacity |
| CLIP | TIGHT | not CLIP, and wrapping again with width - 3 gives lines > capacity (3 px = the largest position error measured, 2 px, plus 1) |
| CLIP | OK | otherwise |
| SCROLL | OK | always; print lines for information |
| CAPTION | CLIP | px > limit |
| CAPTION | TIGHT | not CLIP and px > limit - 3 |
| CAPTION | OK | otherwise |
| NOT_MODELLED | NOT_MODELLED | always |

For every English CLIP the checker also runs the Japanese cell through the same surface with `jp_shadow`, `jp_border` and the Japanese face
(ＭＳ 明朝 where the English build uses ＭＳ Ｐ明朝; the node commentary is ＭＳ 明朝 in both) and adds
`class = AS_ORIGINAL` when the Japanese is CLIP too, else `class = ENGLISH_ONLY`.
Japanese line counts can be off by 1 line (the engine's rule for punctuation at a line start is not known); when Japanese lines == capacity or capacity + 1, print `class = JP_UNSURE`.

### 3.6 Registry rows that are ready

| id | kind | script idx | face size bold | shadow border linespace | width | room | table.column | prefix / suffix | jp flags |
|---|---|---|---|---|---|---|---|---|---|
| scene | PAGE | メッセージボックス作成 8 | ＭＳ Ｐ明朝 30 no | 1 1 4 | 580 | 480 | lns-en cells | none | 1 1 |
| event_box | PAGE | メッセージボックス作成 114 | ＭＳ Ｐ明朝 20 no | 1 0 4 | 590 | 80 | リファレンスヘルプ.テキストN, 雑談リスト page cells | none | 1 0 |
| node_comment | CLIP | 0000001E 1556 | ＭＳ 明朝 25 no | 0 0 2 | 750 | 340, or 475 - picture height when N特殊処理 holds 拡大 | リファレンスターゲット.N概要, N裏概要 | none | 0 1 |
| synopsis | CLIP | 0000001C 3779, 000019DD 362 | ＭＳ Ｐ明朝 22 no | 0 0 2 | 876 | 480 (also report lines > 17 as UNDER_BUTTONS) | あらすじ.内容 (+ 新ルート) | 6 lines before the body; New Route block as in `work/shorten-restore/fit.py` | 0 0 |
| route | CLIP | 0000001C 3773/3776, 000019DD 355/358 | ＭＳ Ｐ明朝 22 no | 0 0 2 | 876 | 480 | ルート概要.あらすじ | 3 lines before the body, body starts with U+3000 | 0 0 |
| ref_summary | CLIP | 0000001E 528 | ＭＳ Ｐ明朝 18 no | 0 0 0 | 760 | 220 | the 6 variables of TextIns idx 529 | read the template from idx 529 | 0 0 |
| people_body | SCROLL | 00001878 570 | ＭＳ Ｐ明朝 24 no | 1 0 3 | 690 | none | 人物/*.テキスト | see 2.3 | 1 0 |
| item_summary | CLIP | 00001878 1629 | ＭＳ Ｐ明朝 25 no | 1 0 4 | 850 | 90 | 事典物.簡易説明 | none | 1 0 |
| event_summary | CLIP | 00001878 1525 | ＭＳ Ｐ明朝 25 no | 1 0 4 | 850 | 90 | 事典出来事.簡易説明 | none | 1 0 |
| name_plate | CAPTION | 00001878 518 | ＭＳ Ｐ明朝 30 yes | - | - | start_x 493, limit_x 680 (ページ 0-2), 960 (ページ 3) | 人物名簿.表示名 | none | Japanese: ＭＳ 明朝 30 bold on 名前, and size 15 bold on 読み仮名; take the wider |
| notice_place | CAPTION | 0000001E 2415, 2515 | ＭＳ Ｐ明朝 30 yes | - | - | start_x 110, limit_x 960 | 事典場所.詳細チャプター | none | ＭＳ 明朝 |
| notice_event | CAPTION | 0000001E 2420, 2520 | ＭＳ Ｐ明朝 30 yes | - | - | 110, 960 | 事典出来事.表示名 | none | ＭＳ 明朝 |
| notice_item | CAPTION | 0000001E 2425, 2525 | ＭＳ Ｐ明朝 22 yes | - | - | 110, 960 | 事典物.簡易説明 | none | size 30 in the original |
| notice_person | CAPTION | 0000001E 2437, 2531 | ＭＳ Ｐ明朝 30 yes | - | - | 110, 960 | 人物名簿.表示名 | none | ＭＳ 明朝 |
| notice_end | CAPTION | 000000F2 1049; 000019DD 135; 00001FBE 123 | ＭＳ Ｐ明朝 22 yes | - | - | 110, 960 | the variable 終了時用事典解禁通知: check 事典物.簡易説明, 事典場所.詳細チャプター, 事典出来事.表示名 and 人物名簿.表示名 at size 22 (which tables feed it: `work/shorten-restore/PROGRESS-C.md` line 426) | none | size 30 in the original |
| jikkyo | NOT_MODELLED | 00001F8A 626..689 | ＭＳ 明朝 20 | flag FONTCHANGEABLED unset | 286 | 290 | 実況/*.テキスト | - | - |

After the failure-2 fix is applied, the name_plate row changes to size 26 and `start_x = Max(410, Min(490, 676 - (px + 4))) + 3`.

Not in the registry and therefore NOT MODELLED until someone resolves their limits from the dump: every other Caption with table or expression text
(about 200 sites, list: `fit/inventory.tsv`, column `text_source` = DB or expression), the place / event / item page captions of 00001878
(idx 838, 1405, 1669), the chatter captions (2.6), the reference unlock notice (2.5), the tutorial boxes, 場所詳細 (shadow 2).

### 3.7 Output

`work/fitcheck/findings.tsv`, UTF-8, one row per checked cell that is not OK, columns:

`surface  table  key  column  lang  lines_or_px  capacity_or_limit  widest_line_px  verdict  jp_lines_or_px  jp_capacity_or_limit  jp_verdict  class  text_first_60`

Plus a last console line per surface: `surface: cells N, OK a, TIGHT b, CLIP c, PAGES d, NOT_MODELLED e`.

Reference results the checker must reproduce: node_comment = 315 cells, 1 CLIP (ID 92 = reference No.101, column 3概要, English 23 lines of 13,
Japanese 18 of 12, class AS_ORIGINAL) (`fit/commentary_scan.tsv`). name_plate at size 30 = 24 names, 12 CLIP (list in 4.2).

## 4. FIX DECISIONS

### 4.1 Failure 1, reference No.101 commentary: leave as the original

Proof (`fit/q3_ref101.out.txt`, `fit/commentary_scan.tsv`):

| | text | lines needed | lines fully visible | share of the text visible |
|---|---|---|---|---|
| Japanese original (border 1: 29 px per character, 25 per line, pitch 29) | 439 characters | 18 | 12 | 300 of 439 = 68% |
| English build (14 px per letter, pitch 27) | 1111 characters | 23 | 13 | 631 of 1111 = 57% |

- The Japanese overflows under any reading of the border constant: K 1, 2 or 3 gives 351, 312 or 300 of 439 characters (`fit/q3_cutpoint.py`).
- It is the only cell of 315 that overflows, in either language, and the table gives this one column a cap of 1200 characters.
- The box has no way to page or scroll in the original either (same commands, 2.2).
- So the cut is the author's. The English copies it. No script or table change.
- Difference to know about: the English cut falls about 50 Japanese characters earlier in the meaning than the Japanese cut
  (Japanese character 248 against 300). Both stop inside the same sentence. No change proposed; never shorten the text to match.

### 4.2 Failure 2, name plate: fix in 00001878

| script | idx | command | property | old | new |
|---|---|---|---|---|---|
| 00001878 | 516 | Caption 人物テキスト ("????" case) | PR_FONTHEIGHT | 30 | 26 |
| 00001878 | 518 | Caption 人物テキスト | PR_FONTHEIGHT | 30 | 26 |
| 00001878 | 554 | PropMotion 土台横移動 (ObjName 人物テキスト土台, ObjProp 3) | Value | `490` | `Max(410, Min(490, 676 - GetProp("人物テキスト土台", 5)))` |

- `Min` and `Max` are engine functions the game already uses (`ノベルシステム/■オプション_テキスト速度.lsb` idx 14).
- 676 = the selector's x 680 minus a 4 px gap. The plate keeps x 490 whenever it fits there and moves left only as far as needed.
- 410 = the left floor. The scroll-up icon (idx 602) covers x 301..409, y 50..70 at a higher priority; the title banner (396 px wide, priority 10000) ends before it.
- Result (`fit/roster2.out.txt`): all 24 names fully visible. The plate moves for 7 names: Haruka Niimura 489, Eiichiro Niimura 484, Kengo Shirozaki 484,
  Abaddon Avatar 483, Chigaya Niimura 481, Iori Goshirakawa 475, Minato no Tsunamune 416; the two page-3 names sit at 410 and end at x 877 and 833.
- The Value edit is an expression, so `tools/lsb_prop.py` cannot write it; it needs a small patch script of the kind of `patch/fix-00001878.py`.
  Fallback with integers only: Value `490` -> `416` for every name (all 24 fit; every plate sits 74 px further left).
- Rejected: size 24 alone (Minato no Tsunamune is 237 px, room 187). Size 30 with the moving plate (Minato no Tsunamune is 293 px, room 266).
  Raising the plate over the selector (different parents; the plate would outlive its page). PR_TOP stays 22.
- Not checked on screen. Ask for one screenshot of Mifuyu Niimura and one of Minato no Tsunamune after the build.

Every 表示名 of `tsv-en/人物名簿.tsv` that is cut today (bold ＭＳ Ｐ明朝 30; room 187 px on pages 0-2, 467 px on page 3):

| ID | page | name | width px | over by |
|---|---|---|---|---|
| 0 | 0 | Natsumi Kogori | 205 | 18 |
| 1 | 0 | Haruka Niimura | 209 | 22 |
| 4 | 0 | Mifuyu Niimura | 204 | 17 |
| 7 | 1 | Eiichiro Niimura | 214 | 27 |
| 9 | 1 | Chigaya Niimura | 218 | 31 |
| 11 | 1 | Kotaro Niimura | 204 | 17 |
| 12 | 1 | Sakura Niimura | 202 | 15 |
| 14 | 1 | Kengo Shirozaki | 215 | 28 |
| 16 | 2 | Minato no Tsunamune | 293 | 106 |
| 18 | 2 | Iori Goshirakawa | 223 | 36 |
| 21 | 3 | Arvore duma Mulher [A Woman's Tree] | 526 | 59 (screen edge) |
| 22 | 3 | Arvore dum Homem [A Man's Tree] | 477 | 10 (screen edge) |

Momoko Goto is 187 px: exactly at the limit, visible. The other 11 names fit.

## 5. WHAT THE OLD MODEL GOT WRONG

1. The extra advance is not 0.15 em. It is a whole number of pixels set by the flags: 1 + shadow + 2 x border. It does not grow with the font size.
   0.15 em happened to equal 4.5 px at size 30, close to the scene box's 4.
2. Glyph widths came from PIL (fractions, no hinting). The engine uses GDI's whole-pixel cell and widens it when the ink is wider than the advance (`f`).
3. The `ui` pass used extra 0 on boxes without a border. The minimum is 1, and shadow adds 1.
4. The wrap test was "the word fits". The engine tests "the word and the space after it fit". The 0.15 fudge hid this on the scene box only.
5. Line pitch was 1.09 x size + linespace. It is size + linespace + shadow + 2 x border: 27 not 29.25 for the node commentary, 24 not 25.98 for the synopsis.
6. Lines per box was height / pitch. It is (height - glyph height) // pitch + 1.
7. The node commentary font was treated as unknown and guessed at 16 to 22 px. It is ＭＳ 明朝 25, written in the TextIns style.
8. `fit_audit.wrap` breaks at a full-width space and drops it. The engine draws it as a glyph and keeps it at a line start.
9. Captions: bold was not modelled, K is 0 there, and the limit "960 - left" ignored objects drawn over the caption.
10. Every surface whose text comes from a table was reported UNMEASURED and never checked. Both field failures are in that class.
11. The calibration used 8 break positions and no glyph positions, so several wrong constants could pass it.

Numbers from other lanes that used the old model and should be recomputed by the checker: synopsis "18 visible lines" (2.7: 20, 17 clear of the buttons);
commentary box "8 lines at 200 px, 9 and 12 lines needed" (00001F8A, section 2.9); the caption widths in `work/shorten-restore/laneB/allfit.tsv`;
the `fitref.py` line counts for node comments (new scan: only reference No.101 overflows).

## 6. Open questions

1. PR_FONTCHANGEABLED unset on the 17 commentary boxes of 00001F8A: does English draw on a half-width or a full-width advance there? One screenshot of a scene
   with the commentary panel answers it. Until then the surface is NOT MODELLED.
2. PR_FONTSHADOW 2 (場所詳細, 00001878 idx 834): K = 3 and pitch + 2 are assumed by extending the rule.
3. Border without shadow (the Japanese node commentary): K = 3 is derived by subtraction, never seen alone.
4. Caption with regular weight: K = 0 is verified for bold only. Line pitch of a multi-line Caption is not known.
5. Japanese line-start rules for punctuation are not known; Japanese counts can be 1 line off.
6. Text past PR_HEIGHT on a box that cannot be clicked: dropped or held on an unreachable second page? Either way it is lost; not tested.
7. The 7 place unlock titles over 850 px (2.5) are a model result only.
8. The friend's machine has the same ＭＳ 明朝 metrics as this one (81 of 81 lines agree); a player with another font file would differ.

## 7. How to re-run

```
cd F:/Projects/shigatsu-youka-en
PYTHONUTF8=1 uv run --no-project --python 3.12 python work/feedback-20261113/fit/verify_all.py            # 81 lines, new model
PYTHONUTF8=1 uv run --no-project --python 3.12 --with pillow python work/feedback-20261113/fit/old_model.py  # old model, same lines
PYTHONUTF8=1 uv run --no-project --python 3.12 python work/feedback-20261113/fit/q3_ref101.py            # failure 1, both languages
PYTHONUTF8=1 uv run --no-project --python 3.12 --with pillow python work/feedback-20261113/fit/commentary_scan.py
PYTHONUTF8=1 uv run --no-project --python 3.12 python work/feedback-20261113/fit/roster2.py              # failure 2, all names, fix check
```
