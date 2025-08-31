@echo off
REM Aladdin Development Environment Launcher (Local API)
REM Batch script to run the PowerShell development setup with local API

echo.
echo ========================================
echo   Aladdin Development Environment
echo   (Genie Frontend - Local API)
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

REM Run the PowerShell script with local API flag
echo Starting development environment with local API...
echo.
echo Starting development server and opening browser...
echo.

REM Start the PowerShell script in background and capture its PID
powershell -ExecutionPolicy Bypass -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0run-dev.ps1\" -UseLocalApi' -WindowStyle Normal"

REM Wait a moment for the server to start
echo Waiting for development server to start...
timeout /t 10 /nobreak >nul

REM Check if server is running by testing the connection
echo Checking if development server is running...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 5 -UseBasicParsing; if ($response.StatusCode -eq 200) { Write-Host 'Server is running' } } catch { Write-Host 'Server not ready yet, waiting...'; Start-Sleep -Seconds 5; try { $response = Invoke-WebRequest -Uri 'http://localhost:3000' -TimeoutSec 5 -UseBasicParsing; if ($response.StatusCode -eq 200) { Write-Host 'Server is now running' } } catch { Write-Host 'Server may not be ready, but opening browser anyway' } }"

REM Open the default browser using the system's default browser handler
echo Opening default browser...
start "" "http://localhost:3000"

REM Alternative: If the above doesn't work, try specific browsers
if errorlevel 1 (
    echo Trying to open with specific browsers...
    
    REM Try Chrome
    where chrome >nul 2>&1
    if not errorlevel 1 (
        echo Opening Chrome...
        start chrome "http://localhost:3000"
    ) else (
        REM Try Edge
        where msedge >nul 2>&1
        if not errorlevel 1 (
            echo Opening Microsoft Edge...
            start msedge "http://localhost:3000"
        ) else (
            REM Try Firefox
            where firefox >nul 2>&1
            if not errorlevel 1 (
                echo Opening Firefox...
                start firefox "http://localhost:3000"
            ) else (
                echo No common browsers found. Please open manually: http://localhost:3000
            )
        )
    )
)

echo.
echo Development environment started!
echo Frontend URL: http://localhost:3000
echo.
echo Press any key to exit this launcher (server will continue running)...
pause >nul
