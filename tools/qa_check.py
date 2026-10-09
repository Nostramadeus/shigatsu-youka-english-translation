"""Mechanical QA for one translated script: `uv run tools/qa_check.py <lsbid>` (from the project root).
Compares lns/<id>-*.lns (JP) with lns-en/<id>-*.lns (EN). Stdlib only. Exit 1 on any hard failure.
Checks (METHOD.md section 5, mechanical): file set parity, line-count parity, tag/command sequence parity per
line, leftover Japanese in text lines, full-width Latin/punctuation, quote-mark count parity, forbidden ellipsis
and dash forms per STYLE.md, .lsbref identical, glossary name spellings.

rev. 2026-09-25, rules audit #3: U+3000 (full-width space), full-width parentheses （） and the banner brackets
【 】 (U+3010/U+3011, CP932 0x8179/0x817A) are CP932-legal and are layout devices CORE A tells the translator
to KEEP, so they are SOFT warnings, not hard failures. Every other Japanese glyph and every other full-width
form stays HARD. A CORE A row beats this checker: leave the glyph and log a DECISIONS row.
Also soft: a run of three or more ASCII hyphens is not a dash error — the source prints rules like
"-----(中略)-----" with ASCII hyphens, and those are copied as they are.
rev. 2026-09-25, rules audit #9: the length-ratio line is a sanity band only; it names no control figure,
because drafters were trimming and padding toward one.
rev. 2026-09-25, section-2 review: STYLE-0 KEYWORD COLOUR (soft). In some files the DEFAULT font style is a
colour, so every character OUTSIDE a <STYLE> span is drawn as a highlighted keyword. The style table is in the
.lns header comment (`;    0: TDecorate(count=..., unk2=<colour>...`); unk2 = 4294967295 means "no colour", any
other value means the file's untagged text is coloured. For those files, an untagged EN run must not be longer
in words than the untagged JP run is in characters, measured per line and counted only where the JP run is
short (<= 8 characters, i.e. a keyword and not a whole sentence the JP itself left outside the spans); the
[TN: ...] tail is excluded. Words may be moved ACROSS a span boundary to achieve this (Q1562, Fable ruling).
rev. 2026-09-26, O-66 (RULE1): a STYLE pair split around a moved name (e.g. `<STYLE ID="1">Seeing </STYLE>Haruka
<STYLE ID="1">'s face...</STYLE>`) is SOFT, not hard: same set of plain style ids opened, ruby tags and all other
tags identical, opens/closes balanced, no id opened fewer times than JP (split_style_ok). Every other tag difference stays HARD.
"""
import os, re, sys, hashlib, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r'<[^>]*>|\{[^}]*\}')
# kana, kanji, and CJK symbols/punctuation EXCEPT U+3000 (full-width space) and 【 】 (U+3010/U+3011): soft, see KEEPABLE
JP = re.compile('[぀-゠ァ-ヺー-ヿ一-鿿、-』〒-〿]')  # ・ U+30FB excluded: kept bullet glyph (Fable ruling 2026-09-25)
# full-width forms U+FF01-FF5E EXCEPT （ U+FF08 and ） U+FF09 (soft, see KEEPABLE)
FULLWIDTH = re.compile('[！-＇＊-．０-［］-｝]')  # U+FF08/09 （）, U+FF0F ／, U+FF3C ＼ (shout brackets, Fable 2026-10-01) and U+FF5E ～ excluded
# allowed only where a CORE A row names the device; reported so they stay visible
KEEPABLE = re.compile('[　（）【】・＼／]')
HYPHEN_RULE = re.compile('-{3,}')
# the .lns header comment that carries the font-style table; style index 0 is the file's default style
STYLE0 = re.compile(r'^;\s+0: TDecorate\(count=\d+, unk2=(\d+)')
NO_COLOUR = 4294967295            # 0xFFFFFFFF in unk2 = "no colour set", i.e. ordinary message text
STYLE_OPEN = '<STYLE'
STYLE_CLOSE = '</STYLE'
JP_PUNCT = '「」『』、。！？…　・'
KEYWORD_MAX_JP = 8                # above this the JP itself left a whole sentence untagged: not a keyword


