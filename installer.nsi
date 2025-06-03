!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "GS Browser"
OutFile "GS_Browser_Setup.exe"
InstallDir "$PROGRAMFILES\GS Browser"
RequestExecutionLevel admin

!define MUI_ABORTWARNING
!define MUI_ICON "icons\chrome.ico"
!define MUI_UNICON "icons\chrome.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    
    # Copy all files
    File /r "dist\GS Browser\*.*"
    
    # Create shortcuts
    CreateDirectory "$SMPROGRAMS\GS Browser"
    CreateShortcut "$SMPROGRAMS\GS Browser\GS Browser.lnk" "$INSTDIR\GS Browser.exe"
    CreateShortcut "$DESKTOP\GS Browser.lnk" "$INSTDIR\GS Browser.exe"
    
    # Write uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    # Add uninstall information to Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser" \
                     "DisplayName" "GS Browser"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser" \
                     "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser" \
                     "DisplayIcon" "$INSTDIR\GS Browser.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser" \
                     "Publisher" "Your Name"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser" \
                     "DisplayVersion" "1.0.0"
SectionEnd

Section "Uninstall"
    # Remove files
    RMDir /r "$INSTDIR"
    
    # Remove shortcuts
    Delete "$SMPROGRAMS\GS Browser\GS Browser.lnk"
    RMDir "$SMPROGRAMS\GS Browser"
    Delete "$DESKTOP\GS Browser.lnk"
    
    # Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\GS Browser"
SectionEnd 