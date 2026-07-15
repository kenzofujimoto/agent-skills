#!/usr/bin/env bash
set -euo pipefail

name="${1:-}"
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: name must be a lowercase hyphenated slug." >&2
  exit 2
fi
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$repo_root/scripts/validate_repo.py"
python3 - "$repo_root" "$name" <<'PY'
import hashlib
import json
import sys
import zipfile
from pathlib import Path

root, name = Path(sys.argv[1]), sys.argv[2]
manifest = json.loads((root / "skills.json").read_text(encoding="utf-8"))
entries = [entry for entry in manifest["skills"] if entry["name"] == name]
if len(entries) != 1:
    raise SystemExit(f"Expected exactly one manifest entry for {name!r}.")
entry = entries[0]
source = root / entry["path"]
if not (source / "SKILL.md").is_file():
    raise SystemExit(f"Skill {name!r} is missing SKILL.md.")
dist = root / "dist"
dist.mkdir(exist_ok=True)
archive = dist / f"{name}-v{entry['version']}.zip"
excluded_dirs = {"__pycache__", "node_modules", "dist", "build", "downloads", "private-assets", "generated-assets", ".scroll-world", ".scroll-world-chrome"}
excluded_suffixes = {".pyc", ".log", ".zip", ".crdownload", ".mp4", ".mov", ".webm"}
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
    for path in sorted(source.rglob("*")):
        rel = path.relative_to(source)
        if not path.is_file() or any(part in excluded_dirs for part in rel.parts):
            continue
        if path.suffix.lower() in excluded_suffixes or path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
            continue
        package.write(path, rel.as_posix())
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
checksum = archive.with_suffix(".zip.sha256")
checksum.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
print(f"Created {archive}")
print(f"SHA256 {digest}")
PY
