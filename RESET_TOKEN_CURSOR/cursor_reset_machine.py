#!/usr/bin/env python3
"""
Cursor Reset Machine Script
This script calls option 1 (reset machine) from the cursor-free-vip tool.
Based on: https://github.com/yeongpin/cursor-free-vip
"""

import os
import sys
import json
import uuid
import hashlib
import shutil
import sqlite3
import platform
import tempfile
import glob
from datetime import datetime
from typing import Tuple
import configparser

# Define emoji constants
EMOJI = {
    "FILE": "📄",
    "BACKUP": "💾", 
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "🔄",
    "WARNING": "⚠️",
}

def get_user_documents_path():
    """Get user Documents folder path"""
    if sys.platform == "win32":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders") as key:
                documents_path, _ = winreg.QueryValueEx(key, "Personal")
                return documents_path
        except Exception:
            # fallback
            return os.path.join(os.path.expanduser("~"), "Documents")
    elif sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Documents")
    else:  # Linux
        # Get actual user's home directory
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            return os.path.join("/home", sudo_user, "Documents")
        return os.path.join(os.path.expanduser("~"), "Documents")

def get_cursor_paths() -> Tuple[str, str]:
    """Get Cursor related paths"""
    system = platform.system()
    
    # Read config file
    config = configparser.ConfigParser()
    config_dir = os.path.join(get_user_documents_path(), ".cursor-free-vip")
    config_file = os.path.join(config_dir, "config.ini")
    
    # Create config directory if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # Default paths for different systems
    default_paths = {
        "Darwin": "/Applications/Cursor.app/Contents/Resources/app",
        "Windows": os.path.join(os.getenv("LOCALAPPDATA", ""), "Programs", "Cursor", "resources", "app"),
        "Linux": ["/opt/Cursor/resources/app", "/usr/share/cursor/resources/app", os.path.expanduser("~/.local/share/cursor/resources/app"), "/usr/lib/cursor/app/"]
    }
    
    if system == "Linux":
        # Look for extracted AppImage with correct usr structure
        extracted_usr_paths = glob.glob(os.path.expanduser("~/squashfs-root/usr/share/cursor/resources/app"))
        # Also check current directory for extraction without home path prefix
        current_dir_paths = glob.glob("squashfs-root/usr/share/cursor/resources/app")
        
        # Add any found paths to the Linux paths list
        default_paths["Linux"].extend(extracted_usr_paths)
        default_paths["Linux"].extend(current_dir_paths)
    
    # If config doesn't exist, create it with default paths
    if not os.path.exists(config_file):
        for section in ['MacPaths', 'WindowsPaths', 'LinuxPaths']:
            if not config.has_section(section):
                config.add_section(section)
        
        if system == "Darwin":
            config.set('MacPaths', 'cursor_path', default_paths["Darwin"])
            config.set('MacPaths', 'storage_path', os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/storage.json"))
            config.set('MacPaths', 'sqlite_path', os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"))
            config.set('MacPaths', 'machine_id_path', os.path.expanduser("~/Library/Application Support/Cursor/machineId"))
        elif system == "Windows":
            config.set('WindowsPaths', 'cursor_path', default_paths["Windows"])
            config.set('WindowsPaths', 'storage_path', os.path.join(os.getenv("APPDATA", ""), "Cursor", "User", "globalStorage", "storage.json"))
            config.set('WindowsPaths', 'sqlite_path', os.path.join(os.getenv("APPDATA", ""), "Cursor", "User", "globalStorage", "state.vscdb"))
            config.set('WindowsPaths', 'machine_id_path', os.path.join(os.getenv("APPDATA", ""), "Cursor", "machineId"))
        else:  # Linux
            # Find the first existing path
            cursor_path = None
            for path in default_paths["Linux"]:
                if os.path.exists(path):
                    cursor_path = path
                    break
            
            if cursor_path is None:
                cursor_path = default_paths["Linux"][0]  # Use first path as default
            
            config.set('LinuxPaths', 'cursor_path', cursor_path)
            config.set('LinuxPaths', 'storage_path', os.path.expanduser("~/.config/Cursor/User/globalStorage/storage.json"))
            config.set('LinuxPaths', 'sqlite_path', os.path.expanduser("~/.config/Cursor/User/globalStorage/state.vscdb"))
            config.set('LinuxPaths', 'machine_id_path', os.path.expanduser("~/.config/Cursor/machineid"))
        
        # Write config file
        with open(config_file, 'w') as f:
            config.write(f)
    
    # Read config
    config.read(config_file)
    
    # Get paths based on system
    if system == "Darwin":
        storage_path = config.get('MacPaths', 'storage_path', fallback=os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/storage.json"))
        sqlite_path = config.get('MacPaths', 'sqlite_path', fallback=os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"))
    elif system == "Windows":
        storage_path = config.get('WindowsPaths', 'storage_path', fallback=os.path.join(os.getenv("APPDATA", ""), "Cursor", "User", "globalStorage", "storage.json"))
        sqlite_path = config.get('WindowsPaths', 'sqlite_path', fallback=os.path.join(os.getenv("APPDATA", ""), "Cursor", "User", "globalStorage", "state.vscdb"))
    else:  # Linux
        storage_path = config.get('LinuxPaths', 'storage_path', fallback=os.path.expanduser("~/.config/Cursor/User/globalStorage/storage.json"))
        sqlite_path = config.get('LinuxPaths', 'sqlite_path', fallback=os.path.expanduser("~/.config/Cursor/User/globalStorage/state.vscdb"))
    
    return storage_path, sqlite_path

def get_cursor_machine_id_path():
    """Get Cursor machineId file path"""
    system = platform.system()
    
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Cursor/machineId")
    elif system == "Windows":
        return os.path.join(os.getenv("APPDATA", ""), "Cursor", "machineId")
    else:  # Linux
        return os.path.expanduser("~/.config/Cursor/machineid")

class MachineIDResetter:
    def __init__(self):
        self.storage_path, self.sqlite_path = get_cursor_paths()
        self.db_path = self.storage_path
    
    def generate_new_ids(self):
        """Generate new machine ID"""
        # Generate new UUID
        dev_device_id = str(uuid.uuid4())

        # Generate new machineId (64 characters of hexadecimal)
        machine_id = hashlib.sha256(os.urandom(32)).hexdigest()

        # Generate new macMachineId (128 characters of hexadecimal)
        mac_machine_id = hashlib.sha512(os.urandom(64)).hexdigest()

        # Generate new sqmId
        sqm_id = "{" + str(uuid.uuid4()).upper() + "}"

        self.update_machine_id_file(dev_device_id)

        return {
            "telemetry.devDeviceId": dev_device_id,
            "telemetry.macMachineId": mac_machine_id,
            "telemetry.machineId": machine_id,
            "telemetry.sqmId": sqm_id,
            "storage.serviceMachineId": dev_device_id,
        }

    def update_machine_id_file(self, machine_id: str) -> bool:
        """Update machineId file with new machine_id"""
        try:
            # Get the machineId file path
            machine_id_path = get_cursor_machine_id_path()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(machine_id_path), exist_ok=True)

            # Create backup if file exists
            if os.path.exists(machine_id_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{machine_id_path}.backup.{timestamp}"
                try:
                    shutil.copy2(machine_id_path, backup_path)
                    print(f"{EMOJI['INFO']} Backup created at: {backup_path}")
                except Exception as e:
                    print(f"{EMOJI['WARNING']} Could not create backup: {str(e)}")

            # Write new machine ID to file
            with open(machine_id_path, "w", encoding="utf-8") as f:
                f.write(machine_id)

            print(f"{EMOJI['SUCCESS']} Successfully updated machineId file")
            return True

        except Exception as e:
            print(f"{EMOJI['ERROR']} Failed to update machineId file: {str(e)}")
            return False

    def update_sqlite_db(self, new_ids):
        """Update machine ID in SQLite database"""
        try:
            print(f"{EMOJI['INFO']} Updating SQLite database...")
            
            conn = sqlite3.connect(self.sqlite_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ItemTable (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

            updates = [
                (key, value) for key, value in new_ids.items()
            ]

            for key, value in updates:
                cursor.execute("""
                    INSERT OR REPLACE INTO ItemTable (key, value) 
                    VALUES (?, ?)
                """, (key, value))
                print(f"{EMOJI['INFO']} Updating: {key}")

            conn.commit()
            conn.close()
            print(f"{EMOJI['SUCCESS']} SQLite database updated successfully")
            return True

        except Exception as e:
            print(f"{EMOJI['ERROR']} SQLite update error: {str(e)}")
            return False

    def reset_machine_ids(self):
        """Reset machine ID and backup original file"""
        try:
            print(f"{EMOJI['INFO']} Checking Cursor installation...")

            if not os.path.exists(self.db_path):
                print(f"{EMOJI['ERROR']} Cursor storage file not found: {self.db_path}")
                return False

            if not os.access(self.db_path, os.R_OK | os.W_OK):
                print(f"{EMOJI['ERROR']} No permission to access Cursor storage file")
                return False

            print(f"{EMOJI['FILE']} Reading Cursor storage file...")
            with open(self.db_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.db_path}.bak.{timestamp}"
            print(f"{EMOJI['BACKUP']} Creating backup: {backup_path}")
            shutil.copy2(self.db_path, backup_path)

            print(f"{EMOJI['RESET']} Generating new machine IDs...")
            new_ids = self.generate_new_ids()

            # Update configuration file
            config.update(new_ids)

            print(f"{EMOJI['FILE']} Saving updated configuration...")
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            # Update SQLite database
            self.update_sqlite_db(new_ids)

            print(f"{EMOJI['SUCCESS']} Machine ID reset completed successfully!")
            print(f"\nNew machine IDs:")
            for key, value in new_ids.items():
                print(f"{EMOJI['INFO']} {key}: {value}")

            return True

        except PermissionError as e:
            print(f"{EMOJI['ERROR']} Permission error: {str(e)}")
            print(f"{EMOJI['INFO']} Please run as administrator")
            return False
        except Exception as e:
            print(f"{EMOJI['ERROR']} Process error: {str(e)}")
            return False

def main():
    """Main function to reset Cursor machine ID"""
    print("=" * 50)
    print(f"{EMOJI['RESET']} Cursor Machine ID Reset Tool")
    print("=" * 50)
    print(f"Based on: https://github.com/yeongpin/cursor-free-vip")
    print()

    # Check if Cursor is running
    if platform.system() == "Windows":
        try:
            import psutil
            cursor_processes = [p for p in psutil.process_iter(['name']) if 'cursor' in p.info['name'].lower()]
            if cursor_processes:
                print(f"{EMOJI['WARNING']} Cursor is currently running. Please close Cursor before proceeding.")
                print("Press Enter to continue anyway, or Ctrl+C to cancel...")
                input()
        except ImportError:
            print(f"{EMOJI['INFO']} psutil not available, skipping process check")

    resetter = MachineIDResetter()
    success = resetter.reset_machine_ids()

    print(f"\n{'=' * 50}")
    if success:
        print(f"{EMOJI['SUCCESS']} Reset completed successfully!")
        print(f"{EMOJI['INFO']} You can now restart Cursor to apply the changes.")
    else:
        print(f"{EMOJI['ERROR']} Reset failed. Please check the error messages above.")
    
    input(f"{EMOJI['INFO']} Press Enter to exit...")

if __name__ == "__main__":
    main()
