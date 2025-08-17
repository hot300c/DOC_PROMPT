#!/usr/bin/env python3
"""
Script để logout khỏi Cursor AI với 2 tùy chọn:
1. Logout account trong Cursor AI và không xóa cache
2. Logout account và xóa cache
"""

import os
import sys
import shutil
import subprocess
import platform
import json
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

def get_cursor_user_path():
    """Lấy đường dẫn User data của Cursor AI"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Cursor" / "User"
    elif system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "Cursor" / "User"
    elif system == "Linux":
        return Path.home() / ".config" / "Cursor" / "User"
    else:
        return None

def clear_cursor_cache():
    """Xóa cache của Cursor AI"""
    cache_path = get_cursor_cache_path()
    
    if not cache_path:
        return False
    
    if not cache_path.exists():
        print(f"Không tìm thấy thư mục cache: {cache_path}")
        return False
    
    try:
        # Xóa các thư mục cache quan trọng
        cache_dirs = [
            "Cache",
            "Code Cache", 
            "GPUCache",
            "Service Worker",
            "Session Storage",
            "Local Storage",
            "IndexedDB",
            "Databases"
        ]
        
        for dir_name in cache_dirs:
            dir_path = cache_path / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"✓ Đã xóa: {dir_name}")
        
        # Xóa file cache khác
        cache_files = [
            "Cookies",
            "Cookies-journal",
            "Preferences",
            "Secure Preferences",
            "Local State",
            "Network Persistent State"
        ]
        
        for file_name in cache_files:
            file_path = cache_path / file_name
            if file_path.exists():
                file_path.unlink()
                print(f"✓ Đã xóa: {file_name}")
        
        print("✓ Đã xóa cache thành công!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi xóa cache: {e}")
        return False

def reset_machine_id():
    """Reset Machine ID của Cursor AI sử dụng script từ cursor-free-vip"""
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            print("🔄 Đang mở Terminal và chạy script reset từ cursor-free-vip...")
            print("📥 Tải script install.sh...")
            
            # Lệnh curl để tải và chạy script
            curl_cmd = "curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh"
            
            print("🚀 Mở Terminal và chạy lệnh:")
            print(f"   {curl_cmd}")
            print("\n⚠️  Lưu ý: Script sẽ tự động reset Machine ID và tạo tài khoản mới.")
            
            # Mở Terminal và chạy lệnh
            terminal_cmd = ["open", "-a", "Terminal"]
            subprocess.run(terminal_cmd, check=True)
            
            # Chờ một chút để Terminal mở
            import time
            time.sleep(2)
            
            # Chạy lệnh curl trong Terminal
            osascript_cmd = f'osascript -e \'tell application "Terminal" to do script "{curl_cmd}"\''
            result = subprocess.run(osascript_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Đã mở Terminal và chạy script cursor-free-vip!")
                print("📱 Script đang chạy trong Terminal mới.")
            else:
                print(f"⚠️  Có thể có lỗi khi chạy script: {result.stderr}")
                print("💡 Bạn có thể copy và paste lệnh này vào Terminal:")
                print(f"   {curl_cmd}")
                
        elif system == "Windows":
            print("🔄 Đang mở PowerShell và chạy script reset từ cursor-free-vip...")
            print("📥 Tải script install.ps1...")
            
            # Lệnh PowerShell để tải và chạy script
            ps_cmd = "irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex"
            
            print("🚀 Mở PowerShell và chạy lệnh:")
            print(f"   {ps_cmd}")
            print("\n⚠️  Lưu ý: Script sẽ tự động reset Machine ID và tạo tài khoản mới.")
            
            # Mở PowerShell và chạy lệnh
            powershell_cmd = ["powershell", "-Command", ps_cmd]
            
            # Mở PowerShell mới
            subprocess.Popen(["powershell", "-NoExit", "-Command", ps_cmd])
            
            print("✅ Đã mở PowerShell và chạy script cursor-free-vip!")
            print("📱 Script đang chạy trong PowerShell mới.")
                
        elif system == "Linux":
            print("🔄 Đang mở Terminal và chạy script reset từ cursor-free-vip...")
            print("📥 Tải script install.sh...")
            
            # Lệnh curl để tải và chạy script
            curl_cmd = "curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh"
            
            print("🚀 Mở Terminal và chạy lệnh:")
            print(f"   {curl_cmd}")
            print("\n⚠️  Lưu ý: Script sẽ tự động reset Machine ID và tạo tài khoản mới.")
            
            # Thử mở terminal khác nhau trên Linux
            terminal_apps = ["gnome-terminal", "konsole", "xterm", "terminator"]
            terminal_opened = False
            
            for terminal_app in terminal_apps:
                try:
                    # Mở terminal mới với lệnh
                    terminal_cmd = [terminal_app, "--", "bash", "-c", curl_cmd]
                    subprocess.Popen(terminal_cmd)
                    print(f"✅ Đã mở {terminal_app} và chạy script cursor-free-vip!")
                    print("📱 Script đang chạy trong Terminal mới.")
                    terminal_opened = True
                    break
                except FileNotFoundError:
                    continue
            
            if not terminal_opened:
                print("⚠️  Không thể mở terminal tự động.")
                print("💡 Bạn có thể copy và paste lệnh này vào terminal:")
                print(f"   {curl_cmd}")
                
        else:
            print(f"❌ Hệ điều hành {system} không được hỗ trợ")
            return False
            
        return True
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy script cursor-free-vip: {e}")
        print("💡 Bạn có thể chạy thủ công:")
        if system == "Darwin" or system == "Linux":
            print("   curl -fsSL https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh -o install.sh && chmod +x install.sh && ./install.sh")
        elif system == "Windows":
            print("   irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex")
        return False

def clear_user_storage():
    """Xóa storage của user (dựa trên cursor-free-vip)"""
    user_path = get_cursor_user_path()
    
    if not user_path:
        return False
    
    try:
        # Xóa các file storage quan trọng
        storage_files = [
            "globalStorage/storage.json",
            "globalStorage/state.vscdb",
            "globalStorage/state.vscdb-journal",
            "settings.json",
            "keybindings.json",
            "snippets",
            "extensions"
        ]
        
        deleted_count = 0
        for file_name in storage_files:
            file_path = user_path / file_name
            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                    print(f"✓ Đã xóa: {file_name}")
                    deleted_count += 1
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"✓ Đã xóa thư mục: {file_name}")
                    deleted_count += 1
        
        # Xóa workspaceStorage
        workspace_storage = user_path / "workspaceStorage"
        if workspace_storage.exists():
            shutil.rmtree(workspace_storage)
            print("✓ Đã xóa workspaceStorage")
            deleted_count += 1
        
        if deleted_count > 0:
            print(f"✓ Đã xóa {deleted_count} file/thư mục storage")
        else:
            print("⚠️  Không tìm thấy file storage để xóa")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi xóa user storage: {e}")
        return False

def logout_cursor():
    """Logout khỏi Cursor AI bằng cách xóa thông tin đăng nhập"""
    cache_path = get_cursor_cache_path()
    
    if not cache_path:
        return False
    
    try:
        # Xóa file chứa thông tin đăng nhập - mở rộng danh sách
        login_files = [
            "User Data/Default/Login Data",
            "User Data/Default/Login Data-journal",
            "User Data/Default/Web Data",
            "User Data/Default/Web Data-journal",
            "User Data/Default/Network Persistent State",
            "User Data/Default/Network Action Predictor",
            "User Data/Default/Network Action Predictor-journal",
            "User Data/Default/Origin Bound Certs",
            "User Data/Default/Origin Bound Certs-journal",
            "User Data/Default/QuotaManager",
            "User Data/Default/QuotaManager-journal",
            "User Data/Default/TransportSecurity",
            "User Data/Default/TransportSecurity-journal",
            "User Data/Default/Visited Links",
            "User Data/Default/Visited Links-journal",
            "User Data/Default/Shortcuts",
            "User Data/Default/Shortcuts-journal",
            "User Data/Default/Top Sites",
            "User Data/Default/Top Sites-journal",
            "User Data/Default/Bookmarks",
            "User Data/Default/Bookmarks.bak",
            "User Data/Default/History",
            "User Data/Default/History-journal",
            "User Data/Default/History Index *",
            "User Data/Default/History Provider Cache",
            "User Data/Default/History Provider Cache-journal",
            "User Data/Default/Last Session",
            "User Data/Default/Last Tabs",
            "User Data/Default/Current Session",
            "User Data/Default/Current Tabs",
            "User Data/Default/Session Storage",
            "User Data/Default/Local Storage",
            "User Data/Default/IndexedDB",
            "User Data/Default/Databases",
            "User Data/Default/Extension State",
            "User Data/Default/Extension Rules",
            "User Data/Default/Extension Settings",
            "User Data/Default/Extension Scripts",
            "User Data/Default/Extension Local Storage",
            "User Data/Default/Extension Session Storage",
            "User Data/Default/Extension IndexedDB",
            "User Data/Default/Extension Cookies",
            "User Data/Default/Extension History",
            "User Data/Default/Extension Visited Links",
            "User Data/Default/Extension Bookmarks",
            "User Data/Default/Extension Shortcuts",
            "User Data/Default/Extension Top Sites",
            "User Data/Default/Extension TransportSecurity",
            "User Data/Default/Extension QuotaManager",
            "User Data/Default/Extension Origin Bound Certs",
            "User Data/Default/Extension Network Action Predictor",
            "User Data/Default/Extension Network Persistent State",
            "User Data/Default/Extension Web Data",
            "User Data/Default/Extension Login Data"
        ]
        
        deleted_count = 0
        for file_name in login_files:
            file_path = cache_path / file_name
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"✓ Đã xóa thông tin đăng nhập: {file_name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️  Không thể xóa {file_name}: {e}")
        
        # Xóa thư mục chứa thông tin đăng nhập
        login_dirs = [
            "User Data/Default/Session Storage",
            "User Data/Default/Local Storage", 
            "User Data/Default/IndexedDB",
            "User Data/Default/Databases",
            "User Data/Default/Extension State",
            "User Data/Default/Extension Local Storage",
            "User Data/Default/Extension Session Storage",
            "User Data/Default/Extension IndexedDB"
        ]
        
        for dir_name in login_dirs:
            dir_path = cache_path / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"✓ Đã xóa thư mục: {dir_name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"⚠️  Không thể xóa thư mục {dir_name}: {e}")
        
        if deleted_count > 0:
            print(f"✓ Đã logout thành công! Đã xóa {deleted_count} file/thư mục.")
        else:
            print("⚠️  Không tìm thấy file thông tin đăng nhập để xóa.")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi logout: {e}")
        return False

def force_kill_cursor():
    """Force kill tất cả process Cursor AI"""
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["pkill", "-f", "Cursor"], check=False)
            subprocess.run(["killall", "Cursor"], check=False)
        elif system == "Windows":
            subprocess.run(["taskkill", "/f", "/im", "Cursor.exe"], check=False)
        elif system == "Linux":
            subprocess.run(["pkill", "-f", "Cursor"], check=False)
            subprocess.run(["killall", "cursor"], check=False)
        
        print("✓ Đã force kill tất cả process Cursor AI")
        return True
        
    except Exception as e:
        print(f"⚠️  Không thể force kill Cursor AI: {e}")
        return False

def open_default_browser():
    """Mở trình duyệt mặc định theo hệ điều hành"""
    system = platform.system()
    
    # URL dashboard settings của Cursor
    cursor_dashboard_url = "https://cursor.com/dashboard?tab=settings"
    
    try:
        if system == "Darwin":  # macOS
            # Mở trình duyệt mặc định trên macOS
            subprocess.run(["open", cursor_dashboard_url], check=True)
            print("✅ Đã mở trình duyệt mặc định để truy cập Cursor Dashboard Settings")
            return True
            
        elif system == "Windows":
            # Mở trình duyệt mặc định trên Windows
            subprocess.run(["start", cursor_dashboard_url], shell=True, check=True)
            print("✅ Đã mở trình duyệt mặc định để truy cập Cursor Dashboard Settings")
            return True
            
        elif system == "Linux":
            # Thử các lệnh mở trình duyệt trên Linux
            browser_commands = [
                ["xdg-open", cursor_dashboard_url],
                ["x-www-browser", cursor_dashboard_url],
                ["firefox", cursor_dashboard_url],
                ["google-chrome", cursor_dashboard_url],
                ["chromium-browser", cursor_dashboard_url]
            ]
            
            for cmd in browser_commands:
                try:
                    subprocess.run(cmd, check=True)
                    print("✅ Đã mở trình duyệt để truy cập Cursor Dashboard Settings")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("⚠️  Không thể mở trình duyệt tự động trên Linux")
            print(f"💡 Vui lòng mở trình duyệt và truy cập: {cursor_dashboard_url}")
            return False
            
        else:
            print(f"❌ Hệ điều hành {system} không được hỗ trợ")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi mở trình duyệt: {e}")
        print(f"💡 Vui lòng mở trình duyệt và truy cập: {cursor_dashboard_url}")
        return False



def show_menu():
    """Hiển thị menu tùy chọn"""
    print("\n" + "="*50)
    print("🚀 CURSOR AI LOGOUT TOOL")
    print("="*50)
    print("Chọn tùy chọn:")
    print("1. 🔄 Reset Machine ID (sử dụng cursor-free-vip)")
    print("2. Logout account và xóa cache")
    print("3. Force kill Cursor AI (khuyến nghị trước khi logout)")
    print("4. 🔥 RESET HOÀN TOÀN (Đóng Cursor AI + Reset Machine ID + Mở Dashboard Settings)")
    print("5. 🌐 Mở trình duyệt truy cập Cursor Dashboard Settings")
    print("6. Thoát")
    print("="*50)

def main():
    """Hàm chính"""
    while True:
        show_menu()
        
        try:
            choice = input("\nNhập lựa chọn của bạn (1-5): ").strip()
            
            if choice == "1":
                print("\n🔄 Đang reset Machine ID sử dụng cursor-free-vip...")
                print("⚠️  Lưu ý: Script sẽ tự động tạo tài khoản mới và reset Machine ID")
                print("   Bạn có thể nhấn Ctrl+C để dừng nếu cần thiết.")
                
                if reset_machine_id():
                    print("✅ Đã reset Machine ID thành công!")
                    print("ℹ️  Sử dụng script từ cursor-free-vip để reset hoàn toàn")
                else:
                    print("❌ Có lỗi xảy ra khi reset Machine ID.")
                    
            elif choice == "2":
                print("\n🔄 Đang logout và xóa cache...")
                logout_success = logout_cursor()
                storage_success = clear_user_storage()
                cache_success = clear_cursor_cache()
                
                if logout_success or storage_success or cache_success:
                    print("✅ Hoàn thành! Vui lòng khởi động lại Cursor AI.")
                else:
                    print("⚠️  Một số thao tác có thể không thành công.")
                    
            elif choice == "3":
                print("\n🔄 Đang force kill Cursor AI...")
                force_kill_cursor()
                print("✅ Hoàn thành! Bây giờ có thể chạy logout.")
                    
            elif choice == "4":
                print("\n🔄 Bắt đầu reset hoàn toàn Cursor AI...")
                print("="*60)
                
                # Bước 1: Force kill Cursor AI
                print("📋 Bước 1: Đóng Cursor AI...")
                force_kill_success = force_kill_cursor()
                
                # Bước 2: Reset Machine ID sử dụng cursor-free-vip
                print("\n📋 Bước 2: Reset Machine ID sử dụng cursor-free-vip...")
                machine_id_success = reset_machine_id()
                
                # Bước 3: Mở trình duyệt để truy cập Cursor Dashboard Settings
                print("\n📋 Bước 3: Mở trình duyệt để truy cập Cursor Dashboard Settings...")
                browser_success = open_default_browser()
                
                print("\n" + "="*60)
                print("📊 KẾT QUẢ RESET HOÀN TOÀN:")
                print(f"  • Đóng Cursor AI: {'✅' if force_kill_success else '❌'}")
                print(f"  • Reset Machine ID: {'✅' if machine_id_success else '❌'}")
                print(f"  • Mở trình duyệt: {'✅' if browser_success else '❌'}")
                
                success_count = sum([force_kill_success, machine_id_success, browser_success])
                
                if success_count >= 2:
                    print("\n🎉 RESET HOÀN TOÀN THÀNH CÔNG!")
                    print("✅ Cursor AI đã được reset hoàn toàn.")
                    print("ℹ️  Sử dụng script từ cursor-free-vip để reset Machine ID")
                    print("🌐 Trình duyệt đã được mở để truy cập Cursor Dashboard Settings")
                    print("🚀 Bạn có thể khởi động lại Cursor AI và đăng nhập với tài khoản mới.")
                else:
                    print("\n⚠️  Một số thao tác có thể không thành công.")
                    print("🔧 Vui lòng thử lại hoặc chạy từng tùy chọn riêng lẻ.")
                    
            elif choice == "5":
                print("\n🌐 Đang mở trình duyệt để truy cập Cursor Dashboard Settings...")
                if open_default_browser():
                    print("✅ Hoàn thành!")
                else:
                    print("⚠️  Có lỗi xảy ra khi mở trình duyệt.")
                    
            elif choice == "6":
                print("\n👋 Tạm biệt!")
                break
                
            else:
                print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1, 2, 3, 4, 5 hoặc 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Đã hủy thao tác. Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Có lỗi xảy ra: {e}")
        
        if choice in ["1", "2", "3", "4", "5"]:
            input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()
