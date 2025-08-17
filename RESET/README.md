# Cursor AI Logout Tool

Tool để logout khỏi Cursor AI với nhiều tùy chọn khác nhau, hoạt động trên Windows, macOS và Linux.

## 📁 Các file trong thư mục

- `cursor_logout.py` - Script Python chính
- `run_cursor_logout.bat` - Script Windows (Batch)
- `run_cursor_logout.ps1` - Script Windows (PowerShell)
- `run_cursor_logout.sh` - Script macOS/Linux (Bash)

## 🚀 Cách sử dụng

### Windows

#### Phương pháp 1: Sử dụng Batch Script (Đơn giản nhất)
1. Double-click vào file `run_cursor_logout.bat`
2. Script sẽ tự động kiểm tra Python và chạy tool

#### Phương pháp 2: Sử dụng PowerShell Script (Khuyến nghị)
1. Chuột phải vào file `run_cursor_logout.ps1`
2. Chọn "Run with PowerShell"
3. Hoặc mở PowerShell và chạy:
   ```powershell
   .\run_cursor_logout.ps1
   ```

#### Phương pháp 3: Chạy trực tiếp Python
```cmd
python cursor_logout.py
```

### macOS

#### Phương pháp 1: Sử dụng Shell Script (Khuyến nghị)
1. Mở Terminal
2. Di chuyển đến thư mục chứa script:
   ```bash
   cd /path/to/DOC_PROMPT_VNVC/RESET
   ```
3. Cấp quyền thực thi cho script:
   ```bash
   chmod +x run_cursor_logout.sh
   ```
4. Chạy script:
   ```bash
   ./run_cursor_logout.sh
   ```

#### Phương pháp 2: Chạy trực tiếp Python
```bash
python3 cursor_logout.py
```

### Linux

Tương tự như macOS, sử dụng shell script:
```bash
chmod +x run_cursor_logout.sh
./run_cursor_logout.sh
```

## ⚠️ Yêu cầu hệ thống

- **Python 3.6+** đã được cài đặt và có trong PATH
- **Windows**: Python từ python.org hoặc Microsoft Store
- **macOS**: Python từ python.org hoặc Homebrew (`brew install python3`)
- **Linux**: Python từ package manager (`sudo apt install python3`)

## 🔧 Các tùy chọn có sẵn

1. **Reset Machine ID** - Sử dụng script từ [cursor-free-vip](https://github.com/yeongpin/cursor-free-vip)
2. **Logout + Xóa cache** - Logout và xóa toàn bộ cache
3. **Force kill Cursor AI** - Đóng tất cả process Cursor AI
4. **Reset hoàn toàn** - Đóng Cursor + Logout + Reset Machine ID
5. **Thoát**

## 🎯 Tùy chọn khuyến nghị

- **Lần đầu sử dụng**: Chọn tùy chọn 4 (Reset hoàn toàn)
- **Chỉ muốn logout**: Chọn tùy chọn 2
- **Gặp vấn đề với Machine ID**: Chọn tùy chọn 1 (sử dụng cursor-free-vip)

## 🔒 Lưu ý bảo mật

- Script sẽ xóa thông tin đăng nhập và cache của Cursor AI
- **KHÔNG** xóa dữ liệu project của bạn
- **KHÔNG** xóa cài đặt Cursor AI
- Chỉ xóa thông tin session và cache

## 🔗 Tích hợp với cursor-free-vip

Tool này tích hợp với [cursor-free-vip](https://github.com/yeongpin/cursor-free-vip) để reset Machine ID:
- **macOS/Linux**: Sử dụng script `install.sh`
- **Windows**: Sử dụng script `install.ps1`
- Tự động tải và chạy script từ repository chính thức
- Hỗ trợ đa ngôn ngữ và đa nền tảng

## 🚨 Xử lý lỗi

### Lỗi "Python không được cài đặt"
- Cài đặt Python từ [python.org](https://www.python.org/downloads/)
- Đảm bảo tích chọn "Add Python to PATH" khi cài đặt

### Lỗi "Permission denied" trên macOS/Linux
```bash
chmod +x run_cursor_logout.sh
```

### Lỗi "Execution Policy" trên Windows PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python đã được cài đặt đúng cách
2. File `cursor_logout.py` nằm cùng thư mục với script
3. Quyền thực thi đã được cấp (macOS/Linux)
4. Execution Policy đã được cho phép (Windows PowerShell)

## 🔄 Cập nhật

Để cập nhật tool:
1. Thay thế file `cursor_logout.py` bằng phiên bản mới
2. Các script wrapper sẽ tự động sử dụng file Python mới
