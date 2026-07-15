# Scroll World Browser

`scroll-world-browser` builds cinematic landing pages where scrolling scrubs through a sequence of generated video clips. It combines browser-assisted media generation, asset preparation, a framework-independent playback engine, and explicit fallbacks for mobile and reduced motion.

## Capabilities

- Converts a brand or product journey into a sequence of connected scenes.
- Generates style-consistent stills and image-to-video transitions through supported browser providers.
- Tracks explicit, bounded provider-credit approvals without treating a general generation request as spending authorization.
- Prepares desktop and mobile encodes with `ffmpeg`.
- Connects clips to a scroll timeline using the included scrub engine.
- Defines recovery steps for provider drift, broken transitions, encoding problems, and mobile playback issues.

## Requirements

- A compatible headed browser automation tool such as `agent-browser`.
- User-controlled accounts for any selected image or video provider.
- Python 3 and `ffmpeg` for the asset pipeline.
- A local web server for playback testing.

The workflow pauses for login, account selection, 2FA, CAPTCHA, terms, or any payment decision outside an explicit user-approved budget. It must never copy passwords, cookies, browser profiles, or session tokens into project files.

## Installation

```powershell
.\scripts\install-skill.ps1 -Name scroll-world-browser -Targets agents,codex,claude
```

```bash
./scripts/install-skill.sh scroll-world-browser agents,codex,claude
```

## Usage

```text
$scroll-world-browser Build a scroll-driven product journey with five connected scenes and a lightweight mobile fallback.
```

Start by defining the scenes, provider constraints, media budget, and reduced-motion behavior. Generated images and videos remain project artifacts and are never distributed with this skill.

## Internal structure

- `SKILL.md`: complete browser-provider workflow and safety rules.
- `references/browser-pipeline.md`: provider-neutral browser sequence.
- `references/autonomous-browser.md`: command-oriented automation playbook.
- `references/prepare-assets.py`: manifest and media preparation utility.
- `references/scrub-engine.js`: portable playback engine.
- `references/index-template.html`: minimal integration template.

## Provenance and licensing

This browser-provider edition is derived from [oso95/scroll-world](https://github.com/oso95/scroll-world) and includes local adaptations. The upstream project is MIT licensed; its license and copyright notice are preserved in `LICENSE`. See `UPSTREAM.md` for provenance details.

Generated media, fonts, provider outputs, and brand assets are not covered by the skill's MIT license. Verify their individual terms before publication.

## Contributing

Keep browser instructions provider-aware, preserve explicit spending boundaries, avoid authenticated data in fixtures, run the repository validator, and update `CHANGELOG.md` for user-visible changes.
