#!/usr/bin/env bash
# Fix "Video has sparse keyframes" — phone MP4s have 5s+ keyframe intervals
# which cause seek failures during HyperFrames render. Forces 1 keyframe/sec.
#
# Usage:  bash scripts/reencode-footage.sh footage/raw.mov footage/speaker.mp4
set -euo pipefail
IN="$1"
OUT="${2:-footage/speaker.mp4}"
mkdir -p "$(dirname "$OUT")"
ffmpeg -y -i "$IN" \
  -c:v libx264 -r 30 -g 30 -keyint_min 30 -pix_fmt yuv420p \
  -movflags +faststart -c:a copy "$OUT"
echo "re-encoded -> $OUT  (30fps, 1 keyframe/sec)"
echo "Speaker video is referenced MUTED in the template; VO is a separate track."
