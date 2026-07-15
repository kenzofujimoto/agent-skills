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
    assert manifest["skills"] == [
        {
            "name": "motion-site-builder",
            "version": "1.3.0",
            "status": "stable",
            "path": "skills/motion-site-builder",
            "description": "Architecture and implementation skill for premium animated websites, dynamic frontends and WebGL experiences.",
            "categories": ["frontend", "motion-design", "ui-ux", "threejs", "gsap"],
            "targets": ["agents", "codex", "claude"],
        }
    ]


def test_repository_validator_passes() -> None:
    result = run_command([sys.executable, "scripts/validate_repo.py"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Validation passed" in result.stdout


def test_package_script_creates_flat_skill_archive() -> None:
    result = run_command(
        [
            "pwsh",
            "-NoProfile",
            "-File",
            "scripts/package-skill.ps1",
            "-Name",
            "motion-site-builder",
        ]
    )
    assert result.returncode == 0, result.stdout + result.stderr
    archive = REPO_ROOT / "dist/motion-site-builder-v1.3.0.zip"
    checksum = archive.with_suffix(".zip.sha256")
    assert archive.is_file()
    assert checksum.is_file()
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
    assert "SKILL.md" in names
    assert not any(name.startswith("motion-site-builder/") for name in names)
    assert not any("__pycache__" in name for name in names)


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
