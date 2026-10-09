"""Find every LSB command that carries PR_FONTCHANGEABLED (the half-width switch).

pylivemaker's docs say: to stop LiveMaker rendering English as fixed-width, set
PR_FONTCHANGEABLED to 0 on the command that creates the message box. This scans all of
orig/ in one process (uvx per file would take ~20 min).
"""
import sys
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.core import PropertyType

TARGET = PropertyType.PR_FONTCHANGEABLED
root = Path(sys.argv[1] if len(sys.argv) > 1 else "orig")

hits = 0
for p in sorted(root.rglob("*.lsb")):
    try:
        lsb = LMScript.from_file(str(p))
    except Exception as e:
        print("SKIP %s (%s)" % (p, e))
        continue
    for index, cmd in enumerate(lsb.commands):
        try:
            items = list(cmd.items())
        except Exception:
            continue
        for key, val in items:
            if key == "PR_FONTCHANGEABLED" or val is TARGET or (
                hasattr(val, "name") and getattr(val, "name", "") == "PR_FONTCHANGEABLED"
            ):
                print("%s  index=%d  type=%s  %s=%r" % (p, index, cmd.type.name, key, val))
                hits += 1
print("total hits:", hits)
