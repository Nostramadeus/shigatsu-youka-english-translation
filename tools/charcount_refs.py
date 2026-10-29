"""Write English reference totals: column 文字数 of tsv-en/リファレンスデータベース.tsv.

    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_refs.py          # dry run
    uv run --no-project --python 3.12 --with pylivemaker python tools/charcount_refs.py --write  # write

WHY (counter repair 2026-10-29, work/feedback-repair-20261029/COUNTERS-PLAN.md, Lane B): a reference document
read as a scenario shows "<running>/<total> chars (NN.NN%)". The running count is the English message-box
length (00001F8A L570-574); the total is 文字数 of the reference table (0000001E L360 -> L2045
リファシナリオテキスト数), which was still Japanese, e.g. "686/305 chars (224.91%)". This script makes the stored
total English, counted with the engine's own rule (tools/count_chars.py) from the text that SHIPS.

HOW, per row of REFS (key = internal reference ID, never the displayed No.):
1. Route gate. 0000001E (orig and work) dispatches the ID: `If/Elseif ID保存 == N` + `PCReset 0000001E:<L>`, and
   at <L> sits `Label`, `Call 0000001E:1`, `Jump <lsb>:0`. From there the script is walked strictly linearly in
   both orig/<lsb>.lsb and work/<lsb>.lsb: TextIns into "メッセージボックス" are collected until the unconditional
   `Jump 00001A13.lsb` exit. Any If/While, conditional Jump/Call, cross-file Jump/Call, PCReset or Exit refuses the
   row. Both block lists must equal the recipe.
2. JP gate. The recipe summed over lns/ (Japanese) must reproduce the stored JP total; STALE_OK rows may differ
   by exactly their recorded residual. Stored JP comes from work/_charcount/jp-ref-totals.tsv once written.
3. VAR gate. A <VAR> in a route block is refused unless VAR_OK names it with the same count in JP and EN.
   ID 295: one <VAR NAME="プレイヤー名">; 0000001E idx 2327 L2570 adds JLength(プレイヤー名) to this row's 文字数
   at runtime, so the stored value is the text without the name in both languages.
4. EN total: work/<lsb>.lsb re-extracted with tools/extract_lsb.py into work/_charcount/<lsb>/ and the same
   blocks counted. The cell must currently hold the stored JP or this EN value (else someone changed it: refuse).
Only the 文字数 cell of REFS rows changes; every other byte (LF/CRLF style, trailing empty cells) is kept.
Old JP values are saved to work/_charcount/jp-ref-totals.tsv (ID, displayed No., JP) on --write.

NOT_CONSUMED rows (form report/object, 32 rows) are left as they are: 0000001E reads 文字数 only for the
scenario and side-tale forms (idx 355 L357, idx 517 L545, idx 799 L834) and has no ID dispatch for them; the other
scripts that open the reference DB (000000F2, 000016C3, 00001878, 000019DD, 00001A13, 00001F85, 00001FBE) never
read the column.
実況 (plan D4): does not apply. 0000001E never activates the 実況 DB (checked on every run), and the commentary
trigger (00001F8A L669) compares the scenario numerator 文字数誤差, which L553 does not advance while
リファレンスシナリオ中 == 1. Files in データベース/実況/ are keyed by scenario 連番; equal numbers are coincidences.
After a write the orchestrator runs build_tsv.py リファレンスデータベース.tsv and build_en_folder.py.
Re-run after any recompile of a reference script: the totals follow the shipped text.
"""
import argparse
import re
import shutil
import sys
from collections import Counter
from io import BytesIO
from pathlib import Path

from livemaker.lsb import LMScript

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from count_chars import blocks, body  # noqa: E402
from extract_lsb import escape_name, extract as lsb_extract  # noqa: E402

TABLE = ROOT / 'tsv-en' / 'リファレンスデータベース.tsv'
JP_STORE = ROOT / 'work' / '_charcount' / 'jp-ref-totals.tsv'
EXTRACT = ROOT / 'work' / '_charcount'
DISPATCHER = '0000001E'
EXIT_PAGE = '00001A13.lsb'
MSGBOX = '"メッセージボックス"'
LSB_ID = re.compile(r'[0-9A-F]{8}')
VAR_TAG = re.compile(r'<VAR\b[^>]*>', re.IGNORECASE)
VAR_NAME = re.compile(r'NAME="([^"]*)"')

# Residual = stored JP minus the route's JP. Proven route, no block subset reproduces the stored number: the
# author's value predates a small text edit (same pattern as first-arc rows 147/170/202 in counters-audit.json).
STALE_OK = {
    '51': 2,   # 000003B4: linear route 000003B6 + 000003BA = 1111, stored 1113; only 2 nonempty blocks, no other subset
    '46': 2,   # 000019E9: linear route 000019EB + 00002406 (empty) + 00002404 = 1235, stored 1237
    '193': 5,  # 0000212D: single live block 0000212F = 1524, stored 1529; the file has no other nonempty block
}
# {ID: {VAR name: count}} - only substitutions the runtime already accounts for (0000001E idx 2327 L2570).
VAR_OK = {'295': {'プレイヤー名': 1}}

