#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
FILM_PYTHON="${FILM_PYTHON:-../.venv/bin/python}"
mkdir -p renders
input_video="${1:-renders/captured-full.mp4}"
final_video="renders/WhatIf_Eine_Minute_Voraus_HyperFrames_1080p.mp4"
credits='Music: The Descent, Carefree, Dream Culture by Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Excerpts, fades and level changes. Full credits in accompanying CREDITS.md.'
ffmpeg -v error -y -i "$input_video" -i assets/audio/mix.wav \
 -map 0:v:0 -map 1:a:0 -t 303 -c:v copy -c:a aac -b:a 256k \
 -metadata title='Was wäre, wenn du eine Minute in die Zukunft sehen könntest?' \
 -metadata artist='Absurditas' -metadata comment="$credits" -movflags +faststart "$final_video"
# GitHub's ordinary file endpoint accepts files up to 100 MiB. If needed,
# create a visually high-quality CRF 18 delivery encode at the same resolution.
if [ "$(wc -c < "$final_video")" -gt 99000000 ]; then
 ffmpeg -v error -y -i "$final_video" -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy \
  -metadata comment="$credits" -movflags +faststart renders/delivery-compressed.mp4
 mv renders/delivery-compressed.mp4 "$final_video"
fi
"$FILM_PYTHON" scripts/qc_film.py "$final_video"
