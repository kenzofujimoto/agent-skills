#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Any

TEMP_SUFFIXES = {".crdownload", ".part", ".partial", ".tmp"}


def snapshot(directory: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not directory.exists():
        return result
    for path in directory.iterdir():
        if path.is_file():
            try:
                stat = path.stat()
            except OSError:
                continue
            result[path.name] = {"size": stat.st_size, "mtime_ns": stat.st_mtime_ns}
    return result


def is_temp(path: Path) -> bool:
    lower = path.name.lower()
    return path.suffix.lower() in TEMP_SUFFIXES or lower.endswith(".crdownload")


def file_signature(path: Path) -> str:
    try:
        head = path.read_bytes()[:16]
    except OSError:
        return "unknown"
    if head.startswith(b"PK\x03\x04"):
        return "zip"
    if head[:4] == b"glTF":
        return "glb"
    stripped = head.lstrip()
    if stripped.startswith(b"{"):
        return "json-or-gltf"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--write-baseline")
    parser.add_argument("--after-file")
    parser.add_argument("--extensions", default=".zip,.glb,.gltf")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--stable-seconds", type=float, default=2.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    directory = Path(os.path.expandvars(os.path.expanduser(args.directory))).resolve()
    directory.mkdir(parents=True, exist_ok=True)

    if args.write_baseline:
        baseline_path = Path(args.write_baseline)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"directory": str(directory), "created": time.time(), "files": snapshot(directory)}
        baseline_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(str(baseline_path))
        return 0

    if not args.after_file:
        parser.error("--after-file is required unless --write-baseline is used")

    baseline_data = json.loads(Path(args.after_file).read_text(encoding="utf-8-sig"))
    baseline = baseline_data.get("files", {})
    extensions = {x.strip().lower() for x in args.extensions.split(",") if x.strip()}
    deadline = time.time() + args.timeout
    stable: dict[str, tuple[int, float]] = {}

    while time.time() < deadline:
        current = snapshot(directory)
        candidates: list[Path] = []
        for name, meta in current.items():
            path = directory / name
            if is_temp(path):
                continue
            old = baseline.get(name)
            changed = old is None or old.get("size") != meta.get("size") or old.get("mtime_ns") != meta.get("mtime_ns")
            if not changed:
                continue
            sig = file_signature(path)
            if path.suffix.lower() in extensions or sig in {"zip", "glb", "json-or-gltf"}:
                candidates.append(path)

        candidates.sort(key=lambda p: p.stat().st_mtime_ns, reverse=True)
        for path in candidates:
            size = path.stat().st_size
            previous = stable.get(path.name)
            now = time.time()
            if previous and previous[0] == size and now - previous[1] >= args.stable_seconds:
                result = {
                    "path": str(path),
                    "name": path.name,
                    "size": size,
                    "signature": file_signature(path),
                    "mtime_ns": path.stat().st_mtime_ns,
                }
                print(json.dumps(result, ensure_ascii=False) if args.json else str(path))
                return 0
            if not previous or previous[0] != size:
                stable[path.name] = (size, now)
        time.sleep(1)

    print("Timed out waiting for a completed browser download.", file=os.sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
