#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [[ ! -d "$VENV_DIR" ]]; then
    echo "Virtual environment not found. Run ./setup.sh first." >&2
    exit 1
fi

source "$VENV_DIR/bin/activate"
pytest -q -s
