#!/usr/bin/env python3
"""
Script để kiểm tra trạng thái đăng nhập hiện tại của Cursor AI
"""

import os
import platform
from pathlib import Path

def get_cursor_cache_path():
    """Lấy đường dẫn cache của Cursor AI dựa trên hệ điều hành"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Cursor"
    elif system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Cursor"
    elif system == "Linux":
        return Path.home() / ".config" / "Cursor"
    else:
        print(f"Hệ điều hành {system} không được hỗ trợ")
        return None

def check_login_files():
    """Kiểm tra các file chứa thông tin đăng nhập"""
    cache_path = get_cursor_cache_path()
    
    if not cache_path:
        return False
    
    if not cache_path.exists():
        print(f"❌ Không tìm thấy thư mục cache: {cache_path}")
        return False
    
    print(f"📁 Thư mục cache: {cache_path}")
    print("="*60)
    
    # Danh sách file quan trọng cần kiểm tra
    important_files = [
        "User Data/Default/Login Data",
        "User Data/Default/Web Data", 
        "User Data/Default/Preferences",
        "User Data/Default/Secure Preferences",
        "User Data/Default/Local State",
        "User Data/Default/Network Persistent State",
        "User Data/Default/History",
        "User Data/Default/Bookmarks",
        "User Data/Default/Cookies",
        "User Data/Default/Visited Links"
    ]
    
    found_files = []
    missing_files = []
    
    for file_name in important_files:
        file_path = cache_path / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            found_files.append((file_name, size))
        else:
            missing_files.append(file_name)
    
    print("📋 TRẠNG THÁI CÁC FILE QUAN TRỌNG:")
    print("-" * 40)
    
    if found_files:
        print("✅ CÁC FILE ĐÃ TÌM THẤY:")
        for file_name, size in found_files:
            size_kb = size / 1024
            print(f"  • {file_name} ({size_kb:.1f} KB)")
    else:
        print("❌ Không tìm thấy file nào!")
    
    if missing_files:
        print("\n❌ CÁC FILE KHÔNG TÌM THẤY:")
        for file_name in missing_files:
            print(f"  • {file_name}")
    
    # Kiểm tra thư mục User Data
    user_data_path = cache_path / "User Data"
    if user_data_path.exists():
        print(f"\n📂 Thư mục User Data: {user_data_path}")
        
        # Kiểm tra thư mục Default
        default_path = user_data_path / "Default"
        if default_path.exists():
            print(f"📂 Thư mục Default: {default_path}")
            
            # Đếm số file trong Default
            try:
                file_count = len(list(default_path.rglob("*")))
                print(f"📊 Tổng số file/thư mục trong Default: {file_count}")
            except Exception as e:
                print(f"⚠️  Không thể đếm file: {e}")
        else:
            print("❌ Không tìm thấy thư mục Default")
    else:
        print("❌ Không tìm thấy thư mục User Data")
    
    return len(found_files) > 0

def check_cursor_processes():
    """Kiểm tra các process Cursor AI đang chạy"""
    import subprocess
    
    system = platform.system()
    
    print("\n🔄 KIỂM TRA PROCESS CURSOR AI:")
    print("-" * 40)
    
    try:
        if system == "Darwin":  # macOS
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            if "Cursor" in result.stdout:
                print("✅ Có process Cursor AI đang chạy:")
                for line in result.stdout.split('\n'):
                    if "Cursor" in line:
                        print(f"  • {line.strip()}")
            else:
                print("❌ Không có process Cursor AI nào đang chạy")
                
        elif system == "Windows":
            result = subprocess.run(["tasklist"], capture_output=True, text=True)
            if "Cursor.exe" in result.stdout:
                print("✅ Có process Cursor AI đang chạy:")
                for line in result.stdout.split('\n'):
                    if "Cursor.exe" in line:
                        print(f"  • {line.strip()}")
            else:
                print("❌ Không có process Cursor AI nào đang chạy")
                
        elif system == "Linux":
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            if "cursor" in result.stdout.lower():
                print("✅ Có process Cursor AI đang chạy:")
                for line in result.stdout.split('\n'):
                    if "cursor" in line.lower():
                        print(f"  • {line.strip()}")
            else:
                print("❌ Không có process Cursor AI nào đang chạy")
                
    except Exception as e:
        print(f"⚠️  Không thể kiểm tra process: {e}")

def main():
    """Hàm chính"""
    print("🔍 CURSOR AI STATUS CHECKER")
    print("="*60)
    
    # Kiểm tra file đăng nhập
    has_login_data = check_login_files()
    
    # Kiểm tra process
    check_cursor_processes()
    
    print("\n" + "="*60)
    print("📊 KẾT LUẬN:")
    
    if has_login_data:
        print("⚠️  CÓ DỮ LIỆU ĐĂNG NHẬP TỒN TẠI!")
        print("   → Cần chạy script logout để xóa dữ liệu")
    else:
        print("✅ KHÔNG CÓ DỮ LIỆU ĐĂNG NHẬP!")
        print("   → Cursor AI đã được logout hoàn toàn")
    
    print("="*60)

if __name__ == "__main__":
    main()
