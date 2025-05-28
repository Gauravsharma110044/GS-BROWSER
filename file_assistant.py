import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import docx
import PyPDF2

class FileAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Assistant")
        self.file_path = None
        self.file_content = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel("Upload a PDF, DOCX, or TXT file and ask questions or summarize.")
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        self.summarize_button = QPushButton("Summarize File (AI)")
        self.summarize_button.clicked.connect(self.summarize_file)
        self.summarize_button.setEnabled(False)
        # Q&A section
        self.question_label = QLabel("Ask a question about the file:")
        self.question_input = QTextEdit()
        self.question_input.setFixedHeight(40)
        self.ask_button = QPushButton("Ask AI")
        self.ask_button.clicked.connect(self.ask_question)
        self.ask_button.setEnabled(False)
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setFixedHeight(80)
        layout.addWidget(self.info_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.content_display)
        layout.addWidget(self.summarize_button)
        layout.addWidget(self.question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(self.ask_button)
        layout.addWidget(QLabel("AI Answer:"))
        layout.addWidget(self.answer_display)
        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Documents (*.pdf *.docx *.txt)")
        if file_path:
            self.file_path = file_path
            ext = os.path.splitext(file_path)[1].lower()
            try:
                if ext == ".pdf":
                    self.file_content = self.read_pdf(file_path)
                elif ext == ".docx":
                    self.file_content = self.read_docx(file_path)
                elif ext == ".txt":
                    self.file_content = self.read_txt(file_path)
                else:
                    self.file_content = "Unsupported file type."
                self.content_display.setText(self.file_content[:5000])
                self.summarize_button.setEnabled(True)
                self.ask_button.setEnabled(True)
            except Exception as e:
                self.content_display.setText(f"Error reading file: {e}")
                self.summarize_button.setEnabled(False)
                self.ask_button.setEnabled(False)

    def read_pdf(self, path):
        text = ""
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    def read_docx(self, path):
        doc = docx.Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def read_txt(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    def summarize_file(self):
        import openai
        import os
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Summarize the following file content:\n\n{self.file_content[:3000]}"
        self.content_display.append("\n[AI is summarizing...]")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            summary = response.choices[0].message['content'].strip()
            self.content_display.append(f"\n[AI Summary]: {summary}")
        except Exception as e:
            self.content_display.append(f"\n[Error]: {e}")

    def ask_question(self):
        import openai
        import os
        openai.api_key = os.getenv("OPENAI_API_KEY")
        question = self.question_input.toPlainText().strip()
        if not question:
            self.answer_display.setText("Please enter a question.")
            return
        prompt = f"Answer the following question based on this file content:\n\nFile Content:\n{self.file_content[:3000]}\n\nQuestion: {question}"
        self.answer_display.setText("AI is thinking...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message['content'].strip()
            self.answer_display.setText(answer)
        except Exception as e:
            self.answer_display.setText(f"[Error]: {e}")
