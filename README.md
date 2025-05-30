# Gemini AI App

[![GitHub license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/yourusername/gemini-ai-app)
[![Free Software](https://img.shields.io/badge/free-100%25-brightgreen.svg)](https://github.com/yourusername/gemini-ai-app)

**This software is 100% free and open source. No ads, no trackers, no hidden costs.**


A modern AI application powered by Google Gemini. Use it for chat, explanations, quizzes, file assistance, and more—all in a single, easy-to-use app.

## Features

- Chat with Gemini AI
- Summarize text and documents
- Extract text from images (OCR)
- Voice commands and responses
- Save and manage chat history
- Multi-platform: Windows, Mac, Android, iOS

## Platform Support

### Windows & Mac (Desktop)

- Uses Python and PyQt5 for a native desktop experience.
- Fully cross-platform: just install Python 3 and dependencies.

### Android & iOS (Mobile)

- Uses Python and Kivy for a touch-friendly mobile app.
- Kivy app source: `kivy_app.py`
- You can build APKs (Android) or IPAs (iOS) using Kivy's tools.

## Setup

### 1. Install dependencies

```sh
pip install -r requirements.txt
```

For mobile: also install Kivy (`pip install kivy`)

### 2. Configure Gemini API key

Create a `.env` file in the project root with:

```env
GEMINI_API_KEY=your-gemini-key-here
```

## Running the App

### Desktop (Windows/Mac)

```sh
python ai_suite_main.py
```

### Mobile (Android/iOS)

```sh
python kivy_app.py
```

(See Kivy documentation for packaging as APK/IPA)

## Usage

- Interact with Gemini AI for chat, learning, and file help.
- All AI features use Google Gemini for responses.
- Ask questions, generate quizzes, analyze files, and more—all in one window.

## Customization

- Add more Gemini-powered features or UI improvements as you wish.
- The code is modular and ready for further development.

## Notes

- Your Gemini API key is kept private in `.env` and never shared.
- For best results, use an up-to-date Gemini API key and dependencies.
- For mobile builds, see <https://kivy.org/doc/stable/guide/packaging.html>
- For support, open an issue or contact <https://github.com/Gauravsharma110044/gemini-ai-app>

# GS Browser

A modern, AI-powered web browser built with Python and Kivy.

## Features

- **AI-Powered Browsing**: Get intelligent assistance while browsing
- **Modern Interface**: Clean and intuitive user interface
- **Smart Search**: Enhanced search capabilities
- **File Management**: Integrated file system access
- **Security**: Built-in ad blocker and privacy features

## Installation

1. Download the latest release from [GitHub Releases](https://github.com/Gauravsharma110044/GS-BROWSER/releases)
2. Extract the downloaded zip file
3. Run `GS_Browser_Setup.exe`
4. Follow the installation wizard

## Development

### Prerequisites

- Python 3.8 or later
- Git
- Windows 10 or later

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Gauravsharma110044/GS-BROWSER.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python kivy_app.py
   ```

## Project Structure

```
GS-BROWSER/
├── frontend/           # Frontend components
├── backend/           # Backend services
├── ai_writer/         # AI writing features
├── ai_assistant/      # AI assistant features
└── docs/             # Documentation
```

## Documentation

1. Check our [documentation](https://github.com/Gauravsharma110044/GS-BROWSER/docs)
2. Read the [installation guide](https://github.com/Gauravsharma110044/GS-BROWSER/docs/installation.md)
3. Learn about [AI features](https://github.com/Gauravsharma110044/GS-BROWSER/docs/ai-features.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- [GitHub Issues](https://github.com/Gauravsharma110044/GS-BROWSER/issues)
- [Documentation](https://github.com/Gauravsharma110044/GS-BROWSER/docs)
- [Community Forum](https://github.com/Gauravsharma110044/GS-BROWSER/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Built with ❤️ by Gauravsharma110044
