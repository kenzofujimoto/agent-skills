from __future__ import annotations

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_command(command: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_manifest_has_motion_site_builder() -> None:
    manifest = json.loads((REPO_ROOT / "skills.json").read_text(encoding="utf-8"))
    assert manifest["schemaVersion"] == 1
    skills = {entry["name"]: entry for entry in manifest["skills"]}
    assert set(skills) == {"motion-site-builder", "scroll-world-browser", "ui-ux-pro-max"}
    assert skills["motion-site-builder"]["version"] == "1.3.0"
    assert skills["scroll-world-browser"]["version"] == "1.0.0"
    assert skills["ui-ux-pro-max"]["version"] == "2.11.0"
    for name, entry in skills.items():
        assert entry["status"] == "stable"
        assert entry["path"] == f"skills/{name}"
        assert entry["targets"] == ["agents", "codex", "claude"]


@pytest.mark.parametrize("name", ["scroll-world-browser", "ui-ux-pro-max"])
def test_bundled_dependency_has_license_and_provenance(name: str) -> None:
    skill = REPO_ROOT / "skills" / name
    for filename in ("SKILL.md", "README.md", "CHANGELOG.md", "VERSION", "LICENSE", "UPSTREAM.md"):
        assert (skill / filename).is_file(), f"missing skills/{name}/{filename}"
    assert "MIT License" in (skill / "LICENSE").read_text(encoding="utf-8")
    upstream = (skill / "UPSTREAM.md").read_text(encoding="utf-8")
    assert "https://github.com/" in upstream
    assert "MIT" in upstream


def test_repository_validator_passes() -> None:
    result = run_command([sys.executable, "scripts/validate_repo.py"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Validation passed" in result.stdout


@pytest.mark.parametrize(
    ("name", "version"),
    [
        ("motion-site-builder", "1.3.0"),
        ("scroll-world-browser", "1.0.0"),
        ("ui-ux-pro-max", "2.11.0"),
    ],
)
def test_package_script_creates_flat_skill_archive(name: str, version: str) -> None:
    result = run_command(
        [
            "pwsh",
            "-NoProfile",
            "-File",
            "scripts/package-skill.ps1",
            "-Name",
            name,
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    archive = REPO_ROOT / f"dist/{name}-v{version}.zip"
    checksum = archive.with_suffix(".zip.sha256")
    assert archive.is_file()
    assert checksum.is_file()
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
    assert "SKILL.md" in names
    assert not any(path.startswith(f"{name}/") for path in names)
    assert not any("__pycache__" in path for path in names)


def test_install_script_replaces_target_and_excludes_temporary_files(tmp_path: Path) -> None:
    fake_home = tmp_path / "home"
    result = run_command(
        [
            "pwsh",
            "-NoProfile",
            "-File",
            "scripts/install-skill.ps1",
            "-Name",
            "motion-site-builder",
            "-Targets",
            "agents,codex,claude",
            "-HomePath",
            str(fake_home),
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    for target in (".agents", ".codex", ".claude"):
        installed = fake_home / target / "skills/motion-site-builder"
        assert (installed / "SKILL.md").is_file()
        assert not list(installed.rglob("*.pyc"))


def test_new_skill_rejects_invalid_slug() -> None:
    result = run_command(
        [
            "pwsh",
            "-NoProfile",
            "-File",
            "scripts/new-skill.ps1",
            "-Name",
            "Invalid Skill",
        ]
    )
    assert result.returncode != 0
    assert "slug" in (result.stdout + result.stderr).lower()


@pytest.mark.parametrize(
    "script_name",
    [
        "install-skill.ps1",
        "install-skill.sh",
        "new-skill.ps1",
        "new-skill.sh",
        "sync-skill.ps1",
        "package-skill.ps1",
        "package-skill.sh",
    ],
)
def test_required_script_exists(script_name: str) -> None:
    assert (REPO_ROOT / "scripts" / script_name).is_file()
