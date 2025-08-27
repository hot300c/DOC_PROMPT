#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor AI Close Script - Python Version

This script closes Cursor AI processes and then:
1. Opens Terminal with PowerShell command for cursor-free-vip installation
2. Opens Chrome with specific profile and tabs for account deletion
3. Offers to reopen Cursor AI after account deletion
4. Cleans up Terminal and Chrome processes
"""

import os
import sys
import time
import argparse
import subprocess
import platform


def print_colored(text: str, color: str = "white") -> None:
    """Print colored text to console."""
    colors = {
        "cyan": "\033[96m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "red": "\033[91m",
        "white": "\033[97m",
        "gray": "\033[90m",
        "dark_yellow": "\033[33m",
        "dark_gray": "\033[37m"
    }
    reset = "\033[0m"
    
    color_code = colors.get(color, colors["white"])
    print(f"{color_code}{text}{reset}")


def close_cursor_processes(dry_run: bool = False) -> bool:
    """Close Cursor AI processes if running. Returns True if processes were found and closed."""
    try:
        if platform.system() == "Windows":
            # Windows: Check for Cursor.exe processes
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Cursor.exe", "/FO", "CSV"],
                capture_output=True, text=True, shell=True
            )
            if "Cursor.exe" in result.stdout:
                if dry_run:
                    print_colored("Would close Cursor AI processes", "dark_yellow")
                    return True
                else:
                    print_colored("Closing Cursor AI...", "yellow")
                    subprocess.run(["taskkill", "/F", "/IM", "Cursor.exe"], shell=True)
                    time.sleep(2)
                    print_colored("Cursor AI closed successfully.", "green")
                    return True
            else:
                print_colored("No Cursor AI processes found running.", "gray")
                return False
        else:
            # Unix-like systems: Check for Cursor processes
            result = subprocess.run(
                ["pgrep", "-f", "Cursor"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                if dry_run:
                    print_colored("Would close Cursor AI processes", "dark_yellow")
                    return True
                else:
                    print_colored("Closing Cursor AI...", "yellow")
                    subprocess.run(["pkill", "-f", "Cursor"])
                    time.sleep(2)
                    print_colored("Cursor AI closed successfully.", "green")
                    return True
            else:
                print_colored("No Cursor AI processes found running.", "gray")
                return False
    except Exception as e:
        print_colored(f"Error closing Cursor processes: {e}", "red")
        return False


def open_terminal_with_powershell_command(dry_run: bool = False) -> None:
    """Open Terminal and run PowerShell command for cursor-free-vip installation."""
    try:
        if platform.system() == "Windows":
            if dry_run:
                print_colored("Would open Terminal with PowerShell command", "dark_yellow")
                print_colored("Command: irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex", "dark_gray")
            else:
                print_colored("Opening Terminal with PowerShell command...", "yellow")
                
                # PowerShell command to install cursor-free-vip
                ps_command = 'irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex'
                
                print_colored(f"PowerShell command: {ps_command}", "dark_gray")
                
                # Method 1: Try to open PowerShell with the command directly
                try:
                    print_colored("Method 1: Opening PowerShell directly...", "yellow")
                    result = subprocess.run([
                        "powershell", "-Command", ps_command
                    ], shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print_colored("✅ PowerShell command executed successfully!", "green")
                        print_colored("Terminal should now be installing cursor-free-vip...", "green")
                    else:
                        print_colored(f"⚠️ PowerShell command had issues: {result.stderr}", "yellow")
                        print_colored("Trying alternative method...", "yellow")
                        
                        # Method 2: Open new PowerShell window with command
                        print_colored("Method 2: Opening new PowerShell window...", "yellow")
                        subprocess.Popen([
                            "powershell", "-Command", 
                            f"Start-Process powershell -ArgumentList '-Command', '{ps_command}' -WindowStyle Normal"
                        ])
                        print_colored("✅ New PowerShell window opened with command.", "green")
                        
                except Exception as e:
                    print_colored(f"Method 1 failed: {e}", "yellow")
                    print_colored("Trying alternative method...", "yellow")
                    
                    # Method 3: Fallback - just open PowerShell
                    try:
                        print_colored("Method 3: Opening PowerShell window...", "yellow")
                        subprocess.Popen(["powershell"])
                        print_colored("✅ PowerShell window opened.", "green")
                        print_colored("Please manually run: irm https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.ps1 | iex", "yellow")
                    except Exception as e2:
                        print_colored(f"All methods failed: {e2}", "red")
                        print_colored("Please open PowerShell manually and run the command.", "red")
                
                print_colored("Terminal setup completed.", "green")
        else:
            print_colored("PowerShell commands are only supported on Windows", "red")
    except Exception as e:
        print_colored(f"Error opening Terminal: {e}", "red")


def open_chrome_with_profile_and_tabs(dry_run: bool = False, profile_name: str = "carphucng2001a@gmail.com") -> None:
    """Open Chrome with specific profile and tabs."""
    try:
        if platform.system() == "Windows":
            if dry_run:
                print_colored(f"Would open Chrome with profile '{profile_name}'", "dark_yellow")
                print_colored("Would open tabs: cursor.com and dashboard settings", "dark_gray")
            else:
                print_colored(f"Opening Chrome with profile '{profile_name}' and tabs...", "yellow")
                
                # Method 1: Try to find the actual profile directory name
                profile_dir = None
                user_data_dir = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
                
                print_colored(f"Searching for Chrome profile with email: {profile_name}", "dark_gray")
                print_colored(f"Chrome User Data directory: {user_data_dir}", "dark_gray")
                
                if os.path.exists(user_data_dir):
                    # Look for profile directories
                    profile_items = os.listdir(user_data_dir)
                    print_colored(f"Found profile directories: {profile_items}", "dark_gray")
                    
                    for item in profile_items:
                        profile_path = os.path.join(user_data_dir, item)
                        if os.path.isdir(profile_path) and item != "System Profile":
                            # Check if this profile contains the email
                            preferences_file = os.path.join(profile_path, "Preferences")
                            if os.path.exists(preferences_file):
                                try:
                                    with open(preferences_file, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                        if profile_name in content:
                                            profile_dir = item
                                            print_colored(f"✅ Found matching profile: {item}", "green")
                                            break
                                        else:
                                            print_colored(f"Profile {item} does not contain the email", "dark_gray")
                                except Exception as e:
                                    print_colored(f"Could not read profile {item}: {e}", "dark_gray")
                                    continue
                else:
                    print_colored(f"❌ Chrome User Data directory not found: {user_data_dir}", "red")
                
                if profile_dir:
                    print_colored(f"Using profile directory: {profile_dir}", "green")
                    
                    # Method 1: Direct subprocess call
                    try:
                        print_colored("Method 1: Direct Chrome launch...", "yellow")
                        chrome_paths = [
                            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
                        ]
                        
                        chrome_exe = None
                        for path in chrome_paths:
                            if os.path.exists(path):
                                chrome_exe = path
                                print_colored(f"✅ Found Chrome at: {path}", "green")
                                break
                        
                        if chrome_exe:
                            tabs = [
                                "https://cursor.com",
                                "https://cursor.com/dashboard?tab=settings"
                            ]
                            
                            print_colored(f"Opening tabs: {tabs}", "dark_gray")
                            
                            chrome_cmd = [
                                chrome_exe,
                                f"--profile-directory={profile_dir}",
                                "--new-window"
                            ] + tabs
                            
                            print_colored(f"Chrome command: {' '.join(chrome_cmd)}", "dark_gray")
                            
                            subprocess.Popen(chrome_cmd)
                            print_colored("✅ Chrome opened with profile using direct method.", "green")
                            print_colored("Chrome should now be open with the specified profile and tabs.", "green")
                            return
                        else:
                            print_colored("❌ Chrome executable not found in common paths", "red")
                    except Exception as e:
                        print_colored(f"Method 1 failed: {e}", "yellow")
                        print_colored("Trying PowerShell method...", "yellow")
                
                # Method 2: PowerShell method (more reliable)
                print_colored("Method 2: PowerShell Chrome launch...", "yellow")
                
                ps_script = f"""
                $chromePath = Get-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe" -ErrorAction SilentlyContinue
                if (-not $chromePath) {{
                    $chromePath = Get-ItemProperty -Path "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe" -ErrorAction SilentlyContinue
                }}
                
                if ($chromePath) {{
                    $chromeExe = $chromePath.'(Default)'
                    if (Test-Path $chromeExe) {{
                        $profileDir = "{profile_dir if profile_dir else 'Default'}"
                        $tabs = @("https://cursor.com", "https://cursor.com/dashboard?tab=settings")
                        
                        Write-Host "Chrome executable: $chromeExe"
                        Write-Host "Profile directory: $profileDir"
                        Write-Host "Tabs: $tabs"
                        
                        $args = @("--profile-directory=$profileDir", "--new-window") + $tabs
                        Start-Process -FilePath $chromeExe -ArgumentList $args
                        Write-Host "Chrome opened with profile: $profileDir"
                    }} else {{
                        Write-Host "Chrome executable not found at: $chromeExe"
                    }}
                }} else {{
                    Write-Host "Chrome not found in registry"
                }}
                """
                
                print_colored("Executing PowerShell script...", "yellow")
                
                # Run PowerShell script
                result = subprocess.run([
                    "powershell", "-Command", ps_script
                ], shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print_colored("✅ Chrome opened with profile using PowerShell method.", "green")
                    print_colored("Chrome should now be open with the specified profile and tabs.", "green")
                else:
                    print_colored(f"⚠️ PowerShell method had issues: {result.stderr}", "yellow")
                    print_colored("Chrome may not have opened properly.", "yellow")
                
        else:
            print_colored("Chrome profile management is primarily supported on Windows", "red")
    except Exception as e:
        print_colored(f"Error opening Chrome: {e}", "red")


def confirm_logout_before_proceeding() -> bool:
    """Ask user to confirm they have logged out of Cursor account before proceeding."""
    print_colored("=" * 60, "cyan")
    print_colored("⚠️  IMPORTANT: ACCOUNT LOGOUT CONFIRMATION REQUIRED ⚠️", "yellow")
    print_colored("=" * 60, "cyan")
    print()
    print_colored("Before this script continues, you MUST:", "white")
    print_colored("1. Open Cursor AI application", "white")
    print_colored("2. Go to Settings/Account", "white")
    print_colored("3. Logout/Sign out of your current account", "white")
    print_colored("4. Close Cursor AI completely", "white")
    print()
    print_colored("This ensures your account data is properly cleared", "white")
    print_colored("and prevents any conflicts during the process.", "white")
    print()
    
    while True:
        try:
            response = input("Have you already logged out of your Cursor account? (yes/no): ").strip().lower()
            if response in ['yes', 'y', '1', 'true']:
                print_colored("✅ Confirmation received! Proceeding with script...", "green")
                print()
                return True
            elif response in ['no', 'n', '0', 'false']:
                print_colored("❌ Please logout from Cursor first, then run this script again.", "red")
                print_colored("Script will exit now.", "red")
                return False
            else:
                print_colored("Please answer 'yes' or 'no'.", "yellow")
        except KeyboardInterrupt:
            print_colored("\n❌ Script interrupted by user. Exiting...", "red")
            return False


def close_terminal_and_chrome() -> None:
    """Close Terminal and Chrome processes that were opened by the script."""
    try:
        print_colored("Cleaning up opened applications...", "yellow")
        
        if platform.system() == "Windows":
            # Close PowerShell/Command Prompt windows more effectively
            try:
                print_colored("Closing PowerShell and Command Prompt windows...", "yellow")
                
                # Method 1: Simple PowerShell cleanup - close all PowerShell except current
                simple_ps_cleanup = """
                $currentPID = $PID
                Get-Process powershell | Where-Object {$_.Id -ne $currentPID} | Stop-Process -Force
                Get-Process cmd | Stop-Process -Force
                Write-Host "Terminal cleanup completed"
                """
                
                result = subprocess.run([
                    "powershell", "-Command", simple_ps_cleanup
                ], shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print_colored("✅ Terminal windows cleanup completed.", "green")
                else:
                    print_colored(f"⚠️ Terminal cleanup had issues: {result.stderr}", "yellow")
                
            except Exception as e:
                print_colored(f"Error closing Terminal: {e}", "yellow")
            
            # Close Chrome processes more effectively
            try:
                print_colored("Closing Chrome...", "yellow")
                
                # Simple Chrome cleanup
                chrome_cleanup = """
                $chromeProcesses = Get-Process chrome -ErrorAction SilentlyContinue
                if ($chromeProcesses) {
                    Write-Host "Found $($chromeProcesses.Count) Chrome processes"
                    $chromeProcesses | Stop-Process -Force
                    Write-Host "Chrome processes closed"
                } else {
                    Write-Host "No Chrome processes found"
                }
                """
                
                result = subprocess.run([
                    "powershell", "-Command", chrome_cleanup
                ], shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print_colored("✅ Chrome cleanup completed.", "green")
                else:
                    print_colored(f"⚠️ Chrome cleanup had issues: {result.stderr}", "yellow")
                
            except Exception as e:
                print_colored(f"Error closing Chrome: {e}", "yellow")
                # Fallback: use taskkill
                try:
                    print_colored("Trying fallback method with taskkill...", "yellow")
                    subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], shell=True, capture_output=True)
                    print_colored("Chrome force closed via taskkill.", "green")
                except Exception as e2:
                    print_colored(f"Fallback Chrome cleanup also failed: {e2}", "red")
            
            # Additional cleanup: close any remaining browser processes
            try:
                print_colored("Checking for remaining browser processes...", "yellow")
                browser_processes = ["msedge.exe", "firefox.exe", "iexplore.exe"]
                
                for browser in browser_processes:
                    try:
                        result = subprocess.run(
                            ["tasklist", "/FI", f"IMAGENAME eq {browser}", "/FO", "CSV"],
                            capture_output=True, text=True, shell=True
                        )
                        if browser in result.stdout:
                            print_colored(f"Closing {browser}...", "yellow")
                            subprocess.run(["taskkill", "/F", "/IM", browser], shell=True, capture_output=True)
                            print_colored(f"{browser} closed.", "green")
                    except Exception as e:
                        print_colored(f"Error closing {browser}: {e}", "yellow")
                        
            except Exception as e:
                print_colored(f"Error during browser cleanup: {e}", "yellow")
                
        else:
            print_colored("Cleanup is primarily supported on Windows", "yellow")
            
    except Exception as e:
        print_colored(f"Error during cleanup: {e}", "red")


def ask_to_reopen_cursor(method: str = "auto") -> None:
    """Ask user if they want to reopen Cursor app after account deletion."""
    print_colored("=" * 50, "cyan")
    print_colored("🎯 FINAL STEP: REOPEN CURSOR APP", "cyan")
    print_colored("=" * 50, "cyan")
    print()
    print_colored("After you have completed deleting your account:", "white")
    print_colored("1. In Chrome: Complete the account deletion process", "white")
    print_colored("2. Wait for cursor-free-vip installation to finish in Terminal", "white")
    print_colored("3. You can now reopen Cursor AI with the new setup", "white")
    print()
    
    while True:
        try:
            response = input("Do you want to reopen Cursor AI now? (yes/no): ").strip().lower()
            if response in ['yes', 'y', '1', 'true']:
                print_colored("Opening Cursor AI...", "yellow")
                reopen_cursor_app(method)
                
                # After reopening Cursor, close Terminal and Chrome
                print()
                print_colored("Cleaning up opened applications...", "cyan")
                close_terminal_and_chrome()
                print_colored("✅ Cleanup completed! Terminal and Chrome have been closed.", "green")
                print_colored("Cursor AI is now running independently.", "green")
                break
            elif response in ['no', 'n', '0', 'false']:
                print_colored("✅ Cursor AI will remain closed.", "green")
                print_colored("You can open it manually later when ready.", "white")
                
                # Even if not reopening Cursor, still offer to close Terminal and Chrome
                print()
                cleanup_response = input("Do you want to close Terminal and Chrome now? (yes/no): ").strip().lower()
                if cleanup_response in ['yes', 'y', '1', 'true']:
                    print_colored("Cleaning up opened applications...", "cyan")
                    close_terminal_and_chrome()
                    print_colored("✅ Cleanup completed! Terminal and Chrome have been closed.", "green")
                else:
                    print_colored("Terminal and Chrome will remain open.", "yellow")
                break
            else:
                print_colored("Please answer 'yes' or 'no'.", "yellow")
        except KeyboardInterrupt:
            print_colored("\n✅ Cursor AI will remain closed.", "green")
            break


def reopen_cursor_app(method: str = "auto") -> None:
    """Reopen Cursor AI application."""
    try:
        if platform.system() == "Windows":
            # Common Cursor installation paths
            cursor_paths = [
                r"C:\Users\%USERNAME%\AppData\Local\Programs\Cursor\Cursor.exe",
                r"C:\Program Files\Cursor\Cursor.exe",
                r"C:\Program Files (x86)\Cursor\Cursor.exe",
                os.path.expanduser(r"~\AppData\Local\Programs\Cursor\Cursor.exe")
            ]
            
            cursor_exe = None
            for path in cursor_paths:
                expanded_path = os.path.expandvars(path)
                if os.path.exists(expanded_path):
                    cursor_exe = expanded_path
                    break
            
            if cursor_exe:
                print_colored(f"Found Cursor at: {cursor_exe}", "green")
                
                if method == "auto":
                    # Try all methods
                    try:
                        # Method 1: Use cmd with /c start (most reliable for independence)
                        print_colored("Trying cmd /c start method...", "yellow")
                        subprocess.run([
                            "cmd", "/c", "start", "", cursor_exe
                        ], shell=True, capture_output=True)
                        print_colored("✅ Cursor AI is now opening (via cmd start)!", "green")
                        return
                    except Exception as e:
                        print_colored(f"Method 1 failed: {e}", "yellow")
                        print_colored("Trying PowerShell method...", "yellow")
                    
                    # Method 2: Use PowerShell Start-Process with -WindowStyle Normal
                    try:
                        ps_script = f"""
                        Start-Process -FilePath "{cursor_exe}" -WindowStyle Normal -PassThru | Out-Null
                        Write-Host "Cursor AI started independently via PowerShell"
                        """
                        
                        subprocess.run([
                            "powershell", "-Command", ps_script
                        ], shell=True, capture_output=True)
                        
                        print_colored("✅ Cursor AI is now opening via PowerShell!", "green")
                        return
                    except Exception as e:
                        print_colored(f"Method 2 failed: {e}", "yellow")
                        print_colored("Trying direct start method...", "yellow")
                    
                    # Method 3: Direct start with start_new_session
                    try:
                        subprocess.Popen([cursor_exe], start_new_session=True)
                        print_colored("✅ Cursor AI is now opening!", "green")
                    except Exception as e:
                        print_colored(f"All methods failed: {e}", "red")
                        print_colored("Please open Cursor manually from Start Menu or desktop shortcut.", "yellow")
                
                elif method == "cmd":
                    # Method 1: Use cmd with /c start (most reliable for independence)
                    try:
                        subprocess.run([
                            "cmd", "/c", "start", "", cursor_exe
                        ], shell=True, capture_output=True)
                        print_colored("✅ Cursor AI is now opening (via cmd start)!", "green")
                    except Exception as e:
                        print_colored(f"cmd method failed: {e}", "red")
                        print_colored("Please open Cursor manually.", "yellow")
                
                elif method == "powershell":
                    # Method 2: Use PowerShell Start-Process
                    try:
                        ps_script = f"""
                        Start-Process -FilePath "{cursor_exe}" -WindowStyle Normal -PassThru | Out-Null
                        Write-Host "Cursor AI started independently via PowerShell"
                        """
                        
                        subprocess.run([
                            "powershell", "-Command", ps_script
                        ], shell=True, capture_output=True)
                        
                        print_colored("✅ Cursor AI is now opening via PowerShell!", "green")
                    except Exception as e:
                        print_colored(f"PowerShell method failed: {e}", "red")
                        print_colored("Please open Cursor manually.", "yellow")
                
                elif method == "direct":
                    # Method 3: Direct start
                    try:
                        subprocess.Popen([cursor_exe], start_new_session=True)
                        print_colored("✅ Cursor AI is now opening!", "green")
                    except Exception as e:
                        print_colored(f"Direct method failed: {e}", "red")
                        print_colored("Please open Cursor manually.", "yellow")
                
                elif method == "detached":
                    # Method 4: Windows detached process (less reliable)
                    try:
                        subprocess.Popen(
                            [cursor_exe],
                            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                            start_new_session=True
                        )
                        print_colored("✅ Cursor AI is now opening (detached from script)!", "green")
                    except Exception as e:
                        print_colored(f"Detached method failed: {e}", "red")
                        print_colored("Please open Cursor manually.", "yellow")
            else:
                print_colored("❌ Cursor AI executable not found.", "red")
                print_colored("Please open Cursor manually from Start Menu or desktop shortcut.", "yellow")
        else:
            print_colored("Cursor reopening is primarily supported on Windows", "red")
    except Exception as e:
        print_colored(f"Error reopening Cursor: {e}", "red")
        print_colored("Please open Cursor manually.", "yellow")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Cursor AI Close Script - Closes processes and opens tools for account deletion")
    parser.add_argument(
        "--skip-pause", "-s",
        action="store_true",
        help="Skip pause at the end"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--chrome-profile", "-p",
        type=str,
        default="carphucng2001a@gmail.com",
        help="Chrome profile name or email to search for (default: carphucng2001a@gmail.com)"
    )
    parser.add_argument(
        "--skip-confirmation", "-c",
        action="store_true",
        help="Skip the logout confirmation step (use with caution)"
    )
    parser.add_argument(
        "--cursor-method", "-m",
        type=str,
        choices=["auto", "cmd", "powershell", "direct", "detached"],
        default="auto",
        help="Method to open Cursor independently (auto=try all, cmd=via cmd start, powershell=via PowerShell, direct=direct start, detached=Windows detached process)"
    )
    
    args = parser.parse_args()
    
    print_colored("=== CURSOR AI CLOSE & SETUP SCRIPT ===", "cyan")
    print_colored("This script will:", "white")
    print_colored("1. Ask for logout confirmation", "white")
    print_colored("2. Close Cursor AI processes", "white")
    print_colored("3. Open Terminal with PowerShell command for cursor-free-vip", "white")
    print_colored(f"4. Open Chrome with profile for account deletion (searching for: {args.chrome_profile})", "white")
    print_colored("5. Ask if you want to reopen Cursor after account deletion", "white")
    print_colored("6. Clean up Terminal and Chrome after setup completion", "white")
    print_colored(f"   (using method: {args.cursor_method})", "white")
    print()
    
    # Step 0: Confirm user has logged out of Cursor account
    if not args.skip_confirmation:
        print_colored("Step 0: Account Logout Confirmation", "cyan")
        if not confirm_logout_before_proceeding():
            sys.exit(1)
    else:
        print_colored("Step 0: Account Logout Confirmation SKIPPED (--skip-confirmation used)", "yellow")
        print()
    
    if args.dry_run:
        print_colored("DRY RUN: No changes will be made", "yellow")
        print()
    
    # Step 1: Close Cursor AI if running
    print_colored("Step 1: Closing Cursor AI...", "cyan")
    processes_found = close_cursor_processes(args.dry_run)
    
    if processes_found or args.dry_run:
        print()
        print_colored("Step 2: Opening Terminal with PowerShell command...", "cyan")
        open_terminal_with_powershell_command(args.dry_run)
        
        print()
        print_colored("Step 3: Opening Chrome with profile and tabs...", "cyan")
        # Pass the profile argument to the function
        open_chrome_with_profile_and_tabs(args.dry_run, args.chrome_profile)
        
        print()
        if args.dry_run:
            print_colored("DRY RUN COMPLETED - No actual changes made", "yellow")
        else:
            print_colored("SETUP COMPLETED!", "green")
            print_colored("1. Cursor AI has been closed", "white")
            print_colored("2. Terminal opened with PowerShell command for cursor-free-vip", "white")
            print_colored(f"3. Chrome opened with profile '{args.chrome_profile}'", "white")
            print_colored("4. Two tabs opened: cursor.com and dashboard settings", "white")
            print()
            print_colored("Next steps:", "yellow")
            print_colored("- In Terminal: Wait for cursor-free-vip installation to complete", "white")
            print_colored("- In Chrome: Navigate to dashboard settings to delete account", "white")
            print()
            
            # Step 4: Ask if user wants to reopen Cursor
            if not args.dry_run:
                ask_to_reopen_cursor(args.cursor_method)
    else:
        print_colored("No Cursor AI processes were running", "gray")
    
    if not args.skip_pause:
        print_colored("Press Enter to exit...", "gray")
        try:
            input()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
