# Installation

Clone the repository and run the installer from its root. Installers replace the selected target atomically after validating that the source contains `SKILL.md`.

Windows:

```powershell
.\scripts\install-skill.ps1 -Name motion-site-builder -Targets agents,codex,claude
```

macOS/Linux:

```bash
./scripts/install-skill.sh motion-site-builder agents,codex,claude
```

Available targets are `agents`, `codex`, and `claude`. Restart or reload the agent if it caches installed skills.
