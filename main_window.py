from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QToolBar, QAction, 
                             QLineEdit, QProgressBar, QStatusBar, QMenu, QMessageBox,
                             QDialog, QVBoxLayout, QLabel, QPushButton, QInputDialog,
                             QShortcut, QMenuBar, QFileDialog, QSystemTrayIcon,
                             QDockWidget, QTreeWidget, QTreeWidgetItem, QSplitter,
                             QWidget, QHBoxLayout, QFrame, QWidgetAction)
from PyQt5.QtCore import Qt, QUrl, QSize, QSettings, QTimer, QPoint
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEnginePage, QWebEngineProfile,
                                     QWebEngineDownloadItem, QWebEngineScript,
                                     QWebEngineSettings, QWebEngineScriptCollection)
from PyQt5.QtGui import QIcon, QKeySequence, QDesktopServices, QPixmap, QPainter, QColor, QFont
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from local_database import LocalDatabase
import os
import json
import hashlib
import base64
from datetime import datetime
import webbrowser
import requests
from urllib.parse import urlencode
import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
from adblock.adblock import AdBlocker

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/oauth2callback'):
            # Extract the authorization code from the URL
            query_components = dict(q.split('=') for q in self.path.split('?')[1].split('&'))
            if 'code' in query_components:
                self.server.auth_code = query_components['code']
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authentication successful! You can close this window.")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authentication failed! No authorization code received.")
        else:
            self.send_response(404)
            self.end_headers()

class OAuthCallbackServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_code = None

class GoogleAuth:
    def __init__(self):
        self.SCOPES = [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'
        ]
        self.credentials = None
        self.user_info = None
        self.load_credentials()

    def load_credentials(self):
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.credentials = pickle.load(token)
        except Exception as e:
            print(f"Error loading credentials: {e}")

    def save_credentials(self):
        try:
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)
        except Exception as e:
            print(f"Error saving credentials: {e}")

    def get_auth_url(self):
        try:
            # Load client configuration
            with open('config/google_oauth.json', 'r') as f:
                client_config = json.load(f)

            # Create flow instance
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config,
                scopes=self.SCOPES,
                redirect_uri=client_config['web']['redirect_uris'][0]
            )

            # Generate authorization URL
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                prompt='consent'
            )
            return auth_url
        except Exception as e:
            print(f"Error generating auth URL: {e}")
            return None

    def get_token(self, code):
        try:
            # Load client configuration
            with open('config/google_oauth.json', 'r') as f:
                client_config = json.load(f)

            # Create flow instance
            flow = google_auth_oauthlib.flow.Flow.from_client_config(
                client_config,
                scopes=self.SCOPES,
                redirect_uri=client_config['web']['redirect_uris'][0]
            )

            # Exchange authorization code for credentials
            flow.fetch_token(code=code)
            self.credentials = flow.credentials
            self.save_credentials()
            return True
        except Exception as e:
            print(f"Error getting token: {e}")
            return False

    def get_user_info(self):
        try:
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                    self.save_credentials()
                else:
                    return None

            # Build the service
            service = build('oauth2', 'v2', credentials=self.credentials)
            
            # Get user info
            user_info = service.userinfo().get().execute()
            self.user_info = user_info
            return user_info
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None

    def start_callback_server(self):
        try:
            # Create server
            server = OAuthCallbackServer(('localhost', 8080), OAuthCallbackHandler)
            
            # Start server in a separate thread
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            return server
        except Exception as e:
            print(f"Error starting callback server: {e}")
            return None

    def wait_for_callback(self, server, timeout=60):
        try:
            start_time = datetime.now()
            while not server.auth_code:
                if (datetime.now() - start_time).seconds > timeout:
                    return None
                QTimer.singleShot(100, lambda: None)  # Keep Qt event loop running
            
            return server.auth_code
        except Exception as e:
            print(f"Error waiting for callback: {e}")
            return None
        finally:
            server.shutdown()

