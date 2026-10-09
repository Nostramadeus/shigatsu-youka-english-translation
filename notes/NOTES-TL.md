# NOTES-TL.md — translator notes destined for the reader

file:line | term/line | note text | first-occurrence only?
---|---|---|---
00000024:00000799.lns:126 | 死神 | "shinigami: a god of death" | first occurrence of the term in READING ORDER; wording copied byte for byte from the 0000034C TN (pass-2 review, romanized-term-per-file rule)
000001DB:15:32 | 四月病 | coined against the real Japanese term for a slump after a new start, the May blues. | first occurrence in variant [15]; the same note is repeated in variants [21] and [30] because only one variant is ever played -> Q1126
000001DB:21:32 | 四月病 | coined against the real Japanese term for a slump after a new start, the May blues. | first occurrence in variant [21]; variant [21] never prints 五月病 anywhere, so the note is the only place the pun is visible on that route
000001DB:30:38 | 四月病 | coined against the real Japanese term for a slump after a new start, the May blues. | first occurrence in variant [30]
000001DB:15:76 | し…… / に…… / が…… | the words break off; the Japanese syllables are kept as sounds. | one note for the three-cell run, placed on the first cell only -> Q1123
system:0000001E | "\r\nが解禁しました。" -> "\r\nhas been unlocked." | SUFFIX: follows reference number + format + title, so the EN reads as the tail of that sentence | n/a (runtime fragment, not a reader-facing TN)
system:0000001E | "リファレンス\r\nNo." -> "Reference\r\nNo." | PREFIX: the number follows immediately with no space, as in the JP | n/a
system:0000001E | "ノード" -> "Node " | PREFIX: the node number is appended; EN adds the space the JP does not need | n/a
system:0000001E | " 残ポイント " / "　残ポイント " / "残ポイント " -> "Points left " | PREFIX/INFIX before a number; three whitespace variants of one JP string take one EN reading, per the brief | n/a
system:0000001E | "必要ポイント " / "必要ポイント　" -> "Points needed " | PREFIX before a number; two whitespace variants, one EN | n/a
system:0000001E | "不足しているパーツ..." + N + "つ目/個目のパーツを追加しますか？" | SPLIT: the prefix now ends "...to add part ", the number is injected, and the suffix is "?" -- the ordinal cannot follow the digit in English | n/a
system:0000001E | "文字数：" + N + "文字" -> "Characters:" + N + " characters" | label PREFIX and counter SUFFIX, both kept | n/a
system:0000001E | "\r\n閲覧人物：" / "　閲覧日時：" -> "\r\nViewed by:" / "  Viewed on:" | LABELS: the value follows the colon with no space, as in the shipped line557 block | n/a
system:0000001E | "ノード数：" / "文字数　：" -> "Nodes        :" / "Characters   :" | LABELS built inside Calc and shown through VAR 概要用ノード文字数 in lns-en/0000001E-line557.lns; added to the map although the pre-filter missed them | n/a
000001DD:000016F6:532 | さきいか | [TN: dried shredded squid, sold as a snack] | yes, first occurrence in the project (GLOSSARY first_seen 000001DD:11:143)
000001E1:00000593:80 | 御神木 | [TN: the sacred tree of a shrine, held to house a god] | yes, first occurrence (GLOSSARY first_seen 000001E1:33:16)
000001E1:00000593.lns:308 | 花見 | "hanami = cherry-blossom viewing" | first occurrence in reading order (earlier than the GLOSSARY first_seen). Wording unified on the general gloss, Q2121 ruling; the drinking sense stays in the LINE, which says "hanami drunk"
000001E3:000002A0:74 | 先輩 | "[TN: senpai = an older schoolmate]" | first occurrence in the project, yes
000001E3:000002A0:253 | ドリンクバー | "[TN: a self-serve drinks counter]" | first occurrence, yes
000001E3:000002A0:436 | 神隠し | "[TN: a disappearance blamed on gods or spirits]" | first occurrence, yes
0000020B:000002D4.lns:230 | 花見 | "hanami = cherry-blossom viewing" | first occurrence in this file; note moved from line 232 to the term's own line per Q1320
000001E3:000002A0.lns:456 | 花見 | "hanami = cherry-blossom viewing" | first occurrence in this file (romanized-term-per-file rule, pass-2 review of part 1)
0000020D:000002E3.lns:153 | 花見 | "hanami = cherry-blossom viewing" | first occurrence in this file (romanized-term-per-file rule, pass-2 review of part 1)
0000020D:000002E3:353 | 鉈 / nata | a nata is a heavy single-edged Japanese billhook | first occurrence only
0000034C:00000353.lns:592 | 死神 | "shinigami: a god of death" | first occurrence per route
0000034C:0000242C.lns:518 | 死神 | "shinigami: a god of death" | same TN in variant [17] per Q1126
0000034C:000024C8.lns:506 | 死神 | "shinigami: a god of death" | same TN in variant [23] per Q1126
000002F8:12:78 | 十三回忌 | "the thirteenth-year rite falls twelve years after a death" | first occurrence only (the term returns at 00000550) -> Q040, Q1486
000002FA:11:60 | 「せ……せ……」 | "the words break off; the Japanese syllables are kept as sounds." | the wording is reused verbatim from the existing TN for this device elsewhere in the project -> Q1490
00000366:00000366-00000376.lns:117 | 能面 | Noh is classical Japanese theater whose actors wear carved wooden masks | y (first occurrence of the romanized term, Q043 best guess)
00000473:00000473-0000047C.lns:187 | 銃刀法違反 | a Japanese law restricting the carrying of blades and firearms | y (first occurrence, the GLOSSARY row asks for it)
000004A7:000004A7-000004AF.lns:392 | キャリア組 | career track = fast-stream police recruits groomed as future executives | y (first occurrence, the GLOSSARY row asks for it)
00000564:00000564-0000057A.lns:127 | 中二病 / chunibyo | "[TN: chunibyo = the middle-school delusions-of-grandeur phase]" | first occurrence only? yes (glossary first_seen 00000564:11:26)
00000564:00000564-0000057A.lns:758 | 緊急逮捕 | "[TN: emergency arrest = arrest made without a warrant]" | first occurrence only? yes (glossary first_seen 00000564:11:182)
00000595:00000595-000005AB.lns:290 | 地理／チリ homophone | "[TN: geography is chiri in Japanese, a homophone of Chile]" | first occurrence only? yes, the gag runs once
00000550:00000579.lns:222 | 十年祭 / the memorial-year arithmetic | "[TN: Shinto counts ten years; the Buddhist tenth-year rite falls at nine]" | first occurrence in the project; 11 words; at the end of that cell's line per Q1320
000004BB:000004C7:8:30 | JK | JK = joshi kosei, a high-school girl | first-occurrence only? yes (first occurrence of the term in the project)
000004BB:line16:16:5 | 津軽弁 | Tsugaru: a dialect of Japan's far north, hard for other Japanese | first-occurrence only? yes; Q070's recorded best guess is to name the dialect and add a short note, and no English accent is assigned
000004CF:000004F7:12:15 | ソメイヨシノ | Somei Yoshino: the cloned cultivar of most Japanese cherry trees | first-occurrence only? yes (the GLOSSARY row asks for a TN at first occurrence, which is this cell)
000004CF:000004F7:12:91 | 夢枕 | the dead appear at a sleeper's pillow to deliver a message | first-occurrence only? yes (GLOSSARY asks for a TN at first occurrence)
000004E3:000004F8:11:115 | 死神 | shinigami: a god of death | first-occurrence only? per route: the wording is copied verbatim from the shipped 0000034C TN, and this branch's player may not have seen that file (Q1126 reasoning)
000004E3:line27:27:131 | 鉈 | a nata is a heavy single-edged Japanese billhook | first-occurrence only? per route, wording copied from the shipped 0000020D TN; placed once for the two occurrences in this file
(none placed in any of the four tables) | - | - | -
system:0000001C | `% 　　` -> `%   ` | suffix after the completion number, then the arc name follows: "Overall completion: 73%   True Jusatsu Arc progress: 12". The two full-width padding spaces become ASCII spaces (1 ASCII + 2 U+3000 -> 3 ASCII).
system:0000001C | `全体進行率:` -> `Overall completion: ` | prefix; the percentage number is concatenated after the colon. Trailing ASCII space added because the ASCII colon has no built-in gap, unlike the full-width one.
system:0000001C | `進行数:` -> ` progress: ` | infix: the arc name is glued in front of it and the count after it ("True Jusatsu Arc progress: 12"), so EN takes a LEADING space (English needs a word gap the JP does not) and a trailing one.
system:0000001C | `\r\n\r\nが出現しました。` -> `\r\n\r\nhas appeared.` | suffix after the whole notification block (arc + title + date + person + character count); the block is the subject of the sentence.
system:0000001C | `\r\n\r\nが解禁しました。` -> `\r\n\r\nhas been unlocked.` | same suffix shape; EN identical to the `\r\nが解禁しました。` row already in patch/labels-0000001E.tsv.
system:0000001C | `\r\n\r\nに分岐が発生しました。` -> `\r\n\r\nnow has a branch.` | suffix; JP marks the title with に (location), EN keeps the title as subject so the attachment side does not move.
system:0000001C | `\r\n\r\nに裏ルートが出現しました。` -> `\r\n\r\nnow has a hidden route.` | same shape as the branch notice.
system:0000001C | `\r\n\r\nの実況モードが解禁しました。` -> `\r\n\r\nCommentary mode has been unlocked.` | suffix, but rendered as a standalone sentence: the JP の makes the title the possessor of 実況モード, and English cannot glue a possessive onto a five-line block. The block still reads as the referent because two \r\n separate them.
system:0000001C | `\r\n\r\nの実況モード(分岐)が解禁しました。` -> `\r\n\r\nCommentary mode (branch) has been unlocked.` | same, with the JP's half-width parentheses kept.
system:0000001C | `\r\n\r\n人物：` -> `\r\n\r\nPerson: ` | prefix; the person name is concatenated after it. One ASCII space after the colon replaces the visual gap the full-width colon had.
system:0000001C | `\r\n\r\n文字数：` / `文字数：` / `\r\n\r\n\r\n\r\n文字数：` -> `Characters: ` | prefix; the character count is concatenated after the colon. Three separate map rows (they differ only in leading newlines) with the same EN.
system:0000001C | `\r\n閲覧者 ：` -> `\r\nViewed by    : ` | prefix in the reference summary block; padded so the colon sits at the same column as `Format       : ` and `Viewed on    : ` (13 characters before the colon, as in patch/labels-0000001E.tsv).
system:0000001C | `\r\n閲覧日時：` -> `\r\nViewed on    : ` | same block, same column.
system:0000001C | `\r\n形式　　：` -> `\r\nFormat       : ` | same JP key as a row in patch/labels-0000001E.tsv; EN reuses that row's padding, plus one trailing space (see the divergence note in the report).
system:0000001C | `セクション` -> `Section ` | prefix; the number and "/total" are concatenated ("Section 1/5"). The trailing space is required: English needs a gap between the noun and the number, the JP does not.
system:0000001C | `チュートリアル(` -> `Tutorial (` | prefix; the page number is concatenated, then `) ` (untranslated, lone punctuation) and the tutorial title from the DB.
system:0000001C | `を分岐直前から開始することができます。 ` -> ` can be started from just before its branch. ` | suffix after a scenario name taken from @Sender; EN adds a LEADING space (the JP glues the particle を directly to the name) and keeps the JP's trailing space.
system:0000001C | `分岐があります。『分岐直前から』を選ぶと、` + `文字目から開始します。` -> `There is a branch. Choosing 'From just before the branch' starts you ` + ` characters in.` | the DB value DBGetStr("コア文字数") is injected between the two literals; the number stays in the middle, so the second fragment remains a suffix after a number. The quoted button label 『分岐直前から』 is NOT a literal anywhere in the scripts or in データベース/システムテキスト.tsv (probably a button image), so 'From just before the branch' is a guess that must be matched to whatever that button ends up saying.
system:0000001C | `残ポイント ` -> `Left: ` | prefix before the point total, and the length is LOAD-BEARING: commands 4749-4761 re-read this caption with JCopy(GetProp("残ポイントテキスト", 50), 7), i.e. they strip exactly 6 characters to get the number back. `Left: ` is exactly 6 characters, so the rolling point counter keeps working. Any replacement must also be 6 characters. (patch/labels-0000001E.tsv uses `Points left ` = 12 characters for the same JP string and breaks 25 such sites — see the report.)
system:0000001C | `→マークのあるシナリオは...` | the arrow → (U+2192, CP932 0x81A8) is KEPT because the JP sentence names the glyph drawn on the chart. Inside the hidden-route hint the other JP arrow (『右クリック→裏ルートボタンをクリック』) is a "then", so it is rendered as the word: 'right-click, then click the hidden route button'.
system:0000001C | `1倍` .. `16倍` -> `1x` .. `16x` | scroll-speed labels; ASCII "x", matching `スクロール速度 ×` -> `Scroll speed x` in patch/labels-0000001E.tsv.
system:0000001C | `②③④` in the hidden-route prompts -> ASCII 2 / 3 / 4 | same treatment as the circled digits in the navigator titles (tl-log-NAV2.md).
000016AE:000016AE-000016B9.lns:27 | 花見 | hanami = cherry-blossom viewing | first occurrence in THIS file; wording reused byte for byte from 0000020B / 000001E3 / 0000020D per Q2121, once per file per Q1490
000016AE:000016AE-000016B9.lns:60 | 御神木 | the sacred tree of a shrine, held to house a god | first occurrence in THIS file; wording reused byte for byte from 000001E1:80
000016AE:000016AE-000016B9.lns:92 | 元木『町』 vs 市 | -cho = town; the next size up is a city | TN case 6 (Q1482/Q1483/Q1486): the cell's whole point is that a place named -cho already has a city's population, and "Motoki-'cho'" cannot carry it in English. First and only occurrence of the reasoning.
雑談リスト.tsv:21:A2 | 三日 in her own name vs 四月八日 | her 'Mika' is written with the characters for 'third day' | first occurrence only? yes
雑談リスト.tsv:37:A4 | たけのこ派 / きのこ派 | rival chocolate snacks shaped as bamboo shoots and mushrooms | first occurrence only? yes (placed on A4, not on the キャプション1 cell, because that cell is a clickable choice label)
