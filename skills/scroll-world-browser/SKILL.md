---
name: scroll-world-browser
description: >
  Build an immersive scroll-scrubbed fly-through landing page for any industry or brand.
  Generate cohesive scene stills with ChatGPT Images or Gemini Images and motion clips with
  Gemini, Google Flow, Sora, or another browser-accessible image-to-video product. Use a
  headed browser workflow that can operate ChatGPT Images and Google Flow end to end through
  agent-browser, pausing only for login, 2FA, CAPTCHA, paid confirmations, or genuinely ambiguous
  visual choices. Then post-process with ffmpeg and wire the portable framework-agnostic scrub engine. Use for a 3D world,
  diorama landing, cinematic product journey, or continuous scroll-driven camera experience.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# scroll-world — browser-provider edition

Produces a landing page where scroll drives pre-rendered video. The page does not render a
live 3D world; it scrubs a chain of generated clips and overlays section copy.

The original frontend engine remains provider-independent. This edition changes only the
asset-generation workflow: no Higgsfield CLI is required.

## Autonomous browser contract — default when requested

When the user asks Codex/Claude Code to control the browser, run the provider workflow rather
than merely printing prompts or stopping at a generic manual checkpoint.

The agent must:

1. Use `agent-browser --auto-connect` with the user's already-open, authenticated **regular
   Chrome** whenever available. On Windows this is preferred over Chrome for Testing because
   Google may reject sign-in from an automation build.
2. Discover existing tabs with `agent-browser --auto-connect tab`, switch to the appropriate
   ChatGPT/Flow tab, and take a fresh `snapshot -i` before interacting.
3. Read prompt files locally, fill the provider composer, upload required references, submit,
   wait for completion, inspect the result, download it, rename/move it to the exact expected
   path, and validate it locally before continuing.
4. Continue through all missing stills and clips automatically. Do **not** ask the user to copy
   prompts, upload routine reference files, rename downloads, or run ordinary validation steps.
5. Pause only for a concrete human-only action: login, account selection, 2FA, CAPTCHA, terms,
   a paid-credit confirmation not covered by an explicit user-approved budget, or selection
   between multiple visually plausible outputs.
   State the exact action needed, keep the browser open, and resume after the user says it is done.
6. Never extract or persist passwords, cookies, session tokens, recovery codes, or private
   authenticated endpoints. Never bypass provider safeguards, quotas, rate limits, or paywalls.
7. Treat every UI element reference as ephemeral: refresh the snapshot after navigation,
   generation completion, modal changes, uploads, and downloads.
8. Never claim an asset exists until its expected local file is present, non-empty, and readable.

If `agent-browser.json` reports `expected value at line 1 column 1`, repair it automatically by
rewriting valid JSON as UTF-8 **without BOM**. Do not stop just to ask the user to repair it.

Read `references/autonomous-browser.md` for the command-oriented execution playbook.

## Budgeted provider-credit approvals

Provider-credit confirmations do not require a human checkpoint when the user has explicitly
authorized both a maximum cost per generation and a maximum accumulated total for the current
project.

When such an authorization exists:

1. Keep `.scroll-world/credit-ledger.json` as the local source of truth for the authorized
   limits, approved entries, accumulated spend and remaining balance.
2. Before clicking an approval control, verify that the generation is in the authorized project
   scope, the disclosed cost does not exceed the per-generation limit, and the new accumulated
   total would not exceed the total limit.
3. Within all limits, click **Approve** automatically and append the approved cost to the ledger.
4. Count an approval against the budget even when the generation later fails, is rejected or is
   regenerated.
5. Stop before approval if the provider omits or ambiguously states the cost, the operation is
   outside the authorized scope, or either limit would be exceeded.

Never infer a budget from a general request to generate assets. It must be explicit and bounded.

## Non-negotiable honesty rule

Browser products do not all expose deterministic first-frame and last-frame controls.
Never claim a seam is pixel-identical unless the generated files actually prove it.

Use one of these continuity grades:

1. **Grade A — sequential extend/edit (recommended):** start with one clip, then use the
   provider's edit/extend workflow to continue the existing shot into the next scene.
