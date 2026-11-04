#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
FILM_PYTHON="${FILM_PYTHON:-../.venv/bin/python}"
credits='Music: The Descent, Carefree, Dream Culture by Kevin MacLeod (incompetech.com), CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Excerpts, fades and level changes. Full credits in accompanying CREDITS.md.'
# Both inputs are HyperFrames renders of the same 303 s project. The source
# manifests prove that only rule-window and limits changed. The replacement
# covers their complete spans and dissolves, with unchanged frames at its ends.
ffmpeg -v error -y -i renders/captured-full.mp4 -i renders/rules-corrected.mp4 -i assets/audio/mix.wav \
 -filter_complex "[1:v]setpts=PTS+40/TB[p];[0:v][p]overlay=eof_action=pass:repeatlast=0:enable='gte(t,40)*lt(t,74)'[v]" \
 -map '[v]' -map 2:a:0 -t 303 -r 30 -frames:v 9090 \
 -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 256k \
 -metadata title='Was wäre, wenn du eine Minute in die Zukunft sehen könntest?' \
 -metadata artist='Absurditas' -metadata comment="$credits" -movflags +faststart \
 renders/final-corrected.mp4
mv renders/final-corrected.mp4 renders/WhatIf_Eine_Minute_Voraus_HyperFrames_1080p.mp4
"$FILM_PYTHON" scripts/qc_film.py renders/WhatIf_Eine_Minute_Voraus_HyperFrames_1080p.mp4