# ID: (displayed No., lsb, route blocks in play order). Comment: proof type, stored JP, 0000001E dispatch
# (If command index + LineNo -> PCReset label index -> Jump), TextIns command indices in the lsb.
# "exact-unique" = the route's JP sum equals the stored value AND it is the only subset of the script's nonempty
# blocks that does. Every route was walked in orig/ and work/ (identical topology, work == game/en).
REFS = {
    '1': (4, '00001073', ('00001075',)),  # exact-unique 1383; idx1837 L2072 -> PCReset 2155 -> Jump 00001073:0 -> TextIns 8
    '5': (9, '00001704', ('00001706',)),  # exact-unique 627; idx1839 L2074 -> PCReset 2158 -> Jump 00001704:0 -> TextIns 8
    '6': (12, '0000170A', ('0000170C',)),  # exact-unique 846; idx1841 L2076 -> PCReset 2161 -> Jump 0000170A:0 -> TextIns 8
    '8': (13, '00001715', ('00001717',)),  # exact-unique 1468; idx1843 L2078 -> PCReset 2164 -> Jump 00001715:0 -> TextIns 8
    '9': (18, '0000171B', ('0000171D',)),  # exact-unique 1015; idx1845 L2080 -> PCReset 2167 -> Jump 0000171B:0 -> TextIns 8
    '11': (32, '0000172F', ('00001731',)),  # exact-unique 823; idx1849 L2084 -> PCReset 2188 -> Jump 0000172F:0 -> TextIns 8
    '12': (37, '00001755', ('00001757',)),  # exact-unique 1152; idx1855 L2090 -> PCReset 2201 -> Jump 00001755:0 -> TextIns 8
    '14': (42, '000017E2', ('000017E4',)),  # exact-unique 216; idx1861 L2096 -> PCReset 2216 -> Jump 000017E2:0 -> TextIns 8
    '18': (50, '00001800', ('00001802',)),  # exact-unique 475; idx1865 L2100 -> PCReset 2222 -> Jump 00001800:0 -> TextIns 8
    '20': (48, '000017FA', ('000017FC',)),  # exact-unique 507; idx1863 L2098 -> PCReset 2219 -> Jump 000017FA:0 -> TextIns 8
    '21': (104, '00001AE8', ('00001AEA',)),  # exact-unique 1097; idx1913 L2148 -> PCReset 2691 -> Jump 00001AE8:0 -> TextIns 8
    '22': (51, '00001807', ('00001809',)),  # exact-unique 1278; idx1867 L2102 -> PCReset 2225 -> Jump 00001807:0 -> TextIns 8
    '24': (58, '00001835', ('00001837',)),  # exact-unique 997; idx1877 L2112 -> PCReset 2240 -> Jump 00001835:0 -> TextIns 8
    '25': (61, '00001844', ('00001846',)),  # exact-unique 752; idx1879 L2114 -> PCReset 2243 -> Jump 00001844:0 -> TextIns 8
    '26': (62, '00001849', ('0000184B',)),  # exact-unique 1434; idx1881 L2116 -> PCReset 2246 -> Jump 00001849:0 -> TextIns 8
    '30': (30, '00001729', ('0000172B',)),  # exact-unique 261; idx1847 L2082 -> PCReset 2185 -> Jump 00001729:0 -> TextIns 8
    '36': (35, '00001741', ('00001743',)),  # exact-unique 938; idx1853 L2088 -> PCReset 2198 -> Jump 00001741:0 -> TextIns 8
    '37': (56, '0000182A', ('0000182C',)),  # exact-unique 504; idx1873 L2108 -> PCReset 2234 -> Jump 0000182A:0 -> TextIns 8
    '38': (57, '00001830', ('00001832',)),  # exact-unique 1024; idx1875 L2110 -> PCReset 2237 -> Jump 00001830:0 -> TextIns 8
    '39': (65, '00001854', ('00001856',)),  # exact-unique 261; idx1883 L2118 -> PCReset 2249 -> Jump 00001854:0 -> TextIns 8
    '43': (118, '00001B81', ('00001B83',)),  # exact-unique 1156; idx1915 L2150 -> PCReset 2704 -> Jump 00001B81:0 -> TextIns 8
    '44': (55, '0000181F', ('00001821',)),  # exact-unique 1182; idx1871 L2106 -> PCReset 2231 -> Jump 0000181F:0 -> TextIns 8
    '46': (66, '000019E9', ('000019EB', '00002406', '00002404')),  # stale residual +2 1237; idx1885 L2120 -> PCReset 2358 -> Jump 000019E9:0 -> TextIns 8+40+26; JP-empty on route: 00002406
    '47': (70, '00001A4E', ('00001A50',)),  # exact-unique 1630; idx1909 L2144 -> PCReset 2685 -> Jump 00001A4E:0 -> TextIns 8
    '49': (71, '00001A52', ('00001A54',)),  # exact-unique 902; idx1887 L2122 -> PCReset 2652 -> Jump 00001A52:0 -> TextIns 8
    '51': (24, '000003B4', ('000003B6', '000003BA')),  # stale residual +2 1113; idx1833 L2068 -> PCReset 2100 -> Jump 000003B4:0 -> TextIns 8+23
    '55': (54, '00001818', ('0000181A',)),  # exact-unique 775; idx1869 L2104 -> PCReset 2228 -> Jump 00001818:0 -> TextIns 8
    '56': (75, '00001A5C', ('00001A5E',)),  # exact-unique 1730; idx1889 L2124 -> PCReset 2655 -> Jump 00001A5C:0 -> TextIns 8
    '57': (78, '00001A65', ('00001A67',)),  # exact-unique 2104; idx1891 L2126 -> PCReset 2658 -> Jump 00001A65:0 -> TextIns 8
    '58': (79, '00001A6B', ('00001F97',)),  # exact-unique 2681; idx1893 L2128 -> PCReset 2661 -> Jump 00001A6B:0 -> TextIns 22
    '60': (77, '00001A74', ('00001A76',)),  # exact-unique 907; idx1895 L2130 -> PCReset 2664 -> Jump 00001A74:0 -> TextIns 8
    '63': (82, '00001A7F', ('00001A81',)),  # exact-unique 1616; idx1897 L2132 -> PCReset 2667 -> Jump 00001A7F:0 -> TextIns 8
    '64': (83, '00001A85', ('00001A87',)),  # exact-unique 547; idx1899 L2134 -> PCReset 2670 -> Jump 00001A85:0 -> TextIns 8
    '73': (10, '000003A8', ('000003AA',)),  # exact-unique 659; idx1829 L2064 -> PCReset 2094 -> Jump 000003A8:0 -> TextIns 8
    '74': (88, '00001A8C', ('00001A8E',)),  # exact-unique 1362; idx1901 L2136 -> PCReset 2673 -> Jump 00001A8C:0 -> TextIns 8
    '78': (39, '000017CB', ('000017CD',)),  # exact-unique 305; idx1857 L2092 -> PCReset 2210 -> Jump 000017CB:0 -> TextIns 8
    '79': (40, '000017D3', ('000017D5',)),  # exact-unique 297; idx1859 L2094 -> PCReset 2213 -> Jump 000017D3:0 -> TextIns 8
    '80': (91, '00001A97', ('00001A99',)),  # exact-unique 924; idx1903 L2138 -> PCReset 2676 -> Jump 00001A97:0 -> TextIns 8
    '82': (94, '00001AA5', ('00001AA7',)),  # exact-unique 884; idx1905 L2140 -> PCReset 2679 -> Jump 00001AA5:0 -> TextIns 8
    '84': (23, '000003BC', ('000003BE',)),  # exact-unique 363; idx1835 L2070 -> PCReset 2103 -> Jump 000003BC:0 -> TextIns 8
    '87': (33, '00001735', ('00001737',)),  # exact-unique 379; idx1851 L2086 -> PCReset 2191 -> Jump 00001735:0 -> TextIns 8
    '88': (96, '00001AAE', ('00001AB0',)),  # exact-unique 809; idx1907 L2142 -> PCReset 2682 -> Jump 00001AAE:0 -> TextIns 8
    '89': (98, '00001AB5', ('00001AB7',)),  # exact-unique 346; idx1911 L2146 -> PCReset 2688 -> Jump 00001AB5:0 -> TextIns 8
    '97': (29, '000003AE', ('000003B0',)),  # exact-unique 787; idx1831 L2066 -> PCReset 2097 -> Jump 000003AE:0 -> TextIns 8
    '99': (116, '00001B8E', ('00001B90',)),  # exact-unique 821; idx1917 L2152 -> PCReset 2727 -> Jump 00001B8E:0 -> TextIns 8
    '106': (122, '00001B98', ('00001B9A',)),  # exact-unique 557; idx1919 L2154 -> PCReset 2730 -> Jump 00001B98:0 -> TextIns 8
    '112': (125, '00001BA2', ('00001BA4',)),  # exact-unique 138; idx1921 L2156 -> PCReset 2733 -> Jump 00001BA2:0 -> TextIns 8
    '113': (128, '00001BA8', ('00001BAA',)),  # exact-unique 424; idx1923 L2158 -> PCReset 2736 -> Jump 00001BA8:0 -> TextIns 8
    '114': (130, '00001BAE', ('00001BB0',)),  # exact-unique 450; idx1925 L2160 -> PCReset 2739 -> Jump 00001BAE:0 -> TextIns 8
    '115': (132, '00001BB4', ('00001BB6',)),  # exact-unique 1071; idx1927 L2162 -> PCReset 2742 -> Jump 00001BB4:0 -> TextIns 8
    '116': (133, '00001BBA', ('00001BBC',)),  # exact-unique 950; idx1929 L2164 -> PCReset 2745 -> Jump 00001BBA:0 -> TextIns 8
    '117': (135, '00001BC4', ('00001BC6',)),  # exact-unique 1055; idx1931 L2166 -> PCReset 2748 -> Jump 00001BC4:0 -> TextIns 8
    '120': (138, '00001BCE', ('00001BD0',)),  # exact-unique 1963; idx1933 L2168 -> PCReset 2751 -> Jump 00001BCE:0 -> TextIns 8
    '121': (141, '00001BD4', ('00001BD6',)),  # exact-unique 155; idx1935 L2170 -> PCReset 2754 -> Jump 00001BD4:0 -> TextIns 8
    '123': (144, '00001BDA', ('00001BDC',)),  # exact-unique 585; idx1937 L2172 -> PCReset 2757 -> Jump 00001BDA:0 -> TextIns 8
    '124': (145, '00001BE8', ('00001BEA',)),  # exact-unique 758; idx1939 L2174 -> PCReset 2760 -> Jump 00001BE8:0 -> TextIns 8
    '125': (146, '00001BEE', ('00001BF0',)),  # exact-unique 847; idx1941 L2176 -> PCReset 2763 -> Jump 00001BEE:0 -> TextIns 8
    '126': (148, '00001BF7', ('00001BF9',)),  # exact-unique 1187; idx1943 L2178 -> PCReset 2766 -> Jump 00001BF7:0 -> TextIns 8
    '129': (149, '00001C02', ('00001C04',)),  # exact-unique 1115; idx1945 L2180 -> PCReset 2769 -> Jump 00001C02:0 -> TextIns 8
    '130': (150, '00001C08', ('00001C0A',)),  # exact-unique 487; idx1947 L2182 -> PCReset 2772 -> Jump 00001C08:0 -> TextIns 8
    '131': (151, '00001C12', ('00001C14',)),  # exact-unique 576; idx1949 L2184 -> PCReset 2775 -> Jump 00001C12:0 -> TextIns 8
    '133': (155, '00001C1D', ('00001C1F',)),  # exact-unique 923; idx1951 L2186 -> PCReset 2778 -> Jump 00001C1D:0 -> TextIns 8
    '135': (158, '00001C23', ('00001C25',)),  # exact-unique 1134; idx1953 L2188 -> PCReset 2781 -> Jump 00001C23:0 -> TextIns 8
    '136': (159, '00001C29', ('00001C2B',)),  # exact-unique 614; idx1955 L2190 -> PCReset 2784 -> Jump 00001C29:0 -> TextIns 8
    '140': (162, '00001C34', ('00001C36',)),  # exact-unique 777; idx1957 L2192 -> PCReset 2787 -> Jump 00001C34:0 -> TextIns 8
    '144': (154, '00001C55', ('00001C57',)),  # exact-unique 342; idx1959 L2194 -> PCReset 2838 -> Jump 00001C55:0 -> TextIns 8
    '145': (166, '00001D0E', ('00001D10',)),  # exact-unique 1861; idx1961 L2196 -> PCReset 2841 -> Jump 00001D0E:0 -> TextIns 8
    '146': (170, '00001D17', ('00001D19', 'line12', 'line16')),  # exact-unique 849; idx1963 L2198 -> PCReset 2844 -> Jump 00001D17:0 -> TextIns 8+12+16
    '147': (173, '00001D1E', ('00001D20',)),  # exact-unique 624; idx1965 L2200 -> PCReset 2847 -> Jump 00001D1E:0 -> TextIns 8
    '148': (175, '00001D2A', ('00001D2C',)),  # exact-unique 318; idx1967 L2202 -> PCReset 2850 -> Jump 00001D2A:0 -> TextIns 8
    '149': (181, '00001D34', ('00001D36',)),  # exact-unique 76; idx1969 L2204 -> PCReset 2853 -> Jump 00001D34:0 -> TextIns 8
    '150': (184, '00001D3B', ('00001D3D',)),  # exact-unique 557; idx1971 L2206 -> PCReset 2856 -> Jump 00001D3B:0 -> TextIns 8
    '151': (186, '00001D40', ('00001D42',)),  # exact-unique 912; idx1973 L2208 -> PCReset 2859 -> Jump 00001D40:0 -> TextIns 8
    '160': (189, '00002090', ('00002092',)),  # exact-unique 1635; idx2019 L2254 -> PCReset 4266 -> Jump 00002090:0 -> TextIns 8
    '161': (190, '00002096', ('00002098',)),  # exact-unique 790; idx2021 L2256 -> PCReset 4269 -> Jump 00002096:0 -> TextIns 8
    '165': (196, '00002078', ('0000207A',)),  # exact-unique 719; idx2011 L2246 -> PCReset 4254 -> Jump 00002078:0 -> TextIns 8
    '166': (197, '0000207E', ('00002080',)),  # exact-unique 863; idx2013 L2248 -> PCReset 4257 -> Jump 0000207E:0 -> TextIns 8
    '168': (198, '00002084', ('00002086',)),  # exact-unique 1397; idx2015 L2250 -> PCReset 4260 -> Jump 00002084:0 -> TextIns 8
    '177': (207, '0000208A', ('0000208C',)),  # exact-unique 338; idx2017 L2252 -> PCReset 4263 -> Jump 0000208A:0 -> TextIns 8
    '180': (209, '000020B4', ('000020B6',)),  # exact-unique 1209; idx2031 L2266 -> PCReset 4284 -> Jump 000020B4:0 -> TextIns 8
    '181': (210, '000020BB', ('000020BD',)),  # exact-unique 987; idx2033 L2268 -> PCReset 4287 -> Jump 000020BB:0 -> TextIns 8
    '185': (214, '000020C0', ('000020C2',)),  # exact-unique 564; idx2035 L2270 -> PCReset 4290 -> Jump 000020C0:0 -> TextIns 8
    '186': (215, '000020C6', ('000020C8',)),  # exact-unique 527; idx2037 L2272 -> PCReset 4293 -> Jump 000020C6:0 -> TextIns 8
    '187': (216, '000020CC', ('000020CE',)),  # exact-unique 593; idx2039 L2274 -> PCReset 4296 -> Jump 000020CC:0 -> TextIns 8
    '188': (217, '000020D2', ('000020D4',)),  # exact-unique 300; idx2041 L2276 -> PCReset 4299 -> Jump 000020D2:0 -> TextIns 8
    '193': (1, '0000212D', ('0000212F',)),  # stale residual +5 1529; idx2071 L2306 -> PCReset 4344 -> Jump 0000212D:0 -> TextIns 8
    '194': (2, '00002137', ('00002139',)),  # exact-unique 1184; idx2073 L2308 -> PCReset 4355 -> Jump 00002137:0 -> TextIns 8
    '195': (3, '0000213D', ('0000214D',)),  # exact-unique 1117; idx2075 L2310 -> PCReset 4358 -> Jump 0000213D:0 -> TextIns 15
    '196': (4, '00002143', ('0000214E',)),  # exact-unique 2144; idx4509 L4746 -> PCReset 4572 -> Jump 00002143:0 -> TextIns 15
    '197': (5, '0000214F', ('00002151',)),  # exact-unique 1104; idx4511 L4748 -> PCReset 4575 -> Jump 0000214F:0 -> TextIns 8
    '198': (6, '00002158', ('0000215A',)),  # exact-unique 913; idx4513 L4750 -> PCReset 4578 -> Jump 00002158:0 -> TextIns 8
    '199': (7, '0000215E', ('00002160',)),  # exact-unique 1360; idx4515 L4752 -> PCReset 4581 -> Jump 0000215E:0 -> TextIns 8
    '200': (8, '00002164', ('00002166',)),  # exact-unique 1519; idx4517 L4754 -> PCReset 4584 -> Jump 00002164:0 -> TextIns 8
    '201': (9, '0000216E', ('00002170',)),  # exact-unique 1031; idx4519 L4756 -> PCReset 4591 -> Jump 0000216E:0 -> TextIns 8
    '202': (10, '00002174', ('00002176',)),  # exact-unique 1002; idx4521 L4758 -> PCReset 4594 -> Jump 00002174:0 -> TextIns 8
    '203': (11, '0000217A', ('0000217C',)),  # exact-unique 1446; idx4523 L4760 -> PCReset 4597 -> Jump 0000217A:0 -> TextIns 8
    '204': (12, '00002181', ('00002183',)),  # exact-unique 1444; idx4525 L4762 -> PCReset 4600 -> Jump 00002181:0 -> TextIns 8
    '205': (13, '00002187', ('00002189',)),  # exact-unique 945; idx4527 L4764 -> PCReset 4603 -> Jump 00002187:0 -> TextIns 8
    '206': (14, '0000218D', ('0000218F',)),  # exact-unique 903; idx4529 L4766 -> PCReset 4606 -> Jump 0000218D:0 -> TextIns 8
    '207': (15, '00002193', ('00002195',)),  # exact-unique 1681; idx4531 L4768 -> PCReset 4609 -> Jump 00002193:0 -> TextIns 8
    '221': (74, '00001FE9', ('00001FEB',)),  # exact-unique 992; idx1977 L2212 -> PCReset 4201 -> Jump 00001FE9:0 -> TextIns 8
    '222': (84, '00001FEF', ('00001FF1',)),  # exact-unique 539; idx1979 L2214 -> PCReset 4204 -> Jump 00001FEF:0 -> TextIns 8
    '223': (86, '00001FF5', ('00001FF7', 'line12', 'line16')),  # exact-unique 748; idx1981 L2216 -> PCReset 4207 -> Jump 00001FF5:0 -> TextIns 8+12+16; JP-empty on route: line16
    '224': (93, '00001FFB', ('00001FFD',)),  # exact-unique 208; idx1983 L2218 -> PCReset 4210 -> Jump 00001FFB:0 -> TextIns 8
    '225': (97, '00002001', ('00002003',)),  # exact-unique 1675; idx1985 L2220 -> PCReset 4213 -> Jump 00002001:0 -> TextIns 8
    '226': (103, '00002007', ('00002009',)),  # exact-unique 1268; idx1987 L2222 -> PCReset 4216 -> Jump 00002007:0 -> TextIns 8
    '227': (109, '0000200D', ('0000200F',)),  # exact-unique 348; idx1989 L2224 -> PCReset 4219 -> Jump 0000200D:0 -> TextIns 8
    '228': (119, '00002013', ('00002015',)),  # exact-unique 492; idx1991 L2226 -> PCReset 4222 -> Jump 00002013:0 -> TextIns 8
    '229': (120, '00002019', ('0000201B',)),  # exact-unique 370; idx1993 L2228 -> PCReset 4225 -> Jump 00002019:0 -> TextIns 8
    '230': (126, '0000201F', ('00002021',)),  # exact-unique 671; idx1995 L2230 -> PCReset 4228 -> Jump 0000201F:0 -> TextIns 8
    '231': (134, '00002026', ('00002028',)),  # exact-unique 1513; idx1997 L2232 -> PCReset 4233 -> Jump 00002026:0 -> TextIns 8
    '232': (25, '0000206C', ('0000206E',)),  # exact-unique 353; idx2007 L2242 -> PCReset 4248 -> Jump 0000206C:0 -> TextIns 8
    '233': (139, '0000202C', ('0000202E',)),  # exact-unique 1140; idx1999 L2234 -> PCReset 4236 -> Jump 0000202C:0 -> TextIns 8
    '234': (140, '00002057', ('00002059',)),  # exact-unique 1096; idx2001 L2236 -> PCReset 4239 -> Jump 00002057:0 -> TextIns 8
    '235': (167, '00002066', ('00002068',)),  # exact-unique 467; idx2005 L2240 -> PCReset 4245 -> Jump 00002066:0 -> TextIns 8
    '236': (180, '00002072', ('00002074',)),  # exact-unique 1066; idx2009 L2244 -> PCReset 4251 -> Jump 00002072:0 -> TextIns 8
    '238': (152, '0000205F', ('00002061',)),  # exact-unique 854; idx2003 L2238 -> PCReset 4242 -> Jump 0000205F:0 -> TextIns 8
    '242': (204, '000020A2', ('000020A4',)),  # exact-unique 687; idx2025 L2260 -> PCReset 4275 -> Jump 000020A2:0 -> TextIns 8
    '243': (199, '0000209C', ('0000209E',)),  # exact-unique 964; idx2023 L2258 -> PCReset 4272 -> Jump 0000209C:0 -> TextIns 8
    '244': (208, '000020A8', ('000020AA',)),  # exact-unique 1400; idx2027 L2262 -> PCReset 4278 -> Jump 000020A8:0 -> TextIns 8
    '246': (206, '000020AE', ('000020B0',)),  # exact-unique 1185; idx2029 L2264 -> PCReset 4281 -> Jump 000020AE:0 -> TextIns 8
    '247': (218, '000020D8', ('000020DA',)),  # exact-unique 958; idx2043 L2278 -> PCReset 4302 -> Jump 000020D8:0 -> TextIns 8
    '248': (219, '000020DE', ('000020E0',)),  # exact-unique 1184; idx2045 L2280 -> PCReset 4305 -> Jump 000020DE:0 -> TextIns 8
    '251': (224, '000020E4', ('000020E6',)),  # exact-unique 968; idx2047 L2282 -> PCReset 4308 -> Jump 000020E4:0 -> TextIns 8
    '253': (226, '000020EA', ('000020EC',)),  # exact-unique 292; idx2049 L2284 -> PCReset 4311 -> Jump 000020EA:0 -> TextIns 8
    '254': (227, '000020F0', ('000020F2',)),  # exact-unique 510; idx2051 L2286 -> PCReset 4314 -> Jump 000020F0:0 -> TextIns 8
    '256': (228, '000020FC', ('000020FE',)),  # exact-unique 1346; idx2055 L2290 -> PCReset 4320 -> Jump 000020FC:0 -> TextIns 8
    '257': (229, '00002102', ('00002104',)),  # exact-unique 533; idx2057 L2292 -> PCReset 4323 -> Jump 00002102:0 -> TextIns 8
    '260': (233, '00002108', ('0000210A',)),  # exact-unique 1215; idx2059 L2294 -> PCReset 4326 -> Jump 00002108:0 -> TextIns 8
    '261': (234, '0000210E', ('00002110',)),  # exact-unique 1072; idx2061 L2296 -> PCReset 4329 -> Jump 0000210E:0 -> TextIns 8
    '263': (238, '00002114', ('00002116',)),  # exact-unique 522; idx2063 L2298 -> PCReset 4332 -> Jump 00002114:0 -> TextIns 8
    '264': (240, '0000211A', ('0000211C',)),  # exact-unique 177; idx2065 L2300 -> PCReset 4335 -> Jump 0000211A:0 -> TextIns 8
    '265': (241, '00002120', ('00002122',)),  # exact-unique 228; idx2067 L2302 -> PCReset 4338 -> Jump 00002120:0 -> TextIns 8
    '267': (235, '00002127', ('00002129',)),  # exact-unique 524; idx2069 L2304 -> PCReset 4341 -> Jump 00002127:0 -> TextIns 8
    '279': (16, '00002199', ('0000219B',)),  # exact-unique 1452; idx4533 L4770 -> PCReset 4612 -> Jump 00002199:0 -> TextIns 8
    '280': (17, '0000219F', ('000021A1',)),  # exact-unique 1299; idx4535 L4772 -> PCReset 4615 -> Jump 0000219F:0 -> TextIns 8
    '281': (18, '000021A5', ('000021A7',)),  # exact-unique 2103; idx4537 L4774 -> PCReset 4618 -> Jump 000021A5:0 -> TextIns 8
    '282': (19, '000021AB', ('000021AD',)),  # exact-unique 574; idx4539 L4776 -> PCReset 4621 -> Jump 000021AB:0 -> TextIns 8
    '283': (20, '000021B1', ('000021B3',)),  # exact-unique 705; idx4541 L4778 -> PCReset 4624 -> Jump 000021B1:0 -> TextIns 8
    '290': (21, '000021B7', ('000021B9',)),  # exact-unique 1619; idx4543 L4780 -> PCReset 4627 -> Jump 000021B7:0 -> TextIns 8
    '291': (22, '000021BD', ('000021BF',)),  # exact-unique 944; idx4545 L4782 -> PCReset 4630 -> Jump 000021BD:0 -> TextIns 8
    '292': (23, '000021C3', ('000021C5',)),  # exact-unique 1066; idx4547 L4784 -> PCReset 4633 -> Jump 000021C3:0 -> TextIns 8
    '293': (24, '000021C9', ('000021CB', 'line12', 'line16')),  # exact-unique 1179; idx4549 L4786 -> PCReset 4636 -> Jump 000021C9:0 -> TextIns 8+12+16
    '294': (25, '000021CF', ('000021D1',)),  # exact-unique 11302; idx4551 L4788 -> PCReset 4639 -> Jump 000021CF:0 -> TextIns 8
    '295': (244, '00002268', ('0000226A',)),  # exact-unique 2490; idx4553 L4790 -> PCReset 4642 -> Jump 00002268:0 -> TextIns 8; VAR プレイヤー名 x1
    '296': (110, '00002306', ('00002308',)),  # exact-unique 522; idx4555 L4792 -> PCReset 4761 -> Jump 00002306:0 -> TextIns 8
    '297': (231, '0000234B', ('0000234D',)),  # exact-unique 231; idx4557 L4794 -> PCReset 4796 -> Jump 0000234B:0 -> TextIns 8
    '298': (236, '00002350', ('00002352',)),  # exact-unique 202; idx4559 L4796 -> PCReset 4799 -> Jump 00002350:0 -> TextIns 8
    '299': (239, '00002355', ('00002357',)),  # exact-unique 203; idx4561 L4798 -> PCReset 4802 -> Jump 00002355:0 -> TextIns 8
    '300': (243, '0000235A', ('0000235C', 'line12')),  # exact-unique 1103; idx4563 L4800 -> PCReset 4805 -> Jump 0000235A:0 -> TextIns 8+12
    '301': (14, '000023AB', ('000023AD',)),  # exact-unique 1469; idx4565 L4802 -> PCReset 4899 -> Jump 000023AB:0 -> TextIns 8
    '312': (60, '000023E7', ('000023E9',)),  # exact-unique 468; idx4567 L4804 -> PCReset 4902 -> Jump 000023E7:0 -> TextIns 8
}

