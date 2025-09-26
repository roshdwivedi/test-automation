# Test Automation

A straightforward test automation setup using Playwright and pytest. No frills, just reliable end-to-end testing that works across browsers.

## What's in the box

- **Stack**: Python 3.8+, Playwright, pytest with async support
- **Browsers**: Chromium, Firefox, WebKit - pick your poison
- **Reports**: HTML reports for humans, JUnit XML for CI
- **Structure**: Clean Page Objects pattern, organized test files

## Quick start

Create a virtual environment and get everything installed:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
python -m playwright install --with-deps
```

## Running tests

Basic test runs:
```bash
# Run everything
pytest tests/ -v --tb=short --browser-type=chromium

# Just the smoke tests
pytest tests/ -m smoke -v

# Authentication tests only
pytest tests/ -m auth -v

# Specific test
pytest tests/test_authentication.py::TestAuthentication::test_valid_login -v
```

Want it faster? Run tests in parallel:
```bash
pytest tests/ -v -n auto
```

## What you get

After running tests, check out:
- **HTML report**: `reports/report.html` - nice visual overview
- **JUnit XML**: `reports/junit.xml` - for your CI pipeline

## Project layout

```
web_automation_tests/
├─ pages/           # Page Objects go here
├─ tests/           # Your actual tests
├─ reports/         # Generated reports
├─ conftest.py      # Playwright setup and fixtures
└─ pytest.ini      # Test configuration
```

## Test markers

Use these to run specific test groups:
- `smoke` - quick sanity checks
- `regression` - full test suite
- `auth` - authentication tests
- `elements` - UI element tests
- `alerts` - alert handling tests

## CI ready

GitHub Actions workflow included. Runs tests across Python versions 3.8-3.11 and all three browsers. Reports get uploaded as artifacts.

## Tips

- Tests use absolute imports (`from pages.login_page import LoginPage`)
- Page Objects keep your tests clean and maintainable
- Use explicit waits, avoid sleeps
- Clean up artifacts regularly: `.pytest_cache/`, `__pycache__/`, `reports/`

## Troubleshooting

**Import errors?** Make sure you're using absolute imports in your tests.

**Browser issues?** Run `python -m playwright install --with-deps` and `python -m playwright doctor`.

**CI permissions?** The workflow handles fork-safe check runs automatically.

