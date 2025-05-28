import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QSplashScreen, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from ai_assistant import AIAssistant
from file_assistant import FileAssistant
from voice_assistant import VoiceAssistant
from image_ocr import ImageOCR
from settings_panel import Settings
from app_utils import show_info, show_error, show_loading

class WebSearch(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Web Search (Coming Soon): Fetch live info from the internet."))
        self.setLayout(layout)

class Organizer(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Organizer (Coming Soon): Notes, calendar, reminders."))
        self.setLayout(layout)

class Automation(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Automation (Coming Soon): Email, file management, app launching."))
        self.setLayout(layout)

class Plugins(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Plugins (Coming Soon): Add new features easily."))
        self.setLayout(layout)

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings (Coming Soon): Preferences, themes, API keys."))
        self.setLayout(layout)

class AISuiteMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Desktop Suite")
        self.setGeometry(100, 100, 1100, 800)
        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setIconSize(QSize(32, 32))
        self.sidebar.setFixedWidth(160)
        from user_profile import UserProfile
        from ai_tutor import AITutor
        sidebar_items = [
            ("User Profile", "👤"),
            ("AI Tutor", "🎓"),
            ("AI Chat", "💬"),
            ("File Assistant", "📄"),
            ("Image & OCR", "🖼️"),
            ("Voice Assistant", "🎤"),
            ("Web Search", "🌐"),
            ("Organizer", "🗓️"),
            ("Automation", "⚙️"),
            ("Plugins", "🧩"),
            ("Settings", "⚙️")
        ]
        for name, emoji in sidebar_items:
            item = QListWidgetItem(f"{emoji}  {name}")
            self.sidebar.addItem(item)
        # Stacked widget for pages
        # Robust widget loader for main modules
        def safe_widget(widget_cls, name):
            try:
                return widget_cls()
            except Exception as e:
                w = QWidget()
                layout = QVBoxLayout()
                layout.addWidget(QLabel(f"{name} failed to load: {e}"))
                w.setLayout(layout)
                return w
        self.pages = QStackedWidget()
        self.pages.addWidget(safe_widget(UserProfile, 'User Profile'))
        self.pages.addWidget(safe_widget(AITutor, 'AI Tutor'))
        self.pages.addWidget(safe_widget(AIAssistant, 'AI Chat'))
        self.pages.addWidget(safe_widget(FileAssistant, 'File Assistant'))
        self.pages.addWidget(safe_widget(ImageOCR, 'Image & OCR'))
        self.pages.addWidget(safe_widget(VoiceAssistant, 'Voice Assistant'))
        self.pages.addWidget(WebSearch())
        self.pages.addWidget(Organizer())
        self.pages.addWidget(Automation())
        self.pages.addWidget(Plugins())
        self.pages.addWidget(safe_widget(Settings, 'Settings'))
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        # Load stylesheet (default to dark)
        self.current_theme = "dark"
        self.load_theme(self.current_theme)
        # Connect theme toggle in settings
        settings_page = self.pages.widget(10)
        if hasattr(settings_page, 'theme_combo'):
            settings_page.theme_combo.currentTextChanged.connect(self.on_theme_changed)
    def load_theme(self, theme):
        qss_file = "style.qss" if theme == "dark" else "style_light.qss"
        try:
            with open(qss_file, "r") as f:
                self.setStyleSheet(f.read())
        except Exception:
            pass
    def on_theme_changed(self, theme):
        self.current_theme = theme.lower()
        self.load_theme(self.current_theme)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Modern splash screen
    splash = QSplashScreen(QPixmap(), Qt.WindowStaysOnTopHint)
    splash.showMessage("Launching AI Desktop Suite...", Qt.AlignCenter | Qt.AlignBottom, Qt.white)
    splash.show()
    app.processEvents()
    time.sleep(1.2)
    window = AISuiteMain()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
