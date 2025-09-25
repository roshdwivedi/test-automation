# Web Automation Test Suite

A comprehensive test automation framework for web application testing using **Playwright** and **pytest**. This suite provides robust, scalable, and maintainable test automation solutions for modern web applications.

## Features

- **Cross-browser Testing**: Support for Chromium, Firefox, and WebKit browsers
- **Async/Await Support**: Modern asynchronous testing approach
- **Page Object Model**: Clean, maintainable test architecture
- **Comprehensive Reporting**: HTML, JUnit XML, and JSON report generation
- **Parallel Execution**: Run tests concurrently for faster execution
- **Test Categorization**: Organized test execution using pytest markers
- **CI/CD Ready**: Integration-friendly configuration and reporting

## Project Structure

```
web_automation_tests/
├── pages/                  # Page Object Model classes
│   ├── base_page.py       # Base page with common functionality
│   ├── login_page.py      # Login page interactions
│   ├── elements_page.py   # Element interaction page
│   ├── alerts_page.py     # JavaScript alerts handling
│   └── __init__.py
├── tests/                 # Test cases
│   ├── test_authentication.py  # Login/logout tests
│   ├── test_elements.py        # Element interaction tests
│   ├── test_alerts.py          # JavaScript alert tests
│   ├── test_file_upload.py     # File upload tests
│   └── __init__.py
├── scripts/               # Utility scripts
│   ├── run_all_tests.ps1      # Run all tests
│   ├── run_category_tests.ps1 # Run tests by category
│   └── run_single_test.ps1    # Run individual tests
├── reports/               # Test execution reports
├── config/                # Configuration files
├── utils/                 # Utility functions
├── conftest.py           # Pytest fixtures and configuration
├── pytest.ini           # Pytest configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Prerequisites

- **Python 3.8+**
- **Node.js 14+** (for Playwright browsers)
- **PowerShell** (for Windows scripts)

## Installation

### 1. Clone or Download the Project
```powershell
# Navigate to project directory
cd web_automation_tests
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
```

### 3. Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows Command Prompt
.\venv\Scripts\activate.bat
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Install Playwright Browsers
```powershell
playwright install
```

## Running Tests

### Quick Start - Run All Tests
```powershell
# Using the PowerShell script (recommended)
.\scripts\run_all_tests.ps1

# Or using pytest directly
pytest tests/ -v
```

### Run Tests by Category

#### Using PowerShell Scripts
```powershell
# Authentication tests
.\scripts\run_category_tests.ps1 -Category auth

# Element interaction tests
.\scripts\run_category_tests.ps1 -Category elements

# JavaScript alerts tests
.\scripts\run_category_tests.ps1 -Category alerts

# Smoke tests (quick validation)
.\scripts\run_category_tests.ps1 -Category smoke

# Full regression tests
.\scripts\run_category_tests.ps1 -Category regression

# Slow-running tests
.\scripts\run_category_tests.ps1 -Category slow
```

#### Using pytest Markers
```powershell
# Run smoke tests
pytest tests/ -m smoke -v

# Run authentication tests
pytest tests/ -m auth -v

# Run regression tests
pytest tests/ -m regression -v

# Run specific test categories
pytest tests/ -m "auth and smoke" -v
```

### Run Individual Tests
```powershell
# Using PowerShell script
.\scripts\run_single_test.ps1 -TestName "test_valid_login"

# Using pytest
pytest tests/ -k "test_valid_login" -v

# Run specific test class
pytest tests/test_authentication.py::TestAuthentication -v

