import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel('moja labelka')
        self.setCentralWidget(self.label)

    def mouseMoveEvent(self, a0):
        self.label.setText('ruch')

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.label.setText("nacisnieto lewy")

        elif e.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("nacisnieto srodkowy")

        elif e.button() == Qt.MouseButton.RightButton:
            self.label.setText("nacisnieto prawy")

    def mouseReleaseEvent(self, a0):
        self.label.setText("mysz puszczona")
        print('Mysz puszczona')

    def mouseDoubleClickEvent(self, a0):
        self.label.setText("Kliknieto 2 razy")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()