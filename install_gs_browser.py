#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import json
import shutil
from pathlib import Path

class GSBrowserInstaller:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.install_dir = os.path.expanduser("~/GS-Browser")
        self.venv_dir = os.path.join(self.install_dir, "venv")
        self.required_dirs = [
            "adblock", "icons", "config", "tests", "extensions",
            "bookmarks", "history", "downloads", "cache", "screenshots"
        ]

    def check_python(self):
        """Check if Python 3.9+ is installed."""
        if sys.version_info < (3, 9):
            print("Error: Python 3.9 or later is required.")
            sys.exit(1)

    def create_directories(self):
        """Create necessary directories."""
        print("Creating directories...")
        for dir_name in self.required_dirs:
            os.makedirs(os.path.join(self.install_dir, dir_name), exist_ok=True)

    def create_virtual_environment(self):
        """Create and activate virtual environment."""
        print("Setting up virtual environment...")
        if os.path.exists(self.venv_dir):
            shutil.rmtree(self.venv_dir)
        
        subprocess.run([sys.executable, "-m", "venv", self.venv_dir], check=True)
        
        # Get the path to the Python executable in the virtual environment
        if self.is_windows:
            python_path = os.path.join(self.venv_dir, "Scripts", "python.exe")
            pip_path = os.path.join(self.venv_dir, "Scripts", "pip.exe")
        else:
            python_path = os.path.join(self.venv_dir, "bin", "python")
            pip_path = os.path.join(self.venv_dir, "bin", "pip")

        return python_path, pip_path

    def install_dependencies(self, pip_path):
        """Install required packages."""
        print("Installing dependencies...")
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
        
        for req in requirements:
            subprocess.run([pip_path, "install", req], check=True)

    def create_shortcuts(self):
        """Create desktop and start menu shortcuts."""
        print("Creating shortcuts...")
        if self.is_windows:
            self.create_windows_shortcuts()
        else:
            self.create_linux_shortcuts()

    def create_windows_shortcuts(self):
        """Create Windows shortcuts."""
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

    def create_linux_shortcuts(self):
        """Create Linux shortcuts."""
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

    def create_default_config(self):
        """Create default configuration file."""
        config = {
            "theme": "light",
            "homepage": "homepage.html",
            "search_engine": "google"
        }
        config_path = os.path.join(self.install_dir, "config", "settings.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

    def install(self):
        """Main installation process."""
        try:
            print("Starting GS Browser installation...")
            self.check_python()
            
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
            
            print("\nInstallation completed successfully!")
            print("\nYou can now run GS Browser by:")
            print("1. Double-clicking the desktop shortcut")
            print("2. Running 'python gs_browser.py' from the installation directory")
            print("\nInstallation directory:", self.install_dir)
            
        except Exception as e:
            print(f"\nError during installation: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    installer = GSBrowserInstaller()
    installer.install() 