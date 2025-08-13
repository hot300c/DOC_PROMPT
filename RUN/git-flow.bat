@echo off
REM Git Flow Automation Launcher
REM Batch script to run the PowerShell Git Flow automation

echo.
echo ========================================
echo   Git Flow Automation
echo ========================================
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell is available'" >nul 2>&1
if errorlevel 1 (
    echo Error: PowerShell is not available on this system.
    echo Please install PowerShell and try again.
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist ".git" (
    echo Error: Not a git repository.
    echo Please run this script from a git repository.
    pause
    exit /b 1
)

REM Run the PowerShell script with all arguments
echo Starting Git Flow automation...
powershell -ExecutionPolicy Bypass -File "%~dp0git-flow.ps1" %*

REM If the script exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Script completed with errors. Press any key to exit...
    pause >nul
)
