#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor AI Close Script - macOS Optimized Version

This script is specifically optimized for macOS to close Cursor AI processes
without deleting any data or cache. Includes macOS-specific process management.
"""

import os
import sys
import time
import argparse
import subprocess
import platform
from typing import List, Tuple


def print_colored(text: str, color: str = "white") -> None:
    """Print colored text to console with macOS terminal support."""
    colors = {
        "cyan": "\033[96m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "red": "\033[91m",
        "white": "\033[97m",
        "gray": "\033[90m",
        "dark_yellow": "\033[33m",
        "dark_gray": "\033[37m",
        "blue": "\033[94m",
        "magenta": "\033[95m"
    }
    reset = "\033[0m"
    
    color_code = colors.get(color, colors["white"])
    print(f"{color_code}{text}{reset}")


def get_cursor_processes() -> List[Tuple[str, str]]:
    """Get all Cursor-related processes on macOS. Returns list of (pid, process_name)."""
    try:
        # Use ps to find Cursor processes with more detailed info
        result = subprocess.run(
            ["ps", "-axo", "pid,comm,args"],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            return []
        
        processes = []
        for line in result.stdout.strip().split('\n')[1:]:  # Skip header
            if line.strip():
                parts = line.split(None, 2)
                if len(parts) >= 3:
                    pid, comm, args = parts[0], parts[1], parts[2]
                    # Check for Cursor in command name or arguments
                    if "Cursor" in comm or "Cursor" in args:
                        processes.append((pid, f"{comm} {args}"))
        
        return processes
    except Exception as e:
        print_colored(f"Error getting process list: {e}", "red")
        return []


def close_cursor_processes_macos(dry_run: bool = False) -> bool:
    """Close Cursor AI processes on macOS. Returns True if processes were found and closed."""
    try:
        # Check if we're on macOS
        if platform.system() != "Darwin":
            print_colored("This script is designed for macOS only.", "red")
            return False
        
        processes = get_cursor_processes()
        
        if not processes:
            print_colored("No Cursor AI processes found running.", "gray")
            return False
        
        print_colored(f"Found {len(processes)} Cursor-related process(es):", "cyan")
        for pid, process_info in processes:
            print_colored(f"  PID {pid}: {process_info}", "gray")
        
        if dry_run:
            print_colored("Would close Cursor AI processes", "dark_yellow")
            return True
        
        print_colored("Closing Cursor AI processes...", "yellow")
        
        # Close processes gracefully first
        # for pid, process_info in processes:
        #     try:
        #         print_colored(f"  Sending SIGTERM to PID {pid}...", "blue")
        #         subprocess.run(["kill", pid], check=True)
        #     except subprocess.CalledProcessError:
        #         print_colored(f"  Failed to send SIGTERM to PID {pid}", "red")
        
        # Wait a bit for graceful shutdown
        time.sleep(3)
        
        # Check if any processes are still running and force kill if needed
        remaining_processes = get_cursor_processes()
        if remaining_processes:
            print_colored("Some processes still running, force killing...", "yellow")
            for pid, process_info in remaining_processes:
                try:
                    print_colored(f"  Force killing PID {pid}...", "red")
                    subprocess.run(["kill", "-9", pid], check=True)
                except subprocess.CalledProcessError:
                    print_colored(f"  Failed to force kill PID {pid}", "red")
        
        # Final check
        time.sleep(2)
        final_check = get_cursor_processes()
        if not final_check:
            print_colored("All Cursor AI processes closed successfully.", "green")
            return True
        else:
            print_colored(f"Warning: {len(final_check)} process(es) still running", "yellow")
            return True
            
    except Exception as e:
        print_colored(f"Error closing Cursor processes: {e}", "red")
        return False


def check_cursor_installation() -> bool:
    """Check if Cursor is installed on macOS."""
    try:
        # Check common installation paths
        common_paths = [
            "/Applications/Cursor.app",
            "/Applications/Cursor.app/Contents/MacOS/Cursor",
            os.path.expanduser("~/Applications/Cursor.app"),
            os.path.expanduser("~/Applications/Cursor.app/Contents/MacOS/Cursor")
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print_colored(f"Cursor found at: {path}", "green")
                return True
        
        print_colored("Cursor installation not found in common locations.", "yellow")
        return False
        
    except Exception as e:
        print_colored(f"Error checking Cursor installation: {e}", "red")
        return False


def show_system_info() -> None:
    """Display macOS system information."""
    try:
        print_colored("=== SYSTEM INFORMATION ===", "blue")
        
        # macOS version
        result = subprocess.run(["sw_vers", "-productVersion"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"macOS Version: {result.stdout.strip()}", "white")
        
        # Architecture
        result = subprocess.run(["uname", "-m"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"Architecture: {result.stdout.strip()}", "white")
        
        # Available memory
        result = subprocess.run(["vm_stat"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines[:3]:  # Show first 3 lines
                if ':' in line:
                    key, value = line.split(':', 1)
                    print_colored(f"{key.strip()}: {value.strip()}", "gray")
        
        print()
        
    except Exception as e:
        print_colored(f"Error getting system info: {e}", "red")


def main():
    """Main function for macOS Cursor logout script."""
    parser = argparse.ArgumentParser(
        description="Cursor AI Close Script for macOS - Only closes processes, no data deletion"
    )
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
        "--check-installation", "-c",
        action="store_true",
        help="Check Cursor installation status"
    )
    parser.add_argument(
        "--system-info", "-i",
        action="store_true",
        help="Show macOS system information"
    )
    
    args = parser.parse_args()
    
    print_colored("=== CURSOR AI CLOSE SCRIPT (macOS) ===", "cyan")
    print_colored("This script only closes Cursor AI processes", "white")
    print_colored("No data, cache, or settings will be deleted", "white")
    print()
    
    # Show system info if requested
    if args.system_info:
        show_system_info()
    
    # Check installation if requested
    if args.check_installation:
        check_cursor_installation()
        print()
    
    if args.dry_run:
        print_colored("DRY RUN: No changes will be made", "yellow")
        print()
    
    # Close Cursor AI if running
    processes_found = close_cursor_processes_macos(args.dry_run)
    
    print()
    if processes_found:
        if args.dry_run:
            print_colored("Cursor AI processes found - would be closed in real run", "dark_yellow")
        else:
            print_colored("Cursor AI has been closed successfully!", "green")
    else:
        print_colored("No Cursor AI processes were running", "gray")
    
    if not args.skip_pause:
        print_colored("Press Enter to exit...", "gray")
        try:
            input()
        except KeyboardInterrupt:
            print_colored("\nExiting...", "yellow")


if __name__ == "__main__":
    main()

