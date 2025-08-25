# Playwright E2E - Auth trước rồi Print từ AUTOTEST

## Tổng quan
- Chạy trực tiếp các file trong thư mục AUTOTEST, KHÔNG copy vào repo `genie/playwright/tests`.
- Dùng cấu hình `C:\PROJECTS\genie\playwright.config.ts` của dự án để kế thừa baseURL, webServer, storage state, reporters...
- Mặc định mở trình duyệt (headed); thêm `--ui` để mở Playwright UI.

## Credentials (hardcoded)
- Username: `phucnnd`
- Password: `Hehehe@12`
- Facility: `VNVC`

## Script
- `run-e2e.bat` (Windows)
- `run-e2e.sh` (Linux/Mac/Git Bash)

## Cách chạy

### Windows (PowerShell/CMD)
```bat
cd C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright
run-e2e.bat           :: Auth -> Print (headed)
run-e2e.bat --ui      :: Auth -> Print (headed + Playwright UI)
```


cd C:\PROJECTS\genie
set PLAYWRIGHT_TEST_USERNAME=phucnnd
set PLAYWRIGHT_TEST_PASSWORD=Hehehe@12
set PLAYWRIGHT_TEST_FACILITY=VNVC
npx playwright install
npx playwright test "C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\login.direct.spec.ts" --config=playwright.config.ts --project=chromium --headed --trace=on --ui


npx playwright test C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\login.direct.spec.ts --config=C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\playwright.autotest.config.ts --project=chromium --headed --ui



### Linux/Mac/Git Bash
```bash
cd /c/PROJECTS/DOCS_PROMPT/FE-genie/AUTOTEST/playwright
chmod +x run-e2e.sh
./run-e2e.sh          # Auth -> Print (headed)
./run-e2e.sh --ui     # Auth -> Print (headed + Playwright UI)
```

## Những gì script làm
1. Thiết lập biến môi trường đăng nhập (hardcoded)
2. Chạy `npx playwright install` (nếu thiếu browsers)
3. Chạy `authentication.setup.ts` (headed, optional `--ui`)
4. Chạy `printBarcode.spec.ts` (headed, optional `--ui`)

## Yêu cầu
- Dự án FE Genie ở: `C:\PROJECTS\genie`
- Có `playwright.config.ts` và có thể chạy `yarn dev`/web server theo config
- Server tại `http://localhost:3000` sẵn sàng trước khi test

## Chạy thủ công từng bước (nếu cần)
Từ thư mục `C:\PROJECTS\genie`:
```bat
set PLAYWRIGHT_TEST_USERNAME=phucnnd
set PLAYWRIGHT_TEST_PASSWORD=Hehehe@12
set PLAYWRIGHT_TEST_FACILITY=VNVC
npx playwright install
npx playwright test "C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\authentication.setup.ts" --config=playwright.config.ts --project=chromium --headed --ui
npx playwright test "C:\PROJECTS\DOCS_PROMPT\FE-genie\AUTOTEST\playwright\printBarcode.spec.ts" --config=playwright.config.ts --project=chromium --headed --ui
```

## Kết quả mong đợi
- Auth: đăng nhập thành công, lưu storage state
- Print: mở "Tiếp nhận mới", tìm KH và click "In mã vạch"; kiểm tra request `/DataAccess` có `ws_MDM_Patient_CheckExists`.
