"""Per-scene block recipes for the English character totals (文字数1 / 文字数2 / コア文字数).

Source of truth for tools/charcount_write.py (work/charcount/recipes.py is a shim that re-exports this).
Proven 2026-09-26 (34 rows, notes/CHARCOUNT-FIX.md) and 2026-10-29 (Lane A of the counter repair: 163 scenario
rows + 18 hidden rows; plan work/feedback-repair-20261029/COUNTERS-PLAN.md).

R[lsb id] = (連番, [blocks summed into 文字数1], [blocks for 文字数2] or None,
             [blocks of the 『分岐直前から』 resume route] or None)
    コア文字数 = 文字数1 - sum(resume route).
H[hidden ID] = (連番, lsb id, [blocks summed into 文字数1], None, None)   # tsv-en/裏ルート.tsv
Block names are the lns/<id>-<name>.lns names (tools/extract_lsb.py naming), listed in route order. New rows
list zero-length blocks on the route too (0 in JP; they would count in EN if they ever carried text).

Proof comment per row:
  exact-unique      the only subset of the script's blocks whose JP sum equals the stored JP value, and the
                    control-flow route from the entry index plays exactly those blocks (TextIns idx listed)
  route             no exact subset (stale author value) or several; the route is proven by control flow
  stale residual N  N = stored JP - reproduced JP; the writer's gate accepts exactly this N (STALE_OK)
True-Jusatsu rows (245-250, 305): 文字数1 = sum of the 真呪殺編選択 section routes 0..N (opening section -1
excluded) = sum of that row's section fields in ノベルシステム/真呪殺編文字数.txt. The per-section routes are TJ /
TJ_STALE at the end of this file; tools/build_tj_counts.py builds the English 真呪殺編文字数.txt from them.

Deliberately not in R:
  FIRST_ARC_OWNED  8 first-arc rows owned by tools/repair_first_arc_totals.py (the writer skips them).
  UNRESOLVED       rows that cannot be proven; they stay Japanese.
"""

FIRST_ARC_OWNED = ('138', '145', '147', '205', '162', '170', '206', '202')

UNRESOLVED = {
    '314': 'stored 2000/5000 are round placeholders; 000021E2 has 17 <VAR> blocks (UNRESOLVED-VAR); dispatch '
           '000015E3 idx 5 -> 1533 -> 1605 never assigns シナリオテキスト数',
}

# (連番, column): (residual = stored JP - reproduced JP, reason). The gate accepts exactly this residual.
STALE_OK = {
    ('119', '文字数1'): (-45, 'author typed 文字数1 before a 45-char edit to 000004A2; コア文字数 proves 3742'),
    ('169', '文字数1'): (-312, 'route plays 00000493, 0000048E, then red-box line48; author left line48 out'),
    ('15', '文字数1'): (+6, 'single unconditional route through all 5 blocks; author value 6 higher'),
    ('30', '文字数1'): (+2, 'single unconditional route through all 3 blocks; author value 2 higher'),
    ('95', '文字数1'): (+2, 'single unconditional route through all 3 blocks; author value 2 higher'),
    ('125', '文字数1'): (-14, 'single route idx 17 -> 29 -> 11 plays all 3 blocks; author value 14 lower'),
    ('227', '文字数1'): (-1009, 'route plays 00000BCD then red-box line15; author counted the first block only'),
    ('245', '文字数1'): (+4, 'section routes; txt/author sections 1 and 3 are 2 higher each'),
    ('247', '文字数1'): (+4, 'section routes; txt/author section 11 is 4 higher'),
    ('250', '文字数1'): (+2, 'section routes; txt/author section 3 is 2 higher'),
    ('266', '文字数1'): (+2, 'single block; author value 2 higher'),
    ('303', '文字数1'): (-25, 'single route 0000153F -> staff roll -> line27; author value 25 lower'),
    ('305', '文字数1'): (+2, 'section routes; txt/author section 12 is 2 higher'),
}

