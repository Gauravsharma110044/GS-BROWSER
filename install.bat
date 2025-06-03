@echo off
echo GS Browser Installation
echo =====================

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Please run this installer as Administrator
    pause
    exit /b 1
)

:: Set installation directory
set INSTALL_DIR=%ProgramFiles%\GS Browser

:: Create installation directory
echo Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy files
echo Copying files...
xcopy /E /I /Y "dist\GS_Browser\*" "%INSTALL_DIR%"

:: Create shortcuts
echo Creating shortcuts...
set START_MENU_DIR=%ProgramData%\Microsoft\Windows\Start Menu\Programs\GS Browser
if not exist "%START_MENU_DIR%" mkdir "%START_MENU_DIR%"

:: Create desktop shortcut
powershell "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%USERPROFILE%\Desktop\GS Browser.lnk'); $SC.TargetPath = '%INSTALL_DIR%\GS_Browser.exe'; $SC.Save()"

:: Create start menu shortcut
powershell "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%START_MENU_DIR%\GS Browser.lnk'); $SC.TargetPath = '%INSTALL_DIR%\GS_Browser.exe'; $SC.Save()"

:: Add to PATH
setx PATH "%PATH%;%INSTALL_DIR%" /M

:: Create uninstaller
echo Creating uninstaller...
echo @echo off > "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstalling GS Browser... >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /S /Q "%INSTALL_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo rmdir /S /Q "%START_MENU_DIR%" >> "%INSTALL_DIR%\uninstall.bat"
echo del "%USERPROFILE%\Desktop\GS Browser.lnk" >> "%INSTALL_DIR%\uninstall.bat"
echo echo Uninstallation complete. >> "%INSTALL_DIR%\uninstall.bat"
echo pause >> "%INSTALL_DIR%\uninstall.bat"

:: Add to Add/Remove Programs
echo Adding to Add/Remove Programs...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GSBrowser" /v "DisplayName" /t REG_SZ /d "GS Browser" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GSBrowser" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GSBrowser" /v "DisplayIcon" /t REG_SZ /d "%INSTALL_DIR%\GS_Browser.exe" /f
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\GSBrowser" /v "Publisher" /t REG_SZ /d "GS Browser Team" /f

:: Run verification with repair mode
echo Running installation verification...
python "%INSTALL_DIR%\verify_installation.py" --repair
if %errorLevel% neq 0 (
    echo.
    echo Installation verification failed!
    echo Please check the logs in %INSTALL_DIR%\logs for details.
    echo.
    echo Would you like to:
    echo 1. View the logs
    echo 2. Try repairing again
    echo 3. Exit
    set /p choice="Enter your choice (1-3): "
    
    if "%choice%"=="1" (
        start "" "%INSTALL_DIR%\logs"
    ) else if "%choice%"=="2" (
        python "%INSTALL_DIR%\verify_installation.py" --repair
    ) else (
        exit /b 1
    )
)

echo.
echo Installation complete!
echo You can now run GS Browser from the desktop shortcut or start menu.
pause 