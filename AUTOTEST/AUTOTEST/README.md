# Auto Test - In mã vạch (Print Barcode)

## Mô tả
Test tự động cho Scenario 1: In mã vạch bệnh nhân trong trang "Tiếp nhận mới" của hệ thống Genie.

## Kịch bản test
**Scenario 1**: In mã vạch gọi `ws_MDM_Patient_CheckExists` và xử lý thành công

### Các bước thực hiện:
1. **Login** vào hệ thống Genie
2. **Mở menu** "Tiếp nhận" → "Tiếp nhận mới"
3. **Tìm kiếm** bệnh nhân bằng tên
4. **Chọn bệnh nhân** từ danh sách kết quả
5. **Bấm nút "In mã vạch"** → API `ws_MDM_Patient_CheckExists` được gọi để validate
6. **Kết quả**: 
   - Nếu bệnh nhân tồn tại → In mã vạch thành công
   - Nếu không tồn tại → Hiển thị thông báo lỗi

## Cách chạy test

### 1. Chuẩn bị môi trường
```bash
# Di chuyển vào thư mục genie
cd genie

# Cài đặt dependencies
yarn install

# Build project
yarn build
```

### 2. Chạy test cụ thể

#### Cách 1: Sử dụng npm scripts (Khuyến nghị)
```bash
# Chạy test printBarcode.spec.ts
npm test

# Chạy với UI mode (để xem test chạy)
npm run test:ui

# Chạy với debug mode
npm run test:debug

# Chạy với HTML report
npm run test:report

# Chạy với video recording
npm run test:video

# Chạy với headed browser
npm run test:headed
```

#### Cách 2: Sử dụng Playwright trực tiếp
```bash
# Chạy test printBarcode.spec.ts
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts

# Chạy với UI mode (để xem test chạy)
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --ui

# Chạy với debug mode
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --debug
```

#### Cách 3: Sử dụng script helper
```bash
# Windows
run-test.bat
run-test.bat --ui
run-test.bat --debug

# Linux/Mac
./run-test.sh
./run-test.sh --ui
./run-test.sh --debug
```

### 3. Chạy test với các options khác
```bash
# Chạy test và tạo report HTML
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --reporter=html

# Chạy test với video recording
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --video=on

# Chạy test với screenshot khi fail
npx playwright test ../../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts --screenshot=only-on-failure
```

### 4. Chạy test từ thư mục hiện tại
```bash
# Nếu đang ở thư mục DOCS_PROMPT/FE-genie/AUTOTEST/
cd ../../genie
npx playwright test ../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts
```

## Cấu hình test

### Authentication
Test sử dụng authentication state được lưu sẵn trong `genie/playwright/.auth/admin.json`

### Test Data
Test sử dụng test data từ fixtures:
- `searchPatientName`: Tên bệnh nhân để tìm kiếm (mặc định: "NGUYỄN VĂN A")

### Environment Variables
Cần có file `.env.playwright` trong thư mục `genie/` với các biến:
```env
PLAYWRIGHT_BASE_URL=http://localhost:3000
```

## Cấu trúc test

### Network Interception
Test intercepts request POST đến `/DataAccess` và kiểm tra:
- Command: `ws_MDM_Patient_CheckExists`
- Parameters: `PatientID` và `FacID`

### Assertions
1. **Request Validation**: Kiểm tra API call có đúng command và parameters
2. **UI Validation**: Kiểm tra loading indicator xuất hiện và biến mất
3. **Patient Selection**: Kiểm tra bệnh nhân được chọn thành công

## Troubleshooting

### Lỗi thường gặp

#### 1. Import errors
```bash
# Lỗi: Cannot find module '@playwright/test'
# Giải pháp: Chạy từ thư mục genie
cd genie
npx playwright test ../DOCS_PROMPT/FE-genie/AUTOTEST/playwright/printBarcode.spec.ts
```

#### 2. Authentication errors
```bash
# Lỗi: Test fails at login
# Giải pháp: Chạy setup authentication trước
npx playwright test genie/playwright/tests/authentication.setup.ts
```

#### 3. Patient not found
```bash
# Lỗi: Không tìm thấy bệnh nhân để test
# Giải pháp: Tạo bệnh nhân test trước hoặc thay đổi searchPatientName trong fixtures
```

#### 4. Network timeout
```bash
# Lỗi: Timeout waiting for DataAccess request
# Giải pháp: Tăng timeout hoặc kiểm tra server đang chạy
npx playwright test --timeout=120000
```

### Debug tips
1. Sử dụng `--debug` flag để chạy test step-by-step
2. Sử dụng `--ui` flag để xem test chạy trực quan
3. Kiểm tra screenshots và videos trong `genie/test-results/`
4. Xem logs chi tiết với `--reporter=line`

## Mở rộng test

### Thêm scenarios khác
1. **Scenario 2**: Test với bệnh nhân không tồn tại
2. **Scenario 3**: Test với keyboard shortcut F3
3. **Scenario 4**: Test với checkbox "In mã vạch" tự động

### Thêm assertions
1. Kiểm tra response từ API
2. Kiểm tra toast messages
3. Kiểm tra print dialog
4. Kiểm tra error handling

## Liên quan
- **API**: `ws_MDM_Patient_CheckExists`
- **Page**: `app/(main)/tiep-nhan/tiep-nhan-moi/page.tsx`
- **Function**: `handlePrintBarcode`
- **Button**: "In mã vạch"
- **Shortcut**: F3
