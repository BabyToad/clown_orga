#!/bin/bash
# Script to run all tests with coverage report

echo "================================================"
echo "Workshop Allocation Tool - Test Suite"
echo "================================================"
echo ""

# Check if pytest is installed
if ! python3 -m pytest --version > /dev/null 2>&1; then
    echo "Error: pytest not found. Please install dependencies:"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "Running all tests..."
echo ""

# Run tests with coverage
python3 -m pytest \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    -v

TEST_EXIT_CODE=$?

echo ""
echo "================================================"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed!"
    echo ""
    echo "Coverage report generated in htmlcov/index.html"
else
    echo "❌ Some tests failed."
    exit 1
fi

echo "================================================"