# Run specific test method
pytest tests/test_authentication.py::TestAuthentication::test_valid_login -v
```

### Run Tests with Additional Options

#### Headless Mode (Faster)
```powershell
pytest tests/ -v --browser-args="--headless"
```

#### Parallel Execution
```powershell
pytest tests/ -v -n auto  # Use all CPU cores
pytest tests/ -v -n 4     # Use 4 parallel workers
```

#### With Coverage Report
```powershell
pytest tests/ -v --cov=pages --cov-report=html --cov-report=term
```

#### Different Browsers
```powershell
pytest tests/ -v --browser chromium
pytest tests/ -v --browser firefox
pytest tests/ -v --browser webkit
```

## Test Reports

### HTML Reports
- **Location**: `reports/report.html`
- **Features**: Interactive HTML report with test results, screenshots, and execution details
- **Auto-generated** with every test run

### JUnit XML Reports
- **Location**: `reports/junit.xml`
- **Use Case**: CI/CD integration (Jenkins, Azure DevOps, etc.)
- **Format**: Standard JUnit XML format

### JSON Reports (Optional)
```powershell
pytest tests/ --json-report --json-report-file=reports/report.json
```

### Coverage Reports (Optional)
```powershell
pytest tests/ --cov=pages --cov-report=html:reports/coverage
```

## Test Markers

The test suite uses pytest markers for test categorization:

| Marker | Description | Usage |
|--------|-------------|-------|
| `smoke` | Quick validation tests | `pytest -m smoke` |
| `regression` | Full regression test suite | `pytest -m regression` |
| `slow` | Long-running tests | `pytest -m slow` |
| `auth` | Authentication tests | `pytest -m auth` |
| `elements` | DOM element interaction tests | `pytest -m elements` |
| `forms` | Form interaction tests | `pytest -m forms` |
| `alerts` | JavaScript alert tests | `pytest -m alerts` |

## Configuration

### Browser Configuration
Edit `conftest.py` to modify browser settings:
```python
browser = await playwright.chromium.launch(
    headless=False,     # Set to True for headless mode
    slow_mo=100,        # Delay between actions (ms)
)
```

### Test Configuration
Modify `pytest.ini` for test behavior:
```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py

# Output options
addopts = 
    -v
    --tb=short
    --html=reports/report.html
    --junit-xml=reports/junit.xml

# Test timeout
timeout = 300
```

## Cleaning Up

### Remove Cache Files
```powershell
# Remove pytest cache
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue

# Remove Python cache files
Get-ChildItem -Name "__pycache__" -Recurse | Remove-Item -Recurse -Force

# Remove old reports (optional)
Remove-Item -Path "reports\*.html" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "reports\*.xml" -Force -ErrorAction SilentlyContinue

# Remove coverage files (if generated)
Remove-Item -Path "htmlcov" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
```

### Complete Cleanup Script
```powershell
# Run this to clean all temporary files
Get-ChildItem -Name "__pycache__" -Recurse | Remove-Item -Recurse -Force
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Remove-Item -Path "reports\*.html" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "reports\*.xml" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "htmlcov" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".coverage" -Force -ErrorAction SilentlyContinue
```

## GitHub Actions CI/CD

This project includes comprehensive GitHub Actions workflows for automated testing and deployment.

### Available Workflows

#### 1. **CI Workflow** (`ci.yml`)
**Triggers:** Push to main/develop, Pull Requests
**Features:**
- Cross-browser testing (Chromium, Firefox, WebKit)
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11)
- Automatic test result publishing
- Artifact uploads for test reports

#### 2. **Nightly Regression** (`nightly.yml`)
**Triggers:** Daily at 2 AM UTC, Manual dispatch
**Features:**
- Full regression test suite
- Coverage report generation
- Automatic issue creation on failure
- Comprehensive test reporting

#### 3. **Release Workflow** (`release.yml`)
**Triggers:** Version tags (v*)
**Features:**
- Pre-release testing
- Automatic GitHub release creation
- Release notes generation
- Asset packaging

#### 4. **Manual Test Execution** (`manual-tests.yml`)
**Triggers:** Manual dispatch with inputs
**Features:**
- Custom test category selection
- Browser-specific testing
- Python version selection
- Environment-specific testing
- Real-time result comments

### Setting Up GitHub Actions

#### 1. **Repository Setup**
```bash
# Create a new repository on GitHub
# Clone your repository
git clone https://github.com/roshdwivedi/test-automation
cd your-repo

