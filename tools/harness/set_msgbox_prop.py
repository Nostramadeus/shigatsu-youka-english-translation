"""Set a property on every MesNew (message box) command in an LSB.

Same logic as livemaker/cli/lmlsb.py:_edit_component, but scripted, because this game
has 13 MesNew commands in メッセージボックス作成.lsb (one per font-size / font-face option)
and `lmlsb edit` only does one at a time, interactively.

    # the half-width switch the pylivemaker docs talk about (already 0 in this game)
    python set_msgbox_prop.py IN.lsb OUT.lsb PR_FONTCHANGEABLED 0

    # the setting that actually controls Latin spacing here: the font face
    python set_msgbox_prop.py IN.lsb OUT.lsb PR_FONTNAME "ＭＳ Ｐ明朝"
"""

import sys
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeData, OpeDataType, Param, ParamType


def main():
    src, dst, key, raw = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]

    lsb = LMScript.from_file(str(src))
    changed = 0
    for cmd in lsb.commands:
        if cmd.type.name != "MesNew":
            continue
        try:
            parser = cmd[key]
        except Exception:
            continue
        if parser.entries:
            op = parser.entries[0].operands[-1]
            value = int(raw) if isinstance(op.value, int) else raw
            print("  line %-5s %r -> %r" % (cmd.LineNo, op.value, value))
            op.value = value
        else:
            print("  line %-5s (empty) -> %r" % (cmd.LineNo, raw))
            parser.entries.append(
                OpeData(type=OpeDataType.To, name="____arg",
                        operands=[Param(int(raw), ParamType.Flag)])
            )
        changed += 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(lsb.to_lsb())
    print("set %s on %d MesNew commands" % (key, changed))
    print("wrote %s (%d bytes, orig %d)" % (dst, dst.stat().st_size, src.stat().st_size))


if __name__ == "__main__":
    main()
