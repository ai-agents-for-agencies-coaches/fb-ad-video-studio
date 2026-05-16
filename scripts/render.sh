#!/usr/bin/env bash
# Render the composition to MP4. Docker is REQUIRED on Pop!_OS / many Linux
# (apparmor blocks puppeteer). ~2-3 min per 60s comp after the first build.
#
# Usage:  bash scripts/render.sh [project_dir] [out.mp4]
#         bash scripts/render.sh --frame 12.5   # extract one debug frame
set -euo pipefail

if [[ "${1:-}" == "--frame" ]]; then
  T="${2:?need timestamp}"; SRC="${3:-renders/out.mp4}"
  ffmpeg -y -ss "$T" -i "$SRC" -frames:v 1 "frame-${T}.jpg"
  echo "frame @ ${T}s -> frame-${T}.jpg  (eyeball before iterating)"
  exit 0
fi

DIR="${1:-.}"
OUT="${2:-renders/out.mp4}"
mkdir -p "$(dirname "$OUT")"

echo "Linting first (fix media_missing_id / gsap_exit_missing_hard_kill)..."
npx hyperframes lint "$DIR"

echo "Rendering (Docker)..."
npx hyperframes render "$DIR" --docker --output "$OUT"
echo "-> $OUT"
echo "Deliver this MP4. If a new reusable structure, generalize it back to templates/."
