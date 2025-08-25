@echo off
echo ========================================
echo Opening Playwright UI
echo ========================================
echo.

REM Check if playwright directory exists
if not exist "C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright" (
    echo Error: Playwright directory not found at C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Current directory: %CD%
echo Moving to playwright directory...
cd C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright

echo.
echo Opening Playwright UI with all test files...
echo This will open a browser window where you can see and run all tests.
echo.

REM Open Playwright UI
npx playwright test --ui

echo.
echo Playwright UI opened successfully!
echo You can now see all test files in the UI and run them individually.
echo.
pause
