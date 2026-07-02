# Whiteboard Video — Runbook

Exact command sequence + hard-won gotchas. Reference builds:
`clients/covenant-roofing/creatives/whiteboard-ad-v1/` (financing offer) and
`.../whiteboard-ad-instant-estimate/` (instant-estimate offer).

## Prereqs (in toolkit `.env`)
`GEMINI_API_KEY` (scene art), `ELEVENLABS_API_KEY` (VO), `DEEPGRAM_API_KEY` (word timing).
`scipy`/`scikit-image` are NOT needed anymore (the SVG-trace path was abandoned). Uses
Playwright from `.claude/skills/image-studio/node_modules`, ffmpeg, PIL, numpy.

## Command sequence
```bash
SK=.claude/skills/whiteboard-video/assets
B=clients/<client>/creatives/whiteboard-ad-<offer>
mkdir -p $B/{audio,scenes,comp,render}
cp $SK/scene_full.html $SK/render.js $SK/hand.png $B/comp/
cp $SK/generate_vo.py $SK/gen_scenes.py $SK/make_lineart.py $SK/assemble.py $B/
# --- edit $B/generate_vo.py (SCRIPT + SCENES) ---
cd $B && python3 generate_vo.py           # -> audio/vo.mp3 + comp/scene_timing.json
# --- edit $B/gen_scenes.py (CHAR/STYLE/SCENES/NOREF) ---
python3 gen_scenes.py s1_<first>          # establish character, then eyeball it
printf '%s\n' <other draw ids> | xargs -P5 -I{} python3 gen_scenes.py {}
python3 make_lineart.py
# --- render slides (fill logo base64 + copy into the two slide_*.html) ---
node ../../../.claude/skills/image-studio/render.js --input scenes/s6_trust.html  --output scenes/s6_trust.png  --width 720 --height 1280 --scale 2
node ../../../.claude/skills/image-studio/render.js --input scenes/s8_signoff.html --output scenes/s8_signoff.png --width 720 --height 1280 --scale 2
node comp/render.js                       # -> comp/frames/*.png  (~1600 for 55s)
python3 assemble.py <client>-whiteboard-<offer>.mp4 s5_<offer>   # accent SFX on the payoff scene
```
Deliver `render/*.mp4` to `/mnt/jellyfin-media/clients/<Client>/whiteboard-ads/` (sudo cp + chown
jellyfin), then `POST http://localhost:8096/Library/Refresh` with `X-Emby-Token`.

## The story arc (fill it)
hook/problem → tension (what they dread) → discovery → how-it-works (often a person-less product/UI
scene → put it in NOREF) → offer/payoff → **trust slide** (family-owned · N years · N★ reviews) →
resolution (happy ending) → **CTA slide** ("Get your <thing>", 👇 click below). ~150 words ≈ 55s.

## Gotchas (each cost real iteration — do not relearn)
1. **Never vectorize the artwork.** Skeleton→SVG strokes botched faces into "terrifying" dead-eyes.
   Keep the cartoon untouched; reveal its own raster outline, then paint the real color on top.
2. **Reveal must follow the hand.** A top-down wipe with a floating hand looks fake ("hand doesn't
   line up"). The coverage-path mask + tip-on-frontier is what lines up.
3. **Outline-free fill for a fade will ghost.** Don't. Use line-then-paint with the strokes hidden
   under the advancing color (both from the same source = perfect registration).
4. **Feel:** loose scribble draws the outline, then color SLOWLY paints in. Not a fast fade.
5. **Hand:** George prefers the cartoon-outline MARKER hand (`hand.png`), not pencil/photoreal.
   Keep it small (handW~320) and bound the wander (rightBound~0.80) or the arm clips the frame.
6. **Randomize** the hand path per scene (the `seed` in scene_timing) so it never looks looped.
7. **hand.src bug:** if you refactor the engine, make sure `init` sets `hand.src=cfg.hand` — a missing
   line makes the hand invisible while everything else looks fine.
8. **Character consistency:** first scene establishes; others pass it as a reference image; a scene
   without the recurring character MUST be in NOREF or it just copies scene 1 (the crew/tech scenes).
9. **AI text is garbled** — prompt "no text, leave blank" for badges/labels; put real copy on the
   designed slides only.
10. **Anchors must be unique** lowercase phrases that appear once in the VO; write numbers as words
    ("thirty six", not "36") so Deepgram tokenizes them predictably.
11. **Jellyfin "Client Projects" is a HOMEVIDEOS library and skips clips <~10s.** Full ads are fine;
    pad any short single-scene review clip to ≥10s (hold last frame). Each mp4 shows separately.
12. **QA every scene ends pristine** (mean-diff <2 vs its `_color.png`), draw scenes animate, slides
    hold. Deliver via Jellyfin LAN links, never Drive.

## Tunables (in the copied files)
- `scene_full.html`: `activeEnd=D*0.90`, `lineDur=activeEnd*0.46`, paint feather, brush stroke-width
  (175 line / 190 color), coverage rows/rightBound.
- `render.js` cfg header: `handW`, `tip`, `rightBound`, `art` box.
- `generate_vo.py`: `VOICE` id, the SCRIPT, SCENES (ids/anchors/types).
- `assemble.py` args: output filename, accent scene id (Pop SFX).
