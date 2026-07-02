#!/usr/bin/env python3
"""TEMPLATE — VO + per-scene timing for a whiteboard video.
Edit SCRIPT and SCENES below, then run from the build root:  python3 generate_vo.py
Writes audio/vo.mp3 and comp/scene_timing.json (each scene carries its `type`).

SCENES: list of (scene_id, anchor_phrase_or_None, type). The anchor is a UNIQUE
lowercase phrase from SCRIPT whose first word marks where that scene begins; the
first scene uses None (starts at 0). type is "draw" (AI illustration, gets drawn)
or "slide" (a designed full-bleed card, pops in). Keep ids stable — assets are
derived from them (scenes/<id>_color.png / _lines.png for draw; scenes/<id>.png for slide)."""
import os, re, json, subprocess, requests, dotenv
dotenv.load_dotenv("/home/georgieporgie/claude_work/home-services-ad-toolkit/.env")
ELEVEN = os.environ["ELEVENLABS_API_KEY"]; DG = os.environ["DEEPGRAM_API_KEY"]
BASE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(BASE, "audio"); COMP = os.path.join(BASE, "comp")
os.makedirs(AUDIO, exist_ok=True); os.makedirs(COMP, exist_ok=True)
VOICE = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs "Rachel" — calm narration (change if desired)

# ---- EDIT THESE (write numbers as spoken words: "thirty six", "two hundred fifty") ----
SCRIPT = ("Meet <name>. <problem>. <tension>. Then <name> found <company>'s <offer>. "
 "<how it works>. <trust: family owned company with thirty six years of experience and "
 "over three thousand five star reviews>. <resolution>. <CTA spoken>. <Company>.")
SCENES = [
 ("s1_problem",    None,                      "draw"),
 ("s2_tension",    "<unique anchor phrase>",  "draw"),
 ("s3_discovery",  "<unique anchor phrase>",  "draw"),
 ("s4_how",        "<unique anchor phrase>",  "draw"),
 ("s5_offer",      "<unique anchor phrase>",  "draw"),
 ("s6_trust",      "family owned company",    "slide"),
 ("s7_resolution", "<unique anchor phrase>",  "draw"),
 ("s8_signoff",    "<unique anchor phrase>",  "slide"),
]
# ---------------------------------------------------------------------------------------

def norm(s): return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
def main():
    mp3 = os.path.join(AUDIO, "vo.mp3")
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}",
        headers={"xi-api-key": ELEVEN, "Content-Type": "application/json"},
        json={"text": SCRIPT, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.15, "use_speaker_boost": True}})
    r.raise_for_status(); open(mp3, "wb").write(r.content)
    dur = float(subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0", mp3],
        capture_output=True, text=True).stdout.strip())
    print(f"VO ok: {dur:.2f}s")
    dg = requests.post("https://api.deepgram.com/v1/listen?model=nova-2&smart_format=false&punctuate=false",
        headers={"Authorization": f"Token {DG}", "Content-Type": "audio/mpeg"}, data=open(mp3,"rb").read()).json()
    words = dg["results"]["channels"][0]["alternatives"][0]["words"]
    toks = [norm(w["word"])[0] for w in words]
    def find(anchor):
        a = norm(anchor)
        for i in range(len(toks)-len(a)+1):
            if toks[i:i+len(a)] == a: return words[i]["start"]
        print("  !! ANCHOR NOT FOUND:", anchor, "-> fix the phrase to match the VO exactly"); return None
    starts = [[sid, (0.0 if anc is None else find(anc)), typ] for sid, anc, typ in SCENES]
    scenes = []
    for i,(sid,t,typ) in enumerate(starts):
        end = starts[i+1][1] if i+1 < len(starts) else dur
        scenes.append({"id": sid, "type": typ, "start": round(t or 0,3), "end": round(end or dur,3), "seed": i+1})
    for i in range(len(scenes)-1): scenes[i]["end"] = scenes[i+1]["start"]
    scenes[-1]["end"] = round(dur,3)
    for s in scenes: s["dur"] = round(s["end"]-s["start"],3)
    json.dump({"audio":"audio/vo.mp3","duration":round(dur,3),"scenes":scenes},
              open(os.path.join(COMP,"scene_timing.json"),"w"), indent=2)
    print("\nScene timing:")
    for s in scenes: print(f"  {s['id']:15s} {s['type']:5s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['dur']:.2f}s)")
if __name__ == "__main__": main()
