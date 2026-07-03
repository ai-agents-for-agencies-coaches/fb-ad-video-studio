#!/usr/bin/env python3
"""Derive the whiteboard LINE layer for every draw scene: extract the cartoon's own
bold black outlines as anti-aliased black-on-transparent. Run from the build root
after gen_scenes.py:  python3 make_lineart.py
Produces scenes/<id>_lines.png for each scenes/<id>_color.png.

Why extract (not vectorize): the drawn line must be the cartoon's REAL outline so it
registers pixel-perfectly with the color that paints in on top. Never skeletonize /
trace to SVG strokes — that mangles faces."""
import os, glob, numpy as np
from PIL import Image
BASE = os.path.dirname(os.path.abspath(__file__)); SC = os.path.join(BASE, "scenes")
def lineart(src, dst, thresh=105, sat_max=70, feather=40):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.int16)
    lum = 0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]
    sat = a.max(2) - a.min(2)
    alpha = np.clip((thresh - lum)/feather, 0, 1) * (sat < sat_max)
    z = np.zeros_like(lum)
    Image.fromarray(np.dstack([z, z, z, alpha*255]).astype("uint8"), "RGBA").save(dst)
if __name__ == "__main__":
    for cp in sorted(glob.glob(os.path.join(SC, "*_color.png"))):
        dst = cp.replace("_color.png", "_lines.png")
        lineart(cp, dst); print("lineart", os.path.basename(dst))
