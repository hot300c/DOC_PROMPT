@echo off
REM Clear Next.js Cache Script
REM Batch script to clear Next.js cache

echo.
echo ========================================
echo   Next.js Cache Cleaner
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

REM Check if user wants to clear all (including node_modules)
set /p CLEAR_ALL="Do you want to clear all cache (including node_modules)? (y/N): "
if /i "%CLEAR_ALL%"=="y" (
    echo Clearing all cache including node_modules...
    powershell -ExecutionPolicy Bypass -File "%~dp0clear-cache.ps1" -ClearAll
) else (
    echo Clearing Next.js cache only...
    powershell -ExecutionPolicy Bypass -File "%~dp0clear-cache.ps1"
)

REM If the script exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Script completed with errors. Press any key to exit...
    pause >nul
)
