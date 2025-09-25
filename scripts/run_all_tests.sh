#!/bin/bash

# Shell script to run all tests

echo "========================================"
echo "  Web Automation Test Suite - Run All Tests"
echo "========================================"
echo ""

# Set working directory to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
playwright install --quiet

echo ""
echo "Running all tests..."
echo "========================================"

# Run pytest with comprehensive options
pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html --junit-xml=reports/junit.xml

echo ""
echo "========================================"
echo "Test execution completed!"
echo "Reports generated in: reports/"
echo "========================================"