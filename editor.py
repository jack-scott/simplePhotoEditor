#!/usr/bin/python3

#TODO make this platform independant

import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QFileDialog, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap, QKeyEvent

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.mModified = True
        self.mUpdate = False
        self.initUI()
        self.pixmap = QPixmap(self.size())  #this creates the default pixmap to be painted
        self.pixmap.fill(Qt.transparent)    

    def initUI(self):
        self.resize(500, 500)
        self.move(2000, 300)    #this decides where the widget is spawned
        self.setWindowTitle('Editor')

        btn = QPushButton('Import Image', self)     #push button for importing an image, would probably be nicer as a dropdown menu
        btn.clicked.connect(self.importButton)
        btn.setToolTip("Press this button to import an image")
        btn.move(10, 10)
        self.show()

    def importButton(self):
        print("You pressed the button")
        filename = self.openFileNameDialog()
        if filename:
            print(filename)
            self.pixmap = QPixmap(filename)     #load whatever filename as the pixmap
            self.mModified = True       #by setting this true the screen will be resized for the widget

    def paintEvent(self, event):    #this is a callbakc which is constantly called to paint the background
        if self.mModified:      #checks if we need to resize, could probably go elsewhere
            print("Painting")
            self.resize(self.pixmap.width(), self.pixmap.height())
            self.mModified = False
        painter = QPainter(self)    #creates a new painter for the widget
        painter.drawPixmap(0, 0, self.pixmap)       #paints the most recent pixmap onto the widget

    def openFileNameDialog(self):   #source https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()     #enumerated options in base 16. For displaying the file explorer
        options |= QFileDialog.DontUseNativeDialog      #native dialog is used by default, this turns it off
        title = "Choose an image"
        startFolder = "" # "" chooses the last folder you were in
        fileFilter = "Images (*.png *.xpm .jpg)"
        fileName, _ = QFileDialog.getOpenFileName(self, title, startFolder, fileFilter, options=options)
        return fileName

    def keyPressEvent(self, event):     #just a test piece of code for working out how to register keystrokes
        gey = event.key()
        self.func = (None, None)
        if gey == Qt.Key_M:
            print("Key 'm' pressed!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    
    