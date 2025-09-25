# PowerShell script to run tests by category

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("auth", "elements", "forms", "alerts", "smoke", "regression", "slow")]
    [string]$Category
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Web Automation Test Suite - $Category Tests" -ForegroundColor Cyan
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

Write-Host "Running $Category tests..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Map categories to pytest markers or files
switch ($Category) {
    "auth" { 
        pytest tests/test_authentication.py -v --tb=short
    }
    "elements" { 
        pytest tests/test_elements.py -v --tb=short
    }
    "forms" { 
        pytest tests/test_file_upload.py -v --tb=short
    }
    "alerts" { 
        pytest tests/test_alerts.py -v --tb=short
    }
    "smoke" { 
        pytest tests/ -m smoke -v --tb=short
    }
    "regression" { 
        pytest tests/ -m regression -v --tb=short
    }
    "slow" { 
        pytest tests/ -m slow -v --tb=short
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "$Category tests completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan