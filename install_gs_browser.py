#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import json
import shutil
import argparse
import time
from pathlib import Path
from tqdm import tqdm

class GSBrowserInstaller:
    def __init__(self, silent=False, install_dir=None):
        self.is_windows = platform.system() == "Windows"
        self.silent = silent
        self.install_dir = install_dir or os.path.expanduser("~/GS-Browser")
        self.venv_dir = os.path.join(self.install_dir, "venv")
        self.required_dirs = [
            "adblock", "icons", "config", "tests", "extensions",
            "bookmarks", "history", "downloads", "cache", "screenshots"
        ]
        self.total_steps = 6  # Total number of installation steps

    def print_step(self, message):
        """Print installation step message."""
        if not self.silent:
            print(f"\n[{message}]")

    def check_system_requirements(self):
        """Check system requirements."""
        self.print_step("Checking system requirements")
        
        # Check Python version
        if sys.version_info < (3, 9):
            raise SystemError("Python 3.9 or later is required")
        
        # Check available disk space (at least 500MB)
        if self.is_windows:
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(self.install_dir), None, None, ctypes.pointer(free_bytes)
            )
            free_space = free_bytes.value
        else:
            st = os.statvfs(self.install_dir)
            free_space = st.f_bavail * st.f_frsize
        
        if free_space < 500 * 1024 * 1024:  # 500MB
            raise SystemError("At least 500MB of free disk space is required")
        
        # Check if running with admin privileges
        if self.is_windows:
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                is_admin = False
        else:
            is_admin = os.geteuid() == 0
        
        if not is_admin:
            self.print_step("Warning: Running without administrator privileges")

    def create_directories(self):
        """Create necessary directories."""
        self.print_step("Creating directories")
        for dir_name in tqdm(self.required_dirs, disable=self.silent):
            os.makedirs(os.path.join(self.install_dir, dir_name), exist_ok=True)

    def create_virtual_environment(self):
        """Create and activate virtual environment."""
        self.print_step("Setting up virtual environment")
        if os.path.exists(self.venv_dir):
            shutil.rmtree(self.venv_dir)
        
        subprocess.run([sys.executable, "-m", "venv", self.venv_dir], 
                      check=True, 
                      stdout=subprocess.DEVNULL if self.silent else None)
        
        if self.is_windows:
            python_path = os.path.join(self.venv_dir, "Scripts", "python.exe")
            pip_path = os.path.join(self.venv_dir, "Scripts", "pip.exe")
        else:
            python_path = os.path.join(self.venv_dir, "bin", "python")
            pip_path = os.path.join(self.venv_dir, "bin", "pip")

        return python_path, pip_path

    def install_dependencies(self, pip_path):
        """Install required packages."""
        self.print_step("Installing dependencies")
        requirements = [
            "PyQt5>=5.15.0",
            "PyQtWebEngine>=5.15.0",
            "requests>=2.25.0",
            "google-auth>=2.3.0",
            "google-auth-oauthlib>=0.4.0",
            "google-auth-httplib2>=0.1.0",
            "google-api-python-client>=2.0.0",
            "adblockparser>=0.7.0",
            "python-dotenv>=0.19.0",
            "cryptography>=3.4.0",
            "pillow>=8.0.0"
        ]
        
        for req in tqdm(requirements, disable=self.silent):
            try:
                subprocess.run([pip_path, "install", req], 
                             check=True,
                             stdout=subprocess.DEVNULL if self.silent else None)
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to install {req}: {str(e)}")
                continue

    def create_shortcuts(self):
        """Create desktop and start menu shortcuts."""
        self.print_step("Creating shortcuts")
        try:
            if self.is_windows:
                self.create_windows_shortcuts()
            else:
                self.create_linux_shortcuts()
        except Exception as e:
            print(f"Warning: Failed to create shortcuts: {str(e)}")

    def create_windows_shortcuts(self):
        """Create Windows shortcuts."""
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            start_menu = winshell.start_menu()
            
            # Create desktop shortcut
            path = os.path.join(desktop, "GS Browser.lnk")
            target = os.path.join(self.venv_dir, "Scripts", "pythonw.exe")
            wd = self.install_dir
            icon = os.path.join(self.install_dir, "icons", "chrome.ico")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.Arguments = "gs_browser.py"
            shortcut.WorkingDirectory = wd
            shortcut.IconLocation = icon
            shortcut.save()
            
            # Create start menu shortcut
            path = os.path.join(start_menu, "Programs", "GS Browser.lnk")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.Arguments = "gs_browser.py"
            shortcut.WorkingDirectory = wd
            shortcut.IconLocation = icon
            shortcut.save()
        except ImportError:
            print("Warning: Required packages for shortcuts not installed")
            print("Run: pip install winshell pywin32")

    def create_linux_shortcuts(self):
        """Create Linux shortcuts."""
        try:
            # Desktop shortcut
            desktop_entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=GS Browser
