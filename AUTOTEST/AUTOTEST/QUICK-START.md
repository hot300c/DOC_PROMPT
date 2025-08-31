# Quick Start - Print Barcode Test

## 🚀 Chạy test nhanh

### Bước 1: Chuẩn bị
```bash
cd genie
yarn install
yarn build
```

### Bước 2: Chạy test
```bash
# Từ thư mục DOCS_PROMPT/FE-genie/AUTOTEST/
npm test
```

## 📋 Các lệnh hữu ích

| Lệnh | Mô tả |
|------|-------|
| `npm test` | Chạy test bình thường |
| `npm run test:ui` | Chạy với UI mode (xem trực quan) |
| `npm run test:debug` | Chạy với debug mode |
| `npm run test:report` | Tạo HTML report |
| `npm run test:video` | Ghi video |
| `npm run auth` | Setup authentication |

## 🔧 Troubleshooting

### Lỗi thường gặp:
1. **Import error**: Chạy từ thư mục `genie`
2. **Auth error**: Chạy `npm run auth` trước
3. **Patient not found**: Kiểm tra test data trong fixtures

### Debug:
```bash
npm run test:debug  # Step-by-step
npm run test:ui     # Visual mode
```

## 📁 Cấu trúc file
```
DOCS_PROMPT/FE-genie/AUTOTEST/
├── README.md           # Hướng dẫn chi tiết
├── QUICK-START.md      # Hướng dẫn nhanh (này)
├── package.json        # NPM scripts
├── run-test.bat        # Script Windows
├── run-test.sh         # Script Linux/Mac
└── playwright/
    └── printBarcode.spec.ts  # Test file
```

## 🎯 Test Scenario
- **Mục tiêu**: Test API `ws_MDM_Patient_CheckExists` khi in mã vạch
- **Kịch bản**: Login → Tìm bệnh nhân → Click "In mã vạch" → Validate API call
- **Assertions**: Request parameters, loading states, UI feedback
