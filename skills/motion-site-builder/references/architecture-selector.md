# Architecture selector

Choose per section, not per site.

## Decision tree

1. Does the section need real recorded motion?
   - Clean footage exists → `video-scrub`.
   - AI footage is watermarked, soft or cannot preserve framing → `layered-2.5d` or WebGL.
2. Must the visual blend with the page background?
   - True transparency/spatial object → WebGL, Rive, SVG or alpha layers.
   - A bounded visual is acceptable → `framed-media-stage`.
   - Full viewport immersion → `full-bleed-cinematic`.
3. Is real depth/free camera required?
   - Yes → Three.js/R3F.
   - No → layered 2.5D.
4. Is it mostly interface?
   - Yes → CSS/Motion, GSAP only for choreography.
   - No, narrative scroll → GSAP/ScrollTrigger.
5. Is it a stateful illustration?
   - Rive for state machines.
   - Lottie for small linear playback.
   - SVG for simple geometry and direct DOM control.

## Default hierarchy

CSS → Motion → GSAP → Rive/Lottie/SVG → Three.js/R3F → generated video.

This order is about reliability and cost, not visual power.
