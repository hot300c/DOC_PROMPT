# Cursor AI Logout Tool - PowerShell Script
# Chạy với quyền Administrator nếu cần thiết

param(
    [switch]$NoCheck
)

# Hàm in thông báo với màu
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" "Green"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" "Red"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" "Yellow"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ️  $Message" "Cyan"
}

# Hiển thị header
Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "    CURSOR AI LOGOUT TOOL - WINDOWS" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

# Lấy đường dẫn thư mục chứa script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Kiểm tra Python có được cài đặt không
if (-not $NoCheck) {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python đã được cài đặt: $pythonVersion"
        } else {
            throw "Python không hoạt động"
        }
    } catch {
        Write-Error "Python không được cài đặt hoặc không có trong PATH"
        Write-Host ""
        Write-Host "Vui lòng cài đặt Python từ: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "Đảm bảo tích chọn 'Add Python to PATH' khi cài đặt" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Nhấn Enter để thoát"
        exit 1
    }

    # Kiểm tra file Python script có tồn tại không
    if (-not (Test-Path "$ScriptDir\cursor_logout.py")) {
        Write-Error "Không tìm thấy file cursor_logout.py"
        Write-Host ""
        Write-Host "Vui lòng đảm bảo file cursor_logout.py nằm cùng thư mục với script này" -ForegroundColor Yellow
        Write-Host "Đường dẫn hiện tại: $ScriptDir" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Nhấn Enter để thoát"
        exit 1
    }

    Write-Success "File cursor_logout.py đã được tìm thấy"
    Write-Host ""
}

Write-Info "🚀 Đang khởi chạy Cursor AI Logout Tool..."
Write-Host ""

# Chạy Python script
try {
    python "$ScriptDir\cursor_logout.py"
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Script đã chạy thành công!"
    } else {
        Write-Warning "Script đã chạy nhưng có thể có lỗi (Exit code: $LASTEXITCODE)"
    }
} catch {
    Write-Error "Không thể chạy Python script: $_"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Magenta
Write-Host "           HOÀN THÀNH" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta
Write-Host ""

Read-Host "Nhấn Enter để thoát"
