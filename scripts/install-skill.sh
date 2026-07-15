#!/usr/bin/env bash
set -euo pipefail

name="${1:-}"
targets="${2:-agents}"
if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: name must be a lowercase hyphenated slug." >&2
  exit 2
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/$name"
[[ -f "$source_dir/SKILL.md" ]] || { echo "Error: missing $source_dir/SKILL.md" >&2; exit 1; }

IFS=',' read -r -a requested <<< "$targets"
for target in "${requested[@]}"; do
  case "$target" in agents|codex|claude) ;; *) echo "Error: unknown target '$target'." >&2; exit 2 ;; esac
  base="$HOME/.$target/skills"
  destination="$base/$name"
  staging="$(mktemp -d "$base/.${name}.installing.XXXXXX" 2>/dev/null || true)"
  if [[ -z "$staging" ]]; then mkdir -p "$base"; staging="$(mktemp -d "$base/.${name}.installing.XXXXXX")"; fi
  trap 'rm -rf "$staging"' EXIT
  cp -R "$source_dir/." "$staging/"
  find "$staging" -type d \( -name __pycache__ -o -name node_modules -o -name dist -o -name build -o -name downloads -o -name private-assets -o -name generated-assets -o -name .scroll-world -o -name .scroll-world-chrome \) -prune -exec rm -rf {} +
  find "$staging" -type f \( -name '*.pyc' -o -name '*.log' -o -name '*.zip' -o -name '*.crdownload' -o -name '*.mp4' -o -name '*.mov' -o -name '*.webm' -o -name '.env' -o -name '.env.*' \) ! -name '.env.example' -delete
  [[ -f "$staging/SKILL.md" ]] || { echo "Error: staged installation is invalid." >&2; exit 1; }
  rm -rf "$destination"
  mv "$staging" "$destination"
  trap - EXIT
  echo "Installed $name -> $destination"
done
