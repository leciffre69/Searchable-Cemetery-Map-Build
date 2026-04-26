@echo off
title Llangynidr Graveyard Map

echo.
echo  =========================================
echo   Llangynidr Graveyard - Interactive Map
echo  =========================================
echo.
echo  Starting server on http://localhost:8000
echo  Press Ctrl+C to stop the server.
echo.

:: Change to the folder where this bat file lives
cd /d "%~dp0"

:: Open browser after a short delay (start is non-blocking)
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8000"

:: Start the server (blocking — keeps window open)
python server.py

:: If python is not found, try py launcher
if errorlevel 1 (
    echo.
    echo  Python not found via "python", trying "py"...
    py server.py
)

pause
