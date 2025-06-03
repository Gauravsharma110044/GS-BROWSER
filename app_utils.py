from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt

def show_info(parent, title, message):
    QMessageBox.information(parent, title, message)

def show_error(parent, title, message):
    QMessageBox.critical(parent, title, message)

def show_loading(parent, label="Loading...", minimum=0, maximum=0):
    dlg = QProgressDialog(label, None, minimum, maximum, parent)
    dlg.setWindowModality(Qt.WindowModal)
    dlg.setCancelButton(None)
    dlg.setMinimumDuration(0)
    dlg.show()
    return dlg
