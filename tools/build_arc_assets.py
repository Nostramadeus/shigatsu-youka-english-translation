"""Copy the per-arc assets whose FILE NAME the scripts build out of the arc-name variable.

    uv run --no-project --python 3.12 python tools/build_arc_assets.py

`0000001C` indices 2366 / 2388 and `00001F8A` indices 40 / 69 build a path out of ナビ編名, which is
the 解禁編 column and is now English:

    Cinema … "グラフィック\\インターフェース\\" ++ ナビ編名 ++ "テキストウェイト.lcm"
    Cinema … "グラフィック\\インターフェース\\" ++ ナビ編名 ++ "テキストウェイト2.lcm"

so the archive's 呪殺編テキストウェイト.lcm is no longer the name the engine asks for. Same class as
Q2370's リファレンス icons: the picture is provided again under the English value name, contents
untouched (a hard copy of the original bytes, no re-render).

Driven by patch/hen-jp-en.tsv, so it stays correct when an arc rendering changes. Prints one line per
copy; exits 1 if an arc in the map has no source file (that would be a silent missing animation).

T1 2026-09-26 (O-74a rename): two more path families built from an arc value, same fix (bytes untouched).
Their sources are the image lane's archive extracts under work/images/gal/ (not in orig/); a missing
source is NOT fatal there, because the Japanese game lacks the same file (永劫回帰編 has no such logo):

    00001878 idx 1875  ImgNew 事典編 … "グラフィック\メニュー\右クリック\" ++ 事典編 ++ "ロゴ.gal"
        事典編 = @Sender (idx 2031) = the arc-logo object's NAME, which the hen map made English.
    0000227A idx 194/268  SetProp("編名" ++ スロット, 2, "グラフィック\システム\セーブロード\編ロゴ\"
        ++ セーブ内容[スロット - 1][1] ++ "ロゴ.gal")  (save-slot arc logo; the JP files are named
        <arc>ロゴ.gal, so column 1 is an arc name; which variable fills it was not traced, the copies are
        harmless if the engine never asks for them).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'orig' / 'グラフィック' / 'インターフェース'
DST = ROOT / 'work' / 'グラフィック' / 'インターフェース'
MAP = ROOT / 'patch' / 'hen-jp-en.tsv'
SUFFIXES = ['テキストウェイト.lcm', 'テキストウェイト2.lcm']


EXTRA = [  # (source dir, destination dir, suffix) ; missing source allowed
    (ROOT / 'work' / 'images' / 'gal' / 'グラフィック' / 'メニュー' / '右クリック',
     ROOT / 'work' / 'グラフィック' / 'メニュー' / '右クリック', 'ロゴ.gal'),
    (ROOT / 'work' / 'images' / 'gal' / 'グラフィック' / 'システム' / 'セーブロード' / '編ロゴ',
     ROOT / 'work' / 'グラフィック' / 'システム' / 'セーブロード' / '編ロゴ', 'ロゴ.gal'),
]


def copy(s, d):
    if not d.exists() or d.read_bytes() != s.read_bytes():
        shutil.copyfile(s, d)
        print('copied  %s -> %s' % (s.name, d.relative_to(ROOT / 'work')))


def main():
    pairs = []
    for line in MAP.read_text(encoding='utf-8').splitlines():
        if line.startswith('#') or '	' not in line:
            continue
        jp, en = line.split('	')[:2]
        pairs.append((jp.strip(), en.strip()))
    DST.mkdir(parents=True, exist_ok=True)
    missing, n = [], 0
    for jp, en in pairs:
        for suf in SUFFIXES:
            s, d = SRC / (jp + suf), DST / (en + suf)
            if not s.exists():
                missing.append(s.name)
                continue
            copy(s, d)
            n += 1
    absent = []
    for src, dst, suf in EXTRA:
        dst.mkdir(parents=True, exist_ok=True)
        for jp, en in pairs:
            s = src / (jp + suf)
            if not s.exists():
                absent.append(str(s.relative_to(ROOT / 'work' / 'images' / 'gal')))
                continue
            copy(s, dst / (en + suf))
            n += 1
    print('build_arc_assets: %d files in place for %d arcs' % (n, len(pairs)))
    if absent:
        print('no source (JP game lacks it too, not an error):', absent)
    if missing:
        print('MISSING sources:', missing)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
