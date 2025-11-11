# Flask Blog App - SQLAlchemy Model Fixes

This project contains fixes for functional bugs in the SQLAlchemy Post model, including timestamp auto-population and relationship configuration.

## Quick Start

### Option 1: Cross-Platform Python Script (Recommended)
```bash
python run_test.py
```

### Option 2: Shell Script (Linux/macOS/Git Bash)
```bash
chmod +x run_test.sh
./run_test.sh
```

### Option 3: Manual Steps
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest test_models.py -v --json-report --json-report-file=raw_results.json

# Generate report
python generate_report.py
```

## Files

- **models.py** - Fixed SQLAlchemy models (User and Post)
- **test_models.py** - Comprehensive test suite
- **run_test.py** - Cross-platform test runner (Windows/Linux/macOS)
- **run_test.sh** - Shell script test runner (Linux/macOS/Git Bash)
- **generate_report.py** - Generates output.json summary report
- **requirements.txt** - Python dependencies
- **EXPLANATION.md** - Detailed explanation of issues and fixes
- **output.json** - Generated audit report (created after running tests)
- **raw_results.json** - Pytest JSON report (created after running tests)

## Issues Fixed

1. **Timestamp Default Bug**: Changed `datetime.utcnow()` to `datetime.utcnow` (function reference)
2. **Missing Foreign Key**: Added `db.ForeignKey('user.id')` to `user_id` column
3. **Missing Backref**: Added `backref='author'` to User.posts relationship

See EXPLANATION.md for detailed information.

## Test Coverage

The test suite verifies:
- ✅ Timestamp auto-population for each Post instance
- ✅ Unique timestamps for different posts
- ✅ Post.author relationship via backref
- ✅ User.posts relationship with lazy='dynamic'
- ✅ Foreign key constraint enforcement

## Output

After running tests, you'll get:
- **raw_results.json**: Pytest JSON report with detailed test results
- **output.json**: Structured summary with issues detected, fixes applied, and verification results

