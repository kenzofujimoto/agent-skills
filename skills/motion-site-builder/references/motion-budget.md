# Motion budget

Suggested default:

```json
{
  "motionIntensity": 7,
  "dominantEngine": "gsap",
  "secondaryEngine": "motion",
  "specialSections": 2,
  "webglCanvases": 1,
  "continuousAnimations": 3,
  "decorativeEffectsPerViewport": 2,
  "targetDesktopFps": 55,
  "targetMobileFps": 45
}
```

Continuous animation pauses offscreen. Mobile may use a simpler recipe, not merely a smaller
version. Avoid simultaneous blur, filters and large shadows on many elements. Do not animate
layout properties when transform/opacity can express the result.
