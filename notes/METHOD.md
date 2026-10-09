# METHOD.md — how we translate this VN

Method only. No story content in this file. Derived from professional JP→EN
localization practice (Honeywood/Square Enix GDC 2007, MangaGamer, ATA game-loc
practice, memoQ QA model, MQM error typology) and from literalist translation
doctrine (Lattimore, Nabokov, Schleiermacher, Pannwitz-via-Benjamin).
Evidence and links: `research/translator-workflow.html`, `research/_raw-notes.md`.

---

## 0. Doctrine — read before touching a line

**This is a TRANSLATION, not a localization.**

Two separate anchors (the owner, 2026-10-01; replaces the single "Lattimore register" line).

**CONTENT anchor = Richmond Lattimore's Iliad.** Faithful, line-for-line, keeps the source's
images and order wherever English permits, no cuts, no added jokes, no replaced cultural
references, does not editorialize. Lattimore's own rule was to avoid mistranslation caused by
"rating the word of my own choice ahead of the word which translates the Greek." Substitute
Japanese for Greek. This anchor governs WHAT goes into a line.

**VOICE anchor = contemporary spoken English.** This is a visual novel, not a scholarly
translation. Dialogue sounds like the speaker would sound if they spoke English: contractions,
slang level, dialect colour, baby talk, flunky-speak, keigo stiffness, all rendered. Narration
matches the narrator's register, not a default formal one. Test per line: would a native
speaker of that age and type say this out loud? If no, the line is wrong even if every word is
accurate. Flat formal English for coloured JP is a defect, not a safe default.

**Cap: never MORE colour than the JP has.** The amount of slang, attitude, idiom and personality
in the EN line matches the JP line, not the translator's idea of the character. A plain JP line
(「お前には隠せないな」) is a plain EN line ("Can't hide anything from you, huh."), not "You'd
sniff out the lie before it scarce passed my lips." Adding colour the JP lacks is Addition
(0b.1); removing colour the JP has is Flattening (0b.2). Both are defects of the same size.

Verbal tics the text treats as a BIT (a put-on voice, a catchphrase another character notices)
may stay romanized with a one-time TN. Everything else that is register is rendered in English
of matching colour.

Supporting positions we adopt:

- **Nabokov (1955):** the clumsiest literal translation beats the prettiest
  paraphrase; "smooth" and "readable" are not compliments for a translation.
- **Schleiermacher (1813):** move the reader toward the author, never the author
  toward the reader.
- **Pannwitz, quoted by Benjamin (1923):** the translator's basic error is
  preserving his own language as it happens to be, instead of letting the
  foreign language act powerfully on it.


### 0b. Fidelity of EFFECT, not only of content (the owner, 2026-09-24)

Literal-not-localized has TWO failure modes, and the doctrine above only banned one.

1. **Addition** (banned above): jokes, quips, references, personality the JP does not have.
2. **Flattening** (banned here): keeping the information but losing the register, the density, the
   rhythm and the mechanism of a joke. Padding, hedging, explaining, splitting one punch into three
   soft clauses. This is what most "faithful" official translations actually do, and it is just as
   unfaithful as addition.

Reference case (Mushoku Tensei, prologue line 1-2):
- JP: 俺は三十四歳住所不定無職。人生を後悔している真っ最中の小太りブサメンのナイスガイだ。
- Official EN: "I was a thirty-four-year-old man with no job and nowhere to live. I was a nice guy, but I
  was on the heavy side, didn't have good looks going for me, and was in the midst of regretting my
  entire life."
- What the JP does: line 1 is written in police-blotter / news-caption register (age, no fixed address,
  unemployed: four nouns, no verb). Line 2 stacks two insults (小太り chubby, ブサメン ugly-guy slang) and
  then deadpans ナイスガイ in katakana English. Three jokes in one sentence: the blotter voice, the
  self-insult stack, the ironic "nice guy" landing last.
