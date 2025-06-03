@echo off
echo Creating GS Browser installer...

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    pip install pyinstaller
) else (
    call venv\Scripts\activate
)

REM Create the executable
pyinstaller --name="GS Browser" ^
            --windowed ^
            --icon=icons/chrome.ico ^
            --add-data "icons;icons" ^
            --add-data "config;config" ^
            --add-data "homepage.html;." ^
            --add-data "*.qss;." ^
            gs_browser.py

REM Create installer
iscc installer.nsi

echo Installation package created successfully!
echo You can find the installer in the Output directory.
pause 