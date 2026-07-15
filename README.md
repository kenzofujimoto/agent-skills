# Agent Skills

Reusable agent skills for Codex, Claude Code, and compatible AI coding agents. This repository provides versioned, auditable skill packages plus cross-platform tools for installation, authoring, synchronization, validation, and releases.

[Português (Brasil)](README.pt-BR.md) · English

## Available skills

| Skill | Version | Category | Status | Description | Source |
| --- | --- | --- | --- | --- | --- |
| `motion-site-builder` | 1.3.0 | frontend / motion / design | stable | Plans and implements premium animated sites and WebGL experiences. | [`skills/motion-site-builder`](skills/motion-site-builder) |

## Compatibility

Skills use the portable `SKILL.md` convention and support:

- Codex at `~/.codex/skills`;
- ChatGPT/Codex app workspaces;
- Claude Code at `~/.claude/skills`;
- compatible agents using the generic `~/.agents/skills` directory.

## Quick install

Clone this repository, then install one or more targets.

### Windows

```powershell
.\scripts\install-skill.ps1 -Name motion-site-builder -Targets agents,codex,claude
```

### macOS/Linux

```bash
./scripts/install-skill.sh motion-site-builder agents,codex,claude
```

## Invoke a skill

Start a compatible agent and reference the skill by name:

```text
$motion-site-builder
```

Then describe the site, audience, constraints, and desired motion language.

## Update a skill

Pull the repository and rerun the installer. Maintainers can import the most complete local installation with:

```powershell
.\scripts\sync-skill.ps1 -Name motion-site-builder -Source auto
```

Repository-specific `README.md` and `CHANGELOG.md` files are preserved during synchronization.

## Create a skill

```powershell
.\scripts\new-skill.ps1 -Name my-new-skill
```

```bash
./scripts/new-skill.sh my-new-skill
```

The command copies the professional template, substitutes placeholders, creates version `0.1.0`, and adds a draft manifest entry. See [Adding a skill](docs/adding-a-skill.md).

## Package a release

```powershell
.\scripts\package-skill.ps1 -Name motion-site-builder
```

```bash
./scripts/package-skill.sh motion-site-builder
```

Packages are written to `dist/<name>-v<version>.zip` with an adjacent SHA-256 file. `SKILL.md` is placed at the archive root.

## Optional integrations

`motion-site-builder` can coordinate with:

- [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) for optional design-system research;
- [scroll-world](https://github.com/oso95/scroll-world) through an optional browser workflow.

Neither project is included in or maintained by this repository.

## Security and licensing

Never commit credentials, browser profiles, cookies, private assets, or `.env` files. Run `python scripts/validate_repo.py` before every contribution and report vulnerabilities according to [SECURITY.md](SECURITY.md).

Original code and documentation are MIT licensed. References, external libraries, and linked assets retain their own licenses; see [THIRD_PARTY.md](THIRD_PARTY.md).

## Roadmap

- Expand the catalog with focused frontend and agent-operations skills.
- Publish machine-verifiable provenance and compatibility metadata.
- Add more installer smoke tests across Windows, macOS, and Linux.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [the skill format](docs/skill-format.md), and [the release process](docs/release-process.md). Open a focused pull request with validation output and no third-party assets.