- What the official EN does: converts the blotter into a normal sentence, moves "nice guy" to the front,
  inserts "but" (which EXPLAINS the irony and kills it), and softens the insults into euphemisms
  ("on the heavy side", "didn't have good looks going for me"). Nothing was added, and the line is dead.
- Faithful-in-effect EN (same material, same order, same register): "Me: thirty-four, no fixed address,
  unemployed. A chubby, ugly nice guy in the middle of regretting his whole life."

Rules that follow:
- **Same material, same order, same length class** (rev. 2026-09-25, rules audit #9 — scoped, because applied
  to every line it produced semicolon chains and kept Japanese topic-comment frames). "Same length class"
  governs the lines whose SHAPE is the point: jokes, lists, blotter lines, one-word cells, refrains. A
  four-noun line stays a four-noun line; a one-sentence punch stays one sentence. Everywhere else: no cell is
  split or merged (cells are engine units), but the SENTENCE COUNT and the CLAUSE ORDER inside a cell follow
  English grammar — a JP sentence stacking て / し / が clauses may become two English sentences.
  PADDING TEST, per word: which Japanese word does this English word come from? A word with no source and no
  grammatical job is padding. Do not pad, do not hedge.
- **Register is data.** Blotter, keigo, baby talk, slang, textbook formality: render the register, not a
  neutral paraphrase of it. Deadpan stays deadpan; a euphemism is only used where the JP used one.
- **Jokes are translated by mechanism, not by meaning.** Identify what makes the line funny (stacking,
  inversion, register clash, anticlimax, pun) and reproduce THAT mechanism with the JP's own material.
  Never explain the joke, never add a "but", never insert a wink. If the mechanism is a pun with no
  English route, keep the surface meaning and log an owner query; do not invent a replacement pun.
- **Insults, crudeness, self-mockery keep their weight.** ブサメン is "ugly", not "not conventionally
  attractive". オ○ニー is jerking off, not "pleasuring myself". (Example word swapped for an American one,
  rev. 2026-09-25, rules audit #18: the spelling and vocabulary decision for this project is American.)
