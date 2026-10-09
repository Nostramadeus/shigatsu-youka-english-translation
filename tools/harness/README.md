# tools/harness - patch and screenshot the game without it appearing on screen

Built 2026-09-25. Drives `F:\4gatsu_8ka_Ver2.0.0.4\死月妖花～四月八日～.exe` (LiveMaker 3,
1 GB, whole game packed in the exe) off-screen, muted, with PostMessage only, and saves
PNGs of the game picture.

Read `PROGRESS.md` next to this file for the findings and the evidence. The short version:

1. **Loose files next to the exe override the archive.** Testing never needs `lmpatch`.
2. **The script format is CP932-only.** No macrons, no accented Latin, no U+2014 em dash.
3. **`PR_FONTCHANGEABLED` is already 0** on all 13 story message boxes. Nothing to change;
   the setting that does change Latin spacing is the font FACE.
4. **Every image button in this game ignores PostMessage** - notices, title, navigator map.
   A TEST-ONLY skip patch jumps over all three; see "Building a test build" below.
5. **`VK_RETURN` posted to the top-level `TFormView` advances scene text.** `VK_SPACE`
   toggles the message box. Clicks do nothing, anywhere.

## Running it

There is no python on PATH. Every command needs `uv run --no-project` plus the deps:

    cd <repo>/tools/harness
    UVRUN="uv run --no-project --python 3.12 --with pywin32 --with pycaw --with pillow --with comtypes"

### run_game.py - the general driver

    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 $UVRUN python run_game.py \
        --warmup 25 --delay 1.3 --script "none*2; down; down; enter" --out shots/run1

| flag | default | what |
|---|---|---|
| `--advances N` | 20 | how many advances (= how many PNGs), if `--script` is not used |
| `--mode M` | `click` | what each advance does: `click`, `enter`, `space`, `down`, `up`, `esc`, `ctrl`, `z`, `all`, `none` |
| `--script S` | - | step script, overrides `--advances`/`--mode`. `"none*2; down; enter; click:480,327"` - `;` separates, `*N` repeats, `:X,Y` gives panel coordinates |
| `--x N` `--y N` | centre | default click position, in TBasePanel client coordinates (960x540) |
| `--delay S` | 0.8 | seconds between advances |
| `--warmup S` | 6.0 | seconds after launch before the first shot. **Use 25** - the first prompt is not up before that |
| `--out DIR` | `shots/run` | where the PNGs go, named `000.png`, `001.png`, ... |
| `--capture M` | `pwtop` | `pwtop` (the only one that works), `pw0`, `pw2`, `pw3`, `bitblt` |
| `--captest` | off | one shot per capture method, then quit. For debugging a black screen |
| `--tree` | off | dump the whole window tree and capture every candidate surface |
| `--mute-timeout S` | 30 | how long to wait for the audio session to appear |

A shot is taken **before** each step, so `000.png` is the state the first input acts on.

### shoot_lines.py - one PNG per advance, for the review page

    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 $UVRUN python shoot_lines.py --advances 40 --out shots/chapter1

Walks the recorded boot navigation, then shoots `001.png`, `002.png`, ... of the 960x540
picture with no window chrome. `--keep-nav-shots` also keeps the navigation frames.
**Needs a test build in place** (below). Validated: 18 advances -> 18 distinct PNGs.

### probe_input.py - which input does anything

    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 $UVRUN python probe_input.py --set sweep \
        --nav "none*2; down; down; enter; none*3; down; down; enter; enter*8"

`--set all | confirm | keys | sweep`. Posts one input, screenshots, compares to the
previous shot, prints `CHANGED` or `same`. The first `CHANGED` in a run is the
attributable one; everything after it may just be an animation continuing.

