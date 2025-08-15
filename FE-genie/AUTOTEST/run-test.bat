@echo off
echo ========================================
echo Auto Test - In ma vach (Print Barcode)
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "..\..\..\genie\playwright.config.ts" (
    echo Error: Please run this script from DOCS_PROMPT/FE-genie/AUTOTEST/
    echo Current directory: %CD%
    echo Expected to find: ..\..\..\genie\playwright.config.ts
    pause
    exit /b 1
)

echo Current directory: %CD%
echo Moving to genie directory...
cd ..\..\..\genie

echo.
echo Running Playwright test for print barcode scenario...
echo.

REM Run the test with different options based on arguments
if "%1"=="--ui" (
    echo Running with UI mode...
    npx playwright test ..\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts --ui
) else if "%1"=="--debug" (
    echo Running with debug mode...
    npx playwright test ..\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts --debug
) else if "%1"=="--report" (
    echo Running with HTML report...
    npx playwright test ..\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts --reporter=html
) else if "%1"=="--video" (
    echo Running with video recording...
    npx playwright test ..\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts --video=on
) else (
    echo Running test normally...
    npx playwright test ..\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts
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
