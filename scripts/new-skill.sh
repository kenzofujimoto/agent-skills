#!/usr/bin/env bash
set -euo pipefail

name="${1:-}"
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: name must be a lowercase hyphenated slug." >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template="$repo_root/templates/skill-template"
destination="$repo_root/skills/$name"
[[ ! -e "$destination" ]] || { echo "Error: skill '$name' already exists; refusing to overwrite it." >&2; exit 1; }
cp -R "$template" "$destination"
python3 - "$repo_root" "$name" <<'PY'
import json
import sys
from datetime import date
from pathlib import Path

root, name = Path(sys.argv[1]), sys.argv[2]
folder = root / "skills" / name
title = " ".join(part.capitalize() for part in name.split("-"))
for path in folder.rglob("*"):
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        text = text.replace("{{SKILL_NAME}}", name).replace("{{SKILL_TITLE}}", title).replace("{{DATE}}", date.today().isoformat())
        path.write_text(text, encoding="utf-8")
manifest_path = root / "skills.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["skills"].append({
    "name": name, "version": "0.1.0", "status": "draft", "path": f"skills/{name}",
    "description": f"TODO: describe {name}.", "categories": ["uncategorized"],
    "targets": ["agents", "codex", "claude"],
})
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
PY
echo "Created skills/$name at version 0.1.0"
