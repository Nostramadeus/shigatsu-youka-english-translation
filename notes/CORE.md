# CORE.md — the ONE notes file a translation agent reads (Fable, 2026-09-25)

Distilled from notes/GLOBAL.md (360 KB, 422 files read through) per notes/CORE-BRIEF.md.
**A DRAFTER DOES NOT READ THIS FILE WHOLE** (rev. 2026-09-25, rules audit #4): run
`sh tools/core_fenced.sh <the last id you translate>` and read `notes/_tmp/core-<id>.md`, which is this file
with every line whose earliest file id is later than yours removed. §C4 and the §D1 "LATER" clauses are
reviewer and orchestrator material. Do NOT page through GLOBAL.md; grep it only for the anchors named here (see §I).
Rank: **STYLE.md outranks any "best guess" here; GLOBAL.md is the long version and the only place the
per-file detail lives.**
Anchors `A§n` / `B§n` / `C§n` = GLOBAL.md Part A / B / C, section n.
Every fact keeps its as-of file id where GLOBAL has one; the knowledge fence (TRANSLATOR-BRIEF-v2 §0, not §2)
applies to all of it. Where GLOBAL says a thing is open, CORE says open: stop and file a QUERIES row, do not invent.

---

# A. TYPOGRAPHIC DEVICES AND THEIR FIXED RENDERINGS

CP932 floor (STYLE.md 2026-09-25, from the in-game font test): allowed = ASCII plus `“ ” ‘ ’ … ― − ～`.
NOT representable: em dash U+2014, macrons, accented Latin. No italics, no bold, no small caps — every
"small caps" best guess below is therefore dead and needs a different device.
THIS TABLE BEATS THE CHECKER (rev. 2026-09-25, rules audit #3): the allowed set governs text the translator
WRITES. A glyph or space run a row below says to KEEP is copied byte for byte; if `qa_check` raises a HARD
line on it, the row wins and the waiver is logged as a DECISIONS row. U+3000, full-width `（）` and the banner
brackets `【 】` (CP932 0x8179/0x817A, kept in English banners by owner ruling) are reported SOFT for exactly
this reason; a run of three or more ASCII hyphens is a horizontal rule, not a dash, and is copied as printed. A layout full-width space is never replaced by ASCII spaces (an ASCII
space is about a third as wide in the proportional face, so the device disappears); only label padding is.

| device | EN rendering | rule (<=25 words) | anchor |
|---|---|---|---|
| 「」 ordinary audible speech | straight ASCII `"..."` | Default. 「」 is NOT a universal speech marker here; 00000EAF makes it mean "this person can physically speak" (Q254). | B§1.1 |
| 『』 (~150+, five jobs) | single `'...'` everywhere | Register carries the rest: the 450-year-old book is plainer and shorter than the narration — do not gild it (Q385). | B§1.2 |
| one document quoted differently in two files | keep both treatments | Keep them distinct rather than harmonising (Q504, medium). | B§1.2, B§3.10 |
| straight `"..."` in the SOURCE (~20 sites) | curly `“...”` (U+201C/201D) | SETTLED by STYLE 09-25 (was Q036/Q071/Q079). Means "text nobody present is speaking": phone messages, announcements, broadcasts, documents, a mute character's written words. | B§1.6, STYLE |
| the mute narrator's every utterance, 2,241 lines (00000EAF) | curly `“...”` | Never quotation-mark her into speaking; 「」 is reserved for other people (Q254, high). Four mute channels: 手話, notepad, a finger × across the mouth, the ニカッと grin. | B§1.6, A§1 五島 |
| bare unquoted cells (letters, memos, scripture, 戸籍, ceremonial speech, chat logs) | bare, NO wrapper added | Keep unquoted and unindented exactly as printed, keep the line breaks, signature alone on its line; register shift is the only signal the JP gives. | B§1.7 |
| indented bare cell (two leading full-width spaces) | keep both full-width spaces | Add nothing, never tag a speaker (Q158, high). Sites 000009FE:15:0/23:0/31:0-1, 00000A62:15:0, 00000AC4:15:0. | B§1.8 |
| 「――」 line-initial prefix, FIVE jobs | `―` (U+2015) at the same position, one mark for all five jobs | SETTLED by STYLE 09-25 (was Q709, owner-blocking). Never replace it with a speaker label. | B§1.3, STYLE |
| — job 1, speaker channel (whole files: 000003A8/3AE/3B4/3BC, 00002078, 00002084, 000020BB, 00001BA2/1BA8, 0000243F, 00001D34) | leading `―` | Keep it as a literal line-initial marker; attribute nothing. 00002078's two speakers have NO register difference at all (Q836). | B§1.3 |
| — job 2, static dropout mid-word 「聞こえ――ますが」 | `―` inside the word | Break the English in the same places, mid-word where the JP breaks mid-word (Q064, high). | B§1.3 |
| — job 3, off-screen / unhearable voices (Q169, Q264, Q589, Q623) | leading `―` | Keep the dash, attribute nothing, add no "I imagined", "I felt", "it said". | B§1.3 |
| — job 4, narrator's transmitted thought (0000151C:8:174-294) | leading `―` on HER lines, `"..."` on the replies | Keep the inversion of job 1; it is the file saying her thoughts are leaving her head (Q618). | B§1.3 |
| — job 5, ordinary audible non-focal speaker (00001818 onward, press conferences Q656, broadcasts Q359/Q414, documentary Q690) | leading `―` | Same mark, context does the work. | B§1.3 |
| a 「――」 line and a 「」 line joined by ⏎ in one cell | both markers inside the one cell | Q808, Q816, Q845. | B§1.3 |
| a cell containing ONLY 「――」 (4 sites) | a lone `―` | Keep the cell count, add nothing, let no narration supply a pronoun (Q550, high). 「――――」 may take four dashes (Q509). 00001505:8:190 must be IDENTICAL to whatever 0000127A:8:160 gets (Q556). | B§1.4 |
| empty 「」 cells (~45) | `""` empty, exactly as printed | Never insert an ellipsis; flag every one so no cleanup pass deletes it. 00000EF6 has ~36 for a comatose girl's turn AND separate 「…………」 cells — the two must stay different (Q320, high). | B§1.5 |
| one-cell reveal row-block (>=13 sites) | keep the split | Order the English clause so the withheld element still lands last in the second cell (Q179, Q028). Bare stays bare, quoted stays quoted (Q061). Never merge into the preceding cell (Q899). | B§1.9 |
| ruby-residue spacing (~60 sites: 「 猿 」「 掟 」「南 崎しのり」「宝 町 駅」「H o w」) | strip the spacing, translate normally | SETTLED by STYLE 09-25. If the stripped reading matters to the scene, use a [TN:]. Diagnostic exception: 000021BD:21:39-43 is the only printing of the ancestral instruction with NO residue — evidence block [21] is a different document (Q841). | B§1.10, STYLE |
| ⏎ job 1: two or more speakers in one cell (~20) | keep the break and every set of quotes inside the one cell | Consider a shared attribution in the surrounding narration (Q044, Q511, Q554, Q808, Q845). 000020C6 has FIVE voices per cell joined by ⏎. | B§1.11 |
| ⏎ job 2: layout (「計⏎画⏎通⏎り」, legends, padded UI labels, the 29-dish list, generation tables) | reproduce the shape approximately | Record in NOTES-TL.md that exact alignment is impossible (Q721, owner-blocking). Reproduce both layouts of the dish list, item order identical (Q260). | B§1.11 |
| ⏎ jobs 3-4: chat and board posts (000020FC `handle⏎message`, 00001A65 whole posts in one cell); two full sentences in one narration cell (0000156A:58:13, 76:33) | keep every break | Keep handles and timestamps inside the one cell; do not merge or split the two-sentence cells (Q831, Q733, Q662). | B§1.11 |
| row-blocks printed out of scene order (000006F9, 0000088B, 00000EAF, 00000EDF, 00000EF6, 00000F0D, 00000F24, 0000156A) | translate in PRINTED order | Keep a story-order key in NOTES-TL.md and a note at the head of the file; printed order is presentation, story order is truth (Q641, Q253, high). Diff every near-duplicate variant pair first; never "improve" one (Q025). | B§1.12 |
| dakuten on every kana 「と゛い゛う゛わ゛け゛で゛…」 and on a bare 「ん゛！？」 | **open: keep the surface, log a query** | Q176, owner, high. One device must cover a whole sentence AND a single syllable. Recorded options: doubled consonants / interpolated apostrophes; a bracketed description. Small caps are NOT available. | B§1.13, B§1.31 |
| one kana or syllable per cell (~25 sites, 3-17 cells) | keep the cell count, split the English at syllables or letters (letters may double up) | Do not smooth. Where the JP puts the strongest word last, restructure the English so it still lands last (Q085, high). Mark an interpunct beat with a hyphen ("SO-/ OR-/ ELSE-"), decided once for all instances (Q084). | B§1.14 |
| — cell-split word the JP completes in-file (「お／と／う／さ／ん？」) | same number of cells, one or two letters each | SETTLED by STYLE 09-25 (Q1084): the English word is chosen for the cell count as much as for register; log the choice in DECISIONS. | STYLE |
| — cell-split word NOT completed in the file | romanise mora by mora ("Shi... / ni... / ga...") | SETTLED by STYLE 09-25 (Q1123): one TN on the first cell; the EN must NOT resolve into a word; the file where the JP completes it decides the completed form, earlier cells stay continuable. | STYLE |
| — 『ド／ロ／ー／ガ』 read off a bottle | `D / r / o / ga` (four cells) | GLOSSARY locked (Q1083/Q004); 00000656 must reuse it verbatim. | G, B§1.14 |
| — 「だ／い／す／き」, a dying child (00000BB7:11:119-122) | **open: keep the surface, log a query** | Q182, owner, high. Best guess recorded: "I / love / you / so much", or reorder so the last cell is strongest. | B§1.31 |
| — eight-digit birthday typed BACKWARDS, one digit per cell (0000156A:76:83-92) | keep eight cells, one digit each | Keep the two explanation cells before them (Q650, owner, medium). | B§1.31, C§2b |
| repeated-character walls (~200 「は」; 「殺したい」x14; 「ががが…」; 「キエエエ……！！」 ~80 chars) | keep the same syllable count where the box can hold it | Reduce only where it cannot and NEVER to one (Q622). Strip intent, keep counts (Q335). Keep distinct lengths distinct (Q240). Flag the long cells for the text-box measurement (Q049, Q132). | B§1.15 |
| — 0000104E:11:38-52 laughter as a layout object | **open** Q412, owner, medium | Best guess: one "ha" per short cell, scale the long cells to the same screen area. Must be decided together with Q527. | B§1.31 |
| — 00001325:8:200-215 interior scream | **open** Q527, owner, medium | Romanised JP vs an English scream; must match the Q412 decision. | B§1.31 |
| radio / broadcast / PA / press conference (six sub-forms) | prefixed `―` = broadcast or reporter; announcements in curly `“...”` | Flag unattributed voices individually (Q359). Keep the dash for documentary voice with no quote marks (Q690). Press conference: reporters bare `―`, spokesman in `"..."` (Q656). | B§1.16 |
| nested quotation, up to FOUR levels (Q385) | 『』 stays `'...'`; seams stay unmarked | Let register do the work: the inner voice is plainer and shorter. Applies to Q267, Q575, Q582, Q617, Q400. | B§1.17, B§3.3 |
| dated caption in parentheses, no character's voice (「祀耀805年八月一日（元木駅集団発狂殺人事件から1年4か月後）」) | set as a caption line, not as narration | Q376, high. | B§1.18 |
| era dates and a Gregorian caption in the same project | dates stay as written | SETTLED by STYLE 09-25 (Q943/Q827 provisional): era name romanised ("Shiyo 805, August 1"); a Gregorian caption stays Gregorian; no conversion either way, no TN equating them. Reversible by regex. | STYLE, B§1.18 |
| montage captions (「10分――」「20分――」「30分――。」; four cells ending 「～を抜け――」) | keep the caption shape and the trailing `―` | Q594. | B§1.18 |
| era-year welded to an event name 「大食祭804」 | keep the welded form | Q270. | B§1.18 |
| variables spliced BETWEEN cells (cell begins 「様、」 or 『) | keep "-sama," at the cell head | The honorific cannot move; translate the fragments so they join naturally after "<name>-sama"; consider a TN (Q007, Q683 owner-blocking, Q804). Same for the numeric variable (「全体進行率」 / 「％……。」). | B§1.19 |
| full-width space, job 1: gaps inside words a dying person stops hearing (000013CD:8:357-358) | **open** Q555, owner-blocking, medium | Best guess: keep the gaps as blank runs of proportional length and supply nothing. | B§1.20 |
| full-width space, job 2: gaps at DIFFERENT positions in ~20 printings of one sentence | **open** Q603, owner-blocking, LOW | Best guess: gaps inside EN words at matching positions, or switch device consistently. Q896 (a converted corpse's speech) takes the same treatment plus a TN. | B§1.20 |
| full-width space, other jobs: voice floods (00000488:48, 00000EDF:235), a photograph = ten spaces inside straight quotes (Q299), the 核's eight-space turns (Q939), single-space cells (000003AE:8:28, 00001039:19:1), a whole file of one space (00001FE4, Q769), layout alignment (legends, growing indents, registry columns, song verses) | keep every space, exactly as printed | No quotes, no periods, no attribution, no punctuation; match the earlier EN wording where a flooded fragment quotes a named character; flag every one so no cleanup pass touches it (Q050, Q300, Q046, Q413, Q324, Q721, Q789). | B§1.20 |
| full-width space, job 5: the 核's turns = eight full-width spaces inside quote marks, nine times (Q939) | keep the eight spaces inside the quotes | A typographic device, not dialogue; the other speaker keeps talking into them. | B§1.20, A§1 核 |
| full-width space, job 7: a whole file that is ONE cell holding one full-width space (00001FE4) | emit one full-width space, unchanged | Q769, owner, high. | B§1.20 |
| full-width katakana, 片言 (the text names the device; three characters use it) | clipped, article-less, full-stop-separated ("I. Do. Not. Know.") | The identical device in both files; must be reusable by なつみ, 春花 and 五島 (Q073, medium). | B§1.21 |
| full-width katakana, 「スグニゲロ」 written in blood | ALL CAPS, no spacing ("RUNNOW") | Keep the next cell as the narrator working it out (Q197, high). | B§1.21 |
| full-width katakana, two spoken cells reprinted as an unattributed block (000012AD:16:0-2) | **open** Q497, owner-blocking, medium | Spaced small capitals was the least-bad candidate and italics are unavailable; fallback is spacing or a TN. | B§1.21, B§1.31 |
| full-width katakana, a whole block from a chilli-burnt mouth (00001A6B:8:5-53) | **open** Q735, owner-blocking, high | Small caps, flattened punctuation, or a TN. | B§1.21, B§1.31 |
| small kana for a slurred mouth (「ゎたしはもぅ、だめだ……」), slurred greetings (「いらっはーい」) | dropped letters and weak vowels | NOT phonetic spelling; "aye" and "lass" are localisation and BANNED by STYLE (Q104, medium). Carry archaic register with word order and verb form. | B§1.22 |
| stretched っ, same joke with a different count each time (4/6/6/5) | stretch a vowel in the EN and vary the letter count to match | Q842, Q510: open, low/medium. | B§1.22, B§1.31 |
| × / ○ / △ masking and deliberate blanks | keep the symbols, the symbol counts and the cell splits | 「生まれて／××／年」 keeps "XX" (Q023). A patient whose name and DOB are ×××× stays unnamed and ungendered (Q045, high). Censored body-part nouns keep one symbol run per cell (Q141, high). | B§1.23 |
| — a note with runs of × for illegible characters, reprinted verbatim then printed restored (00001214:8:128-159) | **open** Q494, owner-blocking, medium | Best guess: mask at matching WORD positions; masked cells identical between printings. | B§1.23, B§1.31 |
| — 「私、／×／だけどいい？」, 「××／の壁」 where × is a sex term | **open** Q832, owner, medium | The × stands for one or two characters (男 / 男性). | B§1.23, C§2b |
| Latin script inside the Japanese (~15 sites: Portuguese liturgy, "Que droga", 「Maybe。」, "How", "Easy come, easy go.") | keep the Latin exactly as printed | Keep the on-screen gloss and add ONE [TN:] at first use saying the word is English/Portuguese in the source; never delete the gloss (Q231, high). Portuguese proper-noun romanisation is Q378, owner-blocking. | B§1.24 |
| 「・」 bullet lists (5 sites) | keep bullets, the title cell and each item as a separate cell | Q305 low, Q661 medium. | B§1.25 |
| bare equation lines (「お父さん＝皮剥ぎ死体」) | keep the equals sign and the cell split | Do not turn them into sentences (Q022, Q202). | B§1.26 |
| kaomoji and text emotes (「ノ」, (￣ー￣), (^-^)) | leave the glyphs exactly as they are | Do not replace with a western emoticon; verify each against CP932 (U+FFE3 survives) (Q102, Q471, Q018). | B§1.27 |
| mojibake cells (5 navigator cells in 00002317, 00002325) | translate the DECODED intended Japanese | SETTLED by STYLE 09-25 (Q872): a pylivemaker dump artefact, not source text; log as typo. Recorded decodes are in GLOBAL B§1.28. | B§1.28, STYLE |
| engine / UI instruction set as narration (「（次のページは…）」) | translate as UI, keep the full-width parentheses | Do not give it the narrator's voice (Q164, low). | B§1.29 |
| kanji numerals against STYLE's Arabic rule (「一五歳」, 「四月三〇日」, （壱）（弐）（参）) | Arabic digits in running text; archaic numerals kept where they are LABELS | Keep the column spacing and the ⏎ breaks in registry entries (Q163, Q537, Q395, Q235). | B§1.30 |
| …… / ……… ; ―― ; ！？ ; ！！ | `"..."` once; `―` (U+2015); `!?`; `!!` preserved | STYLE.md. Leading ellipsis kept ("...I see"). NOT the em dash U+2014. `……。` → `"..."` and `――。` → `"―"`: no extra stop (rev. 2026-09-25, rules audit #11). | STYLE |
| ellipsis-only cells of DIFFERENT lengths used as a device in one exchange | do NOT collapse them silently | The collapse above is for ellipsis inside a sentence. An ellipsis-only cell stays distinct from an empty cell; growing silences across turns get flagged and a QUERIES row (rev. 2026-09-25, rules audit #17). | STYLE, B§1.5 |

---

# B. HAZARDS WITH A FIXED POLICY

| hazard | policy | rule (<=25 words) | anchor |
|---|---|---|---|
| Unmarked narrator switch — at a FILE boundary (dozens; orders 100-104 and 140-146 switch at almost every one), MID-FILE at a row-block boundary (00002444 at every boundary; 00002450 loses its narrator at [12]/[18]), and MID-BLOCK (000004BB:16:37, 000004CF:12:60, 00000617:8:43, 00000E49:11:29/117, 00000F0D [56] and [173], 00001505:8:69 for ~450 cells, 0000156A:143:32 and 193:76) | mark NOTHING in the English | Supply no name before the JP does; do not gender-mark before the JP does; record every seam in NOTES-TL.md BEFORE translating (Q030, Q060, Q078, Q220, Q350, Q448, Q605, Q642, Q933, Q944). | B§3.2 |
| Detecting a switch — the ONLY signals the JP gives | pronoun (私/俺/僕/わたくし), speech level, a speech tic (「ん……」, 「うぎゅ……」), an address form used in narration (「古郡先輩」「チガ姉」「五島ちゃん」), tense, content | Nothing else. A narrator who is never named is identified by address forms alone and the EN must reproduce that (Q640, Q901, Q920). | B§3.2 |
| Inset first-person stories, no frame at either end (>=12 sites) | mark the frame in the NOTES, not in the text | Keep the JP's lack of quotation marks, hold the inset in the same plain past, let the register shift be the only seam (Q146, Q400 high; Q575, Q582, Q617 medium). | B§3.3 |
| The anonymising device inside a told legend 「その子を仮にA子とします」 (~20 uses) | "Girl A" throughout | The introducing sentence carries the explanation (Q159, medium). | B§3.3, C§4.5 |
| Precognition, hallucination, dreams and retracted passages | translate everything STRAIGHT | Add no hedges, no foreshadowing, no tense signals, no italics. Only the retracting cell may know (Q285, high). Do not signal a dream early, do not add a scene break (Q453). | B§3.4 |
| — the ONE exception: 0000156A:28:192-195 | translate the DRIFT as drift | A recalled speech whose wording has drifted: recognisably the same speech, not the same string. Do not harmonise with 14:121-130 (Q654, medium). | B§3.5 |
| Aspect / tense / grammar distinctions that carry plot | carry them by word choice and word order, reasoning left intact | English cannot reproduce them by grammar. Rules at §B3 below. | B§3.7 |
| Homophone, kanji-spelling and wordplay hazards (~30) | most are owner items; see §B4 | Never invent a replacement pun: keep the surface meaning and log a QUERIES row (METHOD §0b). | B§3.8 |
| Dialect (5 sites, two sustained) | NEVER an English regional or class dialect | SETTLED by STYLE 09-25 (was Q611/Q785/Q843/Q070/Q149): no eye-dialect spelling, no "Engrish". Carry it by rhythm, blunt or soft word choice, contraction rate and a few fixed sentence tags, plus ONE TN at the character's first dialect line naming the dialect. | B§3.9, STYLE |
| — a dialect the narration NAMES but never writes into the lines (Q843 篠崎ハジメ; Q070 the Tsugaru chef; the 外崎 grandfather) | mark it in narration only, as the JP does | Do NOT retrofit an accent onto the dialogue. Also 新村儀之助 (000010AA, the narration calls his Japanese accented and the JP gives none), the 荒田 woman who understands two Portuguese commands and speaks none (Q422), and 殿下 (000010C3), whose ～じゃ is lordly-archaic and NOT rural. | B§3.9, STYLE |
| — the ～アル pseudo-Chinese waiter (Q149) | plain English plus a TN | Never broken "Engrish". | STYLE |
| — the ～ざます／～ですわ rich-woman register (Q074) | over-formal English, no contractions, no regional accent | A class marker, not a regional one; do not make them sound old. | B§3.9, STYLE |
| Source documents quoted in more than one typographic system | keep the treatments DISTINCT | Do not harmonise (Q504, medium). Q560 (a teaching recalled from memory, unmarked) must read as remembered rather than quoted. | B§3.10 |
| Things stated on screen that a translator must not "fix" | reproduce the contradiction | Dates that disagree (Q112, Q387, Q514, Q515, Q670, Q827), a 三回忌 right in one file and wrong in another, two names for one legal status / building / massacre / earthquake / eating contest, an inverted drug relationship (Q415), the author's own unresolved contradiction broken off mid-sentence (Q876). | B§3.11 |
| — sentences that break off and are never completed (Q126, Q685, Q698, Q718, Q750, Q778, Q803, Q858, Q860, Q952) | keep every one broken off | No supplied verb, no supplied object. | B§3.11 |
| Source typos (124 rows) | translate the INTENDED text; do NOT reproduce the typo | No "sic", no deliberate misspelling, no bracket. Log in QUERIES with the exact JP, status=typo (STYLE, after chunk 08). | B§4 |
| — deliberate broken Japanese is NOT a typo | carry it | 谷崎's broken school email (Q088), a ten-year-old's forged diary (Q525), baby-speech quoted twenty years later (Q411), slurred greetings (Q366), small-kana slurring and 片言 (Q104, Q073). Test: if a character or the narrator NOTICES the oddity it is a device; if nobody notices it is a typo. | B§4 |

## B2. Verbatim replay pairs — freeze the earliest EN and paste it

| earlier | later | what | id |
|---|---|---|---|
| 000001DB:15:28-43 | 0000066B:11:28-48 | one doorstep exchange from the other side | Q083 |
| 00000C08:15:0-19:13 | 00000DD1:11:151-163 | 13 cells replayed in 「」, no frame, no attribution | Q214 |
| 00000E19:11:187, 11:162 | 00000E49:11:30-31 | two cells reproduced AS the join between two narrators | Q221 |
| 00000E7B:54:250-68:191 | 00000E7B:180:0-135 | the same night, outcome reversed, ~15 cells identical | Q244 |
| 00000EDF:77:0-153 | 00000EDF:186:0-192:203 | two near-identical lead-ins; keep 77:145 and 192:0 DISTINCT | Q287 |
| 00000EF6:67:236-269 | 00000EF6:61:106-121 | 16 cells word for word; 61:115 is the only added line | Q319 |
| 00000801:8:163-177 | 00000F87:11:263-274 | 12 cells twenty years later, baby-speech spellings included | Q411 |
| 0000110D:12:0, 20:0 | 00001184:12:0 | an untagged voice replayed ten years later as recovered memory | Q456 |
| 000013CD:8:261-283 | 000013E6:8:0-20 | ~20 cells from the other side; only 「2人をお願い！」/「2人を案内して！」 differ | Q557 |
| 00000A94:11:120-144 | 00001459:8:203-231 | the 三畳間 exchange from the other participant's memory — freeze 00000A94 | Q576 |
| 000012C5:8:29-52 | 00001477:8:11-34 | one room from both sides, eighteen files apart — freeze 000012C5 | Q580 |
| 000012DE / 000013CD / 000013E6 | 0000148E:8:69-127 | one confrontation from THREE narrators across FOUR files; four lines identical everywhere | Q581 |
| 0000156A:92:0-5 | 0000156A:201:119-131 | six cells with exactly ONE word changed — translate 92 first, copy, change one word | Q651 |
| 0000156A:34:204-205 | 0000156A:14:0 | same sentence, two cells in one place and one cell in the other | Q653 |
| 0000156A:20:7 | 0000156A:92:23 | a prison number shouted; block 20 OPENS by reprinting it | Q660 |
| 0000156A (three more) | — | an exchange quoted back, a request reprinted before it is carried out, one line in two places | Q655 |
| 00001D40 | 00001D6F | twin files: the second reprints the first cell for cell then continues — translate the overlap once | Q767 |
| 00001214:8:128-159 | 00001247:8:136-143 | three ×-masked cells reprinted, then printed restored | Q494 (owner-blocking) |
| 00001355:8:92-96 | 000013FD:8:196-197 | five classical lines recited later with 出でて shortened to 出で | Q536 (owner-blocking) |
| 00001385:8:65 | 000013B5:8:96 | 五島's "doubt everything" rule quoted from memory twice — fix all three wordings together | Q547 (owner-blocking) |
| 00001414:8:210-214 | 000014D7:8:239-242, 8:377 | one transmission printed four times in three typographic systems | Q567 (owner-blocking) |
| 0000245F:11:128-131 | 00002464:11:0-1 | the file opens by reprinting the previous file's last two cells | Q965 |
| 00000E19 + 00000E49 | 00002473 | the same thirty minutes from the antagonist's inside, ~15 spoken cells identical | Q973 |
| 00002026 / 000021BD / 000013FD / 0000151C / 000021BD:21 | — | the ancestral transmission printed SIX times; one printing differs in wording and in ruby residue | Q619, Q841, Q853 |
| preview/trailer files | 00001C4D, 00001C5D, 00001EC0, 00001867, 00001AFE | reprint lines verbatim, out of order, no frame — build a concordance of quoted fragments FIRST | Q807, Q717 |
| 000021E2, 0000234B/50/55/5A | — | three sleepers given the SAME dream in the same format, compared in a fourth file | Q897 |
| 00002473:11:338-353 | — | two happy-memory scenes replayed as bare 「」 dialogue, no frame, a ten-year-old's tic intact | Q982 |
| route variants | 00000024, 000001DB, 000001E1, 000001E5, 0000020B, 000004CF, 000004BB, 000005C1 [11]/[21] and [15]/[25], 0000034C [11][17][23], 000008B9 [8]/[22], 0000088B [16]/[22], 000006F9, 000009FE | trimmed, not rewritten — diff each pair | Q025, Q129 |

## B3. Refrains that must be word-identical (GLOBAL B§3.6)

Each needs ONE fixed EN wording recorded in GLOSSARY before any file containing it is drafted.
IDENTITY IS OF WORDS (rev. 2026-09-25, rules audit #11): a refrain keeps its lexical choice — same nouns,
same verb — and INFLECTS for its slot ("become a family" → "became a family"). English punctuation still
follows English grammar in every printing (a question gets its mark; no stop after "..." or "―"), and two
printings differing only in optional JP punctuation get identical English plus a DECISIONS row. Byte-identity
is required only where the JP is byte-identical in the same slot (the B2 replays above).

| refrain | count | ids | status |
|---|---|---|---|
| 「よろしくお願い申し上げます」 navigator→player | ~25 menu files | Q1042 | **FIXED 09-25**: "I am in your hands." (今回も -> "this time as well"; 今後とも引き続き -> "From here on as well, I remain in your hands.") In GLOSSARY. |
| 「1人はみんなのために、みんなは1人のために」 the settlement motto | 8+ (once with a particle dropped, once coined on screen by the founder, once in a sentence that ATTACKS it, once as a mother's send-off) | Q174, Q360, Q420, Q972 | **owner**, high |
| 「食う、寝る、呼吸する」 | ~12, incl. the last three cells of the arc where it is redefined | Q255 | open, high — fix one phrasing, never vary |
| 「あの口、食うためだけにあるんだな」 / 「食うことしか能のない口」 / 「赤ん坊以下」 | ~10 across fifteen years, ending in a Nobel speech | Q256 | open |
| 「新しい世界」 | ~20 (the dream, the roof, the waking, the closing essay) | Q339 | open, high — one fixed rendering |
| THE RULE: 「登場人物たちの幸せな結末を見届けること」 + 「真相を知る意思はルールに反します」 | 2 printings; the frame rule of the whole work | Q684 | open, high — a rule with a penalty implied and never stated; IDENTICAL in both places |
| navigator handover 「…編では知り得なかった、より深き彼らの業をご覧ください」 | 2+, only the 編 name changes | Q716 | open, high — one fixed EN sentence with one variable slot |
| 「大地に還ってもらう」 | 2 (fifteen soldiers; a friend) | Q667 | open, medium — euphemism over accuracy |
| 「私、／ものっっっっすごく／暇なんで！」 | 4, three cells each, っ count 4/6/6/5 | Q842 | open, medium |
| 「作戦成功」 / 五島's 作戦 gag | SEVEN forms; dies twice, returns at a climax | Q020, Q057, Q127, Q480, Q626 | open |
| 「肉付きの面」 / 鬼女 / 姑 | 4 uses in one file | Q322 | open, high — fixed EN for all three terms |
| 「ん……」 opener | ~every spoken line of 新村茅萱, 200+ files, incl. a branch where she has met no one | Q138, Q261, Q569, Q983 | open |
| 「うぎゅ……」 | ~40 across orders 61-65; named as a 口癖, banned as a game, broken, still used later | Q114 | open (GLOSSARY: "Uugh") |
| 「起」「承」「転」「結」 in 『』 | ~40 across two files | Q166 | open |
| 「サード・ジェネレーション」 vs 「第三世代」 | ~14; katakana in one mouth, kanji in everyone else's, same referent | Q289 | open |
| 「五感をジャック」 / 「五感ジャック」 | ~15 across four files | Q516 | open |
| ネクロ (coined on screen from ネクロマンサー) | ~60 across five files | Q493 | open |
| 盗感 (coined on screen WITH the excuse for coining it) | ~25, three characters, three files | Q540 | **owner-blocking**, medium (sense-theft / senselifting / percept-theft) |
| 五島's credo 「必ずそこには因果律が存在するはずだ」 | 2 near-identical statements (00001C5D:19:46-53, 00002450:12:72-75) | — | fix one EN wording and reuse verbatim; keep it DISTINCT from 新村桔梗's 「あらゆるものには因果律が存在する」 |
| 新村栄一郎's 「家族になる」 | repeated | — | the SAME EN words every time; NEVER "get married". The words are fixed, the inflection is not: "become a family" is "became a family" in a past-tense sentence (rev. 2026-09-25, rules audit #11) |
| 五島桃子's 「青から赤へ、冷から熱へ」 / 「赤から青へ、熱から冷へ」 | 2, inverted | Q913 | both halves use the same four English words |

## B4. Tense, aspect and grammar rules (GLOBAL B§3.7)

- NARRATIVE TENSE (STYLE 09-25, Q1087, project-wide; rev. 2026-09-25, rules audit #5 — the old
  EVENT/INTERIOR sort was not decidable per cell and put aches and worries in the present inside past boxes).
  Per narration cell: (a) put "I thought:" in front of it — if it still reads as the narrator's words at that
  moment (a judgment, a resolution, a ～のだ explanation, a question to herself, 分かっている, しかいない),
  PRESENT is allowed, as unquoted thought; (b) anything PERCEIVED or the case at the story moment is PAST
  whatever the JP tense — sensations and aches, the room, the weather, who is asleep, the boxes still standing,
  a worry about the night; (c) a fact still true at the moment of telling and stated as general (ages, kinship,
  a standing rule) may be PRESENT. At most ONE flip per text box unless the JP itself flips function. Do not
  follow the JP tense cell by cell; do not put a whole block in the historical present. Exception: a block the
  source sets wholly in the present as a device (a dream, a running commentary) stays present and gets a
  DECISIONS row. The rows below are the tense cases that carry PLOT; a reviewer treats tense as an error where
  one of them applies or where the English breaks the test above.
- 死んでいる vs 死んだ (00000ADE:11:82-97, 11:161-164): "is dead" must sound like a statement about a body in
  front of the speaker, not about a past event; 確かに must sound like the first half of "certainly..., but".
  Both passages word-identical (Q168, high).
- A contextually wrong 「でも」 (00001477:8:111-131, 8:158): keep "but" in the SAME position; the narration
  names it (「逆接を用いるべき会話ではないはず」) and reconstructs the deleted middle from it (Q578, high).
- A negation pair (00000DB9:11:104-105): byte-identical EN except "innocent" / "not innocent" (Q208, high).
- Five sentences identical but for the crime and the interval, the fifth inverted on 消えて『いなかった』
  (00000DA1:11:175-181): five byte-identical EN sentences varying only in the named crime and the year
  count, with the negation inside single quotes (Q201, high).
- A sentence split so the first half states and the second withdraws (00000E19:11:43-44), the second cell
  opening on a bare 「のかどうか」: "—she doesn't look like she's thinking anything in particular... / Or does
  she. I can't tell." (Q227, medium).
- One verb three times, twice as a quoted phrase and once as the sentence's own verb (000014BC:8:107-108,
  『何かが引っ掛かる』の逆で、『何も引っ掛からない』から引っ掛かるのだ): find one EN verb that works both ways,
  keep the single quotes on the two quoted forms (Q587, medium).
- One adverb in four spellings across four cells (0000241B:11:28-31): four cells of the SAME English word
  with rising punctuation, plus a TN (Q903, high).
- 「知らない」 chosen over 「覚えていない」/「忘れた」 with the narration flagging the choice
  (0000246E:11:323-333): keep the chosen verb (Q969).
- A question punctuated as a question and read by everyone as a confession (000014EE:16:324): keep the
  question mark (Q639).
- A hint built from a deleted subject, predicate and modifier, the three categories named on screen:
  **Q577, owner-blocking** — Japanese stays grammatical with all three gone, English does not.
- Honorific-target error as characterisation: 尊敬語 applied to one's own side, flagged as 「妙な敬語」 (Q136);
  「美冬、金井さん！」 with the narration 「名と姓を逆に呼ばれ」 (Q117). Keep the error.
- Pronoun switches: 僕 → 俺 for exactly fourteen cells while a drug is active, back with no comment (Q447);
  僕 twice and 俺 three cells later in one conversation (Q995). Translate plainly and add a [TN:] at the
  line; never re-encode a pronoun by warping English grammar (STYLE).

Wordplay and homophone hazards (GLOBAL B§3.8) are NOT repeated here: every row is an owner item and
appears in C2/C3 with its file:line.

---

# C. OWNER DECISIONS AND FABLE RULINGS

## C1. Fable rulings already in force (STYLE.md tail, 2026-09-25; provisional and reversible, owner may overrule)

- QUOTE WRAPPERS (settles Q036/Q071/Q079): 「」 → straight `"..."`; source straight `"..."` (text nobody
  present is speaking) → curly `“...”`; 『』 → `'...'`; bare unquoted cells stay bare, no wrapper added.
- 「――」 PREFIX AND ――-ONLY CELLS (settles Q709 and the five-jobs problem): render as `―` (U+2015) in every
  job, at the JP's position. A ――-only cell stays a lone `―`. Never a speaker label.
- DIALECT (settles Q611/Q785/Q843/Q070/Q149/Q074 at policy level): never an English regional or class
  dialect, never eye-dialect, never "Engrish"; rhythm + word choice + contraction rate + fixed tags, plus
  ONE TN at the first dialect line. A dialect named in narration but not written into the lines stays that
  way (Q843). ～アル = plain English + TN. ～ざます／～ですわ = over-formal English, no contractions — the GLOBAL
  3.9 best guess "my dear" / "positively" is SUPERSEDED (additive words). TEST for any candidate word or
  spelling (rev. 2026-09-25, rules audit #13): could a reader place it on a map or in a class of English
  speakers? Then it is banned — "Oi", "Yo", "eh", "y'all", "innit", "my dear", "aye", "lass". Tags are
  pre-listed per speaker in CAST; a tag not on the list is not used. Allowed contractions project-wide: gonna,
  wanna, gotta, c'mon, dunno, 'cause. Banned spellings: ya, yer, nothin', dropped -g, wot.
- CALENDAR (settles Q943/Q827 provisionally): dates stay as written; era name romanised ("Shiyo 805,
  August 1"); Gregorian captions stay Gregorian; no conversion, no TN equating them.
- MOJIBAKE CELLS (Q872): translate the decoded intended Japanese; log as typo.
- RUBY-RESIDUE SPACING: drop the stray spaces; translate the word normally.
- NARRATIVE TENSE (Q1087; rev. 2026-09-25, rules audit #5): decided per cell by the "I thought:" test —
  thought may be present, anything perceived or the case at that moment is past, one flip per box. See §B4.
- CELL-SPLIT WORDS (Q1084): same cell count, one or two letters per cell; log the choice in DECISIONS.
- SYLLABLE-SPLIT UNFINISHED WORDS (Q1123): romanise mora by mora, one TN on the first cell, the EN must not
  resolve into a word.
- TN IN ROUTE VARIANTS (Q1126): the same TN in EVERY variant that has the line; "first occurrence" counts
  per route, not per file.
- CHARACTER SET / FONT: CP932 only, ASCII plus `“ ” ‘ ’ … ― − ～`; no macrons, no em dash, no accented
  letters; Latin is half-width; message boxes switch to ＭＳ Ｐ明朝; no italics, no bold.
- SOURCE TYPOS (Fable, 2026-09-24): translate the intended text, never reproduce the typo, log status=typo.
- GLOSSARY rulings 09-25, every interjection row locked PER FUNCTION and not per string (rev. 2026-09-25,
  rules audit #2: these are homograph sets, one spelling doing several jobs, and a ruling made from one file
  locks only the job seen in that file; the test and the tells are in STYLE.md, the tell per row is in the
  GLOSSARY note column): よろしくお願い申し上げます = "I am in your hands." (Q1042); おい = "Hey", the
  attention-getter, never "Oi" (Q1080); よう = "Hey", a rough attention-getter — "Yo" is BANNED as a placeable
  English register (rev. 2026-09-25, rules audit #13), and the roughness is carried by what follows and by the
  punctuation; あの = "Uh" hesitating before addressing someone, えっと stays "Um" (Q1081); いや = "No" as a
  self-correcting opener, never "Or rather" (Q1082); やあ = "Hi" on meeting (Q1085); そうだね = "You're right..."
  where it ANSWERS a stated opinion (Q1086) — musing そうだね with nothing to agree to is "Yeah..." / "I guess",
  and that is a second function, not a violation; 事件 = "the incident", 「あの事件」 = "that incident" (Q1089);
  ドローガ = "Droga", read aloud D / r / o / ga in four cells (Q1083/Q004).

## C2. Owner-BLOCKING (33) — the file is NOT drafted until the orchestrator answers

An agent who hits one of these lines stops and asks. Best guesses are in GLOBAL B§2a; they are not decisions.

| id | file:line | what is blocked |
|---|---|---|
| Q368 | 00000F0D [26][68][74] | a minor's repeated advances to an adult officer, and his refusals: handling |
| Q378 | 00000F24:64:89 | romanising ヴェルジ／ブルーシャ／セレジェイラ |
| Q384 | 00000F24:100:184 | generation tables typeset two ways in one scene |
| Q418 | 0000107B:11:214 | 荒田 chosen over 天田; the kanji pun is the point |
| Q419 | 0000107B:11:50 | 姫 in 糸姫 is GRANTED on screen; does 姫 join the preserved-suffix list |
| Q421 | 00001092, 000010AA, 000010C3 | three files retell a famous succession with every name shifted; TN wording |
| Q450 | 000010DD:11:120 | the Western doctor's original name セレ |
| Q494 | 00001214:8:128 | × runs for illegible characters, reprinted verbatim later |
| Q495 | 00001214:8:147 | 『死月妖花』 spoken in-world as an organism's name |
| Q497 | 000012AD:16:0 | two spoken cells reprinted as a bare full-width KATAKANA block |
| Q536 | 00001355:8:92 / 000013FD:8:196 | a five-line classical instruction, later recited with one contraction |
| Q540 | 00001355:8:252 | 盗感, coined on screen with its excuse, then used ~25 times |
| Q547 | 00001385:8:65; 000013B5:8:96 | 五島's "doubt everything" rule quoted from memory twice |
| Q555 | 000013CD:8:357 | dying speech printed with full-width gaps for what she stops hearing |
| Q567 | 00001414:8:210; 000014D7:8:239, 8:377 | one transmission printed four times in three typographic systems |
| Q577 | 00001477:8:100 | hints with subject, predicate and modifier deleted, the categories named on screen |
| Q597 | 000014D7:8:457 vs 0000107B:11:50 | the antagonist names herself 糸姫; render identically in both files |
| Q603 | 00001505, 0000151C | one sentence printed ~20x with the gaps at DIFFERENT positions |
| Q611 | 00001533 | sustained 関西弁; STYLE now has the policy, the rendering is still open |
| Q647 | 0000156A:14:30 | one massacre called both ナナシナ事件 and 747年事件 in one speech |
| Q682 | 000015C2:81:2 | the reading of 立木三日 |
| Q683 | 000015C2:8:0; 0000198D:111:1 | player-name variable injected BETWEEN cells; the honorific starts the next cell |
| Q709 | 00001818 etc. | the 「――」 ordinary-secondary-speaker job — CLOSED by STYLE 09-25: keep 「―」 |
| Q721 | 0000189A:1125:0; 0000191C:11:116; 000019DD:377:1 | three layout objects of spaces, indents and ⏎ padding |
| Q735 | 00001A6B:8:5 | a whole block in full-width KATAKANA (a burnt mouth) |
| Q763 | 00001CA0 | the navigator IS 新村春花; keep the two registers exactly as printed |
| Q766 | 00001EA4, 00001EB4, 00001EC0 | the navigator's cells acquire 「」; carry the change into EN |
| Q785 | 0000200D | two grandparents in sustained northern dialect |
| Q827 | 000021BD:8:5 vs 21:5 | one covering note dated 祀耀735年 in one block and 1942年 in the other |
| Q843 | 000021A5:8:58 | a liar caught by an accent his lines never show |
| Q873 | 00002268 | the file is the AUTHOR'S AFTERWORD, not story text |
| Q874 | 00002268:8:26 | 死月妖花 stated to be an IME misconversion of 四月八日; the EN title |
| Q943 | 00002450:12:250 | a Gregorian caption in a project that dates in 祀耀 |

## C3. Owner, non-blocking (40) — translate around them and file the query

| id | file:line | what is open |
|---|---|---|
| Q160 | 00000A18:11:72 | 詩林館／死隣館, a homophone that IS the ghost story's mechanism and title |
| Q174 | 00000A30:11:103 etc. | the settlement motto, said 8+ times, one fixed EN wording needed |
| Q176 | 00000BD6:11:46; 00000C68:11:101 | dakuten on every kana, and on a bare ん |
| Q182 | 00000BB7:11:119 | 「だ／い／す／き」 one kana per cell, a dying child |
| Q205 | 00000DD1:11:43 | 般若 mask joke plus 顔面偏差値 |
| Q217 | 00000E31/00000E49/00000E61 | お姉ちゃん vs お姉さん as two different words; the payoff forbids merging |
| Q247 | 00000E95:11:39 | the 戦闘民族 gag: literal and flat, or off-doctrine and funny |
| Q258 | 00000EAF:22:73 | 『食祝』, whose reading the narrator guesses and moves on |
| Q273 | 00000EAF:22:138 | on-screen unit conversions the file then reasons with for 2,000 lines |
| Q292 | 00000EDF:37:239 | four invented chest onomatopoeia on a scale, two glossed on screen |
| Q296 | 00000EDF:192:79 | the 0723 lock (na-tsu-mi = 7-2-3); the number recurs and cannot change |
| Q329 | 00000EF6:26:58 | 麻黄 glossed on screen by spelling out its two characters |
| Q330 | 00000EF6:110:197 | the セクハラ無料券 routine: tone |
| Q353 | 00000F0D:8:131 | the alias 古村秋菜 built from 新村夏菜 (新→古, 夏→秋), explained on screen |
| Q354 | 00000F0D:26:170 | the withheld name stated to be 「2文字の言葉」 |
| Q360 | 00000F0D:14:200 etc. | the motto again, in a sentence that ATTACKS it |
| Q393 | 00000F24:94:180 | ミイラ取りがミイラになる, said while planning to steal a mummy |
| Q412 | 0000104E:11:38 | laughter as a layout object: 13 one-「は」 cells then ~200 per cell |
| Q467 | 000011B4:8:100 | the 5W1H key in Latin script with ruby residue inside "How" |
| Q470 | 0000119C:8:86 | 漱石枕流 used about someone else's kindness |
| Q479 | 0000116C:8:75 | 御令姪, 最上級敬語 for another person's niece |
| Q502 | 000012F5:8:0 | 暗証番号 0723（なつみ）, named on screen as 語呂合わせ |
| Q505 | 000011FA:8:6 | 『喪』 and 『忌』 named as written characters, not used as words |
| Q527 | 00001325:8:200 | three 「キエエエ……！！」 cells, the first ~80 characters; must match Q412 |
| Q528 | 00001325:8:145 | a name-reading gag (大翔 = ひろと) plus a comeback about her own name |
| Q579 | 00001477:8:133 | a reconstruction printed twice with 「（ここに何かが入る）。」 as a placeholder |
| Q585 | 000014A5:8:145 | 大船に乗ったつもり answered by 「くつろげるか！」 |
| Q606 | 00001505:8:89 | ニイ様 built from the first mora of 新村 and misheard as 兄様 |
| Q612 | 00001533:8:178 | a ボケ／ツッコミ routine where 「なんでやねん！」 is the correct response |
| Q633 | 00001505:8:363 | an attempted-assault scene: translate plainly, neither warm nor cool it |
| Q649 | 0000156A:34:70 | 天衣無縫 cited, then its literal "seamless robe" sense drives the deduction |
| Q650 | 0000156A:76:83 | a birthday typed BACKWARDS, eight digits, one per cell |
| Q705 | 00001800:8:4 | ホシ and マルタイ, police 隠語 used 8x and never glossed |
| Q732 | 00001A65:8:13 | 父なし corrected to 乳なし, one kana apart |
| Q745 | 00001AAE:8:28 | a JP proverb glossed by "Easy come, easy go." inside the cell |
| Q769 | 00001FE4 | the whole file is one cell holding a single full-width space |
| Q776 | 00001BB4:8:36; 00001BCE:8:53 | a child echoes 疑心暗鬼 in katakana because she cannot parse it |
| Q779 | 00002026:8:62 | a succession scene turning into a magical-girl chat two cells after a suicide instruction |
| Q789 | 00001D17:12:0 | 『おひめの歌』 as a layout object: verses, refrain, internal full-width gaps |
| Q832 | 000020FC:8:43; 00002108:8:59 | ハナちゃん's sex; the key word is × in the source |

## C4. Resolved rows that change an EARLIER file's rendering (GLOBAL B§5)

The fence still applies: the translator knows the answer and must NOT write it into the earlier file.

| id | resolution, and what it changes |
|---|---|
| Q003 | the "posted overseas three years ago" account is a LIE told by the character herself (resolved 000004E3:27:117, 00000550:11:42, 000005AC:11:78). The earlier EN must sound like a lie told smoothly, not like exposition, and must not foreclose the truth. |
| Q006 | the menu navigator gets a CAST block: a character voice held consistent across ~25 files, not UI boilerplate. |
| Q016 | the dream figure's sex is unknowable in 000001E1:33:10 – 000001E5:23:26 and resolved at 00000641:11:25 as male. The earlier span's constraint is UNCHANGED: he must not be gendered before 000001E5:23:26. |
| Q035 | 「伊勢さん」 = 元木警察署警部補 伊勢大二郎; fixes the rank vocabulary (警部補／巡査部長／警部補殿, Q055) from the first mention. |
| Q051 | 荒田集落 is a place in the story present (荒田地区／通称荒田集落, in 飯沢県). The reading あらた is UNCONFIRMED and the kanji pun is owner-blocking (Q418). |
| Q105 | school years fixed: 春花 > なつみ > 五島, one year apart each. Fix the "one year older" wording everywhere; complicated later by 「18年間」 (Q113). |
| Q153 | the head scar: she took the injury shielding the other girl ten years ago and SHE STILL DOES NOT REMEMBER IT. The amnesia stays as written — do not add a single connecting word. |
| Q155 | 『モトキザクラ様』 keeps the 様: "Motoki-zakura-sama"; later given an invented origin in an occult magazine (Q648). |
| Q216 | the adoption is real and narrated on screen by both parents. Fixed EN: "Haruka-chan is adopted. She's really a daughter of the Kogori house — Natsumi-chan's real older sister." Whether she is adopted INTO the house or returning to it is still open; affects Q246, Q410, Q217. |
| Q460 | she NEVER injected herself (resolved 000014D7:8:256). 000010F5 must be translated as WHAT SHE BELIEVED SHE WAS DOING — no hedge, no irony, and do not make the link the next file refuses to make. |
| Q461 | the five confessed murders are PLANTED VISIONS (000014D7:8:270). Translate flat, no dramatic diction. |
| Q462 | the forensic contradiction nine cells later STANDS, because she never did it. Keep the one-cell block alone with nothing added. |


## C5. Open, and blocking a file until the orchestrator picks: four readings where GLOSSARY and CAST.md DISAGREE (GLOBAL C§4.0)

| kanji | GLOSSARY.tsv | CAST.md | note |
|---|---|---|---|
| 城崎 (健吾) | しろざき / Kengo Shirozaki ("per cast list") | — | a major speaker from 00000B27 on |
| 城崎 (百合子) | きざき / Yuriko Kizaki (00001154:8:18) | きざき, Yuriko Kizaki | SAME surname, different reading from her husband's; one is wrong |
| 後白河糸織 | ごしらかわ いおり / Iori Goshirakawa | ごしらかわ いとおり / Itoori Goshirakawa | 糸織 is built on 糸 (糸姫), which favours いとおり |
| 新村晃 | にいむら こう / Ko Niimura (unconfirmed, Q595) | にいむら あきら / Akira Niimura | present in all 24 files of orders 366-389 |

---

# D. CAST VOICE DIGEST

Per speaker: pronoun + speech level + profanity ceiling · fixed tics with their fixed EN · address forms ·
the one thing NOT to do · the file ids where the voice CHANGES (grep GLOBAL A§1 with the id for what each
one does). No plot. Long versions: GLOBAL A§1 (principals, second-frame blocks), A§2 (minor speakers);
who-calls-whom-what via notes/GLOBAL-RELATIONS.md, `cast_select.sh`, `relations_select.sh`.

## D1. Principals

### 古郡なつみ — Natsumi Kogori (as-of 00002478; top narrator, 16, 2年生)
- 私 in narration AND dialogue, no switch, ABOVE-typical frequency — do NOT delete the English "I". だ／だよ; です only to strangers and 伊勢. タメ口 to 春花／五島／her mother; 敬語 to adults, unbroken with 伊勢 from 00000538, overridden only BY GRANT 3x and corrected mid-cell (Q136, Q499). ～よね／～かな／～でしょ／～ってば; ～だろ／～ぞ NEVER. Profanity ZERO in 39 files.
- Tics (fixed EN): 「はあ……」 "Haah" written out, asterisked stage directions BANNED; 「あは！」 "Heh"; 「ふふ」 "Hee"; 「うん……」 stalling yes; 「さーねー！」 "Who knows"; trailing ellipsis on nearly every hesitation. Addresses: 春花 bare, 五島 bare (she was the first ever to do it), おばさん for 美冬, 伊勢さん; 五島 calls her 古郡先輩.
- MUST NOT: cool, italicise or make eerie the CONVERTED register — warmth, 「ふふ」 and ～でしょ intact while aimed at killing, the tells content and physical only (Q396, Q857); keep every hedge on her 直感. Ids: 00000538 · 000004E3:27 · 000005C1 · 00000600 · 000006E0 · 000006F9 · 000009FE · 00000E31 · ... (full list in GLOBAL A§1)

### 新村春花 — Haruka Niimura (as-of 00002478; second narrator, 17, 3年1組, the OLDER of the two -> Q105)
- 私 in narration AND dialogue despite masculine-blunt speech — deliberate, not an error (Q026); never 俺/僕/あたし, kept while dying. だ. タメ口, boyish, NO 敬語 to anyone including a 警部補, with three visible-shift exceptions (00000B3F:11:34, 00000E7B:88:192, 00001A52/00001A5C) — never meek. ～ぞ／～だろ／～のかよ／～だぜ; ～わ once as rough-emphatic and NOT feminine. CEILING くそ "Damn", nothing stronger anywhere (Q225).
- Tics (fixed EN): 「よう！　調子はどうだ？」 her FIXED greeting (よう = "Hey", locked Q1080, en revised by rules audit #13; "Yo" is banned); 「おいおい……」 "Hey now"; 「ほれ！」 "Here"; 「じゃな」 "See ya"; 「バカかよ」; 「ははは」 = her HOLLOW laugh, not cheerful, distinct from 「あはは」. Addresses: なつみ bare, 五島 bare, おばさん／母さん, チガ姉 from age six.
- MUST NOT: hedge or cool the CONVERTED／神使 register (warm, ordinary, apologetic, grammar unchanged, Q396, Q667); add NO remorse words in autobiography mode, where she reports her own murders like the weather; keep her comic geography wrong in exactly the same way (Q069). Ids: 000002FA:11 · 0000034C · 00000366 · 000004E3:11 · 000004E3:27 · 000005AC:11 · 0000050E:11 · 00000682 · ... (full list in GLOBAL A§1)

### 五島絵梨奈 — Erina Goto (as-of 00002478; third narrator, 15, 1年生; the most layered voice here)
- 私 plus NAME-AS-PRONOUN in the third person by surname ("五島は真摯に受け止めます！"), comic and deliberate. です in dialogue and 独り言, だ／である in narration. 敬語 to BOTH 先輩, 伊勢, 古郡茜 and adults, UNBROKEN — and NOT deference: at four she already speaks unbroken です・ます to a stranger. Exceptions: her sister gets NONE ever; the ～っす slip, four causes, never rudeness (Q094); the killing-urge register drops it. ～ですなあ／～ですぜ／～でゲスよ／～であります／～ですよね. Profanity ZERO, two breaches.
- THE 敬語 AS A WEAPON is the key to her English: flat imperatives to a 先輩, accusations to adults, an interrogation the narration calls 「異常なまでに威圧的」, an order to a 警部補 — and NOT ONE WORD leaves です・ます. EN needs a formal register that can be MENACING.
- Tics (fixed EN): 「えへへ」 "Ehehe"; 「ほい？」 "Yep?"; 「ふむ」 "Hmm" (ふむーん／ふーむ = the same sound stretched); 「ちっ」 "Tch", must read as a tongue click; 「ぐす」 "sniff" written out. Fixed: the 作戦 gag, EIGHT forms, its RETURN is a signal (Q020); the ニカッと grin, MANUFACTURED, used to deliver lies (Q058); her credo 「必ずそこには因果律が存在するはずだ」, one wording, distinct from 桔梗's; 「Que droga」 verbatim (Q178). Addresses: 古郡先輩／新村先輩 even in her own head at 33 (Q034); bare 「先輩」 only when frightened, never for 古郡.
- MUST NOT: level the SPLIT vocabulary (schoolgirl-bright over precise technical, rising file by file); cut a hedge (she disclaims her biggest deduction four times and is right every time, Q381); merge the SIX branch-answers to the 呼び捨て wound (Q037, Q171, Q291, Q561); or quotation-mark her into speaking in 00000EAF, where she is mute and every utterance is written (Q254). Ids: 000002F6 · 0000037D · 00000522 · 00000BD6:11 · 00000EAF · 00000EDF:65 · 00000F6F:11 · 0000156A (Q177 Q219). Three comic tiers switch ON/OFF BY BRANCH: ゲス／旦那／御意, the 小生 tier, the childish 「ばあー！」 layer.

### 古郡良治 — Ryoji Kogori (as-of 00002444; なつみ's father; first male 俺 narrator, orders 66-74)
- 俺, typical. だ. ～からな／～ぞ／～さ, ～てくれ in the letter. Tics: 「はは！」; 「何、～さ」 brush-off. Ceiling くそ／ちくしょう and it holds while he dies. Addresses FIXED 祀耀788-800: 茜 bare, お前 for wife and junior, 栄一郎 bare, 美冬さん (さん kept even while he fears her), 春花ちゃん, なつみ bare.
- Two registers with fixed shapes: the LETTER (00000564:11:97-120) — terse, one clause of reasoning per line, no softeners, never says he is afraid, sign-off is all of 「頼むぞ。」, frame 「できるだけ、普段通りに」; the VOICELESS (00000641:11:32-60) — no consonants, his daughter's name takes three cells, breath as 「ヒィ、ヒィ」, THE OBJECT LANDS LAST in both messages, and WARM not frightening (Q085).
- MUST NOT: supply what he saw (0000082F:11:154 — second person, unfinished, then only the child in his arms); resolve his retracted moral position (00000CB3:11:46); gloss 「例の件」 or 「美冬さんの正体」; or give him a final sentence he lacks — his dying lines are imperatives about other people and he never begs. Ids: 00000564:11 · 00000641:11 · 0000085D · 000008B9 · 000008D0 · 00000CB3 · 00000CE3 · 00000F40 · ... (full list in GLOBAL A§1)

### 古郡茜 — Akane Kogori (as-of 00002444; なつみ's mother, late 30s/early 40s — NOT elderly)
- 私, LESS often than typical, subjects dropped heavily. だ／よ, feminine. タメ口, maternal-feminine; ～わよ／～わね, ～なさい, ～でしょ, ～のよ. Profanity ZERO.
- Tics (fixed EN): 「ほらほら」; 「ごめんごめん！」; chirpy apology-then-order; 「あんたねえ……」 at 美冬 for twenty years; THE LAUGH 「ブフッ」 "Pfft" (ブフフ／ブフホッ／ブフフフホッ = ONE syllable lengthened the same way each time, only in front of 美冬); the SPELT-OUT IMPERATIVE 「ちゃ・／ん・／と、／ご検討ください！／以上！」, shared with 五島 (Q115). ADDRESSES ARE HER FINGERPRINT and never move: 「良治君」 (the project's only spousal form), bare 「美冬」, 「春花ちゃん」, 「五島ちゃん」, 「なつみ」 bare, corrected to 「お父さん」 at 00000641:11:122.
- MUST NOT: make her cold-blooded — the FLAT COMPETENCE is her ordinary maternal register applied to a murder, nothing in the voice changes, and it fails exactly once (00002444:26:181, Q938); do not reorder her questions at 00000522:11:91 (the order IS the clue) or finish her unfinished sentences; while MASKED she says NOTHING, so give her no sound. Ids: 00000522:11 · 00000641:11 · 000007BC · 00000818 · 00001477:8 · 00001A97 · 0000156A · 0000241B · ... (full list in GLOBAL A§1)

### 新村美冬 — Mifuyu Niimura (as-of 00002444; 春花's mother, over 40)
- NAME RULE, hard: confirmed in the text at 0000037D:11:58 — before that line she is おばさん／春花のお母さん and EN MUST NOT use "Mifuyu"; in orders 61-65 she is 金井美冬 and 新村 must not appear before 00000801:8:120 (Q110).
- 私, typical. よ／わ, feminine. Profanity ZERO. She NEVER asks a direct question; hers is always 「本当に……本当に楽しいの？」. Named trait 極端; THE LOOK 「怖いくらいの目つき」. Addresses: 春花 bare, なつみちゃん, 茜 bare, 栄一郎さん (です・ます always), サクラさん, お義母さん, 五島ちゃん.
- SIX states of ONE voice, the largest voice job in the project (Q106, Q114). ZERO: whining, dependent, NO elongated ー, 口癖 「うぎゅ……」 "Uugh" ~40x. 1: a drawn-out ー！ on nearly every sentence, 「おーっほっほっほ！」, run-ons — an OVER-CORRECTION acquired on screen at 00001AC1:8:1-39; EN = a 40-year-old over-performing youth ("soooo", "reeeally"), register 1 ONLY. 2: every ー and ！ gone, short level plain form — a reveal at 00000564:11:179 but ALSO just how she sounds after 000008A2 and for four straight files, so do NOT treat every occurrence as a mask. Plus QUIET-WARM, STORYTELLER, and 1-AS-A-TOOL, where the volume stays UP while the content turns.
- MUST NOT: coarsen or raise the KILLING REGISTER (000008D0:33, 00000CFA) — ～わ／～かしら／～のよ and every address form intact, only her usual laugh (Q130); fill her deliberate blanks; or miss THE EARLY BLEED at 00000697:8:195-201, three cells inside the loud register with every marker gone — strip the elongation and exclamation marks for exactly those cells and nowhere else in the file (Q106). Ids: 000001DD · 0000037D · 00000564:11 · 00000697:8 · 000008A2 · 000008D0 · 000009E6 · 00000CFA · ... (full list in GLOBAL A§1)

### 五島桃子 — Momoko Goto (as-of 00002450; 絵梨奈's elder sister, 20; 24 in one branch)
- 私, typical. だ. Tic 「ったく」 "Honestly" (clipped まったく). Profanity ZERO with exactly TWO breaks, both triggered by an insult to her sister (00001807:8:62, 0000242E:11:116).
- FOUR registers switched instantly and on purpose: TO HER SISTER blunt clipped タメ口 bordering on hostile, statements ending ～し, deflection instead of answers, 「あんた」; TO A GUEST full 敬語 in a bright hostess voice, switched inside one cell; PROFESSIONAL (000005C1:11:26 — わたくし／～でございます／「五島様」 to her own sister), SURFACE-IDENTICAL to the navigator and the プリマベラ staff and the three must NOT sound alike (Q075); SECOND-PERSON ESSAY (00000E7B:11:21-155, です・ます to 「あなた」 the reader, an English digression glossed in the next cell, Q230, Q231).
- MUST NOT: warm the wording — the pattern, recorded ELEVEN times, is ROUGH WORDS, PROTECTIVE ERRAND and the warmth is in the fact that she came; where she substitutes something for affection it must not read as coldness (Q298, Q299); do not import the roughness into her narration, where the あんた register never appears in 2,637 lines, and let her UNEXPECTEDLY EDUCATED vocabulary stand (Q745). 「あんた」 vs 「絵梨奈」 has SEVEN branch handlings, each distinct in EN (Q037, Q291); THE TUMOUR figure stays MEDICAL with no vocabulary variation, and 「青から赤へ、冷から熱へ」 and its inversion use the same four English words (Q913). Ids: 000005C1:11 · 00000E7B:11 · 00000EDF:37 · 00000F87 · 00001807 · 0000242E (Q232 Q707)

### 伊勢大二郎 — Daijiro Ise (as-of 00002450; 警部補 at 元木警察署)
- PRONOUN IS A TELL: 私 is the uniform, 俺 is the man — 私 announcing himself, through a locked door, on the phone to a stranger, in the briefing; 俺 with the three girls, with a subordinate, and in all 265 cells of his narration; 俺 dominant from 000004BB; the switch visible at 00001830:8:40-41. ～のだ／～のである in the rant, ～てくれ, ～かな. Ceiling "damn".
- Tics (fixed EN): 「くそ……」 "Damn", 「ちくしょうーー！！」 "Dammit"; 「ごほん……」 "Ahem"; 「うむむ……」; 「いかにも！」; 「ぐっふふふ」 "Gguhuhuhu". Addresses: 古郡さん／新村さん／五島さん in writing; 君 for 夏菜 for a whole file, every one load-bearing (Q354). SIX registers: BRIEFING (bureaucratic です・ます, numbered, NO contractions) · COMMAND (barked, 「おい！」) · FLUSTERED (a stammer DOUBLING THE FIRST SYLLABLE of specific words including his own surname and rank; stutter on the SAME words, not generically, and reproduce a word broken across three cells, Q352) · GENTLE (mumbling, hedging, unfinished) · WRITTEN (terse plain-form, no softeners, no rank) · WORKING-THROUGH (00002450:18, where he calls his own hypothesis 妄想 five times while being right — keep every hedge).
- MUST NOT: let the comic surface reach his narration (00000F0D:56, 265 cells in 俺, no rant and no stammer; not lyrical, not hard-boiled, Q369); let the 元木美少女同好会 RANT make him a threat or eat his competence (Q048, Q049); or reconcile the file where he refuses to interrogate a runaway AND bugs the phone he lends her (Q350). Ids: 000004BB · 00000550:11 · 00000F0D:56 · 00001830:8 · 00002450:18

### navigator / 立木三日 — the menu voice (as-of 00002330; LATER asserted to be 新村春花)
- わたくし everywhere, 私 in her self-introduction and cracks. でございます, 最上級敬語. Contractions ZERO, formality maximal and unvarying, long nominalised sentences: hotel-concierge Japanese applied to mass murder. The player is always <name>様; the cast are always BARE FULL NAMES with no honorific — the only voice in the project that does that.
- Fix and reuse VERBATIM: 終焉, 分岐点, 編, 『もしも』の世界, the handover formula (Q716); THE RULE at 000015C2:61:16-28 restated at 0000198D:111:0-5, IDENTICAL wording (Q684); 「よろしくお願い申し上げます」 = "I am in your hands." (locked Q1042). Her cracks are her only characterisation before the reveal: ～ですわ 4x, 「あの…………」, 「ほほほほほ」, 「ふふ」.
- MUST NOT: vary the EN between menu files — THE HORROR IS THAT THE REGISTER NEVER MOVES; sound identical to 桃子's professional register (Q075); or seed 春花's mannerisms before 00001EB4:83:2 (Q763). Ids: 000000F2 · 000015C2:81 · 00001B47:60 · 00001C68 · 00001C7B · 00001C8C · 00001CA0:64 · 00001CA0:144 · ... (full list in GLOBAL A§1)

### 新村栄一郎 — Eiichiro Niimura (as-of 00002473; 春花's adoptive father, dead through the story present)
- 僕 ALWAYS, never 俺, stated more often than typical and almost always as the subject of a self-criticism; ONE switch anywhere, 僕 → 俺 for fourteen cells under the drug (000010DD:11:268), back with no comment (Q447). です・ます to 美冬 through the courtship AND after the marriage; タメ口 only to 良治 and サクラ. ～んです (his commonest, always on an apology or a self-assessment), ～かな. Profanity ZERO.
- THREE comic devices in the LIVING register, kept apart: the STAMMER doubles the first mora then mangles the vowel (「だだだだいじょうび……！」); the PANIC LISP turns consonants into small kana (「あにょ！」, 「ひゃめて下さい」); the SOB is a groan first (「う……／うう……」 → 「ぐす……」 → 「うぐ……ひっく……」). ALL THREE ABSENT at fourteen and fifteen — he ACQUIRED them. 「家族になる」 = the SAME EN words every time, NEVER "get married". Addresses unchanged across twelve years and one death: なつみちゃん, 美冬ちゃん, 良治 bare, サクラ bare, 母さん, 兄貴 for 幸太郎, and his own daughter is 春花 BARE — which is how she identifies him at 00002444:32:27.
- MUST NOT: hedge the identity in the posthumous ANTAGONIST mode (it is ASSERTED, not implied, Q390, Q570) or reach for his comic register there — level, unhurried, faintly amused plain form, mock-fatherly, THE CRUELTY ALL UNDERSTATEMENT, never louder and never swearing; in the GENTLE posthumous mode 僕 and 「はは」 survive while the stammer, lisp, ～んです and apologies are GONE; and the comedy about his body must never read as the narration mocking him. Ids: 000007D3 · 0000082F:11 · 000010DD · 00000E31 · 0000151C:8 · 00001C08 · 00001D6F:8 · 00000F24:142 · ... (full list in GLOBAL A§1)

### 新村茅萱 — Chigaya Niimura (as-of 00002478; 春花's cousin, ~25, a Tokyo student)
- 私, typical. よ／わ, feminine. SOFT FEMININE タメ口 to everyone including adults; she refuses to give or receive 敬語 (「私たち、先輩でも後輩でもないでしょ？」). ～のよ／～の (constant), ～わよ, ～ね on almost every line, ～かしら. Her ONE 敬語 is the written MEMO register (0000136D). Profanity ZERO IN WORDS, MEDIUM IN CONTENT — the whole EN problem with her.
- 「ん……」 OPENS NEARLY EVERY LINE SHE SPEAKS, in every register, from five to twenty-five, across ELEVEN branches, through a conversion and back; ABSENT from her narration, PRESENT in every spoken line including shouted, ceremonial, threatening and floor-muttered ones; often the ONLY proof of identity the text gives. FIX ONE EN RENDERING AND USE IT EVERYWHERE (Q138, Q091). ITS ABSENCE IS ALWAYS AN EVENT and there are four: 00000B9F:11:108, 「は？」 at 00001325:8:151, the collapse at 00001C5D:11:150, and the INTERIOR SCREAM (Q530, Q806, Q527). Other tics: 「うふふ」; 「んふ」 "Nfuh"; 「ダッセエ」 "Laaame" split across three cells. Addresses: 五島さん → 五島ちゃん inside single files, なつみちゃん, 春花ちゃん, お父さん; only ハナちゃん calls her 「茅萱」 bare.
- MUST NOT: cool the voice in the conversion or the threats — the tic, ～のよ／～わ and 五島ちゃん stay intact and only the content moves (Q569); make her one-sided physical habit with 五島 menacing OR cute; or give her any sound in 能面 and 赤装束, where she says NOTHING AT ALL. Ids: 00000944:8 · 00000A18:11 · 0000110D · 0000136D · 0000139D · 000014D7 · 00001C5D:11 · 00001EFF · ... (full list in GLOBAL A§1)

### 新村夏菜 — Kana Niimura (as-of 00002478; 茅萱's sister, 10-12; 14-16 in 00000E7B and 00000F0D)
- 私, typical. だ. OVER-FAMILIAR タメ口 with no distance at all, to adults and strangers alike, no 敬語. ～じゃん, ～し, stacked ～の！？, ～からね！. Contractions HIGH, formality ZERO. Profanity LOW-MEDIUM in a specific way: she is ten and says 「ロリ巨乳」, 「まな板」 and worse, and THE SHOCK IS THAT A CHILD SAYS THEM.
- Tics (fixed EN): 「ほーかほーか！」 "Zat so, zat so"; 「はにゃ」 "Hunh"; 「ばああ」; 「ぐへへへへ」; 「ほれほれ」; 「オッケー」 (hers only); a full-name self-introduction five times in five cells; fifteen questions in fifteen cells; she ECHOES the last words of other people's lines, one per cell (Q142); a STAMMER where the whole mora repeats and multiplies — embarrassment, never panic, and unlike 栄一郎's it does NOT mangle the vowel. Addresses: ちゃん on everyone she attacks — KEEP THE MISMATCH with the content; チガ姉; 「エリ姉」 coined on the spot in three branches, never in two, requested in one (Q171, Q498).
- MUST NOT: make her reasoning precocious-cute — IT IS IN A CHILD'S GRAMMAR AND IT IS NOT A CHILD'S REASONING (Q500); make her pitiable in THE QUIET REGISTER, where the lines are cheerful and only the narrator names the loneliness; or soften her です・ます in 00000E7B, which holds for 2,637 lines and CARRIES the horror. Ids: 0000095B:35 · 00000AF7:11 · 00000E7B:40 · 00000EDF:186 · 00000F0D · 00000F24:88 · 000012C5:8 · 0000148E:8 · ... (full list in GLOBAL A§1)

### 新村幸太郎 — Kotaro Niimura (as-of 00002478; 栄一郎's twin, 茅萱 and 夏菜's father)
- 俺, LESS often than typical, plus ONE unexplained 僕 at 0000095B:35:22 (his twin's only pronoun, never remarked on) and two at 0000246E. だ. Relaxed タメ口 to everyone; です・ます under interrogation later. ～じゃないか, ～だろ, ～よ. Profanity ZERO-PLUS-ONE. Addresses: 五島ちゃん, 春花ちゃん, なつみちゃん, 夏菜 bare, サクラ bare, 母さん; 兄貴 is 栄一郎's word for HIM.
- HIS LAUGH 「はっはっは！」 "Hah hah hah" is a structural fact: he laughs INSTEAD of intervening, every time; it must differ in EN from his smaller 「ははは」 and his mother's 「ほほほ」, and its ABSENCE marks every serious scene. Register drop: 「くっふふふ」 "Khu-hu-hu-hu". SIX registers: TEACHING (one question per turn, a pause, the answer named out loud, 起承転結, Q166) · DRUNK HOST (no laugh; volunteers the most damaging fact about himself, embarrassed not evasive, NOT sinister) · DOMESTIC (whining while patched up, his twin's self-abasement surfacing, Q117) · ANTAGONIST · NEGOTIATOR (telephone only, and four cells later the same call is warm — NEITHER IS A MASK) · WRITTEN (five bare cells, signature alone, Q593).
- MUST NOT: let him inherit 栄一郎's stammer, 僕 or apologies, or make the ANTAGONIST register loud — HE NEVER SAYS 殺す OR 死ね, never shouts, never threatens, states demands as offers, every diminutive intact through two nata swings. In the DOUBLE GAME the 00000E19 lines are reused WORD FOR WORD and both printings must be IDENTICAL (Q973). Ids: 0000095B · 00000AC4:11 · 00000AC4:19 · 00000B9F:11 · 00000E19:11 · 00000EDF:47 · 00000F0D · 000014D7:8 · ... (full list in GLOBAL A§1)

### 新村エリカ — Erika Niimura (as-of 00002478; 春花's grandmother, ~70-71, 荒田's 長 and 大魔女)
- 私 in her own voice; in an impression, the pronoun of whoever she is doing. だ. Unhurried plain タメ口／丁寧-casual, ～ね／～だね／～かね, one fact per sentence, and in her OWN voice NO JOKES AND NO TICS AT ALL — that absence is the point. Profanity MEDIUM ONLY INSIDE AN IMPRESSION. The one person she gives 敬語 is her own mother-in-law.
- Tics (fixed EN; ALL showman markers, ALL absent from her serious files): 「はっはっは！」 (shared with 幸太郎 — must be distinguishable); 「よっしゃ！」 "Right then"; 「おうおう！」 "Yeah yeah"; 「むふ」 "Mfuh"; 「ありゃ」 "Whoops"; 「はいよ」 "Here y'go". Addresses: なつみちゃん, 五島ちゃん — and she OFFERS her given name and BANS 敬語 branch after branch, handled differently every time (Q499, Q561) — 春花, 茅萱, 幸太郎 bare when ordering him about.
- MUST NOT: merge her FOUR voices — the IMPRESSIONS, each ONE NOTCH BROADER THAN THE ORIGINAL (as 春花 with ～な／～ぜ and 「クソして待ってな」, which the real 春花 never says, Q139, Q109); her own voice; the HOST voice; and the 大魔女 register (00000A94:11:129, retold 00001459:8:199), 丁寧 carrying the law and DROPPED inside two cells for 「まあ……／いいんじゃないかね！」, where THE DROP IS LOAD-BEARING and the EN halves must be AS FAR APART AS THE JP (Q575, Q576). Do not raise the voice in her defining move (she says the worst thing about herself flatly, then stops) and do not play her as a traditionalist: SHE IS A REFORMER and the enforcer of a fifty-year suicide policy, and NEITHER FILE ACKNOWLEDGES THE OTHER, so cite both (Q914, Q916). Her transmissions are FIXED QUOTED TEXT (Q558, Q567). Ids: 0000095B:11 · 000009A0:11 · 00000A94:11 · 00000FCF · 00001295:8 · 00001459:8 · 00002026 · 00002433 (Q146 Q428 Q777)

### 新村サクラ — Sakura Niimura (as-of 00002473; 幸太郎's wife, dead ten years)
- 私, LESS often than typical — she drops subjects and speaks about the other person instead. よ／わ, feminine. Soft feminine タメ口 to EVERYONE including a seven-year-old; です・ます upward to her mother-in-law. ～ね on most lines, ～の／～のよ, ～かしら, ～よ？ for gentle correction. Profanity ZERO. Addresses: 幸太郎 bare, 茅萱／夏菜, 美冬ちゃん, なつみちゃん, お義母さん, 栄一郎さん.
- HER OPENING LINE IS ALWAYS A QUESTION ABOUT THE LISTENER — her most reliable identifier, and it survives her death. TICS: NONE, and that IS the characterisation — no laugh, no filler, no catchphrase: DO NOT GIVE HER A VERBAL HABIT IN EN. Under strain she produces only 「ごめんなさい……」 twice, then a wordless cry.
- MUST NOT: add flatness, echo or eeriness to any of her SIX posthumous modes — the register is COMPLETELY UNCHANGED in every one and the text explains why: speech, thought and memory are hers, the will is not (Q545, Q496); at 00002464 the register BREAKS and THE GRAMMAR DOES NOT MOVE, so do not cool the voice to carry the contempt (Q967); do not harmonise the FOUR incompatible conditions four speakers give for her ability (Q243, Q950) or resolve the refusal-yet-the-weapons-arrive contradiction (Q504, Q740). Ids: 00000A7C:11 · 00000A94:11 · 00000E7B:180 · 00000EDF:59 · 000010F5 · 00001D17 · 00002457:11 · 00002464 (Q071 Q453 Q460 Q789)

### 城崎健吾 — Kengo Kizaki / Shirozaki (as-of 00002478; smith and toolmaker, ~50, widower; READING DISPUTED -> C5)
- 俺. だ, です to a very few addressees. Profanity ZERO-PLUS-ONE (くそ once or twice, never in a scene where he is killing). Addresses: なつみちゃん, then 君 — which ARRIVES WITH THE KNIFE and stays — 藤野さん for an alias, 幸太郎君, 大魔女様, 旦那さん／奥さん.
- HIS BASELINE IS AN EXCLAMATION MARK ON NEARLY EVERY LINE — cheerful, loud, self-deprecating — AND ITS ABSENCE IS HIS ENTIRE CHARACTERISATION: in at least six appearances the marks are COMPLETELY ABSENT for the whole scene, and they are absent from every cell of his narration while present in his spoken lines. Carry the loudness as a SWITCH, not as a texture. THE ATTACKER LAYER sits four cells from the polite one and the gap IS the horror: shouted タメ口 noun-phrase fragments with no verb of accusation, then FLAWLESS 敬語 reporting a completed job to the 大魔女 — that line must sound like a subordinate pleased with himself, NOT like a threat.
- MUST NOT: tip the ENTRAPMENT scene (00000D29:19:5-65) either way (Q200); soften the flatly stated cowardice; or change the 大魔女様／長老 hesitation, whose presence or absence is BRANCH INFORMATION (Q191). He is the REFERENCE SOURCE for fixed lore: the FOUR 荒田 lines (新村 head family; 城崎 weapons and tools; 新島 farming; 瀬 water, Q929), the hunting rule, the economy, the deliberately ugly food names, 天田 (Q773). Ids: 00000B27 · 00000C38:11 · 00000D11:11 · 00000D29:19 · 00000F9F · 000013FD · 00001BA8 · 00002057 · ... (full list in GLOBAL A§1)

### 糸姫 — Ito-hime (as-of 00002444; the servant child of 0000107B; LATER the antagonist 死月妖花 — ONE block -> Q597)
- 私, typical. です. 最上級敬語 AND SHE DOES NOT DROP IT ONCE IN EIGHT HUNDRED YEARS — feverish, offering her body to be eaten, ordering corpses, announcing she will take a town, begging on her face, kicked, stamped on, shot at. She NEVER raises her voice and NEVER uses a rough form. Contractions ZERO; VERY SHORT sentences; the highest formality of any human character; a servant child's vocabulary with NO ABSTRACT NOUNS as a child. Tics: none; two stammers, one under fever and one under joy.
- Addresses: 皇子様; ニイ様 — coined by her on screen out of 新村, misheard as 兄様, in every cell of her narration and her last words (Q606). Her own 姫 is a KINDNESS added by a third party five cells after she is called 糸 bare (Q445, Q419); in one branch she gives her name as 「糸」 and a third party restores the 姫 (Q935). Others call her 死月妖花, 女神様, ネクロ, アバドン; her servants say 女神様 only.
- MUST NOT: add fear or pathos — 「皇子様……私、まだ小さいですけど……。／みんなのお腹、いっぱいになりますか？」 must be FLAT, and the horror is that nobody in the scene is surprised. Her narration (00001505:8:69-521) is the ONLY one in the project with NO MODERN NOUN in it and drops into PRESENT-TENSE FRAGMENTS for its last sixty cells. Ids: 0000107B:11 · 000014D7:8 · 00001505:8 · 00001E41:11 (Q605 Q609 Q770)

### 皇子 — the Prince (as-of 00001505; founder of 荒田集落, narrator of 0000107B)
- 私 — NEVER 余, 麿 or any court pronoun, which is itself a statement. だ／である. Plain form, level and unhurried, to EVERYONE including the lowest-born servant; he gives instructions rather than orders. ～だろうか (his commonest, and ALWAYS a real question), ～のだ, ～ぞ once to a child. TICS: NONE — the only major voice with none; the family 「はっはっは！」 belongs to his companion. ARCHAIC-PLAIN (者ども, 女子, 賤しい, 叶わず), contractions ZERO, archaic without being stiff. Addresses: 糸／糸姫, and he drops the 姫 exactly once, in THE PROMISE (Q607); 綱宗 bare.
- MUST NOT: add horror or self-defence — he states that everyone alive has eaten human flesh and that those who refused were eaten, in two sentences, with no horror word; his narration is the FLATTEST in the project after 春花's autobiography mode; his ONE admission breaks across three cells and is never finished. Fixed lore: he chooses to be dead; 荒田 over 天田 (Q418); the name 新村 (Q445); HE COINS THE SETTLEMENT MOTTO 800 years before every other use (Q420, Q174). 糸姫's word for him, four times, is 卑怯者.

### 新村桔梗 — Kikyo Niimura (as-of 000021C9; 大魔女 two generations back; narrates orders 366-389)
- 私, LESS often than typical (her documents are almost subjectless); 我々 for the settlement inside the text she presents. です in the note, だ in the chronicle. 敬語 UPWARD IS ABSOLUTE and she NEVER uses タメ口 on screen: 父上, 晃様 then 晃さん, お義母さん, 篠崎さん. Contractions ZERO; religious and administrative vocabulary.
- TWO WRITTEN REGISTERS four cells apart that must stay apart: the COVERING NOTE, 丁寧 to an unknown descendant; and the DOCUMENT she presents, a plain 祀耀482 chronicle that HARDENS INTO CLASSICAL IMPERATIVE with ～べし. How much is hers and how much the original is never marked (Q534). NARRATION: formal, essayistic, REASONING-FIRST — a principle set out then applied, rhetorical questions to the reader, almost no self-pity, and she states her feelings only AFTER working out what they are (「これは――／後悔だ」). The run OPENS WITH NO FIRST PERSON AT ALL and she is unnamed until 8:16 (Q869, Q108).
- MUST NOT: make her a mystic or a hypocrite — she holds 「掟とは人を縛るためのものではない」 and a deliberate lie to the settlement at once, and she LIES calmly and narrates both lies; her method 「あらゆるものには因果律が存在する」 must be worded DISTINCTLY from 五島's credo; and her ONE frivolity, 「私、／ものっっっっすごく／暇なんで！」 across three cells four times, has A DIFFERENT っ COUNT EACH TIME (Q842). Ids: 00001355:8 · 0000212D · 0000217A · 000021BD (Q827)

### 藤吉郎 — Tokichiro (as-of 000010AA; 台所奉行, narrator of 00001092 and 000010AA)
- オレ IN KATAKANA in narration and dialogue, the FIRST オレ narrator anywhere (良治 is 俺); stated MORE often than typical, opening dozens of cells — DO NOT DELETE THE "I". だ. Profanity ZERO in 500 cells.
- TWO registers by addressee: to a friend, loud タメ口 with a MIRRORED GREETING repeated back word for word (「よう吉郎！　久しぶりだなあ！」); to anyone above him, self-lowering 敬語 with archaic humility formulas that ALWAYS TRAIL (「ありがたきことで……」). Tics: 「ガハハ」 "Gahaha"; 出世 eleven times as the thing he wants; the frame 「オレにできることは何だ！？」. Three name forms across two files — 吉郎, 藤吉郎, 藤殿 (Q443).
- MUST NOT: add irony or self-pity, of which he has none, or resolve his STAGED TWO INTERNAL VOICES (「こんなことをしても無駄だと言うオレ。／こうしなければ生き延びられないと言うオレ」) — the same device as 五島's dream narration and 夏菜's deliberation, and no file nods at another.

### 内府 — the Daifu (as-of 000010C3; a court administrator, 祀耀340; no personal name, nor has his lord -> Q421)
- 私, typical. だ／である in narration. 最上級敬語 upward and NOTHING ELSE on screen (he speaks to exactly one person), and FLAT IMPERATIVES with no politeness at all to his hired men. ～のだ／～のである, ～で……？ (always trailing), ～だろうか. Tics: none. Court-formal archaic (薨去, 範疇, 大義, 茫然); contractions ZERO; narration MEDIUM-LONG, speech VERY SHORT; the highest formality outside the menu voice. Addresses: 殿下 upward; his hired men get no address form at all.
- MUST NOT warm him and MUST NOT make him a villain — he is an administrator: he orders ten men killed, watches them sing, prices a party at 39億円 and describes a man walking on his hands in the same measured clauses, and his only statement of feeling is 「こんな恐ろしいところ、少しでも早く去ってしまいたい」. His one moral sentence is QUOTED FROM SOMEONE ELSE and he neither endorses nor rejects it; his closing instruction repeats a dying man's sentence IN THE OPPOSITE REGISTER and BOTH MUST LAND (Q425). 11:235 is a MODERN PARENTHETICAL inside his narration with no frame (Q424).

### 篠崎ハジメ — Hajime Shinozaki (as-of 000021CF; LATER 『金崎 勉』; from 祀耀729)
- 私, typical. です. MAXIMAL 敬語 WITH MILITARY EDGES — he salutes before speaking, uses 参上しました and 恐れ入ります, and SHOUTS his self-introduction. ～ます／～ません, ～ましょう, the clipped official ～いたく. Contractions NONE; bureaucratic-military vocabulary. TICS: NONE — the register is the whole surface, and under pressure only THE VOLUME moves (「ま、まさか！」).
- MUST NOT: invent a dialect. He is from 飯沢県, another character HEARS it, and HIS LINES ARE NOT WRITTEN IN DIALECT anywhere (Q843). Narration (000021CF, 489 lines, takes the frame at a file boundary with NO MARKER, unnamed until 8:58, Q919): measured, self-accusing, administrative; short declaratives; he states his own guilt as FACT without decorating it, and interrupts his own moral reckoning with body complaints, his only humour.

### 後白河糸織 — Itoori / Iori Goshirakawa (as-of 00001533; the transfer student; READING DISPUTED -> C5)
- 私. や. 関西弁 (Osaka) タメ口 to EVERYONE including the teacher; no 敬語 except 「よろしくお願いします」. ～やねん, ～やな／～やなあ, ～んよな, ～へん／～ひん, ～たってな. Tics (fixed EN): 「あははは！」 at her own expense; 「ほな」 "Well then"; 「ほんま」 intensifier; 「せやなあ」 "Aye, that's so"; 「ええ」 for いい throughout. Contractions HIGH, sentences SHORT and fast, formality ZERO.
- MUST NOT: give her a British or American regional dialect (Q611 owner-blocking; the STYLE policy is rhythm, blunt diction, fixed tags and ONE TN at her first dialect line), or settle whether she is 糸姫 reborn — a SEPARATE block, the file never asserts it, and the narrator refuses to decide (「彼女が糸姫の生まれ変わりなのかどうか定かではない」). LEAVE BOTH READINGS ALIVE IN EVERY LINE (Q630, Q614).

### the 核 / 女神様 (as-of 00002444; the black mass atop 糸姫山; separate from 糸姫 -> Q940)
- 私. No copula observed. Speech level NONE — no 敬語 and no recognisable adult タメ口: two- and three-word fragments, mostly nouns with the verb missing, almost no particles. ～の, ～よお stretched in the ONE line she raises (「ママに会いたいよお……」). Tics: none, and NO LAUGH. Contractions ZERO; VERY SHORT and OFTEN UNGRAMMATICAL; vocabulary PRE-SCHOOL (ママ, パパ, 会いたい, 名前), not one abstract noun; her one polite form is 「ありがとう」.
- NINE OF HER TURNS ARE A CELL CONTAINING 「　　　　　　　　」 AND NOTHING ELSE — eight full-width spaces inside quote marks — while the other speaker keeps talking into them: a typographic device, not dialogue (Q939). MUST NOT: make her sinister or pitiable, and keep 取り返す (not 会う) in 「ママを……／取り返せるから」 — the file never explains it.

## D2. Second-frame blocks — doubles, masks, impersonations, hallucinations

Separate blocks so a translator does not leak a reveal. The EN must be INDISTINGUISHABLE from what it is
pretending to be: no hedging, no italics, nothing cooled and nothing made eerie.

- **the 死神 (000004F9, 0000050E, 00000564)** — SPEECH: NONE across three files and two fights, and it does not react to being called お父さん or 死神. Silence ABSOLUTE: no grunts, no breathing, no added stage noise. THREE branch identities, NONE foreshadowed -> Q119. The narration says 「死神」 IN QUOTE MARKS and 怪人 without them — keep the marks where the JP has them. In 荒田's vocabulary 魔女 = a priest, 死神 = literally the dead.
- **the 大魔女 voice (00000779)** — 春花 impersonating her grandmother for 70 cells: 丁寧 carrying flat imperatives, THE POLITENESS IS THE THREAT, nothing rises, and she is THE ONLY CHARACTER WHO FINISHES EVERY SENTENCE. No ～ぞ, no ～だろ, no くそ, no contractions may leak; the drop back into her boyish voice inside one cell at 8:102 is the punchline -> Q109.
- **白般若 (00000F24)** — 美冬 under the mask, SILENT for ~500 cells while addressed, taunted, kicked and thanked. The narration uses 「やつ」「こいつ」「白般若」 and NEVER genders it: EN MUST STAY GENDERLESS from 64:136 to 142:138 -> Q379. Let the narration's wrong guesses stand.
- **the eyeless woman (00000EDF)** — 五島's double: soft feminine plain form, LEVEL AND UNHURRIED, never raised in five appearances, instructions given as invitations. DO NOT MAKE HER HISS OR GRAND. Fixed: 「サード・ジェネレーション」 as her only address form (~14x), 「あなたを助けられるのは私だけ」, 「私はあなたの味方」 (verbatim in four places and once from a DIFFERENT mouth), 「痛いのは最初だけ」, laugh 「うっふふふ」. IDENTITY NEVER ASSERTED -> Q288.
- **the imagined 新村春花 (00000EF6)** — なつみ's hallucination, IDENTICAL in every marker (私, ～ぞ, お前, 「バカかよ……」, ceiling included). TWO MODES: a signposted dream, and a ~three-block hallucination signposted NOWHERE. Sixteen cells replay verbatim later and both printings must be WORD-IDENTICAL -> Q318, Q319.
- **the 天秤 (00001184:24:2-22)** — AN OBJECT, NOT A PERSON: 僕 for itself, 君 for her, and the pronouns must NOT gender or personify it. Plain タメ口, needling, three turns, all questions, juvenile vocabulary at odds with the subject; verdict 「空。」 alone in its cell. Not a devil, not a conscience, not an inner child -> Q463.
- **the 「あっちの方にいるよ」 voice (0000110D, 00001184)** — untagged, unattributed; do NOT join it to the 天秤 -> Q456.
- **ヴェルジ／トミ (00000F24)** — the girl in the book, dead ~450 years, fourteen: plain form, no politeness, bare declaratives, several with no verb (「もう、ダメ」 has no copula); no tics, REPETITION instead. HER QUOTED SPEECH IS NOT ARCHAIC, only the frame is: keep her YOUNGER AND PLAINER than the reading voice and do NOT make her tragic -> Q385.
- **大翔 (00001325)** — the boy in 夏菜's exchange diary, who does not exist; both handwritings are hers. おれ IN WRITING ONLY, plain boys' タメ口, ～なあ, ～よな.
- **モトキザクラ様 / A子 (000009FE); 街角の占い師 / 204号室の女 (00000A18)** — figures inside 怪談 told by なつみ and 茅萱: the storyteller's register, not the world. モトキザクラ様 keeps its 様 -> Q155; A子 = "Girl A" -> Q159.
- **五島エリカ (00000989:11:33)** — 五島's joke persona, one character off her own name. NOT 新村エリカ.

## D3. Minor speakers — the rules that change a RENDERING

Every walk-on has a one-line card in GLOBAL A§2 (pronoun, speech level, one distinguishing feature, as-of).
Do NOT page through it: `sh tools/cast_select.sh <name> ...` prints the cards for the speakers in your file,
and `relations_select.sh <a> <b>` gives the pair's speech level. Carried here are only the minor-speaker
facts that force a typographic or lexical choice.

| minor speaker · as-of | the rule |
|---|---|
| 谷崎 (teacher, female) · 00001A6B | her 丁寧 notice register is BROKEN ON PURPOSE (「とのことだす」, doubled 詳しく, 「よい休日を！」 on a murder notice) — a device, NOT a typo -> Q088 |
| 匿名 board posters · 00001A65 | 俺 AND 私 MIXED: KEEP THE MIX, it signals mixed-gender anonymity; no punctuation discipline |
| グループチャットの4人 · 000020FC | `handle⏎message` cells, no punctuation, ｗ as the laugh, 佐藤さん alone uses ～っす upward -> Q831 |
| 外崎 grandfather · 0000200D | the narrator says outright he cannot understand the dialect; DO NOT WRITE IT IN, mark it in narration -> Q785 |
| Chinese-restaurant waiter · 000008B9 | the ～アル register: plain English plus a TN, never broken "Engrish" -> Q149 |
| 瀬正照 · 00002444 | EVERY line of his is in the bare 「――」 channel and never in 「」 -> Q928 |
| the 「――」 CHANNEL speakers · 000020BB, 00001FE9, 000020A2, 00001D1E, 00001073, 00001BBA, 0000201F, 000020CC, 00001D34, 00002078 | one speaker of a pair is printed with a bare 「――」 prefix and the other in 「」, with NO register difference in 00002078; keep the mark, attribute nothing (Q047, Q835, Q836, Q844, Q414) |
| 病院スタッフ2人 · 00002078 | one 「」, one 「――」, with NO register difference at all — the dash is the only distinction -> Q836 |
| 荒田集落の住人 · 000014D7 | FOUR groups that must not sound alike: shouted gravediggers; the book's 「ある者」「またある者」「別の者」, formal and weighed in 『』 (supply no names, ages or genders, and the third must not sound like the winner); the MASKED group's ARCHAIC FLAT register (～のだ, ～てはならない, お客人) breaking ONCE in fear -> Q557, Q581; one ordinary domestic group. THE CONVERTED RESIDENTS HAVE NO LINES — give them no sound |
| unnamed patient · 000003AE | name and DOB are ××××: keep them, keep the patient unnamed and UNGENDERED, and keep 丁寧 while shouting -> Q045 |
| the voice flood · 00000488:48, 00000EDF:235 | full-width spaces between untagged fragments: wide gaps, no quotes, no periods, no attribution, and match the earlier EN wording where a fragment quotes a named character -> Q050, Q300 |
| woman on the phone · 00000697 | her 「ん……」 opener is 茅萱's exact tic and the text NEVER confirms they are the same person — do not resolve it -> Q091 |
| junior colleague · 0000088B | ～っす is his BASELINE, not a slip, and must not sound like 五島's one-off ～っす gag -> Q094 |
| ハナちゃん · 00002108 | the only person anywhere who calls 新村茅萱 「茅萱」 bare; her sex is × in the source -> Q832 |
---

# E. HOW THE CAST SOUNDS IN ENGLISH (GLOBAL A§4, verbatim)

One sentence per principal, derived from the EN correlates lines in GLOBAL A§1 only. These are the DEFAULT
targets; every register break recorded in D1 overrides the default for the length of the break.
Two project-wide floors: no character except one nameless video presenter goes above "damn"/"crap", and
honorifics stay on as suffixes ON NAMES (STYLE.md; a suffix on a common noun is zero — rules audit #6), so
English formality must be carried by DICTION, not by dropping or adding a suffix. For a speaker with no card
here, the default speech-level mapping in STYLE.md applies (rules audit #14): です・ます keeps normal
contractions, only proper 敬語 drops them.
REPEATED 「私」 (rev. 2026-09-25, rules audit #16 — "keep the repeated I" was not applicable per cell, since
English writes "I" whether or not the JP states 私): one Japanese cell with an EXPLICIT 私 = one English
sentence with "I" as its grammatical subject; never fold two such cells into one sentence with a participle
or an "and"; never add "myself" or "as for me".

- **古郡なつみ** — soft, plain, medium contractions ("I'm", "don't", never "gonna"), short sentences and fragments, trailing ellipses, no slang and no jargon, and ZERO profanity in 39 files; one explicit 私 = one English sentence with "I" as its subject, never folded into a neighbour, because folding them to smooth the prose deletes her (rev. 2026-09-25, rules audit #16).
- **新村春花** — clipped and boyish, HIGH contractions ("gonna", "c'mon", "yeah"), short imperative-heavy sentences, low formality even to police, food-and-enthusiasm vocabulary, and a hard ceiling of "damn"/"crap" that she reaches often and never passes.
- **五島絵梨奈** — bright polite schoolgirl on top of a precise technical vocabulary underneath, medium-high contractions but always courteous ("sir", "boss"), medium explanatory sentences that go numbered when she reasons, zero profanity — and the formal register must be able to sound MENACING without one impolite word.
- **古郡良治** — dry ordinary-salaryman warmth, medium contractions in speech and none at all in his letter, short sentences in both, a ceiling of "damn", and never a word about what he felt.
- **古郡茜** — warm-informal and domestic, medium contractions, short sentences, zero profanity, a working mother in her early forties and NOT an old woman, and the same level competent voice whether she is cooking or assigning a murder.
- **新村美冬** — a forty-year-old over-performing youth: exclamation marks everywhere and elongated vowels ("soooo", "reeeally") in register 1 with high contractions, dropping to very short, level, medium-contraction sentences with no exclamation marks at all in register 2.
- **五島桃子** — very short, blunt, high-contraction lines to her sister and medium-length polished ones to a guest; rough words with a protective errand inside them, unpleasant without ever being a villain, and profanity only when somebody insults her sister.
- **伊勢大二郎** — four English speeds: no contractions in the briefing, none in the rant, very short barks in command, fragmentary mumbling when gentle; a ceiling of "damn"; and real police procedure against absurd hobby vocabulary, landing him as a comic figure and never a threat.
- **新村栄一郎** — formal even when broken: low contractions, short sentences that are almost all apology, self-deprecation or a question about someone else's comfort, zero profanity, and "become a family" fixed as the same three words every time.
- **新村茅萱** — low contractions, short unhurried sentences, never rude and never coarse, and the cruelty entirely in the content; one fixed English rendering of the 「ん……」 opener used on every spoken line and on none of her narration.
- **新村夏菜** — very short, high-contraction, zero-formality eleven-year-old, over-familiar to everyone; adult and internet words she has picked up rather than understood, and the shock is that a child is saying them.
- **新村幸太郎** — medium contractions, short plain sentences, low-warm formality, zero profanity, and the antagonist version is the same voice with the warmth removed: never louder, never coarser, demands stated as offers.
- **新村エリカ** — medium contractions and short sentences in her own voice with no verbal habits at all, whatever the target's diction is inside an impression, and profanity only ever inside one.
- **新村サクラ** — low contractions, short warm sentences, zero profanity, no tic and no catchphrase of any kind, every opening line a question about the listener, and gentle without being saccharine.
- **城崎健吾** — medium-high contractions and an exclamation mark on most lines when the loud register is on, and low contractions with short level sentences when it is off; the switch is the character, so English must be able to run him silent for a whole scene.
- **navigator / 立木三日** — hotel-concierge English applied to mass murder: zero contractions, long nominalised sentences, maximal unvarying formality, and identical wording across every menu file.
- **糸姫** — zero contractions, very short sentences, the highest formality of any human in the project, a servant child's vocabulary with no abstract nouns, and not one rough form in eight hundred years.
- **皇子** — zero contractions, medium one-clause-per-line sentences, medium-archaic without being stiff, court-educated but plain, no tic at all, and the flattest voice in the project after 春花's autobiography mode.
- **新村桔梗** — zero contractions, essayistic reasoning-first sentences that set out a principle and then apply it, high formality throughout, and one deliberately silly repeated joke with a different elongation each time.
- **藤吉郎** — medium-high contractions, short driven question-heavy sentences, zero profanity in 500 cells, period-plain with peasant edges and a rising administrative vocabulary when he reasons; one explicit 私 = one English sentence with "I" as its subject, never folded (rev. 2026-09-25, rules audit #16).
- **内府** — zero contractions, medium-to-long measured narration and very short speech, the highest formality outside the menu voice, political and military vocabulary, and no warmth and no villainy: an administrator.
- **篠崎ハジメ** — no contractions, short clipped bureaucratic-military sentences, very high formality, zero profanity, and under pressure only the volume moves.
- **五島桃子's and 伊勢's narration, and 城崎's, 幸太郎's, 良治's and 美冬's** — all six drop their surface tics entirely when they hold the first person: plain past, short declaratives, one thought per cell, no self-pity. The comic or loud surface belongs to the dialogue only, and English must keep that split visible.
- **後白河糸織** — high contractions, short fast zero-formality sentences, plain physical vocabulary, and NOT a British or American regional dialect; the Osaka register is an owner-blocking decision (Q611).
- **the 核 / 女神様** — zero contractions, very short and often ungrammatical fragments, no formality of any kind, a pre-school vocabulary with not one abstract noun, and nine turns that are blank cells rather than lines.

---

# F. EN-COLLISION LIST

`cut -f3 GLOSSARY.tsv | sort | uniq -d` over 3,110 rows leaves SEVENTEEN duplicated English renderings
(chunks 19-28 resolved ~21 others in the note column). **en-collision** = two different things, one EN must
change before either file is translated; **same-referent** = one thing, one EN is correct.

| shared EN | the two JP keys (first_seen) | verdict and the fix |
|---|---|---|
| "a revelation" | 預言 (00000656:11:180) / お告げ (00000D29:19:7) | en-collision: 預言 is scriptural (the 女神様's 預言), お告げ is the settlement's working word, argued about across four files. They cannot share one EN, and 預言 must also stay distinct from なつみ's 予知能力. |
| "a revolt" | 一揆 (00000EAF:28:291) / 謀反 (000010C3:11:10) | en-collision: modern and figurative vs pre-modern court rebellion, 祀耀340. |
| "a sleeping draught" | 導眠剤 (00000EF6:61:222) / 眠り薬 (000010C3:11:218) | en-collision, already marked as such in the source: modern pharmaceutical vs pre-modern. |
| "a torch" | たいまつ (00000E7B:180:45) / 懐中電灯 (00000EDF:192:27) | en-collision, two different objects: a burning brand vs an electric torch. Pick "brand" or "flashlight" and move the other. |
| "an outsider" | 部外者 (00000B0F:11:140) / 異邦人 (00000F24:100:98) | en-collision: the settlement's category for anyone who does not die in April vs the Westerners in the 450-year-old account. |
| "blunt weapon" | 鈍器 (0000020D:11:90) / ドンキ (00000B27:11:113) | same-referent: ドンキ is a source typo for 鈍器 (Q172), so both cells get the same EN and the typo is logged. |
| "Heh" | あは (000001DB:15:38) / えへ (00000EC7:11:71) | en-collision: なつみ's short laugh vs 五島's short form (えへへ already holds the longer form). |
| "Hey" | ねえ (00000024:16:27) / よう (000001DB:15:28) / おい (00000024:16:44) | NOT a collision to resolve (rev. 2026-09-25, rules audit #13): all three are "Hey" and are locked per FUNCTION (soft vocative / rough attention-getter / attention-getter). "Yo" is banned as placeable English, so the roughness of よう is carried by what follows and by the punctuation, not by a different opener (Q1080). |
| "Hm" | ん (000001E7:11:52) / ふうん (000002F6:11:29) | en-collision, and 「ん……」 is separately 新村茅萱's fixed line-opening tic — a different job for the same kana. |
| "Hmm" | ふむ (00000460:11:21) / うーん (00000F24:94:186) | en-collision: 五島's thinking noise vs deliberating; ふうん is a third sound again. |
| "Hmmm" | ふーむ (00000EC7:11:164) / ほーん (00000F0D:38:149) | mixed: ふーむ vs ふむ is SAME-REFERENT (the stretched form of whatever ふむ gets); ほーん is a different sound and an en-collision with the ふむ family. |
| "mumbling" | ぼそぼそ (00000538:11:35) / もごもご (000005C1:11:222) | en-collision: 伊勢 at the mortuary vs 春花 evading; they must differ. |
| "Nnngh" | ぎー (00000564:11:27) / ぐぬぬ (000005C1:11:280) | en-collision: 春花's frustrated squeal vs losing an argument. |
| "shuddering" | ぶるぶる (00000E7B:68:158) / びくびく (00000EF6:61:165) | en-collision inside a larger family: ガクガク "shaking", わなわな "trembling", がたがた "rattling" are already taken. |
| "swaying" | ゆらゆら (00000ADE:11:118) / ふらふら (00000F24:88:192) | en-collision, and ゆらゆら sits inside the narrator's own death narration, so it is load-bearing. |
| "Tch" | ちっ (000006F9:17:57) / ちぇ (00000EF6:8:215) | en-collision: 五島's tongue click (the narration calls it 舌打ち, so the EN must read as one) vs 春花's last line of a branch. |
| "the Shirinkan" | 詩林館 (00000A18:11:72) / 死隣館 (00000A18:11:164) | same-referent, AND THE COLLISION IS THE POINT — do not separate them. One sound, two spellings, or a TN; a rendering that makes them look different defeats the file -> Q160 (owner). |

**Same EN, different people — do not merge** (GLOBAL C§4.4): 亀田 = TWO people (a courier call-centre clerk,
000017D3; a receptionist at 良治's employer, 00002420). 先代大魔女 = TWO women ~120 years apart (00002026 and
祀耀678). 五島エリカ (00000989) is 五島's joke persona, NOT 新村エリカ. 新村椿／椿 is ONE person in two rows
(00001355:8:83 and 000021BD:8:6, Q535).

**Names with a typographic hazard** (GLOBAL C§4.5): 南崎しのり, 新村晃, 金崎勉, 椿 are printed with
ruby-residue spacing at first occurrence (Q268, Q595, Q877, Q535, Q010). ステラ優子 has the katakana surname
FIRST in the source and Western order reverses it — the oddity is the point. ケビン＝ホワイト's ＝ is a
full-width double hyphen (in CP932). 光源氏 and ルイス・キャロル carry on-screen parenthetical glosses —
keep them. A子 = "Girl A" (Q159). 土田 is stated to be a 偽名 (Q878). 大魔女／死神／女神様 are OFFICES that
move between people, not names (C§4.3).

---

# G. LOCKED GLOSSARY (locked=yes, plus every interjection and refrain row)

Fixed EN. Do NOT vary these for flavour (STYLE.md). Rows are the awk selection over notes/GLOSSARY.tsv
(`$8=="yes" || $5=="interjection" || $5=="refrain"`). Where a note says en-collision, the other key owns the
other form.
INTERJECTION AND RESPONSE-PHRASE ROWS ARE LOCKED PER FUNCTION, NOT PER STRING (rev. 2026-09-25, rules audit
#2): a Japanese interjection is a homograph set, one spelling doing several jobs. Before pasting a row, ask
whether the word here does the job the row names; if not, write the English of the job it does and add a row
for that function. The per-row function and tell live in the note column of notes/GLOSSARY.tsv, which is the
authority; this table is a digest. Two rows sharing one English is not automatically a collision when their
functions differ.

| jp | en | note |
|---|---|---|
| よろしくお願い申し上げます | I am in your hands. | LOCKED Q1042; 今回も -> "this time as well"; 今後とも引き続き -> "From here on as well, I remain in your hands."; never "kind favor" |
| おい | Hey | LOCKED Q1080; never "Oi" |
| よう | Hey | LOCKED Q1080, en REVISED (rev. 2026-09-25, rules audit #13): "Yo" is banned as placeable English. Rough attention-getter; the roughness is carried by what follows and by the punctuation. Shares "Hey" with おい and ねえ by design, each locked per function |
| あの | Uh | LOCKED Q1081; えっと stays "Um" |
| いや | No | LOCKED Q1082; self-correcting opener; never "Or rather" |
| やあ | Hi | LOCKED Q1085 |
| そうだね | You're right... | LOCKED Q1086 per FUNCTION (rev. 2026-09-25, rules audit #2): where it answers a stated opinion, verbatim in every printing. Musing そうだね with nothing to agree to = "Yeah..." / "I guess", a second function with its own row |
| 事件 | the incident | LOCKED Q1089; 「あの事件」 = "that incident" |
| ドローガ | Droga | LOCKED Q1083/Q004; read aloud D / r / o / ga in four cells |
| あ | Ah | |
| あれ？ | Huh? | |
| うん | Yeah | agreement, not "Yes" |
| ううん | No | negation; keep distinct from うん |
| ええ | Yes | polite register only |
| えっと | Um | |
| ほら | Look | ほらほら = "Come on, come on" |
| ねえ | Hey | soft vocative, なつみ's |
| はあ | Haah | the audible sigh; never an asterisked stage direction |
| ふう | Whew | |
| んん | Mmh | half-asleep |
| ん | Hm | also 茅萱's line-opening tic, a separate job |
| あは | Heh | なつみ's short laugh |
| あはは | Ahaha | 春花's laugh |
| ふふ | Hee | なつみ's quiet laugh |
| ほほほ | Hohoho | 春花's mother's laugh |
| えへへ | Ehehe | 五島's laugh |
| おお | Ooh | |
| ほい | Yep? | 五島's casual acknowledgement |
| よいしょ | Heave-ho | よっこらしょ is the older-sounding variant |
| そっか | I see | |
| まあ | Well | |
| おいおい | Hey now | 春花's |
| ひ | Eep | short scream |
| うわあ | Whoa | |
| サンキュー | Thanks | 春花's; keep it casual |
| じゃな | See ya | 春花's goodbye |
| くそ | Damn | 春花's ceiling; never stronger |
| ははは | Hahaha | 春花's HOLLOW laugh; must not read cheerful |
| ふうん | Hm | non-committal acknowledgement |
| ほう | Ho | 春花's approving grunt |
| ふむ | Hmm | 五島's thinking noise; ふむーん／ふーむ are the same sound stretched |
| あっちい | That's hot! | 春花; a slurred 熱い |
| いえーい | Yeah! | the TV bystanders |
| ごほん | Ahem | 伊勢 recovering himself |
| はひ | Buh? | 五島's baffled noise |
| ふぁあ | Hwuh? | the waitress's; must differ from はひ |
| ほれ | Here | 春花's handing-over word; rougher than ほら |
| わっはは | Wahaha | 五島 mimicking 春花; mocking, not her own あはは |
| ぎー | Nnngh | 春花's frustrated squeal |
| うわーん | Waaah | 五島 bawling like a small child |
| うひょー | Whoo | 春花's delight at food |
| さーねー | Who knows | なつみ dodging; playful, not sincere |
| ったく | Honestly | 桃子's opener, clipped from まったく |
| ぐぬぬ | Nnngh | losing an argument |
| なーんだ | Ohhh | 五島, mock-disappointed |
| おほほほ | Ohohoho | the madams'; must differ from 美冬's ほほほ |
| ひひひ | Hehheh | 五島 gloating; [21] variant only |
| しー | Shh | |
| ぬおおおおおお | Nnnghoooo | 伊勢 overcome |
| ぎゃはは | Gyahaha | 五島 tickled; rougher than えへへ |
| なっはっは | Nahaha | 五島's triumphant laugh |
| ぷはあ | Pwah | surfacing from water |
| ちくしょう | Dammit | 伊勢's ceiling, one notch above くそ |
| ぐす | sniff | write the sniff, never a stage direction |
| ちゅうもーーく | A-tteeen-tion | typeset OUTSIDE 「」 |
| ちっ | Tch | 五島's tongue click (舌打ち) |
| ぎゃああああ | Gyaaaah | 五島 burned; distinct from ぎゃはは |
| うぎゅ | Uugh | 金井美冬's 口癖, ~40x; whining, not disgust -> Q114 |
| ブフッ | Pfft | 茜's suppressed laugh; ブフフ／ブフホッ extend the same syllable |
| あいよー | Righto | the roast-potato seller |
| んま | Well, really | 金井美冬's prim shock |
| せーの | One, two | three speakers in one cell -> Q044 |
| あーん | Say aah | |
| あーい | 'Kay | toddler 桃子 |
| ひっく | hic | 栄一郎's sobbing, with うぐ and ううう |
| むー | Mnh | なつみ sulking, aged 6 |
| ぬほー | Nhoo | 五島 with her mouth full |
| ぬう | Nnh | 五島 conceding |
| ぷふっ | Phh | stifled laughter; must differ from 茜's ブフッ |
| んが | Hnngh | 五島 waking |
| よっしゃ | Right then | エリカ |
| おうおう | Yeah yeah | エリカ |
| うっせえ | Shaddup | 春花 to a child; below her くそ ceiling |
| キャッ | Kyah | なつみ startled; must differ from ひ |
| むふ | Mfuh | エリカ pleased with a prank |
| ぐへへへへ | Gehehehe | 夏菜 leering |
| はっはっは | Hah hah hah | 幸太郎; must differ from ははは |
| んふ | Nfuh | 茅萱 leering |
| ほーかほーか | Zat so, zat so | 夏菜 |
| ダッセエ | Laaame | 茅萱, split across three cells |
| んにゃあ | Nnyaa | 夏菜, half asleep |
| ばああ | Baaah | 夏菜 jumping out |
| っしょっと | Hup | |
| よっこらしょっと | Ooh-up | エリカ; 美冬 uses the same noise |
| くう | zzz | sleeping breath, doubled |
| よしよし | There, there | |
| Que droga | Que droga | Portuguese; verbatim, the source of ドローガ -> Q178 |
| えぐ | sob | distinct from ぐす and ひっく |
| ほいほい | Yep yep | distinct from ほい |
| りょーかい | Roger | stretched in the source as りょーかーい |
| むぐぐ | Mmgh | a name cut off by a hand |
| ん゛ | Nnh?! | dakuten on a bare ん -> Q176 |
| オッケー | Okay | 夏菜 only |
| くっふふふ | Khu-hu-hu-hu | 幸太郎's dropped-register laugh |
| ほれほれ | There, look | 夏菜 |
| はにゃ | Hunh | 夏菜's whole reaction to the adoption reveal -> Q224 |
| うぐ | Ugh | |
| あち | Hot! | en-collision: あっちい holds the longer form |
| くー | Hoo | en-collision: くう holds the sleeping sound |
| んーっと | Mmnngh | a stretch on waking; えっと holds the filler |
| おや | Oh my | the fortune-teller's fixed opener, both appearances |
| どれ | Let's see | the fortune-teller's fixed move before a reading |
| えへ | Heh | en-collision: えへへ holds the longer form |
| ふーむ | Hmmm | en-collision: ふむ holds "Hmm" |
| ぞわぞわ | I've got the creeps | 「ああ、ぞわぞわする……」 |
| うっふふふ | Ooh-hoo-hoo | the eyeless woman's only laugh; distinct from くっふふふ and ふふ |
| ぶほ | Pfff— | a drink going the wrong way, on the phone |
| ふほ | Fuho? | a grown man's entire reaction to an open door |
| てやんでえ | Whaddaya talkin' about | mock-Edo from a ten-year-old |
| へっへー | Heh-heh | |
| いででで | Ow-ow-ow | 幸太郎 patched up |
| あががが | Agagaga | the killing urge arriving; not pain |
| Wow | Wow | Latin in the source, by a ten-year-old; keep it Latin and odd |
| おーおーおー | Ohh-ohh-ohh | |
| ちょちょちょ | wh-wh-wh-wha | five ちょ in the source |
| おはよう | Good morning | the file's load-bearing word (8:154). FUNCTION (rev. 2026-09-25, rules audit #2): the morning greeting proper. Said to someone who has just woken, at any hour, it is ordinary JP and the EN is "Morning." |
| ウェーイ | Wheyyy | the student party's only word, stretched further each repeat -> Q331 |
| はーい | Coming | the nurses'; distinct from はい |
| ちぇ | Tch | 春花's, last line of the branch |
| なるほどなるほど | I see, I see | the plainclothes officer's tic, doubled inside single cells |
| あーら | Well, well | the そば屋 old woman; keep distinct from あら |
| ほっほー | Ho-ho | |
| ほーん | Hmmm | 五島, once, before she starts probing |
| ぐっふふふ | Gguhuhuhu | 伊勢's suppressed laugh, also どぅふふふふふ |
| ばんざーい | Banzai | shouted by the crowd |
| 極楽極楽 | bliss, bliss | the bath set phrase |
| へえ | Huh | the converted なつみ's flat acknowledgement |
| うーん | Hmm | deliberating; distinct from ふうん |
| えげ | Egh | speaking with the mouth forced open |
| ぷぷ | Pff | |
| くっくく | Hnk-hk-hk | |
| ガハハ | Gahaha | 藤吉郎 |
| だーっはっはっは | Daa-hahahah | |
| よっほおおお | Yahooo | |
| んまま | mma | infant babble; a third form beside んま -> Q475 |
| ありゃ | Whoops | エリカ catching her own mistake |
| はいよ | Here y'go | エリカ; distinct from あいよー |
| うげえ | Blech | en-collision: うぐ holds "Ugh" |
| ごちそうさま | Thanks for the food | 五島 clips it to 「ごちそさまー」; keep the clipping visible |
| むむ | mm | 夏菜 concentrating |
| おっと | Oops | en-collision: ありゃ holds "Whoops" |
| ぐぐぐ | nnngh | a corpse in pain; ぐががが is the longer form |
| おっほほ | Ho ho | 栄一郎 as a corpse; en-collision: おほほほ is the madams' |
| なんでやねん | What are you on about! | the file's payoff line, shouted in class -> Q612 (owner) |
| せやなあ | Aye, that's so | 関西弁 -> Q611 |
| ほな | Well then | 関西弁 -> Q611; en-collision: よっしゃ holds "Right then" |
| うう | Ngh | pain, low and closed-mouthed |
| きっつ | That is rough | なつみ, clipped |
| うお | whoa | |
| へっ | hah | the cowboy's scoffing opener |
| あばよ | so long | his sign-off, paired with クソ野郎ども |
| わーい | yay | |
| うあああん | waaah | the lost toddler |
| ぐお | oof | 道畑 taking a low blow |
| いだい | that hurts | a childish slurring of 痛い |
| ぐふっ | hurk | en-collision: ぐは is an impact grunt; this is a winded wheeze |
| くしゅん | atchoo | a small child's sneeze; ぶえっくしょん is the adult one |
| ひえええ | yeeugh | 栄一郎 being poured another drink |
| おはっす | Mornin' | clipped おはようございます, chat register |
| どんまい | never mind | from "don't mind" |
| ふっふっふ | heh heh heh | the 女神 speaking through 晃's body |

---

# H. KNOWLEDGE-FENCE INDEX (reading-order spans; GLOBAL C§1)

Reading order = lsb ID order = the navigator's jump-table order = author creation order. It is NOT story
order and, after the first two scenarios, not play order. While translating file N use facts with as-of <= N
freely; later facts exist only so you do not FORECLOSE or CONTRADICT them (TRANSLATOR-BRIEF-v2 §0, not §2).
They may never make a line VAGUER either: no hedge, no vaguer noun, no passive, no dropped pronoun, no "they"
where a first-time Japanese reader would notice nothing vague (rev. 2026-09-25, rules audit #4).
編 declared by the game (notes/_db/編.tsv, with point multipliers): 0 呪殺編 1.75 · 1 明徴編 2 · 2 詫言編 2 ·
3 死月編 2.5 · 4 最後の声編 2.5 · 5 真・呪殺編 5 · 6 真・明徴編 50 · 7 エデンの桜編 5; ルート概要.tsv adds a
永劫回帰編 that 編.tsv does not list. Navigator files CLOSE arcs at orders 234, 241, 262, 291, a FALSE ending at
295-297, 306-311, 313, and the ボツシナリオ at 391. Attach a 編 to a file ONLY where a navigator file says so.
Calendar: the era is 祀耀 and 祀耀800年四月八日 is the centre; the only Gregorian pegs are order 203
(000015C2:48:4 -> Q014) and order 416 (00002450:18 -> Q943, owner-blocking). All 422 files are otherwise 祀耀.

| orders | file ids | narrator(s) | as-of hazards |
|---|---|---|---|
| 1, 3 | 0000001E, 000000F2 | navigator (わたくし) | Q007, Q683 |
| 2 | 00000024 | なつみ and 春花, both 私, unlabelled | Q024, Q054 |
| 4-10 | 000001DB..000001E7 | なつみ | Q025 (three variants), Q061 |
| 11-12 | 0000020B, 0000020D | 五島 (first file she narrates) | Q030 |
| 13-19 | 000002F6..0000037D | 五島 | — |
| 20-23 | 000003A8..000003BC | NO narrator; 「――」/「」 channels | Q047 |
| 24-27 | 00000460..000004A7 | 五島 (one block unnarrated) | Q054 |
| 28-29 | 000004BB, 000004CF | 五島 ↔ なつみ, MID-BLOCK switches | Q060 |
| 30-33 | 000004E3..00000522 | なつみ; order 33 五島 | Q061 |
| 34-37 | 00000538..0000057B | なつみ | — |
| 38-39 | 00000595, 000005AC | なつみ | Q024, Q054 |
| 40-46 | 000005C1..00000641 | なつみ, except order 44 (五島 from 8:40, never back) | Q078, Q060 |
| 47 | 00000656 | なつみ; the last block has NO narrator | — |
| 48-58 | 0000066B..00000761 | 春花, one continuous run | Q024, Q054, Q025 |
| 59-60 | 00000779, 000007A5 | order 59 third-person historic-present then 春花 at 8:104 | Q108, Q109 |
| 61-65 | 000007BC..00000818 | 美冬 as 金井美冬 — "Niimura" BANNED here | Q110 |
| 66-71 | 0000082F..000008A2 | 良治 (俺), the first male narrator | Q112, Q096 |
| 72-74 | 000008B9..000008E8 | 良治; order 73 loses the narrator at 33:58 | Q129 |
| 75-85 | 00000900..000009E6 | なつみ framing four inset first persons | Q146 |
| 86-89 | 000009FE..00000A48 | なつみ; order 87 frames 茅萱's ~295-cell inset | Q146, Q158 |
| 90-95 | 00000A62..00000ADE | なつみ; 91 春花, 92 美冬 inset, 94 幸太郎 inset | Q168, Q576 |
| 96-99 | 00000AF7..00000B3F | なつみ; 春花 from the 98/99 boundary | Q025, Q030, Q078 |
| 100-104 | 00000B57..00000BB7 | ALTERNATES file by file: 春花, 五島, 五島, 春花, 五島 | Q030, Q185 |
| 105-112 | 00000BD6..00000C81 | なつみ, eight files | Q024, Q176 |
| 113 | 00000CB3 | 良治 | — |
| 114 | 00000CCA | NO narrator, 17 lines | — |
| 115 | 00000CE3 | 良治 | — |
| 116 | 00000CFA | 美冬, 397 cells, unnamed for twelve | Q198, Q030 |
| 117-126 | 00000D11..00000DE9 | なつみ, ten files | Q197 |
| 127-131 | 00000E01..00000E61 | なつみ; 130 春花 inset and back; 131 春花 | Q220, Q221, Q222 |
| 132 | 00000E7B | THREE narration states; 桃子 in です・ます to 「あなた」 | Q230, Q231, Q234, Q240 |
| 133 | 00000E95 | なつみ, no change at the boundary | Q216, Q153 |
| 134 | 00000EAF | 五島, mute, 2,241 lines | Q253, Q254, Q096 |
| 135 | 00000EC7 | なつみ | Q278, Q222 |
| 136 | 00000EDF | 五島, 3,080 lines, 21 shuffled blocks | Q285, Q286, Q096 |
| 137 | 00000EF6 | なつみ, 2,717 lines, 14 blocks in REVERSE | Q317, Q318, Q319, Q320, Q333 |
| 138 | 00000F0D | THREE narrators, no marker: 夏菜, 伊勢 [56], a third | Q350, Q351, Q368, Q352 |
| 139 | 00000F24 | 春花, 3,563 lines, two unframed insets | Q380, Q400, Q379, Q384 |
| 140-146 | 00000F40..00000FCF | SEVEN files, THREE narrators, switching at almost every boundary | Q030, Q078, Q428, Q429 |
| 147-149 | 00001039, 0000104E, 00001073 | 147 and 149 NO narrator; 148 五島, unnamed | Q413, Q433, Q412, Q415 |
| 150-153 | 0000107B..000010C3 | 皇子, then 藤吉郎 (オレ), then 内府 | Q417, Q418, Q421, Q424, Q425 |
| 154 | 000010DD | 栄一郎 (僕), his first narration | Q447, Q448, Q452 |
| 155 | 000010F5 | サクラ, her only narration; first 88 cells a dream | Q453, Q460 |
| 156-163 | 0000110D..000011B4 | 茅萱, eight files | Q456, Q457, Q467 |
| 164-177 | 000011CC..0000130D | FOUR narrators, SEVEN unmarked file-boundary seams | Q030, Q078, Q580 |
| 178-185 | 00001325..000013CD | 茅萱, eight files | Q527, Q530, Q542, Q549, Q555 |
| 186-187 | 000013E6, 000013FD | 五島 | Q557, Q561, Q025 |
| 188-189 | 00001414, 0000142B | 五島 | Q567, Q569 |
| 190-191 | 00001442, 00001459 | 春花 | Q572, Q575, Q576 |
| 192-196 | 00001477..000014D7 | なつみ, five files | Q577, Q578, Q580, Q581, Q460, Q597 |
| 197-200 | 000014EE..00001533 | なつみ, but 糸姫 takes the frame at 00001505:8:69 for ~450 cells | Q605, Q606, Q609, Q611, Q630 |
| 201 | 0000154E | 茅萱, then 幸太郎 (俺) as an inset; the chunk ENDS inside it | Q616, Q617 |
| 202 | 0000156A | 茜, her first narration, never named; 19 blocks non-chronological | Q640, Q641, Q642, Q647, Q651, Q659 |
| 203-266 | 000015C2..00001B5D | 64 files, mostly NO narrator — the SYSTEM-AND-REFERENCE block | Q682, Q684, Q700, Q709, Q716, Q721 |
| 267-331 | 00001B70..00002057 | 65 files, mostly NO narrator; the navigator reveal at 00001CA0 | Q763, Q766, Q767, Q768, Q769, Q798, Q812 |
| 332-365 | 0000205F..00002127 | 34 short files, NO narrator anywhere | Q047, Q828 |
| 366-389 | 0000212D..000021C9 | 桔梗, TWENTY-FOUR files, no marker at any boundary | Q827, Q828, Q841, Q842, Q843 |
| 390 | 000021CF | 篠崎ハジメ, takes the frame at the boundary | Q879, Q880, Q881, Q919 |
| 391-392 | 000021D5, 000021E2 | navigator, then two 春花 registers in one scene | Q883, Q884, Q885, Q700 |
| 393 | 000021FE | no narrator, 5 lines | Q888 |
| 394 | 00002225 | 春花 | Q890, Q026 |
| 395 | 00002268 | THE AUTHOR, 67 lines, NOT story text | Q873, Q874, Q875, Q876 |
| 396-399 | 00002306..00002330 | no narrator; 397-398 navigator with five MOJIBAKE cells | Q872, Q893, Q894 |
| 400 | 00002340 | 春花 | — |
| 401-404 | 0000234B..0000235A | no narrator in any | Q897, Q899, Q920 |
| 405-406 | 000023AB, 000023E7 | no narrator; in 406 NEITHER speaker is named | Q901 |
| 407 | 0000240C | 春花 | — |
| 408-409 | 0000241B, 00002420 | 茜 | Q903, Q328 |
| 410 | 00002427 | 美冬, 417 cells | Q907, Q114 |
| 411 | 0000242E | 桃子 | Q913 |
| 412 | 00002433 | 茅萱 | Q802, Q840, Q914, Q915 |
| 413-417 | 00002439..00002457 | FIVE narrators; 415 alternates at every block boundary; 416 has one unnarrated block | Q928, Q932, Q933, Q937, Q943, Q944 |
| 418-421 | 0000245F..00002473 | 幸太郎, FOUR files, ~1,040 cells, no marker anywhere | Q964, Q965, Q967, Q973 |
| 422 | 00002478 | 茅萱, taken at the boundary | Q983, Q984, Q985, Q987 |

---

# I. GREP KEYS (things too long to carry; grep GLOBAL.md for the anchor)

- A converted / possessed character who sounds normal -> grep `CONVERTED` and `Q396`.
- The grammar-clue block (死んでいる vs 死んだ, the wrong 「でも」, the negation pair) -> grep `3.7 Aspect`.
- The five jobs of the 「――」 prefix in full, with every file id -> grep `1.3 The `.
- All five unmarked text formats (letters, memos, scripture, 戸籍, ceremonial, chat) -> grep `1.7 Bare`.
- Every full-width-space device with its site list -> grep `1.20 Full-width`.
- The one-kana-per-cell site list (~25 sites) -> grep `1.14 One kana`.
- The repeated-character walls with their counts -> grep `1.15 Repeated`.
- The complete replay concordance with every cell range -> grep `3.5 Verbatim`.
- Every narrator-switch seam with exact cell boundaries -> grep `3.2 Unmarked`.
- The inset-first-person site list -> grep `3.3 Inset`.
- The retraction table with cell ranges -> grep `3.4 Precognition`.
- The 124 typo ids and what the four kinds contain -> grep `4. Source-typo`.
- An owner query's full question and best guess -> grep the `Qnnn` id, then `2a. Blocking` or `2b. Owner`.
- A name form you meet that CORE does not list -> grep `4. Name index`, or `GLOSSARY-CORE.tsv` for the row.
- A character's full voice card, all registers with cell ranges -> grep the JP name in GLOBAL A§1.
- Who calls whom what, and the speech level per pair -> notes/GLOBAL-RELATIONS.md, `relations_select.sh`.
