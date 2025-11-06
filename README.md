# Post model audit

This repository contains corrected SQLAlchemy models, unit tests, and a runnable test script that validates timestamp auto-population and relationship resolution for the Post model.

Usage:
- On Windows PowerShell: .\run_test.ps1
- On Unix-like shells: ./run_test.sh

Outputs:
- raw_results.json: JSON test report produced by pytest-json-report
- output.json: simplified summary of tests
- audit_report.json: JSON-formatted audit describing issues and fixes
