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
    datas=[],
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/assets/icon.ico'
)
"""
    with open('GS_Browser.spec', 'w') as f:
        f.write(spec_content)

    # Run PyInstaller
    subprocess.run(['pyinstaller', 'GS_Browser.spec', '--clean'])

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
    datas=[],
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
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/assets/icon.png'
)
"""
    with open('GS_Browser.spec', 'w') as f:
        f.write(spec_content)

    # Run PyInstaller
    subprocess.run(['pyinstaller', 'GS_Browser.spec', '--clean'])

def create_installer_windows(version):
    print("Creating Windows installer...")
    # Create NSIS script
    nsis_script = f"""
!include "MUI2.nsh"

Name "GS Browser"
OutFile "GS_Browser_Setup_{version}.exe"
InstallDir "$PROGRAMFILES\\GS Browser"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "dist\\GS_Browser\\*.*"
    
    CreateDirectory "$SMPROGRAMS\\GS Browser"
    CreateShortcut "$SMPROGRAMS\\GS Browser\\GS Browser.lnk" "$INSTDIR\\GS_Browser.exe"
    CreateShortcut "$DESKTOP\\GS Browser.lnk" "$INSTDIR\\GS_Browser.exe"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "DisplayName" "GS Browser"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser" \
                     "UninstallString" "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    RMDir /r "$SMPROGRAMS\\GS Browser"
    Delete "$DESKTOP\\GS Browser.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\GSBrowser"
SectionEnd
"""
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)

    # Run NSIS compiler
    subprocess.run(['makensis', 'installer.nsi'])

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
        build_windows()
        create_installer_windows(version)
    elif platform.startswith('linux'):
        build_linux()
        create_installer_linux(version)
    else:
        print(f"Unsupported platform: {platform}")
        sys.exit(1)

if __name__ == '__main__':
    main() 