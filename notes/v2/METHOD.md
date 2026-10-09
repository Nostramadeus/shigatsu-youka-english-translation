# METHOD.md (v2) — how this visual novel is translated (Opus 5.5 remake, 2026-09-26)

Method only; no story content. Replaces notes/METHOD.md for all v2 work. Each rule carries its source:
[O-nn] = owner ruling (notes/v2/OWNER-RULINGS.md, binding, substance never changes); [F] = orchestrator ruling
(reversible); [M] = model-made rule kept after the 2026-09-26 re-check. JP examples are from read/chunk01.txt.
Fixed conventions (punctuation, numerals, names, glyphs) live in notes/v2/STYLE.md; typographic devices in
notes/v2/CORE-RULES.md.

---

## 0. Doctrine [O-01]

TRANSLATION, ZERO LOCALIZATION. Register model: Richmond Lattimore's Iliad. Faithful, line for line, the source's
images and order kept, no smoothing, no quirking-up, no cut or softened lines, no replaced references. A slightly
foreign surface is fine. Never a Treehouse / 8-4 style rewrite for a Western audience.
Supporting position [M]: Nabokov (1955), the clumsiest literal translation beats the prettiest paraphrase;
Schleiermacher (1813), move the reader toward the author.

- JP: 時刻は深夜0時を回っていた。
- EN: "The time had gone past midnight." (owner-confirmed; it STAYS, see §2)

## 1. Two failure modes, both banned [O-02]

1. ADDITION: jokes, quips, interjections, personality, emphasis, swearing, AI-isms the JP does not have.
2. FLATTENING: the information kept but the register, density, rhythm or joke mechanism lost; padding, hedging,
   explaining, softened insults, one punch split into three soft clauses.

