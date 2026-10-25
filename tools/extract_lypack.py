#!/usr/bin/env python3
"""Extract SmartBox lylink packed ZIP members with per-file CRC verification.

The vendor masks the first 128 bytes with a repeating seven-byte XOR key and
also modifies the ZIP directory/trailer. Local headers retain CRC and lengths,
so extraction does not depend on reconstructing the damaged ZIP end record.
This tool only writes a new local directory and has no device/network support.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path, PurePosixPath

HEAD_KEY = b"ya-iepc"
LOCAL_HEADER = struct.Struct("<4s5H3I2H")
MAX_MEMBER_SIZE = 32 * 1024 * 1024


def unpack(data: bytes) -> list[tuple[str, bytes, dict[str, object]]]:
    if len(data) < 128 or not data.endswith(b"wcaolypackfile"):
        raise ValueError("not a supported lylink pack")
    plain = bytearray(data)
    for offset in range(128):
        plain[offset] ^= HEAD_KEY[offset % len(HEAD_KEY)]
    position = 0
    members = []
    names = set()
    while plain[position:position + 4] == b"PK\x03\x04":
        if position + LOCAL_HEADER.size > len(plain):
            raise ValueError("truncated local header")
        (_, _, flags, method, _, _, crc, compressed_size, size,
         name_size, extra_size) = LOCAL_HEADER.unpack_from(plain, position)
        if flags & 9 or method != 8:
            raise ValueError("unsupported encrypted/data-descriptor/compression flags")
        if size > MAX_MEMBER_SIZE:
            raise ValueError("member exceeds extraction limit")
        name_start = position + LOCAL_HEADER.size
        start = name_start + name_size + extra_size
        end = start + compressed_size
        if end > len(plain):
            raise ValueError("truncated compressed member")
        name = bytes(plain[name_start:name_start + name_size]).decode("utf-8")
        parts = PurePosixPath(name)
        if (not name or "\\" in name or ":" in name or parts.is_absolute()
                or any(part in ("..", ".") for part in parts.parts)
                or len(parts.parts) != 1 or name in names):
            raise ValueError(f"unsafe or duplicate member name: {name!r}")
        inflater = zlib.decompressobj(-15)
        content = inflater.decompress(bytes(plain[start:end]), size + 1)
        if (not inflater.eof or inflater.unconsumed_tail or inflater.unused_data
                or len(content) != size or zlib.crc32(content) != crc):
            raise ValueError(f"length/deflate/CRC failure: {name}")
        names.add(name)
        members.append((name, content, {
            "name": name, "local_header_offset": position,
            "compressed_size": compressed_size, "size": size,
            "crc32": f"{crc:08X}",
            "sha256": hashlib.sha256(content).hexdigest().upper(),
        }))
        position = end
    if not members or plain[position:position + 4] != b"PK\x01\x02":
        raise ValueError("expected central directory after local members")
    return members


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output directory must not already exist")
    data = args.pack.read_bytes()
    members = unpack(data)  # Validate every member before creating any output.
    args.output.mkdir(parents=True)
    for name, content, metadata in members:
        (args.output / name).write_bytes(content)
        print(f"{metadata['sha256']}  {name}  size={len(content)} CRC=OK")
    manifest = {
        "source_sha256": hashlib.sha256(data).hexdigest().upper(),
        "validation": "all local-header sizes and deflate CRC32 values verified",
        "members": [metadata for _, _, metadata in members],
    }
    (args.output / "_lypack_metadata.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
