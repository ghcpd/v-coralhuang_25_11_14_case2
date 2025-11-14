#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
if [ -d "$VENV_DIR" ]; then
    echo "Activating virtualenv $VENV_DIR"
    source "$VENV_DIR/bin/activate"
fi

echo "Running tests (pytest if available, otherwise unittest)"
if command -v pytest >/dev/null 2>&1; then
    pytest -q
else
    python -m unittest discover -v
fi

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Tests failed with exit code $EXIT_CODE"
    exit $EXIT_CODE
fi

echo "All tests passed!"