# Copy your project files
cp -r path/to/web_automation_tests/* .

# Commit and push
git add .
git commit -m "Initial commit: Web Automation Test Suite"
git push origin main
```

#### 2. **Workflow Files Structure**
```
.github/
└── workflows/
    ├── ci.yml              # Main CI pipeline
    ├── nightly.yml         # Nightly regression tests
    ├── release.yml         # Release automation
    └── manual-tests.yml    # Manual test execution
```

#### 3. **Running Manual Tests**
1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select **Manual Test Execution** workflow
4. Click **Run workflow**
5. Choose your options:
   - **Test Category:** smoke, regression, auth, elements, etc.
   - **Browser:** chromium, firefox, webkit, all
   - **Python Version:** 3.8, 3.9, 3.10, 3.11
   - **Environment:** staging, production

### GitHub Actions Benefits

#### **Automated Quality Gates**
- ✅ All PRs must pass tests before merge
- ✅ Cross-browser compatibility validation
- ✅ Multi-Python version compatibility
- ✅ Automatic test result reporting

#### **Continuous Monitoring**
- 🌙 Nightly regression testing
- 📧 Automatic failure notifications
- 📊 Test trend analysis
- 🔍 Coverage tracking

#### **Release Automation**
- 🚀 Automated release creation
- 📝 Auto-generated release notes
- ✅ Pre-release testing
- 📦 Asset packaging

### Viewing Results

#### **Test Reports**
1. Go to **Actions** tab in your repository
2. Click on any workflow run
3. Download artifacts:
   - `test-results-*`: HTML reports
   - `junit-results-*`: JUnit XML files
   - `nightly-test-results`: Nightly reports

#### **Test Result Integration**
- **Pull Requests**: Automatic status checks
- **Commit Comments**: Manual test results
- **Issues**: Automatic creation on nightly failures
- **Releases**: Test confirmation before release

### Configuration

#### **Environment Variables**
Set these in your repository settings under **Secrets and variables > Actions**:

```bash
# Optional: Custom test environment URLs
STAGING_URL=https://staging.example.com
PRODUCTION_URL=https://production.example.com

# Optional: Slack/Teams webhook for notifications
SLACK_WEBHOOK=https://hooks.slack.com/...
```

#### **Branch Protection**
Recommended branch protection rules for `main`:
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require CI - Web Automation Tests
- ✅ Restrict pushes that create files

### Workflow Examples

#### **Basic CI Check**
```bash
# This runs automatically on every push/PR
Trigger: git push origin feature-branch
Result: Cross-browser tests on 3 browsers × 4 Python versions = 12 test jobs
```

#### **Manual Smoke Test**
```bash
# Run quick validation before demo
Workflow: Manual Test Execution
Inputs: Category=smoke, Browser=chromium, Python=3.11
Result: Fast feedback in ~5 minutes
```

#### **Release Process**
```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
Result: Full test suite → Create GitHub release → Notify team
```

### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh 'venv/bin/pip install -r requirements.txt'
                sh 'venv/bin/playwright install'
            }
        }
        stage('Test') {
            steps {
                sh 'venv/bin/pytest tests/ -v --junit-xml=reports/junit.xml'
            }
            post {
                always {
                    junit 'reports/junit.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
    }
}
```

## Dependencies

### Core Dependencies
- **pytest**: Testing framework
- **playwright**: Browser automation
- **pytest-asyncio**: Async test support
- **pytest-html**: HTML report generation
- **pytest-xdist**: Parallel test execution

### Development Dependencies
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

### Optional Dependencies
- **pytest-cov**: Code coverage
- **pytest-json-report**: JSON reporting
- **pytest-mock**: Mock utilities

## Best Practices

### Test Writing
1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **Use Descriptive Names**: Test names should describe what they test
3. **Keep Tests Independent**: Each test should be able to run standalone
4. **Use Page Objects**: Encapsulate page interactions in page classes
5. **Add Appropriate Markers**: Tag tests for easy categorization

### Page Objects
1. **Single Responsibility**: Each page class represents one page
2. **Return Page Objects**: Methods should return page objects for chaining
3. **Hide Implementation**: Abstract away complex interactions
4. **Use Explicit Waits**: Wait for elements before interacting

### Maintenance
1. **Regular Updates**: Keep dependencies updated
2. **Clean Reports**: Regularly clean old report files
3. **Review Failures**: Investigate and fix failing tests promptly
4. **Monitor Performance**: Track test execution times

## Troubleshooting

### Common Issues

#### Browser Launch Failures
```powershell
# Reinstall browsers
playwright install

# Check browser installation
playwright doctor
```

#### Module Import Errors
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```
