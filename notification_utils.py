from PyQt5.QtWidgets import QMessageBox

def notify_info(parent, message, title="Info"):
    QMessageBox.information(parent, title, message)

def notify_error(parent, message, title="Error"):
    QMessageBox.critical(parent, title, message)

def notify_success(parent, message, title="Success"):
    QMessageBox.information(parent, title, message)
