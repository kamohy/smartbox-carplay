#!/usr/bin/env python3
"""Compare printable strings and ELF metadata between two binaries."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from elftools.elf.elffile import ELFFile


PRINTABLE = re.compile(rb"[\x20-\x7e]{4,}")


def strings(path: Path) -> set[str]:
    return {match.group().decode("ascii") for match in PRINTABLE.finditer(path.read_bytes())}


def elf_info(path: Path) -> tuple[dict[str, object], set[str]] | None:
    with path.open("rb") as fh:
        if fh.read(4) != b"\x7fELF":
            return None
        fh.seek(0)
        elf = ELFFile(fh)
        dynamic_symbols: set[str] = set()
        section = elf.get_section_by_name(".dynsym")
        if section is not None:
            dynamic_symbols = {symbol.name for symbol in section.iter_symbols() if symbol.name}
        return ({
            "class": elf.elfclass,
            "little_endian": elf.little_endian,
            "machine": elf["e_machine"],
            "type": elf["e_type"],
            "entry": f"0x{elf['e_entry']:X}",
        }, dynamic_symbols)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", type=Path)
    parser.add_argument("new", type=Path)
    parser.add_argument("--filter", default="", help="case-insensitive regex applied to changed strings")
    args = parser.parse_args()

    old_strings = strings(args.old)
    new_strings = strings(args.new)
    added = sorted(new_strings - old_strings)
    removed = sorted(old_strings - new_strings)
    if args.filter:
        pattern = re.compile(args.filter, re.IGNORECASE)
        added = [value for value in added if pattern.search(value)]
        removed = [value for value in removed if pattern.search(value)]

    old_elf = elf_info(args.old)
    new_elf = elf_info(args.new)
    old_symbols = old_elf[1] if old_elf else set()
    new_symbols = new_elf[1] if new_elf else set()
    report = {
        "old": {"path": str(args.old), "elf": old_elf[0] if old_elf else None, "string_count": len(old_strings)},
        "new": {"path": str(args.new), "elf": new_elf[0] if new_elf else None, "string_count": len(new_strings)},
        "dynamic_symbols_added": sorted(new_symbols - old_symbols),
        "dynamic_symbols_removed": sorted(old_symbols - new_symbols),
        "added": added,
        "removed": removed,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
