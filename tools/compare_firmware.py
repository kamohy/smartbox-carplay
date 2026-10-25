#!/usr/bin/env python3
"""Compare two SmartBox firmware images without modifying either file."""

from __future__ import annotations

import argparse
import collections
import difflib
import hashlib
import json
import pathlib


def chunk_hashes(data: bytes, size: int) -> list[bytes]:
    return [hashlib.sha256(data[index : index + size]).digest() for index in range(0, len(data) - size + 1, size)]


def common_prefix(left: bytes, right: bytes) -> int:
    for index, (a, b) in enumerate(zip(left, right)):
        if a != b:
            return index
    return min(len(left), len(right))


def common_suffix(left: bytes, right: bytes) -> int:
    for index, (a, b) in enumerate(zip(reversed(left), reversed(right))):
        if a != b:
            return index
    return min(len(left), len(right))


def compare(left_path: pathlib.Path, right_path: pathlib.Path, chunk_size: int) -> dict[str, object]:
    left = left_path.read_bytes()
    right = right_path.read_bytes()
    overlap = min(len(left), len(right))
    xor = bytes(a ^ b for a, b in zip(left[:overlap], right[:overlap]))
    left_hashes = chunk_hashes(left, chunk_size)
    right_hashes = chunk_hashes(right, chunk_size)
    same_offset = sum(a == b for a, b in zip(left_hashes, right_hashes))
    matcher = difflib.SequenceMatcher(a=left_hashes, b=right_hashes, autojunk=False)
    matches = [
        {
            "left_offset": block.a * chunk_size,
            "right_offset": block.b * chunk_size,
            "length": block.size * chunk_size,
            "chunks": block.size,
        }
        for block in matcher.get_matching_blocks()
        if block.size
    ]
    matches.sort(key=lambda item: item["length"], reverse=True)
    left_counts = collections.Counter(left_hashes)
    right_counts = collections.Counter(right_hashes)
    shared_unique = set(left_counts) & set(right_counts)

    return {
        "left": {
            "path": str(left_path.resolve()),
            "size": len(left),
            "sha256": hashlib.sha256(left).hexdigest().upper(),
        },
        "right": {
            "path": str(right_path.resolve()),
            "size": len(right),
            "sha256": hashlib.sha256(right).hexdigest().upper(),
        },
        "size_difference": len(left) - len(right),
        "common_prefix_bytes": common_prefix(left, right),
        "common_suffix_bytes": common_suffix(left, right),
        "overlap_bytes": overlap,
        "identical_bytes_same_offset": sum(a == b for a, b in zip(left[:overlap], right[:overlap])),
        "xor_zero_bytes": xor.count(0),
        "chunk_size": chunk_size,
        "left_chunks": len(left_hashes),
        "right_chunks": len(right_hashes),
        "identical_chunks_same_offset": same_offset,
        "shared_unique_chunk_values": len(shared_unique),
        "shared_chunk_instances": sum(min(left_counts[value], right_counts[value]) for value in shared_unique),
        "largest_matching_chunk_ranges": matches[:30],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=pathlib.Path)
    parser.add_argument("right", type=pathlib.Path)
    parser.add_argument("--chunk-size", type=int, default=256)
    arguments = parser.parse_args()
    print(json.dumps(compare(arguments.left, arguments.right, arguments.chunk_size), indent=2))


if __name__ == "__main__":
    main()
