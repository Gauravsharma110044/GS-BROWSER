from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class UserProfile(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Profile")
        layout = QVBoxLayout()
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setFixedSize(120, 120)
        self.avatar_label.setStyleSheet("border-radius: 60px; border: 2px solid #3b7ddd;")
        self.avatar_path = None
        avatar_btn = QPushButton("Change Avatar")
        avatar_btn.clicked.connect(self.change_avatar)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Your Name")
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setPlaceholderText("OpenAI API Key")
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        save_btn = QPushButton("Save Profile")
        save_btn.clicked.connect(self.save_profile)
        layout.addWidget(self.avatar_label)
        layout.addWidget(avatar_btn)
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("OpenAI API Key:"))
        layout.addWidget(self.api_key_edit)
        layout.addWidget(save_btn)
        layout.addStretch()
        self.setLayout(layout)
        self.load_profile()

    def change_avatar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Avatar", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.avatar_path = file_path
            pixmap = QPixmap(file_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.avatar_label.setPixmap(pixmap)

    def save_profile(self):
        profile = {
            'name': self.name_edit.text(),
            'api_key': self.api_key_edit.text(),
            'avatar': self.avatar_path or ''
        }
        with open('user_profile.cfg', 'w', encoding='utf-8') as f:
            for k, v in profile.items():
                f.write(f'{k}:{v}\n')

    def load_profile(self):
        if os.path.exists('user_profile.cfg'):
            with open('user_profile.cfg', 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('name:'):
                        self.name_edit.setText(line[5:].strip())
                    elif line.startswith('api_key:'):
                        self.api_key_edit.setText(line[8:].strip())
                    elif line.startswith('avatar:'):
                        avatar_path = line[7:].strip()
                        if avatar_path and os.path.exists(avatar_path):
                            self.avatar_path = avatar_path
                            pixmap = QPixmap(avatar_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            self.avatar_label.setPixmap(pixmap)
