#!/usr/bin/env python3
"""Word-level timestamps -> <audio>.words.json. These drive EVERY caption,
SFX, and visual reveal in the composition. Re-run after any audio cut —
timings shift, and script-based estimates are never tight enough.

Usage:  python3 scripts/whisper-words.py audio/vo.mp3
Requires: pip install faster-whisper
"""
import sys, json, os
from faster_whisper import WhisperModel

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "audio/vo.mp3"
    out = os.path.splitext(src)[0] + ".words.json"
    model = WhisperModel("small.en", compute_type="int8")
    segments, _ = model.transcribe(src, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 400}, word_timestamps=True)
    words = [{"w": w.word.strip(), "start": round(w.start, 3),
              "end": round(w.end, 3)}
             for seg in segments for w in (seg.words or [])]
    json.dump(words, open(out, "w"), indent=2)
    print(f"{len(words)} words -> {out}")
    for x in words[:12]:
        print(f"  {x['start']:6.2f}  {x['w']}")
    print("Use these .start values as data-start on captions/SFX/reveals.")

if __name__ == "__main__":
    main()
