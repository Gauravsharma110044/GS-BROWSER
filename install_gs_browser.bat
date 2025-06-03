@echo off
echo Installing GS Browser...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.9 or later.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Create necessary directories
echo Creating directories...
mkdir adblock 2>nul
mkdir icons 2>nul
mkdir config 2>nul
mkdir tests 2>nul

:: Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\GS Browser.lnk'); $SC.TargetPath = '%~dp0venv\Scripts\pythonw.exe'; $SC.Arguments = 'gs_browser.py'; $SC.WorkingDirectory = '%~dp0'; $SC.IconLocation = '%~dp0icons\chrome.ico'; $SC.Save()"

echo Installation complete!
echo You can now run GS Browser by:
echo 1. Double-clicking the desktop shortcut
echo 2. Running 'python gs_browser.py' from the command line
pause 