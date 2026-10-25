"""Recompute eight audited normal-route totals from compiled English scripts.

Dry run: python tools/repair_first_arc_totals.py
Candidate: python tools/repair_first_arc_totals.py --output /outside/project/candidate.tsv

Requires pylivemaker. The audited input hashes intentionally refuse changed scripts.
Only the eight count1 cells may change; hidden/reference counters are outside scope.
"""
import argparse
from dataclasses import dataclass
import hashlib
from io import BytesIO
from pathlib import Path
import re

from livemaker.lsb import LMScript
from livemaker.lsb.novel import LNSDecompiler

from count_chars import count_text


ROOT = Path(__file__).resolve().parent.parent
TABLE_NAME = "シナリオデータベース.tsv"


@dataclass(frozen=True)
class Route:
    script: str
    original_total: int
    digest: str
    blocks: tuple


ROUTES = {
    "138": Route("000005C1", 5869,
                 "77c12baa7ed0d5e75c80d603fade00054b1187c956e333cf2c32910b1d62dcbc",
                 ((21, "0000242B"), (25, "line25"))),
    "145": Route("000005D6", 3642,
                 "5944453f09b2b334787557fec827b22c2ad7a2891f769b6fd5757193f39178bf",
                 ((11, "000005E1"),)),
    "147": Route("000005EB", 2247,
                 "891c68bdcd841b473647e9b04befc81f0a2fd2bc539098b3216725aed6505ee3",
                 ((11, "000005F8"),)),
    "205": Route("00000600", 2774,
                 "36707e01a5be6db19977bea4f4d68425abadf1fd82aa58c45aadab4c7e29979e",
                 ((11, "0000060D"), (15, "line15"), (19, "line19"))),
    "162": Route("00000617", 5948,
                 "7da562bdc361468528df11a79b7f1fec20a71998b528775b8d0ccb603c50fd5d",
                 ((8, "00000620"),)),
    "170": Route("0000062C", 5422,
                 "484b4e5b3b6bb61662d1d53a61a1a8b43b5498b1ae9fc883cc62174117ca399d",
                 ((11, "0000063A"), (15, "line15"), (19, "line19"))),
    "206": Route("00000641", 4057,
                 "491af8e2c73f288f2a52c1bf3f7d632d7cfddd178f4a0891b92c064a2917d11c",
                 ((11, "0000064C"),)),
    "202": Route("00000656", 4472,
                 "51996383945d991a0da583ccba5915ae87ce4422f3361e0ffc606ada7a676762",
                 ((11, "00000681"), (17, "0000185B"))),
}


def block_count(script, command_index, block_name):
    if command_index < 2 or command_index >= len(script.commands):
        raise ValueError(f"missing block {block_name}")
    command = script.commands[command_index]
    if (command.type.name != "TextIns" or command.LineNo != command_index
            or command.Mute or str(command["Target"]) != '"メッセージボックス"'):
        raise ValueError(f"unexpected TextIns identity/target: {block_name}")
    preceding = script.commands[command_index - 2]
    actual_name = (str(preceding["Name"]) if preceding.type.name == "Label"
                   else f"line{command.LineNo}")
    if actual_name != block_name:
        raise ValueError(f"unexpected block label: {block_name} vs {actual_name}")
    text = LNSDecompiler().decompile(command["Text"])
    body = "\n".join(line.rstrip("\r") for line in text.splitlines()
                     if not line.startswith(";"))
    if re.search(r"<VAR\b", body, re.IGNORECASE):
        raise ValueError(f"dynamic VAR text is unsupported: {block_name}")
    return count_text(body)


def route_total(path, route):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != route.digest:
        raise ValueError(f"changed compiled script requires route review: {route.script}")
    script = LMScript.from_file(BytesIO(data), call_name=path.name)
    total = sum(block_count(script, command_index, block_name)
                for command_index, block_name in route.blocks)
    if total <= 0:
        raise ValueError(f"empty route: {route.script}")
    return total


def assert_no_commentary(root):
    for folder in ("orig/データベース/実況", "tsv-en/実況",
                   "work/データベース/実況", "game/en/データベース/実況"):
        for number in ROUTES:
            for suffix in ("", "分岐"):
                if (root / folder / f"{number}{suffix}.tsv").exists():
                    raise ValueError(f"commentary requires coordinated rescaling: {number}{suffix}")


def compute_totals(root=ROOT, compiled_dir=None):
    assert_no_commentary(root)
    directory = compiled_dir if compiled_dir is not None else root / "work"
    return {number: route_total(directory / f"{route.script}.lsb", route)
            for number, route in ROUTES.items()}


def repair_table(data, totals):
    if set(totals) != set(ROUTES) or any(type(value) is not int or value <= 0
                                       for value in totals.values()):
        raise ValueError("expected exactly eight positive route totals")
    text = data.decode("utf-8")
    if text.startswith("\ufeff") or "\r" in text.replace("\r\n", ""):
        raise ValueError("expected UTF-8 without BOM and LF or CRLF lines")
    lines = text.splitlines(keepends=True)
    if not lines:
        raise ValueError("empty scenario table")
    header = lines[0].rstrip("\r\n").split("\t")
    if header[0] != "連番":
        raise ValueError("unexpected scenario table header")
    count_column = header.index("文字数1")
    branch_column = header.index("文字数2")
    core_column = header.index("コア文字数")
    seen = set()
    for line_index, line in enumerate(lines[1:], 1):
        content = line.rstrip("\r\n")
        ending = line[len(content):]
        cells = content.split("\t")
        number = cells[0]
        if number not in ROUTES:
            continue
        if number in seen or len(cells) != len(header):
            raise ValueError(f"duplicate or malformed scenario row: {number}")
        seen.add(number)
        expected = (str(ROUTES[number].original_total), str(totals[number]))
        if (cells[count_column] not in expected or cells[branch_column] != "0"
                or cells[core_column] != "0"):
            raise ValueError(f"unexpected scenario counts: {number}")
        cells[count_column] = str(totals[number])
        lines[line_index] = "\t".join(cells) + ending
    if seen != set(ROUTES):
        raise ValueError(f"missing scenario rows: {sorted(set(ROUTES) - seen)}")
    return "".join(lines).encode("utf-8")


def write_candidate(path, data, root=ROOT):
    if path.resolve().is_relative_to(root.resolve()):
        raise ValueError("candidate output must be outside the project")
    path.write_bytes(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", type=Path, default=ROOT / "tsv-en" / TABLE_NAME)
    parser.add_argument("--compiled-dir", type=Path, default=ROOT / "work")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        totals = compute_totals(ROOT, args.compiled_dir)
        original = args.table.read_bytes()
        candidate = repair_table(original, totals)
        for number, route in ROUTES.items():
            print(f"{number}: {route.script} count1 {route.original_total} -> {totals[number]}")
        print("candidate table: " + ("unchanged" if candidate == original else "eight count1 cells updated"))
        if args.output is not None:
            write_candidate(args.output, candidate)
            print(f"wrote candidate: {args.output}")
        return 0
    except (OSError, ValueError) as error:
        parser.exit(1, f"repair_first_arc_totals: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
