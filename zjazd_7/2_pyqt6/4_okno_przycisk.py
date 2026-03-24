from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton
from PyQt6.QtCore import QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Moja aplikacja')
        button = QPushButton('przycisk')
        button.clicked.connect(self.button_clicked)
        button.released.connect(self.button_released)
        self.setFixedSize(QSize(600, 200))
        self.setCentralWidget(button)

    def button_clicked(self):
        print('Wciśnięty')

    def button_released(self):
        print('Puszczony')

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()