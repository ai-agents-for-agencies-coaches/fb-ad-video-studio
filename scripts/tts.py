#!/usr/bin/env python3
"""Generate ad VO with ElevenLabs (Chris — confident male read).

Usage:  ELEVENLABS_API_KEY=... python3 scripts/tts.py script.md audio/vo.mp3
Script file: plain text, one beat per paragraph. Use <break time="0.4s"/> for
inter-beat pauses — NEVER 2s+ (dead air kills ad pace). Always run
scripts/whisper-words.py on the output to get word timestamps for sync.
"""
import os, sys, urllib.request, json

VOICE = "iP95p4xoKVk53GoZ742B"          # ElevenLabs "Chris"
MODEL = "eleven_turbo_v2_5"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.78,
            "style": 0.55, "use_speaker_boost": True}

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "script.md"
    out = sys.argv[2] if len(sys.argv) > 2 else "audio/vo.mp3"
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("Set ELEVENLABS_API_KEY")
    text = open(src).read().strip()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
        data=json.dumps({"text": text, "model_id": MODEL,
                         "voice_settings": SETTINGS}).encode(),
        headers={"xi-api-key": key, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"}, method="POST")
    with urllib.request.urlopen(req, timeout=120) as r:
        open(out, "wb").write(r.read())
    print(f"VO -> {out}  ({os.path.getsize(out)} bytes)")
    print("Next: python3 scripts/whisper-words.py", out)

if __name__ == "__main__":
    main()
