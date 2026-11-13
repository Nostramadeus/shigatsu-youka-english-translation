"""Calibration sets for FIT MODEL 2: surface constants, full source text, observed screen lines."""
R = 'F:/Projects/shigatsu-youka-en/'


def cell(table, key_col, key, col):
    rows = open(R + 'tsv-en/' + table, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
    h = [c.split(' ')[0] for c in rows[0].split('\t')]
    for r in rows[1:]:
        c = r.split('\t')
        if len(c) > h.index(key_col) and c[h.index(key_col)] == key:
            return c[h.index(col)]
    raise SystemExit('no row %s=%s in %s' % (key_col, key, table))


PRE = ' \u3000\u3000'
Z = '\u3000'
SETS = []

SETS.append(dict(name='1.png  scene box (標準), friend shot, scale 0.944', face='ＭＳ Ｐ明朝', h=30, shadow=1, border=1, W=580, text=(
    "Shiyo 800, April. Eiichiro's third-year memorial service was coming up soon. [TN: Buddhist memorials count "
    "the year of death as the first year.]\nHaving lost the man of the house, the Niimura family had moved away "
    "to who knew where."), tail=[
    "Shiyo 800, April. Eiichiro's", "third-year memorial service was", "coming up soon. [TN: Buddhist",
    "memorials count the year of death", "as the first year.]", "Having lost the man of the house,",
    "the Niimura family had moved", "away to who knew where."]))

SETS.append(dict(name='fitaudit/004.png  scene box, 1:1 capture (B page)', face='ＭＳ Ｐ明朝', h=30, shadow=1, border=1, W=580, text=(
    "B01 aaaa. B02 bbbb. B03 cccc. B04 dddd. B05 eeee. B06 ffff. B07 gggg. "
    "B08 hhhh. B09 iiii. B10 jjjj. B11 kkkk. B12 llll. B13 mmmm. B14 nnnn. B15 oooo."), tail=[
    "B01 aaaa. B02 bbbb. B03 cccc.", "B04 dddd. B05 eeee. B06 ffff.", "B07 gggg. B08 hhhh. B09 iiii. B10",
    "jjjj. B11 kkkk. B12 llll. B13", "mmmm. B14 nnnn. B15 oooo."]))

SETS.append(dict(name='fitaudit/008.png  scene box, 1:1 capture (W page, first 13 lines)', face='ＭＳ Ｐ明朝', h=30, shadow=1, border=1, W=580,
                 text=' '.join('W%03d' % n for n in range(1, 201)),
                 head=[' '.join('W%03d' % n for n in range(a, a + 5)) for a in range(1, 66, 5)]))

SETS.append(dict(name='fitaudit4/010.png  scene box, 1:1 capture (P/Q page: the wrap rule)', face='ＭＳ Ｐ明朝', h=30, shadow=1, border=1, W=580, text='\n'.join([
    "P1 aaaa bbbb cccc dddd eeee fff." + Z + "Ggg P1", "P2 aaaa bbbb cccc dddd eeee ffff." + Z + "Ggg P2",
    "P3 aaaa bbbb cccc dddd eeee fffff." + Z + "Ggg P3", "Q1 aaaa bbbb cccc dddd eeee fff. Ggg Q1",
    "Q2 aaaa bbbb cccc dddd eeee ffff. Ggg Q2", "Q3 aaaa bbbb cccc dddd eeee fffff. Ggg Q3"]), tail=[
    "P1 aaaa bbbb cccc dddd eeee fff." + Z, "Ggg P1", "P2 aaaa bbbb cccc dddd eeee ffff.", Z + "Ggg P2",
    "P3 aaaa bbbb cccc dddd eeee fffff.", Z + "Ggg P3", "Q1 aaaa bbbb cccc dddd eeee fff.", "Ggg Q1",
    "Q2 aaaa bbbb cccc dddd eeee ffff.", "Ggg Q2", "Q3 aaaa bbbb cccc dddd eeee", "fffff. Ggg Q3"]))

SETS.append(dict(name='2.png  node commentary (部分コメント), friend shot', face='ＭＳ 明朝', h=25, shadow=0, border=0, W=750,
                 text=cell('リファレンスターゲット.tsv', 'ID', '92', '3概要'), head=[
    "The takoyaki dish: that is probably a coffin modeled", "on the Protestant denomination. No, wait, since it's",
    "billed as Russian-roulette takoyaki, it must come", "from Russian Orthodoxy after all? In that case it",
    "belongs to neither Catholicism nor Protestantism,", "and the coffin design should be a little different",
    "too. And eating what was inside it means, so to", "speak, eating a corpse―an embodiment of",
    "cannibalism, of eating human flesh. So, to sum up:", "in Russian Orthodoxy burial in the ground is still",
    "the norm, so a body with its flesh stays in the", "coffin for a while. Digging it up and eating it is",
    "an unmistakable sin, but in famines of the past"]))

t7 = cell('人物/新村美冬.tsv', '表示順', '23', 'テキスト')
t8 = cell('人物/新村美冬.tsv', '表示順', '24', 'テキスト')
SETS.append(dict(name='3.png  people body (人物解説テキスト), friend shot', face='ＭＳ Ｐ明朝', h=24, shadow=1, border=0, W=690,
                 text=PRE + '7．' + t7 + "\n(Wabigoto Arc [Apology] The Shinigami's Rule)\n\n" + PRE + '8．' + t8 +
                 "\n(リファレンス No.104 Mother-in-Law's Nagging)", tail=[
    "forced to live in poverty. Furthermore, she drew up a", "plan to kill the classmates who bullied Haruka Niimura,",
    "and asked the Kogori couple to help her manufacture an", "alibi.", "(Wabigoto Arc [Apology] The Shinigami's Rule)",
    "", PRE + "8．After attending the thirteenth-year memorial",
    "service in the Arata settlement, she visits the grave of", "the child she had with Eiichiro Niimura, who was",
    "stillborn. There her mother-in-law tells her, \"If you ever",
    "get in trouble, never mind the rule; just take Haruka and", "run here.\" Since the two killings in Megasawa City had",
    "already been carried out by that hour, she is seized by a", "feeling that could be taken for regret.",
    "(リファレンス No.104 Mother-in-Law's Nagging)"]))

u10 = cell('人物/古郡良治.tsv', '表示順', '15', 'テキスト')
u11 = cell('人物/古郡良治.tsv', '表示順', '16', 'テキスト')
u12 = cell('人物/古郡良治.tsv', '表示順', '17', 'テキスト')
SETS.append(dict(name='4.png  people body (人物解説テキスト), friend shot', face='ＭＳ Ｐ明朝', h=24, shadow=1, border=0, W=690,
                 text=PRE + '10．' + u10 + "\n(Wabigoto Arc [Apology] Apology)\n\n" + PRE + '11．' + u11 +
                 "\n(Wabigoto Arc [Apology] 見送り)\n\n" + PRE + '12．' + u12 + "\n(Wabigoto Arc [Apology] 凍える親子 新ルート)",
                 tail=["to Eiichiro Niimura.", "(Wabigoto Arc [Apology] Apology)", "",
                       PRE + "11．In Shiyo 800, though he is specially permitted to",
                       "attend Eiichiro Niimura's thirteenth-year memorial",
                       "service, he sends Natsumi Kogori in his place because of",
                       "her warning. However, not knowing what danger awaits,",
                       "he seems uneasy about sending his daughter to the Arata", "settlement.",
                       "(Wabigoto Arc [Apology] 見送り)", "",
                       PRE + "12．Deciding that he cannot, after all, take his",
                       "daughter where a murder may happen, he does not take", "Natsumi Kogori along.",
                       "(Wabigoto Arc [Apology] 凍える親子 新ルート)"]))


