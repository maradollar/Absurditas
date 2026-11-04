#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export NODE_USE_ENV_PROXY=1 npm_config_cache=/tmp/absurditas-hyperframes-npm
export HYPERFRAMES_BROWSER_PATH=/workspace/Absurditas/engine/node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell
npx --yes hyperframes@0.9.12 check --json > production/hyperframes-check.json 2> check.log
python3 - <<'PY'
from pathlib import Path
import json,hashlib
r=json.loads(Path('production/hyperframes-check.json').read_text())
assert all(not x.get('errorCount',0) for x in r.values() if isinstance(x,dict)),r
paths=[Path('index.html'),*Path('compositions').rglob('*.html'),*Path('assets').glob('*.js'),*Path('assets/vendor').glob('*.js'),*Path('assets/fonts').glob('*.ttf')]
Path('production/render-source-hashes.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
print('CHECK PASSED. Source frozen:',len(paths),'files',flush=True)
PY
npx --yes hyperframes@0.9.12 render --fps 30 --quality high --workers 4 --output renders/captured-full.mp4
