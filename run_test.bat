@echo off
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
python -m pytest -q --tb=short --maxfail=1
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
