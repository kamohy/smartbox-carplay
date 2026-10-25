#!/usr/bin/env python3
"""Print printable strings from binaries that match a regular expression."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PRINTABLE = re.compile(rb"[\x20-\x7e]{4,}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pattern")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    pattern = re.compile(args.pattern, re.IGNORECASE)

    for path in args.paths:
        values = sorted(
            {
                match.group().decode("ascii")
                for match in PRINTABLE.finditer(path.read_bytes())
                if pattern.search(match.group().decode("ascii"))
            }
        )
        print(f"===== {path} ({len(values)}) =====")
        for value in values:
            print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
