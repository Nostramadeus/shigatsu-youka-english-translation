"""R1 2026-09-26: encyclopedia names are printed from the display column 表示名, the key column stays Japanese.
See patch/dispcol.py. Run by tools/compile_en.sh (or directly: IN.lsb OUT.lsb; idempotent)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispcol import run
SITES = [
    (79, 'Calc', '出来事名', '表示名'),
]
run(SITES, 'fix-00001FBE')
