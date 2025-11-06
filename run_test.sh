#!/usr/bin/env bash
set -euo pipefail

# Create virtualenv if not exists
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run pytest with JSON report
pytest -q --json-report --json-report-file=raw_results.json

# Convert pytest JSON report to output.json using helper
python generate_output.py raw_results.json output.json

echo "Test run complete. output.json created."