### The patch helpers

    # replace the first narration line of a .lns with a test string (CR CR LF safe)
    $UVRUN python patch_test_line.py

    # build the loose-file override test (a .lsb at archive root + a .tsv in a subfolder)
    $UVRUN python make_override_test.py

    # set a property on every MesNew message box in an LSB, scripted
    uv run --no-project --with pylivemaker python set_msgbox_prop.py IN.lsb OUT.lsb PR_FONTCHANGEABLED 0
    uv run --no-project --with pylivemaker python set_msgbox_prop.py IN.lsb OUT.lsb PR_FONTNAME "ＭＳ Ｐ明朝"

    # find every message box definition in orig/ (one process, ~2 min; uvx per file is ~20 min)
    uv run --no-project --with pylivemaker python find_fontchangeabled.py ../../orig

    # measure Latin advance width against the em, from a screenshot
    uv run --no-project --with pillow python measure_width.py shots/font-fixed-pitch.png

## How to test a patched file

Loose files win over the archive, so:

1. Put the changed file next to the exe **in its archive-relative path**
   (`grep <name> notes/_db/_archive-list.txt` gives the path; `00000024.lsb` is at the
   root, `データベース\注意.tsv` is in a subfolder).
2. Run `run_game.py`.
3. **Delete the loose file and any folders you created.** Leave the game folder as:
   `live.dll`, `Readme.txt`, the `.exe`, plus `save.dat` and `SS/` which the game makes.

Never run `lmpatch` for a test: it rebuilds the 1 GB archive in `%TEMP%` on C:, which has
about 1.2 GB free.

## Where the game keeps its files

All next to the exe. Nothing in `%APPDATA%`, `%LOCALAPPDATA%`, `Documents` or `Saved Games`.

| path | what |
|---|---|
| `F:\4gatsu_8ka_Ver2.0.0.4\save.dat` | the autosave, ~10 KB, written on the first run and on progress |
| `F:\4gatsu_8ka_Ver2.0.0.4\SS\*.gal` | screenshots taken by the game's own capture key |
| `%TEMP%\fon*.tmp` | the embedded font, 26,894 bytes, one per launch, never cleaned up |
| `%TEMP%\~lv*.wmv` | the intro video, 2.4 MB, extracted on every launch |

The `%TEMP%` files are engine litter. Delete them after a batch of runs.

## The four things that each cost a run

All are fixed in `run_game.py`; do not undo them.

1. **Never pass `SW_SHOWMINNOACTIVE` in `STARTUPINFO`.** A minimized window renders nothing
   and every screenshot is solid black. Use `SW_SHOWNOACTIVATE` (4).
2. **Capture the `TBasePanel` child, not the `TFormView` frame.** Children are clipped out
   of the parent DC, so the frame captures as white with a toolbar strip on top.
3. **`PrintWindow` must be called on the TOP-LEVEL window with flag 0.** That is what makes
   the engine repaint into the DC. `PrintWindow` on the panel, `PW_RENDERFULLCONTENT`, and
   plain `BitBlt` all return stale pixels - a single frozen frame that never changes, which
   looks exactly like "the game is stuck". Method `pwtop` does the right thing and crops
   the frame down to the panel.
4. **Post input to the top-level `TFormView`, not to the panel.** Panel coordinates are
   shifted by the panel offset (0, 23 - the toolbar height) first. `run_game.do_steps`
   does this for you.

## What works and what does not

| input | result |
|---|---|
| `WM_KEYDOWN/UP VK_DOWN` / `VK_UP` to TFormView | moves the selection in a text menu |
| `WM_KEYDOWN/UP VK_RETURN` to TFormView | confirms the highlighted row |
| everything else | nothing |

A text menu only answers `VK_RETURN` **after** a `VK_DOWN` has highlighted a row. Repeated
`VK_RETURN` on an unselected menu does nothing, which reads as "the game is frozen".

Clicks never work: `WM_LBUTTONDOWN`/`WM_LBUTTONUP`/`WM_LBUTTONDBLCLK` to either window, at
any coordinate, on any screen. The engine hit-tests with the real cursor position, and the
window is parked at (-32000,-32000) where no cursor can reach. 46 keys were swept at the
title screen (F1-F12, 0-9, Z X C V A B S M N O P Q, Tab, arrows, Enter, Space, Esc, Home,
End, PgUp, PgDn, Ins, Del, Backspace, Shift, Ctrl, Alt, Apps) - none of them moves it.

