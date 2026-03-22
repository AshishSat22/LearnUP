@echo off
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo ERROR: App failed to start. See message above.
    pause
)
