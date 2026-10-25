# Workflow — Opus writes the code → skills guide the look → engines render → Openverse adds the sound

This file documents the 4-stage pipeline that `skill-lab` orchestrates. Each stage maps to installed skills and runtime libraries.

## 01 — Opus writes the code

**Actor:** Muse / Opus (the agent that ran this branch)

- Researches real dimensions, materials, teardowns (anatomy-reveal `references/inputs.md`)
- Writes the spec before geometry: dims, parts list grouped by assembly, feature keys
- Scaffolds via `node <skill>/scripts/new-project.mjs <dir>` (anatomy-reveal template)
- Builds object in `object/geometry.mjs` following `references/object.md` — hollow shell of convex panels, explode assemblies, feature groups, anchors, markings as face planes
- Iterates with `object/test-page.mjs`, `object/shots.mjs`, `object/scan-apart.mjs` until `node object/scan-apart.mjs` reports no intersections from 5 views
- Defines `object/film.mjs` (FILM, FIGURE, FEATURE_DEFAULTS) and choreographs `motion/timeline.mjs` beat by beat

**In this demo:** The espresso machine is 52 convex parts shown (82 in full kit), 6 assemblies, 380×415×470 mm, with 3 feature channels (portafilter 28°, gauge, steam wand).

## 02 — Skills guide the look

**Skills:**

- `annnguyentt/anatomy-reveal-skill` — paper look, 4-tone shading, separating-plane paint order
- `lucasmarkes/hairline` (create + adopt) — isometric line figures, pointer + intensity + tour, one HTML no-deps
- `LottieFiles/motion-design-skill` — 8-step checklist, Disney 12, emotion→motion, 1/3 rule, weight classes
- `motiondivision/ai-kit` (motion) — springs, best practices, CSS `linear()` generation, MotionScore

**In this demo:**

- Paper: warm white `#fdf6ec` with 24px grid, ink outlines, 4-tone fills
- Hairline: Funnel, Clearance, Sidings, Storm — each is a pointer-driven SVG with intensity slider
- Motion Design: joy/urgency/calm/elegance presets with live duration/stagger preview
- Motion: stiffness/damping/mass → `linear()` + `<motion.div transition={spring}>`

## 03 — Engines render

**Engines:**

- **Three.js + @react-three/fiber + drei** — WebGL renderer, OrbitControls, Environment, ContactShadows, Float, Grid
- **@react-three/rapier** — Rapier WASM physics, deterministic 60 Hz, RigidBody + BallCollider/CuboidCollider
- **@react-three/postprocessing + postprocessing** — EffectComposer with Bloom, ChromaticAberration, DepthOfField, Vignette, Noise
- **Scenario Labs Blender Plugin** — Blender 5.0+ viewport generation (local MCP server, loopback, Host/Origin checks, PBR bake)
- **GSAP 3.15** — `gsap.timeline()` with `back.out`, `power3`, `elastic`, `easeReverse`

**In this demo:**

- Physics playground: 6 balls + 5-box stack, gravity slider, walls, shadows, city env
- Postprocessing studio: torus + icosahedron + box with live Bloom/Chroma/Noise/Focus
- GSAP studio: 4 cards with staggered entrance, bar + dots, scrub/reverse
- Blender bridge: fake viewport UI with Shading tab, Scenario panel, MCP `.mcp.json` + PBR maps

## 04 — Openverse adds the sound

**APIs:**

- `https://api.openverse.org/v1/images/?q=&license=&page_size=`
- `https://api.openverse.org/v1/audio/?q=&license=&page_size=` — Freesound, Jamendo, Wikimedia, CC-licensed

**In this demo:**

- **Images:** live search of 800M CC images with attribution (title, creator, license badge)
- **Audio:** live search of CC audio with waveform bars, play/pause, progress, and **assignment to 8 engine slots**:
  - `film` — 10s reveal score (whip → macro → explode → hero)
  - `steam` — boiler + wand
  - `grind` — conical burrs
  - `tick` — marble run escapement
  - `impact` — Rapier collisions
  - `swell` — bloom intensity
  - `ui` — GSAP scrub + Motion spring
  - `ambient` — Hairline + Blender room tone

- **Global audio bar** (sticky bottom): shows currently routed track with progress, attribution link, and waveform ducking hint
- **Soundtrack tab:** assembled 8-track view with per-slot assigned status
- **Foley map tab:** which sound goes where in the page
- **CC guarantee:** no sample is redistributed — every play shows creator · license · URL; export is an EDL of CC URLs, not a file

---

## How to run

```bash
cd skill-lab
npm install --legacy-peer-deps
npm run dev   # http://localhost:5173 + Arena preview https://5173-{sandboxId}.e2b.app
```

## End-to-end

```
Opus drafts spec
  → skills set paper/hairline/motion language
    → engines render pixels, physics, PBR from same convex model
      → Openverse fills silence with CC audio → mix → MP4 cut
```

The anatomy film is silent by design (`anatomy-reveal` spec: “The film is silent; offer to cut it to a track the user supplies”) — this demo supplies that track via Openverse.
