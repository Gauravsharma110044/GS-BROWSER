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
- For support, open an issue or contact <https://github.com/yourusername/gemini-ai-app>

# GS Browser

A modern, AI-powered browser available both as a desktop application and web interface.

## Desktop Application

### Features
- AI-powered browsing experience
- Voice commands
- Smart tab management
- Dark/Light mode
- Enhanced security features
- Cross-platform support (Windows)

### Installation

1. Download the latest release from our [Releases](https://github.com/Gauravsharma110044/GS-BROWSER/releases) page
2. Run the installer
3. Follow the installation instructions

### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/Gauravsharma110044/GS-BROWSER.git
cd GS-BROWSER
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the application:
```bash
python build_app.py
```

The executable will be created in the `dist` directory.

## Website

Visit our [website](https://gsbrowser.vercel.app) to:
- Learn about features
- Download the latest version
- Get support
- View documentation

### Features
- Modern, responsive design
- Interactive AI assistant
- Voice command demo
- Smart tab management preview
- Dark/Light mode toggle

### Development

The website is built with:
- HTML5
- CSS3
- JavaScript
- Deployed on Vercel

To run locally:
1. Navigate to the website directory:
```bash
cd website
```

2. Open `index.html` in your browser

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please:
1. Check our [documentation](https://gsbrowser.vercel.app/docs)
2. Open an issue on GitHub
3. Contact us through our website

## Credits

Built with ❤️ by Gauravsharma110044