That gate is now handled by the TEST-ONLY skip patch below, which jumps over the notices,
the title and the navigator instead of trying to click them.

## Boot flow

autosave-check prompt -> "proceed without testing" prompt -> intro video (~10 s) ->
title + notice screen with the two yellow buttons. `--warmup 25` lands on the first prompt.

Window layout: `TFormView` frame 966x591, client 960x562, a 23 px `TDock97` toolbar
(`終了` / `画面切替`) at the top, and the `TBasePanel` render surface of **960x540** below.


## Building a test build

Three screens are `ImgNew` image objects with mouse handlers and answer to nothing an
off-screen harness can post: the 11 notice items, the title menu, and the scenario
navigator map. `patch_skip_notice.py` jumps over all three with four Jump retargets in two
files - full reasoning and the exact LineNos are in `PROGRESS.md` under 4a.

    # the argument is the scene id to boot into (default 00000024)
    PYTHONUTF8=1 uv run --no-project --with pylivemaker python patch_skip_notice.py 000004A7
    cp work/loose/000000F2.lsb work/loose/0000001C.lsb "F:/4gatsu_8ka_Ver2.0.0.4/"

**THE TWO SKIP FILES - `000000F2.lsb` AND `0000001C.lsb` - MUST NEVER BE PART OF THE
DISTRIBUTED PATCH.** They delete the author's copyright and content notices, which the game
requires a player to accept once, and they bypass the scenario navigator. They exist so a
headless harness can reach scene text, nothing else.

A test build needs, next to the exe:

| file | why | ships? |
|---|---|---|
| `000000F2.lsb` | skip notices + title | **NO - harness only** |
| `0000001C.lsb` | skip navigator, jump into the scene | **NO - harness only** |
| `<scene id>.lsb` | the translated scene under test | yes |
| `メッセージボックス作成.lsb` | `PR_FONTNAME` = `ＭＳ Ｐ明朝` | yes |

Delete `save.dat` before a run if you want a clean state, and delete every loose file
afterwards.

## Addressing: Label is a COMMAND INDEX

`LabelReference.Label` - the number in `Jump`/`Call`/`PCReset` targets - is a **0-based
index into the target page's command list**, not a LineNo and not a label id. LineNo is not
even unique (`WhileInit`/`While`/`WhileLoop` share one), so index and LineNo agree early in
a file and drift apart later. Anything that edits jump targets must work in indices;
`patch_skip_notice.py` and `tools/harness/nav_api.py` both do. Full proof in `PROGRESS.md`
under STEP 5.

## Shooting a scene

Pass the scene id to `patch_skip_notice.py`; it finds its edit sites by structure, so there
are no magic numbers to update:


    # the argument is the scene id to boot into (default 00000024)
    PYTHONUTF8=1 uv run --no-project --with pylivemaker python patch_skip_notice.py 000004A7
    cp work/loose/000000F2.lsb work/loose/0000001C.lsb "F:/4gatsu_8ka_Ver2.0.0.4/"
    cp work/<SCENE ID>.lsb "F:/4gatsu_8ka_Ver2.0.0.4/"
    rm -f "F:/4gatsu_8ka_Ver2.0.0.4/save.dat"

    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 $UVRUN python shoot_lines.py         --advances <N LINES> --delay 1.4 --warmup 10 --out shots/<SCENE ID>

    rm -f "F:/4gatsu_8ka_Ver2.0.0.4/"*.lsb

`NAV = "none*23"` in `shoot_lines.py` is the wait from launch to the first text line of
`00000024` at `--delay 1.4`. A different scene opens differently; if the first shots are
fades rather than text, adjust that number.

## What advances the text

`VK_RETURN` (`WM_KEYDOWN`/`WM_KEYUP`) posted to the top-level `TFormView`. Measured in a
scene, 5 presses each:

