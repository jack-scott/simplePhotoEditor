#!/usr/bin/python3

#TODO make this platform independant

import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QFileDialog, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        self.move(2000, 300)
        self.setWindowTitle('Editor')
        
        self.imageLabel = QLabel(self)
        pixmap = QPixmap('/home/jack/Pictures/3121study.png')
        self.imageLabel.setPixmap(pixmap)
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.imageLabel.setScaledContents(True)

        btn = QPushButton('Import Image', self)
        btn.clicked.connect(self.importButton)
        btn.setToolTip("Press this button to import an image")
        btn.move(10, 10)
        self.show()

    def importButton(self):
        print("You pressed the button")
        filename = self.openFileNameDialog()
        if filename:
            print(filename)
            pixmap = QPixmap(filename)
            self.imageLabel.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())

    # def paintEvent(self, filename):
    #     painter = QPainter(self)
    #     # im = QImage(filename)


    def openFileNameDialog(self):   #source https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()     #enumerated options in base 16. For displaying the file explorer
        options |= QFileDialog.DontUseNativeDialog      #native dialog is used by default, this turns it off
        title = "Choose an image"
        startFolder = "" # "" chooses the last folder you were in
        fileFilter = "Images (*.png *.xpm .jpg)"
        fileName, _ = QFileDialog.getOpenFileName(self, title, startFolder, fileFilter, options=options)
        return fileName

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    
    