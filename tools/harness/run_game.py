"""Launch the LiveMaker game off-screen, muted, and drive it with PostMessage only.

HARD RULES this script exists to enforce (the owner's machine rules):
  * the window NEVER appears on screen and NEVER takes focus
    -> it is moved to (-32000,-32000) by a poll thread that starts BEFORE the process does,
       always with SWP_NOACTIVATE, and it is never shown, restored or foregrounded.
  * audio is muted per-session via pycaw (the game's PID only, never the master volume)
  * the process is always killed at the end, and the kill is verified with tasklist.

Run it with:
    uv run --no-project --with pywin32 --with pycaw --with pillow --with comtypes \
        python run_game.py --advances 25 --out shots/run1

Screenshots are taken with PrintWindow(flag 2 = PW_RENDERFULLCONTENT), which works on an
off-screen window because it asks the window to draw into a memory DC.
"""

from __future__ import annotations

import os
import argparse
import ctypes
import subprocess
import threading
import time
from pathlib import Path

import win32api
import win32con
import win32gui
import win32process
import win32ui
from PIL import Image

GAME_DIR = Path(os.environ.get("SY_GAME_DIR", "F:/4gatsu_8ka_Ver2.0.0.4"))  # SY_GAME_DIR overrides (EN play folder)
# Glob rather than hardcode: the title contains a wide tilde that is easy to get wrong
# (U+FF5E vs U+301C) and the wrong codepoint gives a silent "file not found".
_EXES = sorted(GAME_DIR.glob("*.exe"))
GAME_EXE = _EXES[0] if _EXES else GAME_DIR / "missing.exe"

OFFSCREEN_X = -32000
OFFSCREEN_Y = -32000

user32 = ctypes.windll.user32


# --------------------------------------------------------------------------- windows

def windows_of_pid(pid):
    """Every top-level window owned by pid."""
    found = []

    def cb(hwnd, _):
        try:
            _, wpid = win32process.GetWindowThreadProcessId(hwnd)
        except Exception:
            return True
        if wpid == pid:
            found.append(hwnd)
        return True

    try:
        win32gui.EnumWindows(cb, None)
    except Exception:
        pass
    return found


def move_offscreen(hwnd):
    """Park a window far off the virtual desktop. Never activates it."""
    flags = (
        win32con.SWP_NOSIZE
        | win32con.SWP_NOZORDER
        | win32con.SWP_NOACTIVATE
        | win32con.SWP_NOOWNERZORDER
    )
    try:
        win32gui.SetWindowPos(hwnd, 0, OFFSCREEN_X, OFFSCREEN_Y, 0, 0, flags)
    except Exception:
        pass


class Parker(threading.Thread):
    """Polls every 10 ms and parks any window of the target pid off-screen."""

    daemon = True

    def __init__(self, pid_box, stop):
        super().__init__()
        self.pid_box = pid_box
        self.stop = stop
        self.seen = set()
        self.log = []
        self.t0 = time.time()

    def run(self):
        while not self.stop.is_set():
            pid = self.pid_box.get("pid")
            if pid:
                for hwnd in windows_of_pid(pid):
                    rect = None
                    try:
                        rect = win32gui.GetWindowRect(hwnd)
                    except Exception:
                        pass
                    if hwnd not in self.seen:
                        self.seen.add(hwnd)
                        title = ""
                        try:
                            title = win32gui.GetWindowText(hwnd)
                        except Exception:
                            pass
                        self.log.append(
                            (time.time() - self.t0, hwnd, "new %r %s" % (title, rect))
                        )
                    if rect and rect[0] > OFFSCREEN_X + 1000:
                        move_offscreen(hwnd)
            time.sleep(0.01)


