#!/bin/bash

# Shell script to run tests by category

# Check if category parameter is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <category>"
    echo "Available categories: auth, elements, forms, alerts, smoke, regression, slow"
    exit 1
fi

CATEGORY=$1

# Validate category
case $CATEGORY in
    auth|elements|forms|alerts|smoke|regression|slow)
        ;;
    *)
        echo "Invalid category: $CATEGORY"
        echo "Available categories: auth, elements, forms, alerts, smoke, regression, slow"
        exit 1
        ;;
esac

echo "========================================"
echo "  Web Automation Test Suite - $CATEGORY Tests"
echo "========================================"
echo ""

# Set working directory to project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}/../..)" && pwd)"
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo "Running $CATEGORY tests..."
echo "========================================"

# Map categories to pytest markers or files
case $CATEGORY in
    "auth")
        pytest tests/test_authentication.py -v --tb=short
        ;;
    "elements")
        pytest tests/test_elements.py -v --tb=short
        ;;
    "forms")
        pytest tests/test_file_upload.py -v --tb=short
        ;;
    "alerts")
        pytest tests/test_alerts.py -v --tb=short
        ;;
    "smoke")
        pytest tests/ -m smoke -v --tb=short
        ;;
    "regression")
        pytest tests/ -m regression -v --tb=short
        ;;
    "slow")
        pytest tests/ -m slow -v --tb=short
        ;;
esac

echo ""
echo "========================================"
echo "$CATEGORY tests completed!"
echo "========================================"