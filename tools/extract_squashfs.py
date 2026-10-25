#!/usr/bin/env python3
"""Extract a SquashFS 4.x image without mounting it.

Regular files and directories are materialized below the output directory.
Symlinks and special files are recorded in ``_squashfs_metadata.json`` rather
than being created, which keeps extraction safe and portable on Windows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from dissect.squashfs import SquashFS


def safe_name(name: str) -> str:
    if name in {"", ".", ".."} or "/" in name or "\\" in name:
        raise ValueError(f"unsafe SquashFS entry name: {name!r}")
    return name


def extract(image: Path, output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    output_resolved = output.resolve()
    records: list[dict[str, object]] = []

    with image.open("rb") as fh:
        fs = SquashFS(fh)

        def walk(node, destination: Path, archive_path: str) -> None:
            for child in node.iterdir():
                name = safe_name(child.name)
                target = destination / name
                if output_resolved not in target.resolve().parents:
                    raise ValueError(f"entry escapes output directory: {archive_path}/{name}")

                child_path = f"{archive_path}/{name}" if archive_path else name
                common = {
                    "path": child_path,
                    "mode": oct(child.mode),
                    "uid": child.uid,
                    "gid": child.gid,
                    "mtime": child.mtime.isoformat(),
                }

                if child.is_dir():
                    target.mkdir(exist_ok=True)
                    records.append({**common, "type": "directory"})
                    walk(child, target, child_path)
                elif child.is_file():
                    digest = hashlib.sha256()
                    size = 0
                    with child.open() as source, target.open("wb") as sink:
                        while chunk := source.read(1024 * 1024):
                            sink.write(chunk)
                            digest.update(chunk)
                            size += len(chunk)
                    records.append(
                        {**common, "type": "file", "size": size, "sha256": digest.hexdigest().upper()}
                    )
                elif child.is_symlink():
                    records.append({**common, "type": "symlink", "target": child.link})
                else:
                    records.append({**common, "type": "special"})

        walk(fs.root, output, "")
        manifest = {
            "source": str(image.resolve()),
            "squashfs": {
                "version": f"{fs.major}.{fs.minor}",
                "block_size": fs.block_size,
                "bytes_used": fs.size,
                "mkfs_time": fs.mkfs_time.isoformat(),
            },
            "entries": sorted(records, key=lambda item: str(item["path"])),
        }

    metadata = output / "_squashfs_metadata.json"
    metadata.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"image not found: {args.image}")
    if args.output.exists() and any(args.output.iterdir()):
        parser.error(f"output directory is not empty: {args.output}")

    manifest = extract(args.image, args.output)
    counts: dict[str, int] = {}
    for entry in manifest["entries"]:
        entry_type = str(entry["type"])
        counts[entry_type] = counts.get(entry_type, 0) + 1
    print(json.dumps({"output": str(args.output.resolve()), "counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
