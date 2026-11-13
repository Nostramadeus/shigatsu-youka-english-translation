"""Lane X4 2026-11-13 (Fix 1, see patch/pointmul.py): the scenario-end reward at idx 2327
    書簡残ポイント = 書簡残ポイント + 文字数誤差 * DBGetFloat("ポイント倍率")
reads the whole-number column instead:  + 文字数誤差 * DBGetInt("ポイント倍率100") / 100.
Run by tools/apply_labels.sh after the label map (or directly: IN.lsb OUT.lsb; checks the site, idempotent)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript  # noqa: E402
import exprfix as xf  # noqa: E402
import pointmul  # noqa: E402

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
pointmul.apply(s, [(2327, xf.V('文字数誤差'), '書簡残ポイント')], 'fix-000015DC')
open(dst, 'wb').write(s.to_lsb())
