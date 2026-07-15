#!/usr/bin/env python3
"""Validate repository structure, metadata, portability, and publish safety."""

from __future__ import annotations

import compileall
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "work",
    "outputs",
    "__pycache__",
}
FORBIDDEN_DIRS = {
    "__pycache__",
    "downloads",
    "private-assets",
    "generated-assets",
    ".scroll-world",
    ".scroll-world-chrome",
}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".zip",
    ".log",
    ".crdownload",
    ".mp4",
    ".mov",
    ".webm",
    ".glb",
    ".gltf",
    ".fbx",
    ".obj",
    ".blend",
}
MAX_FILE_BYTES = 2 * 1024 * 1024
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
ABSOLUTE_USER_PATH = re.compile(
    r"(?:[A-Za-z]:\\Users\\[^\\\s]+|/Users/[^/\s]+|/home/[^/\s]+)", re.IGNORECASE
)
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "API secret": re.compile(r"\b(?:sk|rk)_[A-Za-z0-9]{24,}\b"),
    "authorization value": re.compile(
        r"Authorization\s*[:=]\s*(?:Bearer|Basic)\s+(?!<|\$\{|\$[A-Z_]+)[A-Za-z0-9._~+/=-]{16,}",
        re.IGNORECASE,
    ),
    "assigned secret": re.compile(
        r"(?:password|passwd|client[_-]?secret|access[_-]?token|oauth[_-]?token)\s*[:=]\s*[\"']?(?!<|\$\{|\$[A-Z_]+|example|your-|replace-)[A-Za-z0-9._~+/=-]{16,}",
        re.IGNORECASE,
    ),
}


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checked_files = 0

    def error(self, message: str) -> None:
        self.errors.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_repository_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def load_json(path: Path, validation: Validation) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        validation.error(f"Invalid JSON {relative(path)}: {exc}")
        return None


def validate_manifest(validation: Validation) -> list[dict[str, Any]]:
    path = ROOT / "skills.json"
    if not path.is_file():
        validation.error("Missing skills.json")
        return []
    data = load_json(path, validation)
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        validation.error("skills.json must use schemaVersion 1")
        return []
    skills = data.get("skills")
    if not isinstance(skills, list):
        validation.error("skills.json skills must be an array")
        return []
    seen: set[str] = set()
    for entry in skills:
        if not isinstance(entry, dict):
            validation.error("Every skills.json entry must be an object")
            continue
        name = entry.get("name")
        version = entry.get("version")
        path_value = entry.get("path")
        if not isinstance(name, str) or not SLUG.fullmatch(name):
            validation.error(f"Invalid skill name in manifest: {name!r}")
        elif name in seen:
            validation.error(f"Duplicate skill in manifest: {name}")
        else:
            seen.add(name)
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            validation.error(f"Invalid semantic version for {name}: {version!r}")
        expected_path = f"skills/{name}" if isinstance(name, str) else None
        if path_value != expected_path:
            validation.error(f"Manifest path for {name} must be {expected_path}")
    return [entry for entry in skills if isinstance(entry, dict)]


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        validation.error(f"Cannot read {relative(path)}: {exc}")
        return {}
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        validation.error(f"Missing YAML frontmatter in {relative(path)}")
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if item:
            values[item.group(1)] = item.group(2).strip()
    for required in ("name", "description"):
        if not values.get(required):
            validation.error(f"Frontmatter in {relative(path)} requires {required}")
    return values


def validate_skills(entries: list[dict[str, Any]], validation: Validation) -> None:
    skills_root = ROOT / "skills"
    if not skills_root.is_dir():
        validation.error("Missing skills directory")
        return
    manifest_names = {entry.get("name") for entry in entries}
    disk_names = {path.name for path in skills_root.iterdir() if path.is_dir()}
    for name in sorted(disk_names):
        if not SLUG.fullmatch(name):
            validation.error(f"Invalid skill folder name: {name}")
        if name not in manifest_names:
            validation.error(f"Skill folder is not registered in skills.json: {name}")
    for entry in entries:
        name = entry.get("name")
        if not isinstance(name, str):
            continue
        folder = skills_root / name
        if not folder.is_dir():
            validation.error(f"Missing skill folder: skills/{name}")
            continue
        for filename in ("SKILL.md", "README.md", "CHANGELOG.md"):
            if not (folder / filename).is_file():
                validation.error(f"Missing skills/{name}/{filename}")
        skill_file = folder / "SKILL.md"
        if skill_file.is_file():
            frontmatter = parse_frontmatter(skill_file, validation)
            if frontmatter.get("name") != name:
                validation.error(f"Frontmatter name does not match folder for {name}")
        version_file = folder / "VERSION"
        if version_file.is_file():
            version = version_file.read_text(encoding="utf-8").strip()
            if version != entry.get("version"):
                validation.error(f"VERSION does not match skills.json for {name}")


