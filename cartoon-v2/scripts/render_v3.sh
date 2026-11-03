#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p out
.venv/bin/python scripts/make_accents_v3.py
npm run typecheck
NODE_USE_ENV_PROXY=1 npx remotion render src/index.ts WhatIfCartoonV3 out/render-v3-intermediate.mp4 --codec h264 --crf 16 --concurrency 3
ffmpeg -v error -y -i out/render-v3-intermediate.mp4 -i public/cartoon-v2/mix-v3.wav \
  -map 0:v:0 -map 1:a:0 -t 30 -c:v copy -af atrim=duration=30 \
  -c:a aac -b:a 256k -movflags +faststart out/WhatIf_Eine_Minute_Zukunft_Hook_v3_30s.mp4
.venv/bin/python scripts/qc_v3.py
