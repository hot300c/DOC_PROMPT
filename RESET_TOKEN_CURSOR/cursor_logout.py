#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cursor AI Close Script - Python Version

This script only closes Cursor AI processes without deleting any data or cache.
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


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Cursor AI Close Script - Only closes processes, no data deletion")
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
    
    args = parser.parse_args()
    
    print_colored("=== CURSOR AI CLOSE SCRIPT ===", "cyan")
    print_colored("This script only closes Cursor AI processes", "white")
    print_colored("No data, cache, or settings will be deleted", "white")
    print()
    
    if args.dry_run:
        print_colored("DRY RUN: No changes will be made", "yellow")
        print()
    
    # Close Cursor AI if running
    processes_found = close_cursor_processes(args.dry_run)
    
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
            pass


if __name__ == "__main__":
    main()
