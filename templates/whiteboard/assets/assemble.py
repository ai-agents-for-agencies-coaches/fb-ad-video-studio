#!/usr/bin/env python3
"""Mix VO + light SFX and assemble comp/frames into the final MP4.
Run from the build root:  python3 assemble.py [output_name.mp4] [accent_scene_id]
- A soft Woosh plays at each scene transition.
- If accent_scene_id is given, an accent SFX (Pop) plays at that scene's start
  (e.g. an offer reveal / checkmark). Default output: render/whiteboard.mp4"""
import os, sys, json, subprocess
BASE = os.path.dirname(os.path.abspath(__file__))
SFX = "/home/georgieporgie/claude_work/home-services-ad-toolkit/sound_effects"
timing = json.load(open(os.path.join(BASE, "comp/scene_timing.json")))
vo = os.path.join(BASE, "audio/vo.mp3"); mix = os.path.join(BASE, "audio/mix.m4a")
woosh = os.path.join(SFX, "Woosh.mp3"); pop = os.path.join(SFX, "Pop.mp3")
out_name = sys.argv[1] if len(sys.argv) > 1 else "whiteboard.mp4"
accent_id = sys.argv[2] if len(sys.argv) > 2 else None

inputs = ["-i", vo]; filters = ["[0:a]volume=1.0[vo]"]; mixparts = ["[vo]"]; idx = 1
for s in timing["scenes"]:
    if s["start"] < 0.2: continue
    inputs += ["-i", woosh]
    filters.append(f"[{idx}:a]volume=0.22,adelay={int(s['start']*1000)}|{int(s['start']*1000)}[w{idx}]")
    mixparts.append(f"[w{idx}]"); idx += 1
if accent_id:
    acc = next((s for s in timing["scenes"] if s["id"] == accent_id), None)
    if acc:
        inputs += ["-i", pop]
        filters.append(f"[{idx}:a]volume=0.35,adelay={int(acc['start']*1000)}|{int(acc['start']*1000)}[pop]")
        mixparts.append("[pop]")
n = len(mixparts)
filters.append("".join(mixparts) + f"amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.95[aout]")
subprocess.run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(filters),"-map","[aout]",
    "-c:a","aac","-b:a","192k", mix], check=True, capture_output=True)
print("audio mix ok")

out = os.path.join(BASE, "render", out_name); os.makedirs(os.path.dirname(out), exist_ok=True)
enc = subprocess.run(["ffmpeg","-encoders"], capture_output=True, text=True).stdout
vargs = (["-c:v","h264_nvenc","-preset","p4","-cq","20","-b:v","6M"] if "h264_nvenc" in enc
         else ["-c:v","libx264","-crf","18","-preset","medium"])
subprocess.run(["ffmpeg","-y","-framerate","30","-i",os.path.join(BASE,"comp/frames/%05d.png"),
    "-i",mix,*vargs,"-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
    "-map","0:v:0","-map","1:a:0","-shortest", out], check=True, capture_output=True)
dur = subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0",out],
                     capture_output=True, text=True).stdout.strip()
print(f"DONE: {out}  ({os.path.getsize(out)/1e6:.1f} MB, {float(dur):.1f}s)")
