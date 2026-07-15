# Web 3D asset evaluation

Starting budgets:

- Small decorative object: <=2 MB compressed, <=40k triangles, <=4 materials, <=1k textures.
- Hero object: <=5–8 MB, <=100k–150k desktop triangles, <=40k–60k mobile LOD, <=8 materials.
- Full scene: <=10–15 MB preferred, lazy-loaded with LODs and capped DPR.

Inspect primitives/draw-call proxy, transparency/overdraw, texture sizes, skeleton bones,
morph targets, animation duration/loopability, bounding box/origin, scale, dependencies and
extensions. A clip existing does not mean it deforms or loops cleanly.

For scroll playback, map progress to a bounded clip/mixer time, pause offscreen and provide a
static reduced-motion pose.
