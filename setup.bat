@echo off
REM setup.bat - Set up virtual environment and install dependencies for Windows

setlocal enabledelayedexpansion

echo === Flask Email Application Setup ===
echo Detecting Windows environment...
echo Detected Windows
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is not installed. Please install Python 3.8 or later.
    echo Download from: https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%A in ('python --version 2^>^&1') do set PYTHON_VERSION=%%A
echo Found: %PYTHON_VERSION%
echo.

echo Creating virtual environment...
if exist ".venv" (
    echo Virtual environment already exists. Using existing .venv.
) else if exist "venv" (
    echo Virtual environment already exists. Using existing venv.
) else (
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        exit /b 1
    )
    echo Virtual environment created
)
echo.

echo Activating virtual environment...
if exist ".venv" (
    call .venv\Scripts\activate.bat
) else (
    call venv\Scripts\activate.bat
)
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)
echo Virtual environment activated
echo.

echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo pip upgraded
echo.

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements
    exit /b 1
)
echo Requirements installed
echo.

echo === Setup Complete ===
echo.
echo To activate the virtual environment in the future, run:
echo   .venv\Scripts\activate.bat
echo.
echo To run tests, execute:
echo   run_test.bat
echo.

pause
