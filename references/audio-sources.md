# Ad audio — what works, what doesn't

Reality check on free SFX, music, VO, and silence-cutting for short-form video ads. Jump straight to the proven path.

## Sound effects (whoosh / punch / ding / sweep / stamp)

- **Best free source: Mixkit SFX** — `mixkit.co/free-sound-effects/<category>/`. Permissive license (commercial, no attribution). Preview URLs in page HTML: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`. Categories: `whoosh`, `impact`, `notification`, `riser`, `transition`.
- **Mixkit SFX previews ARE the full clip** (unlike their music previews). Trim tight:
  ```bash
  ffmpeg -i mixkit-original.mp3 -t 0.22 -af "afade=t=out:st=0.17:d=0.05" -ac 2 -b:a 192k punch.mp3
  ```
- **Tight ad lengths:** whoosh 0.6s, punch 0.22s (rapid-fire stamps), ding 0.65s, sweep 0.6s, stamp 0.5s.
- **Volume under VO:** punch −3 dB, ding −8 dB (`volume=-XdB` filter).
- **Avoid:** ffmpeg-synthesized SFX (sounds AI-hacky); ElevenLabs `/v1/sound-generation` (mushy, long tails, stacks into noise).

## Music beds

- **Mixkit "free music" is preview-only** — ~3.5s preview MP3s. Looping to fill 60s sounds awful. Don't.
- **Pixabay music** blocks urllib scrapes (403); its API has images/video, not audio.
- **Real options:** user uploads their own licensed track (Epidemic/Splice/Artlist — best); YouTube Audio Library (manual download); Bensound/FMA with attribution.
- **For direct-response ads: skip the music.** Most high-converting Reels/TikTok ads are VO + SFX only. If required and licensed: mix −18 dB under VO, 1.5s fade-in / 2.5s fade-out (−28 dB is inaudible; −18 dB is the sweet spot).

## Voiceover

- **ElevenLabs Chris** — voice `iP95p4xoKVk53GoZ742B`, model `eleven_turbo_v2_5`. Confident male read, default for ads.
- Settings: `{ stability: 0.45, similarity_boost: 0.78, style: 0.55, use_speaker_boost: true }`.
- `<break time="0.4s" />` for inter-beat pauses — never 2s+.
- **Always re-whisper after generation** for word-level timestamps (`faster-whisper small.en`, `word_timestamps=True`). These drive caption + SFX + visual sync.

## Cutting raw recordings (the BIT cut process)

1. **Whisper transcribe** with VAD: `WhisperModel("small.en").transcribe(file, vad_filter=True, vad_parameters={"min_silence_duration_ms":400}, word_timestamps=True)`.
2. **ffmpeg silencedetect** for silences ≥ 0.3s: `silencedetect=noise=-30dB:d=0.3`.
3. **Concat-trim** with `filter_complex`, keeping each speech segment + 0.18s of natural room tone:
   `[0:v]trim=start=A:end=B,setpts=PTS-STARTPTS[vN]; [0:a]atrim=...[aN]; … concat=n=N:v=1:a=1[outv][outa]`.
4. **Re-whisper the cut** — timings shift; use the NEW timestamps for all composition anchors.

Typical: 77s raw → 67s cut, ~13% silence trimmed, no spoken words dropped.
