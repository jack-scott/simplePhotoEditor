#!/usr/bin/python2.7    

#TODO make this platform independant

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip

def buttonFunction():
    print "You pressed the button"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()

    btn = QPushButton('Import Image', w)
    btn.clicked.connect(buttonFunction)
    btn.setToolTip("Press this button to import an image")
    btn.move(10, 10)

    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Editor')
    w.show()
    
    sys.exit(app.exec_())