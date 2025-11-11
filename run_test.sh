#!/bin/bash

# One-click test runner script for SQLAlchemy model fixes
# Sets up environment, runs tests, and generates reports

set -e  # Exit on error

echo "=== Flask Blog App - SQLAlchemy Model Fix Test Runner ==="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Determine Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --quiet --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install --quiet -r requirements.txt

# Run tests with pytest-json-report plugin
echo ""
echo "Running tests..."
pytest test_models.py -v --json-report --json-report-file=raw_results.json || true

# Generate output.json summary
echo ""
echo "Generating output.json summary..."
$PYTHON_CMD generate_report.py

echo ""
echo "=== Test Run Complete ==="
echo "Results saved to:"
echo "  - raw_results.json (pytest JSON report)"
echo "  - output.json (structured summary)"

