# Reverse-template workflow (video)

The highest-leverage use of this skill: turn a winning video ad into a reusable HyperFrames composition. Same principle as `image-studio`'s reverse-template, applied to motion.

You are extracting **structure**, never copying content. The deliverable is a parametric template, not a clone.

## Steps

1. **Get the reference.** Local file, URL, or screen recording. If a URL, download it (`yt-dlp`, or the platform's export). Extract frames at 0.5s intervals for a visual storyboard: `ffmpeg -i ref.mp4 -vf fps=2 frames/%03d.jpg`.
2. **Transcribe it.** `scripts/whisper-words.py ref.mp4` → word timestamps. This is the spine.
3. **Map the scene arc.** Watch the frames + transcript. Write a beat sheet with timestamps:
   - Hook (0–3s) — what stops the scroll? Pattern interrupt, bold claim, motion?
   - Problem / agitate — how long, how stated?
   - Solution / mechanism
   - Proof — testimonial? numbers? screen recording? logo wall?
   - CTA — offer, urgency, where placed?
4. **Measure pacing.** Cut cadence (avg shot length), word-reveal duration, beat length, SFX density (hits per 10s), caption style/position, music presence and level.
5. **Identify the device.** Talking-head + PIP arc? Pure kinetic type? UGC selfie? Screen-recording inset? Split-screen? This picks the base template (`motion-graphics-spot` or `talking-head-founder-ad`).
6. **Parameterize.** Build the composition with variables for the swappable parts:
   - VO script / presenter clip
   - Brand tokens (`--accent`, `--ink`, fonts)
   - Headline beats (the kinetic-type lines)
   - Proof points (numbers, logos, screenshots)
   - CTA / offer / urgency
   - Scene durations (keep the *ratios* from the reference, swap absolute lengths)
7. **Validate.** Render a build with placeholder content; compare the arc and pacing against the reference side-by-side. Match the rhythm, not the pixels.
8. **Save.** Write the generalized composition to `templates/<vertical>-<hook>.html` with a top-comment variable index. Future ads in that style reuse it.

## What to keep vs. discard

| Keep (the template) | Discard (the content) |
|---------------------|------------------------|
| Scene arc & ratios | Their script |
| Pacing / cut cadence | Their footage |
| SFX rail timing pattern | Their brand colors |
| Caption style & position | Their offer |
| The structural device (PIP arc, kinetic stack) | Their logo |

## Ethics

Extract structure and pacing — those aren't ownable. Never reuse a competitor's footage, voiceover, music, or copy. The output must be the user's own brand, script, and assets in a proven *shape*.
