# Dedicated browser automation

Use the user's dedicated regular Chrome profile, never the everyday personal Chrome profile.

## Bootstrap

Before browser work, run from the target project when available:

```powershell
powershell -ExecutionPolicy Bypass -File `
  "$HOME\.agents\skills\motion-site-builder\scripts\ensure-motion-browser.ps1"
```

The script reuses:

- profile: `$HOME\.scroll-world-chrome`
- CDP port: `9222`

All browser commands must use:

```text
agent-browser --cdp 9222
```

Never use:

- `agent-browser --auto-connect`;
- Chrome for Testing;
- the user's personal Chrome profile;
- `--download-path`;
- `AGENT_BROWSER_DOWNLOAD_PATH`;
- CDP download behavior overrides such as `allowAndName`.

## Sketchfab browser procedure

1. Run the bootstrap and verify `agent-browser --cdp 9222 tab`.
2. Reuse an existing Sketchfab tab or open the Downloadable search page.
3. If login is absent, pause for exactly the login action; preserve all other state.
4. Search multiple queries and open candidates in separate tabs.
5. Use snapshots for DOM controls and screenshots for the WebGL viewer.
6. Inspect model, author, license and official downloadable status.
7. Do not infer a license from tags or description; use the explicit license shown by Sketchfab.
8. For a selected free downloadable model, click the official download control autonomously.
9. If a format modal appears, prefer glTF/GLB for web usage.
10. Use Chrome's normal Downloads folder. Do not alter browser download behavior.
11. Record a download baseline before clicking and wait for a new completed file afterward.
12. Validate by archive/file signature, not filename alone.

## Download monitoring

Example:

```powershell
py "$HOME\.agents\skills\motion-site-builder\scripts\wait_for_browser_download.py" `
  --directory "$HOME\Downloads" `
  --after-file ".\.motion-site\sketchfab-download-start.json" `
  --extensions ".zip,.glb,.gltf" `
  --timeout 300 `
  --json
```

Create the baseline immediately before clicking:

```powershell
py "$HOME\.agents\skills\motion-site-builder\scripts\wait_for_browser_download.py" `
  --directory "$HOME\Downloads" `
  --write-baseline ".\.motion-site\sketchfab-download-start.json"
```

The browser may be opened, minimized and operated autonomously. Pause only for protected
identity, CAPTCHA, paid purchase, new legal acceptance or unresolved license ambiguity.
