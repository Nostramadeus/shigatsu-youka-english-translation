# OWNER-RULINGS.md — the owner's decisions that every rule book must keep (Fable, 2026-09-26 15:55)

Purpose: the rule books (METHOD.md, STYLE.md, CORE.md, TRANSLATOR-BRIEF-v2.md, REVIEWER-BRIEF.md,
FULL-REVIEW-BRIEF.md, CHIPS.md) are being remade on Opus 5.5 (owner order 2026-09-27 00:05). Their MODEL-made
content may be rewritten freely. Their OWNER-made content may not change in substance. This file is the ledger of
the owner-made content. Each row: id, ruling, date, where it is written now. The remake agent copies every ruling
into the new books and checks the ledger off at the end (a row not carried = a defect).

## A. Doctrine
| id | ruling (owner's substance) | date | now in |
|---|---|---|---|
| O-01 | TRANSLATION, ZERO LOCALIZATION. Register model Lattimore's Iliad: faithful, line for line, source images and order, no smoothing, no quirking-up, no cut/softened lines, no replaced references; slightly foreign surface is fine. Never Treehouse/8-4-style rewrites. | 2026-09-22 | METHOD §0, BRIEF-v2 §0 |
| O-02 | Two failure modes, BOTH banned: ADDITION (invented quips, interjections, personality, AI-isms) and FLATTENING (Mushoku Tensei EN example: 小太りブサメンのナイスガイだ flattened; the "but" explains the irony, euphemisms soften insults, register gone, jokes die). Recreate the effect from the source's OWN material: same register, same density, same order; jokes by MECHANISM not by meaning; insults keep weight; no padding, hedging, explaining. | 2026-09-24 | METHOD §0b (keep the Mushoku example and the sentence-level test) |
| O-03 | Register SEQUENCE inside a phrase is the joke (小太り soft -> ブサメン crude net-slang -> ナイスガイ ironic katakana English). Density is a DIAGNOSTIC not a rule: 20 EN words for 5 moji can be right; what must match is weight distribution and where the punch lands. | 2026-09-24 | METHOD §0b |
| O-04 | JP ORDER AND FEEL OVER NATURAL ENGLISH. "The time had gone past midnight" (時刻は深夜0時を回っていた) STAYS. A "no subject calques" rule was REJECTED. Only clearly unreadable lines are errors; candidates go to a STIFF-CANDIDATE list for the OWNER to judge; nothing enforced per line; no new stiffness rules added by agents. README-EN states this philosophy. | 2026-09-26 | STYLE (SUBJECT CALQUES line), REVIEWER-BRIEF, FULL-REVIEW-BRIEF |
| O-05 | Honorifics, pronoun and speech-level nuance are KEPT or carried by a short translator note; never re-encoded by warping English (no fake dialect, no odd grammar). Honorifics stay as suffixes on names. | 2026-09-22 | METHOD §(never re-encode), BRIEF-v2 |
| O-06 | Translator notes [TN: ...] ALLOWED where non-spoiler and untranslatable (e.g. first time a character speaks with boku). Short, at the proper spot. | 2026-09-22 | STYLE TN cases, BRIEF-v2 |
| O-07 | No AI-isms in dialogue (Well, / I mean, / Look, / honestly / kind of / wry asides / "It's not X, it's Y"). The owner is testing whether the text reads human. | 2026-09-21 | BRIEF-v2 §0 |
| O-08 | AMERICAN English project-wide (spelling and vocabulary: elevator, apartment, first floor, trash, color). | 2026-09-25 | STYLE, BRIEF-v2 (Q1161) |
| O-09 | Name order GIVEN NAME FIRST (Haruka Niimura); historical の-names and titles stay; surname-only address unaffected. | 2026-09-24 | STYLE line 6 |
| O-10 | DO NOT DECIDE WHAT THE AUTHOR LEFT UNDECIDED (replaces "exactly as ambiguous"). Grammar gaps a native fills (部屋に行こう -> "your room") are filled; withheld gaps (あの人, ungendered figure) stay open; else flag. The owner himself overruled a reviewer's "the room". He distrusts blanket literalism rules: test every new rule against "would this make stiff English". | 2026-09-25 | BRIEF-v2 §0, METHOD §3, RULES-AUDIT-fable #1 |
| O-11 | Never shorten a translation to fit a box; the engine pages long boxes. | 2026-09-26 | PROGRESS 23:10 (not yet in a rule book: ADD to STYLE) |

## B. Review and process
| id | ruling | date | now in |
|---|---|---|---|
| O-20 | REVIEW = EVERY LINE, always. No sampling, ever (25% sampling was rejected flatly). Cost is not a reason to skip lines. | 2026-09-26 | STYLE REVIEW COVERAGE, REVIEWER-BRIEF, FULL-REVIEW-BRIEF |
| O-21 | Reviewers read CONTIGUOUS WINDOWS, never isolated lines; multi-line units (haiku, lists, split sentences) always read whole; every short/elliptical cell checked for REFERENT-BINDING (owner catch: どれか1つでも……。 -> "Even just one of those", not "Even any one of them"). | 2026-09-26 | REVIEWER-BRIEF, FULL-REVIEW-BRIEF, BRIEF-v2 ELLIPTICAL CELLS |
| O-22 | A drafter reads the whole script and packet before block 1; at each later block re-reads its last five English lines so a beat spanning the block boundary is carried on purpose. | 2026-09-26 | BRIEF-v2 §2 |
| O-23 | The owner proofreads ~100 lines per chunk himself; review page shows only the PLAYED path (no looping variants). | 2026-09-26 | RESUME/memory (review page fix owed) |
| O-24 | No claim of "convention" for JP punctuation without a MODERN source (2022 文化審議会建議「公用文作成の考え方」, not 1946). | 2026-09-26 | memory; STYLE must cite it if it cites anything |
| O-25 | Reports to the owner: file ids, line counts, tokens, minutes, done/next ONLY. No plot, structure, mechanics, screen descriptions, note counts, spatial/ordinal words about where things sit. | 2026-09-21..26 | every brief's report section |
| O-26 | Real personal names never appear anywhere in the project folder; the credit line names only the author. | 2026-09-25 | RESUME rules |

## C. Punctuation and typography
| id | ruling | date | now in |
|---|---|---|---|
| O-30 | JP commas are felt pauses: keep them as English commas even after a sentence-initial conjunction ("But, ..."), EXCEPT where English grammar cannot take one; SOFT rule, overruled whenever the English would sound absurd, never applied mechanically ("don't be autistic about it"). = CHIP-01. | 2026-09-26 | CHIPS.md CHIP-01 |
| O-31 | Space at a {PAUSE} cell boundary: when a box is split by {PAUSE ""} and the first cell ends in sentence punctuation or a closing quote, the English first cell ends with ONE ASCII space. | 2026-09-26 | STYLE line 73, tools/pause_space.py |
| O-32 | ENGLISH RUBY: reading-aid rubies dropped automatically; meaning-carrying rubies (double reading, pun, 圏点, gloss) kept above the English via patch/ruby-<id>.tsv. | 2026-09-25 | STYLE line 52 |
| O-33 | IMAGE ORDER CARRIES INFORMATION: where the JP orders its images to carry sequence (dream, then sound, then waking), English keeps that order even at the cost of a fronted phrase; soft, forward-looking, no re-edit of shipped lines for it. | 2026-09-26 | STYLE line 63 |
| O-34 | 【】 and ～ are allowed (CP932). U+3000 / full-width （） only where a device needs them (CORE A rows win over the checker). | 2026-09-25 | STYLE allowed set |
| O-35 | Three shipped DECISIONS rows that swapped U+3000 for ASCII are reviewer re-check candidates (owner distrusts silent flattening of layout spaces). | 2026-09-25 | memory |

## D. Tooling and shipping (not rule-book content, but the books reference them)
| id | ruling | date |
|---|---|---|
| O-40 | Patch-only distribution, never the game files; ask the author (@4gatsu_8ka) first; skip files 000000F2/0000001C never ship. | 2026-09-22 |
| O-41 | Nothing goes to friends until a full on-screen mouse run shows zero Japanese and zero layout defects. | 2026-09-27 |
| O-42 | Every agent on Opus 5.5 (subagent_type opus55); the "opus" alias is Opus 5 and is banned; fable is not a substitute. | 2026-09-27 |
| O-43 | Retranslate all of part 1 from scratch on 5.5, review every line; ask about parts 2-3 and 000016AE. Assume 5.5 is better (owner 15:45, 2026-09-26): do not wait for the bake-off verdict to start work. | 2026-09-27 / 09-26 15:45 |

## What the remake may change
Anything not in this ledger that the books currently say is MODEL-made: the 18 rules-audit items of 2026-09-25 that the
owner did not author (check notes/RULES-AUDIT-fable.md: items marked as the owner's stay), the tense "I thought:" test,
the interjection-by-function rule, the kinship-word table, the GRAMMAR-vs-WITHHELD test wording, the packet mechanics,
the block-size and logging mechanics. Rewrite for clarity and correctness against the JP; keep whatever survives a
check against O-04 ("would this make stiff English?") and O-10.

## E. Owner answers to the 2026-09-26 questions page (review/questions-2026-09-26.html), recorded 18:15
| id | ruling (owner's words, condensed) | date |
|---|---|---|
| O-50 (S1) | Translator notes: keep the OPEN rule (any untranslatable, non-spoiler point may get a short note). | 2026-09-26 |
| O-51 (S2) | Set phrases: lean strongly idiomatic, as long as no layer or subtext is lost. | 2026-09-26 |
| O-52 (S3) | Clause order: keep the JP order where English holds it, as a LEAN, not a hard rule. | 2026-09-26 |
| O-53 (S4) | のだろう / かな: ", I wonder" ALLOWED (it keeps the period ending; a question mark feels different). Fable may vary when three land in a row. | 2026-09-26 |
| O-54 (S5) | Tense: owner has no preference; Fable keeps the current rule (English past base; present allowed for the narrator's own thought, the "I thought:" test). | 2026-09-26 |
| O-55 (S6) | よう = "Hey". | 2026-09-26 |
| O-56 (S7) | One "..." per JP …. | 2026-09-26 |
| O-57 (R1/R7/QB55-2-04) | Kinship words for NON-relatives stay Japanese, untouched: Obasan, Ojisan, Onee-san (speech and narration). Readers can handle it. The narrator's OWN parents in narration stay "Mom"/"Dad"/"my mother" as now. | 2026-09-26 |
| O-58 (R2) | 四月八日 in text is just a date: "April 8th"; the subtitle, if translated, uses the same words. | 2026-09-26 |
| O-59 (R3) | Name-order jokes: keep the JP order in those lines + [TN: In Japanese the family name comes first.] | 2026-09-26 |
| O-60 (R4) | Dialect: a SLIGHT accent in English is allowed, plus a TN that it is a heavy one in the original. The "no eye-dialect" ban was model-made; the owner never wrote it. Full rule list to be audited by the owner (review/rules-audit.html). | 2026-09-26 |
| O-61 (R5) | 卍 = "manji" (no note needed). GENERAL RULE: it is 2026; unfamiliar Japanese terms (manji, torii, etc.) stay as they are, people can look them up. No localization of culture nouns. | 2026-09-26 |
| O-62 (R6) | 『月がきれいですね』 literal + short note on the coded meaning. | 2026-09-26 |
| O-63 (R8) | The doubled polite ending: context decides; if unclear, keep the stumble (doubled English) and mark a note so it can be fixed later. | 2026-09-26 |
| O-64 (R9) | Police ranks: LITERAL ("Assistant Inspector"), a one-time TN allowed. Non-US readers do not know US names either. | 2026-09-26 |
| O-65 (ST1) | CHARACTER VOICE IS A UNIVERSAL RULE: reviewers judge every line against the speaker's CAST sheet (a meek line must not come out bold and clinical). Interpretation like "this sounds like a scientific man, not a demure girl" is expected from the reviewer, based on the bios. ST1: ", I'm sure" is better than "Surely." | 2026-09-26 |
| O-66 (ST2-ST11) | Lines that could be MISREAD (ST2, ST3) get fixed; mere slight awkwardness (ST4-ST11) is fine. The "name must open the line" premise is FALSE: the name's color run can move by splitting the style tags (BRIEF-v2: move the tags with it). | 2026-09-26 |
| O-67 (P1) | Parts 2-3: RETRANSLATE on 5.5 (confirmed; already done). | 2026-09-26 |
| O-68 (P2) | Later-file notes in a packet are tolerable for voice only, never for events/hints/callbacks; be careful. Accept the reviewed text. | 2026-09-26 |
| O-69 (A1) | Logo lettering: leave as art (the small English reading line above the logo stays). | 2026-09-26 |
| O-70 | NO translator notes for culture nouns a reader can look up (shinigami, hanami, nata, goshinboku, drink bar, sakiika, torii, manji, police ranks, Obasan). Notes stay only for wordplay mechanisms and numbers the reader would misparse (puns, name-order joke, coded phrases, memorial-year counting). "Apply throughout." | 2026-09-26 18:25 |
| O-71 | A hanging counterfactual (もし……たら／あれば……。) may be rendered "If only ..." : the wish is the mechanism, not an addition. 00000024 00000799:100 keeps "If only". | 2026-09-26 18:25 |
| O-72 | Owner wording for 00000024 目を開けると、ちょうど正面にテレビ。: "When I opened my eyes, right in front of me was the TV." (smallest change that reads normal without moving away from the JP). | 2026-09-26 18:25 |
| O-73 | 貼り付けられてた = "taped to" is fine: a concrete everyday verb any native would use for the JP action is NOT an addition (the judge's "tape is not in the Japanese" was too literal). | 2026-09-26 18:30 |
| O-74 | Section/arc TITLES: a Japanese reader gets the kanji's meaning, so the English gives it too: translate the meaning (direct English title), no romanization (replaces the current "Meicho Arc"/"Jusatsu Arc" labels; apply in the label maps + navidata). | 2026-09-26 20:05 |
| O-75 | The reversible CHANT: build an English chant that is solvable the same way (reads backwards into the hidden sentence). If it cannot be done well, the English must say (TN) that the puzzle is not solvable in English. Owner's Umineko-poem principle: puzzles stay solvable or are declared unsolvable. (Occurs outside parts 1-3.) | 2026-09-26 20:05 |
| O-76 | ロリコン label: "lolicon" (loanword). | 2026-09-26 20:05 |
| O-77 | EARLY-REACHABLE SIDE CONTENT (chatter, commentary, reference/document bodies, encyclopedia/profile rows) that a player can open within parts 1-3 MUST be translated before the friends build counts as done; the owner does not want "why isn't this translated". | 2026-09-26 20:05 |
| O-74a | AMENDED: section/arc titles stay ROMANIZED and carry the literal meaning in square brackets: "Meicho Arc [Clear Proof]". | 2026-09-26 20:15 |
| O-58a | Date form: "April 8" (numeral, no ordinal suffix) wins; 45+ shipped lines already use it. Supersedes the "April 8th" wording in O-58. (Fable, uniformity) | 2026-09-26 21:20 |
