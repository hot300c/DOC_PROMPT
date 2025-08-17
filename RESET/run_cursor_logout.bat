@echo off
chcp 65001 >nul
title Cursor AI Logout Tool

echo.
echo ========================================
echo    CURSOR AI LOGOUT TOOL - WINDOWS
echo ========================================
echo.

REM Kiểm tra Python có được cài đặt không
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python không được cài đặt hoặc không có trong PATH
    echo.
    echo Vui lòng cài đặt Python từ: https://www.python.org/downloads/
    echo Đảm bảo tích chọn "Add Python to PATH" khi cài đặt
    echo.
    pause
    exit /b 1
)

REM Kiểm tra file Python script có tồn tại không
if not exist "%~dp0cursor_logout.py" (
    echo ❌ Không tìm thấy file cursor_logout.py
    echo.
    echo Vui lòng đảm bảo file cursor_logout.py nằm cùng thư mục với script này
    echo.
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt
echo ✅ File cursor_logout.py đã được tìm thấy
echo.
echo 🚀 Đang khởi chạy Cursor AI Logout Tool...
echo.

REM Chạy Python script
python "%~dp0cursor_logout.py"

echo.
echo ========================================
echo           HOÀN THÀNH
echo ========================================
echo.
pause
