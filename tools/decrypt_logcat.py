#!/usr/bin/env python3
"""Decrypt and unpack SmartBox cpbox logcat exports."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pathlib
import struct
import zlib


KEY = b"liaoyuan.tech\x00"
RESET_SIZE = 1024
LENGTH_OFFSET = 0x333


def decrypt(data: bytes) -> bytes:
    return bytes(
        value ^ KEY[(offset % RESET_SIZE) % len(KEY)]
        for offset, value in enumerate(data)
    )


def unwrap(data: bytes) -> tuple[bytes, int | None]:
    """Remove CGI send_file's uint32 length insertion and short-file padding.

    Verified in the 5234 CGI: gzip bytes 0..818, original gzip size (LE uint32),
    remaining gzip bytes. Exports shorter than 1024 bytes are padded to 1024.
    XOR is applied to the *wire* layout and must be reversed before this step.
    """
    if len(data) >= RESET_SIZE:
        declared = struct.unpack_from("<I", data, LENGTH_OFFSET)[0]
        if declared > 0 and len(data) == max(RESET_SIZE, declared + 4):
            gzip_data = data[:LENGTH_OFFSET] + data[LENGTH_OFFSET + 4:]
            return gzip_data[:declared], declared
    return data, None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path)
    parser.add_argument("--metadata", type=pathlib.Path)
    parser.add_argument(
        "--salvage",
        action="store_true",
        help="explicitly allow unverified partial output if strict gzip/CRC validation fails",
    )
    arguments = parser.parse_args()

    encrypted = arguments.input.read_bytes()
    wire_plain = decrypt(encrypted)
    decrypted, embedded_size = unwrap(wire_plain)
    if not decrypted.startswith(b"\x1f\x8b\x08"):
        raise SystemExit("Decryption did not produce a gzip stream")
    trailer_valid = False
    try:
        plain = gzip.decompress(decrypted)
        trailer_valid = True
    except (gzip.BadGzipFile, EOFError, zlib.error) as error:
        if not arguments.salvage:
            raise SystemExit(f"gzip validation failed: {error}") from error
        inflater = zlib.decompressobj(31)
        chunks: list[bytes] = []
        try:
            for offset in range(0, len(decrypted), 64):
                chunks.append(inflater.decompress(decrypted[offset : offset + 64]))
            chunks.append(inflater.flush())
        except zlib.error:
            pass
        plain = b"".join(chunks)
        if not plain:
            raise SystemExit(f"gzip salvage failed: {error}") from error
    arguments.output.write_bytes(plain)
    metadata = {
        "encrypted_size": len(encrypted),
        "encrypted_sha256": hashlib.sha256(encrypted).hexdigest().upper(),
        "embedded_gzip_size": embedded_size,
        "removed_length_offset": LENGTH_OFFSET if embedded_size is not None else None,
        "decrypted_gzip_sha256": hashlib.sha256(decrypted).hexdigest().upper(),
        "plain_size": len(plain),
        "plain_sha256": hashlib.sha256(plain).hexdigest().upper(),
        "gzip_crc_and_size_valid": trailer_valid,
    }
    if arguments.metadata:
        arguments.metadata.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"encrypted_size={len(encrypted)}")
    print(f"encrypted_sha256={hashlib.sha256(encrypted).hexdigest().upper()}")
    print(f"embedded_gzip_size={embedded_size}")
    print(f"decrypted_gzip_sha256={hashlib.sha256(decrypted).hexdigest().upper()}")
    print(f"plain_size={len(plain)}")
    print(f"plain_sha256={hashlib.sha256(plain).hexdigest().upper()}")
    print(f"gzip_trailer_valid={str(trailer_valid).lower()}")


if __name__ == "__main__":
    main()
