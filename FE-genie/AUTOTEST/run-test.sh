#!/bin/bash

echo "========================================"
echo "Auto Test - In ma vach (Print Barcode)"
echo "========================================"
echo

# Check if genie directory exists
if [ ! -f "/c/PROJECTS/genie/playwright.config.ts" ]; then
    echo "Error: Genie directory not found at /c/PROJECTS/genie/"
    echo "Current directory: $(pwd)"
    echo "Expected to find: /c/PROJECTS/genie/playwright.config.ts"
    exit 1
fi

echo "Current directory: $(pwd)"
echo "Moving to genie directory..."
cd /c/PROJECTS/genie

echo
echo "Running Playwright test for print barcode scenario..."
echo

# Run the test with different options based on arguments
case "$1" in
    "--ui")
        echo "Running with UI mode..."
        npx playwright test /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --ui
        ;;
    "--debug")
        echo "Running with debug mode..."
        npx playwright test /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --debug
        ;;
    "--report")
        echo "Running with HTML report..."
        npx playwright test /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --reporter=html
        ;;
    "--video")
        echo "Running with video recording..."
        npx playwright test /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --video=on
        ;;
    *)
        echo "Running test normally..."
        npx playwright test /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts
        ;;
esac

echo
echo "Test completed!"
echo
echo "Usage options:"
echo "  ./run-test.sh          - Run test normally"
echo "  ./run-test.sh --ui     - Run with UI mode"
echo "  ./run-test.sh --debug  - Run with debug mode"
echo "  ./run-test.sh --report - Run with HTML report"
echo "  ./run-test.sh --video  - Run with video recording"
echo
