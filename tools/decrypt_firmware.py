#!/usr/bin/env python3
"""Offline decryptor for cpbox-abroad OTA images.

The 256-byte XOR table was independently validated against the local 5234 image
after it was published in catplay-labs/catplay-firmware issue 4.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import re


XOR_KEY = bytes.fromhex(
    "1269544837f0d56e927e26c3e525c5ee2a968b51ab10f2a9dc1d1b54b2a0a4b5"
    "faf8fd31e9d2a07b50c63e36eb03246613bfb73fc0a9e89cc704f079a4952e9e"
    "7e3bd077fd70f24e3630842133a887c77742e40df6f32c895249915fbe9164e0"
    "af2d03c12bd809974759061c808fbd48b1a155c8958151e7cbe2478974ab6a13"
    "696dd40445de9b8d37a2a9b73167ff02375e0617e8eeb4aff2a42897395735c7"
    "62053e807530ceab6052cd94fa545b513361697b4f1d2a42c152d9fba90ec22c"
    "2401ac89317a3592cc0226c6568117e94ca0ba4346b40f2e925f1d080d750005"
    "620dc92322fdd4486c6f4f6fd52788a108a5ca9dd61b85a1fecc2b7277958550"
)
HEADER = re.compile(rb"^([0-9a-fA-F]{32})  update\.swu\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=pathlib.Path)
    parser.add_argument("output_directory", type=pathlib.Path)
    arguments = parser.parse_args()

    encrypted = arguments.image.read_bytes()
    decrypted = bytes(value ^ XOR_KEY[index & 0xFF] for index, value in enumerate(encrypted))
    header = HEADER.match(decrypted)
    if header is None:
        raise SystemExit("Decrypted image does not contain the expected update.swu MD5 header")

    swu = decrypted[header.end() :]
    if not swu.startswith((b"070701", b"070702")):
        raise SystemExit("Decrypted payload is not a newc/CRC CPIO archive")

    expected_md5 = header.group(1).decode("ascii").lower()
    actual_md5 = hashlib.md5(swu).hexdigest()  # nosec: vendor container verification
    if actual_md5 != expected_md5:
        raise SystemExit(f"SWU MD5 mismatch: expected {expected_md5}, got {actual_md5}")

    arguments.output_directory.mkdir(parents=True, exist_ok=True)
    (arguments.output_directory / "update.decrypted.img").write_bytes(decrypted)
    (arguments.output_directory / "md5.txt").write_bytes(decrypted[: header.end()])
    (arguments.output_directory / "update.swu").write_bytes(swu)

    print(f"encrypted_sha256={hashlib.sha256(encrypted).hexdigest().upper()}")
    print(f"decrypted_sha256={hashlib.sha256(decrypted).hexdigest().upper()}")
    print(f"swu_size={len(swu)}")
    print(f"swu_md5={actual_md5}")
    print(f"swu_sha256={hashlib.sha256(swu).hexdigest().upper()}")
    print(f"header_size={header.end()}")


if __name__ == "__main__":
    main()
