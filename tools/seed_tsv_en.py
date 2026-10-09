"""Seed tsv-en/<name>.tsv as a UTF-8 copy of orig/データベース/<name>.tsv (agents edit UTF-8; build_tsv.py
writes CP932 back). Skips files that already exist in tsv-en/.
    uv run tools/seed_tsv_en.py 注意.tsv チュートリアル.tsv
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for name in sys.argv[1:]:
    dst = ROOT / 'tsv-en' / name
    if dst.exists():
        print('exists', dst)
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes((ROOT / 'orig' / 'データベース' / name).read_bytes().decode('cp932').encode('utf-8'))
    print('seeded', dst)
