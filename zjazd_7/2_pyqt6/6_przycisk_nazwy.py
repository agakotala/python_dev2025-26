from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt6.QtCore import QSize
import sys
from random import choice

window_titles = [
    'Moja apka',
    'Moja apka',
    'Dalej to samo',
    'Dalej to samo',
    'Ziemia',
    'Ziemia',
    'Tytul',
    'Tytul',
    'BLAD!'
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Moja aplikacja")
        self.button = QPushButton("przycisk")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)
        self.windowTitleChanged.connect(self.wrong_title)
        self.setFixedSize(QSize(600, 200))
        self.setCentralWidget(self.button)

    def button_clicked(self):
        print('Wciśnięty')
        current_title = choice(window_titles)
        print('nowy tytul:', current_title)
        self.setWindowTitle(current_title)

    def wrong_title(self, window_title):
        print('tytul zmieniony na ', window_title)
        if window_title == 'BLAD!':
            self.button.setDisabled(True)
            self.button.setText('NOOO')


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
