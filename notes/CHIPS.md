# CHIPS.md — soft polish rules, versioned, with a per-part application table (owner's idea, 2026-09-26)

A chip is a soft rule added after some parts were already translated. Each chip says what it asks, and the table
says which parts it has been applied to (a sweep worker reads the affected lines and decides each one). New parts
get every chip in the drafter brief; old parts get a sweep when the owner says so. Cost per part per chip
~100-150k tokens (a sweep reads only lines the mechanical filter flags).

| chip | rule (short) | added | applied to |
|---|---|---|---|
| CHIP-01 | punctuation rhythm (owner ruling 2026-09-26, SOFT): a JP 読点 is a pause the reader feels; keep it as an English comma wherever English can hold a comma, INCLUDING after a sentence-initial conjunction (でも、あの人は死んだ。 -> "But, that person died."); drop it where English grammar cannot take one (between a subject and its verb, before a short object). SOFT means (owner, 2026-09-26 afternoon): the pause wins by default, but any other consideration may overrule it on a given line, above all "would this English sound absurd or unreadable". The sweep worker decides line by line and does not apply the rule mechanically; when a comma would make the line stupid, drop it and move on, no log row needed. | 2026-09-26 | parts 1-3: folded into the full-read pass 2 (notes/FULL-REVIEW-BRIEF.md, 2026-09-26); part 4+ via brief |
| CHIP-02 | image order carries information: keep the JP order of images where it carries sequence or logic, if the English stays readily comprehensible (STYLE, 2026-09-26) | 2026-09-26 | parts 1-3: folded into the full-read pass 2 (notes/FULL-REVIEW-BRIEF.md, 2026-09-26); part 4+ via brief |

Mechanical filter for CHIP-01 sweeps: lines where the JP 読点 count differs from the EN comma count, excluding
sentence-initial conjunction commas. Filter for CHIP-02: lines where the EN clause order differs from the JP
clause order (a heuristic; the sweep worker decides).
