#!/usr/bin/env bash
set -euo pipefail

# Create virtualenv if missing
if [ ! -d "venv" ]; then
  python -m venv venv
fi

# Activate venv (works in bash)
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Run pytest with JSON output
pytest --maxfail=1 --disable-warnings -q --json-report --json-report-file=raw_results.json

# Generate a simple summary output.json from the pytest json report
python - <<'PY'
import json
p = json.load(open('raw_results.json'))
summary = {
  'tests_run': p.get('summary', {}).get('total', 0),
  'tests_failed': p.get('summary', {}).get('failed', 0),
  'tests_passed': p.get('summary', {}).get('passed', 0),
  'tests_skipped': p.get('summary', {}).get('skipped', 0),
}
open('output.json','w').write(json.dumps(summary, indent=2))
print('Generated output.json')
PY

echo "Raw report: raw_results.json"
echo "Summary: output.json"
