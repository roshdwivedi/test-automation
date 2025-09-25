# PowerShell script to run all tests

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Web Automation Test Suite - Run All Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory to project root
$ProjectRoot = Split-Path $PSScriptRoot -Parent
Set-Location $ProjectRoot

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
playwright install --quiet

Write-Host ""
Write-Host "Running all tests..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Run pytest with comprehensive options
pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html --junit-xml=reports/junit.xml

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test execution completed!" -ForegroundColor Cyan
Write-Host "Reports generated in: reports/" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan