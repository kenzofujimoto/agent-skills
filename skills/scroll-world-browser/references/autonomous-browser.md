# Autonomous browser playbook

Use this playbook when the user wants one instruction to run the whole provider pipeline.

## Entry conditions

- Work from the project root containing `project.json` and `.scroll-world/prompts/`.
- Prefer regular Chrome through `agent-browser --auto-connect`.
- Ensure ChatGPT and Google Flow are authenticated; pause only when authentication truly blocks the next action.
- Never use Higgsfield.

## Bootstrap

```powershell
agent-browser --version
ffmpeg -version
ffprobe -version
rg --version
py --version
agent-browser --auto-connect tab
```

If `agent-browser.json` is invalid, rewrite it as UTF-8 without BOM:

```powershell
$config = @'
{
  "headed": true,
  "hideScrollbars": false,
  "downloadPath": ".scroll-world/downloads"
}
'@
[System.IO.File]::WriteAllText(
  (Join-Path $PWD 'agent-browser.json'),
  $config,
  [System.Text.UTF8Encoding]::new($false)
)
```

## Tab selection

1. List tabs.
2. Select the ChatGPT tab by URL/title and take `snapshot -i`.
3. Later select Flow by URL/title and take `snapshot -i`.
4. Avoid unrelated personal tabs.
5. Re-list tabs when IDs change.

## ChatGPT image loop

For each missing image in order:

1. Read its prompt file exactly.
2. Switch to the dedicated ChatGPT project chat or start a dedicated new chat.
3. For scene stills, upload `.scroll-world/source/style-anchor.png` first.
4. Fill the composer and submit.
5. Wait at reasonable intervals; refresh snapshot after completion.
6. Inspect with screenshot when needed.
7. Choose an unambiguous result automatically. If two or more are equally viable, ask the user to choose.
8. Click the normal full-resolution download control.
9. Locate the newly downloaded file, move it to the expected `.scroll-world/source/` name, and verify it with Pillow or ffprobe/file metadata.
10. Continue to the next missing asset.

Do not regenerate files that already exist and pass validation unless the user requests it.

## Google Flow video loop

1. Switch to the authenticated Flow tab/project.
2. First leg: upload the first still and submit `leg_<first>.txt`.
3. Later legs: use edit/extend/SceneBuilder from the previously accepted video. Do not start independent text-to-video shots when extend/edit exists.
4. Pause before a paid-credit confirmation only when the provider presents one explicitly.
5. Download accepted MP4s and move them to their exact expected names.
6. Run ffprobe for duration, dimensions, codec, size, and audio streams.
7. Reject obvious restarts, unrelated subjects, portrait output, or accidental audio.

## Human-only pauses

Pause only for:

- login/account selection;
- 2FA or CAPTCHA;
- terms or consent;
- paid-credit confirmation;
- a genuinely ambiguous visual choice;
- a provider control that cannot be operated through exposed accessible UI.

State exactly one action. Keep the browser/session open. After the user says it is done, re-snapshot and continue from the same step.

## Completion

After all source files validate:

```powershell
py references/prepare-assets.py validate --project project.json --work .scroll-world
py references/prepare-assets.py encode-videos --project project.json --work .scroll-world --assets .\assets
py references/prepare-assets.py emit-config --project project.json --assets .\assets
```

Then assemble and QA the page. Never report completion while an expected source file is missing.
