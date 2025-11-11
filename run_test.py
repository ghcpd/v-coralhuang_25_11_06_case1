#!/usr/bin/env python3
"""
Cross-platform test runner for SQLAlchemy model fixes.
Works on Windows, Linux, and macOS.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    return result

def main():
    print("=== Flask Blog App - SQLAlchemy Model Fix Test Runner ===\n")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Using Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Determine if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        # Create virtual environment if it doesn't exist
        venv_path = Path('venv')
        if not venv_path.exists():
            print("Creating virtual environment...")
            run_command([sys.executable, '-m', 'venv', 'venv'])
        
        # Determine activation script path
        if sys.platform == 'win32':
            venv_python = venv_path / 'Scripts' / 'python.exe'
            venv_pip = venv_path / 'Scripts' / 'pip.exe'
        else:
            venv_python = venv_path / 'bin' / 'python'
            venv_pip = venv_path / 'bin' / 'pip'
        
        python_cmd = str(venv_python)
        pip_cmd = str(venv_pip)
    else:
        python_cmd = sys.executable
        pip_cmd = f"{sys.executable} -m pip"
        print("Using existing virtual environment...")
    
    # Upgrade pip
    print("Upgrading pip...")
    run_command([python_cmd, '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip'], check=False)
    
    # Install dependencies
    print("Installing dependencies...")
    run_command([python_cmd, '-m', 'pip', 'install', '--quiet', '-r', 'requirements.txt'])
    
    # Run tests with pytest-json-report plugin
    print("\nRunning tests...")
    result = run_command([
        python_cmd, '-m', 'pytest', 
        'test_models.py', 
        '-v', 
        '--json-report', 
        '--json-report-file=raw_results.json'
    ], check=False)
    
    # Generate output.json summary
    print("\nGenerating output.json summary...")
    run_command([python_cmd, 'generate_report.py'])
    
    print("\n=== Test Run Complete ===")
    print("Results saved to:")
    print("  - raw_results.json (pytest JSON report)")
    print("  - output.json (structured summary)")
    
    # Exit with test result code
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()

