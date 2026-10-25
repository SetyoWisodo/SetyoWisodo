# Skill Lab — 10 Skills, One Instrument

A single Vite + React 19 site that orchestrates **10 skills / libraries** requested:

| # | Skill / Library | Source | What it powers here |
|---|-----------------|--------|---------------------|
| 1 | **Anatomy Reveal** | [`annnguyentt/anatomy-reveal-skill`](https://github.com/annnguyentt/anatomy-reveal-skill) — TypingMind | Interactive **dual-boiler espresso machine** (52 convex parts shown, 82 total) — drag to orbit, explode slider, feature toggles. Paper look, 4-tone shading, separating-plane paint order. Same model drives the 10s film storyboard (whip → macro → explode → hero). |
| 2 | **Anatomy** | [`skills.wheresryan.sh/anatomy`](https://skills.wheresryan.sh/anatomy) — Claude Code skill | Three explanatory machines: **LRU Cache as bookcase** (MRU left, evict oldest), **Hash Map as sorting desk** (hash % 8, chain collisions), **Message Queue as marble run** (FIFO + escapement). The object *is* the explanation. |
| 3 | **Hairline — create** | [`lucasmarkes/hairline`](https://github.com/lucasmarkes/hairline) — `hairline-create` | **Funnel, clearance, sidings, storm** — isometric line figures that answer the pointer, with intensity slider, theme switch and tour. One self-contained HTML pattern, reproduced here as live SVG. |
| 4 | **Hairline — adopt** | `lucasmarkes/hairline` — `hairline-adopt` | Same engine, concept: rebuild an SVG mark as solids (never trace) — shown in docs & code comments. |
| 5 | **Motion Design** | [`LottieFiles/motion-design-skill`](https://github.com/LottieFiles/motion-design-skill) | **Director lab**: 8-step checklist, Disney 12, emotion → motion mapping, weight classes, quality rules. Live emotion/duration/stagger preview with 1/3-rule choreography. |
| 6 | **Motion (AI Kit)** | [`motiondivision/ai-kit`](https://github.com/motiondivision/ai-kit) — Motion for React | **Spring visualizer**: stiffness/damping/mass → `linear()` + `<motion.div transition={spring}>` — with MotionScore-grade performance notes (transform & opacity only). |
| 7 | **Scenario Blender Plugin** | [`scenario-labs/blender-plugin`](https://github.com/scenario-labs/blender-plugin) — 2 skills | **Blender 5.0+ viewport** + **local MCP server** (loopback, Host/Origin checks). Generate images/video/3D/PBR without leaving Blender; agents call `create_object`, `set_material`, `render_viewport`, `bake_pbr` via MCP. |
| 8 | **react-three/rapier** | [`pmndrs/react-three-rapier`](https://github.com/pmndrs/react-three-rapier) | **Physics playground** — Rapier WASM, deterministic 60 Hz. Add balls, watch restitution/friction, stack boxes, orbit controls. |
| 9 | **react-postprocessing** | [`pmndrs/react-postprocessing`](https://github.com/pmndrs/react-postprocessing) | **Postprocessing studio** — `EffectComposer` with Bloom, ChromaticAberration, DepthOfField, Vignette, Noise. All live-tunable. |
| 10 | **GSAP** | [`greensock/GSAP`](https://github.com/greensock/GSAP) — 3.15 | **Timeline lab** — `gsap.timeline()` with `back.out`, `power3`, `elastic`, `easeReverse`, `ScrollTrigger`-ready scrub & reverse. Context-safe. |
| 11 | **Openverse API** | [`api.openverse.org/v1/`](https://api.openverse.org/v1/) | **Live CC image search** — `GET /v1/images/?q=&license=&page_size=9` with CORS headers. Preview shows fallback with explanation when sandbox blocks outbound fetch; production fetch succeeds server-side. 800M+ images from Wikimedia, Flickr, NASA, etc., with attribution. |

## Quick start

```bash
cd skill-lab
npm install --legacy-peer-deps
npm run dev      # http://localhost:5173  (also live preview in Arena)
npm run build    # production to dist/
npm run preview  # serve dist/
```

Vite is configured with `host: 0.0.0.0, allowedHosts: true, X-Frame-Options: ALLOWALL` so Arena's preview proxy (`https://{port}-{sandboxId}.e2b.app`) works.

## Skills installed via `npx skills add`

All skills were installed with the `skills` CLI (v1.7.4):

```bash
npx skills add annnguyentt/anatomy-reveal-skill --agent '*' -y
npx skills add LottieFiles/motion-design-skill --agent '*' -y
npx skills add motiondivision/ai-kit --agent '*' -y
npx skills add scenario-labs/blender-plugin --agent '*' -y
npx skills add lucasmarkes/hairline --agent '*' -y
# wheresryan/anatomy + GSAP/rapier/postprocessing/Openverse are runtime libs, not CLI skills
```

Installed skill manifests are in `.agents/skills/` (not committed) and the lock file `skills-lock.json` at the repo root.

## Project structure

```
skill-lab/
  index.html
  vite.config.js        # host 0.0.0.0, allowedHosts
  package.json          # react 19, gsap 3.15, motion 12, three, @react-three/*, postprocessing
  src/
    main.jsx
    App.jsx             # all 10 skills orchestrated in one page
    App.css             # design system: ink/paper/panel, mono/serif
  dist/                 # built output (git-ignored)
```

## How each skill “runs”

- **Anatomy Reveal**: The `paper-stage` is a real isometric projection with per-group explode vectors. Drag = yaw/pitch, slider = explode %. Feature buttons move portafilter/gauge. The real skill would scaffold via `node <skill>/scripts/new-project.mjs` and build with `puppeteer-core` + `ffmpeg`; here the same convex-part discipline is demonstrated interactively.
- **Anatomy (wheresryan)**: Each machine is a minimal `motion` layout animation — the bookcase reorders on access, the queue animates FIFO, the hash desk computes `hash % 8`.
- **Hairline**: Four SVG figures replicate the skill’s pointer logic: distance-to-pointer → lift/raise, with an intensity scalar. Theme toggle matches `bench.html`’s light/dark.
- **Motion Design + Motion**: Duration/easing tables and spring math are live; the preview cards replay with the chosen archetype.
- **Blender + MCP**: A fake Blender header + viewport shows the Scenario panel; the MCP tab shows `.mcp.json` and tool names.
- **Rapier + Postprocessing + GSAP**: Real R3F canvases (physics and post) + a GSAP timeline with scrub/reverse.
- **Openverse**: `fetch("https://api.openverse.org/v1/images/?q=…")` — live in production, fallback in sandboxed preview (explained in UI).

## Notes

- `three-mesh-bvh@0.7.8` deprecation warning is benign (from `postprocessing` peer) and does not affect the build.
- For a true Anatomy Reveal film render, install `puppeteer-core`, Chrome/Edge, `ffmpeg`, and ImageMagick, then run the skill’s `motion/render.mjs` + `encode.mjs` — ~2 min per second of film.
- Tailwind was intentionally **not** used; the palette is custom (ink #f4f1eb, bg #08080a, paper #fdf6ec, accents #ff3b30/#0a84ff/#30d158) to keep the bundle self-contained.

— Built for Setyo Wisodo · Banyuanyar, East Java, ID · 2026-10-25