2. **Grade B — two-reference bridge:** generate separate scene clips; extract the previous
   last frame and next first frame; upload both as references for a connector; add a short
   crossfade during encoding.
3. **Grade C — editorial crossfade:** when the provider cannot bridge or extend, join clips
   with a restrained ffmpeg crossfade at a low-motion moment. State clearly that this is a
   polished transition, not a truly frame-locked continuous take.

Do not silently downgrade. Record `continuity_grade` in `project.json`.

## Step 0 — Bootstrap

Required:

- A logged-in browser session for at least one image provider and one video provider.
- `ffmpeg` and `ffprobe` on `$PATH`.
- Python 3.10+.
- The original `references/scrub-engine.js`, `index-template.html`, and optionally
  `knockout.py` from this repository.

Browser automation (required for autonomous mode):

- `agent-browser` on `$PATH`.
- Prefer the user's regular Chrome through `agent-browser --auto-connect`.
- The user performs only login, CAPTCHA, 2FA, account selection, terms, sensitive confirmations,
  and paid confirmations not covered by an explicit bounded credit budget. All routine prompting,
  uploads, downloads, renaming, validation and in-budget approvals are agent work.
- Never ask for or store a password in project files.

Create a project manifest from `references/project.example.json`. Then run:

```bash
# macOS/Linux
python3 references/prepare-assets.py prompts --project project.json --work .scroll-world

# Windows PowerShell
py references/prepare-assets.py prompts --project project.json --work .scroll-world
```

On Windows, prefer `py` in every command shown below when `python3` is unavailable.
This writes deterministic prompt files and the expected asset checklist.

## Step 1 — Interview the user

Collect only what cannot be sensibly inferred:

1. Subject/business and one-line pitch.
2. Brand name and either a supplied palette or permission to propose one.
3. Art direction. Default: soft matte clay diorama, isometric, warm studio light.
4. Ordered journey of 5–7 scenes.
5. Desktop only or desktop + mobile beta.
6. Browser providers available to the user:
   - stills: `chatgpt` or `gemini`;
   - video: `gemini`, `flow`, `sora`, or `manual`.
7. Continuity grade. Recommend Grade A whenever edit/extend is available.

For each section capture:

- `id`, `label`, `subject`, `focal_point`;
- `eyebrow`, `title`, `body`, `tags`;
- optional `scroll`, `linger`, `accent`, and final CTA.

## Step 2 — Generate a style anchor

Before generating all scenes, create one approved style-anchor image.

Prompt shape:

```text
[STYLE PREAMBLE]
Create a visual style anchor for a connected world about [SUBJECT]. Show one representative
miniature environment containing [ANCHOR SUBJECT]. This image defines the camera angle,
materials, lighting, palette and level of detail for every later scene. No text, letters,
numbers or logos. Landscape 3:2, centered composition.
```

Save it as:

```text
.scroll-world/source/style-anchor.png
```

Inspect it and present it for approval. Pause only for this visual approval when the user has not
already delegated selection criteria. Once approved, continue automatically with all remaining
stills.

### ChatGPT Images workflow

- Keep all still generation in one project conversation.
- Upload the approved style anchor with every scene request or keep it in the active chat
  context.
- Ask to preserve camera angle, material language, lighting and palette while changing only
  the scene subject.
- Download the full-resolution result to the exact expected filename.

### Gemini Images workflow

- Use one project conversation/library item.
- Use the style anchor as a reference image; multiple references may be used when helpful.
- Preserve the same art direction and composition rules.
- Download the full-size result to the exact expected filename.

Browser automation must perform routine image selection and final download when the accepted
result is unambiguous. Ask the user only when multiple variants are genuinely plausible or the UI
requires a human-only confirmation.

## Step 3 — Generate all scene stills

Prompt files are created at:

```text
.scroll-world/prompts/still_<section>.txt
```

Expected outputs:

```text
.scroll-world/source/still_<section>.png
```

Rules:

