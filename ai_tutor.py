from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
import os
import google.generativeai as genai
from dotenv import load_dotenv

class AITutor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Personal Tutor")
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("AI Personal Tutor")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #3b7ddd;")
        layout.addWidget(title)

        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["Physics", "Chemistry", "Math"])
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_combo)
        layout.addLayout(subject_layout)


        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("Ask your question or enter a topic...")
        self.question_input.setFixedHeight(60)
        self.ask_btn = QPushButton("Ask AI")
        self.ask_btn.clicked.connect(self.ask_ai)
        qa_layout = QHBoxLayout()
        qa_layout.addWidget(self.question_input)
        qa_layout.addWidget(self.ask_btn)
        layout.addLayout(qa_layout)

        self.answer_label = QLabel("Answer will appear here.")
        self.answer_label.setWordWrap(True)
        self.answer_label.setStyleSheet("background: #f0f4fb; border-radius: 8px; padding: 16px; font-size: 1.08rem; color: #222;")
        layout.addWidget(self.answer_label)

        self.quiz_btn = QPushButton("Generate Quiz")
        self.quiz_btn.clicked.connect(self.generate_quiz)
        layout.addWidget(self.quiz_btn)
        self.quiz_display = QTextEdit()
        self.quiz_display.setReadOnly(True)
        self.quiz_display.setStyleSheet("background: #f0f4fb; border-radius: 8px; padding: 12px; margin-bottom: 10px;")
        layout.addWidget(self.quiz_display)

        self.setLayout(layout)

    def ask_ai(self):
        subject = self.subject_combo.currentText()
        question = self.question_input.toPlainText().strip()
        if not question:
            self.answer_label.setText("Please enter a question or topic.")
            return
        self.answer_label.setText("AI is thinking...")
        try:
            prompt = f"Explain the following {subject} concept or question for IIT JEE in detail with examples and step-by-step reasoning: {question}"
            model = genai.GenerativeModel('gemini-pro')
            convo = model.start_chat(history=[])
            convo.send_message(prompt)
            answer = convo.last.text.strip()
            self.answer_label.setText(answer)
        except Exception as e:
            self.answer_label.setText(f"[Error]: {e}")

    def generate_quiz(self):
        subject = self.subject_combo.currentText()
        self.quiz_display.setText("Generating quiz...")
        try:
            prompt = f"Generate 5 multiple-choice questions with 4 options and answers for {subject} at IIT JEE level. Format as JSON."
            model = genai.GenerativeModel('gemini-pro')
            convo = model.start_chat(history=[])
            convo.send_message(prompt)
            answer = convo.last.text.strip()
            import json
            try:
                quiz = json.loads(answer)
                quiz_text = ''
                for i, q in enumerate(quiz):
                    quiz_text += f"Q{i+1}: {q['question']}\n"
                    for opt in q['options']:
                        quiz_text += f"   - {opt}\n"
                    quiz_text += f"Answer: {q['answer']}\n\n"
                self.quiz_display.setText(quiz_text)
            except Exception:
                self.quiz_display.setText(answer)
        except Exception as e:
            self.quiz_display.setText(f"[Error]: {e}")
