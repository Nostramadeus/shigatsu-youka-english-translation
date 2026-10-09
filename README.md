# Shigatsu Youka (死月妖花～四月八日～) English translation

## Play it in English: 3 steps

1. **Get the free Japanese game** (v2.0.0.4) from the author: https://www.freem.ne.jp/win/game/19917 . Unzip it anywhere.
2. **Download the newest patch zip** from https://github.com/Nostramadeus/shigatsu-youka-english-translation/releases/latest .
   Unzip EVERYTHING in it into the game folder, next to `死月妖花～四月八日～.exe`. Overwrite when asked.
3. **Start the exe.** That is it. No game file is modified; the engine loads the loose English files.

Good to know:
- **Boxes instead of letters?** Set Windows' system locale to Japanese (or run the exe through Locale Emulator) and add the Japanese language pack.
- **Do not use the game's own full-screen button** (second button on the toolbar). It resizes every other window. Use Magpie instead: `README-BEFORE-PLAYING.txt` in the zip explains it.
- **Do not look the game up online.** Store pages and wikis spoil its length and structure in the first paragraph.
- **Updating the patch:** unzip the new one over the old. Saves keep working.
- **Japanese text left somewhere?** Screenshot it (Win+Shift+S) and open an issue here.


Free LiveMaker 3 visual novel by New++ (freem game 19917, v2.0.0.4). Game lives at
`F:\4gatsu_8ka_Ver2.0.0.4\死月妖花～四月八日～.exe` (1 GB, the whole game is packed inside the exe).
This folder holds only the SCRIPTS (48 MB). Never copy the game here.


## How to contribute

Fix a line, add a glossary term, extend the translation. Pull requests and issues both welcome.

**What is what**

| Folder | What is in it | Edit it? |
|---|---|---|
| `lns-en-55/` | the English story scripts, one file per scene block. This is the text players read. | **yes, main target** |
| `lns-en/` | the earlier English tree; a few early scripts still ship from it | yes, same rules |
| `tsv-en/` | English menus, notices, tutorial tips, navigator titles, synopses, encyclopedia | yes |
| `patch/` | per-script label / ruby / title tables, plus the two readme files that go inside the patch zip | yes, for wording |
| `work/グラフィック/`, `work/images/out/` | the English pictures: shipped `.gal` files and the English PNGs they were built from | through `tools/images/` |
| `notes/` | the translation rules (`v2/METHOD.md`, `v2/STYLE.md`, `v2/CORE-RULES.md`, `v2/OWNER-RULINGS.md`), glossary (`v2/GLOSSARY.tsv`), character voice sheets (`v2/CAST.md`), read-through summary (`v2/SUMMARY.md`), decisions log, open questions | read first; add a glossary row when you coin a term |
| `review/` | proofreading pages, Japanese left, English right, one per script | regenerate with `tools/render_review.py` |
| `tools/` | build scripts (pylivemaker): compile scripts, build tables, typeset pictures, assemble the patch | if you build |
| `research/` | what the author said about fan translations (the license) | no |

**Rules in four lines**

1. Literal translation, no localization. Keep the order of ideas and the images of the Japanese where English allows.
2. Honorifics stay (-san, -kun, -chan). Names are given name first.
3. A lost nuance gets a short translator note at the end of the line: `[TN: ...]`.
4. Never change a tag. `<STYLE ...>`, `<BR>`, `<PG>`, `<TXSPN>` and friends stay exactly where they are; only the English words between them change.

**Smallest useful contribution**

1. Open the script in `lns-en-55/` (the review page in `review/` tells you which file and line).
2. Change the English. Check `notes/v2/GLOSSARY.tsv` for the fixed rendering of names and terms.
3. Open a pull request. No git? Open an issue with file, line, and the suggested wording.

**Building the patch yourself (optional)**

You need your own copy of the game and `uv` (pylivemaker runs through it). Extract the scripts from the exe into `orig/` and `lns/` as the Layout section below describes, then `sh tools/compile_en.sh <id>` and `uv run tools/build_en_folder.py --zip`. Nothing extracted from the game goes into this repo: the author forbids publishing game data.

---

## Internal notes (project history, kept as is)

## License for fan translations (creator, ci-en page; noted 2026-10-05)

