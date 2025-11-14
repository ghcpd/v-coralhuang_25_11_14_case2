#!/usr/bin/env bash
set -euo pipefail

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "Use PowerShell or Git Bash with Python to create a venv manually on Windows."
    exit 1
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python executable '$PYTHON_BIN' not found." >&2
    exit 1
fi

VENV_DIR=".venv"
if [[ ! -d "$VENV_DIR" ]]; then
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Environment ready. Activate it via 'source .venv/bin/activate'."
