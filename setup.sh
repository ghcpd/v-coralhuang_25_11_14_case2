#!/usr/bin/env bash
set -euo pipefail

PYTHON=${PYTHON:-python3}
PLATFORM=$(uname -s)
echo "Detected platform: $PLATFORM"

if ! command -v "$PYTHON" &>/dev/null; then
  echo "$PYTHON is required but not found in PATH" >&2
  exit 1
fi

if [ ! -d "venv" ]; then
  "$PYTHON" -m venv venv
fi

# shellcheck source=/dev/null
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
