# CHIPS.md (v2) — soft polish rules, versioned, with a per-part application table (owner's idea, 2026-09-26)

A chip is a soft rule added after some parts were already translated. New parts get every chip through the
TRANSLATOR-BRIEF; old parts get a sweep only when the owner says so. A sweep worker reads the lines a mechanical
filter flags and decides each line; it never applies a chip mechanically.

| chip | rule | source | 5.5 tree (lns-en-55) | old tree (lns-en) |
|---|---|---|---|---|
| CHIP-01 | A JP 読点 is a felt pause: keep it as an English comma wherever English can hold one, INCLUDING after a sentence-initial conjunction; drop it where English grammar cannot take one. SOFT: any other consideration may overrule it on a line, above all "would this sound absurd or unreadable"; no log row when declined. JP でも、あの人は死んだ。 = "But, that person died." | O-30 | drafters from the start (TRANSLATOR-BRIEF) | parts 1-3 folded into the full-read pass 2 |
| CHIP-02 | Image order carries information: keep the JP order of images where it carries sequence or logic, if the English stays readily comprehensible on first read. JP ――夢の中に響く、時計の音。 = "―Echoing inside a dream, the sound of a clock." | O-33 | drafters from the start | parts 1-3 folded into the full-read pass 2 |

Sweep filters (heuristics; the worker decides): CHIP-01, lines where the JP 読点 count differs from the EN comma
count, excluding sentence-initial conjunction commas. CHIP-02, lines where the EN clause order differs from the JP.
A chip edit is logged `CHIP | <id>:<file>:<line> | JP | EN before | EN after | CHIP-nn`.
