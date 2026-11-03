"""R1 2026-09-26: encyclopedia names are printed from the display column 表示名, the key column stays Japanese.
See patch/dispcol.py. Run by tools/compile_en.sh (or directly: IN.lsb OUT.lsb; idempotent).

Game follow-up r2 2026-10-30 (same write, patch/exprfix.py checks): the length bar of a scenario-type reference
(idx 372/373, the "start this reference?" panel) was scaled for Japanese reference lengths:
    width  選択文字数バー 5      = 50000 / (200000 / リファレンス文字数)    (500 px at 2,000 characters)
    alpha  選択文字数バーアルファ 11 = 255 * リファレンス文字数 / 2000
English references run about 2.3x the Japanese length, so both get x2.5: 200000 -> 500000, 2000 -> 5000.
Each site must hold its original expression with the constant either the original or the fixed value."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispcol import run, key_at_dblocate, wrap_result
import exprfix as xf

SITES = [
    (2420, 'PR_TEXT', '出来事名', '表示名'),
    (2520, 'PR_TEXT', '出来事名', '表示名'),
]
BAR = [(5, '____1', None, [xf.I(200000), xf.V('リファレンス文字数')]), (4, '____3', None, [xf.I(500), xf.I(100)]),
       (5, '____4', None, [xf.V('____3'), xf.V('____1')]), (1, '____arg', None, [xf.V('____4')])]
ALPHA = [(4, '____0', None, [xf.I(255), xf.V('リファレンス文字数')]), (5, '____1', None, [xf.V('____0'), xf.I(2000)]),
         (1, '____arg', None, [xf.V('____1')])]
R2 = [
    (372, 'PropMotion', None, BAR, xf.const_fixed(BAR, {('____1', 0): (200000, 500000)}),
     xf.obj_is('"選択文字数バー"', '5')),
    (373, 'PropMotion', None, ALPHA, xf.const_fixed(ALPHA, {('____1', 1): (2000, 5000)}),
     xf.obj_is('"選択文字数バーアルファ"', '11')),
]


def r2(script):
    done, already = xf.apply_sites(script, R2, 'fix-0000001E')
    print('fix-0000001E: r2 reference length bar x2.5 at idx 372/373 (%d rewritten, %d already fixed)' % (done, already))
    # Lane 1 2026-11-03 (keyaudit2): C1 the reference viewer name (English, from リファレンスデータベース 閲覧人物) is
    # mapped back to the 人物名簿 key before DBLocate, so the viewer-name colour is found again (idx 609/610 detail
    # panel, 1567/1568 partial comment). C3 the "people unlocked" banner (idx 2437 DBGetActive(), idx 2531
    # データベース名 = the person table name, a key) prints the 人物名簿 表示名.
    key_at_dblocate([(609, 'Calc'), (610, 'Calc'), (1567, 'Calc'), (1568, 'Calc')], 'fix-0000001E')(script)
    wrap_result([(2437, 'PR_TEXT'), (2531, 'PR_TEXT')], 'fix-0000001E')(script)


run(SITES, 'fix-0000001E', extra=r2)