NOT_CONSUMED = {  # ID: (displayed No., form) - see the proof above; never written
    '41': (17, 'report'),
    '77': (90, 'object'),
    '81': (92, 'object'),
    '127': (3, 'report'),
    '128': (4, 'report'),
    '138': (5, 'report'),
    '139': (6, 'report'),
    '141': (147, 'object'),
    '154': (7, 'report'),
    '155': (18, 'report'),
    '156': (8, 'report'),
    '162': (9, 'report'),
    '163': (10, 'report'),
    '169': (11, 'report'),
    '171': (12, 'report'),
    '174': (13, 'report'),
    '176': (14, 'report'),
    '178': (15, 'report'),
    '189': (52, 'object'),
    '190': (1, 'report'),
    '191': (2, 'report'),
    '192': (16, 'report'),
    '268': (19, 'report'),
    '269': (20, 'report'),
    '270': (21, 'report'),
    '272': (22, 'report'),
    '273': (23, 'report'),
    '274': (24, 'report'),
    '275': (27, 'report'),
    '276': (26, 'report'),
    '277': (28, 'report'),
    '284': (25, 'report'),
}


class Refused(Exception):
    pass


_scripts = {}


def script(path):
    """Parsed LSB, cached per (path, size, mtime)."""
    st = path.stat()
    key = (str(path), st.st_size, st.st_mtime_ns)
    if key not in _scripts:
        _scripts[key] = LMScript.from_file(BytesIO(path.read_bytes()), call_name=path.name)
    return _scripts[key]