R = {
    # 1 exact-unique; route TextIns idx 11 (single path)
    '0000107B': ('1', ['00001087'], None, None),
    # 3 exact-unique; route TextIns idx 11 (single path)
    '00001092': ('3', ['0000109E'], None, None),
    # 4 exact-unique; route TextIns idx 11 (single path)
    '000010AA': ('4', ['000010B6'], None, None),
    # 7 exact-unique; route TextIns idx 11 (single path)
    '000010C3': ('7', ['000010CF'], None, None),
    # 13 exact-unique; route TextIns idx 8 (single path)
    '000007BC': ('13', ['000007C9'], None, None),
    # 14 exact-unique; route TextIns idx 11 (single path)
    '00000818': ('14', ['00000825'], None, None),
    # 15 route: single unconditional path TextIns idx 11,15,19,23,27; stale residual +6
    '0000082F': ('15', ['0000083F', 'line15', 'line19', 'line23', 'line27'], None, None),
    # 25 exact-unique; route TextIns idx 11 (single path)
    '00000846': ('25', ['00000852'], None, None),
    # 27 exact-unique; route TextIns idx 11 (single path)
    '0000085D': ('27', ['00001AED'], None, None),
    # 28 exact-unique; route TextIns idx 11 (single path)
    '00000874': ('28', ['00000880'], None, None),
    # 29 exact-unique all 3 columns; route 途中から=0/分岐ルートへ=0 TextIns idx 35,28,16; 文字数2 分岐ルートへ!=0 idx 35,28,22; resume
    #   途中から=1 idx 28,16
    '0000088B': ('29',
        ['00000C9B', '00000C9A', '00000891'],
        ['00000C9B', '00000C9A', '00000C98'],
        ['00000C9A', '00000891']),
    # 30 route: single unconditional path TextIns idx 8,12,16; stale residual +2
    '000008A2': ('30', ['000008AC', 'line12', 'line16'], None, None),
    # 31 exact-unique all 3 columns; route 途中から=0/分岐ルートへ=0 TextIns idx 29,8,36,40,44; 文字数2 分岐ルートへ!=0 idx
    #   29,22,36,40,44; resume 途中から=1 idx 50,8,36,40,44; 文字数2 = path with 分岐案内 == 1 (one-time guide event idx 135..
    #   skipped, author choice)
    '000008B9': ('31',
        ['00000BD0', '000008C4', '00000BD1', 'line40', 'line44'],
        ['00000BD0', '00000BCF', '00000BD1', 'line40', 'line44'],
        ['00000BD2', '000008C4', '00000BD1', 'line40', 'line44']),
    # 32 exact-unique all 3 columns; route 途中から=0/分岐ルートへ=0 TextIns idx 46,33; 文字数2 分岐ルートへ!=0 idx 46,19,23,27; resume
    #   途中から=1 idx 39,33
    '000008D0': ('32',
        ['00001AE4', '00001AD4'],
        ['00001AE4', '00001AD3', 'line23', 'line27'],
        ['00001AD5', '00001AD4']),
    # 33 exact-unique; route TextIns idx 8 (single path)
    '000008E8': ('33', ['000008F2'], None, None),
    # 34 exact-unique; route TextIns idx 8 (single path)
    '00001AC1': ('34', ['00001AC3'], None, None),
    # 70 exact-unique; route TextIns idx 11 (single path)
    '00000CE3': ('70', ['00000CED'], None, None),
    # 78 exact-unique; route TextIns idx 11 (single path)
    '00000900': ('78', ['0000090A'], None, None),
    # 82 exact-unique all 3 columns; route 途中から=0/分岐ルートへ=0 TextIns idx 31,11; 文字数2 分岐ルートへ!=0 idx 31,25; resume 途中から=1
    #   idx 38,11
    '00000916': ('82', ['00000BD4', '00000920'], ['00000BD4', '00000BD3'], ['00000BD5', '00000920']),
    # 83 exact-unique; route TextIns idx 11 (single path)
    '0000092D': ('83', ['00000939'], None, None),
    # 84 exact-unique; route TextIns idx 11 (single path)
    '0000066B': ('84', ['00000680'], None, None),
    # 85 exact; route idx 4 -> 9 -> line15 (CHARCOUNT-FIX §1)
    '000001DB': ('85', ['line15'], None, None),
    # 87 exact-unique; route TextIns idx 11 (single path)
    '00000682': ('87', ['0000068F'], None, None),
    # 88 exact-unique; route TextIns idx 11 (single path)
    '00000CFA': ('88', ['00000D04'], None, None),
    # 89 exact-unique; route TextIns idx 8 (single path)
    '00000944': ('89', ['0000094A'], None, None),
    # 90 exact-unique; route TextIns idx 11 (single path)
    '00000972': ('90', ['0000097D'], None, None),
    # 91 exact-unique; route TextIns idx 11 (single path)
    '00000D11': ('91', ['00000D1D'], None, None),
    # 92 exact-unique; route TextIns idx 11 (single path)
    '00000989': ('92', ['00000992'], None, None),
    # 94 exact-unique; route TextIns idx 11 (single path)
    '000009A0': ('94', ['000009AA'], None, None),
    # 95 route: single unconditional path TextIns idx 11,15,19; stale residual +2
    '000009B7': ('95', ['000009C3', 'line15', 'line19'], None, None),
    # 96 exact-unique; route TextIns idx 11 (single path)
    '000009CF': ('96', ['000009DA'], None, None),
    # 97 exact-unique; route TextIns idx 11,15,19 (single path)
    '000009E6': ('97', ['000009EF', 'line15', 'line19'], None, None),
    # 98 exact-unique; route TextIns idx 11,15,19,23,27,31,35,39,43 (single path)
    '000009FE': ('98',
        ['00000A07', 'line15', 'line19', 'line23', 'line27', 'line31', 'line35', 'line39', 'line43'],
        None,
        None),
    # 99 exact-unique; route TextIns idx 11 (single path)
    '00000A18': ('99', ['00000A21'], None, None),
    # 100 exact-unique all 3 columns; route 途中から=0/分岐ルートへ=0 TextIns idx 11,26; 文字数2 分岐ルートへ!=0 idx 11,32; resume 途中から=1
    #   idx 38,26
    '00000A48': ('100', ['00000A51', '00000A60'], ['00000A51', '00000A61'], ['00000AF6', '00000A60']),
    # 101 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000001DD': ('101', ['000016F6'], None, None),
    # 102 exact-unique; route TextIns idx 8 (single path)
    '00000697': ('102', ['0000069E'], None, None),
    # 103 exact-unique; route TextIns idx 11 (single path)
    '00000DD1': ('103', ['00000DDD'], None, None),
    # 104 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000001DF': ('104', ['000003E0'], None, None),
    # 105 exact-unique; route TextIns idx 11 (single path)
    '00000DE9': ('105', ['00000DF5'], None, None),
    # 107 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000E01': ('107', ['00000E0D', 'line15', 'line19'], None, None),
    # 108 exact-unique; route TextIns idx 11 (single path)
    '00000E49': ('108', ['00000E55'], None, None),
    # 111 exact-unique; route TextIns idx 11 (single path)
    '00000E19': ('111', ['00000E25'], None, None),
    # 113 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000001E1': ('113', ['00000593', '00000591'], ['00000593', '00000590'], ['00000594', '00000591']),
    # 114 exact-unique; route TextIns idx 8 (single path)
    '000006B2': ('114', ['000006C1'], None, None),
    # 116 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000001E3': ('116', ['000002A0', 'line12', 'line16', 'line20', 'line24'], None, None),
    # 117 exact-unique; route TextIns idx 8 (single path)
    '000006C9': ('117', ['000006D8'], None, None),
    # 118 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000D29': ('118', ['00000D35', 'line15', 'line19'], None, None),
    # 119 exact on 文字数2/コア; 文字数1 stale residual -45 (コア proves 3742, CHARCOUNT-FIX §2)
    '000001E5': ('119',
        ['000003E6', '000004A5', '000004A2'],
        ['000003E6', '000004A5', '000004A3'],
        ['000004A5', '000004A2']),
    # 120 exact-unique; route TextIns idx 8,12,16 (single path)
    '000006E0': ('120', ['000006E9', 'line12', 'line16'], None, None),
    # 122 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000595': ('122', ['000005AB'], None, None),
    # 124 exact-unique; route TextIns idx 11 (single path)
    '00000E31': ('124', ['00000E3D'], None, None),
    # 125 route: single unconditional path TextIns idx 17,29,11; stale residual -14
    '000006F9': ('125', ['00000708', '00000713', '00000700'], None, None),
    # 127 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000005AC': ('127', ['000005B9'], None, None),
    # 128 exact-unique; route TextIns idx 8 (single path)
    '00000716': ('128', ['00000725'], None, None),
    # 129 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000001E7': ('129', ['000003EC', 'line15'], None, None),
    # 131 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000004A7': ('131', ['000004AF'], None, None),
    # 132 exact-unique; route TextIns idx 8 (single path)
    '00000731': ('132', ['0000073B'], None, None),
    # 134 exact-unique; route TextIns idx 8 (single path)
    '00000749': ('134', ['00000756'], None, None),
    # 136 exact-unique; route TextIns idx 8 (single path)
    '00000761': ('136', ['0000076D'], None, None),
    # 137 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000004BB': ('137', ['000004C7', 'line12', 'line16'], None, None),
    # 140 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000004CF': ('140', ['000004F7', '0000054C'], ['000004F7', '0000054D'], ['0000054C']),
    # 141 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000004E3': ('141', ['000004F8', 'line15', 'line19', 'line23', 'line27'], None, None),
    # 143 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000538': ('143', ['00000540'], None, None),
    # 148 exact-unique; route TextIns idx 8 (single path)
    '00000779': ('148', ['00000785'], None, None),
    # 149 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000550': ('149', ['00000579'], None, None),
    # 151 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000564': ('151', ['0000057A'], None, None),
    # 153 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000004F9': ('153', ['00000502'], None, None),
    # 154 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000020B': ('154',
        ['000002D4', '0000031C', '0000031E'],
        ['000002D4', '000002F4', '00000407'],
        ['0000031C', '0000031E']),
    # 156 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000050E': ('156', ['00000515'], None, None),
    # 157 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000020D': ('157', ['000002E3'], None, None),
    # 158 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000002F6': ('158', ['00000300'], None, None),
    # 160 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000002F8': ('160',
        ['000003F0', '0000049E', '000004A0'],
        ['000003F0', '0000049D', '000004A0'],
        ['0000049E', '000004A0']),
    # 163 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000002FA': ('163', ['00000336', 'line15', 'line19', 'line23', 'line27'], None, None),
    # 164 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000473': ('164', ['0000047C'], None, None),
    # 168 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000033D': ('168', ['000003F6'], None, None),
    # 169 route: single unconditional path TextIns idx 34,11,44,48,52 (00000493 -> 0000048E -> red box line48);
    #   stale residual -312 (orchestrator 2026-10-29: red-box text counts, D2e; was ['0000048E', '00000493'])
    '00000488': ('169', ['00000493', '0000048E', '00001875', 'line48', 'line52'], None, None),
    # 171 exact; route idx 4 -> 0000242C block, other two blocks dead (CHARCOUNT-FIX §1)
    '0000034C': ('171', ['0000242C'], None, None),
    # 172 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000522': ('172', ['00000530'], None, None),
    # 173 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000366': ('173', ['00000376'], None, None),
    # 177 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000037D': ('177', ['000003FC'], None, None),
    # 183 exact-unique; route TextIns idx 11 (single path)
    '00000E95': ('183', ['00000EA1'], None, None),
    # 184 exact-unique; route TextIns idx 11 (single path)
    '00000F40': ('184', ['00000F4C'], None, None),
    # 185 exact-unique; route TextIns idx 11 (single path)
    '00000F6F': ('185', ['00000F7B'], None, None),
    # 187 exact-unique; route TextIns idx 11 (single path)
    '00000F57': ('187', ['00000F63'], None, None),
    # 188 exact-unique; route TextIns idx 11 (single path)
    '00000EC7': ('188', ['00000ED3'], None, None),
    # 189 exact-unique; route TextIns idx 11 (single path)
    '00000F87': ('189', ['00000F93'], None, None),
    # 191 exact-unique; route TextIns idx 11 (single path)
    '00000F9F': ('191', ['00000FAB'], None, None),
    # 193 exact-unique; route TextIns idx 11 (single path)
    '00000FB7': ('193', ['00000FC3'], None, None),
    # 194 exact-unique; route TextIns idx 11,15,19,23,27,31,35,39,43,47,101 (single path)
    '00000FCF': ('194',
        ['00000FDB', 'line15', 'line19', 'line23', 'line27', 'line31', 'line35', 'line39', 'line43', 'line47',
         '00001C8A'],
        None,
        None),
    # 195 exact; route 分岐ルートへ==0 -> line16, other branch 00000799 (CHARCOUNT-FIX §1)
    '00000024': ('195', ['line16'], ['00000799'], None),
    # 203 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '00000460': ('203', ['00000466'], None, None),
    # 204 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '0000057B': ('204', ['000005AA'], None, None),
    # 207 exact-unique; route TextIns idx 8 (single path)
    '000007A5': ('207', ['000007B0'], None, None),
    # 208 exact-unique; route TextIns idx 11 (single path)
    '000007D3': ('208', ['000007E3'], None, None),
    # 209 exact-unique; route TextIns idx 11 (single path)
    '000007EA': ('209', ['000007FA'], None, None),
    # 210 exact-unique; route TextIns idx 8 (single path)
    '00000801': ('210', ['00000807'], None, None),
    # 211 exact-unique; route TextIns idx 11,15,19,23,27,31,35 (single path)
    '0000095B': ('211', ['00000967', 'line15', 'line19', 'line23', 'line27', 'line31', 'line35'], None, None),
    # 212 exact-unique; route TextIns idx 11 (single path)
    '00000A30': ('212', ['00000A39'], None, None),
    # 213 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000A62': ('213', ['00000A6B', 'line15', 'line19'], None, None),
    # 214 exact-unique; route TextIns idx 11 (single path)
    '00000A7C': ('214', ['00000A85'], None, None),
    # 215 exact-unique; route TextIns idx 11 (single path)
    '00000A94': ('215', ['00000A9D'], None, None),
    # 216 exact-unique; route TextIns idx 11 (single path)
    '00000AAC': ('216', ['00000ADC'], None, None),
    # 217 exact-unique; route TextIns idx 11,15,19,23 (single path)
    '00000AC4': ('217', ['00000ADD', 'line15', 'line19', 'line23'], None, None),
    # 218 exact-unique; route TextIns idx 11 (single path)
    '00000ADE': ('218', ['00000AF4'], None, None),
    # 219 exact-unique; route TextIns idx 11 (single path)
    '00000AF7': ('219', ['00000B0D'], None, None),
    # 220 exact-unique; route TextIns idx 11 (single path)
    '00000B0F': ('220', ['00000B25'], None, None),
    # 221 exact-unique; route TextIns idx 11 (single path)
    '00000B27': ('221', ['00000B3D'], None, None),
    # 222 exact-unique; route TextIns idx 11 (single path)
    '00000B3F': ('222', ['00000B55'], None, None),
    # 223 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000B57': ('223', ['00000B6D', 'line15', 'line19'], None, None),
    # 224 exact-unique; route TextIns idx 11 (single path)
    '00000B6F': ('224', ['00000B85'], None, None),
    # 225 exact-unique; route TextIns idx 11,15,19,23,27 (single path)
    '00000B87': ('225', ['00000B9D', 'line15', 'line19', 'line23', 'line27'], None, None),
    # 226 exact-unique; route TextIns idx 11 (single path)
    '00000B9F': ('226', ['00000BB5'], None, None),
    # 227 route: single unconditional path TextIns idx 11,15; stale residual -1009 (author left out red-box block
    #   line15, plan D2e: text in the counted box counts)
    '00000BB7': ('227', ['00000BCD', 'line15'], None, None),
    # 228 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000BD6': ('228', ['00000BE2', 'line15', 'line19'], None, None),
    # 229 exact-unique; route TextIns idx 11 (single path)
    '00000BED': ('229', ['00000BF9'], None, None),
    # 230 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000C08': ('230', ['00000C14', 'line15', 'line19'], None, None),
    # 231 exact-unique; route TextIns idx 11 (single path)
    '00000C21': ('231', ['00000C2D'], None, None),
    # 232 exact-unique; route TextIns idx 11 (single path)
    '00000C38': ('232', ['00000C44'], None, None),
    # 233 exact-unique; route TextIns idx 11 (single path)
    '00000C50': ('233', ['00000C5C'], None, None),
    # 234 exact-unique; route TextIns idx 11 (single path)
    '00000C68': ('234', ['00000C74'], None, None),
    # 235 exact-unique; route TextIns idx 11,15,19 (single path)
    '00000C81': ('235', ['00000C8D', 'line15', 'line19'], None, None),
    # 236 exact-unique; route TextIns idx 11 (single path)
    '00000CB3': ('236', ['00000CBD'], None, None),
    # 237 exact-unique; route TextIns idx 11,15,19,39,43,47 (single path)
    '00000CCA': ('237', ['00000CD4', 'line15', 'line19', '00000CE2', 'line43', 'line47'], None, None),
    # 238 exact-unique; route TextIns idx 11 (single path)
    '00000D41': ('238', ['00000D4D'], None, None),
    # 239 exact-unique; route TextIns idx 11 (single path)
    '00000D59': ('239', ['00000D65'], None, None),
    # 240 exact-unique; route TextIns idx 11 (single path)
    '00000D71': ('240', ['00000D7D'], None, None),
    # 241 exact-unique; route TextIns idx 11 (single path)
    '00000D89': ('241', ['00000D95'], None, None),
    # 242 exact-unique; route TextIns idx 11 (single path)
    '00000DA1': ('242', ['00000DAD'], None, None),
    # 243 exact-unique; route TextIns idx 11 (single path)
    '00000DB9': ('243', ['00000DC5'], None, None),
    # 244 exact-unique; route TextIns idx 11,55,49 (single path)
    '00000E61': ('244', ['00000E6D', '00001B7E', '00000E7A'], None, None),
    # 245 route: 真呪殺編選択 sections 0..8 (one route each, convergence idx 270) = 真呪殺編文字数.txt section fields; stale
    #   residual +4 (section 1 +2, 3 +2)
    '00000E7B': ('245',
        ['00000E87', '00000FEE', '00000FEF', '00000FF0', 'line44', 'line48', '00000FF1', '00000FF4', 'line64',
         'line68', 'line72', 'line76', '00001D01', '00000FF6', 'line92', 'line96', 'line100', 'line104',
         '00000FF5', '00001D0D'],
        None,
        None),
    # 246 exact-unique; route 真呪殺編選択 sections 0..8 (one route each, convergence idx 115) = 真呪殺編文字数.txt section fields
    '00000EAF': ('246',
        ['00001D9D', '00001D9A', '00001D93', '00001D8D', '00001DD5', '00001D8A', '00001D87', '00001DD6', '00001D82'],
        None,
        None),
    # 247 route: 真呪殺編選択 sections 0..12 (one route each, convergence idx 155) = 真呪殺編文字数.txt section fields; stale
    #   residual +4 (section 11 +4)
    '00000EDF': ('247',
        ['00001DB2', '00001DB3', '00001DDA', '00001DB4', '00001DDC', '00001DB5', '00001DB6', '00001DDF',
         '00001DAF', '00001DB1', '00001DB0', '00001DAE', 'line37', 'line41', '00001DBA'],
        None,
        None),
    # 248 exact-unique; route 真呪殺編選択 sections 0..10 (one route each, convergence idx 70) = 真呪殺編文字数.txt section fields
    '00000EF6': ('248',
        ['00001DFC', '00001DF9', '00001DF7', '00001DEF', '00001DEE', '00001DEC', 'line46', 'line50', '00001DEB',
         '00001DE9', '00001DE6', '00001DE5', '00001DE3'],
        None,
        None),
    # 249 exact-unique; route 真呪殺編選択 sections 0..12 (one route each, convergence idx 88) = 真呪殺編文字数.txt section fields
    '00000F0D': ('249',
        ['00000F19', '0000100C', '0000100D', '0000100E', '00001010', '0000101C', '0000101D', '00001028',
         '000021E0', '00001029', '0000102A', '0000102B', '0000102C', '000021E1'],
        None,
        None),
    # 250 route: 真呪殺編選択 sections 0..14 (one route each, convergence idx 55) = 真呪殺編文字数.txt section fields; stale
    #   residual +2 (section 3 +2)
    '00000F24': ('250',
        ['00001E84', '00001E83', '00001E8E', '00001E8D', '00001E8C', '00001E8B', '00001E8A', '00001E89',
         '00001E82', '00001E88', '00001E87', '00001E86', '00001E8F', '00001E99', '00001EA2'],
        None,
        None),
    # 254 exact-unique; route TextIns idx 11 (single path)
    '000010DD': ('254', ['000010E9'], None, None),
    # 255 exact-unique; route TextIns idx 11 (single path)
    '0000104E': ('255', ['0000105A'], None, None),
    # 256 exact-unique; route TextIns idx 8 (single path)
    '000010F5': ('256', ['00001101'], None, None),
    # 257 exact-unique; route TextIns idx 8,12,16,20,24 (single path)
    '0000110D': ('257', ['00001119', 'line12', 'line16', 'line20', 'line24'], None, None),
    # 258 exact-unique; route TextIns idx 8 (single path)
    '00001124': ('258', ['00001130'], None, None),
    # 259 exact-unique; route TextIns idx 8 (single path)
    '0000113D': ('259', ['00001149'], None, None),
    # 260 exact-unique; route TextIns idx 8 (single path)
    '00001154': ('260', ['00001160'], None, None),
    # 261 exact-unique; route TextIns idx 8 (single path)
    '0000116C': ('261', ['00001178'], None, None),
    # 262 exact-unique; route TextIns idx 8,12,16,20,24 (single path)
    '00001184': ('262', ['00001190', 'line12', 'line16', 'line20', 'line24'], None, None),
    # 263 exact-unique; route TextIns idx 8 (single path)
    '0000119C': ('263', ['000011A8'], None, None),
    # 264 exact-unique; route TextIns idx 8 (single path)
    '000011B4': ('264', ['000011C0'], None, None),
    # 265 exact-unique; route TextIns idx 8 (single path)
    '000011CC': ('265', ['000011D8'], None, None),
    # 266 route: single unconditional path TextIns idx 8; stale residual +2
    '000011E3': ('266', ['000011EF'], None, None),
    # 267 exact-unique; route TextIns idx 8 (single path)
    '000011FA': ('267', ['00001206'], None, None),
    # 268 exact-unique; route TextIns idx 8 (single path)
    '00001214': ('268', ['00001220'], None, None),
    # 269 exact-unique; route TextIns idx 8 (single path)
    '00001295': ('269', ['000012A1'], None, None),
    # 270 exact-unique; route TextIns idx 11 (single path)
    '0000122E': ('270', ['0000123A'], None, None),
    # 271 exact-unique; route TextIns idx 8,12,16,20 (single path)
    '000012AD': ('271', ['000012B9', 'line12', 'line16', 'line20'], None, None),
    # 272 exact-unique; route TextIns idx 8 (single path)
    '0000125E': ('272', ['0000126A'], None, None),
    # 273 exact-unique; route TextIns idx 8 (single path)
    '00001247': ('273', ['00001253'], None, None),
    # 275 exact-unique; route TextIns idx 8 (single path)
    '0000127A': ('275', ['00001286'], None, None),
    # 276 exact-unique; route TextIns idx 8 (single path)
    '000014D7': ('276', ['000014E3'], None, None),
    # 277 exact-unique; route TextIns idx 8 (single path)
    '000012C5': ('277', ['000012D1'], None, None),
    # 278 exact-unique; route TextIns idx 8 (single path)
    '000012DE': ('278', ['000012EA'], None, None),
    # 279 exact-unique; route TextIns idx 8 (single path)
    '000012F5': ('279', ['00001301'], None, None),
    # 280 exact-unique; route TextIns idx 8 (single path)
    '0000130D': ('280', ['00001319'], None, None),
    # 281 exact-unique; route TextIns idx 8 (single path)
    '00001325': ('281', ['00001331'], None, None),
    # 282 exact-unique; route TextIns idx 8 (single path)
    '0000133D': ('282', ['00001349'], None, None),
    # 283 exact-unique; route TextIns idx 8 (single path)
    '00001355': ('283', ['00001361'], None, None),
    # 284 exact-unique; route TextIns idx 8 (single path)
    '0000136D': ('284', ['00001379'], None, None),
    # 285 exact-unique; route TextIns idx 8 (single path)
    '00001385': ('285', ['00001391'], None, None),
    # 286 exact-unique; route TextIns idx 8 (single path)
    '000013B5': ('286', ['000013C1'], None, None),
    # 287 exact-unique; route TextIns idx 8 (single path)
    '0000139D': ('287', ['000013A9'], None, None),
    # 288 exact-unique; route TextIns idx 8 (single path)
    '000013CD': ('288', ['000013D9'], None, None),
    # 289 exact-unique; route TextIns idx 11 (single path)
    '00001E41': ('289', ['00001E44'], None, None),
    # 290 exact-unique; route TextIns idx 8 (single path)
    '000013E6': ('290', ['000013F2'], None, None),
    # 291 exact-unique; route TextIns idx 8 (single path)
    '000013FD': ('291', ['00001409'], None, None),
    # 292 exact-unique; route TextIns idx 8 (single path)
    '00001414': ('292', ['00001420'], None, None),
    # 293 exact-unique; route TextIns idx 8 (single path)
    '0000142B': ('293', ['00001437'], None, None),
    # 294 exact-unique; route TextIns idx 11 (single path)
    '00001442': ('294', ['0000144E'], None, None),
    # 295 exact-unique; route TextIns idx 8 (single path)
    '00001459': ('295', ['00001465'], None, None),
    # 296 exact-unique; route TextIns idx 8 (single path)
    '00001477': ('296', ['00001483'], None, None),
    # 297 exact-unique; route TextIns idx 8 (single path)
    '0000148E': ('297', ['0000149A'], None, None),
    # 298 exact-unique; route TextIns idx 8 (single path)
    '000014A5': ('298', ['000014B1'], None, None),
    # 299 exact-unique; route TextIns idx 8 (single path)
    '000014BC': ('299', ['000014C8'], None, None),
    # 300 exact-unique; route TextIns idx 8,12,16,20,24 (single path)
    '000014EE': ('300', ['000014FA', 'line12', 'line16', 'line20', 'line24'], None, None),
    # 301 exact-unique; route TextIns idx 8 (single path)
    '00001505': ('301', ['00001511'], None, None),
    # 302 exact-unique; route TextIns idx 8 (single path)
    '0000151C': ('302', ['00001528'], None, None),
    # 303 route: single unconditional path TextIns idx 8,23,27; stale residual -25
    '00001533': ('303', ['0000153F', '00001F07', 'line27'], None, None),
    # 304 exact-unique; route TextIns idx 8 (single path)
    '0000154E': ('304', ['0000155A'], None, None),
    # 305 route: 真呪殺編選択 sections 0..13 (one route each, convergence idx 100) = 真呪殺編文字数.txt section fields; stale
    #   residual +2 (section 12 +2)
    '0000156A': ('305',
        ['00001E6C', '00001E68', '00001E67', '00001E64', '00001E63', '00001E62', '00001E61', '00001E60',
         '00001E5F', '00001E5E', '00001E5C', '00001E5B', '00001E5D', 'line24', 'line28', '00001E78', 'line197',
         'line201'],
        None,
        None),
    # 306 exact (CHARCOUNT-FIX 2026-09-26 table, all 3 columns)
    '000016AE': ('306', ['000016B9'], None, None),
    # 307 exact-unique; route TextIns idx 11 (single path)
    '0000191C': ('307', ['00001920'], None, None),
    # 308 exact-unique; route TextIns idx 11 (single path)
    '00001B70': ('308', ['00001B74'], None, None),
    # 309 exact-unique; route TextIns idx 11 (single path)
    '00001B76': ('309', ['00001B7A'], None, None),
    # 310 exact-unique; route TextIns idx 11,15,19 (single path)
    '00001C5D': ('310', ['00001C60', 'line15', 'line19'], None, None),
    # 311 exact-unique; route TextIns idx 8 (single path)
    '00001EFF': ('311', ['00001F01'], None, None),
    # 312 exact-unique; route TextIns idx 11 (single path)
    '000021FE': ('312', ['00002201'], None, None),
    # 313 exact-unique; route TextIns idx 11,17 (single path)
    '00002225': ('313', ['00002228', '0000222A'], None, None),
    # 315 exact-unique; route TextIns idx 11 (single path)
    '00002340': ('315', ['00002343'], None, None),
}

