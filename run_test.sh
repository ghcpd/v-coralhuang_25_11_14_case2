#!/usr/bin/env bash
set -euo pipefail

if [ ! -d "venv" ]; then
  echo "Virtual environment is missing. Run ./setup.sh first." >&2
  exit 1
fi

# shellcheck source=/dev/null
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest tests -s
