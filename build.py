import os
import sys
import shutil
import subprocess
from datetime import datetime

def create_version_file():
    version = datetime.now().strftime('%Y.%m.%d')
    with open('version.txt', 'w') as f:
        f.write(version)
    return version

def verify_build():
    """Verify that the build was successful and files are present"""
    dist_dir = os.path.join('dist', 'GS_Browser')
    if not os.path.exists(dist_dir):
        print("Error: Build directory not found!")
        return False
    
    required_files = ['GS_Browser.exe' if sys.platform == 'win32' else 'GS_Browser']
    for file in required_files:
        if not os.path.exists(os.path.join(dist_dir, file)):
            print(f"Error: Required file {file} not found in build directory!")
            return False
    
    print("Build verification successful!")
    return True

def build_windows():
    print("Building Windows executable...")
    # Create spec file for PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['kivy_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/assets/*', 'frontend/assets'),
        ('version.txt', '.'),
        ('browser_data.json', '.')
    ],
    hiddenimports=['kivy_garden.webview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GS_Browser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/assets/icon.ico'
)
"""
    with open('GS_Browser.spec', 'w') as f:
        f.write(spec_content)

    # Create required files if they don't exist
    if not os.path.exists('version.txt'):
        with open('version.txt', 'w') as f:
            f.write('1.0.0')
    
    if not os.path.exists('browser_data.json'):
        with open('browser_data.json', 'w') as f:
            f.write('{}')

    # Clean previous build
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    # Run PyInstaller with verbose output
    result = subprocess.run(['pyinstaller', 'GS_Browser.spec', '--clean', '--log-level=DEBUG'], 
                          capture_output=True, text=True)
    
    print("PyInstaller output:")
    print(result.stdout)
    if result.stderr:
        print("PyInstaller errors:")
        print(result.stderr)

    return verify_build()

def build_linux():
    print("Building Linux executable...")
    # Create spec file for PyInstaller
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['kivy_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/assets/*', 'frontend/assets'),
        ('*.txt', '.'),
        ('*.json', '.')
    ],
    hiddenimports=['kivy_garden.webview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GS_Browser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/assets/icon.png'
)
"""
    with open('GS_Browser.spec', 'w') as f:
        f.write(spec_content)

    # Clean previous build
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    # Run PyInstaller with verbose output
    result = subprocess.run(['pyinstaller', 'GS_Browser.spec', '--clean', '--log-level=DEBUG'], 
                          capture_output=True, text=True)
    
    print("PyInstaller output:")
    print(result.stdout)
    if result.stderr:
        print("PyInstaller errors:")
        print(result.stderr)

    return verify_build()

def create_installer_windows(version):
    print("Creating Windows installer...")
    # Create NSIS script
    nsis_script = f"""
!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "GS Browser"
OutFile "GS_Browser_Setup_{version}.exe"
InstallDir "$PROGRAMFILES\\GS Browser"

# Request application privileges for Windows Vista/7/8/10
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

# Function to verify installation
Function VerifyInstallation
    # Check if main executable exists
    IfFileExists "$INSTDIR\\GS_Browser.exe" 0 +3
        MessageBox MB_OK "Main executable found."
        Goto +2
    MessageBox MB_OK "Warning: Main executable not found!"

    # Check if assets directory exists
    IfFileExists "$INSTDIR\\frontend\\assets" 0 +3
        MessageBox MB_OK "Assets directory found."
        Goto +2
    MessageBox MB_OK "Warning: Assets directory not found!"
FunctionEnd

Section "Install"
    SetOutPath "$INSTDIR"
    
    # Create directories first
    CreateDirectory "$INSTDIR"
    CreateDirectory "$INSTDIR\\frontend"
    CreateDirectory "$INSTDIR\\frontend\\assets"
    
    # Copy files with verification
    SetOverwrite on
    SetOverwrite ifnewer
    
    # Copy main executable
    File /oname=$INSTDIR\\GS_Browser.exe "dist\\GS_Browser\\GS_Browser.exe"
    
    # Copy all other files
    File /r "dist\\GS_Browser\\*.*"
    
    # Verify file extraction
    Call VerifyInstallation
    
    # Create shortcuts
    CreateDirectory "$SMPROGRAMS\\GS Browser"
    CreateShortcut "$SMPROGRAMS\\GS Browser\\GS Browser.lnk" "$INSTDIR\\GS_Browser.exe"
    CreateShortcut "$DESKTOP\\GS Browser.lnk" "$INSTDIR\\GS_Browser.exe"
    
    # Create uninstaller
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    # Add to Add/Remove Programs
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "DisplayName" "GS Browser"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "DisplayVersion" "{version}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "Publisher" "GS Browser Team"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "DisplayIcon" "$INSTDIR\\GS_Browser.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "URLInfoAbout" "https://github.com/your-repo/gs-browser"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "HelpLink" "https://github.com/your-repo/gs-browser/issues"
    
    # Set installation size
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                       "EstimatedSize" "$0"
SectionEnd

Section "Uninstall"
    # Remove files with verification
    RMDir /r "$INSTDIR"
    
    # Remove shortcuts
    RMDir /r "$SMPROGRAMS\\GS Browser"
    Delete "$DESKTOP\\GS Browser.lnk"
    
    # Remove registry entries
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser"
SectionEnd
"""
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)

    # Run NSIS compiler with verbose output
    result = subprocess.run(['makensis', '/V4', 'installer.nsi'], 
                          capture_output=True, text=True)
    
    print("NSIS output:")
    print(result.stdout)
    if result.stderr:
        print("NSIS errors:")
        print(result.stderr)
        
    # Verify the installer was created
    installer_name = f"GS_Browser_Setup_{version}.exe"
    if not os.path.exists(installer_name):
        print(f"Error: Installer {installer_name} was not created!")
        return False
        
    print(f"Installer created successfully: {installer_name}")
    return True

def create_installer_linux(version):
    print("Creating Linux package...")
    # Create desktop entry
    desktop_entry = f"""[Desktop Entry]
Version={version}
Type=Application
Name=GS Browser
Comment=Modern web browser built with Kivy
Exec=/usr/bin/gs-browser
Icon=/usr/share/icons/gs-browser.png
Terminal=false
Categories=Network;WebBrowser;
"""
    os.makedirs('linux_package/usr/share/applications', exist_ok=True)
    with open('linux_package/usr/share/applications/gs-browser.desktop', 'w') as f:
        f.write(desktop_entry)

    # Create DEB package
    subprocess.run(['dpkg-deb', '--build', 'linux_package', f'gs-browser_{version}_amd64.deb'])

def main():
    # Create version file
    version = create_version_file()
    
    # Determine platform
    platform = sys.platform
    
    if platform == 'win32':
        if not build_windows():
            print("Windows build failed!")
            sys.exit(1)
        create_installer_windows(version)
    elif platform.startswith('linux'):
        if not build_linux():
            print("Linux build failed!")
            sys.exit(1)
        create_installer_linux(version)
    else:
        print(f"Unsupported platform: {platform}")
        sys.exit(1)

if __name__ == '__main__':
    main() 