@echo off
rem ============================================================
rem  Kit 1 ^— Universal Business Core Deployer (Windows)
rem  Edit the three lines below, then double-click this file.
rem ============================================================

set CONFIG_FILE=C:\Users\yourname\path\to\my-business.json
set N8N_URL=https://yourname.app.n8n.cloud
set N8N_API_KEY=your-n8n-api-key-here

rem ^-^- don't edit below this line ^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-

cd /d "%~dp0"

echo.
echo ================================================
echo   Kit 1 ^— Universal Business Core Deployer
echo ================================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found.
    echo Install it from https://www.python.org/downloads/ then try again.
    pause
    exit /b 1
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt --quiet
)

python setup.py --config "%CONFIG_FILE%" --n8n-url "%N8N_URL%" --n8n-key "%N8N_API_KEY%"

echo.
pause
