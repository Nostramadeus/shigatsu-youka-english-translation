# NOTES-DIFF-c01-03.md — pass 1 vs pass 2 notes, read chunks 01-03 (39 files, 0000001E .. 000005AC)

Tag: DIFF1. Pass 1 = notes/CAST.md, RELATIONS.tsv, GLOSSARY.tsv, SUMMARY.md, QUERIES.md. Pass 2 = the same names under notes/v2/.
Scope rule: only facts whose as-of / cited cell id is 000005AC or lower (the 39 files of chunks 01-03). Later-chunk material in either pass is ignored.
Arbiter: the Japanese in read/chunk01-03.txt. Cell refs are file:row:line. "P1" / "P2" = the pass the JP supports.
"both" = both readings fit the JP, or the item is a wording/policy choice with the same meaning. "undecided" = a real difference the JP cannot settle.
One-pass items (a row, block, WITHHELD item or query that only one pass has) are counted as disagreements; the arbiter column then says whether the JP supports the item that is present.

Helper scripts (scratch, not notes): notes/v2/_tmp/diff1-jp.sh (JP cell lookup), notes/v2/_tmp/diff1-*.tsv / .txt (extracts).

## (a) Counts

| category | items compared | agree | disagree | P1 right | P2 right | both | undecided |
|---|---|---|---|---|---|---|---|
| CAST | 184 | 166 | 18 | 0 | 11 | 5 | 2 |
| RELATIONS | 56 | 29 | 27 | 5 | 17 | 5 | 0 |
| GLOSSARY (shared keys) | 228 | 125 | 103 | 0 | 3 | 68 | 32 |
| GLOSSARY (proper nouns in one pass only) | 55 | 0 | 55 | 0 | 9 | 46 | 0 |
| SUMMARY (narrator, time, WITHHELD) | 220 | 118 | 102 | 25 | 71 | 6 | 0 |
| QUERIES | 109 | 39 | 70 | 17 | 27 | 25 | 1 |
| total | 852 | 477 | 375 | 47 | 138 | 155 | 35 |

## (b) Disagreements with JP evidence

### 1. CAST

Compared: 26 speakers present in both passes x 5 fields (pronoun, speech-level baseline, copula, tics, dialect) = 130; 10 first-appearance / naming / gender facts; narrator identity for 39 files; 5 speakers present in one pass only. Total 184.

Speakers in both: なつみ, 春花, 五島, 茜, 美冬, 良治, 栄一郎 (named only in scope), 桃子, 五島's mother, 五島's father, 伊勢, 向井, man at the door, 死神, old detective (0000037D), interviewer (000003AE), patient (000003AE), police colleagues, 西佐波 radio operator, TV voices, rowdy high-schoolers (000003A8), ザッハ customers (00000564), ザッハ staff, police receptionist, board posters, voice flood (00000488:48).

| # | speaker / field | P1 says | P2 says | deciding JP | verdict |
|---|---|---|---|---|---|
| C1 | なつみ / pronoun frequency | 私 MORE often than typical | about as often as typical | a frequency judgement; no line decides it | undecided |
| C2 | なつみ / speech level | casual to 美冬 "despite the age gap"; 敬語 to 伊勢 is "no other living adult" | adds 丁寧 + あなた to 美冬 in 00000564 | 00000564:11:165-166 「あなた……／本当におばさんなの……？」; 11:171-172 「おばさん……春花のお父さんのこと……／さっき聞きました。本当に……すみませんでした」 | P2 |
| C3 | 春花 / speech level | "No 敬語 observed to anyone" | polite to 五島's sister; ごめんなさい as a register break; mock 五島様 (speaker inferred, V032) | 0000034C:11:30 「あの……すみません、お邪魔します」 with 11:31 「先輩が横から顔を出した」; 000004E3:11:39-40 「ご……ごめんなさい……！／なつみ……！　ごめんなさい！」; 000002F6:11:78 「五島様……すみませんでした。もう勘弁して下さい……」 | P2 |
| C4 | 五島 / speech level | 敬語 to both 先輩, to 伊勢 and to 茜, "unbroken" | 丁寧 with plain slips; plain form in text messages to 春花 | 000002FA:27:8 "待って！　勘違いだから！　先輩！", 27:11 "先輩、つらいよね？　苦しいよね？ 話して。全部聞くから。"; 000004BB:8:38 「伊勢さん大丈夫？」; 00000550:11:130 「おじさん、いろいろありがとね！」 | P2 |
| C5 | 茜 / pronoun frequency | less often than typical | about as often as typical | frequency judgement | undecided |
| C6 | old detective / speech level | 丁寧, copula です | タメ口 (avuncular) with polite formulae | plain: 0000037D:11:43 「五島絵梨奈さんだね。ゆうべは大変だったね」, 11:47, 11:50 「何か分かるかな？」; polite: 11:41 「おお、気がついたんですね」, 11:67 「失礼しました。それならいいんですよ」 | P2 |
| C7 | patient / speech level | 丁寧 "even while shouting, the single most distinctive thing" | 丁寧, drops to plain in the outburst | 000003AE:8:20 「どうしてって聞いてるじゃないですか！」 (polite), 8:22 「私は誰も助けられないの！　もうやめてよ！」 (plain) | P2 |
| C8 | 春花 / first appears | 00000024:16:11 (spoken to) | 00000024:16:8 (first line 16:13) | 00000024:16:8 「右を見ると、春花が私の肩にもたれ、すやすやと眠っている」 | P2 |
| C9 | 美冬 / first appears | 000001DD:11:74, quoting 「あ痛！」 | 000001DD:11:73 | 000001DD:11:73 「あ痛！」; 11:74 is narration | P2 |
| C10 | 良治 / first named | "NAMED on screen at 000004E3:11:1" | full name at 0000034C:11:136 | 0000034C:11:136 「古郡良治、先輩のお父さん。」 | P2 |
| C11 | 美冬 / name | "CONFIRMED at 0000037D:11:58 ... from 0000037D:11:58 onward the name may be used" | name on a doll only; identity by inference (V042); linked to 春花's mother at 00000550:11:72 | 0000037D:11:57-58 「新村春花」「新村美冬」 (two dolls, no link); 00000550:11:72 「新村さんのお母さんである美冬さん」 is the first explicit link | P2 |
| C12 | interviewer (000003AE) / gender | "every line of his" | ungendered ("examiner") | no gendered word in 000003AE; lines are 「――」-prefixed only (8:21, 8:24, 8:51-55) | P2 |
| C13 | narrator 000004BB:16 | なつみ 16:0-36, 五島 from 16:37 | なつみ 16:2-36, 五島 from 16:41 | 16:37 「おじさんごめん、電話だ」 is spoken at 五島's end; 16:41 「不審者……？」 is the first narration cell on her side | both |
| C14 | navigator (000000F2) | own CAST block | no block; deferred to V002, listed in RELATIONS as "unnamed guide" | 000000F2 has the わたくし voice | both |
| C15 | red dream figure | no block; tracked inside なつみ + Q016 | own block | 000001E1:33:10 「男とも女ともつかぬうめき声」 | both |
| C16 | officer answering 良治's phone | no block; mentioned in 良治's block | own block | 000004E3:11:1 「こちらは古郡良治さんの携帯です」 | both |
| C17 | epilogue speakers 00000522:11:171-175 | no block; in SUMMARY | own block | 11:171-175 untagged, call her なつみ | both |
| C18 | figure at a distance (00000488) | absent | own block (no lines) | 00000488:34:118 「遠くに立っている誰かを見ているようだ」 | P2 |

