"""Reward points without a decimal multiplier (lane X4, 2026-11-13; used by patch/fix-0000001E.py, fix-000015DC.py,
fix-00001A13.py, fix-000018BF.py; checking and rewriting by patch/exprfix.py).

Twelve Calc commands add reward points as  P = P + X * DBGetFloat("ポイント倍率")  with the table 編 active. The column
holds texts such as "1.75" and "2.5". A player's save paid 0 for every reward of the "1.75" arc and the full amount for a
"2" arc: the best-supported cause is a Windows decimal symbol "," that makes the engine read "1.75" as 0 (not proven).
tsv-en/編.tsv now carries a whole-number column ポイント倍率100 (= ポイント倍率 x 100: 175 200 200 250 250 500 5000 500;
the old column stays). Each site becomes
    P = P + X * DBGetInt("ポイント倍率100") / 100      for a variable X (文字数誤差, リファ文字数誤差)
    P = P + 10 * DBGetInt("ポイント倍率100")           for X = 1000
    P = P +  5 * DBGetInt("ポイント倍率100")           for X = 500
"/" of two integers is an integer quotient in this engine (save data, lane D). Overflow: the largest English total any
X can reach is 206,123 (tsv-en/シナリオデータベース.tsv); 206,123 x 5000 = 1,030,615,000 < 2^31 - 1. Rounding: the new
form truncates; it equals the truncated old value for every X >= 0 and differs from a rounded old value by at most 1
point (work/feedback-20261113/x4/rounding.txt). DBGetInt on an untyped column is the author's own use (DBGetInt("ID")).
"""
import exprfix as xf

OLD_COL, NEW_COL = 'ポイント倍率', 'ポイント倍率100'


def orig_shape(x, lhs):
    """The original entry list of  lhs = lhs + x * DBGetFloat("ポイント倍率")  (x = an exprfix operand tuple)."""
    return [(1, '____0', None, [xf.S(OLD_COL)]),
            (11, '____1', 'DBGetFloat', [xf.V('____0')]),
            (4, '____2', None, [x, xf.V('____1')]),
            (2, '____3', None, [xf.V(lhs), xf.V('____2')]),
            (1, lhs, None, [xf.V('____3')])]


def fixed_shape(x, lhs):
    """The rewritten entry list (see the module docstring)."""
    head = [(1, '____0', None, [xf.S(NEW_COL)]),
            (11, '____1', 'DBGetInt', [xf.V('____0')])]
    if x in (xf.I(1000), xf.I(500)):
        return head + [(4, '____2', None, [xf.I(x[1] // 100), xf.V('____1')]),
                       (2, '____3', None, [xf.V(lhs), xf.V('____2')]),
                       (1, lhs, None, [xf.V('____3')])]
    if x[0] != xf.VAR:
        raise ValueError('X must be 1000, 500 or a variable: %r' % (x,))
    return head + [(4, '____2', None, [x, xf.V('____1')]),
                   (5, '____4', None, [xf.V('____2'), xf.I(100)]),
                   (2, '____3', None, [xf.V(lhs), xf.V('____4')]),
                   (1, lhs, None, [xf.V('____3')])]


def sites(spec):
    """spec = [(idx, X operand tuple, target variable)] -> exprfix.apply_sites rows (Calc commands)."""
    return [(i, 'Calc', None, orig_shape(x, lhs), fixed_shape(x, lhs), None) for i, x, lhs in spec]


def apply(script, spec, tag):
    done, already = xf.apply_sites(script, sites(spec), tag)
    print('%s: reward multiplier %s -> %s at %d sites (%d rewritten, %d already fixed)'
          % (tag, OLD_COL, NEW_COL, len(spec), done, already))
