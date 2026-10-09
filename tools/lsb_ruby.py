"""Set or clear the ruby (furigana) strings stored in an LSB's text style tables.

    uv run --no-project --with pylivemaker python tools/lsb_ruby.py list IN.lsb
    uv run --no-project --with pylivemaker python tools/lsb_ruby.py apply IN.lsb OUT.lsb [MAP.tsv]

Each TextIns command carries a list of TDecorate style entries; a style with a non-empty `ruby` draws that string
above every word that uses the style (that is what `<STYLE ID="n" RUBY="...">` in the .lns means; the attribute in
the .lns is only a rendering of this field, the compiler does not write it back). `apply` sets every ruby that
appears as a JP key in MAP.tsv (JP ruby<TAB>EN ruby, UTF-8, no header) to the EN value and clears every other
ruby to "" (kana over English is meaningless). Without a map, all rubies are cleared. CP932 is enforced.
"""
import sys
from pathlib import Path
from livemaker.lsb import LMScript


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    mode, src = sys.argv[1], sys.argv[2]
    lsb = LMScript.from_file(src)
    if mode == 'list':
        for i, c in enumerate(lsb.commands):
            if c.type.name != 'TextIns':
                continue
            for k, d in enumerate(c['Text'].decorators):
                if d.ruby:
                    print('%d\t%d\t%d\t%s' % (i, c.LineNo, k, d.ruby))
        return 0
    if mode == 'apply':
        out = Path(sys.argv[3])
        m = {}
        if len(sys.argv) > 4 and not sys.argv[4].startswith('--') and Path(sys.argv[4]).exists():
            for line in Path(sys.argv[4]).read_text(encoding='utf-8').splitlines():
                if not line.strip() or line.startswith('#'):
                    continue
                jp, en = line.split('\t')[:2]
                en.encode('cp932')
                m[jp] = en
        keep_en = '--keep-en' in sys.argv  # rubies already rewritten to their English value by the compiler stay
        en_values = set(m.values())
        kept, cleared = 0, 0
        for c in lsb.commands:
            if c.type.name != 'TextIns':
                continue
            for d in c['Text'].decorators:
                if not d.ruby:
                    continue
                if d.ruby in m:
                    d.ruby = m[d.ruby]
                    kept += 1
                elif keep_en and d.ruby in en_values:
                    kept += 1
                else:
                    d.ruby = ''
                    cleared += 1
        out.write_bytes(lsb.to_lsb())
        print('ruby: %d set to English, %d cleared -> %s' % (kept, cleared, out))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
