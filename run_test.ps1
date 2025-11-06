# Windows PowerShell script to create venv, install deps, run pytest and generate a summary
$ErrorActionPreference = 'Stop'
$python = $env:PYTHON; if (-not $python) { $python = "python" }
$venvDir = ".venv"

if (-not (Test-Path $venvDir)) {
    & $python -m venv $venvDir
}

# Activate venv for the current script
. .\$venvDir\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

pytest -q

python test_summary.py raw_results.json

echo "Done. Raw JSON results: raw_results.json; Summary: output.json"
