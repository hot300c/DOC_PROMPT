#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor AI Logout Tool - Enhanced macOS Version
Script tối ưu hóa đặc biệt cho macOS để logout khỏi Cursor AI
"""

import os
import sys
import shutil
import subprocess
import platform
import time
from pathlib import Path


def print_colored(text: str, color: str = "white") -> None:
    """Print colored text to console với hỗ trợ macOS terminal."""
    colors = {
        "cyan": "\033[96m", "yellow": "\033[93m", "green": "\033[92m",
        "red": "\033[91m", "white": "\033[97m", "gray": "\033[90m",
        "blue": "\033[94m", "magenta": "\033[95m"
    }
    reset = "\033[0m"
    color_code = colors.get(color, colors["white"])
    print(f"{color_code}{text}{reset}")


def check_macos() -> bool:
    """Kiểm tra xem có đang chạy trên macOS không."""
    if platform.system() != "Darwin":
        print_colored("❌ Script này chỉ dành cho macOS!", "red")
        return False
    return True


def get_cursor_processes():
    """Lấy tất cả process Cursor trên macOS."""
    try:
        result = subprocess.run(["ps", "-axo", "pid,comm,args"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        processes = []
        for line in result.stdout.strip().split('\n')[1:]:
            if line.strip():
                parts = line.split(None, 2)
                if len(parts) >= 3:
                    pid, comm, args = parts[0], parts[1], parts[2]
                    if "Cursor" in comm or "Cursor" in args:
                        processes.append((pid, f"{comm} {args}"))
        return processes
    except Exception as e:
        print_colored(f"❌ Lỗi khi lấy danh sách process: {e}", "red")
        return []


def force_kill_cursor() -> bool:
    """Force kill tất cả process Cursor AI trên macOS."""
    if not check_macos():
        return False
    
    try:
        print_colored("🔄 Đang đóng Cursor AI...", "yellow")
        processes = get_cursor_processes()
        
        if not processes:
            print_colored("✅ Không có process Cursor nào đang chạy.", "green")
            return True
        
        print_colored(f"📋 Tìm thấy {len(processes)} process Cursor:", "cyan")
        for pid, process_info in processes:
            print_colored(f"  PID {pid}: {process_info}", "gray")
        
        # Gửi SIGTERM trước
        for pid, process_info in processes:
            try:
                subprocess.run(["kill", pid], check=True)
                print_colored(f"  ✓ Đã gửi SIGTERM đến PID {pid}", "blue")
            except subprocess.CalledProcessError:
                print_colored(f"  ⚠️  Không thể gửi SIGTERM đến PID {pid}", "yellow")
        
        time.sleep(3)
        
        # Force kill nếu cần
        remaining_processes = get_cursor_processes()
        if remaining_processes:
            print_colored("🔄 Một số process vẫn còn chạy, đang force kill...", "yellow")
            for pid, process_info in remaining_processes:
                try:
                    subprocess.run(["kill", "-9", pid], check=True)
                    print_colored(f"  ✓ Đã force kill PID {pid}", "red")
                except subprocess.CalledProcessError:
                    print_colored(f"  ⚠️  Không thể force kill PID {pid}", "yellow")
        
        time.sleep(2)
        final_check = get_cursor_processes()
        if not final_check:
            print_colored("✅ Tất cả process Cursor AI đã được đóng thành công!", "green")
            return True
        else:
            print_colored(f"⚠️  Cảnh báo: {len(final_check)} process vẫn còn chạy", "yellow")
            return True
            
    except Exception as e:
        print_colored(f"❌ Lỗi khi đóng Cursor AI: {e}", "red")
        return False


def get_cursor_cache_path():
    """Lấy đường dẫn cache của Cursor AI trên macOS."""
    if not check_macos():
        return None
    return Path.home() / "Library" / "Application Support" / "Cursor"


def get_cursor_user_path():
    """Lấy đường dẫn User data của Cursor AI trên macOS."""
    if not check_macos():
        return None
    return Path.home() / "Library" / "Application Support" / "Cursor" / "User"


def clear_cursor_cache() -> bool:
    """Xóa cache của Cursor AI trên macOS."""
    cache_path = get_cursor_cache_path()
    if not cache_path or not cache_path.exists():
        print_colored("⚠️  Không tìm thấy thư mục cache", "yellow")
        return False
    
    try:
        print_colored("🔄 Đang xóa cache Cursor AI...", "yellow")
        
        cache_dirs = ["Cache", "Code Cache", "GPUCache", "Service Worker", 
                     "Session Storage", "Local Storage", "IndexedDB", "Databases"]
        cache_files = ["Cookies", "Cookies-journal", "Preferences", 
                      "Secure Preferences", "Local State", "Network Persistent State"]
        
        deleted_count = 0
        
        for dir_name in cache_dirs:
            dir_path = cache_path / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print_colored(f"  ✓ Đã xóa: {dir_name}", "green")
                    deleted_count += 1
                except Exception as e:
                    print_colored(f"  ⚠️  Không thể xóa {dir_name}: {e}", "yellow")
        
        for file_name in cache_files:
            file_path = cache_path / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    print_colored(f"  ✓ Đã xóa: {file_name}", "green")
                    deleted_count += 1
                except Exception as e:
                    print_colored(f"  ⚠️  Không thể xóa {file_name}: {e}", "yellow")
        
        if deleted_count > 0:
            print_colored(f"✅ Đã xóa {deleted_count} file/thư mục cache thành công!", "green")
        else:
            print_colored("⚠️  Không tìm thấy file cache để xóa.", "yellow")
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Lỗi khi xóa cache: {e}", "red")
        return False


def logout_cursor() -> bool:
    """Logout khỏi Cursor AI trên macOS."""
    cache_path = get_cursor_cache_path()
    if not cache_path:
        return False
    
    try:
        print_colored("🔄 Đang logout khỏi Cursor AI...", "yellow")
        
        login_files = [
            "User Data/Default/Login Data", "User Data/Default/Web Data",
            "User Data/Default/Network Persistent State", "User Data/Default/History",
            "User Data/Default/Cookies", "User Data/Default/Bookmarks",
            "User Data/Default/Last Session", "User Data/Default/Current Session"
        ]
        
        login_dirs = [
            "User Data/Default/Session Storage", "User Data/Default/Local Storage",
            "User Data/Default/IndexedDB", "User Data/Default/Databases"
        ]
        
        deleted_count = 0
        
        for file_name in login_files:
            file_path = cache_path / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    print_colored(f"  ✓ Đã xóa: {file_name}", "green")
                    deleted_count += 1
                except Exception as e:
                    print_colored(f"  ⚠️  Không thể xóa {file_name}: {e}", "yellow")
        
        for dir_name in login_dirs:
            dir_path = cache_path / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print_colored(f"  ✓ Đã xóa thư mục: {dir_name}", "green")
                    deleted_count += 1
                except Exception as e:
                    print_colored(f"  ⚠️  Không thể xóa thư mục {dir_name}: {e}", "yellow")
        
        if deleted_count > 0:
            print_colored(f"✅ Đã logout thành công! Đã xóa {deleted_count} file/thư mục.", "green")
        else:
            print_colored("⚠️  Không tìm thấy file thông tin đăng nhập để xóa.", "yellow")
        
        return True
        
    except Exception as e:
        print_colored(f"❌ Lỗi khi logout: {e}", "red")
        return False


def reset_machine_id() -> bool:
    """Reset Machine ID của Cursor AI sử dụng cursor-free-vip trên macOS."""
    if not check_macos():
        return False
    
    try:
        print_colored("🔄 Đang reset Machine ID sử dụng cursor-free-vip...", "yellow")
        
        curl_cmd = "curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh"
        
        print_colored("🚀 Mở Terminal và chạy lệnh:", "cyan")
        print_colored(f"   {curl_cmd}", "white")
        print_colored("\n⚠️  Lưu ý: Script sẽ tự động reset Machine ID và tạo tài khoản mới.", "yellow")
        
        # Mở Terminal
        subprocess.run(["open", "-a", "Terminal"], check=True)
        time.sleep(2)
        
        # Chạy lệnh trong Terminal
        osascript_cmd = f'osascript -e \'tell application "Terminal" to do script "{curl_cmd}"\''
        result = subprocess.run(osascript_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print_colored("✅ Đã mở Terminal và chạy script cursor-free-vip!", "green")
        else:
            print_colored("⚠️  Có thể có lỗi khi chạy script", "yellow")
            print_colored("💡 Copy và paste lệnh này vào Terminal:", "cyan")
            print_colored(f"   {curl_cmd}", "white")
        
        return True
            
    except Exception as e:
        print_colored(f"❌ Lỗi khi chạy script cursor-free-vip: {e}", "red")
        return False


def open_default_browser() -> bool:
    """Mở trình duyệt mặc định trên macOS."""
    if not check_macos():
        return False
    
    cursor_dashboard_url = "https://cursor.com/dashboard?tab=settings"
    
    try:
        print_colored("🌐 Đang mở trình duyệt mặc định...", "blue")
        subprocess.run(["open", cursor_dashboard_url], check=True)
        print_colored("✅ Đã mở trình duyệt để truy cập Cursor Dashboard Settings", "green")
        return True
            
    except Exception as e:
        print_colored(f"❌ Lỗi khi mở trình duyệt: {e}", "red")
        print_colored(f"💡 Vui lòng mở trình duyệt và truy cập: {cursor_dashboard_url}", "cyan")
        return False


def show_menu():
    """Hiển thị menu tùy chọn cho macOS."""
    print("\n" + "="*60)
    print_colored("🚀 CURSOR AI LOGOUT TOOL - macOS Enhanced", "cyan")
    print_colored("="*60, "cyan")
    print_colored("Chọn tùy chọn:", "white")
    print_colored("1. 🔄 Reset Machine ID (cursor-free-vip)", "yellow")
    print_colored("2. 📤 Logout account và xóa cache", "blue")
    print_colored("3. 💀 Force kill Cursor AI", "red")
    print_colored("4. 🔥 RESET HOÀN TOÀN", "magenta")
    print_colored("5. 🌐 Mở trình duyệt Dashboard Settings", "cyan")
    print_colored("6. 🚪 Thoát", "white")
    print_colored("="*60, "cyan")


def main():
    """Hàm chính cho macOS Cursor logout tool."""
    if not check_macos():
        return
    
    print_colored("=== CURSOR AI LOGOUT TOOL - macOS Enhanced ===", "cyan")
    print_colored("Script tối ưu hóa đặc biệt cho macOS", "white")
    print()
    
    while True:
        show_menu()
        
        try:
            choice = input("\nNhập lựa chọn của bạn (1-6): ").strip()
            
            if choice == "1":
                print("\n🔄 Đang reset Machine ID...")
                reset_machine_id()
                    
            elif choice == "2":
                print("\n🔄 Đang logout và xóa cache...")
                logout_cursor()
                clear_cursor_cache()
                print_colored("✅ Hoàn thành! Vui lòng khởi động lại Cursor AI.", "green")
                    
            elif choice == "3":
                print("\n🔄 Đang force kill Cursor AI...")
                force_kill_cursor()
                    
            elif choice == "4":
                print("\n🔄 Bắt đầu reset hoàn toàn...")
                force_kill_cursor()
                reset_machine_id()
                open_default_browser()
                print_colored("🎉 RESET HOÀN TOÀN THÀNH CÔNG!", "green")
                    
            elif choice == "5":
                print("\n🌐 Đang mở trình duyệt...")
                open_default_browser()
                    
            elif choice == "6":
                print_colored("\n👋 Tạm biệt!", "cyan")
                break
                
            else:
                print_colored("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1-6.", "red")
                
        except KeyboardInterrupt:
            print_colored("\n\n👋 Đã hủy thao tác. Tạm biệt!", "yellow")
            break
        except Exception as e:
            print_colored(f"\n❌ Có lỗi xảy ra: {e}", "red")
        
        if choice in ["1", "2", "3", "4", "5"]:
            input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    main()
