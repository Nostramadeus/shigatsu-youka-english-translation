"""Shoot one PNG per text advance, for the side-by-side review page.

Launches the game off-screen and muted, walks the recorded boot navigation, then takes
one screenshot per advance into <out>/001.png, 002.png, ... and kills the process.

    uv run --no-project --with pywin32 --with pycaw --with pillow --with comtypes \
        python shoot_lines.py --advances 40 --out shots/chapter1

REQUIRES A TEST BUILD: run patch_skip_notice.py first and copy work/loose/000000F2.lsb
and work/loose/0000001C.lsb next to the exe. Without them the game stops at the title /
notice screen, whose image buttons answer to no posted input at all.

The screenshots are of the 960x540 TBasePanel, i.e. the game picture with no window
chrome, so they can go straight into an <img> in the review page.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import run_game as R

# Recorded 2026-09-25. A TEST BUILD (see patch_skip_notice.py) boots straight into the
# opening scene, so the only navigation left is waiting out the fades and CG waits that
# auto-advance on their own. 23 no-input steps at --delay 1.4 lands on the first text line.
NAV = "none*23"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--advances", type=int, default=40, help="how many advances to shoot")
    p.add_argument("--mode", default="enter",
                   help="VK_RETURN advances text. space TOGGLES the box, click does nothing.")
    p.add_argument("--nav", default=NAV, help="boot navigation script")
    p.add_argument("--delay", type=float, default=1.3, help="seconds between advances")
    p.add_argument("--warmup", type=float, default=25.0,
                   help="seconds before the first prompt is up (intro video)")
    p.add_argument("--out", default="shots/lines")
    p.add_argument("--keep-nav-shots", action="store_true",
                   help="also keep the navigation screenshots (nav-000.png ...)")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    proc, parker, stop, _ = R.launch()
    print("launched pid=%d" % proc.pid)
    try:
        panel = R.wait_for_window(proc.pid, 30)
        if not panel:
            print("no window appeared in 30 s")
            return
        print("muted:", R.mute_pid(proc.pid, 30))
        time.sleep(args.warmup)

        panel = R.main_window(proc.pid) or panel
        print("render surface %s client=%s" % (panel, R._client_area(panel)))

        nav_dir = out if args.keep_nav_shots else out / "_nav"
        R.do_steps(panel, proc.pid, R.parse_script(args.nav, 480, 270),
                   nav_dir, args.delay, prefix="nav-%03d", method="pwtop")

        panel = R.main_window(proc.pid) or panel
        steps = [(args.mode, 480, 270)] * args.advances
        R.do_steps(panel, proc.pid, steps, out, args.delay,
                   start_index=1, prefix="%03d", method="pwtop")
        print("wrote %d shots to %s" % (args.advances, out))
    finally:
        stop.set()
        R.kill(proc)


if __name__ == "__main__":
    main()
