"""State-test runner for Shigatsu Youka (LiveMaker 3): set state, call a routine, read state back.

No clicks, no screenshots. The game boots OFF-SCREEN and MUTED in a test folder built from HARD LINKS
of game/<build>/, runs an injected block appended to 000000F2.lsb (see inject.py), writes save.dat
with GameSave, quits, and the values are read out of save.dat.

  # one run
  run_state_test.py --build en --set st173=5 --set st32=0 --call 0000001C.lsb:00002413 \
      --dump "st32,st173,裏ルート変数[158],裏ルート変数[173],裏ルート解禁"
  # any save.dat, no game launch
  run_state_test.py --read-save F:/path/save.dat --dump "st32,裏ルート変数[173]"
  # boot from a given save.dat instead of a fresh game (2026-11-16, rk119 fix P5); --init none = no init Calls
  run_state_test.py --build en --start-save runs/<run>/save.dat --init none --call 00001F85.lsb:1 --dump rk119
  # a plan of cases on several builds, one table, stop at the first JP/EN difference
  run_state_test.py --plan plans/issue8.tsv --builds jp,en

Run with (no python on PATH):
  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --python 3.12 --with pywin32 --with pycaw \
      --with pillow --with comtypes --with pylivemaker python run_state_test.py ...

Safety (owner rules): window parked at (-32000,-32000) by a 10 ms poll thread started before the
process, SW_SHOWNOACTIVATE, never focused; the game's own audio session muted (pycaw, never the
master volume); one game process at a time (refuses to start if one is running); hard timeout;
kill + tasklist check in `finally`; every injected file removed and the hard links restored.
Never writes into a hard-linked file: a link is deleted first, then a new file is created.
"""
import argparse
import ctypes
import os
import random
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import savelib  # noqa: E402

ROOT = HERE.parents[2]
GAME = ROOT / "game"
TESTROOT = ROOT / "work" / "state-test"
RUNS = TESTROOT / "runs"
SKIP_TOP = {"save.dat", "SS", "jp-sightings"}
CREATE_NO_WINDOW = 0x08000000
OFF_X = OFF_Y = -32000
DIALOG_CLASSES = {"#32770", "TMessageForm"}


# ------------------------------------------------------------------ test folder (hard links)

def guard(path, build):
    """Every write/delete must be inside work/state-test/<build>/."""
    p = Path(os.path.abspath(path))
    base = Path(os.path.abspath(TESTROOT / build))
    if base != p and base not in p.parents:
        raise SystemExit("REFUSED: %s is outside %s" % (p, base))
    return p


def source_files(build):
    src = GAME / build
    out = {}
    for dirpath, dirnames, filenames in os.walk(src):
        rel = Path(dirpath).relative_to(src)
        if rel == Path("."):
            dirnames[:] = [d for d in dirnames if d not in SKIP_TOP]
            filenames = [f for f in filenames if f not in SKIP_TOP]
        for f in filenames:
            out[str(rel / f) if str(rel) != "." else f] = Path(dirpath) / f
    return out


def same_file(a, b):
    try:
        sa, sb = os.stat(a), os.stat(b)
    except OSError:
        return False
    return (sa.st_dev, sa.st_ino) == (sb.st_dev, sb.st_ino)


def sync_folder(build, log):
    """Make work/state-test/<build>/ = hard links of game/<build>/ (minus save.dat, SS/, jp-sightings/)."""
    dst = TESTROOT / build
    dst.mkdir(parents=True, exist_ok=True)
    src = source_files(build)
    made = fixed = removed = 0
    for rel, s in src.items():
        d = guard(dst / rel, build)
        if d.exists() and same_file(s, d):
            continue
        if d.exists():
            os.remove(d)          # stale or injected: remove the NAME only, never write into it
            fixed += 1
        else:
            made += 1
        d.parent.mkdir(parents=True, exist_ok=True)
        os.link(s, d)
    for dirpath, dirnames, filenames in os.walk(dst, topdown=False):
        for f in filenames:
            p = Path(dirpath) / f
            rel = str(p.relative_to(dst))
            if rel not in src:
                os.remove(guard(p, build))
                removed += 1
        if Path(dirpath) != dst and not os.listdir(dirpath):
            os.rmdir(guard(dirpath, build))
    bad = [r for r, s in src.items() if not same_file(s, dst / r)]
    log("sync %s: %d files, %d linked, %d relinked, %d extra removed, %d not hard-linked"
        % (build, len(src), made, fixed, removed, len(bad)))
    if bad:
        raise SystemExit("hard-link check failed for %s" % bad[:5])
    return dst


# ------------------------------------------------------------------ processes

