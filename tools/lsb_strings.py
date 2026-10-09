"""List or replace string literals inside LSB commands (menu labels built with AddArray, captions, etc.),
which `lmlsb extract` does NOT expose as .lns text.

    uv run --no-project --with pylivemaker python tools/lsb_strings.py list IN.lsb            > strings.tsv
    uv run --no-project --with pylivemaker python tools/lsb_strings.py apply IN.lsb OUT.lsb MAP.tsv

`list` prints one row per string literal: command index, LineNo, command type, param key, value
(\\r and \\n escaped), the whole expression the literal sits in (first 100 chars).
Paths (contain "\\" or end in .lsb/.gal/.ogg/.wmv/.tsv) and empty strings are omitted.
MAP.tsv = two columns, JP<TAB>EN, UTF-8, no header, \\r \\n escapes allowed; every JP must match a literal
exactly; every mapped literal is replaced everywhere it occurs. Exit 1 if a JP key is not found or an EN
value is not CP932-encodable. Round-trip with an empty map is byte-identical (verified on 000000F2,
0000001E and 0000001C on 2026-09-26).

2026-09-26: `walk()` is now a deep walker (see its docstring). Before that it followed only
`entries`/`operands`, so every string handed to a subroutine as a `Call` argument was invisible
(`Call.Params` is a `LiveParserArray` -> `.parsers`). `list` counts grew 000000F2 1043 -> 1057,
0000001E 6668 -> 6678, 0000001C 8350 -> 8382; the old output is a strict subset of the new one
(the only rows that differ are additions). `apply` with the three real patch/labels-*.tsv maps
produces byte-identical output and an identical hit table before and after, so nothing shipped
changes. Anything whose text was cleared "by lsb_strings list" before that date was
under-reported; re-list it. NOTE: the expression column contains Python object reprs with
memory addresses for some command types, so it is not stable between runs - strip
`0x[0-9a-f]+` before diffing two `list` outputs.
"""
import sys
from pathlib import Path
from livemaker.lsb import LMScript
from livemaker.lsb.core import Param, ParamType

PATH_SUFFIX = ('.lsb', '.gal', '.ogg', '.wmv', '.tsv', '.png', '.jpg', '.wav', '.mp3')
META = ('type', 'LineNo', 'Indent', 'Mute', 'NotUpdate')


def walk(obj, depth=0, seen=None):
    """Yield every Param of type Str reachable from obj, however deeply nested.

    Descends construct Containers (anything with .keys()), plain objects (__dict__),
    lists/tuples, and finally the named attributes entries / operands / parsers / value.
    `parsers` is the one that matters: a Call command's arguments are a LiveParserArray,
    which has .parsers and no .entries, so the pre-2026-09-26 walker (entries + operands
    only) could not see a single string passed to a subroutine. Same traversal as
    work/gap-audit/lits.py, but it yields the mutable Param objects so `apply` still works.
    `seen` dedups: one Param is yielded once per top-level command argument even when two
    routes reach it, and it breaks reference cycles.
    """
    if depth > 14:
        return
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return
    if isinstance(obj, Param):
        seen.add(id(obj))
        if obj.type == ParamType.Str and isinstance(obj.value, str):
            yield obj
        return
    if isinstance(obj, (str, bytes, bytearray, int, float, bool)) or obj is None:
        return
    seen.add(id(obj))
    if isinstance(obj, (list, tuple)):
        for x in obj:
            yield from walk(x, depth + 1, seen)
        return
    if hasattr(obj, 'keys'):  # construct Container / dict
        for k in list(obj.keys()):
            if k in META or (isinstance(k, str) and k.startswith('_io')):
                continue
            try:
                v = obj[k]
            except Exception:
                continue
            yield from walk(v, depth + 1, seen)
        return
    d = getattr(obj, '__dict__', None)
    if d:
        for k, v in list(d.items()):
            if k.startswith('_'):
                continue
            yield from walk(v, depth + 1, seen)
        return
    for attr in ('entries', 'operands', 'parsers', 'value'):
        if hasattr(obj, attr):
            yield from walk(getattr(obj, attr), depth + 1, seen)


def safe_str(obj):
    """str() of a command argument, surviving pylivemaker's constant folder.

    Folding an expression that holds a numpy array raises
    `ValueError: Could not guess datatype for [ 0. -2.078125]`; the expression text is only
    context here, so fall back to the type name rather than losing the row.
    """
    try:
        return str(obj)
    except Exception as e:
        return '<<UNFOLDABLE %s: %s>>' % (type(obj).__name__, type(e).__name__)


def literals(lsb):
    for i, cmd in enumerate(lsb.commands):
        keys = list(cmd.keys()) if hasattr(cmd, 'keys') else []
        for k in keys:
            if k in META:
                continue
            try:
                v = cmd[k]
            except Exception:
                continue
            for p in walk(v):
                yield i, cmd.LineNo, cmd.type.name, k, p, v


def visible(s):
    if not s.strip():
        return False
    if '\\' in s or s.lower().endswith(PATH_SUFFIX):
        return False
    return True


def esc(s):
    return s.replace('\r', '\\r').replace('\n', '\\n')


def unesc(s):
    return s.replace('\\r', '\r').replace('\\n', '\n')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    mode = sys.argv[1]
    lsb = LMScript.from_file(sys.argv[2])
    if mode == 'list':
        seen = 0
        for i, ln, t, k, p, expr in literals(lsb):
            if visible(p.value):
                print('\t'.join([str(i), str(ln), t, k, esc(p.value), esc(safe_str(expr))[:100]]))
                seen += 1
        print('# %d string literals' % seen, file=sys.stderr)
        return 0
    if mode == 'apply':
        out, mapfile = Path(sys.argv[3]), Path(sys.argv[4])
        m = {}
        for line in mapfile.read_text(encoding='utf-8').splitlines():
            if not line.strip() or line.startswith('#'):
                continue
            parts = line.split('\t')
            jp, en = unesc(parts[0]), unesc(parts[1])
            ctx = parts[2] if len(parts) > 2 and parts[2].strip() else None  # optional: expression must contain this
            en.encode('cp932')  # raises if not representable
            m[jp] = (en, ctx)
        hits = {k: 0 for k in m}
        for i, ln, t, k, p, expr in literals(lsb):
            if p.value in m:
                en, ctx = m[p.value]
                if ctx and ctx.startswith('idx:'):
                    # idx:N targets one command; idx:N.KEY targets one PARAM of it (a Caption whose
                    # Name and PR_TEXT hold the same literal needs only the text moved).
                    spec = ctx[4:].strip()
                    if '.' in spec:
                        wi, wk = spec.split('.', 1)
                        if str(i) != wi.strip() or k != wk.strip():
                            continue
                    elif str(i) != spec:
                        continue
                elif ctx and ctx not in safe_str(expr):
                    continue
                hits[p.value] += 1
                p.value = en
        missing = [k for k, n in hits.items() if n == 0]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(lsb.to_lsb())
        for k, n in hits.items():
            print('%d\t%s\t->\t%s' % (n, esc(k), esc(m[k][0])))
        print('wrote %s (%d bytes)' % (out, out.stat().st_size))
        if missing:
            print('NOT FOUND:', [esc(x) for x in missing], file=sys.stderr)
            return 0 if '--allow-missing' in sys.argv else 1
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
