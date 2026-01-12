#!/bin/bash
# setup.sh - Set up virtual environment and install dependencies
# Works on Linux and macOS

set -e

echo "=== Flask Email Application Setup ==="
echo "Detecting OS..."

OS_TYPE=$(uname -s)
if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "✓ Detected Linux"
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "✓ Detected macOS"
else
    echo "✗ Unsupported OS: $OS_TYPE"
    exit 1
fi

echo ""
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Found: $PYTHON_VERSION"

echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists. Using existing venv."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

echo ""
echo "Installing requirements..."
pip install -r requirements.txt
echo "✓ Requirements installed"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run tests, execute:"
echo "  ./run_test.sh"
echo ""
