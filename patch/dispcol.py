"""Shared helper for the encyclopedia display-name fix (lane R1, 2026-09-26, UNTR1 row "c encyclopedia names", Q2054).

事典場所.tsv 場所名 and 事典出来事.tsv 出来事名 are KEYS (object names, DBLocate, .gal path components, a literal
compare) and are also printed as captions. The key columns stay Japanese; tsv-en/事典場所.tsv and 事典出来事.tsv gain a
trailing column 表示名 (English name for translated rows, a copy of the key for the others), and every PRINT site reads
DBGetStr("表示名") instead of the key. Only the string operand inside the named property of the named command changes;
nothing else in the file is touched.

    SITES = [(index, property, old column, new column), ...]
    run(SITES, 'fix-<id>')   # reads sys.argv[1] (IN.lsb), writes sys.argv[2] (OUT.lsb)

Each site must hold exactly one string operand equal to `old` (or, when already fixed, `new`); anything else is an
error and nothing is written. Idempotent.
"""
import sys
from livemaker.lsb import LMScript


def _operands(parser):
    for e in parser.entries:
        for o in e.operands:
            yield o


def run(sites, tag):
    src, dst = sys.argv[1], sys.argv[2]
    s = LMScript.from_file(src)
    errs, done, already = [], 0, 0
    for idx, prop, old, new in sites:
        cmd = s.commands[idx]
        try:
            parser = cmd[prop]
        except KeyError:
            errs.append(f'idx {idx}: no property {prop}')
            continue
        ops = [o for o in _operands(parser) if getattr(o, 'value', None) in (old, new)]
        if len(ops) != 1:
            errs.append(f'idx {idx} {prop}: expected one operand {old!r}, found {len(ops)} in {parser}')
            continue
        if ops[0].value == new:
            already += 1
            continue
        ops[0].value = new
        done += 1
    if errs:
        sys.exit(f'{tag}: ' + '; '.join(errs))
    open(dst, 'wb').write(s.to_lsb())
    print(f'{tag}: {done} display sites repointed, {already} already fixed')
