#!/bin/bash

echo "Installing GS Browser..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed! Please install Python 3.9 or later."
    echo "On Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p adblock icons config tests extensions bookmarks history downloads cache screenshots

# Create config files
echo "Creating configuration files..."
if [ ! -f config/settings.json ]; then
    echo '{"theme": "light", "homepage": "homepage.html", "search_engine": "google"}' > config/settings.json
fi

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/GS\ Browser.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=GS Browser
Comment=Modern web browser with ad-blocking
Exec=$(pwd)/venv/bin/python $(pwd)/gs_browser.py
Icon=$(pwd)/icons/chrome.ico
Terminal=false
Categories=Network;WebBrowser;
EOL

chmod +x ~/Desktop/GS\ Browser.desktop

# Create application menu entry
echo "Creating application menu entry..."
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/gs-browser.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=GS Browser
Comment=Modern web browser with ad-blocking
Exec=$(pwd)/venv/bin/python $(pwd)/gs_browser.py
Icon=$(pwd)/icons/chrome.ico
Terminal=false
Categories=Network;WebBrowser;
EOL

echo "Installation complete!"
echo "You can now run GS Browser by:"
echo "1. Double-clicking the desktop shortcut"
echo "2. Running 'python gs_browser.py' from the command line"
echo
echo "Features installed:"
echo "- Advanced ad-blocking with toggle"
echo "- Google account integration"
echo "- Bookmarks and history sync"
echo "- Developer tools"
echo "- Extensions support"
echo "- Security features" 