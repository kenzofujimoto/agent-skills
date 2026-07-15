---
name: motion-site-builder
description: >
  Build premium animated websites and dynamic frontends by selecting the correct motion
  architecture per section: CSS/DOM motion, Motion, GSAP storytelling, framed media,
  layered 2.5D, video scrubbing, Three.js/React Three Fiber, Rive, Lottie, shaders,
  particle typography, licensed Sketchfab 3D assets, and industry-specific market patterns across 40+ niches. Coordinates ui-ux-pro-max for
  design intelligence and scroll-world-browser for browser-assisted AI media when installed.
  Use for animated landing pages, creative portfolios, cinematic product sites, interactive
  3D sections, scroll storytelling, and motion-system upgrades.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# Motion Site Builder

Build a coherent product experience, not a collage of effects.

## Companion skills

- `ui-ux-pro-max`: design system, UX, typography, color, layout, accessibility.
- `motion-site-builder`: motion architecture, media contracts, implementation and QA.
- `scroll-world-browser`: optional AI image/video generation when the motion plan requires it.

The current project remains the source of truth. Do not overwrite approved decisions silently.

## Core rule

Classify every important section before choosing media or libraries:

- `full-bleed-cinematic`
- `framed-media-stage`
- `transparent-layered-object`
- `layered-2.5d`
- `dom-motion`
- `interactive-vector`
- `webgl-scene`
- `video-scrub`

Do not force all sections into 16:9 video. Media must match its actual layout role.

## Read order

1. `references/architecture-selector.md`
2. `references/media-contracts.md`
3. `references/motion-budget.md`
4. `references/integration.md`
5. `references/industry-router.md`
6. `references/industry-index.md` and the selected industry files
7. `references/experience-archetypes.md`
8. `references/qa-checklist.md`
9. Read only the recipes selected by the motion plan.
10. For Sketchfab work, also read `references/sketchfab-assets.md`,
   `references/threejs-asset-evaluation.md` and `references/browser-automation.md`.

## Non-negotiable rules

1. Resolve hierarchy, grid, typography, color and accessibility before choreography.
2. Use one dominant motion language, one secondary language and at most two showcase sections
   by default.
3. No visible provider watermark in shipped media. Do not crop, conceal, blur or inpaint it.
4. No blind upscaling. Reject media that cannot support the intended display size.
5. No unexplained zoom. `fit`, `objectPosition`, safe area and scale must be explicit.
6. Motion must reveal hierarchy, state, causality, continuity or depth.
7. `prefers-reduced-motion` is required.
8. Heavy effects must lazy-load, pause offscreen and clean up on route changes.
9. References are analyzed as principles, never copied as proprietary layouts or assets.
10. Use only licensed, officially downloadable 3D assets and preserve attribution.
11. Sketchfab acquisition is browser-first. Never ask for an OAuth application or access token unless the user explicitly requests API integration.
12. Never apply a creative-tech aesthetic blindly across industries. Industry semantics, task archetype, trust level and content requirements constrain the motion system.

## Workflow

### 0 — Inspect

- Detect the existing stack from project files.
- Read `AGENTS.md`, project briefs, design systems, animation code and media.
- Detect companion skills and available local/browser tools.
- Never migrate a working stack only to use a preferred library.

### 1 — Classify industry and experience

Before visual design, classify the project on two axes:

- primary industry plus at most two secondary industries;
- one or more experience archetypes describing the job the website must perform.

Read `references/industry-router.md`, run `scripts/industry_router.py`, then create
`industry-profile.json`. Use the strictest applicable trust, accessibility, claims and
performance constraints. Re-open selected reference URLs in the browser and analyze their
current desktop/mobile behavior; the catalog is a seed, not a cached truth.

Validate with `scripts/validate_industry_profile.py`.

### 2 — Resolve design system

Use `ui-ux-pro-max` first when installed. Retrieve or generate its persisted
`design-system/<project>/MASTER.md`, then read page overrides. Treat it as the source of truth
for visual and UX constraints.

When unavailable, document product type, audience, brand tone, typography, colors, spacing,
grid, accessibility and mobile behavior.

### 3 — Analyze references

For every URL or screenshot, extract:

- layout, hierarchy, typography and rhythm;
- full-bleed vs framed media;
- sticky/pinned sections;
- scroll-linked vs triggered motion;
- text splitting, cursor effects and transitions;
- canvas/WebGL, video, SVG, Rive/Lottie and shader signals;
- performance and accessibility risks.

Write `reference-profile.json`. Use `references/reference-analysis.md`.

### 4 — Create `motion-plan.json`

Required per section:

- `renderMode`
- `engine`
- `assetType`
- `containerRatio`
- `assetRatio`
- `fit`
- `objectPosition`
- `safeArea`
- `initialScale`
- `maxScale`
- `trigger`
- `backgroundStrategy`
- `reducedMotion`

Validate with `scripts/validate_motion_plan.py`.

### 5 — Select recipes

Use the lightest engine that expresses the experience:

- CSS: simple transitions and states.
- Motion: UI/layout/gesture animation.
- GSAP + ScrollTrigger: pinned narratives, scrub and complex timelines.
- Layered 2.5D: sharp stills with controlled depth.
- Rive: stateful interactive vector illustration.
- Lottie: small linear vector animation.
- Three.js/R3F: real depth, transparent objects, free camera and shaders.
- Video scrub: only clean, high-quality, watermark-free source footage.
- Particle typography: one focal experiment, never body copy.

### 6 — Source or generate assets

Only after layout contracts exist.

Use `scroll-world-browser` only when the plan genuinely needs generated media. Pass exact
aspect ratio, preferred resolution, safe area, first-frame contract, background strategy,
watermark policy and rejection rules.

For genuine 3D objects, evaluate downloadable Sketchfab models before generating fake 3D
video. Create `3d-asset-brief.json`, shortlist multiple candidates, verify license, inspect
viewer quality, download through the official authenticated browser control, audit glTF/GLB and optimize only a permitted project copy. The default workflow must not request an OAuth token.

### 7 — Implement

- Preserve the detected stack.
- Install only selected engines.
- Keep text and controls in the DOM.
- Prefer transform and opacity.
- Separate content data from orchestration.
- Scope and clean up timelines/listeners.
- Lazy-load WebGL, media and special sections.
- Smooth-scroll is optional, not a default.
- Progressive enhancement is mandatory.

### 8 — QA

Run `references/qa-checklist.md` and local scripts.

Minimum:

- desktop and mobile visual QA;
- keyboard and focus;
- reduced motion;
- no horizontal overflow or major CLS;
- no watermark, accidental crop or upscaling;
- console/network errors;
- media dimensions, codec and framing;
- WebGL cleanup and DPR cap;
- CPU-throttled usability;
- fallbacks for autoplay/WebGL/provider failure.

## Deliverables

```text
design-system/<project>/MASTER.md    # when companion skill is available
industry-profile.json                # always for a new project or major redesign
reference-profile.json               # when references were supplied
motion-plan.json
3d-asset-brief.json                  # when 3D sourcing is needed
3d-asset-shortlist.json              # when Sketchfab is searched
docs/motion-rationale.md
docs/3d-asset-rationale.md           # when applicable
public/assets/ optimized media/models
ATTRIBUTION.md or credits page       # when licenses require it
tests/ motion/accessibility checks
```
