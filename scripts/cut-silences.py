#!/usr/bin/env python3
"""The BIT cut: trim dead air from a raw presenter recording while keeping
0.18s of natural room tone between phrases. Typical 77s -> 67s, ~13% removed,
no spoken words dropped. ALWAYS re-whisper the cut afterward (timings shift).

Usage:  python3 scripts/cut-silences.py footage/raw.mov footage/speaker-cut.mp4
Requires: faster-whisper, ffmpeg.  Tunables below.
"""
import sys, subprocess, os
from faster_whisper import WhisperModel

GAP = 0.18          # room tone kept between segments (s)
MIN_SIL = 0.40      # silence >= this is a cut candidate (s)

def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "footage/speaker-cut.mp4"
    model = WhisperModel("small.en", compute_type="int8")
    segs, _ = model.transcribe(src, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": int(MIN_SIL * 1000)},
        word_timestamps=True)
    spans = [(round(s.start, 3), round(s.end + GAP, 3)) for s in segs]
    # merge overlaps
    keep = []
    for a, b in spans:
        if keep and a <= keep[-1][1]:
            keep[-1] = (keep[-1][0], max(keep[-1][1], b))
        else:
            keep.append((a, b))
    fc = []
    for i, (a, b) in enumerate(keep):
        fc.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]")
    cat = "".join(f"[v{i}][a{i}]" for i in range(len(keep)))
    fc.append(f"{cat}concat=n={len(keep)}:v=1:a=1[outv][outa]")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", src, "-filter_complex", ";".join(fc),
        "-map", "[outv]", "-map", "[outa]", "-c:v", "libx264", "-r", "30",
        "-g", "30", "-keyint_min", "30", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", out], check=True)
    print(f"cut {len(keep)} segments -> {out}")
    print("Next: extract audio + python3 scripts/whisper-words.py on the CUT")

if __name__ == "__main__":
    main()
