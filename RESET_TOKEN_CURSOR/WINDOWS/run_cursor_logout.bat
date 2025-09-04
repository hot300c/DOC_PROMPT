@echo off
REM Cursor AI Close Runner Script
REM This script runs the Python cursor close script

echo ========================================
echo    CURSOR AI CLOSE RUNNER
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
echo Running Cursor AI Close Script...
echo.
echo NOTE: This script only closes Cursor AI processes
echo       No data, cache, or settings will be deleted
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
