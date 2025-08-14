# 🚀 Cursor AI Logout Tool

Script Python để logout khỏi Cursor AI với 2 tùy chọn khác nhau.

## 📋 Tính năng

- **Tùy chọn 1**: Logout account trong Cursor AI (không xóa cache)
- **Tùy chọn 2**: Logout account và xóa toàn bộ cache
- Hỗ trợ đa nền tảng (Windows, macOS, Linux)
- Giao diện menu thân thiện
- Xử lý lỗi an toàn

## 🛠️ Cách sử dụng

### 1. Chạy script

```bash
python3 cursor_logout.py
```

### 2. Chọn tùy chọn

```
==================================================
🚀 CURSOR AI LOGOUT TOOL
==================================================
Chọn tùy chọn:
1. Logout account trong Cursor AI (không xóa cache)
2. Logout account và xóa cache
3. Thoát
==================================================
```

## 📁 Đường dẫn cache theo hệ điều hành

### macOS
```
~/Library/Application Support/Cursor
```

### Windows
```
%APPDATA%/Cursor
```

### Linux
```
~/.config/Cursor
```

## 🔧 Cách hoạt động

### Tùy chọn 1: Logout (không xóa cache)
- Xóa file thông tin đăng nhập
- Giữ nguyên cache và cài đặt
- Phù hợp khi chỉ muốn đổi tài khoản

### Tùy chọn 2: Logout + Xóa cache
- Xóa file thông tin đăng nhập
- Xóa toàn bộ cache và cài đặt
- Phù hợp khi gặp lỗi hoặc muốn reset hoàn toàn

## ⚠️ Lưu ý quan trọng

1. **Đóng Cursor AI** trước khi chạy script
2. **Sao lưu dữ liệu** quan trọng trước khi xóa cache
3. **Khởi động lại Cursor AI** sau khi hoàn thành
4. Script cần quyền truy cập vào thư mục cache

## 🐛 Xử lý lỗi

Nếu gặp lỗi:
1. Kiểm tra quyền truy cập thư mục
2. Đảm bảo Cursor AI đã được đóng hoàn toàn
3. Chạy script với quyền admin (nếu cần)

## 📝 Yêu cầu hệ thống

- Python 3.6+
- Quyền truy cập file system
- Cursor AI đã được cài đặt

## 🔒 Bảo mật

Script chỉ thao tác với thư mục cache của Cursor AI và không thu thập thông tin cá nhân.
