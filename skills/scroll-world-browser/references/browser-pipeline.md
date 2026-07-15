# Browser-assisted generation pipeline

This workflow is designed for consumer browser products. It is intentionally headed and
autonomous for routine operations, with narrowly scoped human checkpoints only when required.

## Operating principles

1. Prefer `agent-browser --auto-connect` to control the user's authenticated regular Chrome.
2. The user signs in interactively only when authentication is actually required.
3. Use semantic locators and refresh snapshots after every major UI change.
4. Never enter account passwords from a project file or terminal history.
5. Never bypass CAPTCHA, 2FA, rate limits, quotas or product safeguards.
6. A generated asset is not complete until it is downloaded, renamed and validated locally.
7. Do not send the user away to copy prompts, upload routine files, or rename downloads.

## Session setup with agent-browser

### Preferred: authenticated regular Chrome

Recent Google sign-in flows may reject Chrome for Testing. When regular Chrome is open with
remote debugging enabled, use:

```bash
agent-browser --auto-connect tab
agent-browser --auto-connect tab <chatgpt-tab-id>
agent-browser --auto-connect snapshot -i
```

Open a fresh provider tab through the connected browser only when needed. Keep the tab ID or URL
in the active task notes; do not assume element refs survive navigation.

If the project config is malformed or BOM-prefixed, repair it automatically. On PowerShell:

```powershell
$config = '{"headed":true,"hideScrollbars":false,"downloadPath":".scroll-world/downloads"}'
[System.IO.File]::WriteAllText(
  (Join-Path $PWD 'agent-browser.json'),
  $config,
  [System.Text.UTF8Encoding]::new($false)
)
```

### Fallback: dedicated headed browser

Use only when authentication already works in that browser or the user explicitly chooses it:

```bash
agent-browser --headed --session scroll-chatgpt open https://chatgpt.com/
agent-browser --headed --session scroll-flow open https://flow.google/
```

Ask the user to complete login only if required. Never collect their credentials. After every
navigation, generation completion, modal, or download, take a new snapshot.

## Image generation loop

For each prompt file:

1. Open the project conversation/library item.
2. Attach `style-anchor.png` for scene prompts.
3. Fill the prompt from `.scroll-world/prompts/still_<id>.txt`.
4. Submit.
5. Wait for generation completion without aggressive polling.
6. Select the correct variant automatically when unambiguous; otherwise ask one focused visual-choice question.
7. Download full size through the visible UI.
8. Move/rename to `.scroll-world/source/still_<id>.png`.
9. Run `prepare-assets.py validate` before continuing.

When file upload/download is not exposed reliably, try semantic UI controls and the configured
download directory. Use a user-assisted checkpoint only for the exact blocked upload/download
action; never use DOM hacks or authenticated private endpoints.

## Gemini/Flow sequential video loop — recommended

### First leg

1. Open Create video or the Flow project.
2. Attach `still_<first>.png`.
3. Submit `.scroll-world/prompts/leg_<first>.txt`.
4. Review the result, especially the last second.
5. Download as `.scroll-world/source/leg_<first>.mp4`.

### Later legs

1. Start an edit/extend/SceneBuilder action from the prior accepted video.
2. Submit `.scroll-world/prompts/leg_<next>.txt`.
3. Confirm there is no restart, cut, lens jump or backward camera movement at the beginning.
4. Confirm the final second settles into a forward drift.
5. Download as `.scroll-world/source/leg_<next>.mp4`.

Do not generate the next leg from only a prose description when a prior-video edit/extend
workflow is available.

## Sora workflow

When Sora is available to the user:

- use uploaded image/video sources;
- prefer Re-cut, Storyboard, Remix or Blend from an accepted generation;
- keep the user's selected variant as the source of the next operation;
- use a manual download checkpoint;
- expect UI changes and avoid unattended selectors.

## Two-reference bridge loop

After independent dives exist:

```bash
python3 references/prepare-assets.py extract-frames --project project.json --work .scroll-world
```

For each `bridge_XX.txt`:

1. Attach `.scroll-world/frames/last_<left>.png` first.
2. Attach `.scroll-world/frames/first_<right>.png` second.
3. Submit the bridge prompt.
4. Download to `.scroll-world/source/conn_XX.mp4`.
5. Inspect beginning/end visually; reference conditioning is not exact frame locking.

## Validation after every download

```bash
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 .scroll-world/source/<file>
```

Reject files that are empty, unexpectedly short, portrait when landscape was required, or
contain audio when the project is intended to be silent.

## Recovery

- UI changed: snapshot again and use semantic text/role locators.
- Generation failed: retry only the failed asset.
- Style drift: return to the original project conversation and reattach the style anchor.
- Video begins with a jump: regenerate via edit/extend from the prior accepted clip.
- Bridge still pops: regenerate, shorten motion near endpoints, or increase the encoding
  crossfade slightly.