- Use the identical style preamble and approved anchor for every scene.
- Generate scenes sequentially or in small batches so visual drift is caught early.
- Keep focal content centered because mobile uses a center crop.
- Regenerate any scene whose angle, palette, lighting or material treatment visibly drifts.
- Convert approved stills to site-ready WebP later with `prepare-assets.py encode-stills`.

## Step 4 — Choose the video architecture

### Architecture A — sequential extend/edit (recommended)

Use when Gemini/Flow/Sora exposes a workflow that can edit, extend, re-cut, or continue an
existing video.

- Leg 0 starts from `still_<first>.png`.
- Leg 1+ uses the previous rendered video as the source/reference and instructs the provider
  to continue the same shot into the next scene.
- Every leg begins by continuing the previous velocity and ends with a calm forward drift.
- Prefer a single provider and model for the full chain.
- Export each accepted leg as `.scroll-world/source/leg_<section>.mp4`.
- No separate connectors are required.

This is the best browser-only substitute for the original frame-handoff pipeline because the
provider works on the prior shot rather than reconstructing it from scratch.

### Architecture B — separate scene clips + generated bridges

Use when the provider supports image/video references but not reliable extension.

1. Generate `dive_<section>.mp4` from each scene still.
2. Extract the actual last and first frames:

```bash
python3 references/prepare-assets.py extract-frames --project project.json --work .scroll-world
```

3. For each adjacent pair, upload both boundary frames and ask for a connector that begins
   from the first reference and arrives at the second reference.
4. Save connectors as `.scroll-world/source/conn_01.mp4`, etc.
5. During encoding, add a short crossfade because references do not guarantee exact pixels.

### Architecture C — direct crossfade fallback

Use independent scene clips and let the post-processing pipeline join them with short
crossfades. Choose moments with low camera velocity and similar framing. This is acceptable
for an MVP but must not be described as frame-locked.

## Step 5 — Browser video provider playbook

Read `references/browser-pipeline.md` before interacting with a provider.

### Gemini Apps

Recommended browser default when available:

- can use image/video references;
- supports iterative video edits in a conversation;
- use Grade A by uploading the prior clip and asking to continue/change the destination;
- otherwise upload the scene still for a new clip or both boundary images for a bridge.

### Google Flow

Best option when the user's plan includes Flow:

- create reusable ingredients from the approved style anchor and scene stills;
- use SceneBuilder/extend for Grade A continuity;
- keep camera controls and the same project/assets across the entire journey.

### Sora

Use only when currently available to the user:

- upload an image or video as source;
- prefer Re-cut/Storyboard/Remix/Blend workflows over isolated text-to-video generations;
- do not build brittle unattended automation around an interface that may change;
- user confirms the accepted variant and downloads the MP4.

## Step 6 — Validate and post-process

Validate expected files:

```bash
python3 references/prepare-assets.py validate --project project.json --work .scroll-world
```

Encode approved source clips:

```bash
python3 references/prepare-assets.py encode-videos \
  --project project.json --work .scroll-world --assets ./assets
```

Add `--mobile` only when the user opted into mobile beta.

The helper:

- strips audio;
- preserves native resolution for desktop;
- encodes H.264/yuv420p, CRF 20, GOP 8, faststart;
- creates optional 720p mobile variants with GOP 4;
- converts stills to WebP;
- never upscales a source video.

## Step 7 — Assemble the page

Use the original `references/scrub-engine.js` and configure it from generated assets.

Generate a config snippet:

```bash
python3 references/prepare-assets.py emit-config \
  --project project.json --assets ./assets > scroll-world-config.js
```

For Architecture A, `connectors` is empty. For B, it contains `conn01.mp4`, etc. For C,
prefer empty connectors and set a slightly larger engine crossfade, or pre-compose the clips
before wiring them.

Keep copy chrome quiet; the generated world is the visual identity.

## Step 8 — QA

Always verify:

- every expected still/video exists and is non-empty;
- no clip contains an accidental hard cut or unrelated subject;
- section copy appears over the intended scene;
- desktop scrubbing tracks scroll smoothly;
- `video.seekable.end(0) > 0` after blob loading;
- transitions look acceptable in both scroll directions;
- reduced-motion falls back to stills;
- mobile beta serves `-m.mp4`, does not blank on iOS, and keeps focal subjects in crop.

