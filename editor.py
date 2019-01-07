#!/usr/bin/python3   

#TODO make this platform independant

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QFileDialog

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        btn = QPushButton('Import Image', self)
        btn.clicked.connect(self.buttonFunction)
        btn.setToolTip("Press this button to import an image")
        btn.move(10, 10)

        self.resize(250, 150)
        self.move(300, 300)
        self.setWindowTitle('Editor')

        self.show()

    def buttonFunction(self):
        print("You pressed the button")
        self.openFileNameDialog()

    def openFileNameDialog(self):   #source https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()     #enumerated options in base 16. For displaying the file explorer
        options |= QFileDialog.DontUseNativeDialog      #native dialog is used by default, this turns it off
        title = "Choose an image"
        startFolder = "" # "" chooses the last folder you were in
        fileFilter = "Images (*.png *.xpm .jpg)"
        fileName, _ = QFileDialog.getOpenFileName(self, title, startFolder, fileFilter, options=options)
        if fileName:
            print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    
    