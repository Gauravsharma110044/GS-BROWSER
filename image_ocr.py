from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract

class ImageOCR(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image & OCR Tools")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.info_label = QLabel("Upload an image to extract text (OCR).")
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.ocr_result = QTextEdit()
        self.ocr_result.setReadOnly(True)
        layout.addWidget(self.info_label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.image_label)
        layout.addWidget(QLabel("Extracted Text (OCR):"))
        layout.addWidget(self.ocr_result)
        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))
            try:
                text = pytesseract.image_to_string(Image.open(file_path))
                self.ocr_result.setText(text.strip())
            except Exception as e:
                self.ocr_result.setText(f"[Error reading image: {e}]")
