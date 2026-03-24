from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton
from PyQt6.QtCore import QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Moja aplikacja')
        button = QPushButton('przycisk')
        self.setFixedSize(QSize(600, 200))
        self.setCentralWidget(button)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()