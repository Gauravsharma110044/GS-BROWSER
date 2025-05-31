import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application icon
    app_icon = QIcon("icons/app_icon.png")
    app.setWindowIcon(app_icon)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 