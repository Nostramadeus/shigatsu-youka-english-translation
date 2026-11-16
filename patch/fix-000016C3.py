"""Structural fix for work/000016C3.lsb (reference-unlocked popup), run by tools/apply_labels.sh after the label map and
patch/props-000016C3.tsv (bug 2026-11-16).

    uv run --no-project --with pylivemaker python patch/fix-000016C3.py IN.lsb OUT.lsb

Cause: patch-2026-11-03 moved the popup's resting x 610 -> 570 (props-000016C3.tsv, PropMotion Value idx 374/397/420),
but idx 460 `Exit Calc=GetProp(@Sender, 3) != 610` still tests the old x, so a click on the resting popup does nothing.
Fix: that one literal 610 -> 570. The retreat tests in 00001F8A (idx 105/110/115) get the same change in fix-00001F8A.py.

The expression must be exactly the original or the fixed one (idempotent); anything else and the script refuses to
write. Checks: patch/exprfix.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript  # noqa: E402
import exprfix as xf  # noqa: E402
from exprfix import I, V  # noqa: E402

X_OLD, X_NEW = 610, 570
SITES = [  # (idx, command, property, original expression)
    (460, 'Exit', 'Calc', [  # Exit GetProp(@Sender, 3) != 610
        (11, '____0', 'GetProp', [V('@Sender'), I(3)]), (20, '____1', None, [V('____0'), I(X_OLD)]),
        (1, '____arg', None, [V('____1')])]),
]

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
if len(s.commands) != 502:
    sys.exit('fix-000016C3: %d commands, expected 502 (not 000016C3, or its structure changed)' % len(s.commands))
done, already = xf.apply_sites(
    s, [(i, kind, key, shape, xf.const_fixed(shape, {('____1', 1): (X_OLD, X_NEW)}), None)
        for i, kind, key, shape in SITES], 'fix-000016C3')
print('fix-000016C3: reference popup click test resting x %d -> %d, %d expression (%d rewritten, %d already fixed)'
      % (X_OLD, X_NEW, len(SITES), done, already))
open(dst, 'wb').write(s.to_lsb())
