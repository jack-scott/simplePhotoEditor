#!/usr/bin/python3

#TODO add file saving
#TODO make this platform independant
#TODO Set a translucent rectangle to define the boundary of the area to crop

import sys
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QFileDialog, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QImage, QPaintEvent, QPixmap, QKeyEvent, QTransform

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.toolbarH = 50
        self.toolbarCent = 10
        self.initUI()
        self.pixmap = QPixmap(self.size())  #this creates the default pixmap to be painted
        self.pixmap.fill(Qt.transparent) 
        self.transform = QTransform()
        self.clickOn = False
        self.initYPos = 0
        self.initXPos = 0
        self.totalRotation = 0
        self.zoomLevel = 0
        self.editingMode = "rotate"
        self.filename = ""

    def initUI(self):
        self.resize(500, 500)
        self.move(2000, 300)    #this decides where the widget is spawned
        self.setWindowTitle('Editor')
        btn1 = QPushButton('Import', self)     #push button for importing an image, would probably be nicer as a dropdown menu
        btn1.clicked.connect(self.importButton)
        btn1.setToolTip("Press this button to import an image")
        btn1.move(10, self.toolbarCent)

        btn2 = QPushButton('Rotate', self)     #push button for changin editting mode, would probably be nicer as a dropdown menu
        btn2.clicked.connect(lambda: self.changeEditingMode("rotate"))
        btn2.setToolTip("Press this button to allow rotation")
        btn2.move(110, self.toolbarCent)

        btn3 = QPushButton('Translate', self)     #push button for changin editting mode, would probably be nicer as a dropdown menu
        btn3.clicked.connect(lambda: self.changeEditingMode("translate"))
        btn3.setToolTip("Press this button to allow dragging")
        btn3.move(210, self.toolbarCent)

        btn4 = QPushButton('Save', self)     #push button for saving image
        btn4.clicked.connect(self.saveImage)
        btn4.setToolTip("Press this button to save image")
        btn4.move(310, self.toolbarCent)

        self.show()

    def importButton(self):
        print("You pressed the button")
        filename = self.openFileNameDialog()
        if filename:
            print(filename)
            self.filename = filename
            self.pixmap = QPixmap(filename)     #load whatever filename as the pixmap
            self.transform = QTransform()
            self.resize(self.pixmap.width(), self.pixmap.height() + self.toolbarH)
            self.totalRotation = 0
            self.update()

    def changeEditingMode(self, newMode):
        self.editingMode = newMode
        print(newMode)

    def paintEvent(self, event):    #this is a callbakc which is constantly called to paint the background
        print("PaintEvent")
        painter = QPainter(self)    #creates a new painter for the widget
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        # painter.rotate(self.rotation)
        painter.setTransform(self.transform)
        painter.drawPixmap(0, self.toolbarH, self.pixmap)       #paints the most recent pixmap onto the widget

    def openFileNameDialog(self):   #source https://pythonspot.com/pyqt5-file-dialog/
        options = QFileDialog.Options()     #enumerated options in base 16. For displaying the file explorer
        options |= QFileDialog.DontUseNativeDialog      #native dialog is used by default, this turns it off
        title = "Choose an image"
        startFolder = "/home/jack/Pictures/" # "" chooses the last folder you were in
        fileFilter = "Images (*.png *.xpm .jpg)"
        fileName, _ = QFileDialog.getOpenFileName(self, title, startFolder, fileFilter, options=options)
        return fileName

    def keyPressEvent(self, event):     #just a test QPainter.SmoothPixmapTransform, True piece of code for working out how to register keystrokes
        getKey = event.key()
        print(getKey)
        if getKey == 44:
            print("Key up pressed!")
            self.rotatePixmap(1)
            self.update()
        
        if getKey == 46:
            print("Key down pressed!")
            self.rotatePixmap(-1)
            self.update()
    
    def wheelEvent(self, event):
        scaleWheel = event.angleDelta()
        if scaleWheel.y() > 0:
            scaleFactor = 0.1
        else:
            scaleFactor = -0.1
        scaleVal = 1 +  scaleFactor
        print("Scaling by: " + str(scaleVal))
        self.scalePixmap(scaleVal)
        self.update()

    def mouseMoveEvent(self, event):
        if self.clickOn:
            yPos = event.y()
            xPos = event.x()
            if self.editingMode == "rotate":
                posDiff = yPos - self.initYPos
                if abs(posDiff) > 1:
                    rotation = posDiff 
                    self.initYPos = yPos
                    self.rotatePixmap(rotation)
                    self.update()
            
            if self.editingMode == "translate":
                posDiff = abs(yPos - self.initYPos) + abs(xPos - self.initXPos)
                if posDiff > 1:
                    xOffset = xPos - self.initXPos
                    yOffset = yPos - self.initYPos
                    self.initXPos = xPos
                    self.initYPos = yPos
                    self.translatePixmap(xOffset, yOffset)
                    self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickOn = True
            self.initYPos = event.y()
            self.initXPos = event.x()
            print('press')

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clickOn = False
            print('release')

    def rotatePixmap(self, angle):
        self.totalRotation += angle
        print(self.totalRotation)
        self.transform.translate(self.pixmap.width()/2,self.pixmap.height()/2)
        self.transform.rotate(angle)
        self.transform.translate(-self.pixmap.width()/2, -self.pixmap.height()/2)

    def scalePixmap(self, scale):
        self.transform.translate(self.pixmap.width()/2,self.pixmap.height()/2)
        self.transform.scale(scale, scale)
        self.transform.translate(-self.pixmap.width()/2, -self.pixmap.height()/2)

    def translatePixmap(self, xOffset, yOffset):
        self.transform.translate(self.pixmap.width()/2,self.pixmap.height()/2)
        self.transform.rotate(-self.totalRotation)
        self.transform.translate(xOffset, yOffset)
        self.transform.rotate(self.totalRotation)
        self.transform.translate(-self.pixmap.width()/2, -self.pixmap.height()/2)

    def saveImage(self):
        screen = QApplication.primaryScreen()
        grab = screen.grabWindow(self.winId())
        print("Saving image")
        parsedFname = self.filename.split(".")
        grab.save(parsedFname[0] + '_edit.png', 'png')  #might want to save in origional filetype?

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

    
    