#!/usr/bin/env bash
set -e

# Activate venv
if [ -f .venv/bin/activate ]; then
    . .venv/bin/activate
fi

pytest -q --disable-warnings --maxfail=1
