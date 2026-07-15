# Media contracts

## Full-bleed cinematic

Generate 16:9 directly, preferably 1920×1080 or higher. Keep essential content outside the
outer 12% safe-area band. First video frame must preserve the approved still framing. Initial
scale is 1.0. No automatic initial zoom or aggressive dolly-in.

## Framed media stage

Use the actual container ratio: 1:1, 4:3, 3:2, 16:10 or custom. Build an intentional stage
with surface, radius, border, contact shadow, ambient spill and controlled overflow. The media
does not need transparency when the frame is deliberate.

## Transparent layered object

Preferred order: GLB/GLTF → Rive → SVG → PNG/WebP alpha layers → alpha video only when the
whole delivery stack supports it. Use transparent canvas and preserve the page background.

## Layered 2.5D

Separate or approximate background, architecture, subject, foreground, lights and particles.
Move layers at different depths. Keep scale restrained to preserve sharpness.

## Video scrub

Require no visible watermark, adequate native resolution, no upscaling, correct first frame,
expected aspect ratio, short GOP, matching poster and reduced-motion fallback.

## Background strategies

- `exact-match`
- `stage`
- `ambient-extension`
- `transparent`
- `full-bleed`

## Reject

Visible watermark, unexpected crop/zoom, resolution below contract, broken alpha, generated
text when prohibited, double compression, unplanned letterbox, inconsistent subject/style.
