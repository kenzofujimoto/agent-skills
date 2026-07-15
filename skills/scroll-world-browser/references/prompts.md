# Provider-neutral prompt templates

Keep the style preamble byte-for-byte identical across the whole project.

## Style preamble — default clay world

```text
Isometric low-poly 3D diorama floating as a small rounded island on a plain solid
[BG_HEX] background with a soft contact shadow beneath it. Soft matte clay render,
rounded toy-model shapes, gentle warm studio lighting, soft long shadows and a tilt-shift
miniature look. Cohesive palette of [PALETTE]. Highly detailed, centered composition,
absolutely no text, letters, numbers or logos.
```

Alternative opening phrases:

- Flat papercraft: layered cardstock, clean die-cut edges, subtle layer shadows.
- Glossy toy: smooth vinyl/plastic surfaces, soft rim light, collectible-toy finish.
- Claymation: handmade plasticine, slight thumbprint texture, stop-motion set lighting.
- Neon night: miniature night scene, warm windows, neon accents, reflective ground.
- Photoreal architectural: editorial architectural photography, wide-angle, natural
  materials, golden-hour light, no people; use full-bleed scenes rather than floating islands.

## Style-anchor prompt

```text
[STYLE PREAMBLE]
Create the visual style anchor for one connected world about [SUBJECT]. Show
[ANCHOR_SUBJECT]. This image defines the camera angle, materials, lighting, palette and
level of detail for every later scene. Landscape 3:2, centered with comfortable margins.
```

## Scene still

```text
Use the attached approved style-anchor image as the authoritative reference. Preserve its
camera angle, lens feel, materials, lighting, palette, background and detail density.

[STYLE PREAMBLE]

Create a new scene in that exact same world.
Scene: [SECTION_SUBJECT]
Focal point: [FOCAL_POINT]
Keep the focal point horizontally centered with headroom for a 16:9 video crop and a narrow
portrait center crop. Change only the subject matter required for this scene. No text,
letters, numbers, logos, captions or watermark-like marks. Landscape 3:2.
```

## Architecture A — initial leg

```text
Create one continuous cinematic camera move with no cuts, starting from the attached scene
image. Begin with a slow, steady forward glide toward [FOCAL_POINT]. [OPTIONAL_MID_LEG_MOVE]
Reveal [SCENE_SUBJECT] as one coherent space. In the final second, settle into a slow,
steady forward drift toward [NEXT_DIRECTION]. Preserve the attached image's art direction,
materials, palette and lighting. Smooth motion, subtle parallax, no text or captions.
Landscape 16:9. Do not generate audio unless explicitly requested.
```

## Architecture A — continuation/edit leg

```text
Continue the attached video as the same uninterrupted camera shot. Do not restart the shot,
change lens, jump position, reverse direction or introduce a cut. Continue the exact camera
velocity and visual treatment from the final moment of the source video.

The camera travels into [NEXT_SCENE_SUBJECT] toward [FOCAL_POINT].
[OPTIONAL_MID_LEG_MOVE]
In the final second, settle back into a slow, steady forward drift toward [NEXT_DIRECTION].
Preserve the same world, materials, palette, lighting and camera language. No text or
captions. Landscape 16:9. Do not generate audio unless explicitly requested.
```

## Architecture B — independent dive

```text
Create one continuous cinematic camera move with no cuts, starting from the attached scene
image. Begin high and outside the scene, then glide forward and descend toward
[FOCAL_POINT], revealing [SCENE_SUBJECT]. Preserve the attached image's exact art direction,
palette, materials and lighting. End in a calm, low-motion composition suitable for a
transition. Smooth motion, subtle parallax, no text or captions. Landscape 16:9.
```

## Architecture B — two-reference bridge

Attach the previous clip's actual last frame first and the next clip's actual first frame
second.

```text
Create a single continuous transition between the two attached boundary frames. Begin as
close as possible to reference image 1, continuing its camera direction and velocity. Move
through the connected world toward [NEXT_SCENE], and arrive as close as possible to reference
image 2 without a hard cut. Keep the same art direction, palette, lighting and lens language.
Use smooth slow motion and subtle parallax. No text or captions. Landscape 16:9.
```

The browser provider may treat these as references rather than exact endpoint constraints.
Use a short crossfade during encoding and visually verify the result.

## Copy per section

- `eyebrow`: 2–4 words.
- `title`: 3–7 words.
- `body`: one concise sentence.
- `tags`: 0–3 proof/value chips.
- Final section: payoff plus CTA.
