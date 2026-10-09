"""Assemble the playable English game folder and (optionally) the patch zip for friends.

    uv run tools/build_en_folder.py            # sync F:/4gatsu_8ka_EN from work/ per tools/ship-list.txt
    uv run tools/build_en_folder.py --zip      # also write patch/shigatsu-youka-en-patch-YYYY-MM-DD.zip

The EN folder holds a HARD LINK of the 1 GB exe (same bytes as the original folder, zero extra disk),
live.dll, Readme.txt, and the translated loose files. LiveMaker loads loose files next to the exe in their
archive-relative path and they override the archive, so nothing is patched into the exe (see tools/harness/README).
The folder keeps its own save.dat, separate from the Japanese install.

Safety: never copies the harness skip files (0000001C.lsb, or a 000000F2.lsb identical to the harness skip build);
never touches the exe, live.dll, Readme.txt, save.dat, SS/. Stale .lsb / .tsv files that are no longer in the
ship list are removed from the EN folder so it always equals work/ + ship-list.
"""
import hashlib
import os
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / 'work'
EN_DIR = Path(os.environ.get('SY_EN_DIR', 'F:/4gatsu_8ka_EN'))
JP_DIR = Path('F:/4gatsu_8ka_Ver2.0.0.4')
SHIP_LIST = ROOT / 'tools' / 'ship-list.txt'
SKIP_F2 = ROOT / 'tools' / 'harness' / 'work' / 'loose' / '000000F2.lsb'
SKIP_1C = ROOT / 'tools' / 'harness' / 'work' / 'loose' / '0000001C.lsb'
NEVER = set()  # the harness skip builds are refused by HASH (below), so a translated 0000001C / 000000F2 can ship
KEEP = {'live.dll', 'Readme.txt', 'save.dat', 'SS', 'README-EN.txt'}


def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def ship_entries():
    out = []
    for line in SHIP_LIST.read_text(encoding='utf-8').splitlines():
        line = line.split('#')[0].strip()
        if line:
            out.append(line.replace('\\', '/'))
    return out


def main(argv):
    exes = sorted(EN_DIR.glob('*.exe'))
    if not exes:
        sys.exit(f'{EN_DIR} has no exe. Create it once with: cd {EN_DIR} && ln "<JP exe>" . (hard link)')
    skip_hashes = {p.name: md5(p) for p in (SKIP_F2, SKIP_1C) if p.exists()}
    shipped, pending = [], []
    for rel in ship_entries():
        name = Path(rel).name
        if name in NEVER:
            sys.exit(f'REFUSING to ship harness skip file {rel}')
        src = WORK / rel
        if not src.exists():
            pending.append(rel)
            continue
        if name in skip_hashes and md5(src) == skip_hashes[name]:
            sys.exit(f'REFUSING: work/{name} is the harness skip build (notices/navigator bypassed). Recompile it from lns-en.')
        dst = EN_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists() or md5(dst) != md5(src):
            shutil.copyfile(src, dst)
            print('updated ', rel)
        shipped.append(rel)
    # remove stale loose files
    want = set(shipped)
    for p in list(EN_DIR.rglob('*.lsb')) + list(EN_DIR.rglob('*.tsv')):
        rel = p.relative_to(EN_DIR).as_posix()
        if rel not in want:
            p.unlink()
            print('removed stale', rel)
    readme = ROOT / 'patch' / 'README-EN.txt'
    if readme.exists():
        shutil.copyfile(readme, EN_DIR / 'README-EN.txt')
    print(f'EN folder: {len(shipped)} files shipped, {len(pending)} pending: {pending}')
    if '--zip' in argv:
        out = ROOT / 'patch' / f'shigatsu-youka-en-patch-{date.today().isoformat()}.zip'
        out.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for rel in shipped:
                z.write(WORK / rel, rel)
            for extra in ('README-EN.txt', 'README-BEFORE-PLAYING.txt', 'Play (fullscreen).cmd'):
                f = ROOT / 'patch' / extra
                if f.exists():
                    z.write(f, extra)
        print('zip:', out, out.stat().st_size, 'bytes')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
