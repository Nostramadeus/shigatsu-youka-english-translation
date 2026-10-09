# CORE-RULES.md (v2) — the rule sections of CORE.md, rewritten (Opus 5.5 remake, 2026-09-26)

Rules only: how to write a device, never what the story contains. CORE.md (the story digest: per-site device
lists, cast voices, owner queries, collisions, fence index) is being rebuilt from the new read-through; until then
a drafter reads it only FENCED (`PYTHONUTF8=1 uv run --no-project --python 3.12 python tools/kb/kb.py core <last id>`, then
notes/_tmp/core-<id>.md) and treats its site rows as reference. Where a CORE.md rule sentence and this file differ,
this file wins; STYLE.md outranks both on conventions. This file has no file ids past part 1 and no story facts, so
it is read WHOLE. Source tags as in STYLE.md; Q-ids are the QUERIES rows the rule came from. JP examples from
read/chunk01.txt.

## 1. Rank and fence
- STYLE.md > CORE-RULES.md > CORE.md best guesses > GLOBAL.md (the long version; grep it only for an anchor CORE
  names; never page through it) [M].
- Where CORE or GLOBAL says a thing is open, it is open: stop and file a QUERY, do not invent [M].
- An OWNER-BLOCKING query on a line = that file is not drafted until the orchestrator answers; an owner non-blocking
  query = translate around it and file the query [F].
- A name whose reading is disputed between GLOSSARY and CAST blocks the file until the orchestrator picks [F].
- Resolved rows that change an earlier file's rendering: the translator of the earlier file must not write the
  answer in; the fence (METHOD §3) applies [M].

