"""Find every LSB command that references a given page (e.g. '00000024.lsb')."""
import sys
from pathlib import Path
from livemaker.lsb import LMScript

target = sys.argv[1]
root = Path(sys.argv[2] if len(sys.argv) > 2 else "orig")
for p in sorted(root.rglob("*.lsb")):
    try:
        lsb = LMScript.from_file(str(p))
    except Exception:
        continue
    for cmd in lsb.commands:
        s = ""
        try:
            s = str(cmd)
        except Exception:
            continue
        if target in s:
            print("%s  line=%s  %s  %s" % (p, cmd.LineNo, cmd.type.name, s[:160].replace("\n", " ")))
