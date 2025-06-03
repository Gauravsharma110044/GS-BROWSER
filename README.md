# GS Browser

A modern web browser built with Python and PyQt5, featuring advanced ad-blocking capabilities.

## Features

- **Advanced Ad-Blocking**
  - Blocks ads on YouTube, Facebook, Twitter, and other popular sites
  - Uses EasyList filters for comprehensive ad blocking
  - CSS injection for hiding ad elements
  - Blocks tracking scripts and malware domains

- **Modern UI**
  - Clean and intuitive interface
  - Tab management
  - Bookmarks
  - History tracking
  - Developer tools

- **Security Features**
  - SSL/TLS support
  - Privacy protection
  - Safe browsing

## Installation

### Windows

1. **Prerequisites**
   - Python 3.9 or later
   - Git (optional, for development)

2. **Quick Install**
   - Download the latest release
   - Run `install_gs_browser.bat`
   - Follow the on-screen instructions

3. **Manual Install**
   ```bash
   # Clone the repository
   git clone https://github.com/Gauravsharma110044/GS-BROWSER.git
   cd GS-BROWSER

   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the browser
   python gs_browser.py
   ```

### Linux

1. **Prerequisites**
   ```bash
   sudo apt-get update
   sudo apt-get install python3-venv python3-pip
   ```

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/Gauravsharma110044/GS-BROWSER.git
   cd GS-BROWSER

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the browser
   python gs_browser.py
   ```

## Usage

1. **Starting the Browser**
   - Double-click the desktop shortcut (Windows)
   - Run `python gs_browser.py` from the command line

2. **Ad-Blocking**
   - Works automatically on supported sites
   - Toggle ad-blocking on/off using the shield icon in the toolbar
   - Green shield: Ad-blocking enabled
   - Gray shield: Ad-blocking disabled
   - Changes apply to all open tabs

3. **Keyboard Shortcuts**
   - `Ctrl+T`: New tab
   - `Ctrl+W`: Close tab
   - `Ctrl+N`: New window
   - `Ctrl+Shift+N`: Incognito window
   - `Ctrl+F`: Find text
   - `Ctrl++`: Zoom in
   - `Ctrl+-`: Zoom out
   - `Ctrl+0`: Reset zoom

## Development

1. **Running Tests**
   ```bash
   pytest tests/
   ```

2. **Code Style**
   ```bash
   black .
   flake8
   mypy .
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Project Structure

```
GS-BROWSER/
├── frontend/           # Frontend components
├── backend/           # Backend services
└── docs/             # Documentation
```

## Documentation

1. Check our [documentation](https://github.com/Gauravsharma110044/gs-browser/docs)
2. Read the [installation guide](https://github.com/Gauravsharma110044/gs-browser/docs/installation.md)

## Credits

Built with ❤️ by [Gaurav Sharma](https://github.com/Gauravsharma110044)
