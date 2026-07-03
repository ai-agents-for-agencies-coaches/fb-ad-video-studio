# whiteboard/ — the whiteboard family inside fb-ad-video-studio

This is the **whiteboard** template family. It produces an authentic "whiteboard animation"
explainer ad: a marker hand scribbles each scene's outline in, then the color slowly paints in
over the line, ending on a pristine cartoon. 9:16 vertical, ElevenLabs VO, consistent
AI-illustrated characters, designed trust/CTA slides, SFX, rendered to MP4. Built for
home-services offers (roofing, HVAC, etc.) but works for any short story-driven explainer.

## This family uses its OWN engine — NOT HyperFrames

Unlike the rest of fb-ad-video-studio, the whiteboard style does **not** author HyperFrames
compositions. It is a **self-contained render engine** that lives entirely in `assets/`:

- `scene_full.html` — the render engine (the raster "line-then-paint" reveal + slide scenes).
- `render.js` — generic renderer; reads `comp/scene_timing.json` (each scene has a `type`).
- `hand.png` — the cartoon marker hand. Tip at (0.177, 0.545).
- `assemble.py` — mixes VO + per-scene Woosh + optional accent SFX, encodes the MP4.

Render via `node comp/render.js` + `python3 assemble.py`, **not** the HyperFrames CLI. Do not
try to port this into HyperFrames — the reveal is the whole point and it is already proven.

## How the effect works (do NOT reinvent this)

- The original AI cartoons are **never modified**. Each scene's own outline is extracted as a
  raster line layer; the pristine color image is revealed on top. The final frame == the
  untouched cartoon.
- A seeded "coverage" scribble path is used as an SVG stroke **mask** — the marker-hand tip
  rides its leading edge, so the reveal follows the hand and lines up. First it reveals the
  LINE layer, then slowly paints the COLOR in over it.
- NEVER vectorize/skeletonize the art into SVG strokes to "draw" it — it mangles faces
  (rejected hard). Don't cross-fade a full color image over offset outlines — it ghosts. The
  raster line-then-paint approach above is the answer. See `references/RUNBOOK.md` for the full
  backstory and failure history.

## Required keys

- **ElevenLabs** — voiceover generation (`generate_vo.py`). Default voice "Rachel" (calm).
- **Gemini** — the consistent AI character illustrations (`gen_scenes.py`).

## Assets (in this family's `assets/`)

- `scene_full.html` — render engine (draw + slide scenes). **Do not edit per build.**
- `render.js` — generic renderer; reads `comp/scene_timing.json`. **No edits.**
- `hand.png` — the cartoon marker hand. Tip at (0.177, 0.545).
- `generate_vo.py` — TEMPLATE: fill `SCRIPT` + `SCENES` (ids, unique anchor phrases, types) → VO + timing.
- `gen_scenes.py` — TEMPLATE: fill `CHAR` + `STYLE` + `SCENES` + `NOREF` → consistent Gemini illustrations.
- `make_lineart.py` — extracts the line layer from every `*_color.png`. No edits.
- `slide_trustcard.html`, `slide_signoff.html` — designed-slide templates (navy/gold; swap brand).
- `assemble.py` — mixes VO + Woosh (per scene) + optional accent SFX, encodes MP4. No edits.

## Build workflow (run each build in its own folder)

1. **Scaffold + copy engine.** `mkdir -p <build>/{audio,scenes,comp,render}`. Copy into
   `<build>/comp/`: `scene_full.html`, `render.js`, `hand.png`. Copy `generate_vo.py`,
   `gen_scenes.py`, `make_lineart.py`, `assemble.py` into `<build>/`.
2. **Script + timing.** Edit `generate_vo.py`: write the ~150-word / ~55s VO in the classic arc
   (hook/problem → tension → discovery → how-it-works → offer → trust slide → resolution → CTA
   slide). Set each scene's `id`, a UNIQUE lowercase `anchor` phrase from the VO, and `type`
   (`draw` | `slide`). Write numbers as spoken words. Run `python3 generate_vo.py`; confirm every
   anchor matched.
3. **Illustrations.** Edit `gen_scenes.py`: `CHAR` lock, `STYLE`, per-scene prompts, `NOREF` for
   person-less scenes. Run `python3 gen_scenes.py s1_<first>` first, eyeball the character, then
   batch the rest. Prompts must say "no text / leave blank" for any badge/label. QA a contact
   sheet for character consistency.
4. **Line layers.** `python3 make_lineart.py`.
5. **Slides.** Render `slide_trustcard.html` + `slide_signoff.html` (fill logo base64 + copy) to
   `scenes/<slide_id>.png` at 720×1280.
6. **Render + assemble.** `node comp/render.js`, then
   `python3 assemble.py <client>-whiteboard-<offer>.mp4 <accent_scene_id?>`.
7. **QA (mandatory).** Each draw scene must animate (frame diff >2) and END on its pristine
   cartoon (mean-diff <2 vs `<id>_color.png`); slides hold static; video+audio present. Verify
   the hand actually renders (a dropped `hand.src` = invisible hand).

## Defaults & knobs

- 9:16 720×1280, 30fps, ~55s, 8 scenes (6 draw + trust slide + CTA slide). Art box 660×660 at (30,230).
- Timing auto-fits each scene to its VO span (in `scene_full.html`: draw ~46% then paint to 90%, hold 10%).
- Character consistency: first scene establishes; others pass it as a reference; person-less scenes → NOREF.

See `references/RUNBOOK.md` for the exact command sequence, the failure history, and every gotcha.
