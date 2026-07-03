#!/usr/bin/env python3
"""TEMPLATE — generate consistent cartoon scene illustrations via Gemini 2.5 Flash Image.
Edit CHAR, STYLE, SCENES, NOREF. Run per scene:  python3 gen_scenes.py s1_problem
or all at once:  python3 gen_scenes.py

The FIRST scene establishes the character. Every other CHARACTER scene passes the first
scene's image as a reference so the character stays identical. Scenes with NO recurring
character (product/tech shots, a crew, an aerial view) MUST be listed in NOREF, or the
reference dominates and just copies scene 1. Prompts should say "no text, leave blank"
for any label/badge so the model doesn't render garbled words."""
import os, sys, base64, requests, dotenv
from PIL import Image
dotenv.load_dotenv("/home/georgieporgie/claude_work/home-services-ad-toolkit/.env")
KEY = os.environ["GEMINI_API_KEY"]
BASE = os.path.dirname(os.path.abspath(__file__)); SC = os.path.join(BASE, "scenes"); os.makedirs(SC, exist_ok=True)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={KEY}"

FIRST = "s1_problem"   # id of the establishing scene (others reference it)
CHAR = ("<Name> is a <age/gender> with <hair>, <distinguishing features>, wearing <outfit>. "
 "Keep <their> face, hair and outfit EXACTLY consistent.")
STYLE = ("Flat 2D cartoon vector illustration, clean BOLD solid black outlines, soft flat cel shading, "
 "warm friendly palette, simple whiteboard-explainer style, single centered subject with generous "
 "empty margins, on a PURE WHITE #FFFFFF background, absolutely NO text, no words, no logos, no border, "
 "vertical portrait composition.")
NOREF = {"s4_how"}     # ids that should NOT use the character reference
SCENES = {
 "s1_problem":    "<establishing scene: the character + their problem>",
 "s2_tension":    "<the pain / what they dread>",
 "s3_discovery":  "<they discover the solution>",
 "s4_how":        "<how it works — product/UI/tech, usually no person>",
 "s5_offer":      "<the payoff / offer moment>",
 "s7_resolution": "<happy ending>",
}
def gen(prompt, refs=()):
    parts=[{"text": prompt}]
    for rp in refs: parts.append({"inline_data":{"mime_type":"image/png","data":base64.b64encode(open(rp,"rb").read()).decode()}})
    r=requests.post(URL, json={"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"]}}, timeout=180)
    if r.status_code!=200: print("  HTTP",r.status_code,r.text[:200]); return None
    for p in r.json()["candidates"][0]["content"]["parts"]:
        d=p.get("inlineData") or p.get("inline_data")
        if d: return base64.b64decode(d["data"])
    return None
def process(name, prompt):
    ref = os.path.join(SC, FIRST+"_color.png")
    use = [] if (name==FIRST or name in NOREF) else ([ref] if os.path.exists(ref) else [])
    png = gen(f"{STYLE} {'' if name in NOREF else CHAR} SCENE: {prompt}", refs=use)
    if not png: print(f"  {name}: FAILED"); return
    open(os.path.join(SC,f"{name}_color.png"),"wb").write(png)
    print(f"  {name}: ok{' (ref)' if use else ''}")
if __name__=="__main__":
    only=sys.argv[1] if len(sys.argv)>1 else None
    for n,p in SCENES.items():
        if only and n!=only: continue
        process(n,p)
    print("done")
