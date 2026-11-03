"""R1 2026-09-26: encyclopedia names are printed from the display column 表示名, the key column stays Japanese.
See patch/dispcol.py. Run by tools/compile_en.sh (or directly: IN.lsb OUT.lsb; idempotent).
Lane 1 2026-11-03 (friend report item 6): the unlock-list Caption idx 135 prints a person's English name from
tsv-en/人物名簿.tsv 表示名 (dispcol.person_caption)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dispcol import run, person_caption
SITES = [
    (90, 'Calc', '出来事名', '表示名'),
]
run(SITES, 'fix-000019DD', extra=person_caption(135, 'fix-000019DD'))
