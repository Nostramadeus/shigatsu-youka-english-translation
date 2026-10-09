"""Extract the .lns text scenarios of one LSB - a drop-in replacement for `lmlsb extract`
that does not crash on 0000001C.lsb.

    uv run --no-project --with pylivemaker python tools/extract_lsb.py <id> [-o OUTDIR]
    uv run --no-project --with pylivemaker python tools/extract_lsb.py path/to/file.lsb -o DIR

Default input is `orig/<id>.lsb`, default output dir is `lns/`. Writes exactly what
`lmlsb extract -o DIR orig/<id>.lsb` writes: `<id>.lsbref` (one `name:line` row per text
scenario, CR LF) plus one `<id>-<scenario>.lns` per scenario (CR CR LF, no trailing newline),
utf-8, scenarios in run order. Verified byte-identical to the committed lns/00000024-* files.

WHY THIS EXISTS (notes/PART1-GAP-AUDIT.md blocker 2): `lmlsb extract` dies on 0000001C.lsb with

    lmlsb.py:248 _escape_scenario_name -> re.sub(...)
    TypeError: expected string or bytes-like object, got 'LiveParser'

because `LMScript.text_scenarios()` takes the scenario name from the `Label` command two
commands before the `TextIns` (`self.commands[i - 2].get("Name", "")`), and in this file some of
those names are COMPUTED - the Label's Name is an expression (a `LiveParser`), not a string.
`_escape_scenario_name` assumes a string. Fix here: run the name through `str()` first (an
expression's `str()` is its source text, e.g. `"chapter" ++ n`), then escape. The scenario name
is cosmetic on the way back in: `lmlsb batchinsert` matches .lns files to `TextIns` commands by
the `name:line` pairs in the .lsbref, never by the name itself, so a renamed file round-trips.

Gate before trusting any output (this is how the project gates every compile):

    SRC_DIR=lns sh tools/compile_en.sh <id>      # work/<id>.lsb must be byte-identical to orig/
"""
import re
import sys
from pathlib import Path

from livemaker.lsb import LMScript
from livemaker.lsb.novel import LNSDecompiler

# byte-for-byte the pattern in livemaker.cli.lmlsb._escape_scenario_name. Note it does NOT
# contain a backslash: inside a character class `\/` is just `/`.
INVALID = re.compile(r'[\/:*?"<>|]+')
# a computed name's str() is source text and can hold a backslash (a path literal in the
# expression), which would turn the filename into a subdirectory. Only computed names get this.
INVALID_EXPR = re.compile(r'[\\\/:*?"<>|]+')


def escape_name(name):
    """Replace invalid Windows path characters with underscore.

    Same as `livemaker.cli.lmlsb._escape_scenario_name` for a string name, so output filenames
    are unchanged for every file `lmlsb extract` already handles. A non-string name (a COMPUTED
    scenario name, i.e. a LiveParser - what makes lmlsb crash) is rendered with str() first and
    then escaped a little harder, backslash included.
    """
    if isinstance(name, str):
        return INVALID.sub('_', name)
    try:
        name = str(name)
    except Exception as e:  # a LiveParser whose constant folder chokes (numpy array)
        name = 'expr_%s' % type(e).__name__
    return INVALID_EXPR.sub('_', name)


def extract(lsb_path, out_dir, encoding='utf-8'):
    lsb_path, out_dir = Path(lsb_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lsb = LMScript.from_file(str(lsb_path))
    stem = lsb_path.stem
    written = []
    # text mode on purpose: lmlsb extract writes in text mode too, so the LNSDecompiler's CR LF
    # becomes CR CR LF in the .lns and the .lsbref rows become CR LF. compile_en.sh depends on it.
    with open(out_dir / ('%s.lsbref' % stem), 'w', encoding=encoding) as ref:
        for line, name, scenario in lsb.text_scenarios():
            escaped = escape_name(name)
            fname = '%s-%s.lns' % (stem, escaped) if escaped else '%s-line%d.lns' % (stem, line)
            body = LNSDecompiler().decompile(scenario)
            with open(out_dir / fname, 'w', encoding=encoding) as f:
                f.write(body)
            ref.write('%s:%d\n' % (fname, line))
            written.append((fname, line, name if isinstance(name, str) else escaped))
    return stem, written


def main():
    args = [a for a in sys.argv[1:]]
    out_dir = 'lns'
    if '-o' in args:
        i = args.index('-o')
        out_dir = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 2
    target = args[0]
    lsb_path = Path(target if target.lower().endswith('.lsb') else 'orig/%s.lsb' % target)
    if not lsb_path.exists():
        print('no such file: %s' % lsb_path, file=sys.stderr)
        return 1
    print('Extracting scripts from %s' % lsb_path)
    stem, written = extract(lsb_path, out_dir)
    for fname, line, name in written:
        print('  wrote %s/%s  (line %d)' % (out_dir, fname, line))
    print('# %d scenarios -> %s/%s.lsbref' % (len(written), out_dir, stem), file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
