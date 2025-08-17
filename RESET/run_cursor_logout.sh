#!/bin/bash

# Cursor AI Logout Tool - macOS/Linux Script
# Đảm bảo script có quyền thực thi: chmod +x run_cursor_logout.sh

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Hàm in thông báo với màu
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo
    echo "========================================"
    echo "    CURSOR AI LOGOUT TOOL - $(uname -s)"
    echo "========================================"
    echo
}

# Lấy đường dẫn thư mục chứa script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_header

# Kiểm tra Python có được cài đặt không
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python không được cài đặt hoặc không có trong PATH"
        echo
        echo "Vui lòng cài đặt Python:"
        echo "  • macOS: brew install python3"
        echo "  • Ubuntu/Debian: sudo apt install python3"
        echo "  • CentOS/RHEL: sudo yum install python3"
        echo
        read -p "Nhấn Enter để thoát..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_success "Python đã được cài đặt: $($PYTHON_CMD --version)"

# Kiểm tra file Python script có tồn tại không
if [ ! -f "$SCRIPT_DIR/cursor_logout.py" ]; then
    print_error "Không tìm thấy file cursor_logout.py"
    echo
    echo "Vui lòng đảm bảo file cursor_logout.py nằm cùng thư mục với script này"
    echo "Đường dẫn hiện tại: $SCRIPT_DIR"
    echo
    read -p "Nhấn Enter để thoát..."
    exit 1
fi

print_success "File cursor_logout.py đã được tìm thấy"
echo
print_info "🚀 Đang khởi chạy Cursor AI Logout Tool..."
echo

# Chạy Python script
$PYTHON_CMD "$SCRIPT_DIR/cursor_logout.py"

echo
echo "========================================"
echo "           HOÀN THÀNH"
echo "========================================"
echo
read -p "Nhấn Enter để thoát..."