## 2. Quotation channels [F]
| JP | EN | rule |
|---|---|---|
| 「」 | straight "..." | ordinary audible speech |
| 『』 | '...' | quoted titles, words, inner quotes; register does the rest of the work |
| straight "..." in the source | curly “...” | text nobody present is speaking (phone, broadcast, document, a mute character's writing) |
| bare cell (letter, memo, notice) | bare, no wrapper | keep line breaks; the register shift is the only signal |
| 「――」 line-initial prefix | ― at the same position | one mark for every job (a speaker channel, a voice over a device, an unhearable voice, a transmitted thought, a non-focal speaker); attribute nothing, add no "I imagined" or "it said" |
| a cell that is only 「――」 | a lone ― | keep the cell count; add nothing |
| empty 「」 | "" | never insert an ellipsis; different from an ellipsis-only cell |
| two quoted turns joined by ⏎ in one cell | both sets of quotes inside the one cell | e.g. 「あ……」⏎「あ……」 = "Ah..."⏎"Ah..." |
| nested quotation | inner 『』 = '...' | seams unmarked |

## 3. Cells and splits [F]
- Never split or merge a cell. A one-cell reveal keeps its split, and the English orders its clause so the withheld
  element still lands last in the second cell (Q179).
- **A word spread one mora per cell and completed in the file:** the same number of cells, one or two letters per
  cell; the English word is chosen for the cell count as much as for register; log a DECISION (Q1084).
  - JP: 「お／と／う／さ／ん？」 (five cells) EN: five cells, one or two letters each, the word chosen for the count
    and the register, logged as a DECISION.
- **A word spread one mora per cell and NOT completed in the file:** romanize mora by mora, one TN on the first cell,
  and the English must not resolve into a word; the file that completes the word decides its English (Q1123).
  - JP: し……／に……／が…… EN: "Shi..." / "ni..." / "ga..." [TN on the first cell]
- **A label read aloud one character per cell** keeps the cells and the GLOSSARY spelling.
  - JP: 『ド／ロ／ー／ガ』？ EN: 'D / r / o / ga'? (GLOSSARY locked, Q1083)
- Row-blocks printed out of story order: translate in PRINTED order (Q641).
- Two sentences in one cell stay in one cell; two voices in one cell stay in one cell (Q831, Q733).

## 4. Spaces and glyphs [M, O-34]
- A layout full-width space (an indent, a gap inside a word, a blank turn, column alignment) is copied byte for
  byte; the device row wins over qa_check, and a HARD line on it is waived with a DECISION row naming this rule.
- A cell that holds only spaces keeps them; no quotes, no punctuation, no attribution are added.
- Kaomoji and text emotes stay exactly as printed (check each glyph against CP932); no Western emoticon.
- ×, ○, △ masks and deliberate blanks keep the symbols, their counts and the cell splits; a masked person stays
  unnamed and ungendered (「××」 = "XX").
- Latin script inside the JP is kept exactly; keep the on-screen gloss; ONE TN at first use saying the word is
  English / Portuguese in the source (Q231).
- UI instructions set as narration keep the full-width parentheses and the UI register: 「（次のページは…）」.
- Kanji numerals follow the STYLE numeral rule in running text; archaic numerals used as LABELS stay.
- Equation lines keep the equals sign and the cell split; they are not turned into sentences.
- Bullet lists with ・ keep bullets, the title cell and one item per cell.

## 5. Repetition and length devices [F]
- Repeated-character walls keep the same syllable count where the box can hold it (the engine pages, O-11); never
  reduce to one; keep distinct lengths distinct (Q622, Q240).
- A stretched っ or vowel, repeated as a gag with different counts, stretches an English vowel with a matching count.
- Ellipsis-only cells: one "..." per JP … (STYLE).

## 6. Things not to fix [M]
- Contradictions the text states on screen (dates that disagree, two names for one thing) are reproduced.
- Sentences that break off stay broken off: no supplied verb, no supplied object.
  - JP: 桜が咲く季節になると、私は――。 EN: "When the season of cherry blossoms comes, I―"
- Deliberate broken Japanese (a broken notice, baby speech, slurring, 片言) is a device, carried in English by
  clipped or dropped letters, never by phonetic dialect spelling. Test: if a character or the narrator NOTICES the
  oddity, it is a device; if nobody does, it is a typo (STYLE §Source errors).
- Precognition, hallucination and dreams are translated STRAIGHT: no hedge, no italics, no early signal, no added
  scene break (Q285, Q453).
  - JP: 桜の木の横で、誰かがもがいている……。 The dream cells get no marker before, inside or after them; the
    English of the dream reads like the English of the waking narration.
- A narrator switch at a file, block or cell boundary is marked NOTHING in the English: no name before the JP gives
  one, no gender before the JP gives one. The JP's only signals are pronoun, speech level, a tic, an address form in
  narration, tense and content; the English reproduces those and nothing else (Q030, Q640).
- An inset first-person story with no frame stays unframed; the register shift is the only seam (Q146).
- A second-frame block (a double, a mask, an impersonation, a hallucination) is written INDISTINGUISHABLE from what it
  pretends to be: no hedging, nothing cooled, nothing made eerie.

## 7. Replays and refrains [M]
- A verbatim replay (the same cells printed again later) is frozen to the earliest English and pasted.
- A refrain keeps ONE fixed English wording, recorded in GLOSSARY before any file with it is drafted. Identity is of
  WORDS: the refrain inflects for its slot ("become a family" -> "became a family"); punctuation follows English
  grammar in every printing; byte identity only where the JP is byte-identical in the same slot.
  - JP: もし、あの2人にもっと勇気があったら。／もし、あの人に耐える勇気があったなら。 The repeated frame もし…勇気が
    あったら keeps one English frame: "If those two had had more courage." / "If that person had had the courage
    to endure."
- A grammar distinction the plot turns on (a negation pair, a chosen verb the narration remarks on, a question mark
  read as a confession) is kept by word choice and word order, reasoning left intact.

## 8. Wordplay [O-02, M]
Never invent a replacement pun. Keep the surface meaning, file a QUERY, and add a TN only if the owner's TN test
(STYLE §TN) passes. Two spellings of one sound that the text makes a point of stay one sound in English (or get a TN).

## 9. Voice floors [M]
- Formality is carried by DICTION, not by adding or dropping a suffix (STYLE).
- Profanity carries the JP word's own weight and is never escalated: くそ = "damn" / "crap".
  - JP: 「くそ……もうちょっとでいいシーンだったのになあ」 EN: "Damn... it was just about to get to a good part."
- One JP cell with an explicit 私 = one English sentence with "I" as its subject; never fold two such cells into one
  sentence with a participle or "and"; never add "myself" or "as for me".
  - JP: 私にできることなんて、何もなかった。 EN: "There was nothing I could have done."
- Same English name for two different people in the JP: keep them as two people; one person under two JP forms:
  one English referent (check GLOSSARY).

## 10. Collisions [M]
Two different JP terms may not share one English rendering unless GLOSSARY marks them same-referent; interjection
rows sharing one English by FUNCTION (おい / よう / ねえ = "Hey") are not a collision.
