@echo off
SETLOCAL

IF NOT EXIST .venv (
    echo Virtual environment not found. Please run setup.sh (WSL/macOS/Linux) or create .venv manually.
    EXIT /B 1
)

CALL .venv\Scripts\activate
pytest -q
EXIT /B %ERRORLEVEL%
