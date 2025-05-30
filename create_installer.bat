@echo off
echo Creating GS Browser Installer...

:: Create dist directory if it doesn't exist
if not exist "dist" mkdir dist

:: Copy necessary files
echo Copying files...
copy kivy_app.py dist\
copy requirements.txt dist\
copy run_browser.bat dist\

:: Create a simple README
echo Creating README...
echo GS Browser > dist\README.txt
echo ========== >> dist\README.txt
echo. >> dist\README.txt
echo Installation: >> dist\README.txt
echo 1. Install Python 3.8 or higher >> dist\README.txt
echo 2. Run: pip install -r requirements.txt >> dist\README.txt
echo 3. Double-click run_browser.bat to start >> dist\README.txt

:: Create ZIP file
echo Creating ZIP file...
powershell Compress-Archive -Path dist\* -DestinationPath GS_Browser_Setup.zip -Force

echo Done! Your installer is ready: GS_Browser_Setup.zip 