| input | result |
|---|---|
| `VK_RETURN` | **advances** - 5 presses, 5 distinct frames |
| `VK_SPACE` | toggles the message box on/off - alternates between two frames |
| `VK_DOWN` | nothing in a scene (it only drives boot TEXT menus) |
| `VK_CONTROL` held (LiveMaker skip) | nothing |
| `WM_LBUTTONDOWN/UP` | nothing |

`{WAITPLAY "000" "CLICK"}` waits and the opening fades expire on their own, so no
auto-play rewrite of the `.lns` is needed.

## Font

`PR_FONTCHANGEABLED` is already 0 on all 13 `MesNew` commands in `メッセージボックス作成.lsb`;
there is no half-width switch left to flip. The lever is the face: eleven of the 13 use
`ＭＳ 明朝`, which is FIXED PITCH, so English comes out as evenly spaced typewriter text.

    uv run --no-project --with pylivemaker python set_msgbox_prop.py         ../../orig/メッセージボックス作成.lsb work/loose/メッセージボックス作成.lsb         PR_FONTNAME "ＭＳ Ｐ明朝"

Compare `shots/font-mincho.png` (as shipped, 6 lines) with `shots/font-pmincho.png`
(proportional, 5 lines) - same test line, same box, same scene.


## Which scene is which navigator entry

`notes/_db/_navigator-order.tsv` (agents only) lists all 219 navigator entries in map order
with their unlock conditions and, for 205 of them, the scene `.lsb` they launch. Built by
`tools/harness/nav_api.py` + `tools/harness/build_nav_order.py` from dumps alone, and
spot-checked in-game: booting a test build straight into the predicted scene and grepping
the first text line across `csv/*.csv` returned a unique, matching file.

## 2026-09-25: driving the English play folder

`run_game.py` (and everything that imports it) honours `SY_GAME_DIR`. The English folder
`F:\4gatsu_8ka_EN` holds a HARD LINK of the exe (same bytes, zero extra disk), its own
`save.dat`, and the shipped loose files. `SY_GAME_DIR=F:/4gatsu_8ka_EN ... run_game.py` boots it.
The skip files still go next to whichever exe you drive; delete them afterwards as before.

## mouse/ (on-screen)

On-screen driver with the real mouse and keyboard (added 2026-09-26, run 1). The window sits at
(0,0) of the primary screen, is not parked off-screen, and may take focus.

- `mouse/drive.py` is a server. Start it in the background:
  `uv run --no-project --python 3.12 --with pywin32 --with pycaw --with pillow --with comtypes python drive.py --deadline 16:28 --out <folder>`.
  It launches the EN exe (cwd = the game folder), sets HIGH priority, moves the frame to (0,0),
  mutes only the game's audio session, then waits for commands.
- `mouse/send.sh "click 720 512 2" "key enter 1.2" ...` writes a batch to `inbox.txt` and waits
  for `DONE`. Each command = input, wait, screenshot `NNN.png`, pixel diff, one row in `steps.tsv`.
  The command list is in the `drive.py` docstring. `mouse/contact.py A B` builds a contact sheet.
- `--deadline HH:MM`: a guard thread runs `shutdown()` at that wall-clock time, whatever the state.
  `quit` does the same on demand. Every exit path goes through `shutdown()`.
- `shutdown()` sets the game's audio session back to unmuted (and volume 1.0 if the remembered
  volume was ~0) BEFORE the kill, reads it back, kills the process tree, verifies with `tasklist`,
  and parks the cursor at the screen centre. The result is in `<out>/shutdown.txt`.
- `mouse/failsafe.py HH:MM:SS|now`: independent backup kill (unmute + kill by image name).
- On a 150% DPI screen `pwtop` capture does not work (the 960x540 frame lands in the top-left of a
  1440x810 bitmap). Use `capmode grab` (ImageGrab of the on-screen panel). Coordinates are then
  physical pixels of the 1440x810 panel.
- `mouse/walk_run1.py` replays `walk_run1.cmds` (run 1's exact command list). `mouse/screens.md`
  maps every screen and its clickables.