H = {
    # hidden 0 (連番 158) exact-unique; hidden dispatch 000015E3 idx 1754 -> PCReset 1745 -> Jump 0000240C:0 (idx 1747);
    #   route TextIns idx 11
    '0': ('158', '0000240C', ['0000240F'], None, None),
    # hidden 1 (連番 85) exact-unique; hidden dispatch 000015E3 idx 1756 -> PCReset 1791 -> Jump 0000241B:0 (idx 1793);
    #   route TextIns idx 11
    '1': ('85', '0000241B', ['0000241E'], None, None),
    # hidden 2 (連番 104) exact-unique; hidden dispatch 000015E3 idx 1758 -> PCReset 1794 -> Jump 00002420:0 (idx 1796);
    #   route TextIns idx 11
    '2': ('104', '00002420', ['00002423'], None, None),
    # hidden 3 (連番 170) exact-unique; hidden dispatch 000015E3 idx 1760 -> PCReset 1797 -> Jump 0000242E:0 (idx 1799);
    #   route TextIns idx 11
    '3': ('170', '0000242E', ['00002431'], None, None),
    # hidden 4 (連番 173) exact-unique; hidden dispatch 000015E3 idx 1764 -> PCReset 1803 -> Jump 00002427:0 (idx 1805);
    #   route TextIns idx 11
    '4': ('173', '00002427', ['0000242A'], None, None),
    # hidden 5 (連番 102) exact-unique; hidden dispatch 000015E3 idx 1762 -> PCReset 1800 -> Jump 00002433:0 (idx 1802);
    #   route TextIns idx 11
    '5': ('102', '00002433', ['00002436'], None, None),
    # hidden 6 (連番 239) exact-unique; hidden dispatch 000015E3 idx 1774 -> PCReset 1818 -> Jump 00002457:0 (idx 1820);
    #   route TextIns idx 11
    '6': ('239', '00002457', ['0000245A'], None, None),
    # hidden 7 (連番 240) exact-unique; hidden dispatch 000015E3 idx 1776 -> PCReset 1821 -> Jump 0000245F:0 (idx 1823);
    #   route TextIns idx 11
    '7': ('240', '0000245F', ['00002462'], None, None),
    # hidden 8 (連番 242) exact-unique; hidden dispatch 000015E3 idx 1778 -> PCReset 1824 -> Jump 00002464:0 (idx 1826);
    #   route TextIns idx 11
    '8': ('242', '00002464', ['00002467'], None, None),
    # hidden 9 (連番 107) exact-unique; hidden dispatch 000015E3 idx 1780 -> PCReset 1827 -> Jump 0000246E:0 (idx 1829);
    #   route TextIns idx 11
    '9': ('107', '0000246E', ['00002471'], None, None),
    # hidden 10 (連番 111) exact-unique; hidden dispatch 000015E3 idx 1782 -> PCReset 1830 -> Jump 00002473:0 (idx
    #   1832); route TextIns idx 11
    '10': ('111', '00002473', ['00002476'], None, None),
    # hidden 11 (連番 255) exact-unique; hidden dispatch 000015E3 idx 1784 -> PCReset 1833 -> Jump 00002478:0 (idx
    #   1835); route TextIns idx 11
    '11': ('255', '00002478', ['0000247B'], None, None),
    # hidden 12 (連番 213) exact-unique; hidden dispatch 000015E3 idx 1766 -> PCReset 1806 -> Jump 00002439:0 (idx
    #   1808); route TextIns idx 11
    '12': ('213', '00002439', ['0000243C'], None, None),
    # hidden 13 (連番 217) exact-unique; hidden dispatch 000015E3 idx 1768 -> PCReset 1809 -> Jump 0000243F:0 (idx
    #   1811); route TextIns idx 11
    '13': ('217', '0000243F', ['00002442'], None, None),
    # hidden 14 (連番 218) exact-unique; hidden dispatch 000015E3 idx 1770 -> PCReset 1812 -> Jump 00002444:0 (idx
    #   1814); route TextIns idx 14; 裏分岐=0
    '14': ('218', '00002444', ['00002447'], None, None),
    # hidden 15 (連番 218) exact-unique; hidden dispatch 000015E3 idx 1770 -> PCReset 1812 -> Jump 00002444:0 (idx
    #   1814); route TextIns idx 20; 裏分岐=2
    '15': ('218', '00002444', ['00002449'], None, None),
    # hidden 16 (連番 218) exact-unique; hidden dispatch 000015E3 idx 1770 -> PCReset 1812 -> Jump 00002444:0 (idx
    #   1814); route TextIns idx 26; 裏分岐=3
    '16': ('218', '00002444', ['0000244D'], None, None),
    # hidden 17 (連番 218) exact-unique; hidden dispatch 000015E3 idx 1770 -> PCReset 1812 -> Jump 00002444:0 (idx
    #   1814); route TextIns idx 32; 裏分岐=4
    '17': ('218', '00002444', ['0000244E'], None, None),
}

