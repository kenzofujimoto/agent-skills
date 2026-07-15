# UI/UX Pro Max

`ui-ux-pro-max` is a searchable design-intelligence skill for creating and reviewing web and mobile interfaces. It combines structured datasets, reasoning rules, and stack-specific guidance to produce design systems rather than isolated visual suggestions.

This bundled copy tracks the official stable upstream release `v2.11.0`.

## Capabilities

- Recommends product patterns, interface styles, color palettes, and typography pairings.
- Generates a complete design-system proposal with rationale and anti-patterns.
- Searches focused UX, accessibility, motion, icon, chart, and landing-page guidance.
- Provides implementation recommendations for React, Next.js, Vue, Svelte, Tailwind, shadcn/ui, Flutter, SwiftUI, React Native, Three.js, and additional stacks.
- Persists a master design system with optional page-level overrides.
- Supports terminal and Markdown output.

## Installation

```powershell
.\scripts\install-skill.ps1 -Name ui-ux-pro-max -Targets agents,codex,claude
```

```bash
./scripts/install-skill.sh ui-ux-pro-max agents,codex,claude
```

## Usage

Invoke the skill:

```text
$ui-ux-pro-max Design a trustworthy healthcare dashboard with accessible data visualization.
```

Run the search engine directly from an installed skill directory:

```bash
python3 scripts/search.py "healthcare SaaS dashboard trustworthy" --design-system -p "Care Console"
python3 scripts/search.py "animation accessibility" --domain ux
python3 scripts/search.py "responsive forms" --stack react
```

Use `python` instead of `python3` when that is the configured executable on Windows.

## Workflow

1. Identify product type, audience, industry, tone, platform, and implementation stack.
2. Generate a complete design system before selecting individual details.
3. Supplement it with focused domain or stack searches.
4. Persist the design system when the project benefits from a durable source of truth.
5. Validate contrast, semantics, keyboard access, responsive layouts, motion preferences, and implementation quality.

## Internal structure

- `SKILL.md`: agent workflow, usage rules, and quality checklist.
- `data/`: curated CSV datasets and stack-specific guidance.
- `scripts/search.py`: command-line search interface.
- `scripts/core.py`: ranking and data-access core.
- `scripts/design_system.py`: design-system reasoning and persistence.

## Provenance and licensing

The skill is maintained upstream at [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill). This copy is pinned to tag `v2.11.0` and commit `6142b073958df645d0fb27e682428e69599386dc`. The upstream project is MIT licensed; the license and copyright notice are preserved in `LICENSE`. See `UPSTREAM.md`.

External fonts, icons, frameworks, and sites referenced by the datasets retain their own licenses and terms.

## Contributing

Prefer fixes upstream when they apply generally. Repository-specific changes must retain provenance, include tests for data or search behavior, pass `python ../../scripts/validate_repo.py`, and be recorded in `CHANGELOG.md`.
