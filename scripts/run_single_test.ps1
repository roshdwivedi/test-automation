# PowerShell script to run a single test

param(
    [Parameter(Mandatory=$true)]
    [string]$TestName
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Web Automation Test Suite - Single Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory to project root
$ProjectRoot = Split-Path $PSScriptRoot -Parent
Set-Location $ProjectRoot

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

Write-Host "Running test: $TestName" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Run the specific test
pytest tests/ -k "$TestName" -v --tb=short

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test execution completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan