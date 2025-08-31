@echo off
echo ========================================
echo Auto Test - Playwright Test Runner
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

REM Check if --list option is provided
if "%1"=="--list" (
    echo Available test files:
    echo ----------------------------------------
    powershell -Command "Get-ChildItem -Path '.' -Recurse -Filter '*.spec.ts' | ForEach-Object { Write-Host $_.FullName.Replace('C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\', '') }"
    echo.
    echo Usage examples:
    echo   run-test.bat TASK1/printBarcode.spec.ts
    echo   run-test.bat TASK1/login.direct.spec.ts
    echo   run-test.bat tests-examples/demo-todo-app.spec.ts
    echo   run-test.bat testslogin/example.spec.ts
    echo.
    pause
    exit /b 0
)

REM Check if --ui-open option is provided
if "%1"=="--ui-open" (
    echo Opening Playwright UI with all test files...
    echo This will open a browser window where you can see and run all tests.
    echo.
    npx playwright test --ui
    echo.
    echo Playwright UI opened successfully!
    echo You can now see all test files in the UI and run them individually.
    echo.
    pause
    exit /b 0
)

REM Check if test file is provided
if "%1"=="" (
    echo No test file specified. Available options:
    echo   run-test.bat --list                    - List all available test files
    echo   run-test.bat --ui-open                 - Open Playwright UI with all tests
    echo   run-test.bat [test-file]               - Run specific test file
    echo   run-test.bat [test-file] --ui          - Run with UI mode
    echo   run-test.bat [test-file] --debug       - Run with debug mode
    echo   run-test.bat [test-file] --report      - Run with HTML report
    echo   run-test.bat [test-file] --video       - Run with video recording
    echo.
    echo Example: run-test.bat TASK1/printBarcode.spec.ts
    echo.
    pause
    exit /b 1
)

REM Check if the specified test file exists
if not exist "%1" (
    echo Error: Test file not found: %1
    echo.
    echo Available test files:
    echo ----------------------------------------
    powershell -Command "Get-ChildItem -Path '.' -Recurse -Filter '*.spec.ts' | ForEach-Object { Write-Host $_.FullName.Replace('C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\', '') }"
    echo.
    pause
    exit /b 1
)

echo Running Playwright test: %1
echo.

REM Run the test with different options based on arguments
if "%2"=="--ui" (
    echo Running with UI mode...
    npx playwright test "%1" --ui
) else if "%2"=="--debug" (
    echo Running with debug mode...
    npx playwright test "%1" --debug
) else if "%2"=="--report" (
    echo Running with HTML report...
    npx playwright test "%1" --reporter=html
) else if "%2"=="--video" (
    echo Running with video recording...
    npx playwright test "%1" --video=on
) else (
    echo Running test normally...
    npx playwright test "%1" --ui
)

echo.
echo Test completed!
echo.
echo Usage options:
echo   run-test.bat --list                        - List all available test files
echo   run-test.bat --ui-open                     - Open Playwright UI with all tests
echo   run-test.bat [test-file]                   - Run specific test file
echo   run-test.bat [test-file] --ui              - Run with UI mode
echo   run-test.bat [test-file] --debug           - Run with debug mode
echo   run-test.bat [test-file] --report          - Run with HTML report
echo   run-test.bat [test-file] --video           - Run with video recording
echo.
pause
