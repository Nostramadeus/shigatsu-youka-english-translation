"""Try every PostMessage input variant against the game and report which one moves it.

Launches once, off-screen and muted, then for each variant: screenshot, post the input,
wait, screenshot again, compare. Prints CHANGED or same. Nothing here uses SendInput or
SetForegroundWindow - if every variant says "same", PostMessage cannot drive this engine.

    uv run --no-project --with pywin32 --with pycaw --with pillow --with comtypes \
        python probe_input.py --warmup 25
"""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

import win32con
import win32gui

import run_game as R


def sha(path):
    return hashlib.md5(Path(path).read_bytes()).hexdigest()[:10]


def variants(panel, top, px, py):
    """(label, callable) pairs. px/py are TBasePanel client coords."""
    fx, fy = px, py
    dx, dy = R.panel_offset(panel)
    formx, formy = px + dx, py + dy

    def click(h, x, y):
        def go():
            lp = win32gui.PostMessage
            lparam = (y << 16) | (x & 0xFFFF)
            lp(h, win32con.WM_MOUSEMOVE, 0, lparam)
            time.sleep(0.05)
            lp(h, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(0.08)
            lp(h, win32con.WM_LBUTTONUP, 0, lparam)
        return go

    def dbl(h, x, y):
        def go():
            lparam = (y << 16) | (x & 0xFFFF)
            win32gui.PostMessage(h, win32con.WM_LBUTTONDBLCLK, win32con.MK_LBUTTON, lparam)
            time.sleep(0.05)
            win32gui.PostMessage(h, win32con.WM_LBUTTONUP, 0, lparam)
        return go

    def key(h, vk):
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    def char(h, c):
        def go():
            win32gui.PostMessage(h, win32con.WM_CHAR, c, 0)
        return go

    return [
        ("click panel(%d,%d)" % (fx, fy), click(panel, fx, fy)),
        ("click form(%d,%d)" % (formx, formy), click(top, formx, formy)),
        ("dblclick panel", dbl(panel, fx, fy)),
        ("dblclick form", dbl(top, formx, formy)),
        ("VK_RETURN -> form", key(top, win32con.VK_RETURN)),
        ("VK_RETURN -> panel", key(panel, win32con.VK_RETURN)),
        ("VK_SPACE -> form", key(top, win32con.VK_SPACE)),
        ("VK_SPACE -> panel", key(panel, win32con.VK_SPACE)),
        ("VK_DOWN -> form", key(top, win32con.VK_DOWN)),
        ("VK_DOWN -> panel", key(panel, win32con.VK_DOWN)),
        ("VK_CONTROL -> form", key(top, win32con.VK_CONTROL)),
        ("WM_CHAR CR -> form", char(top, 13)),
        ("WM_CHAR SP -> form", char(top, 32)),
        ("click panel centre", click(panel, 480, 270)),
        ("click form centre", click(top, 480, 293)),
    ]


def confirm_variants(panel, top, px, py):
    """VK_DOWN is known to move the menu selection. Find what CONFIRMS it.

    Run this after a menu is on screen. px/py should be the centre of a menu row.
    """
    dx, dy = R.panel_offset(panel)

    def key(h, vk):
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    def click(h, x, y):
        def go():
            lparam = (y << 16) | (x & 0xFFFF)
            win32gui.PostMessage(h, win32con.WM_MOUSEMOVE, 0, lparam)
            time.sleep(0.06)
            win32gui.PostMessage(h, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_LBUTTONUP, 0, lparam)
        return go

    return [
        ("VK_DOWN (select row 2)", key(top, win32con.VK_DOWN)),
        ("hover form row2", click(top, px + dx, py + dy)),
        ("VK_RETURN -> form", key(top, win32con.VK_RETURN)),
        ("VK_RETURN -> panel", key(panel, win32con.VK_RETURN)),
        ("VK_SPACE -> form", key(top, win32con.VK_SPACE)),
        ("Z -> form", key(top, 0x5A)),
        ("VK_RIGHT -> form", key(top, win32con.VK_RIGHT)),
        ("VK_EXECUTE -> form", key(top, 0x2B)),
        ("click form row2 again", click(top, px + dx, py + dy)),
        ("click panel row2", click(panel, px, py)),
        ("VK_UP -> form", key(top, win32con.VK_UP)),
        ("VK_RETURN -> form #2", key(top, win32con.VK_RETURN)),
    ]


def keys_variants(panel, top, px, py):
    """Broad sweep: which key or click does ANYTHING on the current screen."""
    dx, dy = R.panel_offset(panel)

    def key(h, vk, name):
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    def click(h, x, y):
        def go():
            lparam = (y << 16) | (x & 0xFFFF)
            win32gui.PostMessage(h, win32con.WM_MOUSEMOVE, 0, lparam)
            time.sleep(0.06)
            win32gui.PostMessage(h, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_LBUTTONUP, 0, lparam)
        return go

    named = [
        ("TAB", win32con.VK_TAB), ("RIGHT", win32con.VK_RIGHT),
        ("LEFT", win32con.VK_LEFT), ("DOWN", win32con.VK_DOWN),
        ("UP", win32con.VK_UP), ("RETURN", win32con.VK_RETURN),
        ("SPACE", win32con.VK_SPACE), ("Z", 0x5A), ("X", 0x58),
        ("ESCAPE", win32con.VK_ESCAPE), ("HOME", win32con.VK_HOME),
        ("NEXT", win32con.VK_NEXT),
    ]
    out = [("%s -> form" % n, key(top, vk, n)) for n, vk in named]
    out += [
        ("click btn1 form(305,473)", click(top, 305, 450 + dy)),
        ("click btn2 form(630,473)", click(top, 630, 450 + dy)),
        ("click btn1 panel(305,450)", click(panel, 305, 450)),
        ("RETURN -> form (after clicks)", key(top, win32con.VK_RETURN, "RETURN")),
    ]
    return out


def sweep_variants(panel, top, px, py):
    """Every plausible key, one at a time. The FIRST 'CHANGED' is the attributable one."""
    def key(h, vk):
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    keys = []
    for n in range(1, 13):
        keys.append(("F%d" % n, 0x70 + n - 1))
    for c in "0123456789":
        keys.append((c, ord(c)))
    for c in "ZXCVABSMNOPQ":
        keys.append((c, ord(c)))
    keys += [
        ("BACK", win32con.VK_BACK), ("INSERT", win32con.VK_INSERT),
        ("DELETE", win32con.VK_DELETE), ("END", win32con.VK_END),
        ("PRIOR", win32con.VK_PRIOR), ("SHIFT", win32con.VK_SHIFT),
        ("CONTROL", win32con.VK_CONTROL), ("MENU", win32con.VK_MENU),
        ("NUMPAD_ENTER", 0x0D), ("APPS", 0x5D),
    ]
    return [("%s -> form" % n, key(top, vk)) for n, vk in keys]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--set", default="all", choices=("all", "confirm", "keys", "sweep", "advance"))
    p.add_argument("--nav", default=None,
                   help="run_game script to run before probing (gets to the right screen)")
    p.add_argument("--warmup", type=float, default=25.0)
    p.add_argument("--settle", type=float, default=1.6)
    p.add_argument("--x", type=int, default=480, help="panel-x of the hotspot to click")
    p.add_argument("--y", type=int, default=327, help="panel-y of the hotspot to click")
    p.add_argument("--out", default="shots/probe")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    proc, parker, stop, _ = R.launch()
    print("launched pid=%d" % proc.pid)
    try:
        panel = R.wait_for_window(proc.pid, 30)
        if not panel:
            print("no window")
            return
        print("muted:", R.mute_pid(proc.pid, 30))
        time.sleep(args.warmup)

        panel = R.main_window(proc.pid) or panel
        top = R.top_window(proc.pid)
        print("panel=%s top=%s offset=%s client=%s"
              % (panel, top, R.panel_offset(panel), win32gui.GetClientRect(panel)))

        base = out / "before-000.png"
        R.capture(panel, base, "pwtop")
        prev = sha(base)
        print("baseline %s" % prev)

        if args.nav:
            steps = R.parse_script(args.nav, 480, 270)
            print("nav: %d steps" % len(steps))
            R.do_steps(panel, proc.pid, steps, out, args.settle,
                       prefix="nav-%03d", method="pwtop")
            panel = R.main_window(proc.pid) or panel
            top = R.top_window(proc.pid)
            R.capture(panel, base, "pwtop")
            prev = sha(base)
            print("post-nav baseline %s" % prev)

        sets = {"all": variants, "confirm": confirm_variants, "keys": keys_variants,
                "sweep": sweep_variants, "advance": advance_variants}
        for i, (label, fn) in enumerate(sets[args.set](panel, top, args.x, args.y)):
            fn()
            time.sleep(args.settle)
            panel = R.main_window(proc.pid) or panel
            shot = out / ("%02d.png" % i)
            R.capture(panel, shot, "pwtop")
            h = sha(shot)
            print("  %-28s %s  %s" % (label, h, "CHANGED" if h != prev else "same"))
            prev = h
    finally:
        stop.set()
        R.kill(proc)




def advance_variants(panel, top, px, py):
    """4b: what advances scene text? Five presses of each input, one shot per press."""
    dx, dy = R.panel_offset(panel)

    def key(h, vk):
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    def hold(h, vk, secs=1.2):
        """VK_CONTROL held down = LiveMaker's skip mode."""
        def go():
            win32gui.PostMessage(h, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(secs)
            win32gui.PostMessage(h, win32con.WM_KEYUP, vk, 0)
        return go

    def click(h, x, y):
        def go():
            lparam = (y << 16) | (x & 0xFFFF)
            win32gui.PostMessage(h, win32con.WM_MOUSEMOVE, 0, lparam)
            time.sleep(0.06)
            win32gui.PostMessage(h, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            time.sleep(0.08)
            win32gui.PostMessage(h, win32con.WM_LBUTTONUP, 0, lparam)
        return go

    out = []
    for n in range(5):
        out.append(("RETURN #%d" % (n + 1), key(top, win32con.VK_RETURN)))
    for n in range(5):
        out.append(("SPACE #%d" % (n + 1), key(top, win32con.VK_SPACE)))
    for n in range(5):
        out.append(("DOWN #%d" % (n + 1), key(top, win32con.VK_DOWN)))
    for n in range(5):
        out.append(("CTRL held #%d" % (n + 1), hold(top, win32con.VK_CONTROL)))
    for n in range(5):
        out.append(("CLICK form #%d" % (n + 1), click(top, 480, 270 + dy)))
    return out


if __name__ == "__main__":
    main()
