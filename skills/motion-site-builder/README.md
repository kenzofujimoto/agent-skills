# Motion Site Builder

`motion-site-builder` is an architecture and implementation skill for premium animated websites, dynamic frontends, and WebGL experiences. It turns a product brief into a section-by-section experience plan, selects an appropriate motion stack, and adds explicit accessibility and performance checks.

## Capabilities

- Routes briefs through multi-industry profiles and experience archetypes.
- Maps each section to DOM, 2.5D, video, canvas, WebGL, Rive, or Lottie.
- Defines media ownership, loading, fallback, licensing, and reduced-motion contracts.
- Selects between GSAP, Motion, Three.js/React Three Fiber, shaders, and compositing patterns.
- Curates references as evidence rather than templates to copy.
- Evaluates 3D assets for topology, format, licensing, attribution, and runtime cost.

## Section architecture and media contracts

The workflow creates a motion plan per section: narrative purpose, visual layer, animation owner, interaction, breakpoint behavior, fallback, budget, and QA criteria. Media contracts define when an asset loads, who controls it, how it degrades, and whether it can legally ship.

## Industry routing

Industry profiles pair audience expectations with trust signals, content priorities, visual risks, and suitable archetypes. The router can propose a primary profile and adjacent profiles when a product spans industries.

## Sketchfab workflow

Sketchfab discovery is browser-assisted and optional. Search, license review, attribution capture, download, inspection, and optimization are separate gates. No model is bundled with this repository, and a model must not ship until its individual license is verified.

## Bundled companion skills

- [`ui-ux-pro-max`](../ui-ux-pro-max) contributes design-system and interface research.
- [`scroll-world-browser`](../scroll-world-browser) supports browser-assisted cinematic media workflows.

Both companion skills are included in this repository and can be installed alongside `motion-site-builder`. Their upstream projects, licenses, and provenance remain documented in their respective directories.

## Installation

From the repository root:

```powershell
.\scripts\install-skill.ps1 -Name motion-site-builder -Targets agents,codex,claude
```

```bash
./scripts/install-skill.sh motion-site-builder agents,codex,claude
```

## Usage examples

```text
$motion-site-builder Design a launch site for an electric aircraft with a restrained WebGL hero.
```

```text
$motion-site-builder Audit this landing page's motion architecture, reduced-motion behavior, and mobile performance.
```

## Limitations and policies

The skill does not replace product strategy, brand approval, accessibility testing with users, device profiling, or legal review. Browser automation can fail when providers change their interfaces.

Do not remove provider watermarks or attribution unless the applicable license and plan explicitly permit it. Do not disguise preview output as licensed production output. Every 3D model must have documented provenance, license, attribution requirements, and redistribution permission before publication.

## Internal structure

- `SKILL.md`: agent workflow and rules.
- `references/`: architecture, industries, archetypes, providers, QA, and asset guidance.
- `recipes/`: implementation patterns.
- `scripts/`: routing, validation, inspection, and browser helpers.
- `templates/`: briefs, profiles, plans, and evaluation records.

## Contributing and changelog

Keep guidance portable, validate JSON and Python, avoid third-party assets, and update [CHANGELOG.md](CHANGELOG.md). Repository-wide contribution rules are in the root `CONTRIBUTING.md`.