def top_window(pid):
    """The game's top-level frame window.

    LiveMaker 3 is a Delphi app: the frame is 'TFormView'. Rank by CLIENT area, not
    window rect - 'TApplication' has a large rect but a 0x0 client area and would win.
    """
    best, best_area, best_pref = None, 0, -1
    for hwnd in windows_of_pid(pid):
        try:
            cls = win32gui.GetClassName(hwnd)
            l, t, r, b = win32gui.GetClientRect(hwnd)
        except Exception:
            continue
        area = (r - l) * (b - t)
        if area <= 0:
            continue
        pref = 1 if cls == "TFormView" else 0
        if (pref, area) > (best_pref, best_area):
            best, best_area, best_pref = hwnd, area, pref
    return best


def main_window(pid):
    """The window the game actually DRAWS on: the 'TBasePanel' child of TFormView.

    This matters. Child windows are clipped out of the parent's DC, so capturing
    TFormView gives a blank white frame with the toolbar on top, no matter which
    capture method is used - that cost an hour. The panel is 960x540 (the frame's
    client area is 960x562 because of the 22 px TDock97 toolbar).
    """
    top = top_window(pid)
    if not top:
        return None
    found = []

    def cb(h, _):
        try:
            if win32gui.GetClassName(h) == "TBasePanel":
                found.append(h)
        except Exception:
            pass
        return True

    try:
        win32gui.EnumChildWindows(top, cb, None)
    except Exception:
        pass
    if not found:
        return top
    return max(found, key=lambda h: _client_area(h))


def panel_offset(panel):
    """Where the TBasePanel sits inside the TFormView's CLIENT area, in pixels.

    Input has to be PostMessage'd to the top-level TFormView, not to the panel - the
    engine's mouse handling lives on the form, and messages posted to the panel are
    simply ignored (that cost a run). Screenshots, on the other hand, are of the panel.
    So panel coordinates have to be shifted by this offset before they are posted.
    Currently (0, 23): the TDock97 toolbar is 23 px tall.
    """
    try:
        top = user32.GetAncestor(panel, GA_ROOT)
        pl, pt, _, _ = win32gui.GetWindowRect(panel)
        cx, cy = win32gui.ClientToScreen(top, (0, 0))
        return pl - cx, pt - cy
    except Exception:
        return 0, 23


def _client_area(h):
    try:
        l, t, r, b = win32gui.GetClientRect(h)
        return (r - l) * (b - t)
    except Exception:
        return 0


def describe_windows(pid):
    out = []
    for hwnd in windows_of_pid(pid):
        try:
            out.append(
                "hwnd=%s vis=%s icon=%s title=%r class=%r rect=%s client=%s"
                % (
                    hwnd,
                    win32gui.IsWindowVisible(hwnd),
                    win32gui.IsIconic(hwnd),
                    win32gui.GetWindowText(hwnd),
                    win32gui.GetClassName(hwnd),
                    win32gui.GetWindowRect(hwnd),
                    win32gui.GetClientRect(hwnd),
                )
            )
        except Exception as e:
            out.append("hwnd=%s <%s>" % (hwnd, e))
    return out


# --------------------------------------------------------------------------- audio

def mute_pid(pid, timeout=30.0):
    """Mute only this pid's audio session. Never touches the master volume."""
    import comtypes
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            comtypes.CoInitialize()
            for session in AudioUtilities.GetAllSessions():
                if session.ProcessId == pid:
                    vol = session._ctl.QueryInterface(ISimpleAudioVolume)
                    vol.SetMute(1, None)
                    vol.SetMasterVolume(0.0, None)
                    return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


# --------------------------------------------------------------------------- capture

CAPTURE_METHODS = ("pwtop", "pw2", "pw0", "pw3", "bitblt")
GA_ROOT = 2


