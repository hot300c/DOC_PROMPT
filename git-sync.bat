@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Change to the directory of this script (project root)
cd /d "%~dp0"

REM Validate working directory
set EXPECTED_DIR=C:\PROJECTS\DOCS_PROMPT
if /i not "%CD%"=="%EXPECTED_DIR%" (
  echo Current directory is "%CD%".
  echo Expected directory is "%EXPECTED_DIR%".
  echo Please run the script from the correct project root.
  exit /b 1
)

REM Ensure git is available
where git >nul 2>nul
if errorlevel 1 (
  echo Git is not installed or not in PATH.
  exit /b 1
)

REM Ensure we're in a git repository
for /f "delims=" %%i in ('git rev-parse --is-inside-work-tree 2^>nul') do set INSIDE=%%i
if /i not "!INSIDE!"=="true" (
  echo This directory is not a git repository.
  exit /b 1
)

REM Validate remote origin URL
for /f "delims=" %%r in ('git config --get remote.origin.url 2^>nul') do set REMOTE=%%r
if "!REMOTE!"=="" (
  echo Could not retrieve remote.origin.url.
  exit /b 1
)
set EXPECTED_HTTPS=https://github.com/hot300c/DOC_PROMPT_VNVC
set EXPECTED_HTTPS_GIT=https://github.com/hot300c/DOC_PROMPT_VNVC.git
set EXPECTED_SSH=git@github.com:hot300c/DOC_PROMPT_VNVC.git
if /i not "!REMOTE!"=="%EXPECTED_HTTPS%" if /i not "!REMOTE!"=="%EXPECTED_HTTPS_GIT%" if /i not "!REMOTE!"=="%EXPECTED_SSH%" (
  echo Remote origin URL is "!REMOTE!".
  echo Expected one of:
  echo   %EXPECTED_HTTPS%
  echo   %EXPECTED_HTTPS_GIT%
  echo   %EXPECTED_SSH%
  echo Please fix the git remote before proceeding.
  exit /b 1
)

REM Fetch and rebase latest changes
echo Pulling latest changes...
git pull --rebase --autostash
if errorlevel 1 (
  echo Failed to pull latest changes. Resolve issues and try again.
  exit /b 1
)

REM Stage all changes
echo Staging changes...
git add -A

REM Check if there is anything to commit
git diff --cached --quiet
if %errorlevel%==0 (
  echo No changes to commit. Up to date.
  goto push
)

REM Use provided commit message or fallback to timestamped default
set MSG=%*
if "%MSG%"=="" set MSG=chore: auto-commit %date% %time%

echo Committing changes...
git commit -m "%MSG%"
if errorlevel 1 (
  echo Commit failed. Resolve issues and try again.
  exit /b 1
)

:push
echo Pushing to remote...
git push
if errorlevel 1 (
  echo Push failed. Resolve issues and try again.
  exit /b 1
)

echo Done.
exit /b 0
