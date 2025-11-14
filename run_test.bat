@echo off
SET VENV_DIR=.venv
if NOT EXIST %VENV_DIR% (
    echo Creating virtualenv
    python -m venv %VENV_DIR%
)
call %VENV_DIR%\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -v
IF %ERRORLEVEL% NEQ 0 (
    echo Tests failed
    EXIT /B %ERRORLEVEL%
)

echo All tests passed