Continuity-specific QA:

- Grade A: inspect each leg boundary for velocity and content continuity.
- Grade B: compare screenshots immediately before/after each seam; tune crossfade or
  regenerate the connector when a visible pop remains.
- Grade C: disclose that the transition is editorial and optimize it rather than pretending
  it is continuous.

## Gotchas

- **Browser selectors change:** use semantic labels and fresh snapshots; never hardcode a
  long-lived element reference.
- **Authentication:** the user signs in interactively. Never store credentials in scripts.
- **Generation still running:** do not busy-loop aggressively; re-check at reasonable
  intervals and let the user use other tabs/chats.
- **Wrong downloaded variant:** verify resolution, duration and filename with `ffprobe`.
- **Style drift:** return to the same conversation and re-upload the style anchor.
- **Seam pop:** browser references are not guaranteed endpoint locks. Regenerate, lengthen a
  gentle crossfade, or switch to sequential edit/extend.
- **Camera rewind:** the next clip must continue the previous velocity; end each leg with a
  slow forward drift.
- **Mobile stutter:** use the 720p GOP-4 encode and the original engine's seek coalescing.
- **Frozen frame 0:** serve through the original engine's Blob-loading path.

## References

- `references/prompts.md` — provider-neutral prompts.
- `references/browser-pipeline.md` — provider workflow and recovery rules.
- `references/autonomous-browser.md` — one-shot browser operation playbook.
- `references/project.example.json` — manifest schema example.
- `references/prepare-assets.py` — prompt generation, validation, extraction, encoding and
  config emission.
- Original unchanged files: `scrub-engine.js`, `index-template.html`, `knockout.py`.

<!-- safe-browser-download-isolation-v2 -->
## Safe browser download isolation

- Never pass `--download-path` when using `agent-browser --auto-connect`.
- Never set `AGENT_BROWSER_DOWNLOAD_PATH` while connected to the user's regular Chrome.
- Never modify the regular Chrome download behavior through CDP.
- Never use `allowAndName` download behavior.
- Native downloads in the user's regular Chrome must keep Chrome's default filenames and download directory.
- For ChatGPT images, prefer retrieving the selected image URL or creating a clean image-only natural-resolution capture instead of clicking the native Download button.
- For Flow videos, use Chrome's ordinary download behavior, then detect the newest completed file in the regular Downloads directory.
- Wait until no `.crdownload` file remains before moving or renaming a completed download.
- Move the completed file into `.scroll-world/source/` only after validating its type and contents.
- Browser automation must use a dedicated regular-Chrome profile rather than the user's everyday Chrome profile.
<!-- /safe-browser-download-isolation-v2 -->

<!-- autonomous-browser-bootstrap-v3 -->
## Autonomous dedicated-browser bootstrap

Before every browser workflow, run:

powershell -ExecutionPolicy Bypass -File .\scripts\ensure-scroll-world-browser.ps1

The bootstrap script is responsible for:

- detecting whether CDP port 9222 is available;
- launching the dedicated regular Chrome automatically when it is absent;
- using the persistent profile `$HOME\.scroll-world-chrome`;
- opening ChatGPT and Google Flow;
- waiting until CDP is ready;
- confirming the connection with `agent-browser --cdp 9222 tab`.

Never ask the user to open the browser manually.

Never use:

- `agent-browser --auto-connect`;
- Chrome for Testing;
- the user's personal Chrome profile;
- `--download-path` through CDP;
- `chrome://inspect/#remote-debugging`.

All browser commands after bootstrap must use:

agent-browser --cdp 9222

The dedicated Chrome may be launched, minimized and reused automatically.

Pause only when login has expired, or when 2FA, CAPTCHA, terms, an unbudgeted payment
confirmation, a credit approval outside its explicit limits, or another protected provider
interaction genuinely requires the user.
<!-- /autonomous-browser-bootstrap-v3 -->
