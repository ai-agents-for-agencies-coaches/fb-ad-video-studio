# HyperFrames ad patterns — what works, what bites

Distilled from 23 production iterations of a real founder ad. Start from these instead of the naive approach.

## Lottie integration

- **Container = the clip element directly.** `container: document.getElementById("clip-id")`, not a nested `.lottie-layer` div. Nesting can leave the SVG at 0 dimensions when HyperFrames hides the parent at page load.
- **Keep Lottie clip wrappers alive from t=0 to end** (`data-start="0" data-duration="<full>"`). HF hides clips with late `data-start` at load → lottie-web injects SVG into a 0-sized hidden container → never sizes correctly. Use GSAP `opacity` tweens for the real visibility window.
- **Looping seek must be clip-relative.** `compositionMs % loopMs` lands on frame 0 at exact multiples (t=27s → 0 for a 3s loop). If frame 0 is empty (pre-launch, fade-in) you see nothing. Pass `clipStartMs`, subtract before wrapping.
- **`path:` over `animationData:`.** Inline JSON has ready-state issues; local-file `path:` is the proven pattern.
- **If Lottie still won't render, fall back to CSS/GSAP.** A conic-gradient burst + GSAP-scattered dots ships faster than debugging async lottie-web edge cases.

## GSAP + CSS transform conflicts

- CSS `transform: translateX(-50%)` + GSAP animating `scale`/`y` = GSAP overwrites the whole `transform` → element loses centering, flies off-screen.
- **Fix:** remove CSS transforms; center with `gsap.set(el,{ xPercent:-50 })`.
- PIP scaling: with `transform-origin: bottom right`, `scale 0.296` + `x:-28, y:-28` correctly insets the bottom-right corner. Never translate large positive values.

## Captions

- **Position y ≈ 1180–1400** (below face, above hands). Not y≥1500 (torso covers it), not y≈200 (covers face).
- **Anchor to actual whisper word starts**, not script estimates. After cutting silences, re-whisper the cut and use the new timestamps.
- **Split beats > 5s** into two captions so none lingers stale.

## Speaker PIP arc (talking-head)

Most engaging structure: **hidden → PIP → full → PIP → full → hidden (lockup takes over)**. Rhythmic variety, never "covered" by overlays. Cold-open with the motion graphic alone (speaker hidden 0–3s) is the strongest hook.

## Pacing for short-form social

- Scene transitions: **0.18s drift cuts**, not 0.5s fades.
- Word reveals: **0.25s**, not 0.4s.
- ElevenLabs `<break>` ≤ 0.4s — long breaks add ad-killing dead air.
- Silence cutting: trim to **0.18s gaps**.

## Video element warnings

- "Video has sparse keyframes (max interval: 5.53s)" — phone MP4s have 5s+ keyframe intervals → seek failures. Re-encode:
  ```bash
  ffmpeg -i raw.mov -c:v libx264 -r 30 -g 30 -keyint_min 30 -movflags +faststart -c:a copy clean.mp4
  ```
- Speaker video `muted`; VO on a separate `<audio>`.

## Render

- **Docker required on Pop!_OS / many Linux** (apparmor blocks puppeteer): `npx hyperframes render --docker`. ~2–3 min per 68s comp after first build.
- Fix before render: `media_missing_id` (audio without `id` renders silent — it's an error), `gsap_exit_missing_hard_kill` (add `tl.set(el,{opacity:0}, exitTime)` after fade-out for seek safety), `overlapping_gsap_tweens` (add `overwrite:"auto"` on the later tween). `composition_file_too_large` is advisory — ignore unless splitting helps readability.

## Debugging when nothing renders

- `ffmpeg -ss <t> -i render.mp4 -frames:v 1 frame.jpg` — verify visually before iterating.
- Temporary debug paint: `background: rgba(255,0,0,0.4); border:4px solid #f0f` — confirms the container is positioned even when content fails.
- `console.log("[TAG]", v)` from page JS surfaces in the render log as `[Browser] [TAG] …` — confirms Lottie/GSAP events fire.
