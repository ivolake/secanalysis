from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import sys
import os
import pandas as pd


class Form(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        tab = QTabWidget()
        first = QWidget()
        second = QWidget()
        third = QWidget()

        tab.addTab(first, 'Main Menu')
        tab.addTab(second, 'Tables')
        tab.addTab(third, 'Graphics')

        button = QPushButton('Выбрать конфиги', first)
        button.setGeometry(10, 100, 120, 20)
        button.clicked.connect(self.Choose_Folders)

        self.textedit = QLabel(first)

        self.textedit.setGeometry(200, 100, 300, 20)

        self.setWindowTitle('Calc1.0')
        self.setCentralWidget(tab)
        self.resize(740, 480)

    def Choose_Folders(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.textedit.setText("Выбрали папку: {}".format(dirlist))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec())