Agreements worth stating (no row above): 私 for なつみ / 春花 / 五島; 伊勢's 私/俺 split; 良治's 俺 and letter register; 桃子's two registers; 茜's ～わよ／～なさい; 美冬's stretched register and its flat unmasked form (00000564:11:179-191); the 死神 has no lines; 38 of 39 narrator assignments.

CAST: 184 compared, 166 agree, 18 disagree: P1 0, P2 11, both 5, undecided 2. (checkpoint 1 done)

### 2. RELATIONS

Compared: 39 ordered pairs present in both (in-scope rows), 8 pairs only in P1, 9 pairs only in P2. Total 56.
Rows that differ only in wording of the same forms (e.g. 良治→茜 "plain, terse" vs "written plain") count as agree.

| # | pair | P1 says | P2 says | deciding JP | verdict |
|---|---|---|---|---|---|
| R1 | 五島→春花 | 敬語 (です・ます), "never drops" / "unbroken" | plain form in text messages (000002FA) | 000002FA:27:8 "待って！　勘違いだから！　先輩！"; 27:11 "先輩、つらいよね？　苦しいよね？ 話して。全部聞くから。私、味方だから。" | P2 |
| R2 | 五島→伊勢 | 敬語, comic layer gone | 丁寧 with plain slips | 000004BB:8:38 「伊勢さん大丈夫？」; 00000550:11:130 「おじさん、いろいろありがとね！」 | P2 |
| R3 | 伊勢→五島 (000004A7) | "plain-form barking, then flustered 丁寧" | タメ口 with stiff official lines | 000004A7:11:94 「えーっと、五島絵梨奈さん」, 11:96-97 「君の考えを聞いてみたい。場所を変えて俺と……その……／はは、話をしよう！」 (plain) | P2 |
| R4 | 春花→伊勢 | "no address form; おじさん once", citing 00000550:11:130 「ありがとう、伊勢さん！」 | 伊勢さん, タメ口 (speaker inferred, V066) | 00000550:11:130 「ありがとうございます！」⏎「ありがとう、伊勢さん！」⏎「おじさん、いろいろありがとね！」; おじさん is 五島's form for him (000004BB:16:37-38), so 春花's cell is 「ありがとう、伊勢さん！」. P1's row contradicts its own quote | P2 |
| R5 | なつみ→美冬 | casual, no 敬語 (000001DD row only) | adds 00000564: 丁寧, あなた, kneeling apology | 00000564:11:165-166, 11:171-172 (see C2) | P2 |
| R6 | old detective→五島 | 丁寧, folksy | タメ口 gentle, polite formulae | see C6 | P2 |
| R7 | 伊勢→なつみ | 00000538:11:25 「古郡なつみさん」 assigned to 伊勢 (P1's CAST assigns the same cell to a staff member) | speaker not tagged (V072) | 00000538:11:16 「新村春花さんだね。2階へ行ってもらえるかな」, 11:25 「それと、古郡なつみさん、君には地下に来てもらいたい」 — untagged; 「それと」 continues the 11:16 speaker | P2 |
| R8 | 伊勢→subordinates | by rank, "never by name" (おい, 巡査部長) | adds 君 | 000003B4:8:26 「君は年上好きなのか？」 | P2 |
| R9 | interviewer→patient | no address; 「××さん」 on the phone | none | 000003AE:8:52-54 「――もしもし。すみませんが、」「××さん」「は常時監視してください。」 | P1 |
| R10 | 桃子→五島 | あんた; 0000057B:11:89 is "her first use of the given name on screen" | あんた; 3p 絵梨奈 to her mother at 0000037D:11:5 | 0000037D:11:5 「おかあさーん！　絵梨奈が目開けたよー！」 with 11:7 「この声は……お姉ちゃんだ」 | P2 |
| R11 | P1-only: 五島→なつみ's parents | お父さん / お母さん | — | 0000020B row cited by P1; P2 has no row | P1 |
| R12 | P1-only: 五島's father→桃子 | 桃子 | (in P2's "why" column: 3p 桃子, 000002F8:12:17) | same forms | both |
| R13 | P1-only: 佐波放送 reporter→bystanders | すみません, 丁寧 | — | 000003A8:8:5 「――すみません、こちら佐波放送の者ですが……。」 | P1 |
| R14 | P1-only: 良治→春花 / 五島 / 美冬 (3 rows) | 春花ちゃん / 五島ちゃん / 美冬さん | same forms in the "why" column of 良治→なつみ and 良治→茜 | 00000538:11:109-111; 00000564:11:102-114 | both (x3) |
| R15 | P1-only: 西佐波 radio→伊勢 | no address, 丁寧 radio procedure | — | 000004F9:11:136 「――こちら西佐波警察。聞こえ――ますが、少し――途切れます。どうぞ」 | P1 |
| R16 | P1-only: ザッハ customers | タメ口, ～だって | — | 00000564:11:3 「ねえねえ、今日死んだの、あの子のお父さんだって」 | P1 |
| R17 | P2-only: 茜→春花 | (in P1's "why" column: 春花ちゃん) | 春花ちゃん (3p) | 000001DD:11:44 | both |
| R18 | P2-only: 春花→美冬 | — | お母さん (3p 000001DF; direct 00000564) | 00000564:11:175 「お母さん……何してんだよ……」 | P2 |
| R19 | P2-only: 桃子→her mother | — | おかあさーん | 0000037D:11:5 | P2 |
| R20 | P2-only: 五島's mother→桃子 | — | 桃子 | 0000037D:11:74 「桃子……もうやめなさいよ」 | P2 |
| R21 | P2-only: patient→interviewer | — | 先生 | 000003AE:8:40 (cited by P2) | P2 |
| R22 | P2-only: 伊勢↔ザッハ waitress (2 rows) | generic "staff→customers: お客様" | お客様 / 君 | 000004BB:8:12 「き、君！」, 8:14 「な、なんでしょうかお客様……」 | P2 (x2) |
| R23 | P2-only: 伊勢→美冬 | — | 新村美冬 (bare full name, arrest) | 00000564:11:182 「新村美冬！　殺人および死体遺棄の容疑で緊急逮捕する！」 | P2 |
| R24 | P2-only: 春花→桃子 | — (P1 CAST: no 敬語 to anyone) | すみません, 丁寧 | 0000034C:11:30 「あの……すみません、お邪魔します」 | P2 |

Counting note: R14 is three pairs and R22 is two pairs, so the table has 24 rows for 27 disagreeing pairs.
RELATIONS: 56 compared, 29 agree, 27 disagree: P1 5 (R9, R11, R13, R15, R16), P2 17 (R1-R8, R10, R18-R21, R22 x2, R23, R24), both 5 (R12, R14 x3, R17), undecided 0. (checkpoint 2 done)

### 3. GLOSSARY

Compared: 228 jp keys present in both passes whose first_seen (either pass) is in scope. 125 agree: 63 identical EN, 62 cosmetic only (article, capital, punctuation, or P2 "TBD (X)" with the same X). 103 differ in wording.
Verdict key for the 103: P2 / P1 = the JP context makes one rendering wrong in meaning; both = same meaning, wording choice; undecided = rendering-policy choice (romanize vs translate, proper-noun form, interjection spelling) that the JP cannot settle — these go to STYLE/owner, not to the text.

JP-decided rows:

| key | P1 | P2 | deciding JP | verdict |
|---|---|---|---|---|
| 補導 | taken into custody | taken in (as a minor) | 00000473:11:53 「でも、警戒中の警察官に職務質問されたら、銃刀法違反で補導されるかもしれない。」 — 補導 is juvenile guidance, not custody | P2 |
| ツーツー | the dial tone | beep... beep... | 000002FA:11:75 「ツーツーという電話からの音がしばらく鳴り響いた。」 — the tone after the other side hangs up, not a dial tone | P2 |
| 宗派 | a Buddhist sect | sect | 00000564:11:72 「うちって何か宗派とかあるのかな。⏎新村家は特別な宗派みたいだけど。」 — nothing says Buddhist | P2 |
| 十三回忌 | the thirteenth-year memorial (note: 12 years after, TN) | the twelfth-anniversary memorial service | 000002F8:12:33 「今からちょうど12年前の今日」 + 12:78 「十三回忌」 — both notes state the 12-year count | both |
| 面会 | a visit | visiting hours (prison) | 0000033D:11:17 「面会にはまだ早いぞ？」 (jail joke) | both |

All 103 wording differences (P1 = pass 1 EN, P2 = pass 2 EN):

| key | cat P1/P2 | P1 | P2 | verdict |
|---|---|---|---|---|
| 元木町 | place/place | Motoki-cho | TBD (Motoki Town) | undecided |
| 元木高校掲示板 | place/ui | the Motoki High board | Motoki High message board | both |
| 女ケ沢市事件 | event/event | the Megasawa City murders | TBD (the Megasawa City case) | both |
| 中央公園 | place/place | Chuo Park | TBD (Central Park) | undecided |
| 御神木 | object/term | the goshinboku | the sacred tree | undecided |
| 危険予知 | term/concept | danger sense | danger premonition | both |
| 惨殺死体 | term/term | brutalized body | brutally murdered body | both |
| 神隠し | term/concept | spiriting-away | TBD (spirited away) | both |
| 愉快犯 | term/term | thrill-killer | someone who commits crimes for the thrill | both |
| 鉈 | object/object | nata | hatchet | undecided |
| 脳挫滅 | term/term | crushing of the brain | crushed brain | both |
| 通り魔 | term/term | random attacker | random street attacker | both |
| 参考人 | term/term | person of interest | person of interest / witness | both |
| 霊安室 | place/place | the mortuary | morgue | both |
| 聞き込み調査 | term/term | door-to-door questioning | door-to-door inquiries | both |
| 桜祭り | event/event | the Cherry Blossom Festival | cherry-blossom festival | both |
| 先輩 | address/title | -senpai / Senpai | Senpai | undecided |
| ニカッと | term/term | grinned from ear to ear | grin / a big grin | both |
| ノ | term/ui | o/ | TBD (raised-hand sign) | undecided |
| 釣り乙 | term/term | nice bait | TBD (nice try, troll) | undecided |
| オフ会 | term/term | meetup | offline meetup | both |
| 雑談 | ui/ui | chatter | Chats | both |
| 解禁 | ui/ui | unlock | unlock / unlocked | both |
| 呪殺編 | title/title | the Jusatsu Arc | TBD | undecided |
| 明徴編 | title/title | the Meicho Arc | TBD | undecided |
| 中継 | term/term | live from the scene | live report | both |
| 闇の熾天使 | person/person | the Dark Seraph | Seraph of Darkness | undecided |
| さきいか | food/food | sakiika | shredded dried squid | undecided |
| きんぴらごぼう | food/food | kinpira gobo | braised burdock root | undecided |
| あは | interjection/interjection | Heh | Aha | undecided |
| ふふ | interjection/interjection | Hee | Heh | undecided |
| ほほほ | interjection/interjection | Hohoho | TBD (Ohoho) | undecided |
| よいしょ | interjection/interjection | Heave-ho | Hup / Heave-ho | undecided |
| もぐもぐ | sfx/sfx | nom nom | munch munch | undecided |
| 花見 | term/event | hanami | TBD (cherry-blossom viewing) | undecided |
| 花見客 | term/term | hanami visitor | cherry-blossom viewers | undecided |
| 十三回忌 | term/event | the thirteenth-year memorial | TBD (the twelfth-anniversary memorial service) | both |
| 命日 | term/term | the anniversary of a death | the anniversary of his death | both |
| 単身赴任 | term/term | a posting away from the family | transferred away alone (family stays behind) | both |
| 自首 | term/term | turning oneself in | turn myself in | both |
| ツーツー | sfx/sfx | the dial tone | TBD (beep... beep...) | P2 |
| 紙人形 | object/object | a paper figure | paper doll | both |
| 死神 | term/concept | shinigami | TBD (Death / a death god) | undecided |
| 赤装束 | object/object | red vestments | TBD (red robes) | both |
| 事情聴取 | term/term | a formal statement | questioning | both |
| 警部補 | term/title | Assistant Inspector | TBD (Lieutenant) | undecided |
| 元木美少女同好会 | org/org | the Motoki Bishojo Appreciation Society | TBD (the Motoki Pretty Girl Appreciation Society) | undecided |
| 美少女愛好家 | term/term | connoisseur of beautiful girls | TBD (a devotee of pretty girls) | both |
| 監視カメラ | object/object | security cameras | security camera | both |
| 警察手帳 | object/object | a police ID | police badge | both |
| キャリア組 | term/term | the career track | career-track officers | both |
| 盗難車 | term/term | a stolen vehicle | stolen car | both |
| 銃刀法違反 | term/term | violating the Firearms and Swords Law | violating the weapons law | both |
| 職務質問 | term/term | a police stop | stopped and questioned by the police | both |
| 補導 | term/term | taken into custody | taken in (as a minor) | P2 |
| 麻薬 | term/term | narcotics | drugs | both |
| あっちい | interjection/interjection | That's hot! | Hot! | undecided |
| イケメン | term/term | a looker | a hunk / good-looking | both |
| JK | term/term | JK | TBD (high-school girl) | undecided |
| ソメイヨシノ | term/term | Somei Yoshino | Somei-yoshino cherry | both |
| 樹齢 | term/term | tree age | (tree) age | both |
| かりそめの友情 | term/concept | a friendship that was never real | TBD (a make-believe friendship) | both |
| 西佐波警察 | org/org | Nishisawa Police | TBD (West Sawa Police) | undecided |
| つばぜり合い | term/term | a blade lock | locked blade to blade | both |
| ブレーキ痕 | term/term | brake marks | skid marks | both |
| 焼死体 | term/term | a body burned to death | burned body | both |
| パトランプ | object/object | the patrol car's light bar | the police car's light | both |
| 社会復帰 | term/term | returning to society | return to normal life | both |
| 供花 | object/object | memorial flowers | funeral flowers | both |
| カラス | term/term | crows | crow(s) | both |
| 年忌 | term/term | memorial years | memorial anniversaries | both |
| 三回忌 | term/event | the third-year memorial | TBD (third memorial) | both |
| 七回忌 | term/event | the seventh-year memorial | TBD (seventh memorial) | both |
| 十回忌 | term/event | the tenth-year memorial | TBD (tenth memorial) | both |
| 十年祭 | term/event | the ten-year rite | TBD (tenth-year rite) | both |
| 黒歴史 | term/term | my dark history | embarrassing past | both |
| 死体遺棄 | term/term | abandonment of a corpse | abandoning a body | both |
| 緊急逮捕 | term/term | an emergency arrest | arrest (on the spot, without a warrant) | both |
| 衆人環視 | term/term | in front of this many witnesses | in front of all these people | both |
| 宗派 | term/term | a Buddhist sect | sect | P2 |
| 広告塔 | term/term | an advertising figurehead | poster child | both |
| 超炭酸ボンバー | food/brand | Ultra Fizz Bomber | TBD (Super Soda Bomber) | undecided |
| はひ | interjection/sfx | Buh? | Huh? | undecided |
| ふぁあ | interjection/sfx | Hwuh? | Whaa? | undecided |
| うひょー | interjection/interjection | Whoo | Woo-hoo! | undecided |
| ぶあっぺ | sfx/sfx | Pbbaht | Bwahpff! | undecided |
| ったく | interjection/interjection | Honestly | Geez | undecided |
| 怪人 | term/term | the figure | TBD (the strange figure) | both |
| 実行犯 | term/term | the one who carried it out | the one who does the killing | both |
| 面会 | term/term | a visit | visiting hours (prison) | both |
| 桜吹雪 | term/term | a blizzard of cherry petals | a storm of cherry petals | both |
| 主犯 | term/term | the principal | mastermind | both |
| 元木町事件 | event/event | the Motoki-cho incident | TBD (the Motoki Town case) | undecided |
| 取調室 | place/place | an interview room | interrogation room | both |
| パトカー | object/object | a patrol car | police car | both |
| 冥福 | term/term | peace for the dead | rest in peace | both |
| 土下座 | term/term | a kowtow | get down on my knees and bow | both |
| 発作 | term/term | an attack | attack / fit | both |
| スマホ | object/object | a smartphone | phone / smartphone | both |
| 郵便受け | object/object | the mailboxes | mailbox | both |
| 表札 | object/object | the nameplate | nameplate (on a door) | both |
| おかゆ | food/food | rice gruel | rice porridge | both |
| 作戦遂行 | refrain/term | on to carrying out the Operation | TBD ("carry out the operation") | both |

Proper-noun keys present in only one pass (categories person/place/org/brand/title/event/era/address, first_seen in scope): 55.
- P2 only, 51. 42 of them are keying differences, not gaps: P2 keys bare names, suffixed forms and kin terms (なつみ, 春花, 伊勢, 五島, 茜, 美冬, 桃子, 絵梨奈, 古郡, 新村, 古郡先輩, 新村先輩, せーんぱい, 春花ちゃん, なつみちゃん, 絵梨奈ちゃん, 五島ちゃん, おばさん, お母さん, お父さん, 母ちゃん, お姉ちゃん, お姉さん, 後輩, 古郡家, 伊勢警部補, 警部補殿, 天才美少女, 女ケ沢, and common place/event nouns 駐輪場, 丁字路, 警察署, 病室, 受付, 実家, 葬儀屋, ベランダ, 県道, 外科医, 入試, 墓参り, マンション) where P1 keys full names or has the forms inside CAST/STYLE -> both.
- 9 are real gaps in P1, all present in the JP: 東北 (000001DD:11:13), ピザフェア (000004BB:16:2), and the seven landmarks of 春花's geography gag 自然史博物館, エッフェル塔, チリ, パリ, ピサの斜塔, サグラダファミリア, ヨーロッパ (00000595:11:79-87) -> P2. P1 covers the gag only as Q069 ("keep the same landmarks") with no fixed EN.
- P1 only, 4: 古郡なつみ, 古郡茜, 五島桃子 (full names, from the cast list; P2 keys the parts) and 四月八日 (date) -> both.

GLOSSARY: 228 shared keys compared, 125 agree, 103 disagree: P1 0, P2 3, both 68, undecided 32. One-pass proper nouns: 55, all disagree by definition: P2 9, both 46. (checkpoint 3 done)

### 4. SUMMARY

Narrator per file: 39 compared, 38 agree. The one difference is the 000004BB:16 switch point, recorded as C13 (both). 000004CF 12:0 vs 12:1 as the first なつみ cell is not counted (12:0 is a bare line either way).
Time markers per file: 39 compared, 39 agree. No marker in one pass contradicts the other. P1 adds interpretive placements (for example 00000595 "set on the afternoon of 四月八日, before orders 30-37"); P2 says the same file is "a different route" in the afternoon. Both fit 00000595:11:8-10 (「おととい」 / 「昨日の朝」 / 「昨日」).

WITHHELD items: P2 has a WITHHELD line per file; P1 has an "ambiguity that the translation MUST keep open" list that mixes withheld content with typesetting notes. Only content items (unnamed or ungendered referents, cut-off sentences, unexplained facts, unmarked speakers) are compared; pure format notes (cell splits, quote styles, ruby residue) are left to section 5. 142 items: 41 listed by both, 101 by one pass only.

The only item where the passes CONTRADICT each other rather than one omitting it is 0000037D:11:58 (新村美冬): P2 lists her identity as withheld in that file; P1 CAST calls the name confirmed there. JP 11:57-58 gives two bare names on dolls; the link to 春花's mother is first made at 00000550:11:72. -> P2 (same as C11).

One-pass items. The JP column is the first cell the listing pass cites (pulled by script); every cell exists and says what the listing pass says. verdict = the listing pass, except five items the other pass records elsewhere (marked both).

| cell | listed by | item | JP (first cited cell, truncated) | verdict |
|---|---|---|---|---|
| 00000024:16:35 | P2 | how she "killed" anyone is not stated | 私が殺したも同然なのだ。 | P2 |
| 00000024:16:57 | P2 | 事件 unnamed | 後悔どころか、私の力の及ばないところで事件は動いていたのだ。 | P2 |
| 00000024:47:37 | P2 | 死神 unexplained | もし、お母さんが死神にならなかったら。 | P2 |
| 00000024:47:41 | P2 | 私が魔女になった時 unexplained | 昔、私が魔女になった時、何があったのだろうか……。 | P2 |
| 00000024:51:6 | P2 | syringe contents unexplained | それは、桃色の液体が入った注射器だった。 | P2 |
| 00000024:16:27 | P1 | 私は本物の魔女だって is a quotative report (P2 raises it as V028, not in SUMMARY) | 「ねえ春花、覚えてる？　私は本物の魔女だって」 | both |
| 00000024:47:17 | P1 | お父さん = 春花's father by context only | お父さんが木から落ちる時、落下する軌道がずれたのだ。 | P1 |
| 00000024:51:9 | P1 | 51:9-13 untagged alternating lines | 「何なんだろ、これ……」 | P1 |
| 000001DB:15:186 | P2 | 誰かが倒れている unnamed, ungendered | 桜の木の下で、誰かが倒れている。 | P2 |
| 000001DB:15:155 | P2 | why the mother is uneasy with her phone (P1 has it in CAST 古郡茜) | お母さんが妙にそわそわしている。 | both |
| 000001DB:15:8 | P2 | 春花たち group not listed | お祭りに誘ってくれたのはありがたいけど、私にとって桜祭りなんて自殺行為だ。 | P2 |
| 000001DB:15:103 | P1 | Hokkaido trip is the mother's report only | 「急に北海道に出張になったって。帰るのは来週だそうよ」 | P1 |
| 000001DD:11:6 | P2 | cause of sirens not stated | 事故でもあったのだろうか。 | P2 |
| 000001DD:11:24 | P2 | why the mother is sleepy | 朝に強いはずのお母さんがずいぶんと眠そうだ。 | P2 |
| 000001DF:11:96 | P2 | relative who likes impressions unnamed | 「別にそんな……私の親戚にモノマネ好きなやつがいるだけだって」 | P2 |
| 000001E1:33:48 | P2 | what the red person wants | 充血した目を見開き、話せない代わりに強烈な眼光で何かを訴えようとしているような― | P2 |
| 000001E1:33:57 | P2 | dream cut off before the figure acts | 私がそう言うと――。 | P2 |
| 000001E3:8:122 | P2 | dead flower-viewer unnamed, ungendered | しかしそれよりも数年前の四月八日に、 | P2 |
| 000001E3:8:154 | P2 | unattributed 「…………？　あれ……？」 | 「…………？ | P2 |
| 000001E3:8:182 | P2 | Goto's grave look unexplained | 五島は一瞬神妙な顔つきになったが、 | P2 |
| 000001E5:23:80 | P2 | what Goto wrote and erased | 私がそう言うと、五島はメモ帳を隠すようにして何かを書きだした。 | P2 |
| 000001E5:41:13 | P2 | Goto's intent cut off | 「せーんぱい！」 | P2 |
| 000001E5:41:0 | P1 | 「ダメ！」 subjectless until next line | 「ダメ！」 | P1 |
| 000001E7:11:16 | P2 | Haruka's reason for hiding from police: stated reason only | 「聞き込み調査か……。ってことは、うちにも来たんだろうなあ……」 | P2 |
| 0000020B:12:32 | P2 | 誰か subject | 誰かが「まさか」と思った。 | P2 |
| 0000020B:12:61 | P2 | when the cherry aversion began | 「え？　さあ……気がついたら、ずっと嫌いだったな。小さい頃は一緒に花見にも行った | P2 |
| 0000020B:12:0 | P1 | narrator never named in the file | 時計はちょうど19時を示している。 | P1 |
| 0000020D:11:19 | P2 | intuition "law" is Goto's hypothesis | 先輩の直感というのは、被害に遭う人が | P2 |
| 000002F6:11:12 | P2 | the action she is about to take | 今なら、まだ行動を起こさずに騙さなかったことにできる。 | P2 |
| 000002F8:12:2 | P2 | sister unnamed except via 桃子 at 12:17 | お姉ちゃんは、また男と遊び歩いているに違いない。 | P2 |
| 000002F8:12:81 | P2 | sentence cut off | もし新村さんの命日を意識して今朝の事件が引き起こされたなら――。 | P2 |
| 000002F8:12:89 | P1 | 「一緒にいて」 vs other files' wording (P2 raises it as V036, not in SUMMARY) | 昼に3人でザッハを出ようとしたとき、古郡先輩は私に「一緒にいて」と言った。 | both |
| 000002FA:11:23 | P2 | 妙に引っ掛かる言い回し unexplained | 「へえ……五島は今、家に1人なのか。 | P2 |
| 000002FA:19:10 | P2 | how 春花 would kill なつみ | "私、このままだとなつみを殺してしまう。助けてくれ。なつみを助けてくれ。なつみを� | P2 |
| 000002FA:23:0 | P2 | claim of killing なつみ's father, method unstated | なつみのお父さんを殺したんだぞ | P2 |
| 000002FA:27:9 | P2 | why なつみ cannot be saved | "でも多分、もうなつみは助からない。" | P2 |
| 0000033D:11:43 | P2 | 春花's reason for staying away | 四月八日に新村先輩は豹変するとでも言いたいのだろうか。 | P2 |
| 0000033D:11:77 | P1 | abandoned sentence | 「でも……！　お前に頼ったって…… | P1 |
| 0000034C:11:97 | P2 | what she could not bear | 「私が初めて人を呪い殺したのは、10年前に住んでいた女ケ沢市っていうところで……。 | P2 |
| 0000034C:11:264 | P2 | what 五島 overlooks | 何なのだろうか、この違和感は。 | P2 |
| 0000034C:11:201 | P2 | 死神になったお父さん unexplained | 　死神になったお父さんが私の願いを聞き入れてくれてるんだよ！」 | P2 |
| 0000034C:11:166 | P1 | 吐き出したもの double meaning | 「これ、私が吐き出したものなんだ」 | P1 |
| 00000366:11:68 | P2 | who killed the three | 床に血が広がり、壁にも大量の血が飛び散っていた。 | P2 |
| 00000366:11:77 | P2 | sentence cut off | 振り返ると、新村先輩がそこに――。 | P2 |
| 00000366:11:70 | P1 | bodies listed by relationship, not name | 頭部から大量の血を流して倒れている新村先輩のお母さん。 | P1 |
| 0000037D:11:50 | P2 | who put the dolls in the pocket | 「これ、君のポケットから見つかったんだけど、何か分かるかな？」 | P2 |
| 0000037D:11:83 | P2 | what 五島 realised | そうか……。そういうことだったのか……。 | P2 |
| 0000037D:11:34 | P2 | cause of the fire | 「その後、古郡家は火事になって、玄関にいたあんただけギリギリ助け出されたって。 | P2 |
| 0000037D:11:58 | P2 | 新村美冬 not identified in this file (conflicts with P1 CAST) | 新村美冬 | P2 |
| 0000037D:11:29 | P1 | four deaths, zero names | 「落ち着いて聞いて。みんな、死んじゃったってよ。 | P1 |
| 000003A8:8:5 | P1 | nobody named, no tags | ――すみません、こちら佐波放送の者ですが……。⏎「お！　インタビュー！？　インタ | P1 |
| 000003AE:8:9 | P2 | who the pictured person is | ――この人は誰だか分かる？ | P2 |
| 000003AE:8:58 | P2 | what the patient did with the tongue | 舌を……！？ | P2 |
| 000003B4:8:24 | P2 | suspicion about the 警部補 unexplained | 「そりゃそうだけど……。でも、いざとなったら警部補が何かするんじゃないの？」 | P2 |
| 000003B4:8:0 | P1 | briefing speaker established only at 8:14 | 「それでは、お手元の資料をご覧ください。 | P1 |
| 000003B4:8:15 | P1 | a gossip speaker's sex never stated | ――そりゃ警部補は、元木町一の美少女愛好家だからな。 | P1 |
| 000003BC:8:16 | P2 | when the scene happens (P1 gives "late" as a time marker) | それに今から捜索してもこの時間じゃ無理ですよ」 | both |
| 000003BC:8:6 | P1 | one speaker or two | 「白のミニバン、中央公園の屋台準備用の車……。 | P1 |
| 00000460:11:45 | P1 | あの2人 inferred | あ、どうせ行くなら、あの2人も誘ってみようかな……。 | P1 |
| 00000488:34:118 | P2 | far figure ungendered | 遠くに立っている誰かを見ているようだ。 | P2 |
| 00000488:11:4 | P2 | さっきの人 unnamed | さっきの人がやったの？ | P2 |
| 00000488:48:7 | P2 | 荒田集落 and 麻薬 unexplained | 能面を着けて　これが荒田集落の習わし　麻薬……？ | P2 |
| 000004A7:11:9 | P2 | さっきの先輩の夢 / what was odd | 目を閉じると、さっきの先輩の夢が思い出される。 | P2 |
| 000004A7:11:96 | P2 | Ise's intent | 「君の考えを聞いてみたい。場所を変えて俺と……その…… | P2 |
| 000004BB:8:47 | P2 | Goto's doubt about Ise | 私は会った時から、直感で伊勢さんに疑問を持っていた。 | P2 |
| 000004BB:16:61 | P2 | which 先輩 told Ise | 「やっぱりそうか……。新村さんとこ、大変だったって先輩から聞いたことがあるからね | P2 |
| 000004BB:16:62 | P2 | content of Ise's account withheld | こうして私は、初めて警察官の顔を見せる伊勢さんの口から、新村先輩のお父さんの死を | P2 |
| 000004BB:16:29 | P1 | 不審者 is hearsay through two people | 「なつみ……五島が……ザッハで不審者といるって……」 | P1 |
| 000004CF:12:96 | P2 | person beside 古郡先輩 not named | 古郡先輩の隣にいる人は……！ | P2 |
| 000004CF:12:56 | P2 | what 春花 denies | 「違う……！　なつみ、違うんだ……！ | P2 |
| 000004CF:25:11 | P2 | だって春花は―― cut off | だって春花は――」⏎「なつみ！」 | P2 |
| 000004CF:12:80 | P2 | nature of the 古郡家/新村家 feud | 12年前の事故、今回の事件、古郡家と新村家の確執、そして古郡先輩の夢。 | P2 |
| 000004E3:11:41 | P2 | what なつみ has guessed | 私はなんとなく勘付いていた。 | P2 |
| 000004E3:11:66 | P2 | flat belief, no hedge | 私のお父さん、殺されたのに。 | P2 |
| 000004E3:27:46 | P2 | 今朝実際に―― cut off | 「でも……でも、今朝実際に――」 | P2 |
| 000004E3:27:28 | P2 | source of かりそめの友情 | 一瞬、かりそめの友情という文言が浮かんだ。 | P2 |
| 000004E3:15:0 | P1 | bare-line blocks, speech not marked as speech | 今まで6人殺した。 | P1 |
| 000004E3:11:106 | P1 | 多分 hedge | 「多分……」 | P1 |
| 000004F9:11:64 | P2 | Goto's guess not stated | 「ここからは私の推測でしかないんですが…… | P2 |
| 000004F9:11:36 | P1 | 春花's half cut off | 「はい……もしも――」⏎「もしもし先輩！？　いったいどこにいるんですか！？　古郡 | P1 |
| 0000050E:11:163 | P2 | what happened to 春花 not shown | 「は……春花……？」 | P2 |
| 00000522:11:143 | P2 | 止められたはずなのに止めなかった人 unnamed | こんなことを起こした人へ、そして止められたはずなのに止めなかった人への怒りに身体 | P2 |
| 00000522:11:0 | P1 | opening is hearsay | これは聞いた話ではあるが。 | P1 |
| 00000538:11:15 | P2 | why the mother pities 春花 | 心なしか、お母さんの目は、春花を憐れんでいるようにも見えた。 | P2 |
| 00000538:11:162 | P2 | お父さんは一体何をしたの open | お父さんは……一体何をしたの？ | P2 |
| 00000538:11:181 | P2 | 前もこうだった unexplained | 「あいつら、何も分かってない……！　前もこうだった……」 | P2 |
| 00000538:11:57 | P1 | 『何か』 uncommitted word | その上には、白い布をかぶせられた『何か』。 | P1 |
| 00000538:11:18 | P1 | quoted label is her guess | 「殺人容疑での事情聴取」なのだろうか。 | P1 |
| 00000550:11:36 | P2 | bullies unnamed | 「被害者はいずれも、新村さんが女ケ沢市で通っていた学校と関係のある者ばかりだった | P2 |
| 00000550:11:100 | P2 | who placed the dolls | どうやったのかは知らないけど、何らかの方法で紙人形を置いたやつがいる。新村家に罪 | P2 |
| 00000550:11:83 | P1 | third figure held back across a cell break | 「ああ、やっぱり無意識のうちに作ったみたいだよ……。なつみのお父さんと、お母さん | P1 |
| 00000564:11:200 | P2 | where they went | いくら目を凝らしても、人影が全く見当たらない。 | P2 |
| 0000057B:11:83 | P2 | Goto's self-protection named without detail | 五島の中には、まだどこか幼さの残る自己保身精神があるようだ。 | P2 |
| 0000057B:11:41 | P1 | deliberate lie, meaning unspoken | 「この前の先輩の手紙、面白かったですよ！　でも私からの手紙は、人に見つからない場 | P1 |
| 00000595:11:107 | P2 | why 春花 will not talk about her father | 多分、お父さんのことは触れられたくなかったのだろう。 | P2 |
| 00000595:11:96 | P2 | blank in なつみ's memory after the hanami | あれ？　ここから先がぼんやりとしていて思い出せない。 | P2 |
| 00000595:11:92 | P1 | デブ said casually as part of the lie | うん、ま、まあ、大きいっていうより、はっきり言ってデブだよ。お母さんより背が低い | both |
| 000005AC:11:89 | P2 | what 春花 still cannot say | 春花の顔が曇った気がする。 | P2 |
| 000005AC:11:129 | P2 | why she cannot go home | 五島の塾までは結構遠いが、そこまでして家に戻れない理由が気になる。 | P2 |
| 000005AC:11:117 | P1 | no subject, no tense | 「ずっと……一緒だから……」 | P1 |
| 000005AC:11:82 | P1 | euphemism for a psychiatric hospital | 女ケ沢はここよりお父さんの実家も近いし、お母さんの心を治すいい病院があってさ。 | P1 |

Both-listed items (41, agree): 00000024 あの人 / あの2人 / visitor identity; 000001DB dream figure, し／に／が; 000001DD ×× age; 000001DF victim sex, 人 at 11:126; 000001E1 red person ungendered; 000001E3 bare reveal cells 12:0 / 20:0; 000001E5 23:26 gender hedge, 29:13 お面; 000001E7 caller withheld, Hokkaido-call contradiction; 0000020D 11:45-51, 11:74, 11:90; 000002F6 あの人 = なつみ; 000002F8 12:69; 0000034C 11:232 あいつら; 00000366 11:112; 0000037D 11:63; 000003AE patient name; 00000488 voice flood, 48:2; 000004A7 11:109; 000004CF 12:81-82; 000004F9 figure description; 0000050E 11:17, 11:79, 11:184; 00000522 11:111, 11:123, 11:171-175; 00000564 例の件, 11:105, 11:189, the figure until unmasked; 0000057B 11:55, 11:69; 000005AC reason deferred to 明日.

SUMMARY: 220 compared (39 narrator + 39 time + 142 withheld), 118 agree, 102 disagree: P1 25, P2 71, both 6, undecided 0. The 000004BB narrator row is counted here as well as in CAST. (checkpoint 4 done)

### 5. QUERIES

Compared: P1 Q001-Q072 (72 queries raised on in-scope files) and P2 V001-V076 (76). 39 pairs ask the same question: Q001/V028, Q002/V004, Q004/V005, Q005/V006, Q006/V002, Q007/V001, Q008/V029, Q009/V008, Q011/V009, Q012/V012, Q013/V013, Q015/V017, Q016/V030, Q017/V031, Q018/V024, Q019/V015, Q021/V025, Q023/V040, Q024/V003, Q031/V026, Q032/V010, Q038/V033, Q039/V034, Q040/V035, Q043/V051, Q045/V050, Q046/V041, Q047/V046, Q048/V047, Q049/V056, Q051/V043, Q052/V014, Q055/V048, Q056/V036, Q061/V060, Q062/V063, Q066/V067, Q069/V068, Q070/V057. Within these pairs the proposed answers do not contradict each other (P1 has since resolved Q012 and Q014 from source ruby; P2 leaves V012 open; that is a status difference, not a disagreement).
Items: 39 matched + 33 P1-only + 37 P2-only = 109.
verdict for a one-pass query: the listing pass if the question is real in the JP and the other pass has nothing on it; both if the other pass records the same point in CAST / SUMMARY / GLOSSARY without a query; undecided if the other pass asserts an answer the JP cannot confirm.

Queries that COLLIDE with an assertion in the other pass (JP quoted):

| query | question | other pass asserts | deciding JP | verdict |
|---|---|---|---|---|
| V042 | 新村美冬: identity is inference only | P1 CAST: name confirmed at 0000037D:11:58 | 0000037D:11:57-58 two names on dolls, no link; link at 00000550:11:72 | P2 |
| V066 | speaker order of the three thanks | P1 RELATIONS: 春花 says おじさん once | 00000550:11:130 (see R4) | P2 |
| V072 | speaker of 00000538:11:16 / 11:25 | P1 RELATIONS: 伊勢 (P1 CAST: a staff member) | 00000538:11:16, 11:25 untagged (see R7) | P2 |
| V032 | speaker of 000002F6:11:78 「五島様……すみませんでした。もう勘弁して下さい……」 | P1 CAST: 春花 uses no 敬語 to anyone | 000002F6:11:77 春花 offers to pay 「ザッハで何かおごってやろう！」; 11:78 follows untagged | P2 |
| V039 | 000003B4:8:28 「――お疲れ様でございますでございます！」: gag or copy error | P1 CAST: an intended "panic formula" | the JP cell alone cannot say which | undecided |

P1-only queries (33):

| query | topic | verdict |
|---|---|---|
| Q003 | 春花's father dead or posted abroad | both (P2 CAST records the resolution from 00000550:11:44 / 000005AC:11:78) |
| Q010 | stray spaces = ruby residue (000001DB:15:131 「 苛 まれる」) | P1 |
| Q014 | 祀耀 reading | P1 |
| Q020 | 作戦 running gag, fixed EN | both (P2 CAST: "fixed 'Operation ___' pattern TBD") |
| Q022 | 0000020B:12:33 「お父さん＝皮剥ぎ死体」 bare equation line | P1 |
| Q025 | near-duplicate route-variant blocks need identical EN | P1 |
| Q026 | 春花's 私 and 「怖いわ」 (000001E5:23:9 「うわあ……なつみのそれ怖いわ。」) | P1 |
| Q027 | 000001DF:11:115 headline register, 性別不明 | both (P2 WITHHELD 000001DF) |
| Q028 | reveals split so the key noun lands alone | P1 |
| Q029 | 000001E3:8:20 narrator explains the surnames | P1 |
| Q030 | narrator switches to 五島 unlabelled (0000020B) | both (P2 SUMMARY names the narrator per block) |
| Q033 | 00000024:51:9-13 untagged alternating lines | P1 |
| Q034 | 五島 says 古郡先輩 / 新村先輩 in her own narration | both (P2 CAST / RELATIONS record it) |
| Q035 | who is 伊勢さん (00000024:51:11) | both (P2 CAST first_appears 00000024:51:11) |
| Q036 | text messages in straight quotes vs 「」 | P1 |
| Q037 | the 呼び捨て / 絵梨奈ちゃん contrast in EN | P1 |
| Q041 | 0000034C three route variants | P1 |
| Q042 | 0000034C:11:166 「これ、私が吐き出したものなんだ」 double meaning | P1 |
| Q044 | one cell, two or more speakers joined by ⏎ | both (P2 SUMMARY NOTE lines + V066) |
| Q050 | the voice flood's spacing and non-attribution | both (P2 CAST "unnamed voices" EN correlates) |
| Q053 | 000002F6 あの人 = なつみ | both (P2 WITHHELD 000002F6) |
| Q054 | orders 24-27 / 38-39 are earlier branches of 四月八日 | both (P2 SUMMARY "different route") |
| Q057 | 作戦 gag dies twice | both (P2 CAST 五島 chunk-02/03 tics) |
| Q058 | the ニカッと grin's origin | P1 |
| Q059 | 000004A7:11:64 / 11:68 伊勢 blurts then self-corrects | P1 |
| Q060 | mid-block narrator switches | both (P2 SUMMARY 000004BB, 000004CF) |
| Q063 | 00000522:11:111 unfinished hypothesis | both (P2 WITHHELD 00000522) |
| Q064 | 「――」 as radio dropouts (000004F9:11:136 「聞こえ――ますが」) | both (P2 CAST radio operator) |
| Q065 | 超炭酸ボンバー fixed EN | both (P2 GLOSSARY TBD row) |
| Q067 | 000004E3:27:131 JP glosses メイス | P1 |
| Q068 | 00000538:11:85-87 hypothetical 『』 block | P1 |
| Q071 | 00000564:11:97-120 letter set with no quote marks | P1 |
| Q072 | 000005AC:11:41-45 超 one per cell | both (P2 SUMMARY NOTE 000005AC) |

P2-only queries (37):

| query | topic | verdict |
|---|---|---|
| V007 | EN for おばさん (non-relative) | P2 |
| V011 | 佐波県 reading | both (P1 GLOSSARY: reading さわ from source ruby) |
| V016 | 桜: cherry blossoms / trees / sakura | P2 |
| V018 | 000001DF:11:187 typo 生活していいて | P2 |
| V019 | 000001DD:11:131 typo もしよかった今日 | P2 |
| V020 | 000001E3:8:47 らしきの | P2 |
| V021 | 000001DB:15:75 half-width leading space | P2 |
| V022 | 000001E3:8:154-155 unattributed 「…………？　あれ……？」 | P2 |
| V023 | 0000020B:12:68 「10年前の事件」 vs 12 years | P2 |
| V027 | 000001DF:11:29 katakana echo of 問い合わせ先を分散 | P2 |
| V032 | see collision table | P2 |
| V037 | 新村栄一郎 reading | both (P1 GLOSSARY reading) |
| V038 | 000003B4:23:0 typo だいだい | P2 |
| V039 | see collision table | undecided |
| V042 | see collision table | P2 |
| V044 | 00000488:48:8 echo of 00000024:16:48 needs identical EN | P2 |
| V045 | replayed 春花 lines, identical EN across re-split cells | both (P1 SUMMARY 0000037D / 00000488 / 000004CF: "must match word for word") |
| V049 | date of 000003BC | both (P1 time marker: "late", no date) |
| V052 | 0000033D:11:17 「面会にはまだ早いぞ？」 jail sense | P2 |
| V053 | 000002FA:11:75 ツーツー | P2 |
| V054 | 0000037D:11:51 ビニールバック | P2 |
| V055 | お姉ちゃん in 五島's narration | P2 |
| V058 | 000004CF:12:0 五島様様 idiom | P2 |
| V059 | EN for おじさん to 伊勢 | P2 |
| V061 | 000004E3:27:12-20 corrupted laughter | both (P1 SUMMARY 000004E3 + CAST 春花 register 3) |
| V062 | 0000050E:11:97 「……み！」 | P2 |
| V064 | 00000522:11:171-175 epilogue speaker | both (P1 SUMMARY 00000522) |
| V065 | 0000057B:11:55 who put the letter away | P2 |
| V066 | see collision table | P2 |
| V069 | mailbox 暗証番号式 (00000595:11:123) vs ダイヤル式 (000005AC:11:2) | P2 |
| V070 | 中二病 | both (P1 GLOSSARY chunibyo) |
| V071 | 00000564:11:19-20 天才美少女 variant of the refrain | P2 |
| V072 | see collision table | P2 |
| V073 | かりそめの友情 fixed EN, source unknown | both (P1 GLOSSARY row) |
| V074 | 000004BB:8:30 JK | both (P1 GLOSSARY row) |
| V075 | 00000538:11:54 無機質／有機質 pair | P2 |
| V076 | 000004CF:12:36 茜's polite text, self-reference お母さん | P2 |

QUERIES: 109 compared, 39 agree, 70 disagree: P1 17, P2 27, both 25, undecided 1. (checkpoint 5 done)

## (c) Verdict: can pass-1 notes be trusted for parts 1-3 translation work?

1. Mostly yes for what happens and what is withheld: narrators (38/39), time markers (39/39) and the shared WITHHELD items agree, and pass 1's one-pass SUMMARY and QUERY items all check out against the JP.
2. CAST and RELATIONS speech levels FAIL where pass 1 wrote absolutes: 春花 "no 敬語 to anyone", 五島 "unbroken 敬語", なつみ "no 敬語 to 美冬", the patient "丁寧 even while shouting" are each contradicted by in-scope lines (C2-C4, C7, R1-R5); pass 1 was right against pass 2 in 0 CAST items.
3. Naming firsts FAIL: 良治 is named at 0000034C:11:136 (not 000004E3), 美冬's identity is not confirmed at 0000037D:11:58, 桃子 uses 絵梨奈 at 0000037D:11:5; attributions of untagged lines (00000538:11:25, 00000550:11:130) are stated as fact where the JP leaves them open.
4. GLOSSARY does not fail on meaning (3 wrong renderings in 228: 補導, ツーツー, 宗派) but 32 keys are open policy choices (romanize vs translate, proper-noun form, interjections) that pass 1 presents as settled.
5. Use pass 1 for plot, WITHHELD and format queries; re-check every pass-1 speech-level, address-form, first-named and speaker-attribution claim against the JP (or take pass 2's) before drafting parts 1-3.
