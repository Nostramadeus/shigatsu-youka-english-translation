"""Set PR_FONTCHANGEABLED on every MesNew (message box) command in an LSB.

pylivemaker's docs: LiveMaker renders Latin text with a fixed advance unless
PR_FONTCHANGEABLED is 0 for the message box type. `lmlsb edit <file> <index>` does this
interactively, one command at a time; this does all of them in one pass with the same
logic as livemaker/cli/lmlsb.py:_edit_component.

    uv run --no-project --with pylivemaker python set_fontchangeabled.py \
        ../../orig/メッセージボックス作成.lsb work/loose/メッセージボックス作成.lsb 0
"""

import sys
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeData, OpeDataType, Param, ParamType

KEY = "PR_FONTCHANGEABLED"


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    want = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    lsb = LMScript.from_file(str(src))
    changed = 0
    for cmd in lsb.commands:
        if cmd.type.name != "MesNew":
            continue
        try:
            parser = cmd[KEY]
        except Exception:
            continue
        if parser.entries:
            op = parser.entries[0].operands[-1]
            print("  line %-5s current=%r -> %d" % (cmd.LineNo, op.value, want))
            op.value = want
        else:
            print("  line %-5s (empty) -> %d" % (cmd.LineNo, want))
            parser.entries.append(
                OpeData(type=OpeDataType.To, name="____arg",
                        operands=[Param(want, ParamType.Flag)])
            )
        changed += 1

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(lsb.to_lsb())
    print("set %s=%d on %d MesNew commands" % (KEY, want, changed))
    print("wrote %s (%d bytes, orig %d)" % (dst, dst.stat().st_size, src.stat().st_size))


if __name__ == "__main__":
    main()
