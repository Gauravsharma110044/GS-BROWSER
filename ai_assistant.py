import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QHBoxLayout)
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract
import google.generativeai as genai
from dotenv import load_dotenv

class AIAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant")
        self.setGeometry(100, 100, 600, 600)
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.handle_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_input)
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        self.status_label = QLabel("")


        self.save_button = QPushButton("Save Chat History")
        self.save_button.clicked.connect(self.save_chat)
        self.load_button = QPushButton("Load Chat History")
        self.load_button.clicked.connect(self.load_chat)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)

        layout.addWidget(QLabel("AI Assistant Chat (Gemini)"))
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_line)
        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def handle_input(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
        if not hasattr(self, 'chat_history'):
            self.chat_history = []
        self.chat_display.append(f"You: {user_text}")
        self.chat_history.append({"role": "user", "content": user_text})
        self.input_line.clear()
        self.status_label.setText("Thinking...")
        QApplication.processEvents()
        try:
            model = genai.GenerativeModel('gemini-pro')
            convo = model.start_chat(history=[{"role": msg["role"], "parts": [msg["content"]]} for msg in self.chat_history])
            convo.send_message(user_text)
            reply = convo.last.text.strip()
            self.chat_display.append(f"Gemini: {reply}\n")
            self.chat_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            self.chat_display.append(f"[Error] {e}\n")
        self.status_label.setText("")

    def save_chat(self):
        if not self.chat_history:
            notify_error(self, "No chat to save.")
            return
        filename = save_history("chat", self.chat_history)
        notify_success(self, f"Chat history saved as {filename}")

    def load_chat(self):
        files = list_history("chat")
        if not files:
            notify_info(self, "No chat history found.")
            return
        # Simple file picker
        file, ok = QFileDialog.getOpenFileName(self, "Select Chat History", "history", "*.json")
        if file:
            try:
                history = load_history(os.path.basename(file))
                self.chat_history = history
                self.chat_display.clear()
                for msg in self.chat_history:
                    prefix = "You" if msg["role"] == "user" else "AI"
                    self.chat_display.append(f"{prefix}: {msg['content']}")
                notify_success(self, "Chat history loaded!")
            except Exception as e:
                notify_error(self, str(e), title="Load Error")

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.chat_display.append(f"[Image uploaded: {file_path}]")
            try:
                text = pytesseract.image_to_string(Image.open(file_path))
                self.chat_display.append(f"[Extracted Text]: {text.strip()}")
            except Exception as e:
                self.chat_display.append(f"[Error reading image: {e}]")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = AIAssistant()
    assistant.show()
    sys.exit(app.exec_())