def capture_via_top(panel, path):
    """THE method that works on this game. Everything else gives a frozen blank frame.

    PrintWindow has to be called on the TOP-LEVEL window (TFormView) with flag 0: that is
    what makes the engine repaint its back buffer into the DC, children included. Calling
    it on the TBasePanel child, or BitBlt-ing any of them, returns whatever stale pixels
    the off-screen window happens to hold - usually plain white.

    So: print the whole frame into a window-sized bitmap, then crop out the TBasePanel
    rectangle (drops the title bar, the border and the 22 px toolbar).
    """
    src = mem = bmp = dc = None
    try:
        top = user32.GetAncestor(panel, GA_ROOT)
        wl, wt, wr, wb = win32gui.GetWindowRect(top)
        W, H = wr - wl, wb - wt
        pl, pt, pr, pb = win32gui.GetWindowRect(panel)
        if W <= 0 or H <= 0:
            return None
        dc = win32gui.GetWindowDC(top)
        src = win32ui.CreateDCFromHandle(dc)
        mem = src.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(src, W, H)
        mem.SelectObject(bmp)
        user32.PrintWindow(top, mem.GetSafeHdc(), 0)
        info = bmp.GetInfo()
        bits = bmp.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB", (info["bmWidth"], info["bmHeight"]), bits, "raw", "BGRX", 0, 1
        )
        img = img.crop((pl - wl, pt - wt, pr - wl, pb - wt))
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, optimize=True)
        return img.size
    except Exception as e:
        print("  capture failed (pwtop): %s" % e)
        return None
    finally:
        try:
            if bmp is not None:
                win32gui.DeleteObject(bmp.GetHandle())
            if mem is not None:
                mem.DeleteDC()
            if src is not None:
                src.DeleteDC()
            if dc:
                win32gui.ReleaseDC(top, dc)
        except Exception:
            pass


def capture(hwnd, path, method="pw2"):
    """Grab the window into a PNG. Returns (w, h) or None.

    Methods, in the order they were tried on this game:
      pw2     PrintWindow(PW_RENDERFULLCONTENT) - asks the window to repaint into a DC
      pw0     PrintWindow(0)                    - same, without the full-content flag
      pw3     PrintWindow(PW_CLIENTONLY|PW_RENDERFULLCONTENT)
      bitblt  BitBlt from GetWindowDC           - reads the window's existing pixels,
              which under DWM exist even for a window parked off-screen
    """
    if method == "pwtop":
        return capture_via_top(hwnd, path)
    src = mem = bmp = hwnd_dc = None
    try:
        l, t, r, b = win32gui.GetClientRect(hwnd)
        w, h = r - l, b - t
        if w <= 0 or h <= 0:
            return None
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        src = win32ui.CreateDCFromHandle(hwnd_dc)
        mem = src.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(src, w, h)
        mem.SelectObject(bmp)
        if method == "bitblt":
            # window DC origin is the window rect; offset to the client area
            wl, wt, _, _ = win32gui.GetWindowRect(hwnd)
            cl_x, cl_y = win32gui.ClientToScreen(hwnd, (0, 0))
            mem.BitBlt((0, 0), (w, h), src, (cl_x - wl, cl_y - wt), win32con.SRCCOPY)
        else:
            flag = {"pw2": 2, "pw0": 0, "pw3": 3}[method]
            user32.PrintWindow(hwnd, mem.GetSafeHdc(), flag)
        info = bmp.GetInfo()
        bits = bmp.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB", (info["bmWidth"], info["bmHeight"]), bits, "raw", "BGRX", 0, 1
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, optimize=True)
        return (w, h)
    except Exception as e:
        print("  capture failed (%s): %s" % (method, e))
        return None
    finally:
        try:
            if bmp is not None:
                win32gui.DeleteObject(bmp.GetHandle())
            if mem is not None:
                mem.DeleteDC()
            if src is not None:
                src.DeleteDC()
            if hwnd_dc:
                win32gui.ReleaseDC(hwnd, hwnd_dc)
        except Exception:
            pass


# --------------------------------------------------------------------------- input

def post_click(hwnd, x, y):
    lp = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lp)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lp)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lp)


def post_key(hwnd, vk):
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, 0)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk, 0)


VKS = {
    "enter": win32con.VK_RETURN,
    "space": win32con.VK_SPACE,
    "down": win32con.VK_DOWN,
    "up": win32con.VK_UP,
    "esc": win32con.VK_ESCAPE,
    "ctrl": win32con.VK_CONTROL,
    "z": 0x5A,
}


