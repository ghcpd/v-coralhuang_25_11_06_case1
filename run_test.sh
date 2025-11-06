#!/usr/bin/env bash
set -euo pipefail

# Create virtual environment
PYTHON=${PYTHON:-python}
VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
  $PYTHON -m venv "$VENV_DIR"
fi

# Activate it
source "$VENV_DIR/bin/activate"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run pytest; pytest.ini config creates raw_results.json
pytest -q

# Generate a structured summary output.json
python test_summary.py raw_results.json

echo "Done. Raw JSON results: raw_results.json; Summary: output.json"
