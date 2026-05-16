#!/usr/bin/env bash
# Fetch + tight-trim ad SFX from Mixkit (free, commercial, no attribution).
# Mixkit SFX previews ARE the full clip. Find IDs at mixkit.co/free-sound-effects/
# and paste the preview URLs below. Output lands in assets/sfx/.
#
# Usage:  bash scripts/fetch-sfx.sh
set -euo pipefail
OUT="${1:-assets/sfx}"
mkdir -p "$OUT"

# id  ->  Mixkit preview URL  (replace with the ones you picked)
declare -A SFX=(
  [whoosh]="https://assets.mixkit.co/active_storage/sfx/2308/2308-preview.mp3"
  [punch]="https://assets.mixkit.co/active_storage/sfx/2648/2648-preview.mp3"
  [ding]="https://assets.mixkit.co/active_storage/sfx/2870/2870-preview.mp3"
  [stamp]="https://assets.mixkit.co/active_storage/sfx/1655/1655-preview.mp3"
)
# tight ad lengths (s): whoosh .6  punch .22  ding .65  stamp .5
declare -A LEN=( [whoosh]=0.6 [punch]=0.22 [ding]=0.65 [stamp]=0.5 )
# gain under VO: punch -3dB, ding -8dB
declare -A VOL=( [whoosh]=-2 [punch]=-3 [ding]=-8 [stamp]=-4 )

for k in "${!SFX[@]}"; do
  raw="$OUT/.${k}-raw.mp3"
  curl -fsSL "${SFX[$k]}" -o "$raw"
  L="${LEN[$k]}"; FO=$(echo "$L - 0.05" | bc)
  ffmpeg -y -loglevel error -i "$raw" -t "$L" \
    -af "afade=t=out:st=${FO}:d=0.05,volume=${VOL[$k]}dB" \
    -ac 2 -b:a 192k "$OUT/${k}.mp3"
  rm -f "$raw"
  echo "  $OUT/${k}.mp3  (${L}s)"
done
echo "Done. Reference these in the template's <audio> SFX rail."