def advance(hwnd, mode, x, y):
    if mode == "click":
        post_click(hwnd, x, y)
    elif mode in VKS:
        post_key(hwnd, VKS[mode])
    elif mode == "all":
        post_click(hwnd, x, y)
        time.sleep(0.1)
        post_key(hwnd, win32con.VK_RETURN)
        time.sleep(0.1)
        post_key(hwnd, win32con.VK_SPACE)
    elif mode in ("wheelup", "wheeldown"):
        # FIX1 2026-09-26: posted wheel (delta +-120 in the high word of wParam; lParam = coords)
        delta = 120 if mode == "wheelup" else -120
        win32gui.PostMessage(hwnd, 0x020A, (delta & 0xFFFF) << 16, win32api.MAKELONG(x, y))
    elif mode == "rclick":
        lp = win32api.MAKELONG(x, y)
        win32gui.PostMessage(hwnd, win32con.WM_MOUSEMOVE, 0, lp)
        win32gui.PostMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lp)
        time.sleep(0.05)
        win32gui.PostMessage(hwnd, win32con.WM_RBUTTONUP, 0, lp)
    elif mode == "none":
        pass
    else:
        raise SystemExit("unknown advance mode %s" % mode)


# --------------------------------------------------------------------------- run

def launch():
    """Start the parker thread first, then the game, so the window is parked instantly."""
    stop = threading.Event()
    pid_box = {}
    parker = Parker(pid_box, stop)
    parker.start()

    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # SW_SHOWNOACTIVATE. Do NOT use SW_SHOWMINNOACTIVE here: a minimized window renders
    # nothing, so every screenshot comes out black. The parker thread is what keeps the
    # window off the owner's screen; this flag only stops it grabbing focus.
    si.wShowWindow = 4

    proc = subprocess.Popen(
        [str(GAME_EXE)],
        cwd=str(GAME_DIR),
        startupinfo=si,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )
    pid_box["pid"] = proc.pid
    return proc, parker, stop, pid_box


def kill(proc):
    subprocess.run(
        ["taskkill", "/PID", str(proc.pid), "/F", "/T"], capture_output=True, text=True
    )
    time.sleep(1.0)
    out = subprocess.run(
        ["tasklist", "/FI", "PID eq %d" % proc.pid], capture_output=True, text=True
    ).stdout
    print("tasklist after kill:", "CLEAN" if str(proc.pid) not in out else "STILL RUNNING")


