@echo off
echo ========================================
echo List All Playwright Test Files
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
echo Scanning playwright directory...
echo.

REM List all .spec.ts files recursively
echo Found test files:
echo ----------------------------------------
powershell -Command "Get-ChildItem -Path 'C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright' -Recurse -Filter '*.spec.ts' | ForEach-Object { Write-Host $_.FullName.Replace('C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\', '') }"

echo.
echo ----------------------------------------
echo Total test files found:
powershell -Command "$count = (Get-ChildItem -Path 'C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright' -Recurse -Filter '*.spec.ts').Count; Write-Host $count"

echo.
echo Available test files by category:
echo ----------------------------------------
echo TASK1:
powershell -Command "Get-ChildItem -Path 'C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\TASK1' -Filter '*.spec.ts' | ForEach-Object { Write-Host '  - ' $_.Name }"

echo.
echo tests-examples:
powershell -Command "Get-ChildItem -Path 'C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\tests-examples' -Filter '*.spec.ts' | ForEach-Object { Write-Host '  - ' $_.Name }"

echo.
echo testslogin:
powershell -Command "Get-ChildItem -Path 'C:\PROJECTS\DOCS_PROMPT\AUTOTEST\AUTOTEST\playwright\testslogin' -Filter '*.spec.ts' | ForEach-Object { Write-Host '  - ' $_.Name }"

echo.
echo Usage:
echo   To run a specific test, use: run-test.bat [test-file-name]
echo   Example: run-test.bat TASK1/printBarcode.spec.ts
echo.
pause
