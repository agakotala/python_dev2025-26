from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton
from PyQt6.QtCore import QSize
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Moja aplikacja')
        button = QPushButton('przycisk')
        button.setCheckable(True)
        button.clicked.connect(self.button_clicked)
        button.clicked.connect(self.button_toggle)
        self.setFixedSize(QSize(400, 200))
        self.setCentralWidget(button)

    def button_clicked(self):
        print('Wciśnięty')

    def button_toggle(self, checked):
        print('Stan przycisku: ',checked)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()