class DeveloperTools(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Developer Tools", parent)
        self.setup_ui()

    def setup_ui(self):
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        # Create main widget
        main_widget = QTreeWidget()
        main_widget.setHeaderLabels(["Element", "Value"])
        
        # Add elements
        elements = [
            ("Console", "View console output"),
            ("Elements", "Inspect DOM elements"),
            ("Network", "Monitor network requests"),
            ("Sources", "Debug JavaScript"),
            ("Performance", "Analyze performance"),
            ("Memory", "Memory usage"),
            ("Application", "Storage and cache"),
            ("Security", "Security information")
        ]
        
        for element, value in elements:
            item = QTreeWidgetItem([element, value])
            main_widget.addTopLevelItem(item)
        
        self.setWidget(main_widget)

class ExtensionsManager:
    def __init__(self, parent):
        self.parent = parent
        self.extensions = {}
        self.load_extensions()

    def load_extensions(self):
        # Load extensions from extensions directory
        extensions_dir = "extensions"
        if os.path.exists(extensions_dir):
            for ext_id in os.listdir(extensions_dir):
                manifest_path = os.path.join(extensions_dir, ext_id, "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as f:
                        manifest = json.load(f)
                        self.extensions[ext_id] = manifest

    def inject_extension(self, browser, ext_id):
        if ext_id in self.extensions:
            ext = self.extensions[ext_id]
            # Inject extension scripts
            for script in ext.get('content_scripts', []):
                for js_file in script.get('js', []):
                    script = QWebEngineScript()
                    script.setSourceCode(open(js_file, 'r').read())
                    script.setInjectionPoint(QWebEngineScript.DocumentCreation)
                    script.setWorldId(QWebEngineScript.MainWorld)
                    browser.page().scripts().insert(script)

class SyncManager:
    def __init__(self, parent):
        self.parent = parent
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_data)
        self.sync_timer.start(300000)  # Sync every 5 minutes

    def sync_data(self):
        # Sync bookmarks
        self.sync_bookmarks()
        # Sync history
        self.sync_history()
        # Sync settings
        self.sync_settings()
        # Sync extensions
        self.sync_extensions()

    def sync_bookmarks(self):
        # Implement bookmark sync
        pass

    def sync_history(self):
        # Implement history sync
        pass

    def sync_settings(self):
        # Implement settings sync
        pass

    def sync_extensions(self):
        # Implement extension sync
        pass

class ProfileButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(32, 32)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 16px;
                background-color: #303134;
            }
            QPushButton:hover {
                background-color: #3c4043;
            }
        """)
        self.setIcon(QIcon("icons/profile.png"))
        self.setIconSize(QSize(24, 24))
        self.setToolTip("Sign in to Chrome")
        
        # Create profile menu
        self.profile_menu = QMenu(self)
        self.setMenu(self.profile_menu)
        
        # Add profile actions
        self.setup_profile_menu()
        
        # Track sign-in state
        self.is_signed_in = False
        self.current_user = None

    def setup_profile_menu(self):
        # Add profile section
        profile_section = QWidget()
        profile_layout = QVBoxLayout(profile_section)
        
        # Profile picture
        profile_pic = QLabel()
        profile_pic.setFixedSize(64, 64)
        profile_pic.setStyleSheet("""
            QLabel {
                background-color: #303134;
                border-radius: 32px;
            }
        """)
        profile_pic.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(profile_pic, alignment=Qt.AlignCenter)
        
        # Profile name
        profile_name = QLabel("Sign in to Chrome")
        profile_name.setStyleSheet("color: #e8eaed; font-size: 14px;")
        profile_name.setAlignment(Qt.AlignCenter)
        profile_layout.addWidget(profile_name)
        
        # Profile email
        profile_email = QLabel("to sync your bookmarks, history, and more")
        profile_email.setStyleSheet("color: #9aa0a6; font-size: 12px;")
        profile_email.setAlignment(Qt.AlignCenter)
        profile_email.setWordWrap(True)
        profile_layout.addWidget(profile_email)
        
        # Add profile section to menu
        profile_action = QWidgetAction(self.profile_menu)
        profile_action.setDefaultWidget(profile_section)
        self.profile_menu.addAction(profile_action)
        
        # Add separator
        self.profile_menu.addSeparator()
        
        # Add sign in button
        sign_in_action = QAction("Sign in to Chrome", self)
        sign_in_action.triggered.connect(self.show_sign_in_dialog)
        self.profile_menu.addAction(sign_in_action)
        
        # Add other options
        other_options = [
            ("Other Chrome profile", self.add_profile),
            ("Guest", self.use_guest_profile),
            ("Add person", self.add_person)
        ]
        
        for text, slot in other_options:
            action = QAction(text, self)
            action.triggered.connect(slot)
            self.profile_menu.addAction(action)
        
        # Add separator
        self.profile_menu.addSeparator()
        
        # Add settings
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        self.profile_menu.addAction(settings_action)
        
        # Add help
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.show_help)
        self.profile_menu.addAction(help_action)

    def show_sign_in_dialog(self):
        dialog = AuthDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.is_signed_in = True
            self.current_user = dialog.get_user()
            self.update_profile_menu()

    def update_profile_menu(self):
        if self.is_signed_in and self.current_user:
            # Update profile picture
            profile_pic = self.profile_menu.actions()[0].defaultWidget().findChild(QLabel)
            if profile_pic and self.current_user.get('profile_pic'):
                # Load profile picture from URL
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(self.current_user['profile_pic']).content)
                profile_pic.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                profile_pic.setStyleSheet("""
                    QLabel {
                        background-color: #303134;
                        border-radius: 32px;
                        border: 2px solid #8ab4f8;
                    }
                """)
            
            # Update profile name
            profile_name = self.profile_menu.actions()[0].defaultWidget().findChildren(QLabel)[1]
            if profile_name:
                profile_name.setText(self.current_user.get('name', 'User'))
            
            # Update profile email
            profile_email = self.profile_menu.actions()[0].defaultWidget().findChildren(QLabel)[2]
            if profile_email:
                profile_email.setText(self.current_user.get('email', ''))
            
            # Update sign in action
            sign_in_action = self.profile_menu.actions()[2]
            sign_in_action.setText("Sign out")
            sign_in_action.triggered.disconnect()
            sign_in_action.triggered.connect(self.sign_out)

    def sign_out(self):
        self.is_signed_in = False
        self.current_user = None
        self.setup_profile_menu()

    def add_profile(self):
        # Implement add profile functionality
        pass

    def use_guest_profile(self):
        # Implement guest profile functionality
        pass

    def add_person(self):
        # Implement add person functionality
        pass

    def show_settings(self):
        # Implement settings dialog
        pass

    def show_help(self):
        # Implement help dialog
        pass

class AuthDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign in to Chrome")
        self.setup_ui()
        self.user = None
        self.google_auth = GoogleAuth()

    def setup_ui(self):
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #202124;
                color: #e8eaed;
            }
            QLabel {
                color: #e8eaed;
            }
            QPushButton {
                padding: 10px;
                background-color: #8ab4f8;
                color: #202124;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #93bbf9;
            }
        """)

        layout = QVBoxLayout()
        
        # Chrome logo
        logo = QLabel()
        logo.setPixmap(QPixmap("icons/chrome.png").scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # Title
        title = QLabel("Sign in to Chrome")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("to sync your bookmarks, history, and more")
        subtitle.setStyleSheet("color: #9aa0a6;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Google Sign In button
        google_sign_in = QPushButton("Sign in with Google")
        google_sign_in.setIcon(QIcon("icons/google.png"))
        google_sign_in.setIconSize(QSize(24, 24))
        google_sign_in.clicked.connect(self.sign_in_with_google)
        layout.addWidget(google_sign_in)
        
        # Other options
        other_options = [
            ("Use as Guest", self.use_guest),
            ("Add another account", self.add_account)
        ]
        
        for text, slot in other_options:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background: none;
                    color: #8ab4f8;
                    text-align: left;
                    padding: 5px;
                }
                QPushButton:hover {
                    background: none;
                    color: #93bbf9;
                }
            """)
            btn.clicked.connect(slot)
            layout.addWidget(btn)
        
        self.setLayout(layout)

    def sign_in_with_google(self):
        try:
            # Get authorization URL
            auth_url = self.google_auth.get_auth_url()
            if not auth_url:
                QMessageBox.critical(self, "Error", "Failed to generate authorization URL")
                return

            # Start callback server
            server = self.google_auth.start_callback_server()
            if not server:
                QMessageBox.critical(self, "Error", "Failed to start callback server")
                return

            # Open browser
            webbrowser.open(auth_url)

            # Wait for callback
            code = self.google_auth.wait_for_callback(server)
            if not code:
                QMessageBox.critical(self, "Error", "Authentication timed out")
                return

            # Get token
            if not self.google_auth.get_token(code):
                QMessageBox.critical(self, "Error", "Failed to get access token")
                return

            # Get user info
            user_info = self.google_auth.get_user_info()
            if not user_info:
                QMessageBox.critical(self, "Error", "Failed to get user information")
                return

            self.user = {
                'email': user_info['email'],
                'name': user_info['name'],
                'profile_pic': user_info.get('picture')
            }
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Authentication failed: {str(e)}")

    def use_guest(self):
        self.user = {
            'email': 'guest',
            'name': 'Guest',
            'profile_pic': None
        }
        self.accept()

    def add_account(self):
        # Open Google OAuth page for adding another account
        auth_url = self.google_auth.get_auth_url() + "&prompt=select_account"
        webbrowser.open(auth_url)
        
        code = self.wait_for_oauth_callback()
        if code and self.google_auth.get_token(code):
            user_info = self.google_auth.get_user_info()
            if user_info:
                self.user = {
                    'email': user_info['email'],
                    'name': user_info['name'],
                    'profile_pic': user_info.get('picture')
                }
                self.accept()

    def get_user(self):
        return self.user

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = LocalDatabase()
        # Initialize advanced features BEFORE setup_ui
        self.extensions_manager = ExtensionsManager(self)
        self.sync_manager = SyncManager(self)
        self.developer_tools = DeveloperTools(self)
        self.setup_ui()
        self.load_settings()
        self.setup_shortcuts()
        self.setup_menu()
        # Setup security features
        self.setup_security()
        # Setup performance monitoring
        self.setup_performance_monitoring()
        
        # Initialize ad blocker
        self.ad_blocker = AdBlocker(self)

    def setup_ui(self):
        # Set window properties
        self.setWindowTitle("GS Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Create toolbar
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # Navigation buttons
        back_btn = QAction(QIcon("icons/back.png"), "Back", self)
        back_btn.triggered.connect(lambda: self.current_tab().back())
        self.toolbar.addAction(back_btn)

        forward_btn = QAction(QIcon("icons/forward.png"), "Forward", self)
        forward_btn.triggered.connect(lambda: self.current_tab().forward())
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction(QIcon("icons/reload.png"), "Reload", self)
        reload_btn.triggered.connect(lambda: self.current_tab().reload())
        self.toolbar.addAction(reload_btn)

        home_btn = QAction(QIcon("icons/home.png"), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        self.toolbar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Bookmark button
        bookmark_btn = QAction(QIcon("icons/bookmark.png"), "Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        self.toolbar.addAction(bookmark_btn)

        # Add new tab button
        new_tab_btn = QAction(QIcon("icons/new_tab.png"), "New Tab", self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(new_tab_btn)

        # Add profile button to the right of the toolbar
        self.profile_button = ProfileButton(self)
        self.toolbar.addWidget(self.profile_button)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Add first tab
        self.add_new_tab()

    def setup_shortcuts(self):
        # New tab
        QShortcut(QKeySequence("Ctrl+T"), self, self.add_new_tab)
        
        # Close tab
        QShortcut(QKeySequence("Ctrl+W"), self, lambda: self.close_tab(self.tabs.currentIndex()))
        
        # New window
        QShortcut(QKeySequence("Ctrl+N"), self, self.new_window)
        
        # Incognito window
        QShortcut(QKeySequence("Ctrl+Shift+N"), self, self.new_incognito_window)
        
        # Find
        QShortcut(QKeySequence("Ctrl+F"), self, self.find_text)
        
        # Zoom in/out
        QShortcut(QKeySequence("Ctrl++"), self, lambda: self.current_tab().setZoomFactor(self.current_tab().zoomFactor() + 0.1))
        QShortcut(QKeySequence("Ctrl+-"), self, lambda: self.current_tab().setZoomFactor(self.current_tab().zoomFactor() - 0.1))
        QShortcut(QKeySequence("Ctrl+0"), self, lambda: self.current_tab().setZoomFactor(1.0))

    def show_auth_dialog(self):
        dialog = AuthDialog(self)
        dialog.exec_()

    def current_tab(self):
        return self.tabs.currentWidget()

    def add_new_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        
        # Apply ad blocker to the new tab
        browser.page().profile().setUrlRequestInterceptor(self.ad_blocker)
        
        # Inject ad-blocking CSS for popular sites
        def inject_cosmetic_script():
            script = AdBlocker.get_cosmetic_script_for_url(browser.url().toString())
            if script:
                browser.page().scripts().insert(script)
        browser.urlChanged.connect(lambda url: inject_cosmetic_script())
        inject_cosmetic_script()
        
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda qurl, browser=browser: 
            self.update_urlbar(qurl, browser))
        
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
            self.tabs.setTabText(i, browser.page().title()))
        
        return browser

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.current_tab().setUrl(q)

    def navigate_home(self):
        # Use the local homepage
        self.current_tab().setUrl(QUrl.fromLocalFile(os.path.abspath("homepage.html")))

    def update_urlbar(self, q, browser=None):
        if browser != self.current_tab():
            return
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        if progress == 100:
            self.progress_bar.hide()
        else:
            self.progress_bar.show()

    def add_bookmark(self):
        current = self.current_tab()
        url = current.url().toString()
        title = current.page().title()
        
        if self.db.add_bookmark(title, url):
            QMessageBox.information(self, "Bookmark Added", 
                f"Added bookmark: {title}")
        else:
            QMessageBox.warning(self, "Error", 
                "Failed to add bookmark")

    def new_window(self):
        window = MainWindow()
        window.show()

    def new_incognito_window(self):
        window = MainWindow()
        # Set incognito mode
        profile = QWebEngineProfile("Incognito")
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        window.show()

    def find_text(self):
        # Implement find functionality
        pass

    def load_settings(self):
        # Load theme
        theme = self.db.get_setting('theme', 'light')
        self.apply_theme(theme)
        
        # Load other settings
        self.homepage = self.db.get_setting('homepage', 'homepage.html')
        self.search_engine = self.db.get_setting('search_engine', 'google')

    def apply_theme(self, theme):
        if theme == 'dark':
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #232629;
                    color: #f3f6fb;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                    background-color: #232629;
                }
                QTabBar::tab {
                    background-color: #2c2f34;
                    color: #f3f6fb;
                    border: 1px solid #444;
                    padding: 8px 12px;
                }
                QTabBar::tab:selected {
                    background-color: #3b7ddd;
                }
                QLineEdit {
                    background-color: #2c2f34;
                    color: #f3f6fb;
                    border: 1px solid #444;
                    padding: 5px;
                }
                QToolBar {
                    background-color: #232629;
                    border: none;
                }
                QStatusBar {
                    background-color: #232629;
                    color: #f3f6fb;
                }
            """)
        else:
            self.setStyleSheet("") 

    def setup_security(self):
        # Enable security features
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, False)
        settings.setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)

    def setup_performance_monitoring(self):
        self.performance_timer = QTimer()
        self.performance_timer.timeout.connect(self.check_performance)
        self.performance_timer.start(5000)  # Check every 5 seconds

    def check_performance(self):
        # Monitor memory usage
        memory_usage = self.current_tab().page().profile().httpCacheMaximumSize()
        
        # Monitor CPU usage
        # This would require platform-specific code
        
        # Monitor network usage
        # This would require network monitoring code
        
        # If performance is poor, show warning
        if memory_usage > 1000000000:  # 1GB
            QMessageBox.warning(self, "Performance Warning",
                "High memory usage detected. Consider closing some tabs.")

    def setup_menu(self):
        menubar = self.menuBar()
        
        # Add Developer Tools menu
        dev_menu = menubar.addMenu("Developer")
        
        inspect_action = QAction("Inspect Element", self)
        inspect_action.setShortcut("Ctrl+Shift+I")
        inspect_action.triggered.connect(self.toggle_developer_tools)
        dev_menu.addAction(inspect_action)
        
        console_action = QAction("JavaScript Console", self)
        console_action.setShortcut("Ctrl+Shift+J")
        console_action.triggered.connect(self.show_console)
        dev_menu.addAction(console_action)
        
        # Add Extensions menu
        extensions_menu = menubar.addMenu("Extensions")
        
        manage_extensions_action = QAction("Manage Extensions", self)
        manage_extensions_action.triggered.connect(self.manage_extensions)
        extensions_menu.addAction(manage_extensions_action)
        
        # Add Sync menu
        sync_menu = menubar.addMenu("Sync")
        
        sync_now_action = QAction("Sync Now", self)
        sync_now_action.triggered.connect(self.sync_manager.sync_data)
        sync_menu.addAction(sync_now_action)
        
        sync_settings_action = QAction("Sync Settings", self)
        sync_settings_action.triggered.connect(self.show_sync_settings)
        sync_menu.addAction(sync_settings_action)

    def toggle_developer_tools(self):
        if self.developer_tools.isVisible():
            self.developer_tools.hide()
        else:
            self.developer_tools.show()

    def show_console(self):
        # Implement JavaScript console
        pass

    def manage_extensions(self):
        # Implement extension management dialog
        pass

    def show_sync_settings(self):
        # Implement sync settings dialog
        pass

    def handle_ssl_errors(self, reply, errors):
        # Handle SSL certificate errors
        if reply.url().scheme() == "https":
            # Check if the certificate is valid
            cert = reply.sslConfiguration().peerCertificate()
            if cert.isValid():
                reply.ignoreSslErrors()
            else:
                QMessageBox.warning(self, "SSL Error",
                    "The SSL certificate is not valid. Do you want to proceed anyway?",
                    QMessageBox.Yes | QMessageBox.No)
                if QMessageBox.Yes:
                    reply.ignoreSslErrors()
                else:
                    reply.abort()

    def handle_permission_request(self, permission):
        # Handle permission requests (geolocation, notifications, etc.)
        if permission == QWebEnginePage.Geolocation:
            reply = QMessageBox.question(self, "Permission Request",
                "Allow this website to access your location?",
                QMessageBox.Yes | QMessageBox.No)
            return reply == QMessageBox.Yes
        return False

    def handle_authentication(self, url, auth, is_proxy):
        # Handle HTTP authentication
        if not is_proxy:
            username, ok = QInputDialog.getText(self, "Authentication Required",
                f"Enter username for {url.host()}:")
            if ok and username:
                password, ok = QInputDialog.getText(self, "Authentication Required",
                    "Enter password:", QLineEdit.Password)
                if ok and password:
                    auth.setUser(username)
                    auth.setPassword(password)
                    return True
        return False

    # ... (rest of the existing methods remain unchanged) 