def page_of(cmd):
    pg = cmd['Page']
    return str(pg['Page']), int(pg['Label'])


def dispatch(lsb):
    """{reference ID: (lsb id, entry index)} from the 0000001E ID保存 chain."""
    out = {}
    cmds = lsb.commands
    for i, c in enumerate(cmds[:-1]):
        if c.type.name not in ('If', 'Elseif'):
            continue
        m = re.fullmatch(r'ID保存 == (\d+)', str(c['Calc']).strip())
        if not m or cmds[i + 1].type.name != 'PCReset':
            continue
        page, lab = page_of(cmds[i + 1])
        if page != DISPATCHER + '.lsb':
            continue
        lbl, call, jump = cmds[lab:lab + 3]
        if (lbl.type.name != 'Label' or call.type.name != 'Call' or page_of(call) != (DISPATCHER + '.lsb', 1)
                or jump.type.name != 'Jump' or str(jump['Calc']).strip() != '1'):
            out[m.group(1)] = None
            continue
        tpage, tlab = page_of(jump)
        out[m.group(1)] = (tpage[:-4], tlab) if m.group(1) not in out else None   # a second entry = ambiguous
    return out


def block_name(cmds, i):
    """The .lns block name extract_lsb.py gives TextIns command i."""
    name = escape_name(cmds[i - 2].get('Name', '') if i >= 2 else '')
    return name if name else 'line%d' % cmds[i].LineNo


