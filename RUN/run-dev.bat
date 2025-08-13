@echo off
REM Aladdin Development Environment Launcher
REM Batch script to run the PowerShell development setup

echo.
echo ========================================
echo   Aladdin Development Environment
echo   (Genie Frontend)
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

REM Find genie directory from current location
set GENIE_DIR=
set CURRENT_DIR=%CD%

REM Check if we're already in genie directory
if exist "package.json" (
    echo Running from genie directory...
    set GENIE_DIR=.
    goto :found_genie
)

REM Check if genie is in current directory
if exist "genie\package.json" (
    echo Found genie in current directory...
    set GENIE_DIR=genie
    goto :found_genie
)

REM Check if we're in DOCS_PROMPT/RUN and need to go up
if exist "..\..\genie\package.json" (
    echo Found genie in parent directory...
    set GENIE_DIR=..\..\genie
    goto :found_genie
)

REM Check if we're in DOCS_PROMPT and need to go up
if exist "..\genie\package.json" (
    echo Found genie in parent directory...
    set GENIE_DIR=..\genie
    goto :found_genie
)

REM Try to find genie in C:\PROJECTS
if exist "C:\PROJECTS\genie\package.json" (
    echo Found genie in C:\PROJECTS\genie...
    set GENIE_DIR=C:\PROJECTS\genie
    goto :found_genie
)

echo Error: Cannot find genie project.
echo Current directory: %CURRENT_DIR%
echo Please ensure genie project exists in one of these locations:
echo   - C:\PROJECTS\genie
echo   - Current directory or subdirectory
echo   - Parent directories
pause
exit /b 1

:found_genie

REM Change to genie directory if needed
if not "%GENIE_DIR%"=="." (
    cd %GENIE_DIR%
)

REM Run the PowerShell script
echo Starting development environment...
powershell -ExecutionPolicy Bypass -File "%~dp0run-dev.ps1" %*

REM If the script exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Script completed with errors. Press any key to exit...
    pause >nul
)
