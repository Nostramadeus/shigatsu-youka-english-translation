"""Lane X4 2026-11-13 (Fix 1, see patch/pointmul.py): the scenario-type reference reward at idx 37 / 39
    書簡残ポイント = 書簡残ポイント + 1000 * DBGetFloat("ポイント倍率")              (リファ文字数誤差 < 1000)
    書簡残ポイント = 書簡残ポイント + リファ文字数誤差 * DBGetFloat("ポイント倍率")   (else)
reads the whole-number column instead: 10 * DBGetInt("ポイント倍率100") and リファ文字数誤差 * DBGetInt("ポイント倍率100") / 100.
Run by tools/apply_labels.sh after the extra maps (or directly: IN.lsb OUT.lsb; checks both sites, idempotent)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript  # noqa: E402
import exprfix as xf  # noqa: E402
import pointmul  # noqa: E402

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
pointmul.apply(s, [(37, xf.I(1000), '書簡残ポイント'), (39, xf.V('リファ文字数誤差'), '書簡残ポイント')], 'fix-00001A13')
open(dst, 'wb').write(s.to_lsb())
