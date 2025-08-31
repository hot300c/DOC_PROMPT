# TASK12 Playwright Tests

## Cấu trúc Test

### 1. `task12_login.spec.ts` - Test Đăng nhập
- Đăng nhập vào hệ thống
- Chọn cơ sở "VNVC Hoàng Văn Thụ - SRV TEST"
- Lưu trạng thái đăng nhập vào file `auth.json`

### 2. `task12_test_playwright.spec.ts` - Test Chính
- Sử dụng trạng thái đăng nhập đã lưu
- Thực hiện các bước test chính:
  - Tiếp nhận bệnh nhân mới
  - Nhập thông tin bệnh nhân
  - Chỉ định vaccine
  - Quản lý phác đồ vaccine

## Cách Chạy Test

### Chạy toàn bộ test theo thứ tự:
```bash
npx playwright test --config=playwright.config.ts
```

### Chạy riêng từng test:
```bash
# Chạy test đăng nhập trước
npx playwright test task12_login.spec.ts

# Sau đó chạy test chính
npx playwright test task12_test_playwright.spec.ts
```

### Chạy với UI:
```bash
npx playwright test --ui --config=playwright.config.ts
```

## Lưu ý

- Test login phải chạy trước để tạo file `auth.json`
- File `auth.json` chứa trạng thái đăng nhập và sẽ được sử dụng bởi test chính
- Cấu hình trong `playwright.config.ts` đảm bảo thứ tự chạy đúng
- Test chính sẽ tự động sử dụng trạng thái đăng nhập đã lưu

## Troubleshooting

Nếu gặp lỗi về trạng thái đăng nhập:
1. Xóa file `auth.json` nếu có
2. Chạy lại test login trước
3. Sau đó chạy test chính
