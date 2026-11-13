"""Lane X4 2026-11-13 (Fix 1, see patch/pointmul.py): the chatter reward at idx 45
    書簡残ポイント = 書簡残ポイント + 500 * DBGetFloat("ポイント倍率")
reads the whole-number column instead:  + 5 * DBGetInt("ポイント倍率100").
Run by tools/apply_labels.sh after the label map (or directly: IN.lsb OUT.lsb; checks the site, idempotent)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from livemaker.lsb import LMScript  # noqa: E402
import exprfix as xf  # noqa: E402
import pointmul  # noqa: E402

src, dst = sys.argv[1], sys.argv[2]
s = LMScript.from_file(src)
pointmul.apply(s, [(45, xf.I(500), '書簡残ポイント')], 'fix-000018BF')
# Lane W 2026-11-14: two-line reply captions and their echo lines (patch/layoutw.py)
import layoutw  # noqa: E402
layoutw.fix_18bf(s)
open(dst, 'wb').write(s.to_lsb())
