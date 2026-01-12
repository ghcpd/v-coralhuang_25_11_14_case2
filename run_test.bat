@echo off
REM run_test.bat - Run tests with proper environment activation for Windows

setlocal enabledelayedexpansion

echo === Flask Email Application Tests ===
echo.

REM Check if virtual environment exists (try both .venv and venv)
if exist ".venv" (
    set VENV_DIR=.venv
) else if exist "venv" (
    set VENV_DIR=venv
) else (
    echo Virtual environment not found.
    echo Please run setup.bat first.
    exit /b 1
)

echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)
echo Virtual environment activated
echo.

echo Running tests with unittest...
echo.

python -m unittest tests.py -v

if errorlevel 1 (
    echo.
    echo === Tests failed! ===
    exit /b 1
)

echo.
echo === All tests passed! ===
exit /b 0
