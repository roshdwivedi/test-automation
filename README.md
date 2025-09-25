# Web Automation Test Suite

Playwright + pytest end‑to‑end tests with async support, clean Page Objects, cross‑browser runs, rich reports, and CI out of the box.

- Stack: Python 3.8+, Playwright, pytest, pytest-asyncio, pytest-html
- Browsers: Chromium, Firefox, WebKit
- Reports: HTML, JUnit XML (for CI), optional JSON and coverage

---

## Quick start

1) Create and activate a virtual env
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2) Install dependencies and browsers
```powershell
pip install -r requirements.txt
python -m playwright install --with-deps
```

3) Run tests
```powershell
# All tests (default browser from workflow/fixtures)
pytest tests/ -v --tb=short --browser-type=chromium

# Quick smoke
pytest tests/ -m smoke -v --tb=short --browser-type=chromium

# By marker
pytest tests/ -m auth -v
pytest tests/ -m regression -v

# Specific test/class
pytest tests/test_authentication.py::TestAuthentication::test_valid_login -v
```

4) See reports
- HTML: reports/report.html
- JUnit: reports/junit.xml

Tip: Parallel runs with xdist
```powershell
pytest tests/ -v -n auto
```

---

## Project layout (essentials)
```
web_automation_tests/
├─ pages/           # Page Objects (base_page.py, alerts_page.py, elements_page.py, login_page.py)
├─ tests/           # Tests (authentication, elements, alerts, upload)
├─ reports/         # HTML + JUnit outputs
├─ conftest.py      # Playwright fixtures (browser/page) and options
├─ pytest.ini       # Markers, addopts, timeouts, PYTHONPATH
└─ .github/workflows/  # CI pipelines
```

Notes
- Imports in tests use absolute paths (e.g., `from pages.alerts_page import AlertsPage`).
- Custom CLI option: `--browser-type` (chromium | firefox | webkit) from conftest fixtures.

---

## Useful commands
```powershell
# Headless
pytest tests/ -v --browser-type=chromium --browser-args="--headless=new"

# Coverage
pytest tests/ -v --cov=pages --cov-report=term --cov-report=html:reports/coverage

# JSON report (optional)
pytest tests/ --json-report --json-report-file=reports/report.json
```

---

## CI (GitHub Actions)
- CI runs matrix: Python [3.8–3.11] × Browsers [chromium, firefox, webkit]
- Artifacts uploaded: reports/ (HTML, JUnit)
- Unit test results published via EnricoMi/publish-unit-test-result-action
- Safe for forks: the workflow creates a Check Run only for trusted events and falls back to job summary on forked PRs

Key bits in .github/workflows/ci.yml:
- checks: write permissions on the publish job (for non‑fork contexts)
- Conditional steps:
  - Non‑fork PRs/pushes → `check_run: true`
  - Forked PRs → `check_run: false` and `job_summary: true`

No extra setup is required if you use the provided workflow files. If you enable “Restrict forking” scenarios, ensure repo “Workflow permissions” are set to “Read and write” for first‑party check runs.

---

## Troubleshooting

- ImportError: attempted relative import beyond top‑level package
  - Use absolute imports in tests: `from pages.alerts_page import AlertsPage`
  - `pytest.ini` already sets `pythonpath = .`

- Playwright browser errors / timeouts
  - Install browsers: `python -m playwright install --with-deps`
  - Verify: `python -m playwright doctor`

- GitHub action 403 “Resource not accessible by integration” (check runs)
  - First‑party PRs/pushes: publish job has `checks: write` and will create a Check Run
  - Forked PRs: workflow auto‑disables check runs and posts only to the job summary

---

## Markers (categories)
- smoke, regression, slow, auth, elements, forms, alerts
```powershell
pytest -m smoke -v
pytest -m "auth and not slow" -v
```

---

## Contributing / maintenance
- Keep tests independent and explicit (Arrange‑Act‑Assert)
- Encapsulate UI interactions in Page Objects
- Prefer explicit waits over sleeps
- Regularly clean artifacts: `.pytest_cache/`, `__pycache__/`, `reports/`

---

Happy testing! 🚀