def walk(lsb, sid, entry):
    """Block names of a strictly linear route from entry to the 00001A13 exit; Refused on anything else."""
    cmds, i, seen, out = lsb.commands, entry, set(), []
    while True:
        if i in seen or i >= len(cmds):
            raise Refused('%s: loop or end of script at %d' % (sid, i))
        seen.add(i)
        c = cmds[i]
        t = c.type.name
        if t == 'TextIns':
            if str(c['Target']) != MSGBOX or c.Mute:
                raise Refused('%s:%d TextIns target %s mute %s' % (sid, i, c['Target'], c.Mute))
            out.append(block_name(cmds, i))
        elif t == 'Jump':
            page, lab = page_of(c)
            if str(c['Calc']).strip() != '1':
                raise Refused('%s:%d conditional Jump' % (sid, i))
            if page == EXIT_PAGE:
                return out
            if page != sid + '.lsb':
                raise Refused('%s:%d Jump to %s' % (sid, i, page))
            i = lab
            continue
        elif t == 'Call':
            page, lab = page_of(c)
            if str(c['Calc']).strip() != '1':
                raise Refused('%s:%d conditional Call' % (sid, i))
            if re.fullmatch(r'[0-9A-F]{8}\.lsb', page) and (page, lab) != (sid + '.lsb', 1):
                raise Refused('%s:%d Call into %s:%d' % (sid, i, page, lab))
        elif t in ('If', 'Elseif', 'Else', 'While', 'WhileInit', 'WhileLoop', 'PCReset', 'Exit'):
            raise Refused('%s:%d %s on the route' % (sid, i, t))
        if i + 1 < len(cmds) and cmds[i + 1].Indent != c.Indent:
            raise Refused('%s:%d indentation change on the route' % (sid, i))
        i += 1