# True-Jusatsu section routes: the source of ノベルシステム/真呪殺編文字数.txt (built in English by
# tools/build_tj_counts.py). TJ[連番] = (lsb id, [opening blocks = section -1], [[section 0 blocks], ...]).
# Each section is traced alone from its 真呪殺編選択 dispatch jump to the label where all sections converge;
# the opening runs to the counter reset 文字数誤差 = 0. Sections 0..N concatenated = R[lsb] 文字数1 recipe.
# File line: 連番, title, N, opening, section 0..N-1, zero padding (00000E7B idx 132-145 picks the line).
TJ = {
    # 245: 9 sections, convergence idx 270
    '245': ('00000E7B',
        ['00001D0A', 'line215', 'line219', 'line223', 'line227'],
        [
            ['00000E87'],
            ['00000FEE'],
            ['00000FEF'],
            ['00000FF0', 'line44', 'line48'],
            ['00000FF1'],
            ['00000FF4', 'line64', 'line68', 'line72', 'line76'],
            ['00001D01'],
            ['00000FF6', 'line92', 'line96', 'line100', 'line104'],
            ['00000FF5', '00001D0D'],
        ]),
    # 246: 9 sections, convergence idx 115
    '246': ('00000EAF',
        ['00001DA1', 'line62', 'line66', 'line70', 'line74'],
        [
            ['00001D9D'],
            ['00001D9A'],
            ['00001D93'],
            ['00001D8D'],
            ['00001DD5'],
            ['00001D8A'],
            ['00001D87'],
            ['00001DD6'],
            ['00001D82'],
        ]),
    # 247: 13 sections, convergence idx 155
    '247': ('00000EDF',
        ['00001DB7', 'line99', 'line103', 'line107', 'line111', '00001E79', '00001E7C'],
        [
            ['00001DB2'],
            ['00001DB3'],
            ['00001DDA'],
            ['00001DB4'],
            ['00001DDC'],
            ['00001DB5'],
            ['00001DB6'],
            ['00001DDF'],
            ['00001DAF'],
            ['00001DB1'],
            ['00001DB0'],
            ['00001DAE', 'line37', 'line41'],
            ['00001DBA'],
        ]),
    # 248: 11 sections, convergence idx 70
    '248': ('00000EF6',
        ['00001DFF'],
        [
            ['00001DFC'],
            ['00001DF9'],
            ['00001DF7'],
            ['00001DEF'],
            ['00001DEE'],
            ['00001DEC', 'line46', 'line50'],
            ['00001DEB'],
            ['00001DE9'],
            ['00001DE6'],
            ['00001DE5'],
            ['00001DE3'],
        ]),
    # 249: 13 sections, convergence idx 88
    '249': ('00000F0D',
        ['00002056'],
        [
            ['00000F19'],
            ['0000100C'],
            ['0000100D'],
            ['0000100E'],
            ['00001010'],
            ['0000101C'],
            ['0000101D'],
            ['00001028'],
            ['000021E0'],
            ['00001029'],
            ['0000102A'],
            ['0000102B'],
            ['0000102C', '000021E1'],
        ]),
    # 250: 15 sections, convergence idx 55
    '250': ('00000F24',
        ['00001E85'],
        [
            ['00001E84'],
            ['00001E83'],
            ['00001E8E'],
            ['00001E8D'],
            ['00001E8C'],
            ['00001E8B'],
            ['00001E8A'],
            ['00001E89'],
            ['00001E82'],
            ['00001E88'],
            ['00001E87'],
            ['00001E86'],
            ['00001E8F'],
            ['00001E99'],
            ['00001EA2'],
        ]),
    # 305: 14 sections, convergence idx 100
    '305': ('0000156A',
        ['00001E75'],
        [
            ['00001E6C'],
            ['00001E68'],
            ['00001E67'],
            ['00001E64'],
            ['00001E63'],
            ['00001E62'],
            ['00001E61'],
            ['00001E60'],
            ['00001E5F'],
            ['00001E5E'],
            ['00001E5C'],
            ['00001E5B'],
            ['00001E5D', 'line24', 'line28'],
            ['00001E78', 'line197', 'line201'],
        ]),
}

# (連番, section; -1 = opening): residual = value in orig 真呪殺編文字数.txt - reproduced JP (stale author
# values; the build accepts exactly these). Their sums are the 文字数1 residuals in STALE_OK.
TJ_STALE = {
    ('245', 1): +2,
    ('245', 3): +2,
    ('247', -1): +4,
    ('247', 11): +4,
    ('250', 3): +2,
    ('305', 12): +2,
}