def oem_decode(b):
    try:
        return b.decode("cp%d" % ctypes.windll.kernel32.GetOEMCP())
    except Exception:
        return b.decode("utf-8", "replace")


def tasklist_rows(filt):
    r = subprocess.run(["tasklist", "/FI", filt, "/FO", "CSV", "/NH"], capture_output=True,
                       creationflags=CREATE_NO_WINDOW)
    return [ln for ln in oem_decode(r.stdout).splitlines() if ln.startswith('"')]


def game_exe(folder):
    exes = sorted(Path(folder).glob("*.exe"))
    if len(exes) != 1:
        raise SystemExit("expected one .exe in %s, found %s" % (folder, exes))
    return exes[0]


def free_ram_gb():
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = MS()
    m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2 ** 30


class Parker(threading.Thread):
    """Every 10 ms: park every top-level window of the pid off-screen (never activates it)."""
    daemon = True

    def __init__(self, pid_box, stop):
        super().__init__()
        self.pid_box, self.stop, self.seen, self.log, self.gone = pid_box, stop, {}, [], set()
        self.t0 = time.time()

    def run(self):
        import win32con
        import win32gui
        import win32process
        flags = win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER
        while not self.stop.is_set():
            pid = self.pid_box.get("pid")
            if pid:
                found = []

                def cb(h, _):
                    try:
                        if win32process.GetWindowThreadProcessId(h)[1] == pid:
                            found.append(h)
                    except Exception:
                        pass
                    return True
                try:
                    win32gui.EnumWindows(cb, None)
                except Exception:
                    pass
                for h in list(self.seen):
                    if h not in self.gone and not win32gui.IsWindow(h):
                        self.gone.add(h)
                        self.log.append("%6.1fs window %s class=%s closed"
                                        % (time.time() - self.t0, h, self.seen[h]))
                for h in found:
                    try:
                        rect = win32gui.GetWindowRect(h)
                        if h not in self.seen:
                            cls = win32gui.GetClassName(h)
                            self.seen[h] = cls
                            self.log.append("%6.1fs window %s class=%s title=%r rect=%s"
                                            % (time.time() - self.t0, h, cls, win32gui.GetWindowText(h), rect))
                        if rect[0] > OFF_X + 1000:
                            win32gui.SetWindowPos(h, 0, OFF_X, OFF_Y, 0, 0, flags)
                    except Exception:
                        pass
            time.sleep(0.01)

    def dialogs(self):
        import win32gui
        out = []
        for h, cls in list(self.seen.items()):
            if cls in DIALOG_CLASSES:
                texts = []

                def cb(c, _):
                    try:
                        t = win32gui.GetWindowText(c)
                        if t:
                            texts.append(t)
                    except Exception:
                        pass
                    return True
                try:
                    win32gui.EnumChildWindows(h, cb, None)
                    texts.insert(0, win32gui.GetWindowText(h))
                except Exception:
                    pass
                out.append("%s: %s" % (cls, " | ".join(texts)))
        return out


def mute_pid(pid, result, timeout=60.0):
    """Mute only this pid's audio session (never the master volume)."""
    import comtypes
    from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
    deadline = time.time() + timeout
    comtypes.CoInitialize()
    while time.time() < deadline and not result.get("stop"):
        try:
            for s in AudioUtilities.GetAllSessions():
                if s.ProcessId == pid:
                    v = s._ctl.QueryInterface(ISimpleAudioVolume)
                    v.SetMute(1, None)
                    v.SetMasterVolume(0.0, None)
                    result["muted_at"] = time.time()
                    return
        except Exception:
            pass
        time.sleep(0.1)


def temp_litter():
    t = Path(os.environ.get("TEMP", ""))
    return {p for pat in ("fon*.tmp", "~lv*.wmv") for p in t.glob(pat)}


# ------------------------------------------------------------------ one run

def step_of(save, nonce):
    """This run's step number from a decoded save, or None if the save is not from this run."""
    import inject
    hit = save.lookup(inject.MARK, inject.CAPTION)
    if not (hit and hit[3] and hit[3][0] == nonce):
        return None
    st = save.lookup(inject.STEP, inject.CAPTION)
    return st[3][0] if st and st[3] else None


