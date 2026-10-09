# tools/images - replacing pictures that carry Japanese text

Built 2026-09-25 (image lane). Findings, inventory and the plan: `notes/IMAGE-LANE-PLAN.md`.
Format-test evidence and exact commands: `tools/harness/PROGRESS.md`, section "Images".

Every command runs from the project root with `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` and
`uv run --no-project --with pylivemaker python ...` (pylivemaker pulls in Pillow and lxml).
Disk: F: has under 1 GB free. Never extract the whole archive; never convert the art folders
(背景 / リファレンス / 立ち絵 / イラスト) to PNG in bulk.

| tool | what |
|---|---|
| `extract_images.py --prefix "グラフィック\\タイトル\\"` / `--names-file LIST` / `--list-only` | pulls single entries out of the 1 GB exe into `work/images/gal/<archive path>`; refuses more than `--max-mb` (60) |
| `gal_to_png.py SRC DST` | GAL -> PNG with pylivemaker's PIL plugin (mirrors the folder tree; skips existing) |
| `galx_probe.py FILE` / `gal_probe.py FILE` | dump the header of a GaleX200 / old Gale10x file |
| `galx_stats.py DIR [--list-blocked]` | tabulate CompType / Bpp / block / frames / alpha over a folder |
| `contact_sheet.py SRC OUT_PREFIX [--cols 4 --rows 4 --cell 300x200]` | labelled contact sheets + a TSV index, for judging many images with one Read |
| `scene_images.py orig OUT.tsv` | which images every `.lsb` references (commands + TextIns bodies) -> `notes/_db/_image-usage.tsv` |
| `font_sheet.py` | renders review/images/FONTS.html: the candidate-font sheet for the owner (5 styles x 4 installed fonts on the demo samples) |
| `typeset_ui.py JOB.json` | paint out + set English on a PNG (erase modes flat / alpha / box / none / inpaint (colour mask + Telea, for textured backgrounds); PIL text with auto-fit, stroke, letter-spacing) |
| `gal_write.py ORIG.gal NEW.png OUT.gal [--comp keep|jpeg|zip] [--verify]` | PNG -> GaleX using the original as the header template; `--verify` re-reads with pylivemaker and prints per-channel error |
| `mark_test.py IN OUT COLOR` | draws a coloured bar (format-test marker) |
| `jobs_tierb.py` | the Tier B jobs (rest of the UI: right-click menu, main menu, encyclopedia, chatter, reference screen, document mode, the engine option menu, help panels, shatter frames) + Tier C part 1 (3 story pictures). Run it with `batch.py --jobs jobs_tierb` |
| `jobs_part1.py` | the part-1 picture jobs (id, screen, style, items = pictures sharing a layout, English strings, erase method, overrides), in order of first encounter |
| `batch.py [--jobs MODULE] [--only ID,..] [--styles s,..] [--no-ship] [--dry]` | runs the jobs: analyse (background, lettering mask, fill/outline colours), erase, set English with the style's font (FONTS = the owner's picks), encode + verify, copy to F:/4gatsu_8ka_EN/グラフィック/..., append to tools/ship-list.txt "# pictures", previews in review/images/preview/, first translations to notes/_tmp/tl-log-IMAGES.md |

## The batch loop (part 1 done 2026-09-26; the next batch = copy jobs_part1.py, add jobs)

    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 uv run --no-project --with pylivemaker --with numpy --with opencv-python-headless python tools/images/batch.py --no-ship
    # read review/images/preview/*.png (<= 7 per turn), fix jobs (explicit color / mask_color / box / word_boxes / two-line strings), re-run --only ID
    # then without --no-ship: files land in work/グラフィック/ + the EN folder + the ship list
    # verify with the harness: notice gate (run_game.py, no skip patch) and the opening scene end (shoot_lines.py --advances 235 with the
    # skip builds copied INTO the EN folder and the shipped 000000F2.lsb / 0000001C.lsb restored from work/ afterwards)

New since the part-1 batch: `--jobs MODULE` picks the job file (previews go to `review/images/preview-<name>/`, first translations to `notes/_tmp/tl-log-IMAGES2.md`, and the log no longer writes a row twice). Erase modes gained `inpainta` (inpaint the colour AND the alpha plane - lettering drawn over icon art), `maskfill` (repaint only the glyph pixels in the plate colour - shatter frames) and `maskalpha`. Modes gained `blank` (erase, set nothing), `rotated` (`rot_lines` = several strings set at an angle) and `lines` (one English string per named box, erased box by box, so table rules and icon columns survive - this is how the help panels are rebuilt). Job keys gained `max_size` (cap the auto-fit so a menu keeps ONE type size), `mask_grow`, `alpha_thr` (mask lettering that sits on a semi-transparent fade), `keep_alpha`, `align` and `chain` (start from the previous job's output instead of the Japanese original, for a second pass on the same picture).

Per-item overrides (third tuple element): `color`, `stroke`, `stroke_color`, `mask_color` [rmin,rmax,gmin,gmax,bmin,bmax],
`box` (limit the lettering search), `textbox`, `keep_edges`, `pad`, `thr`. Modes: default (one string per picture),
`words` (one word per `word_boxes` entry, re-set in place), `boxes` (composite: red+pink mask, `protect` boxes, two passes).

## The loop for one image

    extract_images.py --name "グラフィック\\タイトル\\了承する.gal"
    gal_to_png.py "work/images/gal/グラフィック/タイトル/了承する.gal" work/images/png/グラフィック/タイトル
    # write a job (see work/images/demo/job.json), then:
    typeset_ui.py JOB.json
    gal_write.py ORIG.gal NEW.png OUT.gal --comp zip --verify        # zip = pixel exact; jpeg = smaller
    mkdir -p "F:/4gatsu_8ka_EN/グラフィック/タイトル" && cp OUT.gal "F:/4gatsu_8ka_EN/グラフィック/タイトル/了承する.gal"
    # screenshot with tools/harness/run_game.py (SY_GAME_DIR=F:/4gatsu_8ka_EN), then delete the loose file for tests;
    # shipped files go through tools/ship-list.txt + build_en_folder.py like every other patch file.

Rules the engine taught us: the replacement must be a real GaleX file (a PNG renamed `.gal` is
ignored and blanks the whole screen it belongs to), the same pixel size as the original, and
`--verify` must report a clean re-read before it goes anywhere near the exe.

## Structural check before shipping (added 2026-09-26 after the black-screen bug)

    PYTHONUTF8=1 uv run --no-project python tools/images/compare_gal.py "タイトル/残酷/残酷.gal" ...   # one or more
    PYTHONUTF8=1 uv run --no-project python tools/images/scan_tail.py                                # all shipped files

`compare_gal.py` prints the original and the replacement side by side (size, header XML, frame names, Bpp,
AlphaOn, blob sizes, leftover bytes) and names the differences. `scan_tail.py` walks every picture in
`work/グラフィック/`, compares it with its original in `work/images/gal/` and must print `MISMATCHES: 0`.
A GaleX layer always carries an alpha block, `AlphaOn="0"` included; dropping it truncates the file and the
engine silently refuses the picture, which blanks the whole screen it belongs to.

`warn_colors.py` samples the text colour of a picture (mean of the visible pixels, mode colour of the opaque
core, mode colour of the outer rim) for the original and our replacement side by side; `warn_preview.py` builds
review/images/preview-warnings/index.html from it. Use them before trusting the analyser's fill: on lettering
over transparency batch.py adds a 1 px stroke and, with no outline colour in the original, paints it white.
