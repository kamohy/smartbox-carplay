#!/usr/bin/env python3
"""Static, non-modifying inspection of SmartBox firmware images."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import pathlib
import statistics
import zlib


MAGICS = {
    "elf": b"\x7fELF",
    "gzip": b"\x1f\x8b\x08",
    "xz": b"\xfd7zXZ\x00",
    "zip": b"PK\x03\x04",
    "squashfs_le": b"hsqs",
    "squashfs_be": b"sqsh",
    "ubifs": b"\x31\x18\x10\x06",
    "uimage": b"\x27\x05\x19\x56",
    "fit_fdt": b"\xd0\x0d\xfe\xed",
    "cpio_newc": b"070701",
    "cpio_crc": b"070702",
    "zstd": b"\x28\xb5\x2f\xfd",
}


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = collections.Counter(data)
    size = len(data)
    return -sum((count / size) * math.log2(count / size) for count in counts.values())


def printable_strings(data: bytes, minimum: int = 8) -> list[str]:
    found: list[str] = []
    current = bytearray()
    for value in data:
        if 32 <= value <= 126:
            current.append(value)
        else:
            if len(current) >= minimum:
                found.append(current.decode("ascii"))
            current.clear()
    if len(current) >= minimum:
        found.append(current.decode("ascii"))
    return found


def single_byte_xor_hits(data: bytes, magic: bytes, limit: int = 16) -> list[dict[str, int]]:
    hits: list[dict[str, int]] = []
    first = magic[0]
    end = len(data) - len(magic) + 1
    for offset in range(max(0, end)):
        key = data[offset] ^ first
        if key == 0:
            continue
        if all((data[offset + index] ^ key) == expected for index, expected in enumerate(magic)):
            hits.append({"offset": offset, "key": key})
            if len(hits) >= limit:
                break
    return hits


def inspect(path: pathlib.Path, block_size: int) -> dict[str, object]:
    data = path.read_bytes()
    block_entropies = [entropy(data[index : index + block_size]) for index in range(0, len(data), block_size)]
    strings = printable_strings(data)
    repeated_16 = collections.Counter(data[index : index + 16] for index in range(0, len(data) - 15, 16))
    duplicate_blocks = sum(count - 1 for count in repeated_16.values() if count > 1)
    repeated_samples = []
    for block, count in repeated_16.most_common(12):
        if count < 2:
            break
        offsets = [
            index
            for index in range(0, len(data) - 15, 16)
            if data[index : index + 16] == block
        ][:12]
        repeated_samples.append({"hex": block.hex().upper(), "count": count, "offsets": offsets})
    signature_hits = {
        name: [offset for offset in range(len(data)) if data.startswith(magic, offset)][:16]
        for name, magic in MAGICS.items()
    }
    xor_hits = {name: single_byte_xor_hits(data, magic) for name, magic in MAGICS.items()}
    compressed = zlib.compress(data, level=9)
    chunk_repetition = {}
    for chunk_size in (16, 32, 64, 128, 256, 512, 4096):
        chunks = [data[index : index + chunk_size] for index in range(0, len(data) - chunk_size + 1, chunk_size)]
        counts = collections.Counter(chunks)
        block, count = counts.most_common(1)[0]
        chunk_repetition[str(chunk_size)] = {
            "duplicate_chunks": sum(value - 1 for value in counts.values() if value > 1),
            "most_common_count": count,
            "most_common_prefix_hex": block[:32].hex().upper(),
            "first_offsets": [
                index * chunk_size for index, candidate in enumerate(chunks) if candidate == block
            ][:12],
        }

    return {
        "path": str(path.resolve()),
        "size": len(data),
        "size_mod_16": len(data) % 16,
        "sha256": hashlib.sha256(data).hexdigest().upper(),
        "header_hex": data[:64].hex().upper(),
        "tail_hex": data[-64:].hex().upper(),
        "entropy_bits_per_byte": round(entropy(data), 6),
        "block_size": block_size,
        "block_entropy": {
            "count": len(block_entropies),
            "minimum": round(min(block_entropies), 6),
            "maximum": round(max(block_entropies), 6),
            "mean": round(statistics.mean(block_entropies), 6),
            "stdev": round(statistics.pstdev(block_entropies), 6),
            "lowest_blocks": sorted(
                (
                    {"offset": index * block_size, "entropy": round(value, 6)}
                    for index, value in enumerate(block_entropies)
                ),
                key=lambda item: item["entropy"],
            )[:8],
        },
        "zlib_recompression_ratio": round(len(compressed) / len(data), 6),
        "aligned_16_byte_duplicate_blocks": duplicate_blocks,
        "top_repeated_16_byte_blocks": repeated_samples,
        "aligned_chunk_repetition": chunk_repetition,
        "plain_signature_hits": signature_hits,
        "single_byte_xor_signature_hits": xor_hits,
        "printable_strings": {
            "count_min_8": len(strings),
            "longest": sorted(strings, key=len, reverse=True)[:20],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=pathlib.Path)
    parser.add_argument("--block-size", type=int, default=65536)
    arguments = parser.parse_args()
    print(json.dumps(inspect(arguments.image, arguments.block_size), indent=2))


if __name__ == "__main__":
    main()
