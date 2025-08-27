@echo off
REM Cursor AI Close & Setup Runner Script
REM This script runs the Python cursor close and setup script

echo ========================================
echo    CURSOR AI CLOSE & SETUP RUNNER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if the Python script exists
if not exist "%~dp0cursor_logout.py" (
    echo ERROR: cursor_logout.py not found in the same directory
    echo Please ensure both files are in the same folder
    echo.
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.
echo Running Cursor AI Close & Setup Script...
echo.
echo IMPORTANT: This script will ask for confirmation that you have
echo already logged out of your Cursor account before proceeding.
echo.
echo This script will:
echo 1. Ask for logout confirmation
echo 2. Close Cursor AI processes
echo 3. Open Terminal with PowerShell command for cursor-free-vip
echo 4. Open Chrome with profile for account deletion
echo 5. Ask if you want to reopen Cursor after account deletion
echo 6. Clean up Terminal and Chrome after setup completion
echo.

REM Run the Python script
python "%~dp0cursor_logout.py"

REM Check if the script ran successfully
if %errorlevel% equ 0 (
    echo.
    echo Script completed successfully!
) else (
    echo.
    echo Script encountered an error (exit code: %errorlevel%)
)

echo.
pause