The creator's ci-en page states (EN rendering): "Fan translations & derivative works: publishing fan
translations or adapting the scenario into other content is free, but you must clearly state that it is
unofficial (secondary creation / 二次創作)." Consequence for this project: every distributed artifact
(patch readme, release post, title/opening screen if text is injected, review HTML pages) must carry a
visible "Unofficial fan translation (非公式・二次創作). Not affiliated with New++." line. Applied 2026-10-09: patch/README-EN.txt,
patch/README-BEFORE-PLAYING.txt, tools/render_review.py (+ every review/*.html). No text is injected into the title screen, so nothing there.

Exact JP wording (ci-en post 2026-07-29, saved in `research/_author-src/`):
「有志による翻訳や別コンテンツでのシナリオ化等の公開は自由ですが、必ず「非公式（二次創作）」である旨を明記してください。」

SECOND RULE in the same post: publishing program, image, audio, BGM or text data extracted directly from
the game is forbidden (「ゲーム本編のプログラム、画像、音声、BGM、テキストデータ等を直接抽出・複製して公開する行為」).
Consequences: never publish the patched exe, the `orig/` or `lns/` script files, or review pages that show
the JP script lines. A public release = English text + a patcher that modifies the player's own copy.
This repo folder itself must stay private. Rules cover the free version only; the author gives no help
to translators. Full research: `research/_author-satsuki.md`.

## THE RULE (the owner, 2026-09-21) — no structure spoilers, ever

the owner is reading this story blind. In any report, summary, progress note or chat:
- never say chapter/scene X of N, never count arcs, chapters, scenes, routes or endings
- never state total length, total hours, total characters, total lines, "one of the longest"
- never name arcs (編), never describe how the story is divided
- never estimate tokens or time for the WHOLE game
- never mention extras, unlockables, alternate routes
- REVOKED 2026-10-01 (owner): no precise line / char counts or cards-per-part even for the chunk being worked on.
  Say done / not done; token cost is fine; exact sizes stay in notes/RESUME.md and BACKLOG.md only.

`line-counts.tsv`, `orig/データベース/*.tsv` and the `orig/グラフィック` folder names all leak this. Agents read them, the owner does not. Filter before reporting.

Also carry: no AI-isms in dialogue (memory `manga-dialogue-no-ai-isms`), neutral literal prose in reports.

## Layout

| Path | What |
|---|---|
| `orig/` | every script/data file from the exe, untouched (542 `.lsb`, 95 `.tsv`, menus). This is also the UNDO for any patch. |
| `csv/` | `lmlsb extractcsv` of every `.lsb` with text (423 files). For counting and reading only. NOT the translation format (CSV round-trip drops `<STYLE>` tags = character-name colors). |
| `lns/` | `lmlsb extract` output = decompiled scripts with tags. THIS is what gets translated. One `.lsbref` + several `.lns` per `.lsb`. |
| `line-counts.tsv` | per-file line and char counts. Spoiler-heavy, agents only. |
| `extract_scripts.py` | pulls only script/data files out of the exe (no images/audio). Already run. |
| `extract_csv_all.py` | writes `csv/` + `line-counts.tsv`. Already run. |

Tool: pylivemaker, run without installing: `uvx --from pylivemaker lmlsb ...`, `uvx --from pylivemaker lmpatch ...`.
Run `lmlsb dump/extract` with the working directory INSIDE `orig/` (it wants the project root).

## Chapter 1 (the first chunk)

Game start flow: main menu `00000001.lsb` → opening scene `00000024.lsb` → system `000015DC.lsb` → scenario navigator `0000001C.lsb` → first scene `000004A7.lsb` → back to navigator.

| Script | Lines | JP chars | Role |
|---|---|---|---|
| `00000024.lsb` | 225 | 4,422 | opening scene, plays on first boot |
| `000004A7.lsb` | 111 | 2,563 | first scene from the navigator |

Each scene script is self-contained and returns to the navigator, so "one chapter" = one or two scene scripts.

## Text format inside `.lns`

```
右を見ると、<STYLE ID="1">春花</STYLE>が私の肩にもたれ、すやすやと眠っている。
<STYLE ID="2">「</STYLE><STYLE ID="1">春花</STYLE><STYLE ID="2">、起きて。寝るなら、部屋に行こう」</STYLE>
```
`STYLE ID="1"` = character name color, `ID="2"` = spoken dialogue color. `<BR>` line break, `<PG>` page/click break, `<TXSPN>/<TXSPS>` text speed, `<EVENT>`/`<SCENARIO>` engine markers. Translate only the text; keep every tag and its order.

## Pipeline per chapter

1. `cd orig && uvx --from pylivemaker lmlsb extract <id>.lsb -o ../lns` (done for the two chapter-1 scripts)
2. Translate `lns/<id>-*.lns` in place (or into `lns-en/` mirroring the names). Tags stay, `.lsbref` stays.
3. Compile back: `cd orig && uvx --from pylivemaker lmlsb batchinsert --no-backup ../work/<id>.lsb ../lns-en/` on a COPY of the lsb in `work/` (never on `orig/`).
4. Patch the exe in place, no duplicate on F: `uvx --from pylivemaker lmpatch --no-backup -r "F:\4gatsu_8ka_Ver2.0.0.4\死月妖花～四月八日～.exe" work\`
   - lmpatch builds the new 1 GB archive in `%TEMP%` on C: (needs ~1 GB free there), then overwrites the exe on F:. F: peak stays flat.
   - Undo = `lmpatch --no-backup -r <exe> orig\` with the same file names (or re-unzip the game).
5. Half-width Latin text: LiveMaker renders English as full-width by default. Set `PR_FONTCHANGEABLED = 0` on the message box via `lmlsb edit` (pylivemaker usage docs, "half-width" section). Do this once, verify on chapter 1.
6. Windows Defender may flag the patched exe (it flags the original too). Add the game folder as an exclusion.

## Proofreading for the owner

He proofreads ~100 lines per chunk by hand. Give him an HTML page (JP left, EN right, line numbers, speaker color kept) at `review/<id>.html`. HTML, never markdown.

## Progress

- 2026-09-21: scripts extracted, chapter 1 identified, tag format understood. Nothing translated yet.

## 2026-09-22 rules from the owner

- Spoilers of ANY kind are forbidden in anything he reads: no small details, hints, meta, structure, "matters later". None.
- Prep before translating = full read-through of every script into notes under `notes/` (agents only, never shown to the owner): `characters/<name>.md` (self-reference, how they address others, speech level, tics, tone shifts), `glossary.md` (names, places, terms, fixed renderings), `relations.md`. Read in chunks, write notes to disk after every chunk, keep `notes/PROGRESS.md` (last file read / next file).
- Translation leans literal. No editorializing, no sharpening foreshadowing, no smoothing. Keep what is on the page.
- Short translator notes allowed where a non-spoiler nuance is lost in English (e.g. first line of a boku-speaking girl: "she uses boku, the male first-person pronoun"). Put them where the line is.
- Chapter size target: ~5-8k English words (between War and Peace ch.1 and Iliad Book 1) = ~12-19k JP chars.
  Chapter 1 candidate: `00000024` + `000004A7` `000004BB` `000004CF` `000004E3` = 889 lines, 18,861 chars. Navigator order still to verify in-game.
- 2026-09-22 decision: Opus does the read-through and the translation. Notes are LIVING files: update a
  character sheet or glossary entry the moment the story changes it, and keep an "as of <file>" line per
  fact so early-chapter translation does not leak later knowledge into wording. Reports to the owner contain
  file names, counts, done/next only.
- DOCTRINE (2026-09-22): TRANSLATION, ZERO LOCALIZATION. Register = Lattimore's Iliad: faithful,
  line-for-line, keep the source's images and order where English allows, no smoothing, no added jokes,
  no cuts, no replaced cultural references, slightly foreign is acceptable. Honorifics and pronoun /
  speech-level nuance are kept or carried by a short translator note. See notes/METHOD.md.
- 2026-09-24 state: NOTHING RUNNING. Research done (research/translator-workflow.html, notes/METHOD.md,
  Murakami tense trick banned). Next step on the owner's word: the READ-THROUGH (Opus, effort high, one agent,
  chunked, notes/ files per METHOD.md, PROGRESS.md checkpoints). Translation only after the read-through.
  Optional first: 40-line bake-off (Opus 5 / Fable 5.1 / others) on the opening scene, blind HTML for the owner.

## 2026-09-25: translation pass running; playable English folder

- **`F:\4gatsu_8ka_EN\`** = the English game folder. The exe there is a HARD LINK of the Japanese one (same
  bytes, no extra disk; do not `lmpatch` either copy, both would change). It has its own `save.dat`. The loose
  files next to the exe (`*.lsb`, `データベース\*.tsv`, `メッセージボックス作成.lsb`) override the packed archive;
  `uv run tools/build_en_folder.py` syncs them from `work/` per `tools/ship-list.txt`, `--zip` also writes the
  friends' patch to `patch/`. Never put the harness skip files (`0000001C.lsb`, skip build of `000000F2.lsb`) in
  the ship list; the builder refuses them.
- Pipeline per script: agent translates `lns/<id>-*.lns` → `lns-en/` (brief `notes/TRANSLATOR-BRIEF.md` +
  `notes/TL-AGENT-ADDENDUM.md`) → TLC agent (`notes/TLC-BRIEF.md`) → `uv run tools/qa_check.py <id>` →
  `sh tools/compile_en.sh <id> [patch/labels-<id>.tsv]` → `work/<id>.lsb` → `build_en_folder.py`.
- System text outside the scripts (boot prompts, notices, choice labels, title captions, navigator titles,
  tutorial tips): `notes/SYSTEM-TEXT-BRIEF.md`; tables live as UTF-8 in `tsv-en/`, `tools/build_tsv.py` writes
  the CP932 copies; string literals inside commands via `tools/lsb_strings.py list|apply`.
- Status board: `notes/PROGRESS.md` (agents only; contains structure facts).
