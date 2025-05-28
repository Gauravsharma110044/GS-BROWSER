import os
import openai
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel

class VoiceAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Assistant")
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.init_ui()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def init_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel("Click 'Record' and speak. The AI will transcribe and reply with voice.")
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record_voice)
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.info_label)
        layout.addWidget(self.record_button)
        layout.addWidget(QLabel("Transcript and AI Response:"))
        layout.addWidget(self.text_display)
        self.setLayout(layout)

    def record_voice(self):
        self.text_display.append("Listening...")
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source, phrase_time_limit=8)
        try:
            user_text = self.recognizer.recognize_google(audio)
            self.text_display.append(f"You: {user_text}")
            self.text_display.append("AI is thinking...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_text}]
            )
            ai_reply = response.choices[0].message['content'].strip()
            self.text_display.append(f"AI: {ai_reply}\n")
            self.speak(ai_reply)
        except Exception as e:
            self.text_display.append(f"[Error]: {e}\n")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
