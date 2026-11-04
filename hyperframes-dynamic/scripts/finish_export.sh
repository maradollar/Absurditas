#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
film_out=renders/WhatIf_Eine_Minute_Voraus_HyperFrames_Dynamic_v2_1080p.mp4
ffmpeg -v error -y -i renders/captured-full.mp4 -i assets/audio/mix.wav \
 -map 0:v:0 -map 1:a:0 -t 344 -frames:v 10320 \
 -c:v copy \
 -c:a aac -b:a 224k -ar 48000 -ac 2 -movflags +faststart \
 -metadata title='Eine Minute voraus – Dynamic Edition' -metadata artist='Absurditas' \
 -metadata comment='Music: The Descent (USUAN1200094), Carefree (USUAN1400037), Dream Culture (USUAN1300046) by Kevin MacLeod, incompetech.com. CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ . Excerpts, fades, level changes.' \
 "$film_out"
FILM_PYTHON="${FILM_PYTHON:-python3}"
"$FILM_PYTHON" scripts/qc_film.py "$film_out"
