#!/usr/bin/env bash
set -e

if [ -z "$VIRTUAL_ENV" ]; then
    python3 -m venv .venv
fi

# Activate venv
. .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Environment ready. Activate with: source .venv/bin/activate"
