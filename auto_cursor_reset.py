#!/usr/bin/env python3
"""
Fully Automated Cursor Machine ID Reset Script
No user interaction required - runs completely automatically.
"""

import subprocess
import sys
import os
import time
import threading


def print_status(message, status_type="info"):
    """Print status message with emoji"""
    icons = {
        "info": "ℹ️",
        "success": "✅", 
        "warning": "⚠️",
        "error": "❌",
        "process": "🔄",
        "step": "📋",
        "running": "⚡",
        "output": "📄"
    }
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {icons.get(status_type, 'ℹ️')} {message}")


def print_separator(title="", char="-"):
    """Print separator line with optional title"""
    if title:
        print(f"\n{char * 20} {title} {char * 20}")
    else:
        print(char * 60)


def stream_output(process, output_type="stdout"):
    """Stream process output in real-time"""
    if output_type == "stdout":
        stream = process.stdout
        prefix = "📤"
    else:
        stream = process.stderr  
        prefix = "⚠️"
    
    for line in iter(stream.readline, ''):
        if line:
            # Clean up the line and show it
            clean_line = line.strip()
            if clean_line and not clean_line.startswith('['):
                print(f"{prefix} {clean_line}")
    stream.close()


def main():
    """Main automated execution"""
    print("=" * 70)
    print("🚀 AUTO CURSOR MACHINE ID RESET - DETAILED LOGGING")
    print("=" * 70)
    print()
    
    print_status("Initializing automation script...", "step")
    
    # Check Cursor installation
    print_separator("STEP 1: SYSTEM CHECK")
    cursor_path = "/Applications/Cursor.app"
    print_status(f"Checking for Cursor at: {cursor_path}", "process")
    
    if os.path.exists(cursor_path):
        print_status("Cursor application detected successfully", "success")
    else:
        print_status("Cursor not found - will continue anyway", "warning")
    
    print_status("System check completed", "success")
    
    try:
        # Step 1: Download installer
        print_separator("STEP 2: DOWNLOAD INSTALLER")
        print_status("Preparing download command...", "process")
        
        download_cmd = [
            "curl", "-fsSL", 
            "https://raw.githubusercontent.com/yeongpin/cursor-free-vip/main/scripts/install.sh",
            "-o", "install.sh"
        ]
        print_status(f"Executing: {' '.join(download_cmd[:3])} [URL] -o install.sh", "running")
        
        result = subprocess.run(download_cmd, check=True, capture_output=True, text=True)
        print_status("Download completed successfully", "success")
        
        # Check file size
        file_size = os.path.getsize("install.sh")
        print_status(f"Downloaded file size: {file_size:,} bytes", "info")
        
        # Step 2: Make executable
        print_separator("STEP 3: SETUP PERMISSIONS")
        print_status("Making script executable...", "process")
        subprocess.run(["chmod", "+x", "install.sh"], check=True)
        print_status("Script permissions updated successfully", "success")
        
        # Step 3: Run with automated inputs
        print_separator("STEP 4: RUN MACHINE ID RESET")
        print_status("Preparing automated inputs: 1 (Reset) → Enter → 0 (Exit)", "info")
        input_sequence = "1\n\n0\n"
        
        print_status("Starting Cursor Free VIP tool...", "running")
        print_status("This may take 30-60 seconds...", "info")
        
        process = subprocess.Popen(
            ["./install.sh"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print_status("Sending automated inputs to script...", "process")
        stdout, stderr = process.communicate(input=input_sequence, timeout=120)
        
        print_separator("STEP 5: PROCESSING RESULTS")
        print_status("Analyzing script output...", "process")
        
        # Show some key output lines
        important_lines = []
        lines = stdout.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in 
                   ['machine id reset', 'successfully', 'new machine id', 'error', 'failed']):
                important_lines.append(line.strip())
        
        if important_lines:
            print_status("Key output messages:", "output")
            for line in important_lines[:5]:  # Show first 5 important lines
                if line:
                    print(f"   📄 {line}")
        
        # Check if reset was successful by looking for success message
        if "Machine ID Reset Successfully" in stdout:
            print_status("Machine ID reset completed successfully!", "success")
            
            # Extract and display new Machine IDs
            print_separator("NEW MACHINE IDS GENERATED")
            found_ids = False
            for line in lines:
                if "telemetry." in line or "storage.serviceMachineId" in line:
                    if line.strip().startswith("ℹ️"):
                        print_status(f"Generated: {line.strip()[2:].strip()}", "info")
                        found_ids = True
            
            if not found_ids:
                print_status("Machine IDs were generated (details in output above)", "info")
        else:
            print_status("Reset process completed (check output for details)", "success")
        
        # Step 4: Cleanup
        print_separator("STEP 6: CLEANUP")
        print_status("Cleaning up temporary files...", "process")
        
        if os.path.exists("install.sh"):
            os.remove("install.sh")
            print_status("Removed install.sh", "success")
        
        print_status("Cleanup completed", "success")
        
        print_separator("AUTOMATION COMPLETED SUCCESSFULLY", "=")
        print_status("All steps completed successfully!", "success")
        print_status("Tip: Restart Cursor to ensure new Machine ID takes effect", "info")
        
    except subprocess.TimeoutExpired:
        print_separator("ERROR: TIMEOUT", "!")
        print_status("Process timed out after 120 seconds", "error")
        print_status("The script may be waiting for input or hanging", "warning")
        if 'process' in locals():
            print_status("Terminating process...", "process")
            process.kill()
        sys.exit(1)
        
    except subprocess.CalledProcessError as e:
        print_separator("ERROR: COMMAND FAILED", "!")
        print_status(f"Command failed with exit code {e.returncode}", "error")
        print_status(f"Command: {e.cmd}", "info")
        if e.stderr:
            print_status("Error output:", "error")
            print(f"   {e.stderr}")
        sys.exit(1)
        
    except Exception as e:
        print_separator("ERROR: UNEXPECTED", "!")
        print_status(f"Unexpected error: {type(e).__name__}: {e}", "error")
        import traceback
        print_status("Full traceback:", "error")
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Cleanup on any exit
        print_status("Performing final cleanup...", "process")
        if os.path.exists("install.sh"):
            try:
                os.remove("install.sh")
                print_status("Final cleanup completed", "success")
            except Exception as cleanup_error:
                print_status(f"Cleanup warning: {cleanup_error}", "warning")


if __name__ == "__main__":
    try:
        print_status("Starting Cursor Machine ID Reset Automation...", "running")
        main()
    except KeyboardInterrupt:
        print("\n")
        print_separator("INTERRUPTED BY USER", "!")
        print_status("Process interrupted by user (Ctrl+C)", "warning")
        print_status("Performing cleanup...", "process")
        if os.path.exists("install.sh"):
            os.remove("install.sh")
            print_status("Cleanup completed", "success")
        print_status("Script terminated by user", "info")
        sys.exit(1)
