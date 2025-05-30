# Installation Guide

This guide will walk you through the process of installing GS Browser on your Windows system.

## Prerequisites

Before installing GS Browser, ensure your system meets these requirements:

- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- Internet connection for AI features
- Administrator privileges for installation

## Installation Methods

### Method 1: Using the Installer (Recommended)

1. Download the latest release from [GitHub Releases](https://github.com/Gauravsharma110044/GS-BROWSER/releases)
2. Locate the downloaded `GS_Browser_Setup.zip` file
3. Extract the zip file to a temporary location
4. Run `GS_Browser_Setup.exe` as administrator
5. Follow the installation wizard:
   - Accept the license agreement
   - Choose installation location (default: `C:\Program Files\GS Browser`)
   - Select components to install
   - Choose start menu folder
   - Create desktop shortcut (optional)
6. Click "Install" to begin installation
7. Wait for the installation to complete
8. Click "Finish" to launch GS Browser

### Method 2: Portable Version

1. Download the portable version from [GitHub Releases](https://github.com/Gauravsharma110044/GS-BROWSER/releases)
2. Extract the zip file to your desired location
3. Run `GS_Browser.exe` directly

### Method 3: Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/Gauravsharma110044/GS-BROWSER.git
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the application:
   ```bash
   python build_app.py
   ```

4. Run the application:
   ```bash
   python kivy_app.py
   ```

## Post-Installation

After installation, you should:

1. Launch GS Browser
2. Complete the initial setup wizard
3. Configure your preferences
4. Sign in to your account (optional)

## Troubleshooting Installation

### Common Issues

1. **"Access Denied" Error**
   - Run the installer as administrator
   - Check folder permissions

2. **Missing Dependencies**
   - Install Visual C++ Redistributable
   - Update Windows to latest version

3. **Installation Fails**
   - Check system requirements
   - Clear temporary files
   - Try portable version

### Uninstallation

1. Open Windows Settings
2. Go to Apps & Features
3. Find "GS Browser"
4. Click Uninstall
5. Follow the uninstallation wizard

## Support

If you encounter any issues during installation:

- Check the [FAQ](../docs/README.md#faq)
- Visit our [GitHub Issues](https://github.com/Gauravsharma110044/GS-BROWSER/issues)
- Join our [Community Forum](https://github.com/Gauravsharma110044/GS-BROWSER/discussions) 