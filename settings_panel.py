from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt5.QtCore import Qt

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings & Preferences"))
        # Theme toggle
        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)
        # Placeholder for more settings
        layout.addStretch()
        self.setLayout(layout)