def wait_for_window(pid, timeout=30.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        hwnd = main_window(pid)
        if hwnd:
            l, t, r, b = win32gui.GetClientRect(hwnd)
            if (r - l) > 100 and (b - t) > 100:
                return hwnd
        time.sleep(0.05)
    return main_window(pid)


def do_steps(hwnd, pid, steps, out, delay, start_index=0, prefix="%03d", method="pw2"):
    """steps = list of (mode, x, y). One PNG per step, taken BEFORE the step."""
    i = start_index
    for mode, x, y in steps:
        for h in windows_of_pid(pid):
            try:
                if win32gui.GetWindowRect(h)[0] > OFFSCREEN_X + 1000:
                    move_offscreen(h)
            except Exception:
                pass
        cur = main_window(pid) or hwnd
        shot = out / ((prefix % i) + ".png")
        size = capture(cur, shot, method)
        top = user32.GetAncestor(cur, GA_ROOT) or cur
        dx, dy = panel_offset(cur)
        print("  %s %s panel(%d,%d)->form(%d,%d) -> %s"
              % (shot.name, mode, x, y, x + dx, y + dy, size))
        advance(top, mode, x + dx, y + dy)
        time.sleep(delay)
        i += 1
    return i


def parse_script(text, cx, cy):
    """'click:480,327*2; none*5; enter' -> [(mode, x, y), ...]

    Coordinates are CLIENT coordinates of the TBasePanel render surface (960x540).
    Omit the coordinates to use the default (the centre, or --x/--y).
    """
    steps = []
    for part in text.split(";"):
        part = part.strip()
        if not part:
            continue
        count = 1
        if "*" in part:
            part, n = part.rsplit("*", 1)
            count = int(n)
        if ":" in part:
            mode, coords = part.split(":", 1)
            x, y = (int(v) for v in coords.split(","))
        else:
            mode, x, y = part, cx, cy
        steps.extend([(mode.strip(), x, y)] * count)
    return steps


def run(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    proc, parker, stop, pid_box = launch()
    print("launched pid=%d" % proc.pid)
    try:
        hwnd = wait_for_window(proc.pid, 30)
        if not hwnd:
            print("no window appeared in 30 s")
            return
        for line in describe_windows(proc.pid):
            print(" ", line)

        print("muted:", mute_pid(proc.pid, timeout=args.mute_timeout))
        time.sleep(args.warmup)

        hwnd = main_window(proc.pid) or hwnd
        cl = win32gui.GetClientRect(hwnd)
        cx = args.x if args.x is not None else (cl[2] - cl[0]) // 2
        cy = args.y if args.y is not None else (cl[3] - cl[1]) // 2
        print(
            "client=%s advance mode=%s at (%d,%d) x%d"
            % (cl, args.mode, cx, cy, args.advances)
        )

        if args.tree:
            # dump every top-level window and its children, and try to capture each one
            # that is big enough to be a render surface
            for top in windows_of_pid(proc.pid):
                kids = []

                def kid_cb(h, _):
                    kids.append(h)
                    return True

                try:
                    win32gui.EnumChildWindows(top, kid_cb, None)
                except Exception:
                    pass
                for h in [top] + kids:
                    try:
                        cls = win32gui.GetClassName(h)
                        cr = win32gui.GetClientRect(h)
                        wr = win32gui.GetWindowRect(h)
                    except Exception:
                        continue
                    tag = "top" if h == top else "kid"
                    print("  %s hwnd=%s cls=%r client=%s rect=%s" % (tag, h, cls, cr, wr))
                    if cr[2] > 100 and cr[3] > 100:
                        for m in CAPTURE_METHODS:
                            capture(h, out / ("tree-%s-%s-%s.png" % (tag, h, m)), m)
            return

        if args.captest:
            # one shot per capture method, so we can see which one is not black
            for m in CAPTURE_METHODS:
                print("  captest %s -> %s" % (m, capture(hwnd, out / ("captest-%s.png" % m), m)))
            return

        if args.script:
            steps = parse_script(args.script, cx, cy)
            print("script: %d steps" % len(steps))
        else:
            steps = [(args.mode, cx, cy)] * args.advances
        n = do_steps(hwnd, proc.pid, steps, out, args.delay, method=args.capture)
        capture(main_window(proc.pid) or hwnd, out / ("%03d.png" % n), args.capture)

        print("window event log:")
        for t, h, msg in parker.log:
            print("  +%5.2fs hwnd=%s %s" % (t, h, msg))
    finally:
        stop.set()
        kill(proc)


def parse(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--advances", type=int, default=20, help="how many advances (= shots)")
    p.add_argument(
        "--mode", default="click", help="click | enter | space | down | up | esc | ctrl | z | all | none"
    )
    p.add_argument("--x", type=int, default=None, help="click X in CLIENT coords (default centre)")
    p.add_argument("--y", type=int, default=None, help="click Y in CLIENT coords (default centre)")
    p.add_argument("--delay", type=float, default=0.8, help="seconds between advances")
    p.add_argument("--warmup", type=float, default=6.0, help="seconds to wait after launch")
    p.add_argument("--mute-timeout", type=float, default=30.0)
    p.add_argument("--out", default="shots/run", help="output folder for the PNGs")
    p.add_argument("--capture", default="pwtop", choices=CAPTURE_METHODS,
                   help="how to grab the window (see capture() docstring)")
    p.add_argument("--captest", action="store_true",
                   help="take one shot with every capture method, then quit")
    p.add_argument("--script", default=None,
                   help="step script, e.g. 'none*3; click:480,327; click*20'. Overrides --advances")
    p.add_argument("--tree", action="store_true",
                   help="dump the whole window tree and capture every candidate surface")
    return p.parse_args(argv)


if __name__ == "__main__":
    run(parse())
