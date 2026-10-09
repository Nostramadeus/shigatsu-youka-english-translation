"""List or set NON-STRING command properties (ints and flags) inside an LSB.

    uv run --no-project --with pylivemaker python tools/lsb_prop.py list IN.lsb [CMDTYPE ...]
    uv run --no-project --with pylivemaker python tools/lsb_prop.py apply IN.lsb OUT.lsb MAP.tsv

tools/lsb_strings.py handles string literals only. Some render defects are a numeric flag instead,
so they need this. MAP.tsv = `index<TAB>PROPERTY<TAB>old<TAB>new`, UTF-8, no header, # comments
allowed. `old` is checked against what is in the file (write `-` for "currently unset/empty"), so a
map cannot silently hit the wrong command after the script is re-extracted; `new` is written as an
int, or clears the property when it is `-`. Exit 1 if any row's index, property or old value does
not match. `list` prints index, LineNo, command type and every non-empty numeric property.

Why it exists (2026-09-26, UI lane): PR_FONTBORDER=1 on a MesNew makes LiveMaker draw that box's
text one character at a time on a FULL-WIDTH advance, so English comes out letter-spaced and takes
about twice the width. Clearing the flag restores proportional advance.

FIX1 2026-09-26 correction: the in-game test (work/_fix1/shots/compare_ABCD.png) shows the full-width advance
on 0000001C idx 1123 is cured by PR_FONTCHANGEABLED=0, not by PR_FONTBORDER (border 0 or unset stays wide).
A map row with old = `-` now SETS an unset property (needed: FONTCHANGEABLED is unset on most UI boxes).
"""
import sys
from pathlib import Path

from livemaker.lsb import LMScript

SKIP = ('type', 'LineNo', 'Indent', 'Mute', 'NotUpdate', 'components')
FLAG_PROPS = {'PR_FONTCHANGEABLED', 'PR_FONTBORDER', 'PR_FONTSHADOW', 'PR_VISIBLE', 'PR_ANTIALIAS', 'PR_PAUSED',
              'PR_TEXTPAUSED', 'PR_HANDLEKEY', 'PR_CAPTURELINK'}


def val(cmd, key):
    try:
        v = cmd[key]
    except Exception:
        return None
    return v


def as_text(v):
    if v is None:
        return '-'
    s = str(v)
    return s if s.strip() else '-'


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    mode = argv[0]
    lsb = LMScript.from_file(argv[1])
    if mode == 'list':
        want = set(argv[2:])
        for i, cmd in enumerate(lsb.commands):
            t = cmd.type.name
            if want and t not in want:
                continue
            keys = list(cmd.keys()) if hasattr(cmd, 'keys') else []
            shown = []
            for k in keys:
                if k in SKIP:
                    continue
                v = val(cmd, k)
                s = as_text(v)
                if s != '-' and not isinstance(v, str) and s.lstrip('-').isdigit():
                    shown.append('%s=%s' % (k, s))
            if shown:
                print('%d\t%d\t%s\t%s' % (i, cmd.LineNo, t, ' '.join(shown)))
        return 0
    if mode == 'apply':
        out, mapfile = Path(argv[1 + 1]), Path(argv[1 + 2])
        rows = []
        for line in mapfile.read_text(encoding='utf-8').splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            p = line.split('\t')
            rows.append((int(p[0]), p[1].strip(), p[2].strip(), p[3].strip()))
        bad = 0
        for idx, prop, old, new in rows:
            if idx >= len(lsb.commands):
                print('NO SUCH INDEX %d' % idx)
                bad += 1
                continue
            cmd = lsb.commands[idx]
            keys = list(cmd.keys()) if hasattr(cmd, 'keys') else []
            if prop not in keys:
                print('%d %s has no %s' % (idx, cmd.type.name, prop))
                bad += 1
                continue
            cur = as_text(val(cmd, prop))
            if cur != old:
                print('%d %s.%s is %r, map says %r' % (idx, cmd.type.name, prop, cur, old))
                bad += 1
                continue
            lp = val(cmd, prop)
            if new == '-':
                lp.entries = []                      # unset the property
            else:
                ents = getattr(lp, 'entries', None)
                if not ents:
                    # FIX1 2026-09-26: set a currently-unset property (old = '-'). Built as the compiler
                    # writes a literal argument: one To-op named ____arg holding one Param. Flags get
                    # ParamType.Flag (as on 0000001C idx 3859 PR_FONTCHANGEABLED), everything else Int.
                    from livemaker.lsb.core import OpeData, OpeDataType, Param, ParamType
                    ptype = ParamType.Flag if prop in FLAG_PROPS else ParamType.Int
                    lp.entries = [OpeData(type=OpeDataType.To, name='____arg',
                                          operands=[Param(value=int(new), type=ptype)])]
                else:
                    prm = ents[0].operands[0]            # same in-place mutation lsb_strings uses
                    prm.value = int(new)
            print('%d\t%s\t%s\t%s\t->\t%s' % (idx, cmd.type.name, prop, old, new))
        if bad:
            print('%d PROBLEMS, nothing written' % bad, file=sys.stderr)
            return 1
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(lsb.to_lsb())
        print('wrote %s (%d bytes, %d properties)' % (out, out.stat().st_size, len(rows)))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
