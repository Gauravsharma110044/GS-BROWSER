import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import sys
from gs_browser import MainWindow

@pytest.fixture
def app():
    """Create a QApplication instance."""
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def main_window(app):
    """Create a MainWindow instance."""
    window = MainWindow()
    window.show()
    return window

def test_window_title(main_window):
    """Test if the window title is correct."""
    assert main_window.windowTitle() == "GS Browser"

def test_new_tab(main_window):
    """Test if new tab can be created."""
    initial_tab_count = main_window.tabs.count()
    main_window.new_tab()
    assert main_window.tabs.count() == initial_tab_count + 1

def test_close_tab(main_window):
    """Test if tab can be closed."""
    main_window.new_tab()
    initial_tab_count = main_window.tabs.count()
    main_window.close_tab(0)
    assert main_window.tabs.count() == initial_tab_count - 1

def test_navigation(main_window):
    """Test if navigation works."""
    url = "https://www.google.com"
    main_window.navigate_to_url(url)
    QTest.qWait(2000)  # Wait for page to load
    current_url = main_window.tabs.currentWidget().url().toString()
    assert "google.com" in current_url.lower() 