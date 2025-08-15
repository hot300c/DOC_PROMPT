@echo off
echo ========================================
echo Auto Test - In ma vach (Print Barcode)
echo ========================================
echo.

REM Check if genie directory exists
if not exist "C:\PROJECTS\genie\playwright.config.ts" (
    echo Error: Genie directory not found at C:\PROJECTS\genie\
    echo Current directory: %CD%
    echo Expected to find: C:\PROJECTS\genie\playwright.config.ts
    pause
    exit /b 1
)

echo Current directory: %CD%
echo Moving to genie directory...
cd C:\PROJECTS\genie

echo.
echo Running Playwright test for print barcode scenario...
echo.

REM Run the test with different options based on arguments
if "%1"=="--ui" (
    echo Running with UI mode...
    npx playwright test playwright\tests\printBarcode.spec.ts --ui
) else if "%1"=="--debug" (
    echo Running with debug mode...
    npx playwright test playwright\tests\printBarcode.spec.ts --debug
) else if "%1"=="--report" (
    echo Running with HTML report...
    npx playwright test playwright\tests\printBarcode.spec.ts --reporter=html
) else if "%1"=="--video" (
    echo Running with video recording...
    npx playwright test playwright\tests\printBarcode.spec.ts --video=on
) else (
    echo Running test normally...
    npx playwright test playwright\tests\printBarcode.spec.ts
)

echo.
echo Test completed!
echo.
echo Usage options:
echo   run-test.bat          - Run test normally
echo   run-test.bat --ui     - Run with UI mode
echo   run-test.bat --debug  - Run with debug mode
echo   run-test.bat --report - Run with HTML report
echo   run-test.bat --video  - Run with video recording
echo.
pause
