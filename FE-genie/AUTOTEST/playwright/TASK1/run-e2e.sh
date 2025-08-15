#!/usr/bin/env bash
set -euo pipefail

# ===== Config: Hardcoded credentials & facility =====
export PLAYWRIGHT_TEST_USERNAME="phucnnd"
export PLAYWRIGHT_TEST_PASSWORD="Hehehe@12"
export PLAYWRIGHT_TEST_FACILITY="VNVC"

# ===== Paths =====
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
AUTH_TEST="$SCRIPT_DIR/login.direct.spec.ts"
PRINT_TEST="$SCRIPT_DIR/printBarcode.spec.ts"
GENIE_DIR="/c/PROJECTS/genie"
GENIE_CONFIG="playwright.config.ts"

# ===== Validate paths =====
if [ ! -f "$GENIE_DIR/$GENIE_CONFIG" ]; then
  echo "[ERROR] Genie project not found at $GENIE_DIR"
  exit 1
fi
if [ ! -f "$AUTH_TEST" ]; then
  echo "[ERROR] Auth test not found: $AUTH_TEST"
  exit 1
fi
if [ ! -f "$PRINT_TEST" ]; then
  echo "[ERROR] Print test not found: $PRINT_TEST"
  exit 1
fi

# ===== Install browsers if needed =====
pushd "$GENIE_DIR" >/dev/null
echo "[INFO] Installing Playwright browsers if missing..."
npx playwright install

# ===== Run direct login first =====
echo
echo "[RUN] Direct Login (headed)..."
if [ "${1-}" = "--ui" ]; then
  npx playwright test "$AUTH_TEST" --config="$GENIE_CONFIG" --project=chromium --headed --ui
else
  npx playwright test "$AUTH_TEST" --config="$GENIE_CONFIG" --project=chromium --headed
fi

# ===== Run print barcode scenario =====
echo
echo "[RUN] Print Barcode scenario (headed)..."
if [ "${1-}" = "--ui" ]; then
  npx playwright test "$PRINT_TEST" --config="$GENIE_CONFIG" --project=chromium --headed --ui
else
  npx playwright test "$PRINT_TEST" --config="$GENIE_CONFIG" --project=chromium --headed
fi

popd >/dev/null

echo
echo "[OK] E2E finished successfully."
