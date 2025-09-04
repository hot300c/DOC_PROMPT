@echo off
setlocal ENABLEDELAYEDEXPANSION

REM LOAN Project GitHub Manager
REM Simple batch wrapper for PowerShell script

cd /d "%~dp0"

echo ========================================
echo    LOAN GitHub Project Manager
echo ========================================
echo.

if "%1"=="" goto menu

if "%1"=="status" (
    powershell -ExecutionPolicy Bypass -File "github-project-manager.ps1" -Action status
    goto end
)

if "%1"=="inprogress" (
    if "%2"=="" (
        echo Please provide project number: loan-git.bat inprogress [PROJECT_NUMBER]
        goto end
    )
    powershell -ExecutionPolicy Bypass -File "github-project-manager.ps1" -Action inprogress -ProjectNumber %2
    goto end
)

if "%1"=="add" (
    if "%2"=="" (
        echo Please provide title: loan-git.bat add "TASK_TITLE" [PROJECT_NUMBER]
        goto end
    )
    if "%3"=="" (
        echo Please provide project number: loan-git.bat add "TASK_TITLE" [PROJECT_NUMBER]
        goto end
    )
    powershell -ExecutionPolicy Bypass -File "github-project-manager.ps1" -Action add -Title "%2" -ProjectNumber %3
    goto end
)

if "%1"=="board" (
    if "%2"=="" (
        echo Please provide project number: loan-git.bat board [PROJECT_NUMBER]
        goto end
    )
    powershell -ExecutionPolicy Bypass -File "github-project-manager.ps1" -Action board -ProjectNumber %2
    goto end
)

:menu
echo Available commands:
echo.
echo   status                    - Show available projects
echo   inprogress [NUMBER]       - Show in-progress tasks
echo   add "TITLE" [NUMBER]      - Add new task
echo   board [NUMBER]            - Show project board
echo.
echo Examples:
echo   loan-git.bat status
echo   loan-git.bat inprogress 1
echo   loan-git.bat add "Implement notification service" 1
echo   loan-git.bat board 1
echo.

:end
pause
