@echo off
REM Aladdin Backend Development Environment Launcher
REM Batch script to run the PowerShell backend development setup

echo.
echo ========================================
echo   Aladdin Backend Development Environment
echo   (WebService API)
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

REM Find aladdin directory from current location
set ALADDIN_DIR=
set CURRENT_DIR=%CD%

REM Check if we're already in aladdin directory
if exist "Aladdin.sln" (
    echo Running from aladdin directory...
    set ALADDIN_DIR=.
    goto :found_aladdin
)

REM Check if aladdin is in current directory
if exist "aladdin\Aladdin.sln" (
    echo Found aladdin in current directory...
    set ALADDIN_DIR=aladdin
    goto :found_aladdin
)

REM Check if we're in DOCS_PROMPT/RUN and need to go up
if exist "..\..\aladdin\Aladdin.sln" (
    echo Found aladdin in parent directory...
    set ALADDIN_DIR=..\..\aladdin
    goto :found_aladdin
)

REM Check if we're in DOCS_PROMPT and need to go up
if exist "..\aladdin\Aladdin.sln" (
    echo Found aladdin in parent directory...
    set ALADDIN_DIR=..\aladdin
    goto :found_aladdin
)

REM Try to find aladdin in C:\PROJECTS
if exist "C:\PROJECTS\aladdin\Aladdin.sln" (
    echo Found aladdin in C:\PROJECTS\aladdin...
    set ALADDIN_DIR=C:\PROJECTS\aladdin
    goto :found_aladdin
)

echo Error: Cannot find aladdin project.
echo Current directory: %CURRENT_DIR%
echo Please ensure aladdin project exists in one of these locations:
echo   - C:\PROJECTS\aladdin
echo   - Current directory or subdirectory
echo   - Parent directories
pause
exit /b 1

:found_aladdin

REM Change to aladdin directory if needed
if not "%ALADDIN_DIR%"=="." (
    cd %ALADDIN_DIR%
)

REM Run the PowerShell script
echo Starting backend development environment...
powershell -ExecutionPolicy Bypass -File "%~dp0run-be-dev.ps1" %*

REM If the script exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Script completed with errors. Press any key to exit...
    pause >nul
)