def var_counts(folder, sid, names):
    """{VAR name (or the whole tag if it has no NAME): count} over the route blocks."""
    n = Counter()
    for b in names:
        p = Path(folder) / ('%s-%s.lns' % (sid, b))
        if p.exists():
            for tag in VAR_TAG.findall(body(p)):
                m = VAR_NAME.search(tag)
                n[m.group(1) if m else tag] += 1
    return dict(n)


def no_jikkyo(lsb):
    """D4 evidence: the reference dispatcher never touches the 実況 tables."""
    for c in lsb.commands:
        try:
            s = str(c)
        except Exception:  # a TextIns body; not a DB call
            continue
        if '実況' in s:
            raise Refused('0000001E mentions 実況: %s' % s[:80])


def extract(sid, out_root):
    """Re-extract the shipped work/<sid>.lsb into <out_root>/<sid>/ (emptied first, as charcount_write.py does)."""
    if not LSB_ID.fullmatch(sid):
        raise Refused('bad script id %r' % sid)
    out = Path(out_root) / sid
    if out.exists():
        shutil.rmtree(out)
    lsb_extract(ROOT / 'work' / (sid + '.lsb'), out)
    return out


def read_store(path):
    store = {}
    if path.exists():
        for ln in path.read_text(encoding='utf-8').splitlines():
            c = ln.split('\t')
            if len(c) == 3 and c[2].isdigit():
                store[c[0]] = int(c[2])
    return store


