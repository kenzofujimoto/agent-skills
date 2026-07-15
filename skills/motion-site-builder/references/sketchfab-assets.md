# Sketchfab asset discovery and browser acquisition

Use Sketchfab as a licensed asset source, never as an unrestricted scraper.

## Default policy: browser first, no OAuth token

The normal workflow uses the dedicated authenticated Chrome profile and the official Sketchfab
website. Do **not** ask the user to register an OAuth application, obtain a client secret or
provide `SKETCHFAB_ACCESS_TOKEN`.

The public Data API may be used without authentication as a discovery supplement, but asset
acquisition must default to the official browser Download control.

Only discuss the Download API/OAuth path when the user explicitly asks for API integration.

## Browser workflow

1. Derive `3d-asset-brief.json` from `motion-plan.json`:
   - subject and semantic queries;
   - art direction;
   - target section and engine;
   - animation/rig needs;
   - background/transparency behavior;
   - maximum transfer, triangle, material and texture budgets;
   - commercial/modification requirements.
2. Start or reuse the dedicated Chrome browser through `references/browser-automation.md`.
3. Open Sketchfab's **Downloadable** model search and ensure the user is signed in.
4. Search multiple semantic and style variants.
5. Build a shortlist of 5–12 candidates before downloading anything.
6. Inspect each shortlisted model in the official viewer:
   - silhouette at the intended camera angle;
   - material and texture quality;
   - transparency and emissive behavior;
   - animation clips and loop quality;
   - rig deformation when relevant;
   - pivot, origin, scale and orientation;
   - hidden geometry and visible branding;
   - overall art-direction fit.
7. Read and record the visible model metadata:
   - model title and URL;
   - author and profile URL;
   - license name and license URL;
   - downloadable status;
   - animation indicators;
   - geometry/material metrics when shown;
   - attribution text.
8. Treat license as a hard gate:
   - reject NonCommercial for commercial/promotional work;
   - reject Editorial for marketing;
   - reject NoDerivatives when optimization or modification is required;
   - review ShareAlike obligations before accepting;
   - preserve attribution when required.
9. Score candidates with `templates/3d-asset-score.example.json` and write
   `3d-asset-shortlist.json`.
10. Select the highest-scoring license-compatible candidate.
11. Click the model's official **Download 3D Model** control in the browser.
12. Choose glTF/GLB or the closest web-compatible format offered by the official dialog.
13. Do not use a CDP download-path override. Let regular Chrome download normally.
14. Wait for the file to complete with `scripts/wait_for_browser_download.py`.
15. Validate the archive/file, move it into `private-assets/<slug>/`, extract safely and inspect
   it with `scripts/inspect_gltf.py`.
16. Keep the original archive outside public web folders. Optimize only a licensed project copy.
17. Create `ATTRIBUTION.md` and `asset-source.json`, then expose user-facing credits where the
   license requires it.

## What the agent may click autonomously

The agent may autonomously:

- run searches;
- open model pages;
- rotate/zoom the official viewer for inspection;
- play available animation clips;
- open the visible license details;
- click the ordinary official download button for a shortlisted, license-compatible,
  no-cost downloadable model;
- choose an offered web-compatible format;
- save and process the completed download.

Pause only for:

- expired login;
- account selection or 2FA;
- CAPTCHA;
- a new explicit legal/terms acceptance not previously accepted;
- a paid purchase or checkout;
- an ambiguous license that cannot be resolved from the visible page;
- two genuinely equivalent final visual choices.

Do not pause merely because the action is a normal free download.

## Forbidden behavior

Never:

- ask the user for a Sketchfab OAuth token in the default workflow;
- extract files from the viewer cache;
- use private or undocumented media endpoints;
- bypass login, download eligibility or model restrictions;
- download a model not explicitly offered as downloadable;
- accept unclear legal terms on the user's behalf;
- hide or omit required attribution;
- expose the original archive as a public stand-alone download.

## Scoring

Recommended score:

- visual fit: 25
- web suitability: 20
- animation suitability: 15
- license compatibility: pass/fail plus 15
- optimization headroom: 10
- materials/textures: 10
- provenance confidence: 5

A failed license gate rejects the model regardless of total score.

## Redistribution warning

A publicly delivered glTF can often be extracted by end users. Verify that the license permits
the intended web delivery model. Keep the original archive private and ship only the optimized
runtime copy needed by the application.