- **Images and set phrases** (rev. 2026-09-25, rules audit #8). Keep an image only where the text USES it:
  extends it, puns on it, a character or the narrator notices it, or it is a listed refrain or motif (CORE B3).
  Otherwise render the idiom or set phrase by the English phrase of the same register and weight — the CORE
  B§4 device test decides: if nobody in the text notices the image, it is idiom, not imagery. Verbs inside set
  phrases (弁を吐く, 顔を上げる, 口にする, 目を向ける) take the set-phrase sense, not their literal one. See
  STYLE.md for the worked examples.
- **Register whiplash inside a phrase is part of the mechanism (the owner, 2026-09-24).** In 小太りブサメンのナイスガイ,
  小太り is soft, almost cute or polite (a plump, harmless word); ブサメン is crude 2ch net-slang, a compressed
  portmanteau (ブサイク + イケメン) that carries "ugly" AND "internet loser register" AND "compression as a
  texture"; ナイスガイ is katakana English, ironic. Three registers in eight characters, and the ORDER
  (soft -> crude slang -> ironic loanword) is the joke's shape. The EN must keep the sequence of registers,
  not just the three meanings: e.g. a mild word, then a blunt slangy one, then the ironic landing.
  Compressed slang PREFERS a compressed EN (one short blunt word) when one exists; do not force it. If no
  short English word carries the meaning and the register, a longer phrase that does is correct (see the
  density rule below). Never a polite paraphrase, whatever the length.
- **Density is a DIAGNOSTIC, not a rule (the owner, 2026-09-24).** Five JP characters may need twenty English
  words, and that can be the right translation. What must match is the WEIGHT distribution: which words
  carry the punch, where the punch lands, and that no English word is filler, hedge or explanation. Use the
  per-word padding test above as the prompt to re-check for padding, never as a reason to cut something that
  carries weight.
- **Sentence-level test:** read the JP line, note (a) its register sequence, (b) its weight distribution (words that carry
  weight vs filler), (c) where the punch lands. The EN must match all three. (The old "30% longer than a
  literal gloss" line is DELETED, rev. 2026-09-25, rules audit #9: no literal gloss exists to measure against,
  and drafters were trimming toward a character-count band instead. `qa_check`'s length ratio is a sanity
  band only: out of range means check for padding or a dropped clause.)
- Keywords the owner can use to describe this: *tonal fidelity*, *register fidelity*, *equivalence of effect
  within the source's own material*, *no additive localization, no subtractive flattening*, *joke by
  mechanism*, *density matching*. In translation-studies terms it is closer to Lattimore or Nabokov than to
  Nida's dynamic equivalence, but with the added demand that the source's HUMOR and REGISTER survive, which
  Nabokov-style word-for-word does not guarantee either.

### What we do NOT do

| Banned | Why |
|---|---|
| Making a line "punchier", wittier or more quotable than the JP | Not our text |
| Adding jokes, quips, memes, internet register, or a "personality pass" | Invention |
| Replacing a Japanese cultural reference with a Western one | Domestication |
| Cutting, merging or reordering lines to improve flow | Structure is data |
| "Making it feel native" / removing the sense that this is Japanese | The opposite of the goal |
| Smoothing a deliberately flat, repetitive or awkward JP line | Flatness may be authorial |
| Censoring, softening, or sanitising content | Not our call |
| Deciding a subject, gender, number or referent that the JP leaves open for its own reader (rev. 2026-09-25, rules audit #1) | See §3 GRAMMAR vs WITHHELD, and §6 failure modes |
| Any Treehouse / 8-4 style rewrite-for-Western-audience method | Out of scope by owner decision |

We take from pro studios **only the project-organization layer**: read-first
discipline, note files, glossary and voice-sheet fields, consistency tooling,
QA checks. None of their adaptation philosophy.

### The style rule on Japanese-specific nuance

**Honorifics, first-person pronoun nuance and speech-level nuance are PRESERVED,
or carried by a short translator note. Never rewritten into English idiom.**

- Honorifics (`-san`, `-kun`, `-chan`, `-senpai`, `-sensei`, `-sama`, bare name,
  no name) are kept as written ON A NAME. A drop or change of suffix is an EVENT — flag it.
  SCOPE (rev. 2026-09-25, rules audit #6): "kept as written" applies where the suffix sits on a personal
  name, a nickname used as a name, or a title used as a name. On a common noun the suffix is ZERO and the
  politeness goes into the noun (お客さん → "the customer", not "the customer-san"). Kinship words used to or
  about non-relatives take what a native English speaker says in that situation. Full rule and examples: STYLE.md.
- First-person pronouns: keep the nuance where English can carry it (see
  `notes/CAST.md` per-character correlates); where English cannot, do **not**
  invent slang to compensate. If the pronoun itself is doing work in the scene
  (a switch, a joke, a reveal), add a translator note rather than rewriting.
- Speech level (敬語 / 丁寧語 / タメ口 / 乱暴) is tracked per speaker-pair and
  rendered by formality of English diction, not by adding character quirks.
  DEFAULT MAPPING for a speaker with no CAST card (rev. 2026-09-25, rules audit #14): 乱暴 → high
  contractions, blunt words, imperatives; タメ口 → normal contractions; 丁寧 (です・ます) → normal
  contractions plus polite words; 敬語 proper (尊敬語 / 謙譲語) → few contractions, formal words; fixed keigo
  formulae → the GLOSSARY rendering. 丁寧 and 敬語 are two levels, not one, and a です・ます walk-on is not
  contraction-free. A CAST card always wins. Table in STYLE.md.
- Untranslatable terms stay romanized in the glossary's fixed rendering, with one
  translator note at first occurrence.
- **Translator notes are the escape valve, inside a closed list** (rev. 2026-09-25, rules audit #10). When
  literal costs comprehension, the fix is a note, not a rewrite — but only in the five cases STYLE.md lists
  (first romanized term; a speaker's first dialect line; a switch the text treats as an event; a pun kept at
  surface meaning where the point is unrecoverable; the Latin-script and on-screen-gloss cases in CORE A).
  Never a note for register colour the text does not remark on, and never an explanation inside the line.
  12 words maximum. "Never explain the joke" (above) is about the LINE; it does not forbid a listed note.
  Log every note in `notes/NOTES-TL.md`.

---

## 1. Order of work

Professional order, adapted. Do not skip to translating.

1. **Read first.** Square Enix budgets an explicit familiarization period before
   any translation. Honeywood lists "text arrives in random order; branching
   plots cause confusion" as a top failure of game localization. A VN script
   read line-by-line out of order is the worst case of this.
2. **Build the notes.** Glossary, cast, relations, style — all decided and
   written down BEFORE bulk translation (Square Enix's "glossary creation"
   stage, where every character, place, item and thing is named up front).
3. **Translate** in reading order, one file at a time, with the notes loaded.
4. **Check** (TLC pass — meaning against the Japanese).
5. **Edit** (English pass — never changes meaning, only English well-formedness).
6. **Automated QA** (mechanical checks, §5).
7. **In-context QA** — the only place tag/overflow/speaker errors actually surface.

One translator voice for the whole work. J-Novel Club's stated reason for not
splitting a long series across translators: inconsistency, and roughly tripled
editing time.

---

## 2. Files we keep under `notes/`

Every file is append-mostly and **dated by source file**, never by wall-clock.

### `notes/STYLE.md` — decided once, at the start, never per-line

Decisions that MUST be written down before bulk translation:

- Honorific policy (ours: **preserve**) and the exact romanization of each suffix
- Name order (given-family vs family-given) and per-character exceptions
- Romanization system (Hepburn variant), long vowels (`ō` vs `ou` vs `oo`),
  particle spelling (`wa`/`ha`), apostrophes (`n'`)
- 「」 rendering: quote marks vs none; nested 『』 rendering
- Ellipsis: `…` vs `...`; how many; whether JP ellipsis count is preserved
- Dash: `—` vs `--`; how 「ーー」 is rendered
- `！？` and `!?` order; whether JP doubled punctuation is preserved
- Numerals: digits vs words; JP counters
- SFX / onomatopoeia policy in narration vs in dialogue
- Italics policy (thoughts, emphasis, foreign words) — and whether the engine
  supports them at all (a real question pros ask up front)
- Interjection policy (あ, え, うん, ほら) — renderings listed in GLOSSARY and fixed PER FUNCTION, not per
  string: each row names the function and its tell (rev. 2026-09-25, rules audit #2; the test is in STYLE.md)
- Line-break and text-box length ceiling (measure it, §5)
- Translator-note format and where notes live
- Capitalization of in-world proper terms

### `notes/GLOSSARY.tsv` — the term base

Tab-separated, one row per term. Columns:

```
jp	reading	en	pos	category	first_seen	status	locked	note
```

- `jp` — exact source string
- `reading` — kana reading (disambiguates homographs; needed for name ambiguity)
- `en` — the fixed rendering. One term, one rendering.
- `pos` — noun / name / place / title / spell / item / phrase / interjection
- `category` — person | place | org | object | concept | honorific | SFX | idiom
- `first_seen` — `file:line` of first occurrence
- `status` — `provisional` | `fixed` | `superseded`
- `locked` — `y` once it appears in a released file; changing a locked term
  requires a sweep of every prior file (see §4)
- `note` — why this rendering; ambiguity; what was rejected

A long project's glossary *changes*. The Ascendance of a Bookworm wiki openly
tracks "obsolete translation" entries. Plan for supersession, do not pretend it
will not happen.

### `notes/CAST.md` — character voice sheets

One block per speaker. Every fact gets an **as-of** tag.

```
## <SPEAKER_ID>  (JP name, reading, EN rendering)
- first_appears: file:line
- pronoun(s): 俺 / 僕 / 私 / あたし / うち / わし / name-as-pronoun / none
  - pronoun switches: <when, as-of file>, and whether the switch is plot-relevant
  - pronoun FREQUENCY: does this character state the pronoun more than typical?
- speech level baseline: 敬語 / 丁寧 / タメ口 / 乱暴 / archaic / dialect(<which>)
- sentence-final particles: よ ね さ ぜ ぞ わ かしら のだ っす etc.
- copula: だ / です / じゃ / や / である
- verbal tics, catchphrases, stutters, verbal fillers (exact JP, fixed EN)
- dialect: region, which features (copula, negation, accent markers)
- EN correlates (how the above is carried in English):
  - contraction rate: none / normal / heavy
  - profanity ceiling
  - typical sentence length
  - formality register
  - vocabulary register (plain / bookish / crude / archaic)
- addresses others as: see RELATIONS.md
- known ambiguity / open questions: -> QUERIES.md
- as-of: <file>   # every line above is true AS OF THIS FILE
```

Rationale: Mandelin's point is that without character notes specifying the
pronoun up front, a translator defaults to safe-neutral and the whole cast goes
monotone. Pronoun switches are plot (FFV's Faris). The two-pronoun structure of
*Hard-Boiled Wonderland* was carried into English as a tense distinction.
**We do NOT do that (the owner, 2026-09-22).** Never re-encode a Japanese signal by
warping English grammar (tense, person, dialect, spelling). When English cannot
carry a pronoun / speech-level signal, carry it with a short translator note at
the first line where it matters, and otherwise translate the line plainly.
Record the note in NOTES-TL.md.

### `notes/RELATIONS.md` — the address matrix

The single highest-value JP→EN document. One row per **ordered pair**
(A speaking to B). This is not symmetric.

```
from	to	calls_them	speech_level	as_of_file	changed_from	why
```

- `calls_them` — exact JP form of address (名字+さん, 名前呼び捨て, あんた,
  お前, 君, あなた, kinship term, nickname, title)
- `speech_level` — 敬語 / 丁寧 / タメ口 / 乱暴
- `changed_from` — the previous value, when the relationship shifts

A change in either column is a story beat. Never let it drift silently.
Also record: **who is present** in scenes where a character's register changes
(many speakers switch level depending on who else is in the room).

### `notes/SUMMARY.md` — the running summary, strictly dated

Prevents later knowledge leaking into earlier files. Append one block per source
file, in reading order, and **never revise an earlier block**.

```
## <file id>
- events: 3-8 bullets, what happens, in order
- speakers present:
- new terms added to GLOSSARY:
- voice/relationship changes (with the RELATIONS row that changed):
- open ambiguities raised here:
- ambiguities from EARLIER files that THIS file resolves:
  - "<file:line>" -> now known to mean X. ACTION: revisit? y/n
```

Rules:
- Any fact written into CAST / RELATIONS / GLOSSARY carries `as_of: <file>`.
- When translating file N, an agent may read SUMMARY blocks for files `<= N`
  only. Later blocks are out of bounds.
- The `resolves` list is the mechanism for a late reveal recoloring earlier
  chapters. When a reveal lands, every prior line flagged against it is re-checked
  — the earlier English must leave open what the Japanese left open FOR ITS
  FIRST-TIME READER: neither foreclose the reveal, nor hedge what that reader takes
  as settled (rev. 2026-09-25, rules audit #1; the GRAMMAR vs WITHHELD test is in
  §3). Do not retro-insert the reveal into earlier lines.

### `notes/QUERIES.md` — unresolved questions

```
id | file:line | question | why it matters | best guess | confidence | status | resolved_by
```

Pros escalate to the author. We cannot. So: an unresolved query that ships
becomes permanent (Birnbaum and Luke guessed two creature names; the misspellings
are still in print). Therefore every shipped guess must be logged with confidence,
so it can be swept later.

### `notes/DECISIONS.md` — judgment log

Every time a literal rendering is departed from at all, log it:

```
file:line | JP | EN shipped | the more literal rendering | why the departure | reversible?
```

Direct from professional practice: leave the editor a note describing how you
*would* have rendered the line more literally and why you did not.

### `notes/NOTES-TL.md` — translator notes destined for the reader

```
file:line | term/line | note text | first-occurrence only? (y/n)
```

### `notes/PROGRESS.md` — status board

One row per source file: `read | translated | tlc | edited | qa | in-context`.
Percentages per stage, the way NekoNyan/MangaGamer publish them. Update as you go;
never hold a file's work in conversation only.

---

## 3. The per-line record

Whatever the working format (TSV/CSV/JSONL), every line carries at minimum:

```
id, file, index, speaker_id, addressee(s), jp, en, status, flags, note, tags_jp, tags_en
```

- `speaker_id` — **required**. Blank speaker is a blocker, not a warning.
  Wrong-speaker is the error audiences notice most.
- `addressee` — drives honorifics and speech level. Guessed addressees get flagged.
- `tags_jp` / `tags_en` — every engine tag, ruby, variable and control code,
  extracted and compared. Mismatch = hard fail.
- `flags` — `subject-guessed`, `gender-guessed`, `number-guessed`,
  `pronoun-marked`, `overflow`, `term-provisional`, `needs-tlc`.

Japanese does not mark singular/plural, gender, or articles (Honeywood's own
list of what makes JP→European output underdetermined). English forces a choice
constantly, so the rule is not "flag every choice" but this one test.

**GRAMMAR vs WITHHELD — the one test, binding everywhere** (rev. 2026-09-25, rules
audit #1; it replaces "keep the English exactly as ambiguous as the Japanese",
which produced English nobody reads that way — "the room" for 部屋, "the guilt
toward Dad" for a narrator's own 罪悪感):

> A gap is GRAMMAR when two first-time Japanese readers would fill it the same way
> without noticing a gap: fill it as they do; no flag, no DECISIONS row. A gap is
> WITHHELD when those readers could fill it differently, or when the text later
> turns on which filling is right: keep it open if the pack lists it or if English
> can do so without a contortion; otherwise take the pack-supported reading and flag
> `needs-tlc`. The `subject-guessed` / `gender-guessed` / `number-guessed` flags
> exist for WITHHELD gaps ONLY.

Those flags are the re-check queue when a reveal lands. A gap filled under GRAMMAR
is not a guess and does not enter the queue; flagging it wastes the reviewer's
budget, and a reviewer reading the flag reverts a fill every Japanese reader makes.
The per-file "ambiguity that the translation MUST keep open" lists in SUMMARY.md
were written under the OLD definition and mix real withholding with grammar habits
and structural notes: read every such list through this test until the lists are
re-tagged.

---

## 4. Consistency mechanics

- **One rendering per term, per FUNCTION** (rev. 2026-09-25, rules audit #2). Enforced by script against
  GLOSSARY.tsv, both directions: same JP → different EN (drift), and different JP → same EN (collision).
  A NOUN, name, place or coined term has one function and therefore one rendering. An INTERJECTION or
  response phrase is a homograph set — one Japanese spelling doing several jobs — so its row is locked per
  function, with the tell stated in the note column (the punctuation after it, what follows, who says it).
  Per line: does the word here do the job the row names? If not, write the natural English for the job it
  does and add a row for that function. A ruling made from ONE file locks the function seen in that file,
  never the string. A rendering that a GLOSSARY row prescribes is never an AI-ism.
- **Locked terms.** Once a term ships in a completed file it is locked. Unlocking
  requires: mark `superseded`, record the new rendering, and run a sweep across
  every completed file. Log the sweep in DECISIONS.md.
- **Translation memory.** Keep a JP→EN pair store of every completed line. VN
  scripts repeat heavily (route branches, recollection scenes, common
  interjections). SCOPE (rev. 2026-09-25, rules audit #2): identical JP gets
  identical EN for the CORE B2 verbatim replays, the CORE B3 refrains, and any line
  of about eight characters or more with the same speaker, addressee and function —
  and if the speaker, addressee or function differs, that must be deliberate and
  noted. SHORTER strings (「そう」「はい」「なんで」「だから」, every interjection) are
  matched by FUNCTION, not by bytes: a four-character string is not evidence of a
  repeated line.
- **Name spelling sweep.** A single regex pass per release checking every EN name
  form against GLOSSARY. Inconsistent name spellings across a long project is the
  classic multi-translator failure; it also happens with one translator over time.

---

## 5. QA checklist — run per file, before it counts as done

**Mechanical (scripted, zero tolerance).** Modelled on memoQ's automated check set.

- [ ] No untranslated lines; no lines left as raw Japanese
- [ ] No leftover kana/kanji in EN output except intentional romanization/terms
- [ ] Tag/variable/control-code parity JP vs EN (count, order, well-formedness).
      Malformed tags break export and can corrupt saves — one shipped VN broke
      save files because narration contained a colon the engine used as a delimiter
- [ ] Forbidden characters per engine (colons, brackets, backslashes, `@`, `%` —
      determine the engine's actual delimiter set ONCE and encode it as a check)
- [ ] Ruby / furigana preserved or deliberately converted
- [ ] Line length within the measured text-box ceiling, in **characters and in
      rendered pixels**, per text-box type (dialogue, narration, choice, name plate)
- [ ] Line-break count within the box's line ceiling
- [ ] Speaker field present and non-empty on every dialogue line
- [ ] Glossary compliance: every JP glossary term rendered with its fixed EN
- [ ] Glossary collisions: no two distinct JP terms sharing one EN rendering
- [ ] Honorific preservation: every JP honorific suffix ON A NAME present in EN (a suffix on a common noun
      is zero in EN: rev. 2026-09-25, rules audit #6. A regex for this check matches name + suffix only)
- [ ] Consistency: identical JP lines have identical EN (or a logged exception)
- [ ] Numbers, dates, counters match the source
- [ ] Punctuation conforms to STYLE.md (ellipsis form, dash form, quote form)
- [ ] Encoding: no mojibake, no smart-quote substitution the engine cannot render

**Linguistic (human/model read, per file).** Modelled on the MQM dimensions —
Accuracy, Terminology, Linguistic Conventions, Style, Locale, Audience, Markup —
each finding tagged **Major / Minor**.

- [ ] **Accuracy**: no omission, no addition, no mistranslation. Read EN against
      JP line by line. This is the category an LLM reviewer under-reports — an
      LLM evaluator put 27% of its flags in "style/awkward" while human MQM
      annotators concentrate on accuracy/mistranslation. Force the accuracy pass.
- [ ] **Speaker attribution**: does each line belong to the labelled speaker?
      Does the register match that speaker's CAST sheet?
- [ ] **Subject/gender/number**: every `*-guessed` flag reviewed against context.
      Is the English deciding something the Japanese's OWN READER could not decide?
      (rev. 2026-09-25, rules audit #1. A fill that any first-time Japanese reader
      makes is not an error and is not reverted; see the §3 test.)
- [ ] **Register**: politeness level matches the RELATIONS row for this pair
      in this file. No unexplained 敬語→タメ口 drift.
- [ ] **Honorific drift**: no suffix silently added, dropped or changed
- [ ] **Voice**: no character flattened into generic neutral English; no
      character given a quirk that is not in the Japanese
- [ ] **No invention**: nothing in EN that is not in JP (jokes, emphasis,
      swearing, interjections, emotional colour)
- [ ] **No smoothing**: repetition, flatness, and abrupt shifts in the JP survive
      into the EN
- [ ] Tone across the file matches the JP's tonal arc (no tone flattening)
- [ ] New terms added to GLOSSARY; new facts appended to SUMMARY with `as_of`
- [ ] Queries raised logged in QUERIES.md, not silently guessed

**In-context (the only pass that catches the rest).** Run the build. Nothing is
"done" until it has been seen in the running game. This is where pros catch
overflow, wrong speaker, broken tags, and lines that were undecidable on a
spreadsheet.

---

## 6. Failure modes to check for

Documented, real, and all of them apply to an LLM pipeline more than to a human one.

1. **Wrong speaker.** The defect audiences notice most. Cause: line-by-line work
   with no scene context.
2. **Invented referents** (title rev. 2026-09-25, rules audit #1). Japanese drops
   the subject constantly and English forces one; the defect is not the filling, it
   is filling in a referent the Japanese reader cannot identify — a model
   confidently supplying "she" where the text names nobody AND nobody is inferable.
   Where the referent is obvious to a first-time Japanese reader, supplying it is
   reading, not invention (§3). Documented symptom of context-free spreadsheet
   translation: unstable first-person pronouns, wrong gender, mixed politeness.
3. **Gender errors.** Fallout 4's JP localization defaults the player's speech to
   masculine; Stardew Valley characters flip between male and female speech
   patterns inside one conversation. Both are the no-character-sheet failure.
4. **Honorific drift.** `-san` in one file, nothing in the next, `-chan` in a
   third, with no event behind it.
5. **Name spelling drift.** Same character, two romanizations, hundreds of files apart.
6. **Term drift and term collision.** Two JP terms collapsed into one EN word,
   destroying a distinction the story depends on.
7. **Register drift.** A character who uses 敬語 to a superior throughout
   suddenly casual, because that one line was translated without the pair context.
8. **Text-box overflow.** Japanese is compact; English is longer. Kanji → English
   expansion is a named professional hazard. Catch it in pixels, not characters.
9. **Broken tags / variables / control codes.** Blocks export; can corrupt saves.
10. **Ambiguity foreclosed too early.** The Japanese kept something unclear on
    purpose; the English picked a reading and killed the later reveal.
11. **Ambiguity manufactured.** The reverse — hedging into "they", "s/he",
    passive voice to dodge a decision the Japanese actually made. This is the
    documented no-context hedge and it reads as mush.
12. **Tone flattening.** Every character converges on the same mid-register
    English. The direct consequence of missing CAST sheets.
13. **Over-localization.** Any of the banned items in §0. For this project it is
    a defect, not a style choice.
14. **Smoothing.** Making the English nicer than the Japanese. Burton Watson's
    translations are criticized for exactly this: a smooth surface lets the reader
    skim past the details, and the details were the point.
15. **Unanswered queries shipping silently.** Log them or they become permanent.
16. **Duplicate/ambiguous short strings.** Identical short lines belonging to
    different scenes. In a LocJam post-mortem every transition screen read
    "Office" and the translator had to reconstruct meaning from screen IDs.
17. **Superseded glossary terms never swept back** into already-finished files.

---

## 7. Rules for agents on this project

- **Never read ahead.** Translating file N means SUMMARY blocks `<= N` only — and CORE.md fenced the same
  way: run `sh tools/core_fenced.sh <N>` and read `notes/_tmp/core-<N>.md`, not CORE.md whole (rev.
  2026-09-25, rules audit #4: CORE's later-fact rows, C4 resolutions and D1 "LATER" clauses state reveals in
  the clear, which contradicted this rule). The knowledge fence is TRANSLATOR-BRIEF-v2 §0.
- **Never invent a heuristic.** If STYLE.md or the plan is silent, stop and write
  the question in QUERIES.md. Do not pick a convention and proceed.
- **Never guess silently.** Guess + flag + log, or ask.
- **Save to disk as you go.** Files written per batch, PROGRESS.md updated. Never
  hold a batch's work in conversation only.
- **Never touch the game's story files outside your assigned range**, and never
  summarize plot outside SUMMARY.md.
- Translator ≠ editor ≠ checker. An editing pass may not change meaning. A TLC
  pass may not change English style. Keep the passes separate even when the same
  model runs both.