def positive_ids(lines, col):
    out = set()
    for ln in lines[1:]:
        c = ln.split('\t')
        if ln and len(c) > col and c[col].strip().isdigit() and int(c[col]) > 0:
            out.add(c[0])
    return out


def run(table=TABLE, jp_store=JP_STORE, extract_root=EXTRACT, write=False, ids=None, report=None):
    """Returns (results, failures). results: [(ID, disp, lsb, stored JP, JP, EN, proof, status)]."""
    raw = Path(table).read_bytes().decode('utf-8')
    nl = '\r\n' if '\r\n' in raw else '\n'
    lines = raw.split(nl)
    head = lines[0].split('\t')
    col = head.index('文字数')
    rowidx = {}
    for k, ln in enumerate(lines[1:], 1):
        if ln:
            rid = ln.split('\t')[0]
            if rid in rowidx and (rid in REFS or rid in NOT_CONSUMED):   # blank placeholder rows all have ID 0
                raise Refused('duplicate ID %s in %s' % (rid, table))
            rowidx[rid] = k
    store = read_store(Path(jp_store))
    covered = set(REFS) | set(NOT_CONSUMED)
    failures = []
    if ids is None:
        missing = positive_ids(lines, col) - covered
        if missing:
            failures.append('uncovered positive rows: %s' % sorted(missing, key=int))
    d_orig = dispatch(script(ROOT / 'orig' / (DISPATCHER + '.lsb')))
    d_work = dispatch(script(ROOT / 'work' / (DISPATCHER + '.lsb')))
    no_jikkyo(script(ROOT / 'orig' / (DISPATCHER + '.lsb')))
    no_jikkyo(script(ROOT / 'work' / (DISPATCHER + '.lsb')))
    results, changed = [], 0
    todo = [r for r in REFS if ids is None or r in ids]
    for rid in sorted(todo, key=int):
        disp, sid, route = REFS[rid]
        k = rowidx.get(rid)
        cells = lines[k].split('\t') if k else None
        stored = store.get(rid) or (int(cells[col]) if cells and cells[col].strip().isdigit() else 0)
        res = [rid, str(disp), sid, str(stored), '', '', '', '']
        try:
            if cells is None:
                raise Refused('row missing from table')
            if cells[head.index('表示')] != str(disp):
                raise Refused('displayed No. is %s, recipe says %s' % (cells[head.index('表示')], disp))
            for d in (d_orig, d_work):
                if d.get(rid) != (sid, 0):
                    raise Refused('dispatch %s, recipe says %s:0' % (d.get(rid), sid))
            for folder in ('orig', 'work'):
                got = walk(script(ROOT / folder / (sid + '.lsb')), sid, 0)
                if tuple(got) != tuple(route):
                    raise Refused('%s route %s != recipe %s' % (folder, got, list(route)))
            jpd = dict(blocks(sid, 'lns'))
            jp = sum(jpd.get(b, 0) for b in route)
            res[4] = str(jp)
            if stored - jp != STALE_OK.get(rid, 0):
                raise Refused('GATE FAIL: recipe gives JP %d, stored %d' % (jp, stored))
            want = VAR_OK.get(rid, {})
            if var_counts(ROOT / 'lns', sid, route) != want:
                raise Refused('UNRESOLVED-VAR (JP): %s' % var_counts(ROOT / 'lns', sid, route))
            out = extract(sid, extract_root)
            for b in route:
                if not (out / ('%s-%s.lns' % (sid, b))).exists():
                    raise Refused('compiled script has no block %s' % b)
            if var_counts(out, sid, route) != want:
                raise Refused('UNRESOLVED-VAR (EN): %s' % var_counts(out, sid, route))
            end = dict(blocks(sid, str(out)))
            en = sum(end.get(b, 0) for b in route)
            if en <= 0:
                raise Refused('empty English route')
            res[5] = str(en)
            if cells[col] not in (str(stored), str(en)):
                raise Refused('cell holds %s, expected JP %d or EN %d' % (cells[col], stored, en))
            res[6] = ('stale residual +%d' % STALE_OK[rid]) if rid in STALE_OK else 'exact-unique'
            if want:
                res[6] += ' + VAR %s' % want
            if cells[col] != str(en):
                changed += 1
            res[7] = ('DONE' if write else 'DRY') + (' (unchanged)' if cells[col] == str(en) else ' %s -> %d' % (cells[col], en))
            cells[col] = str(en)
            lines[k] = '\t'.join(cells)
            store[rid] = stored
        except Refused as e:
            res[7] = 'UNRESOLVED: %s' % e
            failures.append('%s: %s' % (rid, e))
        results.append(res)
        print('%-4s No.%-4s %s  JP %-5s/%-5s  EN %-6s  %s' % (rid, disp, sid, res[3], res[4], res[5], res[7]))
    forms = {'report': ('report', 'レポート'), 'object': ('object', 'オブジェクト')}
    for rid in sorted(NOT_CONSUMED, key=int):
        if ids is None or rid in ids:
            disp, form = NOT_CONSUMED[rid]
            k = rowidx.get(rid)
            cells = lines[k].split('\t') if k else []
            bad = ('row missing' if not cells else
                   'form is %s' % cells[head.index('形式')] if cells[head.index('形式')] not in forms[form] else
                   'displayed No. is %s' % cells[head.index('表示')] if cells[head.index('表示')] != str(disp) else
                   'dispatched by 0000001E' if rid in d_orig or rid in d_work else '')
            if bad:
                failures.append('%s: not-consumed check: %s' % (rid, bad))
            results.append([rid, str(disp), '-', cells[col] if cells else '', '', '', 'not consumed (%s)' % form,
                            'UNRESOLVED: %s' % (bad or 'not consumed (no reader of 文字数 for this form), left as is')])
    if write and changed:
        Path(table).write_bytes(nl.join(lines).encode('utf-8'))
    if write:
        Path(jp_store).parent.mkdir(parents=True, exist_ok=True)
        disp_of = {r: str(REFS[r][0]) for r in REFS}
        Path(jp_store).write_bytes(''.join('%s\t%s\t%d\n' % (r, disp_of.get(r, ''), v)
                                           for r, v in sorted(store.items(), key=lambda x: int(x[0]))).encode('utf-8'))
    if report:
        Path(report).write_text('ID\tdisp\tlsb\tstored_jp\tjp\ten\tproof\tstatus\n'
                                + ''.join('\t'.join(r) + '\n' for r in results), encoding='utf-8', newline='\n')
    ok = sum(1 for r in results if r[7].startswith(('DONE', 'DRY')))
    refused = sum(1 for r in results if r[2] != '-' and r[7].startswith('UNRESOLVED'))
    print('%s: %d rows %s (%d cells %s), %d refused, %d not consumed' % (
        'WRITE' if write else 'DRY RUN', ok, 'written' if write else 'would be written', changed,
        'changed' if write else 'would change', refused, sum(1 for r in results if r[2] == '-')))
    for f in failures:
        print('  FAIL', f)
    return results, failures


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true', help='write the table and the JP store (default: dry run)')
    ap.add_argument('--table', type=Path, default=TABLE)
    ap.add_argument('--jp-store', type=Path, default=JP_STORE)
    ap.add_argument('--extract-dir', type=Path, default=EXTRACT)
    ap.add_argument('--ids', help='comma-separated reference IDs (default: all)')
    ap.add_argument('--report', type=Path, help='write a per-row TSV report here')
    a = ap.parse_args(argv)
    ids = set(a.ids.split(',')) if a.ids else None
    try:
        _, failures = run(a.table, a.jp_store, a.extract_dir, a.write, ids, a.report)
    except Refused as e:
        print('REFUSED:', e)
        return 2
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
