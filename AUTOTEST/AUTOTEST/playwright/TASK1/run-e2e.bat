@echo off
setlocal enabledelayedexpansion

REM ===== Config: Hardcoded credentials & facility =====
set PLAYWRIGHT_TEST_USERNAME=phucnnd
set PLAYWRIGHT_TEST_PASSWORD=Hehehe@12
set PLAYWRIGHT_TEST_FACILITY=VNVC

REM ===== Paths =====
set AUTOTEST_DIR=%~dp0
set AUTH_TEST=%AUTOTEST_DIR%login.direct.spec.ts
set PRINT_TEST=%AUTOTEST_DIR%printBarcode.spec.ts
set GENIE_DIR=C:\PROJECTS\genie
set GENIE_CONFIG=playwright.config.ts

REM ===== Validate paths =====
if not exist "%GENIE_DIR%\%GENIE_CONFIG%" (
  echo [ERROR] Genie project not found at %GENIE_DIR%
  exit /b 1
)
if not exist "%AUTH_TEST%" (
  echo [ERROR] Auth test not found: %AUTH_TEST%
  exit /b 1
)
if not exist "%PRINT_TEST%" (
  echo [ERROR] Print test not found: %PRINT_TEST%
  exit /b 1
)

REM ===== Install browsers if needed =====
pushd "%GENIE_DIR%"
echo [INFO] Installing Playwright browsers if missing...
npx playwright install

REM ===== Run direct login first (headed + optional UI) =====
echo.
echo [RUN] Direct Login (headed)...
if /I "%1"=="--ui" (
  npx playwright test "%AUTH_TEST%" --config=%GENIE_CONFIG% --project=chromium --headed --ui
) else (
  npx playwright test "%AUTH_TEST%" --config=%GENIE_CONFIG% --project=chromium --headed
)
if errorlevel 1 (
  echo [ERROR] Direct login failed.
  popd
  exit /b 1
)

REM ===== Run print barcode scenario =====
echo.
echo [RUN] Print Barcode scenario (headed)...
if /I "%1"=="--ui" (
  npx playwright test "%PRINT_TEST%" --config=%GENIE_CONFIG% --project=chromium --headed --ui
) else (
  npx playwright test "%PRINT_TEST%" --config=%GENIE_CONFIG% --project=chromium --headed
)
set EXIT_CODE=%ERRORLEVEL%
popd

if %EXIT_CODE% NEQ 0 (
  echo [FAIL] E2E failed with exit code %EXIT_CODE%
  exit /b %EXIT_CODE%
)

echo.

echo [OK] E2E finished successfully.
exit /b 0
