# Recipe: Sketchfab model to Three.js/R3F

Use when a section needs a genuine transparent 3D object, authored animation or controllable
camera.

## Browser-first sequence

1. Create `3d-asset-brief.json`.
2. Start the dedicated browser automatically.
3. Search the Sketchfab Downloadable catalog using several query variants.
4. Shortlist and visually inspect 5–12 candidates.
5. Verify author, explicit license and downloadable status.
6. Score candidates and document the rationale.
7. Click the official free Download control for the selected candidate.
8. Prefer glTF/GLB when the official dialog offers it.
9. Wait for the ordinary browser download; never override the Chrome download directory via
   CDP.
10. Keep the original archive private and extract safely.
11. Inspect with `inspect_gltf.py`.
12. Optimize a project copy only when the license permits modification.
13. Integrate using the existing Three.js/R3F stack.
14. Preserve visible attribution and provenance.

## Integration

- calculate bounds and place the authored model inside a wrapper group;
- choose camera distance from bounds rather than hardcoded arbitrary scale;
- cap DPR;
- lazy-load;
- pause mixer/rendering offscreen;
- dispose geometry, materials and textures on teardown;
- map scroll to bounded camera/object/clip progress;
- provide a static or simplified reduced-motion fallback.

Do not ask the user for a Sketchfab API token unless they explicitly request API automation.