def style0_colour(lines):
    """The default style's colour from the .lns header, or None when the file declares no style table."""
    for line in lines[:16]:
        m = STYLE0.match(line)
        if m:
            return int(m.group(1))
    return None


def untagged(line):
    """The text of a line that sits OUTSIDE every <STYLE> span (commands and other tags removed)."""
    out, depth, pos = [], 0, 0
    for m in TAG.finditer(line):
        if depth == 0:
            out.append(line[pos:m.start()])
        tag = m.group(0)
        if tag.startswith(STYLE_OPEN):
            depth += 1
        elif tag.startswith(STYLE_CLOSE):
            depth = max(0, depth - 1)
        pos = m.end()
    if depth == 0:
        out.append(line[pos:])
    return ''.join(out)

def split_style_ok(tj, te):
    """O-66 (2026-09-26): a STYLE pair may be split around a moved name, so EN can open the same plain style id
    more often than JP. Allowed when: every non-STYLE tag is identical and in order; every RUBY-carrying STYLE tag
    is identical (multiset); the SET of plain STYLE ids opened is the same; EN opens and closes balance."""
    def parts(tags):
        other = [t for t in tags if not t.startswith(STYLE_OPEN) and not t.startswith(STYLE_CLOSE)]
        ruby = sorted(t for t in tags if t.startswith(STYLE_OPEN) and 'RUBY=' in t)
        plain = {t for t in tags if t.startswith(STYLE_OPEN) and 'RUBY=' not in t}
        return other, ruby, plain
    if parts(tj) != parts(te):
        return False
    # a split only ADDS opens of an id the JP already opens; EN never opens an id fewer times than JP
    if any(te.count(t) < tj.count(t) for t in parts(tj)[2]):
        return False
    depth = 0
    for t in te:
        if t.startswith(STYLE_OPEN):
            depth += 1
        elif t.startswith(STYLE_CLOSE):
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def main(lsbid):
    # SY_EN_DIR (absolute or ROOT-relative) checks another EN tree, e.g. lns-en-55 (2026-09-26).
    jp_dir = ROOT / 'lns'
    en_dir = Path(os.environ['SY_EN_DIR']) if os.environ.get('SY_EN_DIR') else ROOT / 'lns-en'
    if not en_dir.is_absolute():
        en_dir = ROOT / en_dir
    jp_files = sorted(p.name for p in jp_dir.glob(f'{lsbid}-*.lns'))
    en_files = sorted(p.name for p in en_dir.glob(f'{lsbid}-*.lns'))
    hard, soft = [], []
    if jp_files != en_files:
        hard.append(f'file set differs: only-JP {set(jp_files)-set(en_files)} only-EN {set(en_files)-set(jp_files)}')
    ref_jp, ref_en = jp_dir / f'{lsbid}.lsbref', en_dir / f'{lsbid}.lsbref'
    if not ref_en.exists():
        hard.append('lns-en/.lsbref missing')
    elif ref_jp.read_bytes() != ref_en.read_bytes():
        hard.append('.lsbref differs from lns/')
    names = load_glossary_names()
    text_lines = 0
    for name in jp_files:
        if name not in en_files:
            continue
        jl = (jp_dir / name).read_bytes().decode('utf-8').replace('\r', '').split('\n')
        el = (en_dir / name).read_bytes().decode('utf-8').replace('\r', '').split('\n')
        colour = style0_colour(jl)
        keyword_default = colour is not None and colour != NO_COLOUR
        if len(jl) != len(el):
            hard.append(f'{name}: line count JP {len(jl)} vs EN {len(el)}')
        for i, (j, e) in enumerate(zip(jl, el), 1):
            where = f'{name}:{i}'
            if j.startswith(';') or j.startswith('{') and TAG.sub('', j).strip() == '':
                if j != e:
                    hard.append(f'{where}: comment/command line changed')
                continue
            tj, te = TAG.findall(j), TAG.findall(e)
            if tj != te:
                if sorted(tj) == sorted(te):
                    soft.append(f'{where}: tag ORDER differs (allowed when English word order moves a tagged name)')
                elif split_style_ok(tj, te):
                    soft.append(f'{where}: STYLE pair split around a moved name (same style ids, O-66)')
                else:
                    hard.append(f'{where}: tag sequence differs JP {tj} EN {te}')
            j_text, e_text = TAG.sub('', j), TAG.sub('', e)
            if not j_text.strip():
                if e_text.strip():
                    hard.append(f'{where}: EN has text where JP has none')
                continue
            text_lines += 1
            if JP.search(e_text):
                hard.append(f'{where}: Japanese left in EN: {e_text[:60]}')
            if FULLWIDTH.search(e_text):
                hard.append(f'{where}: full-width Latin/punct in EN: {e_text[:60]}')
            if KEEPABLE.search(e_text):
                soft.append(f'{where}: U+3000 / full-width （） / 【】 in EN: keep only where a CORE A row names '
                            f'the device, else ASCII: {e_text[:60]}')
            if not e_text.strip():
                hard.append(f'{where}: EN empty for JP text')
            try:
                e_text.encode('cp932')
            except UnicodeEncodeError as ex:
                hard.append(f'{where}: not CP932-encodable: {ex.object[ex.start:ex.end]!r}')
            if (j_text.count("「") + j_text.count("」")) != e_text.count(chr(34)):
                soft.append(f'{where}: 「 count {j_text.count("「")} vs EN double quotes {e_text.count(chr(34))}')
            if '…' in e_text or '..' in e_text.replace('...', ''):
                soft.append(f'{where}: ellipsis form (want "...")')
            e_nohr = HYPHEN_RULE.sub('', e_text)  # a run of 3+ ASCII hyphens is a horizontal rule, not a dash
            if '--' in e_nohr or '—' in e_nohr:
                soft.append(f'{where}: dash form (want ― U+2015)')
            if '[TN:' in e_text and not e_text.rstrip().endswith(']'):
                soft.append(f'{where}: [TN:] not at line end')
            if keyword_default:
                ju, eu = untagged(j), untagged(e).split('[TN:')[0]
                jc = len([c for c in ju if c not in JP_PUNCT and not c.isspace()])
                ew = len([w for w in eu.split() if re.search('[A-Za-z0-9]', w)])
                if jc <= KEYWORD_MAX_JP and ew > max(1, jc):
                    soft.append(f'{where}: style-0 keyword colour (0x{colour:06X}): {ew} EN words sit OUTSIDE '
                                f'the STYLE spans where the JP has {jc} character(s); only the highlighted '
                                f'keyword belongs there, so move words across the boundary (Q1562): {eu[:60]}')
            jn, en_ = len(j_text.strip()), len(e_text.split('[TN:')[0].strip())
            if jn >= 6 and (en_ > 6.0 * jn or en_ < 1.0 * jn):
                soft.append(f'{where}: length ratio out of range: check for padding or a dropped clause '
                            f'(EN/JP {en_/jn:.1f}): {e_text[:50]}')
            for jp_name, en_name in names:
                if jp_name in j_text and en_name.split()[0] not in e_text and en_name.split()[-1] not in e_text:
                    soft.append(f'{where}: name {jp_name} present, EN "{en_name}" absent')
    print(f'{lsbid}: {text_lines} text lines checked, {len(hard)} hard, {len(soft)} soft')
    for h in hard: print('HARD', h)
    for s in soft: print('soft', s)
    return 1 if hard else 0

def load_glossary_names():
    out = []
    with open(ROOT / 'notes' / 'GLOSSARY.tsv', encoding='utf-8') as f:
        for row in csv.reader(f, delimiter='\t'):
            if len(row) >= 5 and row[3] == 'name' and row[4] == 'person' and ' ' in row[2]:
                out.append((row[0], row[2]))
    return out

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
