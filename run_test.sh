#!/usr/bin/env bash
set -euo pipefail

# This script creates a virtual environment, installs dependencies, runs pytest
# and writes a JSON summary to output.json. It also leaves raw_results.json
# produced by pytest-json-report for machine consumption.

VENV_DIR=.venv
PYTHON=${PYTHON:-python3}

if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv $VENV_DIR
fi

# shellcheck disable=SC1090
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run tests and create pytest json report
pytest -q --json-report --json-report-file=raw_results.json

# Convert raw_results.json to simplified output.json containing counts and status
python3 - <<'PY'
import json,sys
with open('raw_results.json') as f:
    raw=json.load(f)
summary={
    'totals': raw.get('summary',{}),
    'duration_seconds': raw.get('duration', None),
    'tests': [{'nodeid':t['nodeid'], 'outcome':t['outcome']} for t in raw.get('tests',[])],
}
with open('output.json','w') as f:
    json.dump(summary, f, indent=2)
print('Test run complete. output.json and raw_results.json created.')
PY