Reference case (keep it; it is the owner's):
- JP: 俺は三十四歳住所不定無職。人生を後悔している真っ最中の小太りブサメンのナイスガイだ。
- Official EN (flattened): "I was a thirty-four-year-old man with no job and nowhere to live. I was a nice guy,
  but I was on the heavy side, didn't have good looks going for me, and was in the midst of regretting my
  entire life." The blotter voice became a sentence, "nice guy" moved to the front, the added "but" explains
  the irony and kills it, the insults became euphemisms.
- Faithful in effect: "Me: thirty-four, no fixed address, unemployed. A chubby, ugly nice guy in the middle of
  regretting his whole life."

Rules that follow:
- **Register sequence is the joke [O-03].** 小太り (soft) -> ブサメン (crude net slang) -> ナイスガイ (ironic
  katakana English): the English keeps the sequence, not only the three meanings.
- **Density is a diagnostic, not a rule [O-03].** Twenty English words for five characters can be right. What must
  match is the weight distribution and where the punch lands.
- **Sentence-level test [O-02].** Read the JP line; note (a) its register sequence, (b) which words carry weight,
  (c) where the punch lands. The English matches all three.
- **Jokes by mechanism, not by meaning [O-02].** Rebuild the mechanism (stacking, inversion, register clash,
  anticlimax) from the JP's own material. Never add a "but", never wink. A pun with no English route keeps its
  surface meaning, gets a QUERY row, and may get a TN (STYLE §TN).
- **Insults keep their weight [O-02].** ブサメン is "ugly", not "not conventionally attractive". Crude stays crude
  (American words: "jerking off", not a British one) [M].
- **Padding test, per word [M].** Which JP word does this English word come from? No source and no grammatical
  job = padding. Use it as a prompt to re-check, never as a reason to cut a word that carries weight.
- JP: 春花は頭をかきながら、反省の弁を吐く。 The joke is the newsroom formula 反省の弁 on a teenager.
  EN: "Haruka scratched her head as she delivered a statement of remorse." ("spat out words of self-reproach"
  adds anger the JP does not have: an ADDITION.)

## 2. Japanese order and feel over natural English [O-04]

- The project values the JP order and feel over 100% natural English. "No subject calques" was REJECTED as a rule.
- Only a clearly unreadable line is an error. A reviewer who finds a line hard to read logs it as a
  STIFF-CANDIDATE row for the OWNER to judge; nothing is enforced per line; agents add no new stiffness rules.
- **Cells and clause order [M, changed].** A cell is an engine unit: never split or merge cells. Inside a cell the
  English may split one JP sentence that stacks て / し / が clauses into two sentences, but it keeps the JP CLAUSE
  ORDER wherever English can hold it; reorder only where English grammar forces it.
  - JP: 眠りが浅かったのだろうか、春花はすぐに、そしてゆっくりと顔を上げた。
  - EN: "Maybe her sleep had been shallow. Haruka lifted her head right away, and slowly."
- **Same shape for lines whose shape is the point [M]:** jokes, lists, blotter lines, one-word cells, refrains.
  A four-noun line stays four nouns; a one-sentence punch stays one sentence.
  - JP: たまに子供の声、／たまに自動車の音、／たまに風の音。 (three cells, one frame each)
  - EN: "Sometimes a child's voice," / "sometimes the sound of a car," / "sometimes the sound of the wind."
- **Image order carries information [O-33]:** see STYLE §Order.

## 3. Do not decide what the author left undecided [O-10]

The owner's rule, replacing "exactly as ambiguous as the Japanese". Test every new rule against "would this make
stiff English?"; the owner overruled a reviewer's "the room" himself.

**GRAMMAR vs WITHHELD (the one test) [M, from O-10].**
- A gap is GRAMMAR when two first-time Japanese readers would fill it the same way without noticing a gap. Fill it
  as they do. No flag, no DECISIONS row.
  - JP: 「春花、起きて。寝るなら、部屋に行こう」 EN: "Haruka, wake up. If you're going to sleep, let's go to your room."
- A gap is WITHHELD when those readers could fill it differently, or when the text later turns on which filling is
  right. Keep it open if the packet lists it or English can do it without a contortion; else take the
  packet-supported reading and flag `needs-tlc`.
  - JP: でも、あの人は死んだ。 EN: "But, that person died." (not "he", not a name)
- `subject-guessed` / `gender-guessed` / `number-guessed` flags are for WITHHELD gaps only.
- The packet's "ambiguity that the translation MUST keep open" lines were written under the older definition and
  mix real withholding with grammar habits and structural notes: read every such line through this test.

**Knowledge fence [M].**
1. Translate file N as its first-time JP reader reads it. What that reader takes as settled is written as settled.
2. Later knowledge may only choose, between two EQUALLY natural English forms, the one that does not contradict the
   later fact, or keep two terms distinct. It never adds a hedge, a vaguer noun, a passive, a dropped pronoun or a
   "they". Test: would a first-time JP reader at this file notice anything vague here? If not, the English is not
   vague either.
   - JP: 「だったら家宅捜索のときに伊勢さんが持っていってるはずだよね？」 A surname + さん is a specific adult to
     that reader; the English may use the pronoun that reader assumes.
3. Every fact in CAST, RELATIONS, GLOSSARY and SUMMARY carries an as-of file id (reading order =
   notes/_db/_file-order.tsv). A CAST or RELATIONS bullet WITHOUT an id passes the packet fence unseen (the fence
   drops only lines whose earliest id is later than yours; found 2026-09-26). Every bullet a read-through agent
   writes carries its as-of id; a drafter who meets an id-free bullet treats it as unfenced and follows the JP.

## 4. Japanese nuance [O-05, O-06]

- Honorifics, pronoun nuance and speech level are KEPT or carried by a short translator note, never re-encoded by
  warping English (no fake dialect, no odd grammar, no tense trick). Honorifics stay as suffixes on names [O-05].
- A pronoun, name-form or speech-level switch the scene uses gets a TN at the line, and the line is translated
  plainly [O-05, O-06].
- Speech level is carried by English diction (contraction rate, polite words), per CAST / RELATIONS; defaults in
  STYLE §Speech level [M].
- TN rules: STYLE §TN [O-06].

## 5. Consistency [M]

- **One rendering per term.** GLOSSARY is binding; drift (same JP, different EN) and collision (different JP, same
  EN) are both errors. A locked term changes only by marking the row `superseded` and sweeping every finished file.
- **Interjections are locked per FUNCTION, not per string** (one spelling does several jobs). The row names the job
  and its tell; if the word here does another job, write the English of that job and add a row.
  - JP: 「よう！　調子はどうだ？」 and 「おい、なつみ」 both take "Hey" (rough greeting / attention-getter); the
    roughness rides on what follows.
- **Translation memory.** Identical JP gets identical EN for verbatim replays, refrains, and lines of about eight
  characters or more with the same speaker, addressee and function. Shorter strings match by function.
- **Near-duplicate variants.** A scene printed in several variants: diff the variants first; a shared line gets the
  same English in every variant; a JP difference is carried; never "improve" one variant.
  - JP: 「ダメだな……。新生活の初日から、こんなだらけてたら……」 and 「くそ、ダメだな……。新生活の初日から、
    こんなだらけてたら……」 differ by one word; the English differs by that word only.

## 6. Note files (v2 paths, all under <repo>/notes/v2/)

| file | holds | rule |
|---|---|---|
| GLOSSARY.tsv | jp, reading, en, pos, category, first_seen, status, locked, note | one row per term (per function for interjections) |
| CAST.md | one block per speaker: pronoun, speech level, particles, tics, EN correlates | every bullet ends with its as-of file id |
| RELATIONS.tsv | ordered pair (A to B): calls_them, speech_level, as_of_file, changed_from, why | a change in either column is a story beat |
| SUMMARY.md | one block per file in reading order | never revise an earlier block; a drafter reads blocks <= N only |
| QUERIES.md | id, file:line, question, why it matters, best guess, confidence, status | a shipped guess is logged with confidence |
| _tmp/tl-log-<tag>.md | one log per agent: DECISION, TN, QUERY, RESOLVED, PROGRESS rows | the orchestrator merges (tools/kb/kb.py merge-log <tag>) |

## 7. Process

1. Read-through first, notes built before drafting [M].
2. Draft: one agent, 2-3 files, blocks of at most 60 text lines (TRANSLATOR-BRIEF) [M]. The drafter reads the whole
   script and packet before block 1 and re-reads its last five English lines at each block start [O-22].
3. Review: EVERY line, always; no sampling, ever; cost is not a reason to skip lines [O-20]. Contiguous windows,
   multi-line units whole, every short or elliptical cell checked for referent binding [O-21] (REVIEWER-BRIEF).
4. Owner proofreading: the owner proofreads about 100 lines per chunk himself; the review page shows only the
   PLAYED path, no looping variants [O-23].
5. Mechanical QA: `SY_EN_DIR=lns-en-55 uv run tools/qa_check.py <id>` for the 5.5 tree [M].
6. In-context: nothing goes to friends until a full on-screen mouse run shows zero Japanese and zero layout
   defects [O-41].
7. Shipping: patch-only distribution, never the game files; ask the author first; files 000000F2 / 0000001C never
   ship [O-40].
8. Agents: every agent runs on Opus 5.5 (subagent_type opus55); the "opus" alias (Opus 5) is banned; fable is not a
   substitute [O-42]. Part 1 is retranslated from scratch on 5.5 and every line reviewed; parts 2-3 and 000016AE
   wait for the owner; work starts without waiting for a bake-off verdict [O-43].
9. Real personal names never appear anywhere in the project folder; the credit line names only the author [O-26].
10. Reports to the owner: file ids, line counts, tokens, minutes, done/next ONLY. No plot, structure, mechanics,
    screen descriptions, note counts, spatial/ordinal words about where things sit [O-25].

## 8. Failure modes to check for [M]

Wrong speaker; invented referents (a referent no first-time JP reader can identify); manufactured ambiguity (a
hedge, "they", a passive where the JP decided); gender errors; honorific drift; name-spelling drift; term drift and
collision; register drift inside a speaker pair; broken tags; ambiguity foreclosed early; tone flattening (every
voice converging on one mid register); over-localization; smoothing; queries shipping silently; superseded glossary
rows never swept back. Overflow is not fixed by cutting: the engine pages long boxes [O-11]; layout defects are
caught in the on-screen run [O-41].

## 9. Rules for agents [M]

- Never read ahead: SUMMARY blocks <= N, CORE fenced at your last id (`PYTHONUTF8=1 uv run --no-project --python 3.12 python
  tools/kb/kb.py core <id>`).
- Never invent a heuristic. If STYLE or the brief is silent, write a QUERY row and move on.
- Never guess silently: guess, flag, log.
- Save to disk as you go; one log file per agent.
- A reviewer never re-translates a judgment call between two faithful renderings.
