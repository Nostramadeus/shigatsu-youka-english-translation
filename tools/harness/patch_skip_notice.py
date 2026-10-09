"""TEST BUILD ONLY: boot straight into a chosen scene, skipping every mouse-only gate.

WHY: the 11 notice items (`了承する`), the title menu (`タイトル開始`) and the scenario
navigator map are LiveMaker `ImgNew` image objects driven by mouse handlers. None of them
answer a posted key or a posted mouse message, so an off-screen harness cannot pass them.

ADDRESSING: LabelReference.Label is a 0-BASED COMMAND INDEX into the target page's
command list, NOT a LineNo and NOT a label id. (Verified 2026-09-25: every
`PCReset Page=<f> Label=<n>` in the dispatcher lands on cmds[n] == a `Label` command
followed by `Call <self>:1` and `Jump <scene>.lsb:0`.) Earlier versions of this script
picked numbers off the dump's LineNo column and happened to work; this one resolves every
address by index and finds its edit sites by structure instead of by number.

WHAT IT EDITS
  000000F2.lsb  the three boot-dispatcher Jumps, identified by their current targets
                (000000F2.lsb:286 = autosave check, :432 = notice items, :66 = title)
                -> 0000001C.lsb : index of `Call メッセージボックス作成.lsb "(標準)"`
  0000001C.lsb  the first Jump after that Call (it normally continues into the navigator)
                -> <scene>.lsb : 0

Net effect: boot -> build the standard message box -> the chosen scene.

*** NEVER SHIP THESE TWO FILES IN THE DISTRIBUTED PATCH. ***
They remove the author's copyright / content notices, which the game requires players to
accept once, and they bypass the scenario navigator. Harness-only.
"""

import sys
from pathlib import Path

from livemaker.lsb import LMScript

SCENE = sys.argv[1] if len(sys.argv) > 1 else "00000024"
ORIG = Path("../../orig")
OUT = Path("work/loose")

def ref(c):
    try:
        r = c.get("Page")
    except Exception:
        return None
    return r if r is not None and hasattr(r, "Page") else None

# ---- 0000001C.lsb: find the standard-message-box Call, retarget the Jump after it ----
nav = LMScript.from_file(str(ORIG / "0000001C.lsb"))
cmds = nav.commands
call_idx = None
for i, c in enumerate(cmds):
    r = ref(c)
    if c.type.name == "Call" and r is not None and str(r.Page).startswith("メッセージボックス作成"):
        call_idx = i
        break
if call_idx is None:
    sys.exit("could not find the message box Call in 0000001C.lsb")
jump_idx = None
for i in range(call_idx + 1, call_idx + 12):
    if cmds[i].type.name == "Jump" and ref(cmds[i]) is not None:
        jump_idx = i
        break
if jump_idx is None:
    sys.exit("no Jump after the message box Call")
r = ref(cmds[jump_idx])
print("0000001C.lsb  box Call at index %d (LineNo %d)" % (call_idx, cmds[call_idx].LineNo))
print("0000001C.lsb  index %d (LineNo %d)  %s:%s -> %s.lsb:0"
      % (jump_idx, cmds[jump_idx].LineNo, r.Page, r.Label, SCENE))
r.Page, r.Label = SCENE + ".lsb", 0
(OUT / "0000001C.lsb").parent.mkdir(parents=True, exist_ok=True)
(OUT / "0000001C.lsb").write_bytes(nav.to_lsb())

# ---- 000000F2.lsb: retarget the three boot-dispatcher jumps ----
boot = LMScript.from_file(str(ORIG / "000000F2.lsb"))
want = {286, 432, 66}
hits = 0
for i, c in enumerate(boot.commands):
    r = ref(c)
    if c.type.name != "Jump" or r is None:
        continue
    if str(r.Page) != "000000F2.lsb" or r.Label not in want:
        continue
    print("000000F2.lsb  index %d (LineNo %d)  000000F2.lsb:%s -> 0000001C.lsb:%d"
          % (i, c.LineNo, r.Label, call_idx))
    r.Page, r.Label = "0000001C.lsb", call_idx
    hits += 1
if hits < 3:
    sys.exit("expected at least 3 dispatcher jumps, patched %d" % hits)
(OUT / "000000F2.lsb").write_bytes(boot.to_lsb())
print("wrote work/loose/000000F2.lsb and work/loose/0000001C.lsb; scene = %s" % SCENE)