Comment=Modern web browser with ad-blocking
Exec={os.path.join(self.venv_dir, 'bin', 'python')} {os.path.join(self.install_dir, 'gs_browser.py')}
Icon={os.path.join(self.install_dir, 'icons', 'chrome.ico')}
Terminal=false
Categories=Network;WebBrowser;
"""
            desktop_path = os.path.expanduser("~/Desktop/GS Browser.desktop")
            with open(desktop_path, "w") as f:
                f.write(desktop_entry)
            os.chmod(desktop_path, 0o755)
            
            # Application menu entry
            app_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(app_dir, exist_ok=True)
            with open(os.path.join(app_dir, "gs-browser.desktop"), "w") as f:
                f.write(desktop_entry)
        except Exception as e:
            print(f"Warning: Failed to create Linux shortcuts: {str(e)}")

    def create_default_config(self):
        """Create default configuration file."""
        self.print_step("Creating configuration")
        config = {
            "theme": "light",
            "homepage": "homepage.html",
            "search_engine": "google",
            "ad_blocking": True,
            "sync_enabled": False,
            "developer_mode": False
        }
        config_path = os.path.join(self.install_dir, "config", "settings.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

    def create_uninstaller(self):
        """Create uninstaller script."""
        self.print_step("Creating uninstaller")
        if self.is_windows:
            uninstaller = os.path.join(self.install_dir, "uninstall.bat")
            with open(uninstaller, "w") as f:
                f.write(f"""@echo off
echo Uninstalling GS Browser...
rmdir /s /q "{self.install_dir}"
echo Uninstallation complete!
pause
""")
        else:
            uninstaller = os.path.join(self.install_dir, "uninstall.sh")
            with open(uninstaller, "w") as f:
                f.write(f"""#!/bin/bash
echo "Uninstalling GS Browser..."
rm -rf "{self.install_dir}"
echo "Uninstallation complete!"
""")
            os.chmod(uninstaller, 0o755)

    def install(self):
        """Main installation process."""
        try:
            if not self.silent:
                print("=" * 50)
                print("GS Browser Installation")
                print("=" * 50)
            
            # Check system requirements
            self.check_system_requirements()
            
            # Create installation directory
            os.makedirs(self.install_dir, exist_ok=True)
            
            # Create necessary directories
            self.create_directories()
            
            # Set up virtual environment
            python_path, pip_path = self.create_virtual_environment()
            
            # Install dependencies
            self.install_dependencies(pip_path)
            
            # Create default configuration
            self.create_default_config()
            
            # Create shortcuts
            self.create_shortcuts()
            
            # Create uninstaller
            self.create_uninstaller()
            
            if not self.silent:
                print("\n" + "=" * 50)
                print("Installation completed successfully!")
                print("=" * 50)
                print("\nYou can now run GS Browser by:")
                print("1. Double-clicking the desktop shortcut")
                print("2. Running 'python gs_browser.py' from the installation directory")
                print("\nInstallation directory:", self.install_dir)
                print("To uninstall, run the uninstaller in the installation directory")
            
            return True
            
        except Exception as e:
            if not self.silent:
                print(f"\nError during installation: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description="GS Browser Installer")
    parser.add_argument("--silent", action="store_true", help="Run installation silently")
    parser.add_argument("--install-dir", help="Custom installation directory")
    args = parser.parse_args()
    
    installer = GSBrowserInstaller(silent=args.silent, install_dir=args.install_dir)
    success = installer.install()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 