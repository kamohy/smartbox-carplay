#!/usr/bin/env python3
"""Unpack the legacy Android boot image used by the SmartBox firmware."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import struct
from pathlib import Path


def align(value: int, boundary: int) -> int:
    return (value + boundary - 1) // boundary * boundary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    data = args.image.read_bytes()
    if data[:8] != b"ANDROID!":
        parser.error("not a legacy Android boot image")

    fields = struct.unpack_from("<10I", data, 8)
    kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size, second_addr, tags_addr, page_size, header_version, os_version = fields
    if page_size <= 0 or page_size & (page_size - 1):
        parser.error(f"invalid page size: {page_size}")

    name = data[48:64].split(b"\0", 1)[0].decode("ascii", errors="replace")
    kernel_offset = page_size
    ramdisk_offset = kernel_offset + align(kernel_size, page_size)
    second_offset = ramdisk_offset + align(ramdisk_size, page_size)
    recovery_dtbo_size = 0
    recovery_dtbo_offset = 0
    header_size = page_size
    dt_size = 0
    dt_addr = 0
    if header_version >= 1:
        recovery_dtbo_size = struct.unpack_from("<I", data, 1632)[0]
        recovery_dtbo_offset = struct.unpack_from("<Q", data, 1636)[0]
        header_size = struct.unpack_from("<I", data, 1644)[0]
    if header_version >= 2:
        dt_size = struct.unpack_from("<I", data, 1648)[0]
        dt_addr = struct.unpack_from("<Q", data, 1652)[0]
    dt_offset = second_offset + align(second_size, page_size)

    parts = {
        "kernel.gz": data[kernel_offset : kernel_offset + kernel_size],
        "ramdisk": data[ramdisk_offset : ramdisk_offset + ramdisk_size],
        "second": data[second_offset : second_offset + second_size],
        "recovery-dtbo": data[recovery_dtbo_offset : recovery_dtbo_offset + recovery_dtbo_size],
        "device-tree.dtb": data[dt_offset : dt_offset + dt_size],
    }
    args.output.mkdir(parents=True, exist_ok=True)
    written: dict[str, dict[str, object]] = {}
    for filename, content in parts.items():
        if not content:
            continue
        target = args.output / filename
        target.write_bytes(content)
        written[filename] = {
            "size": len(content),
            "sha256": hashlib.sha256(content).hexdigest().upper(),
        }

    if parts["kernel.gz"].startswith(b"\x1f\x8b"):
        raw_kernel = gzip.decompress(parts["kernel.gz"])
        target = args.output / "kernel.raw"
        target.write_bytes(raw_kernel)
        written[target.name] = {
            "size": len(raw_kernel),
            "sha256": hashlib.sha256(raw_kernel).hexdigest().upper(),
        }

    report = {
        "source": str(args.image.resolve()),
        "name": name,
        "page_size": page_size,
        "header_version": header_version,
        "header_size": header_size,
        "os_version": os_version,
        "addresses": {
            "kernel": f"0x{kernel_addr:08X}",
            "ramdisk": f"0x{ramdisk_addr:08X}",
            "second": f"0x{second_addr:08X}",
            "tags": f"0x{tags_addr:08X}",
            "dtb": f"0x{dt_addr:08X}",
        },
        "parts": written,
    }
    (args.output / "boot-image.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