def validate_required_scripts(validation: Validation) -> None:
    required = {
        "install-skill.ps1",
        "install-skill.sh",
        "new-skill.ps1",
        "new-skill.sh",
        "sync-skill.ps1",
        "package-skill.ps1",
        "package-skill.sh",
        "validate_repo.py",
    }
    for filename in sorted(required):
        if not (ROOT / "scripts" / filename).is_file():
            validation.error(f"Missing scripts/{filename}")


def validate_relative_references(path: Path, text: str, validation: Validation) -> None:
    candidates: set[str] = set()
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        candidates.add(target.split("#", 1)[0])
    for target in re.findall(r"`((?:references|recipes|scripts|templates)/[A-Za-z0-9._/-]+)`", text):
        candidates.add(target)
    for target in candidates:
        if not target or re.match(r"^(?:https?://|mailto:|#)", target, re.IGNORECASE):
            continue
        target = target.split()[0].strip("<>")
        resolved = (path.parent / target).resolve()
        if not resolved.exists() and target.split("/", 1)[0] in {"references", "recipes", "scripts", "templates"}:
            skill_root = next((parent for parent in (path.parent, *path.parents) if (parent / "SKILL.md").is_file()), None)
            if skill_root is not None:
                resolved = (skill_root / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            validation.error(f"Reference escapes repository in {relative(path)}: {target}")
            continue
        if not resolved.exists():
            validation.error(f"Missing reference in {relative(path)}: {target}")


def validate_files(validation: Validation) -> None:
    for path in iter_repository_files():
        validation.checked_files += 1
        rel = path.relative_to(ROOT)
        lower_name = path.name.lower()
        if any(part in FORBIDDEN_DIRS for part in rel.parts):
            validation.error(f"Forbidden directory content: {relative(path)}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            validation.error(f"Forbidden file type: {relative(path)}")
        if lower_name == ".env" or (lower_name.startswith(".env.") and lower_name != ".env.example"):
            validation.error(f"Forbidden environment file: {relative(path)}")
        if path.stat().st_size > MAX_FILE_BYTES:
            validation.error(f"File exceeds {MAX_FILE_BYTES} bytes: {relative(path)}")
        if path.suffix.lower() == ".json":
            load_json(path, validation)
        if path.suffix.lower() not in {".md", ".py", ".ps1", ".sh", ".json", ".yml", ".yaml", ".txt", ""}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            validation.error(f"Cannot read text file {relative(path)}: {exc}")
            continue
        if path.resolve() != Path(__file__).resolve() and ABSOLUTE_USER_PATH.search(text):
            validation.error(f"Absolute user path found in {relative(path)}")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                validation.error(f"Probable {label} found in {relative(path)}")
        if path.suffix.lower() == ".md":
            validate_relative_references(path, text, validation)


def validate_python(validation: Validation) -> None:
    with tempfile.TemporaryDirectory(prefix="agent-skills-pycache-") as cache:
        previous = sys.pycache_prefix
        sys.pycache_prefix = cache
        try:
            for folder in (ROOT / "scripts", ROOT / "skills"):
                if folder.exists() and not compileall.compile_dir(folder, quiet=1, force=True):
                    validation.error(f"Python compilation failed under {relative(folder)}")
        finally:
            sys.pycache_prefix = previous


def main() -> int:
    validation = Validation()
    entries = validate_manifest(validation)
    validate_skills(entries, validation)
    validate_required_scripts(validation)
    validate_files(validation)
    validate_python(validation)
    if validation.errors:
        print(f"Validation failed with {len(validation.errors)} error(s):")
        for error in validation.errors:
            print(f"- {error}")
        return 1
    print(f"Validation passed: {validation.checked_files} files checked, {len(entries)} skill(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
