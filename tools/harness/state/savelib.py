"""Read variables out of a LiveMaker save.dat (Shigatsu Youka). Read-only.

Copied from work/feedback-20261113/save-decode/decode_save.py (lane S, 2026-11-13), which documents
the format:
  "vff\\0" + header, then zlib streams back to back. All but the last are game save slots
  (u32 202, caption, current .lsb, ... screen objects ..., scope-0 variable records).
  The last stream starts "Status103" + u32 count + scope-3 (status) variable records.
  Variable record: u8 type (1 int32, 2 Delphi 80-bit float, 3 bool u8, 4 string u32len+CP932)
  + u32-length CP932 name + u32 ndims + ndims*u32 sizes + u32 count + values + 7 trailer bytes.
"""
import re
import struct
import zlib


def ext80(b):
    mant = int.from_bytes(b[:8], "little")
    se = int.from_bytes(b[8:10], "little")
    if se & 0x7FFF == 0 and mant == 0:
        return 0.0
    return (-1 if se & 0x8000 else 1) * mant * 2.0 ** ((se & 0x7FFF) - 16383 - 63)


def parse_record(d, pos):
    t = d[pos]
    if t not in (1, 2, 3, 4):
        raise ValueError("type")
    pos += 1
    n = struct.unpack_from("<I", d, pos)[0]; pos += 4
    if not 0 < n <= 200:
        raise ValueError("namelen")
    name = d[pos:pos + n].decode("cp932"); pos += n
    nd = struct.unpack_from("<I", d, pos)[0]; pos += 4
    if nd > 4:
        raise ValueError("ndims")
    dims = list(struct.unpack_from("<%dI" % nd, d, pos)); pos += 4 * nd
    cnt = struct.unpack_from("<I", d, pos)[0]; pos += 4
    if cnt > 200000:
        raise ValueError("count")
    vals = []
    for _ in range(cnt):
        if t == 1:
            vals.append(struct.unpack_from("<i", d, pos)[0]); pos += 4
        elif t == 3:
            vals.append(d[pos]); pos += 1
        elif t == 2:
            vals.append(ext80(d[pos:pos + 10])); pos += 10
        else:
            m = struct.unpack_from("<I", d, pos)[0]; pos += 4
            if m > 100000:
                raise ValueError("strlen")
            vals.append(d[pos:pos + m].decode("cp932", "replace")); pos += m
    tr = d[pos:pos + 7]
    if len(tr) < 7 or tr[2:6] != b"\xff\xff\xff\xff":
        raise ValueError("trailer")
    return (t, name, dims, vals), pos + 7


def parse_run(d, pos):
    out = []
    while pos < len(d):
        try:
            r, pos2 = parse_record(d, pos)
        except Exception:
            break
        out.append(r)
        pos = pos2
    return out, pos


def longest_run(d):
    best, pos = [], 0
    while pos < len(d) - 16:
        if d[pos] in (1, 2, 3, 4) and 0 < d[pos + 1] < 200 and d[pos + 2:pos + 5] == b"\0\0\0":
            recs, end = parse_run(d, pos)
            if len(recs) > len(best):
                best = recs
            if len(recs) > 50:
                pos = end
                continue
        pos += 1
    return best


def split_blocks(raw):
    blocks, i = [], 0
    while True:
        j = raw.find(b"\x78\x9c", i)
        if j < 0:
            break
        try:
            z = zlib.decompressobj()
            out = z.decompress(raw[j:])
            if z.eof:
                blocks.append(out)
                i = len(raw) - len(z.unused_data)
                continue
        except zlib.error:
            pass
        i = j + 1
    return blocks


def slot_header(b):
    pos = 4
    out = []
    for _ in range(2):
        n = struct.unpack_from("<I", b, pos)[0]; pos += 4
        out.append(b[pos:pos + n].decode("cp932", "replace")); pos += n
    return out[0], out[1]


class Save:
    """status: {name: (type, dims, vals)}; slots: list of (caption, lsb, {name: (type, dims, vals)})."""

    def __init__(self, path):
        raw = open(path, "rb").read()
        if raw[:3] != b"vff":
            raise ValueError("not a vff save: %s" % path)
        blocks = split_blocks(raw)
        if not blocks or blocks[-1][:9] != b"Status103":
            raise ValueError("no Status103 block in %s" % path)
        st = blocks[-1]
        cnt = struct.unpack_from("<I", st, 9)[0]
        recs, _ = parse_run(st, 13)
        if len(recs) != cnt:
            raise ValueError("status block: parsed %d of %d records" % (len(recs), cnt))
        self.size = len(raw)
        self.status = {n: (t, dims, vals) for t, n, dims, vals in recs}
        self.slots = []
        for b in blocks[:-1]:
            try:
                cap, lsb = slot_header(b)
            except Exception:
                cap, lsb = "?", "?"
            self.slots.append((cap, lsb, {n: (t, dims, vals) for t, n, dims, vals in longest_run(b)}))

    def lookup(self, name, slot_caption=None):
        """Return (where, type, dims, vals) for a variable: status first, then the named slot, then any slot."""
        if name in self.status:
            return ("status",) + self.status[name]
        order = sorted(self.slots, key=lambda s: s[0] != slot_caption)
        for cap, lsb, V in order:
            if name in V:
                return ("slot:%s" % cap,) + V[name]
        return None


REF = re.compile(r"^\s*([^\[\]=\s]+)\s*((?:\[\s*[0-9,\s]+\s*\]\s*)*)$")
BRK = re.compile(r"\[\s*([0-9,\s]+)\s*\]")


def split_top(text, seps=",;"):
    """Split on separators that are not inside [...]."""
    out, cur, depth = [], "", 0
    for ch in text:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch in seps and depth == 0:
            if cur.strip():
                out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def fmt(t, v):
    if t == 2:
        return repr(v)
    return str(v)


def read_values(save, refs, slot_caption=None):
    """refs: list of 'name' or 'name[i]'. Returns list of (ref, value-string, where)."""
    rows = []
    for ref in refs:
        m = REF.match(ref)
        if not m:
            rows.append((ref, "(bad name)", "-"))
            continue
        name, idx = m.group(1), m.group(2)
        hit = save.lookup(name, slot_caption)
        if hit is None:
            rows.append((ref, "(absent)", "-"))
            continue
        where, t, dims, vals = hit
        if not idx:
            if dims:
                rows.append((ref, "(array %s; give an index)" % dims, where))
            else:
                rows.append((ref, fmt(t, vals[0]), where))
            continue
        # name[i], name[i][j] or name[i,j]; N-D is flattened row-major (last index fastest)
        ix = [int(x) for g in BRK.findall(idx) for x in g.split(",")]
        if len(ix) != len(dims) or not ix:
            rows.append((ref, "(%d indexes given; dims %s)" % (len(ix), dims), where))
            continue
        if any(not 0 <= i < d for i, d in zip(ix, dims)):
            rows.append((ref, "(index out of range; dims %s)" % dims, where))
            continue
        flat = 0
        for i, d in zip(ix, dims):
            flat = flat * d + i
        if flat >= len(vals):
            rows.append((ref, "(flat index %d beyond %d values)" % (flat, len(vals)), where))
            continue
        ix = [flat]
        rows.append((ref, fmt(t, vals[ix[0]]), where))
    return rows
