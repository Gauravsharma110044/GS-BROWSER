import os
import sys
import shutil
import json
import platform
import subprocess
import socket
import requests
import logging
from pathlib import Path
from datetime import datetime

class InstallationVerifier:
    def __init__(self, repair_mode=False):
        self.install_dir = os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'GS Browser')
        self.required_files = [
            'GS_Browser.exe',
            'frontend/assets/icon.ico',
            'frontend/assets/icon.png',
            'browser_data.json',
            'version.txt'
        ]
        self.required_dirs = [
            'frontend',
            'frontend/assets',
            'backend'
        ]
        self.min_requirements = {
            'ram': 4,  # GB
            'disk_space': 500,  # MB
            'os_version': '10.0.0',
            'python_version': '3.8.0'
        }
        self.repair_mode = repair_mode
        self.setup_logging()

    def setup_logging(self):
        """Setup detailed logging"""
        log_dir = os.path.join(self.install_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'verification_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('InstallationVerifier')

    def verify_all(self):
        """Run all verification checks with detailed reporting"""
        self.logger.info("Starting installation verification...")
        
        checks = {
            "System Requirements": self.verify_system_requirements(),
            "File Structure": self.verify_file_structure(),
            "Dependencies": self.verify_dependencies(),
            "Permissions": self.verify_permissions(),
            "Registry": self.verify_registry(),
            "Network": self.verify_network()
        }
        
        all_passed = all(checks.values())
        
        self.logger.info("\nVerification Results:")
        self.logger.info("====================")
        for check, result in checks.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            self.logger.info(f"{check}: {status}")
        
        if not all_passed and self.repair_mode:
            self.logger.info("\nAttempting automatic repair...")
            self.repair_installation()
            
        return all_passed

    def verify_system_requirements(self):
        """Verify system meets minimum requirements with detailed reporting"""
        try:
            self.logger.info("Checking system requirements...")
            
            # Check RAM
            if platform.system() == 'Windows':
                import psutil
                ram_gb = psutil.virtual_memory().total / (1024**3)
                self.logger.info(f"RAM: {ram_gb:.1f}GB (Required: {self.min_requirements['ram']}GB)")
                if ram_gb < self.min_requirements['ram']:
                    self.logger.error(f"Insufficient RAM. Required: {self.min_requirements['ram']}GB, Found: {ram_gb:.1f}GB")
                    return False

            # Check disk space
            free_space = shutil.disk_usage(self.install_dir).free / (1024**2)  # MB
            self.logger.info(f"Free disk space: {free_space:.1f}MB (Required: {self.min_requirements['disk_space']}MB)")
            if free_space < self.min_requirements['disk_space']:
                self.logger.error(f"Insufficient disk space. Required: {self.min_requirements['disk_space']}MB, Found: {free_space:.1f}MB")
                return False

            # Check OS version
            if platform.system() == 'Windows':
                os_version = platform.version()
                self.logger.info(f"OS Version: {os_version} (Required: {self.min_requirements['os_version']})")
                if os_version < self.min_requirements['os_version']:
                    self.logger.error(f"OS version too old. Required: {self.min_requirements['os_version']}, Found: {os_version}")
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking system requirements: {str(e)}", exc_info=True)
            return False

    def verify_file_structure(self):
        """Verify all required files and directories exist with detailed reporting"""
        try:
            self.logger.info("Checking file structure...")
            
            # Check directories
            for dir_path in self.required_dirs:
                full_path = os.path.join(self.install_dir, dir_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Missing directory: {dir_path}")
                    if self.repair_mode:
                        os.makedirs(full_path, exist_ok=True)
                        self.logger.info(f"Created directory: {dir_path}")
                    else:
                        return False

            # Check files
            for file_path in self.required_files:
                full_path = os.path.join(self.install_dir, file_path)
                if not os.path.exists(full_path):
                    self.logger.error(f"Missing file: {file_path}")
                    if self.repair_mode:
                        self.repair_missing_file(file_path)
                    else:
                        return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking file structure: {str(e)}", exc_info=True)
            return False

    def verify_dependencies(self):
        """Verify all required dependencies are installed with detailed reporting"""
        try:
            self.logger.info("Checking dependencies...")
            required_packages = {
                'kivy': '2.2.1',
                'kivymd': '1.1.1',
                'kivy_garden.webview': '0.1.0'
            }

            for package, min_version in required_packages.items():
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'show', package],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        self.logger.error(f"Missing package: {package}")
                        if self.repair_mode:
                            self.repair_missing_package(package)
                        else:
                            return False
                    else:
                        self.logger.info(f"Found package: {package}")
                except Exception as e:
                    self.logger.error(f"Error checking package {package}: {str(e)}", exc_info=True)
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking dependencies: {str(e)}", exc_info=True)
            return False

    def verify_permissions(self):
        """Verify file permissions and access rights with detailed reporting"""
        try:
            self.logger.info("Checking permissions...")
            
            # Check if we can write to the installation directory
            test_file = os.path.join(self.install_dir, 'test_write.tmp')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                self.logger.info("Write permission verified")
            except Exception as e:
                self.logger.error(f"Permission error: Cannot write to installation directory: {str(e)}")
                if self.repair_mode:
                    self.repair_permissions()
                else:
                    return False

            # Check if we can read all required files
            for file_path in self.required_files:
                full_path = os.path.join(self.install_dir, file_path)
                try:
                    with open(full_path, 'r') as f:
                        f.read(1)
                    self.logger.info(f"Read permission verified for {file_path}")
                except Exception as e:
                    self.logger.error(f"Permission error: Cannot read {file_path}: {str(e)}")
                    if self.repair_mode:
                        self.repair_file_permissions(file_path)
                    else:
                        return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking permissions: {str(e)}", exc_info=True)
            return False

    def verify_registry(self):
        """Verify registry entries with detailed reporting"""
        try:
            self.logger.info("Checking registry entries...")
            if platform.system() == 'Windows':
                import winreg
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GSBrowser"
                    )
                    winreg.CloseKey(key)
                    self.logger.info("Registry entries verified")
                    return True
                except WindowsError:
                    self.logger.error("Missing registry entries")
                    if self.repair_mode:
                        self.repair_registry()
                    else:
                        return False
            return True
        except Exception as e:
            self.logger.error(f"Error checking registry: {str(e)}", exc_info=True)
            return False

    def verify_network(self):
        """Verify network connectivity with detailed reporting"""
        try:
            self.logger.info("Checking network connectivity...")
            
            # Check internet connection
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                self.logger.info("Internet connection verified")
            except OSError:
                self.logger.error("No internet connection")
                return False

            # Check DNS resolution
            try:
                socket.gethostbyname("www.google.com")
                self.logger.info("DNS resolution verified")
            except socket.gaierror:
                self.logger.error("DNS resolution failed")
                return False

            # Check web connectivity
            try:
                response = requests.get("https://www.google.com", timeout=5)
                if response.status_code == 200:
                    self.logger.info("Web connectivity verified")
                else:
                    self.logger.error(f"Web connectivity failed: HTTP {response.status_code}")
                    return False
            except requests.RequestException as e:
                self.logger.error(f"Web connectivity failed: {str(e)}")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error checking network: {str(e)}", exc_info=True)
            return False

    def repair_installation(self):
        """Attempt to repair failed installation"""
        self.logger.info("Starting repair process...")
        
        # Repair file structure
        self.verify_file_structure()
        
        # Repair dependencies
        self.verify_dependencies()
        
        # Repair permissions
        self.verify_permissions()
        
        # Repair registry
        self.verify_registry()
        
        self.logger.info("Repair process completed")

    def repair_missing_file(self, file_path):
        """Repair a missing file"""
        try:
            self.logger.info(f"Attempting to repair missing file: {file_path}")
            # Add file repair logic here
            pass
        except Exception as e:
            self.logger.error(f"Error repairing file {file_path}: {str(e)}")

    def repair_missing_package(self, package):
        """Repair a missing package"""
        try:
            self.logger.info(f"Attempting to install missing package: {package}")
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        except Exception as e:
            self.logger.error(f"Error installing package {package}: {str(e)}")

    def repair_permissions(self):
        """Repair directory permissions"""
        try:
            self.logger.info("Attempting to repair directory permissions")
            # Add permission repair logic here
            pass
        except Exception as e:
            self.logger.error(f"Error repairing permissions: {str(e)}")

    def repair_file_permissions(self, file_path):
        """Repair file permissions"""
        try:
            self.logger.info(f"Attempting to repair file permissions: {file_path}")
            # Add file permission repair logic here
            pass
        except Exception as e:
            self.logger.error(f"Error repairing file permissions: {str(e)}")

    def repair_registry(self):
        """Repair registry entries"""
        try:
            self.logger.info("Attempting to repair registry entries")
            # Add registry repair logic here
            pass
        except Exception as e:
            self.logger.error(f"Error repairing registry: {str(e)}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='GS Browser Installation Verifier')
    parser.add_argument('--repair', action='store_true', help='Enable repair mode')
    args = parser.parse_args()

    verifier = InstallationVerifier(repair_mode=args.repair)
    if verifier.verify_all():
        print("\nInstallation verification completed successfully!")
        return 0
    else:
        print("\nInstallation verification failed. Please check the logs for details.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 