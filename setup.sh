#!/usr/bin/env bash
set -euo pipefail

# Detect platform
OS=$(uname -s)
VENV_DIR=".venv"
PYTHON="python3"
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
fi

echo "Using Python: $($PYTHON --version 2>&1)"

# create virtualenv if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv at $VENV_DIR"
    $PYTHON -m venv $VENV_DIR
fi

# Install dependencies
echo "Installing dependencies into $VENV_DIR"
$VENV_DIR/bin/$PYTHON -m pip install --upgrade pip
$VENV_DIR/bin/$PYTHON -m pip install -r requirements.txt

# Show a success message
echo "Setup complete. Activate the virtualenv with: source $VENV_DIR/bin/activate"