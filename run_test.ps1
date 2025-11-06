# PowerShell script to create venv, install requirements, run pytest and produce JSON outputs
$venv = ".venv"
if (-Not (Test-Path $venv)) {
    py -3 -m venv $venv
}
$activate = "$venv\Scripts\Activate.ps1"
if (Test-Path $activate) { . $activate } else { Write-Error "Activate script not found" }
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q --json-report --json-report-file=raw_results.json
python - <<'PY'
import json
with open('raw_results.json') as f:
    raw = json.load(f)
summary = { 'totals': raw.get('summary', {}), 'duration_seconds': raw.get('duration', None)}
with open('output.json', 'w') as f:
    json.dump(summary, f, indent=2)
print('Created output.json')
PY
