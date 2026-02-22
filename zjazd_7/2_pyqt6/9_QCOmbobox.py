import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QComboBox

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        widget = QComboBox()
        widget.addItems(['Raz','Dwa','Trzy'])
        widget.currentIndexChanged.connect(self.index_change)
        widget.currentTextChanged.connect(self.text_changed)
        self.setCentralWidget(widget)

    def index_change(self, i):
        print(i)

    def text_changed(self, s):
        print(s)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()