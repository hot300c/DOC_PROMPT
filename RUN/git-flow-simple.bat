@echo off
REM Git Flow Simple Launcher
REM Batch script để chạy Git Flow đơn giản

echo.
echo ========================================
echo   Git Flow Simple
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

REM Note: PowerShell script will automatically find git repository

REM Run the PowerShell script with all arguments
echo Starting Git Flow Simple...
powershell -ExecutionPolicy Bypass -File "%~dp0git-flow-simple.ps1" %*

REM If the script exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Script completed with errors. Press any key to exit...
    pause >nul
)