def run_one(build, sets, call, dump, init, timeout, label, trace=False, pause_ms=0, start_save=None):
    import inject
    stamp = time.strftime("%Y%m%d-%H%M%S")
    rundir = RUNS / ("%s-%s-%s" % (stamp, build, label))
    rundir.mkdir(parents=True, exist_ok=True)
    lines = []

    def log(msg):
        lines.append(msg)
        print("  [%s] %s" % (build, msg), file=sys.stderr, flush=True)

    folder = sync_folder(build, log)
    exe = game_exe(folder)
    running = tasklist_rows("IMAGENAME eq %s" % exe.name)
    if running:
        raise SystemExit("REFUSED: a game process is already running (maybe the owner's): %s" % running)
    log("free RAM %.1f GB" % free_ram_gb())

    nonce = random.randint(1, 2 ** 31 - 2)
    boot_name = "000000F2.lsb"
    boot_src = (GAME / build / boot_name) if (GAME / build / boot_name).exists() else inject.ORIG / boot_name
    data, listing = inject.build(folder, boot_src, sets, call, nonce, init, trace, pause_ms, bool(start_save))
    log("boot source %s; marker %s=%d" % (boot_src, inject.MARK, nonce))
    for ln in listing:
        log(ln)

    injected = guard(folder / boot_name, build)
    save = guard(folder / "save.dat", build)
    litter0 = temp_litter()
    proc = None
    stop = threading.Event()
    mres = {}
    result = None
    try:
        if injected.exists():
            os.remove(injected)                 # delete the hard link first ...
        with open(injected, "xb") as f:         # ... then create a NEW file (never write through a link)
            f.write(data)
        if save.exists():
            os.remove(save)                     # fresh game: no save.dat
        if start_save:                          # --start-save: boot from a copy (a NEW file, never a link)
            shutil.copyfile(start_save, save)
            log("start save %s -> %s (%d bytes)" % (start_save, save, save.stat().st_size))
        pid_box = {}
        parker = Parker(pid_box, stop)
        parker.start()
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 4                      # SW_SHOWNOACTIVATE (never minimized: see harness README)
        t0 = time.time()
        proc = subprocess.Popen([str(exe)], cwd=str(folder), startupinfo=si,
                                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        pid_box["pid"] = proc.pid
        threading.Thread(target=mute_pid, args=(proc.pid, mres), daemon=True).start()
        log("launched pid %d" % proc.pid)
        last_mtime = save.stat().st_mtime if start_save else None   # the start save is not a result
        while time.time() - t0 < timeout:
            if proc.poll() is not None:
                log("game exited by itself after %.1fs (code %s)" % (time.time() - t0, proc.returncode))
                break
            dl = parker.dialogs()
            if dl:
                log("DIALOG: %s" % dl)
                break
            if save.exists():
                m = save.stat().st_mtime
                if m != last_mtime:
                    last_mtime = m
                    try:
                        s = savelib.Save(save)
                        stp = step_of(s, nonce)
                        if stp is not None and stp != inject.DONE:
                            log("save.dat at %.1fs: step %d" % (time.time() - t0, stp))
                        elif stp == inject.DONE:
                            log("save.dat at %.1fs: step %d = routine returned; waiting for Terminate"
                                % (time.time() - t0, stp))
                            end = time.time() + 15
                            while time.time() < end and proc.poll() is None:
                                time.sleep(0.5)
                            log("game %s" % ("exited" if proc.poll() is not None else "still running -> kill"))
                            break
                        else:
                            log("save.dat written at %.1fs without this run's marker (engine autosave)"
                                % (time.time() - t0))
                    except Exception as ex:
                        log("save.dat not readable yet (%s)" % ex)
            time.sleep(1.0)
        else:
            log("TIMEOUT after %ds" % timeout)
        if mres.get("muted_at"):
            log("audio session muted %.1fs after launch" % (mres["muted_at"] - t0))
        else:
            log("no audio session seen (nothing to mute)")
        for w in parker.log:
            log(w)
        if save.exists():
            shutil.copy2(save, rundir / "save.dat")
            s = savelib.Save(rundir / "save.dat")
            stp = step_of(s, nonce)
            if stp == inject.DONE:
                result = savelib.read_values(s, dump, inject.CAPTION)
                log("save.dat %d bytes, marker OK, step %d (routine returned)" % (s.size, stp))
            elif stp is not None:
                log("FAILED after step %d (0 = block reached; see the step list above)" % stp)
            else:
                log("save.dat has no marker %d -> the injected block never saved (not reached, or its "
                    "first GameSave failed; rerun with --trace)" % nonce)
    finally:
        mres["stop"] = True
        if proc is not None:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True,
                           creationflags=CREATE_NO_WINDOW)
            time.sleep(1.5)
            stop.set()
            left_pid = tasklist_rows("PID eq %d" % proc.pid)
            left_img = tasklist_rows("IMAGENAME eq %s" % exe.name)
            log("tasklist after kill: pid %d %s; image name: %s"
                % (proc.pid, "STILL RUNNING" if left_pid else "CLEAN",
                   "%d process(es) LEFT" % len(left_img) if left_img else "CLEAN"))
        stop.set()
        if injected.exists():
            os.remove(injected)
        if save.exists():
            os.remove(save)
        sync_folder(build, log)                 # restores the 000000F2 hard link (EN), drops SS/ etc.
        new_litter = temp_litter() - litter0
        for p in new_litter:
            try:
                p.unlink()
            except OSError:
                pass
        log("removed %d engine temp files (fon*.tmp, ~lv*.wmv) created by this run" % len(new_litter))
        (rundir / "run.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if result is None:
        raise RuntimeError("no values: see %s" % (rundir / "run.log"))
    (rundir / "result.tsv").write_text("".join("%s\t%s\n" % (n, v) for n, v, _ in result), encoding="utf-8")
    return result, rundir


# ------------------------------------------------------------------ CLI

def read_plan(path):
    rows = []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        c = ln.split("\t")
        if c[0] == "test":
            continue
        c += [""] * (5 - len(c))
        rows.append(dict(test=c[0], sets=savelib.split_top(c[1], ";"), call=c[2],
                         dump=savelib.split_top(c[3]), expect=savelib.split_top(c[4])))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", choices=["jp", "en"])
    ap.add_argument("--set", action="append", default=[], help="NAME=INT, NAME[i]=INT or NAME=\"str\"; repeat or ';'-separate")
    ap.add_argument("--call", help="PAGE.lsb:LABELNAME or PAGE.lsb:INDEX, e.g. 0000001C.lsb:00002413")
    ap.add_argument("--dump", help="comma list: st32,裏ルート変数[158],...")
    ap.add_argument("--init", help="comma list of PAGE:LABEL to Call first (default %s)" % ",".join(
        ["0000001C.lsb:000024C7", "00001F85.lsb:00001F86"]))
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--label", default="run")
    ap.add_argument("--read-save", help="decode this save.dat only; no game launch")
    ap.add_argument("--where", action="store_true", help="add a column: status or slot the value came from")
    ap.add_argument("--plan", help="TSV: test, set (;-list), call, dump (,-list), expect (,-list, - = none)")
    ap.add_argument("--builds", default="jp,en")
    ap.add_argument("--no-stop-on-diff", action="store_true")
    ap.add_argument("--trace", action="store_true", help="GameSave after every step (debug a run that fails)")
    ap.add_argument("--pause-ms", type=int, default=0, help="debug: Wait this long before every block command")
    ap.add_argument("--start-save", help="boot from a copy of this save.dat instead of a fresh game (single runs)")
    a = ap.parse_args()

    if a.read_save:
        s = savelib.Save(a.read_save)
        for n, v, w in savelib.read_values(s, savelib.split_top(a.dump or "")):
            print("%s\t%s%s" % (n, v, "\t" + w if a.where else ""))
        return

    init = [] if a.init == "none" else (savelib.split_top(a.init) if a.init else None)
    if a.plan:
        builds = [b.strip() for b in a.builds.split(",") if b.strip()]
        table = [("test", "build", "name", "value", "expected", "ok")]
        stopped = None
        for case in read_plan(a.plan):
            got = {}
            for b in builds:
                print("== %s on %s" % (case["test"], b), file=sys.stderr, flush=True)
                res, rundir = run_one(b, case["sets"], case["call"], case["dump"], init, a.timeout,
                                      case["test"], a.trace)
                got[b] = {n: v for n, v, _ in res}
                for k, (n, v, _) in enumerate(res):
                    exp = case["expect"][k] if k < len(case["expect"]) else "-"
                    ok = "-" if exp == "-" else ("yes" if v == exp else "NO")
                    table.append((case["test"], b, n, v, exp, ok))
                table.append(("", b, "(run folder)", str(rundir), "", ""))
            diff = [n for n in case["dump"] if len({got[b].get(n) for b in builds}) > 1]
            if diff:
                stopped = "%s: builds differ on %s" % (case["test"], ", ".join(diff))
                if not a.no_stop_on_diff:
                    break
        for r in table:
            print("\t".join(r))
        print("RESULT\t%s" % (stopped or "no difference between builds"))
        return

    if not (a.build and a.call and a.dump):
        ap.error("--build, --call and --dump are required (or use --read-save / --plan)")
    sets = [x for s in a.set for x in savelib.split_top(s, ";")]
    res, rundir = run_one(a.build, sets, a.call, savelib.split_top(a.dump), init, a.timeout, a.label, a.trace, a.pause_ms,
                         a.start_save)
    for n, v, w in res:
        print("%s\t%s%s" % (n, v, "\t" + w if a.where else ""))
    print("# run folder: %s" % rundir, file=sys.stderr)


if __name__ == "__main__":
    main()
