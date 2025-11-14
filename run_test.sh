#!/bin/bash
# run_test.sh - Run tests with proper environment activation
# Works on Linux and macOS

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=== Running Flask Email Application Tests ==="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "✗ Virtual environment not found."
    echo "Please run ./setup.sh first."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Running tests with unittest..."
echo ""

python -m pytest tests.py -v 2>/dev/null || python -m unittest tests.py -v

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "=== All tests passed! ==="
    exit 0
else
    echo "=== Tests failed! ==="
    exit 1
fi
