#!/bin/bash

# Shell script to run a single test

# Check if test name parameter is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <test_name>"
    echo "Example: $0 test_valid_login"
    exit 1
fi

TEST_NAME=$1

echo "========================================"
echo "  Web Automation Test Suite - Single Test"
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

echo "Running test: $TEST_NAME"
echo "========================================"

# Run the specific test
pytest tests/ -k "$TEST_NAME" -v --tb=short

echo ""
echo "========================================"
echo "Test execution completed!"
echo "========================================"